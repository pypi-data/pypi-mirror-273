from typing import Tuple

import torch
from detectools.formats import Format
from torch import Tensor
from torchvision.ops import box_iou


def match_boxes(
    prediction: Format, target: Format, iou_threshold: float = 0.5
) -> Tuple[Tensor, Tensor, Tensor, Tuple[Tensor, Tensor]]:
    """Match better prediction boxes candidates with target boxes. Return indexes of
    prediction and target boxes that match and compute statistics of detection quality (Tp, FP, FN).

    Args:
        prediction (Format): Prediction.
        target (Format): Target.
        iou_threshold (float, optional): IoU threshold to discard some matchs with overlapping < to thr. Defaults to 0.5.

    Returns:
        Tuple[Tensor, Tensor, Tensor, Tuple[Tensor, Tensor]]: Detection statsitics (TP, FN, FN)
        & prediction and target boxes indexes that match well.
    """
    # set box format to XYXY for torch box iou computation
    assert (
        prediction.box_format == target.box_format
    ), f"Predictio and taget should have the same box_format, got {prediction.box_format} & {target.box_format}"
    origin_box_format = prediction.box_format
    prediction.set_boxes_format("XYXY")
    target.set_boxes_format("XYXY")
    # extract boxes
    pred_boxes = prediction.get("boxes")
    target_boxes = target.get("boxes")
    # compute cross matrix of ious
    cross_ious = box_iou(pred_boxes, target_boxes)
    # boolean matrix of max pred iou == max target iou --> true positives candidates
    max_matchs = (
        torch.max(cross_ious, dim=1)[0][..., None]
        == torch.max(cross_ious, dim=0)[0][None, ...]
    ).view(cross_ious.shape)

    # true positive if iou of max_matchs > iou threshold
    tp = torch.sum((max_matchs > 0) & (cross_ious > iou_threshold))
    # false positive: all boxes with no match with targets
    fp = torch.sum(pred_boxes.shape[0] - torch.sum(tp))
    # false negative if target has no pred box with iou > threshold
    fn = torch.sum(torch.max(cross_ious, dim=0)[0] < 0.5)
    # tp pairs index
    pred_idxs, target_idxs = torch.where(
        (max_matchs > 0) & (cross_ious > iou_threshold)
    )
    # extract indexes
    pred_idxs = pred_idxs.tolist() if pred_idxs.nelement() > 0 else []
    target_idxs = target_idxs.tolist() if target_idxs.nelement() > 0 else []
    match_idxs = (torch.tensor(pred_idxs).long(), torch.tensor(target_idxs).long())
    # send back box format to original format
    prediction.set_boxes_format(origin_box_format)
    target.set_boxes_format(origin_box_format)

    return tp, fp, fn, match_idxs


# functionnals metrics
def f1score(tp, fp, tn, fn):
    return (2 * tp) / (2 * tp + fp + fn)


def precision(tp, fp, tn, fn):
    if tp + fp == 0:
        return torch.tensor(torch.nan)
    return (tp) / (tp + fp)


def recall(tp, fp, tn, fn):
    return (tp) / (tp + fn)


def iou(tp: Tensor, fp: Tensor, tn: Tensor, fn: Tensor) -> Tensor:
    """Compute IoU from statistics."""
    return tp / (tp + fp + fn)


def accuracy(tp: Tensor, fp: Tensor, tn: Tensor, fn: Tensor):
    """Compute accuracy from statistics."""
    return (tp + tn) / (tn + tp + fp + fn)
