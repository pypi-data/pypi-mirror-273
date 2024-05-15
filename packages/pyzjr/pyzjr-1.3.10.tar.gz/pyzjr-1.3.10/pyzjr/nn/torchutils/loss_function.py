"""
Copyright (c) 2024, Auorui.
All rights reserved.
time 2024-01-25
"""
import torch
import torch.nn as nn
import torch.nn.functional as F
from pyzjr.nn.torchutils.loss_utils import (
    boundary_loss,
    sigmoid_focal_loss_3d,
    softmax_focal_loss_3d,
)
import warnings

__all__ = ["L1Loss", "L2Loss", "BCELoss", "CrossEntropyLoss", "FocalLoss", "DiceLoss",
           "Joint2loss", "BoundaryLoss", "DiceFocalLoss", "LabelSmoothingCrossEntropy",
           "DiceLoss3D", "FocalLoss3D", "DiceFocalLoss3D"]

class L1Loss(nn.Module):
    """
    L1损失，也称为平均绝对误差（MAE），测量预测输出中的每个元素与目标或地面实况中的相应元素之间的平均绝对差。
    在数学上，它表示为预测值和目标值之间差异的绝对值的平均值。与L2损耗相比，L1损耗对异常值不那么敏感。依据公式实现。
    Args:
        input (torch.Tensor): The predicted output.
        target (torch.Tensor): The target or ground truth.
        reduction (str, optional): Specifies the reduction to apply to the output.
            Options are 'none', 'mean', or 'sum'. Default is 'mean'.
    Examples::
        >>> criterion1 = nn.L1Loss()
        >>> criterion2 = L1Loss()
        >>> input_data=torch.Tensor([2, 3, 4, 5])
        >>> target_data=torch.Tensor([4, 5, 6, 7])
        >>> loss1 = criterion1(input_data, target_data)  # tensor(2.)
        >>> loss2 = criterion2(input_data, target_data)  # tensor(2.)
    Returns:
        torch.Tensor: The L1 loss between input and target.
    """
    def __init__(self):
        super(L1Loss, self).__init__()

    def forward(self, input, target):
        loss = torch.mean(torch.abs(input - target))
        return loss

class L2Loss(nn.Module):
    """
    L2损失，也称为均方误差（MSE），测量预测输出中的每个元素与目标或地面实况中的相应元素之间的平均平方差。
    在数学上，它表示为预测值和目标值之间差异的平方的平均值。相比于L1损耗，L2损耗对异常值更敏感。依据公式实现。
    在torch当中是MSELoss
    Args:
        input (torch.Tensor): The predicted output.
        target (torch.Tensor): The target or ground truth.
        reduction (str, optional): Specifies the reduction to apply to the output.
            Options are 'none', 'mean', or 'sum'. Default is 'mean'.
    Examples::
        >>> criterion1 = nn.MSELoss()
        >>> criterion2 = L2Loss()
        >>> input_data=torch.Tensor([2, 3, 4, 5])
        >>> target_data=torch.Tensor([4, 5, 6, 7])
        >>> loss1 = criterion1(input_data, target_data)  # tensor(4.)
        >>> loss2 = criterion2(input_data, target_data)  # tensor(4.)

    Returns:
        torch.Tensor: The L2 loss between input and target.
    """
    def __init__(self):
        super(L2Loss, self).__init__()

    def forward(self, input, target):
        loss = torch.mean(torch.pow(input - target, 2))
        return loss

class BCELoss(nn.Module):
    """
    二元交叉熵损失（Binary Cross Entropy Loss），也称为对数损失。
    用于测量预测输出中的每个元素与目标或地面实况中的相应元素之间的对数概率差异。依据公式实现。
    Args:
        input (torch.Tensor): The predicted output.Map to (0,1) through sigmoid function.
        target (torch.Tensor): The target or ground truth.
        reduction (str, optional): Specifies the reduction to apply to the output.
            Options are 'none', 'mean', or 'sum'. Default is 'mean'.

    Examples::
        >>> criterion1 = nn.BCELoss()
        >>> criterion2 = BCELoss()
        >>> input_data = torch.randn((5,))
        >>> target_data = torch.randint(0, 2, (5,), dtype=torch.float32)
        >>> loss1 = criterion1(torch.sigmoid(input_data), target_data)
        >>> loss2 = criterion2(input_data, target_data)
        >>> print("PyTorch BCELoss:", loss1.item())
        >>> print("Custom BCELoss:", loss2.item())

    Returns:
        torch.Tensor: The binary cross entropy loss between input and target.
    """
    def __init__(self, ignore_index=None, reduction='mean'):
        super(BCELoss, self).__init__()
        self.reduction = reduction
        self.ignore_index = ignore_index

    def forward(self, input, target):
        if self.ignore_index:
            input = input[:,:self.ignore_index,...]
            target = target[:, :self.ignore_index, ...]
        input = torch.sigmoid(input)
        loss = - (target * torch.log(input) + (1 - target) * torch.log(1 - input))
        if self.reduction == 'mean':
            return loss.mean()
        elif self.reduction == 'sum':
            return loss.sum()
        elif self.reduction == 'none':
            return loss
        else:
            raise ValueError(f'Unsupported reduction: {self.reduction}, available options are ["mean", "sum", "none"].')

class CrossEntropyLoss(nn.Module):
    """
    交叉熵损失（Cross Entropy Loss）用于多分类问题。
    用于测量预测输出和目标分布之间的交叉熵。依据公式实现。
    Args:
        input (torch.Tensor): The predicted output (logits).
        target (torch.Tensor): The target or ground truth (class labels).
        reduction (str, optional): Specifies the reduction to apply to the output.
            Options are 'none', 'mean', or 'sum'. Default is 'mean'.

    Examples::
        >>> criterion1 = nn.CrossEntropyLoss()
        >>> criterion2 = CrossEntropyLoss()
        >>> input_data = torch.randn((3, 5), requires_grad=True)
        >>> target_data = torch.randint(0, 5, (3,))
        >>> loss1 = criterion1(input_data, target_data)
        >>> loss2 = criterion2(input_data, target_data)
        >>> print("PyTorch CrossEntropyLoss:", loss1.item())
        >>> print("Custom CrossEntropyLoss:", loss2.item())

    Returns:
        torch.Tensor: The cross entropy loss between input and target.
    """
    def __init__(self, ignore_index=None):
        super(CrossEntropyLoss, self).__init__()
        self.ignore_index = ignore_index

    def forward(self, input, target):
        if self.ignore_index:
            input = input[:,:self.ignore_index,...]
            target = target[:, :self.ignore_index, ...]
        return nn.NLLLoss(reduction=self.reduction)(F.log_softmax(input, dim=1), target)


class FocalLoss(nn.Module):
    """
    Focal Loss 用于解决类别不平衡问题，通过缩小易分类的类别的损失来关注难分类的类别。依据公式实现。

    Args:
        alpha (float, optional): 控制易分类的类别的权重，大于1表示增加权重，小于1表示减小权重。默认为1.
        gamma (float, optional): 控制难分类的类别的损失的下降速度，大于0表示下降较慢，小于0表示下降较快。默认为2.
        reduction (str, optional): Specifies the reduction to apply to the output.
            Options are 'none', 'mean', or 'sum'. Default is 'mean'.

    Examples::
        >>> criterion = FocalLoss(alpha=1, gamma=2, reduction='mean')
        >>> input_data = torch.randn((5, 3), requires_grad=True)
        >>> target_data = torch.randint(0, 3, (5,))
        >>> loss = criterion(input_data, target_data)
        >>> print("Focal Loss:", loss.item())
    """
    def __init__(self, alpha=1, gamma=2, ignore_index=None, reduction='mean'):
        super(FocalLoss, self).__init__()
        self.alpha = alpha
        self.gamma = gamma
        self.reduction = reduction
        self.ignore_index = ignore_index

    def forward(self, input, target):
        if self.ignore_index:
            input = input[:,:self.ignore_index,...]
            target = target[:, :self.ignore_index, ...]
        ce_loss = F.cross_entropy(input, target, reduction='none')
        class_weights = torch.exp(-ce_loss)
        focal_loss = self.alpha * (1 - class_weights) ** self.gamma * ce_loss
        if self.reduction == 'mean':
            return focal_loss.mean()
        elif self.reduction == 'sum':
            return focal_loss.sum()
        elif self.reduction == 'none':
            return focal_loss
        else:
            raise ValueError(f'Unsupported reduction: {self.reduction}, available options are ["mean", "sum", "none"].')

class DiceLoss(nn.Module):
    """
    Dice Loss 测量预测的和目标的二进制分割掩码之间的不相似性。它被计算为1减去Dice系数，Dice系数是重叠的度量
    在预测区域和目标区域之间。

    Examples::
        >>> criterion = DiceLoss(reduction='mean')
        >>> predictions = torch.rand((1,2,16,16), dtype=torch.float32)
        >>> targets = torch.randn((1,2,16,16), dtype=torch.float32)
        >>> loss = criterion(predictions, targets)
        >>> print("Dice Loss:", loss.item())

    Returns:
        torch.Tensor: The Dice Loss between input and target.
    """
    def __init__(self, ignore_index=None, reduction='mean', eps=1e-5):
        super(DiceLoss, self).__init__()
        self.eps = eps
        self.ignore_index = ignore_index
        self.reduction = reduction

    def forward(self, input, target):
        if self.ignore_index:
            input = input[:,:self.ignore_index,...]
            target = target[:, :self.ignore_index, ...]

        input = torch.sigmoid(input)
        intersection = torch.sum(input * target)
        union = torch.sum(input) + torch.sum(target)
        dice_loss = 1 - (2 * intersection + self.eps) / (union + self.eps)
        if self.reduction == 'mean':
            return dice_loss.mean()
        elif self.reduction == 'sum':
            return dice_loss.sum()
        elif self.reduction == 'none':
            return dice_loss
        else:
            raise ValueError(f'Unsupported reduction: {self.reduction}, available options are ["mean", "sum", "none"].')

class DiceFocalLoss(nn.Module):
    """
    DiceFocalLoss结合了Dice Loss和Focal Loss两种损失函数，用于解决图像分割任务中的类别不平衡和边界模糊的问题。
    在计算损失时，综合考虑了模型预测结果与真实标签的 Dice Loss 和 Focal Loss 。

    Args:
        ignore_index (int, optional): 需要忽略的标签索引，如果设置了该参数，则计算损失时会忽略这些标签。默认为None。
        reduction (str, optional): 损失值的缩减模式，可选值为'mean'（求平均）、'sum'（求和）或'none'（不缩减）。默认为'mean'。
        eps (float, optional): 用于数值稳定性的小值。默认为1e-5。
        lambda_dice (float, optional): Dice Loss的权重系数。默认为1.0。
        lambda_focal (float, optional): Focal Loss的权重系数。默认为1.0。

    Examples::
        >>> criterion = DiceFocalLoss(ignore_index=0, reduction='mean', lambda_dice=0.8, lambda_focal=0.2)
        >>> input_data = torch.rand((4, 2, 16, 16), dtype=torch.float32)
        >>> target_data = torch.randint(0, 2, (4, 2, 16, 16), dtype=torch.float32)
        >>> loss = criterion(input_data, target_data)
        >>> print("DiceFocal Loss:", loss.item())

    Returns:
        torch.Tensor: 计算得到的DiceFocal Loss值。
    """
    def __init__(self,
                 ignore_index=None,
                 reduction='mean',
                 eps=1e-5,
                 lambda_dice=1.0,
                 lambda_focal=1.0):
        super(DiceFocalLoss, self).__init__()
        self.eps = eps
        self.reduction = reduction
        self.dice = DiceLoss(
            ignore_index,
            reduction='none',
        )
        self.focal = FocalLoss(
            ignore_index,
            reduction='none',
        )
        if lambda_dice < 0.0:
            raise ValueError("lambda_dice should be no less than 0.0.")
        if lambda_focal < 0.0:
            raise ValueError("lambda_focal should be no less than 0.0.")
        self.lambda_dice = lambda_dice
        self.lambda_focal = lambda_focal

    def forward(self, input, target):
        input, target = input.float(), target.float()
        dice_loss = self.dice(input, target)
        focal_loss = self.focal(input, target)
        total_loss = self.lambda_dice * dice_loss + self.lambda_focal * focal_loss
        if self.reduction == 'mean':
            return total_loss.mean()
        elif self.reduction == 'sum':
            return total_loss.sum()
        elif self.reduction == 'none':
            pass
        else:
            raise ValueError(f'Unsupported reduction: {self.reduction}, available options are ["mean", "sum", "none"].')

class BoundaryLoss(nn.Module):
    """
    计算二进制分割的边界损失

    Args:
        None

    Examples:
        >>> criterion = BoundaryLoss()
        >>> outputs_soft = torch.rand((1, 1, 3, 3))  # model prediction
        >>> outputs_soft = torch.sigmoid(outputs_soft)
        >>> label_batch = torch.randint(2, (1, 1, 3, 3))  # binary segmentation mask
        >>> loss = criterion(outputs_soft, label_batch)
        >>> print("Boundary Loss:", loss.item())
    Returns:
        torch.Tensor: The Boundary Loss between model predictions and ground truth.
    """
    def __init__(self, ignore_index=None, reduction='mean'):
        super(BoundaryLoss, self).__init__()
        self.reduction = reduction
        self.ignore_index = ignore_index

    def forward(self, input, target):
        if self.ignore_index:
            input = input[:,:self.ignore_index,...]
            target = target[:, :self.ignore_index, ...]
        loss = boundary_loss(input, target)
        if self.reduction == 'mean':
            return loss.mean()
        elif self.reduction == 'sum':
            return loss.sum()
        elif self.reduction == 'none':
            return loss
        else:
            raise ValueError(f'Unsupported reduction: {self.reduction}, available options are ["mean", "sum", "none"].')

class LabelSmoothingCrossEntropy(torch.nn.Module):
    def __init__(self, smoothing=0.1):
        super().__init__()
        self.smoothing = smoothing

    def forward(self, pred, target):
        confidence = 1. - self.smoothing
        log_probs = F.log_softmax(pred, dim=-1)
        idx = torch.stack([torch.arange(log_probs.shape[0]), target], dim=1)
        nll_loss = torch.gather(-log_probs, dim=-1, index=idx)
        smooth_loss = torch.mean(-log_probs, dim=-1)
        loss = confidence * nll_loss + self.smoothing * smooth_loss

        return loss.mean()


class Joint2loss(nn.Module):
    """
    联合损失函数, 传入两个损失函数
        >>> criterion1 = FocalLoss()
        >>> criterion2 = DiceLoss()
        >>> joint_loss = Joint2loss(criterion1, criterion2, alpha=0.7, reduction='mean')
        >>> input_tensor = torch.rand((1,2,16,16), dtype=torch.float32)
        >>> target_tensor = torch.randn((1,2,16,16), dtype=torch.float32)
        >>> loss = joint_loss(input_tensor, target_tensor)
        >>> print("Joint Loss:", loss.item())
    """
    def __init__(self, *args, alpha, beta=None, ignore_index=None, reduction='mean'):
        super(Joint2loss, self).__init__()
        self.reduction = reduction
        self.ignore_index = ignore_index
        self.alpha = alpha
        self.beta = beta if beta is not None else 1-self.alpha
        self.criterion_1, self.criterion_2 = args

    def forward(self, input, target):
        if self.ignore_index:
            input = input[:, :self.ignore_index,...]
            target = target[:, :self.ignore_index, ...]
        loss_1 = self.criterion_1(input, target)
        loss_2 = self.criterion_2(input, target)
        loss = self.alpha * loss_1 + self.beta * loss_2
        if self.reduction == 'mean':
            return loss.mean()
        elif self.reduction == 'sum':
            return loss.sum()
        elif self.reduction == 'none':
            pass
        else:
            raise ValueError(f'Unsupported reduction: {self.reduction}, available options are ["mean", "sum", "none"].')

class FocalLoss3D(nn.Module):
    """
    3D Focal Loss实现，用于处理3D图像分割任务。

    Args:
        include_background (bool): 是否包含背景类在损失计算中。默认为True。
        gamma (float): Focal Loss中的聚焦参数。默认为2.0。
        alpha (list or None): 用于平衡正负样本的权重。默认为None，表示不使用类别权重。
        use_softmax (bool): 是否使用softmax函数进行多分类。默认为False，表示使用sigmoid进行二分类或多标签分类。
        reduction (str): 指定损失函数的归约方式，可选值有'none', 'mean', 'sum'。默认为'mean'，表示计算损失的平均值。
    Example:
        >>> focal = FocalLoss3D()
        >>> batch_size = 2
        >>> num_classes = 3
        >>> d = h = w = 64
        >>> predictions = torch.randint(0, num_classes, (batch_size, num_classes, d, h, w))
        >>> true_labels = torch.randint(0, num_classes, (batch_size, num_classes, d, h, w))
        >>> loss = focal(predictions, true_labels)
        >>> print(f"Loss from FocalLoss3D: {loss.item()}")
    """
    def __init__(self,
                 include_background=True,
                 gamma=2.0,
                 alpha=None,
                 use_softmax=False,
                 reduction='mean'):
        super(FocalLoss3D, self).__init__()
        self.include_background = include_background
        self.gamma = gamma
        self.alpha = alpha
        self.use_softmax = use_softmax
        self.reduction = reduction

    def forward(self, input, target):
        n_pred_ch = input.shape[1]
        if not self.include_background:
            if n_pred_ch == 1:
                warnings.warn("single channel prediction, `include_background=False` ignored.")
            else:
                # if skipping background, removing first channel
                target = target[:, 1:]
                input = input[:, 1:]
        input = input.float()
        target = target.float()
        if target.shape != input.shape:
            raise ValueError(f"ground truth has different shape ({target.shape}) from input ({input.shape}),"
                             f"It may require one hot encoding")
        if self.use_softmax:
            if not self.include_background and self.alpha is not None:
                self.alpha = None
                warnings.warn("`include_background=False`, `alpha` ignored when using softmax.")
            loss = softmax_focal_loss_3d(input, target, self.gamma, self.alpha)
        else:
            loss = sigmoid_focal_loss_3d(input, target, self.gamma, self.alpha)

        if self.reduction == 'mean':
            return loss.mean()
        elif self.reduction == 'sum':
            return loss.sum()
        elif self.reduction == 'none':
            return loss
        else:
            raise ValueError(f'Unsupported reduction: {self.reduction}, available options are ["mean", "sum", "none"].')

class DiceLoss3D(nn.Module):
    """
    用于计算三维 Dice Loss 的 PyTorch 模块。
    注意“input”的轴N被期望为每个类的logits或概率，必须设置“sigmoid=True”或“softmax=True”
    Args:
        include_background (bool): 是否包括背景类，默认为 True。
        sigmoid (bool): 是否应用 sigmoid 函数，默认为 False。
        softmax (bool): 是否应用 softmax 函数，默认为 False。
        squared_pred (bool): 是否使用预测值的平方，默认为 False。
        jaccard (bool): 是否使用 Jaccard 损失（相当于 Dice Loss 的变体），默认为 False。
        reduction (str): 损失值的减少方式，可选值包括 "mean"、"sum" 和 "none"，默认为 "mean"。
        smooth_nr (float): 分子平滑参数，默认为 1e-5。
        smooth_dr (float): 分母平滑参数，默认为 1e-5。
    Example:
        >>> dice = DiceLoss3D()
        >>> batch_size = 2
        >>> num_classes = 3
        >>> d = h = w = 64
        >>> predictions = torch.randint(0, num_classes, (batch_size, num_classes, d, h, w))
        >>> true_labels = torch.randint(0, num_classes, (batch_size, num_classes, d, h, w))
        >>> loss = dice(predictions, true_labels)
        >>> print(f"Loss from DiceLoss3D: {loss.item()}")
    """
    def __init__(
            self,
            include_background=True,
            sigmoid=False,
            softmax=False,
            squared_pred=False,
            jaccard = False,
            reduction='mean',
            smooth_nr=1e-5,
            smooth_dr=1e-5,
    ):
        super(DiceLoss3D, self).__init__()
        self.include_background = include_background
        self.reduction = reduction
        self.sigmoid = sigmoid
        self.softmax = softmax
        self.squared_pred = squared_pred
        self.jaccard = jaccard
        self.smooth_nr = float(smooth_nr)
        self.smooth_dr = float(smooth_dr)

    def forward(self, input: torch.Tensor, target: torch.Tensor) -> torch.Tensor:
        if self.sigmoid:
            input = torch.sigmoid(input)

        n_pred_ch = input.shape[1]
        if self.softmax:
            if n_pred_ch == 1:
                warnings.warn("single channel prediction, `softmax=True` ignored.")
            else:
                input = torch.softmax(input, 1)

        if not self.include_background:
            if n_pred_ch == 1:
                warnings.warn("single channel prediction, `include_background=False` ignored.")
            else:
                target = target[:, 1:]
                input = input[:, 1:]

        if target.shape != input.shape:
            raise AssertionError(f"ground truth has different shape ({target.shape}) from input ({input.shape}),"
                                 f"It may require one hot encoding")

        reduce_axis = torch.arange(2, len(input.shape)).tolist()
        intersection = torch.sum(target * input, dim=reduce_axis)

        if self.squared_pred:
            ground_o = torch.sum(target**2, dim=reduce_axis)
            pred_o = torch.sum(input**2, dim=reduce_axis)
        else:
            ground_o = torch.sum(target, dim=reduce_axis)
            pred_o = torch.sum(input, dim=reduce_axis)

        denominator = ground_o + pred_o

        if self.jaccard:
            denominator = 2.0 * (denominator - intersection)

        f = 1.0 - (2.0 * intersection + self.smooth_nr) / (denominator + self.smooth_dr)

        if self.reduction == "mean":
            return torch.mean(f)
        elif self.reduction == "sum":
            return torch.sum(f)
        elif self.reduction == "none":
            return f
        else:
            raise ValueError(f'Unsupported reduction: {self.reduction}, available options are ["mean", "sum", "none"].')

class DiceFocalLoss3D(nn.Module):
    """
  用于结合 Dice Loss 和 Focal Loss 的三维损失函数模块。

    Args:
        include_background (bool): 是否包含背景类在损失计算中。默认为 True。
        sigmoid (bool): 是否应用 sigmoid 函数到预测值。默认为 False。
        softmax (bool): 是否应用 softmax 函数到预测值。默认为 False。多类别要改为 True。
        squared_pred (bool): 是否使用预测值的平方版本。仅用于 Dice Loss。
        jaccard (bool): 是否计算 Jaccard Index（软 IoU）而不是 Dice。默认为 False。
        reduction (str): 损失值的减少方式，可选值为 "mean"、"sum" 和 "none"。默认为 "mean"。
        smooth_nr (float): 分子平滑参数，默认为 1e-5。
        smooth_dr (float): 分母平滑参数，默认为 1e-5。
        gamma (float): Focal Loss 中的聚焦参数。默认为 2.0。
        lambda_dice (float): Dice Loss 的权重值。默认为 1.0。
        lambda_focal (float): Focal Loss 的权重值。默认为 1.0。
    Args:

    Example:
        >>> dice_focal = DiceFocalLoss3D()
        >>> batch_size = 2
        >>> num_classes = 3
        >>> d = h = w = 64
        >>> predictions = torch.randint(0, num_classes, (batch_size, num_classes, d, h, w))
        >>> true_labels = torch.randint(0, num_classes, (batch_size, num_classes, d, h, w))
        >>> loss = dice_focal(predictions, true_labels)
        >>> print(f"Loss from DiceFocalLoss3D: {loss.item()}")
    """
    def __init__(
            self,
            include_background=True,
            sigmoid=False,
            softmax=False,
            squared_pred=False,
            jaccard=False,
            reduction="mean",
            smooth_nr=1e-5,
            smooth_dr=1e-5,
            gamma=2.0,
            lambda_dice=1.0,
            lambda_focal=1.0,
    ):
        super(DiceFocalLoss3D, self).__init__()
        self.dice = DiceLoss3D(
            include_background=include_background,
            sigmoid=sigmoid,
            softmax=softmax,
            squared_pred=squared_pred,
            jaccard=jaccard,
            reduction='mean',
            smooth_nr=smooth_nr,
            smooth_dr=smooth_dr,
        )
        self.focal = FocalLoss3D(
            include_background=include_background,
            gamma=gamma,
            use_softmax=softmax,
            reduction='mean',
        )
        if lambda_dice < 0.0:
            raise ValueError("lambda_dice should be no less than 0.0.")
        if lambda_focal < 0.0:
            raise ValueError("lambda_focal should be no less than 0.0.")
        self.lambda_dice = lambda_dice
        self.lambda_focal = lambda_focal
        self.reduction = reduction

    def forward(self, input, target):
        dice_loss = self.dice(input, target)
        focal_loss = self.focal(input, target)
        total_loss = self.lambda_dice * dice_loss + self.lambda_focal * focal_loss

        if self.reduction == "mean":
            return torch.mean(total_loss)
        elif self.reduction == "sum":
            return torch.sum(total_loss)
        elif self.reduction == "none":
            return total_loss
        else:
            raise ValueError(f'Unsupported reduction: {self.reduction}, available options are ["mean", "sum", "none"].')


if __name__=="__main__":
    criterion = DiceFocalLoss(ignore_index=0, reduction='mean', lambda_dice=0.8, lambda_focal=0.2)
    input_data = torch.rand((4, 2, 16, 16))
    target_data = torch.randint(0, 2, (4, 2, 16, 16))
    loss = criterion(input_data, target_data)
    print("DiceFocal Loss:", loss.item())

    focal = DiceFocalLoss3D()
    batch_size = 2
    num_classes = 3
    d = h = w = 64
    predictions = torch.randint(0, num_classes, (batch_size, num_classes, d, h, w))
    true_labels = torch.randint(0, num_classes, (batch_size, num_classes, d, h, w))
    loss = focal(predictions, true_labels)
    print(f"Loss from FocalLoss3D: {loss.item()}")