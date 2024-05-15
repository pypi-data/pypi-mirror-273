from typing import Tuple
import logging

import torch
import pyro


def calculate_multiquestion_loss(labels: torch.Tensor, predictions: torch.Tensor, question_index_groups: Tuple, careful=True) -> torch.Tensor:
    """
    The full decision tree loss used for training GZ DECaLS models

    Negative log likelihood of observing ``labels`` (volunteer answers to all questions)
    from Dirichlet-Multinomial distributions for each question, using concentrations ``predictions``.
    
    Args:
        labels (torch.Tensor): (galaxy, k successes) where k successes dimension is indexed by question_index_groups.
        predictions (torch.Tensor):  Dirichlet concentrations, matching shape of labels
        question_index_groups (list): Answer indices for each question i.e. [(question.start_index, question.end_index), ...] for all questions. Useful for slicing model predictions by question. See :ref:`schemas`.
    
    Returns:
        torch.Tensor: neg. log likelihood of shape (batch, question).
    """
    if careful:
        # some models give occasional nans for all predictions on a specific galaxy/row
        # these are inputs to the loss and only happen many epochs in so probably not a case of bad labels, but rather some instability during training
        # handle this by setting loss=0 for those rows and throwing a warning
        nan_prediction = torch.isnan(predictions) | torch.isinf(predictions)
        if nan_prediction.any():
            logging.warning(f'Found nan values in predictions: {predictions}')
        safety_value = torch.ones(1, device=predictions.device, dtype=predictions.dtype)  # fill with 1 everywhere i.e. fully uncertain
        predictions = torch.where(condition=nan_prediction, input=safety_value, other=predictions)

    # very important that question_index_groups is fixed and discrete, else tf.function autograph will mess up 
    q_losses = []
    # will give shape errors if model output dim is not labels dim, which can happen if losses.py substrings are missing an answer
    for q_n in range(len(question_index_groups)):
        q_indices = question_index_groups[q_n]
        q_start = q_indices[0]
        q_end = q_indices[1]
        q_loss = dirichlet_loss(labels[:, q_start:q_end+1], predictions[:, q_start:q_end+1])

        q_losses.append(q_loss)
    
    total_loss = torch.stack(q_losses, axis=1)

    return total_loss  # leave the reduction to pytorch lightning


def dirichlet_loss(labels_for_q, concentrations_for_q):
    """
    Negative log likelihood of ``labels_for_q`` being drawn from Dirichlet-Multinomial distribution with ``concentrations_for_q`` concentrations.
    This loss is for one question. Sum over multiple questions if needed (assumes independent).
    Applied by :meth:`calculate_multiquestion_loss`, above.

    Args:
        labels_for_q (tf.constant): observed labels (count of volunteer responses) of shape (batch, answer)
        concentrations_for_q (tf.constant): concentrations for multinomial-dirichlet predicting the observed labels, of shape (batch, answer)

    Returns:
        tf.constant: negative log. prob per galaxy, of shape (batch_dim).
    """
    # if you get a dimension mismatch here like [16, 2] vs. [64, 2], for example, check --shard-img-size is correct in train_model.py.
    # images may be being reshaped to the wrong expected size e.g. if they are saved as 32x32, but you put --shard-img-size=64,
    # you will get image batches of shape [N/4, 64, 64, 1] and hence have the wrong number of images vs. labels (and meaningless images)
    # so check --shard-img-size carefully!
    total_count = torch.sum(labels_for_q, axis=1)

    # pytorch dirichlet multinomial implementation will not accept zero total votes, need to handle separately
    return get_dirichlet_neg_log_prob(labels_for_q, total_count, concentrations_for_q)


    # # return tf.where(
    # #     tf.math.equal(total_count, 0),  # if total_count is 0 (i.e. no votes)
    # #     tf.constant(0.),  # prob is 1 and (neg) log prob is 0, with no gradients attached. broadcasts
    # #     get_dirichlet_neg_log_prob(labels_for_q, total_count, concentrations_for_q)  # else, calculate neg log prob
    # # )
    # # # slightly inefficient as get_dirichlet_neg_log_prob forward pass done for all, but avoids gradients
    # # # https://www.tensorflow.org/api_docs/python/tf/where
    # # works great, but about 50% slower than optimal

    # logging.info(total_count)

    # indices = torch.arange(0, len(total_count), dtype=torch.long)
    # indices_with_nonzero_counts = indices[total_count > 0]  # returns a tuple for some reason
    #     # torch.equal(total_count, torch.zeros(size=(1,)))

    # logging.info(indices_with_nonzero_counts)
    # # logging.info(type(indices_with_nonzero_counts))
    # # logging.info('Nonzero indices: {}'.format(indices_with_nonzero_counts.cpu().numpy()))
    
    # # may potentially need to deal with the situation where there are 0 valid indices?
    # nonzero_total_count = total_count[indices_with_nonzero_counts]
    # nonzero_labels_for_q = labels_for_q[indices_with_nonzero_counts]
    # nonzero_concentrations_for_q = concentrations_for_q[indices_with_nonzero_counts]

    # logging.info(nonzero_total_count)

    # neg_log_prob_of_indices_with_nonzero_counts = get_dirichlet_neg_log_prob(nonzero_labels_for_q, nonzero_total_count, nonzero_concentrations_for_q)
    # logging.info(neg_log_prob_of_indices_with_nonzero_counts)
    # # logging.info('Probs of nonzero indices: {}'.format(neg_log_prob_of_indices_with_nonzero_counts.numpy()))

    # # not needed, scatter_nd has 0 where no value is placed (and 0 as log prob = 0 as prob = 1)
    # # neg_log_prob_of_indices_with_zero_counts = tf.zeros_like(indices_with_zero_counts)

    # # now mix back together
    # # The backward pass is implemented only for src.shape == index.shape, true in my case (each neg lob prob goes exactly one place)
    # mixed_back = torch.zeros_like(total_count).scatter_(dim=0, index=indices_with_nonzero_counts, src=neg_log_prob_of_indices_with_nonzero_counts)
    # return mixed_back
    # # return tf.scatter_nd(indices_with_nonzero_counts, neg_log_prob_of_indices_with_nonzero_counts, shape=output_shape)


    # # return get_dirichlet_neg_log_prob(labels_for_q, total_count, concentrations_for_q)


def get_dirichlet_neg_log_prob(labels_for_q, total_count, concentrations_for_q):
    # https://docs.pyro.ai/en/stable/distributions.html#dirichletmultinomial
    # .int()s avoid rounding errors causing loss of around 1e-5 for questions with 0 votes
    dist = pyro.distributions.DirichletMultinomial(
        total_count=total_count.int(), concentration=concentrations_for_q, is_sparse=False, validate_args=True)
    return -dist.log_prob(labels_for_q.int())  # important minus sign
