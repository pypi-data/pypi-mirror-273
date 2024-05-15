import torch
import numpy as np
from scipy.ndimage import _ni_support, binary_erosion, distance_transform_edt, generate_binary_structure
import sklearn.metrics as skmetrics

def _surface_distances(y_pred, y, voxelspacing=None, connectivity=1):
    """
    计算两个二值对象中表面体素之间的距离
    """
    y_pred = np.atleast_1d(y_pred.astype(np.bool_))
    y = np.atleast_1d(y.astype(np.bool_))
    if voxelspacing is not None:
        voxelspacing = _ni_support._normalize_sequence(voxelspacing, y_pred.ndim)
        voxelspacing = np.asarray(voxelspacing, dtype=np.float64)
        if not voxelspacing.flags.contiguous:
            voxelspacing = voxelspacing.copy()

    # binary structure
    footprint = generate_binary_structure(y_pred.ndim, connectivity)

    # test for emptiness
    if 0 == np.count_nonzero(y_pred):
        raise RuntimeError(
            "The first supplied array does not contain any binary object."
        )
    if 0 == np.count_nonzero(y):
        raise RuntimeError(
            "The second supplied array does not contain any binary object."
        )
    result_border = y_pred ^ binary_erosion(y_pred, structure=footprint, iterations=1)
    reference_border = y ^ binary_erosion(
        y, structure=footprint, iterations=1
    )
    dt = distance_transform_edt(~reference_border, sampling=voxelspacing)
    sds = dt[result_border]

    return sds

def hd(y_pred, y, voxelspacing=None, connectivity=1):
    """
    Hausdorff Distance.
    Hausdorff距离衡量了两个点集之间的最大不匹配程度。在此函数中，它用于计算两个二值图像（result和reference）的表面体素之间的最大不匹配距离。

    Args:
        y_pred (array_like): 预测的二值图像，形状与参考图像（y）相同。
        y (array_like): 参考的二值图像，形状与预测图像（y_pred）相同。
        voxelspacing (array_like, optional): 形状为（N，）的数组，表示每个维度上的体素间距。默认为None。
        connectivity (int, optional): 表面距离计算中使用的连接性。默认为1，表示3D中的26连通（在3D情况下）或2D中的8连通（在2D情况下）。

    Returns:
        float: Hausdorff距离，即两个图像表面体素之间的最大不匹配距离。
    """
    hd1 = _surface_distances(y_pred, y, voxelspacing, connectivity).max()
    hd2 = _surface_distances(y, y_pred, voxelspacing, connectivity).max()
    hausdorff = max(hd1, hd2)
    return hausdorff

def hd95(y_pred, y, voxelspacing=None, connectivity=1):
    """
    计算 Hausdorff 距离的 95% 的数据点的值
    """
    hausdorff = hd(y_pred, y, voxelspacing, connectivity)
    return np.percentile(hausdorff, 95)

def ignore_background(y_pred, y):
    """
    Used to remove the background (first channel) of "yyred" and "y".
    Args:
        y_pred: predictions. As for classification tasks, `y_pred` should has the shape [BN] where N is larger than 1. As for segmentation tasks,
        the shape should be [BNHW] or [BNHWD].
        y: ground truth, the first dim is batch.
    """
    y = y[:, 1:] if y.shape[1] > 1 else y
    y_pred = y_pred[:, 1:] if y_pred.shape[1] > 1 else y_pred
    return y_pred, y

def do_metric_reduction(f, reduction='mean'):
    """
    This function is to do the metric reduction for calculated `not-nan` metrics of each sample's each class.
    The function also returns `not_nans`, which counts the number of not nans for the metric.

    Args:
        f: a tensor that contains the calculated metric scores per batch and
            per class. The first two dims should be batch and class.
        reduction: define the mode to reduce metrics, will only apply reduction on `not-nan` values,
            available reduction modes: {``"none"``, ``"mean"``, ``"sum"``, ``"mean_batch"``, ``"sum_batch"``,
            ``"mean_channel"``, ``"sum_channel"``}, default to ``"mean"``.
            if "none", return the input f tensor and not_nans.

    Raises:
        ValueError: When ``reduction`` is not one of
            ["mean", "sum", "mean_batch", "sum_batch", "mean_channel", "sum_channel" "none"].
    """
    # some elements might be Nan (if ground truth y was missing (zeros))
    # we need to account for it
    nans = torch.isnan(f)
    not_nans = (~nans).float()

    t_zero = torch.zeros(1, device=f.device, dtype=f.dtype)
    if reduction == 'none':
        return f, not_nans

    f[nans] = 0
    if reduction == 'mean':
        # 2 steps, first, mean by channel (accounting for nans), then by batch
        not_nans = not_nans.sum(dim=1)
        f = torch.where(not_nans > 0, f.sum(dim=1) / not_nans, t_zero)  # channel average

        not_nans = (not_nans > 0).float().sum(dim=0)
        f = torch.where(not_nans > 0, f.sum(dim=0) / not_nans, t_zero)  # batch average

    elif reduction == 'sum':
        not_nans = not_nans.sum(dim=[0, 1])
        f = torch.sum(f, dim=[0, 1])  # sum over the batch and channel dims
    elif reduction == 'mean_batch':
        not_nans = not_nans.sum(dim=0)
        f = torch.where(not_nans > 0, f.sum(dim=0) / not_nans, t_zero)  # batch average
    elif reduction == 'sum_batch':
        not_nans = not_nans.sum(dim=0)
        f = f.sum(dim=0)  # the batch sum
    elif reduction == 'mean_channel':
        not_nans = not_nans.sum(dim=1)
        f = torch.where(not_nans > 0, f.sum(dim=1) / not_nans, t_zero)  # channel average
    elif reduction == 'sum_channel':
        not_nans = not_nans.sum(dim=1)
        f = f.sum(dim=1)  # the channel sum
    elif reduction != 'none':
        raise ValueError(
            f"Unsupported reduction: {reduction}, available options are "
            '["mean", "sum", "mean_batch", "sum_batch", "mean_channel", "sum_channel" "none"].'
        )
    return f, not_nans

def calculate_area(pred, label, num_classes, ignore_index=256):
    """
    Calculate intersect, prediction and label area

    Args:
        pred (Tensor): The prediction by model.
        label (Tensor): The ground truth of image.
        num_classes (int): The unique number of target classes.
        ignore_index (int): Specifies a target value that is ignored. Default: 256.

    Returns:
        Tensor: The intersection area of prediction and the ground on all class.
        Tensor: The prediction area on all class.
        Tensor: The ground truth area on all class
    """
    if len(pred.shape) == 4:
        pred = pred.squeeze(1)
    if len(label.shape) == 4:
        label = label.squeeze(1)
    if not pred.shape == label.shape:
        raise ValueError('Shape of `pred` and `label should be equal, '
                         'but there are {} and {}.'.format(pred.shape,
                                                           label.shape))
    pred_area = []
    label_area = []
    intersect_area = []
    mask = label != ignore_index

    for i in range(num_classes):
        pred_i = (pred == i) & mask
        label_i = label == i
        intersect_i = pred_i & label_i
        pred_area.append(pred_i.int().sum())
        label_area.append(label_i.int().sum())
        intersect_area.append(intersect_i.int().sum())

    pred_area = torch.cat(pred_area)
    label_area = torch.cat(label_area)
    intersect_area = torch.cat(intersect_area)

    return intersect_area, pred_area, label_area


def auc_roc(logits, label, num_classes, ignore_index=None):
    """
    Calculate area under the roc curve

    Args:
        logits (Tensor): The prediction by model on testset, of shape (N,C,H,W) .
        label (Tensor): The ground truth of image.   (N,1,H,W)
        num_classes (int): The unique number of target classes.
        ignore_index (int): Specifies a target value that is ignored. Default: 255.

    Returns:
        auc_roc(float): The area under roc curve
    """
    if ignore_index or len(np.unique(label)) > num_classes:
        raise RuntimeError('labels with ignore_index is not supported yet.')

    if len(label.shape) != 4:
        raise ValueError(
            'The shape of label is not 4 dimension as (N, C, H, W), it is {}'.
                format(label.shape))

    if len(logits.shape) != 4:
        raise ValueError(
            'The shape of logits is not 4 dimension as (N, C, H, W), it is {}'.
                format(logits.shape))

    N, C, H, W = logits.shape
    logits = np.transpose(logits, (1, 0, 2, 3))
    logits = logits.reshape([C, N * H * W]).transpose([1, 0])

    label = np.transpose(label, (1, 0, 2, 3))
    label = label.reshape([1, N * H * W]).squeeze()

    if not logits.shape[0] == label.shape[0]:
        raise ValueError('length of `logit` and `label` should be equal, '
                         'but they are {} and {}.'.format(logits.shape[0],
                                                          label.shape[0]))

    if num_classes == 2:
        auc = skmetrics.roc_auc_score(label, logits[:, 1])
    else:
        auc = skmetrics.roc_auc_score(label, logits, multi_class='ovr')

    return auc


def mean_iou(intersect_area, pred_area, label_area):
    """
    Calculate iou.

    Args:
        intersect_area (Tensor): The intersection area of prediction and ground truth on all classes.
        pred_area (Tensor): The prediction area on all classes.
        label_area (Tensor): The ground truth area on all classes.

    Returns:
        np.ndarray: iou on all classes.
        float: mean iou of all classes.
    """
    intersect_area = intersect_area.numpy()
    pred_area = pred_area.numpy()
    label_area = label_area.numpy()
    union = pred_area + label_area - intersect_area
    class_iou = []
    for i in range(len(intersect_area)):
        if union[i] == 0:
            iou = 0
        else:
            iou = intersect_area[i] / union[i]
        class_iou.append(iou)
    miou = np.mean(class_iou)
    return np.array(class_iou), miou


def dice(intersect_area, pred_area, label_area):
    """
    Calculate DICE.

    Args:
        intersect_area (Tensor): The intersection area of prediction and ground truth on all classes.
        pred_area (Tensor): The prediction area on all classes.
        label_area (Tensor): The ground truth area on all classes.

    Returns:
        np.ndarray: DICE on all classes.
        float: mean DICE of all classes.
    """
    intersect_area = intersect_area.numpy()
    pred_area = pred_area.numpy()
    label_area = label_area.numpy()
    union = pred_area + label_area
    class_dice = []
    for i in range(len(intersect_area)):
        if union[i] == 0:
            dice = 0
        else:
            dice = (2 * intersect_area[i]) / union[i]
        class_dice.append(dice)
    mdice = np.mean(class_dice)
    return np.array(class_dice), mdice


def accuracy(intersect_area, pred_area):
    """
    Calculate accuracy

    Args:
        intersect_area (Tensor): The intersection area of prediction and ground truth on all classes..
        pred_area (Tensor): The prediction area on all classes.

    Returns:
        np.ndarray: accuracy on all classes.
        float: mean accuracy.
    """
    intersect_area = intersect_area.numpy()
    pred_area = pred_area.numpy()
    class_acc = []
    for i in range(len(intersect_area)):
        if pred_area[i] == 0:
            acc = 0
        else:
            acc = intersect_area[i] / pred_area[i]
        class_acc.append(acc)
    macc = np.sum(intersect_area) / np.sum(pred_area)
    return np.array(class_acc), macc


def kappa(intersect_area, pred_area, label_area):
    """
    Calculate kappa coefficient

    Args:
        intersect_area (Tensor): The intersection area of prediction and ground truth on all classes..
        pred_area (Tensor): The prediction area on all classes.
        label_area (Tensor): The ground truth area on all classes.

    Returns:
        float: kappa coefficient.
    """
    intersect_area = intersect_area.numpy()
    pred_area = pred_area.numpy()
    label_area = label_area.numpy()
    total_area = np.sum(label_area)
    po = np.sum(intersect_area) / total_area
    pe = np.sum(pred_area * label_area) / (total_area * total_area)
    kappa = (po - pe) / (1 - pe)
    return kappa

if __name__=="__main__":
    y_pred = np.random.randint(0, 3, size=(100, 100))
    y = np.random.randint(0, 3, size=(100, 100))
    hausdorff_distance = hd95(y_pred, y)
    print("Hausdorff Distance:", hausdorff_distance)

    batch_size = 1
    num_channels = 3
    depth = 2
    height = 2
    width = 2

    y_pred = torch.rand(batch_size, num_channels, depth, height, width)
    y_true = torch.rand(batch_size, num_channels, depth, height, width)
    print("Shape of y_pred:", y_pred.shape)
    print("Shape of y_true:", y_true.shape)