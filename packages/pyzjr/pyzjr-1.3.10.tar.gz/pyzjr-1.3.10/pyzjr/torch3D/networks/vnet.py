import torch
import torch.nn as nn

class InputTransition(nn.Module):
    def __init__(
            self, in_channels, out_channels, act, bias=False
    ):
        super(InputTransition, self).__init__()
        if out_channels % in_channels != 0:
            raise ValueError(
                f"out channels should be divisible by in_channels. Got in_channels={in_channels}, out_channels={out_channels}."
            )
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.conv1 = nn.Conv3d(in_channels, out_channels, kernel_size=5, padding=2, bias=bias)
        self.bn1 = nn.BatchNorm3d(out_channels)
        self.act1 = act

    def forward(self, x):
        out = self.bn1(self.conv1(x))
        repeat_num = self.out_channels // self.in_channels
        x16 = x.repeat([1, repeat_num, 1, 1, 1][: 5])
        out = self.act1(torch.add(out, x16))
        return out

class LUConv(nn.Module):
    def __init__(self, nchan, bias=False):
        super().__init__()
        self.conv1 = nn.Conv3d(nchan, nchan, kernel_size=5, padding=2, bias=bias)
        self.bn1 = nn.BatchNorm3d(nchan)
        self.act = nn.ELU(inplace=True)

    def forward(self, x):
        return self.act(self.bn1(self.conv1(x)))

def _make_nconv(nchan, depth, bias=False):
    layers = []
    for _ in range(depth):
        layers.append(LUConv(nchan, bias))
    return nn.Sequential(*layers)

class DownTransition(nn.Module):
    def __init__(
            self,
            in_channels,
            nconvs,
            act,
            dropout=None,
            bias=False,
    ):
        super().__init__()

        out_channels = 2 * in_channels
        self.down_conv = nn.Conv3d(in_channels, out_channels, kernel_size=2, stride=2, bias=bias)
        self.bn1 = nn.BatchNorm3d(out_channels)
        self.act = act
        self.dropout = dropout
        self.do1 = nn.Dropout3d()
        self.ops = _make_nconv(out_channels, nconvs, bias)

    def forward(self, x):
        down = self.act(self.bn1(self.down_conv(x)))
        if self.dropout:
            down = self.do1(down)
        out = self.ops(down)
        out = self.act(torch.add(out, down))
        return out

class UpTransition(nn.Module):
    def __init__(
            self,
            in_channels,
            out_channels,
            nconvs,
            act,
            dropout=None,
    ):
        super().__init__()
        self.up_conv = nn.ConvTranspose3d(in_channels, out_channels // 2, kernel_size=2, stride=2)
        self.norm = nn.BatchNorm3d(out_channels // 2)
        self.dropout_type = dropout
        self.dropout = nn.Dropout3d()
        self.act = act
        self.ops = _make_nconv(out_channels, nconvs)
        self.do1 = nn.Dropout()
        self.do2 = nn.Dropout3d()


    def forward(self, x, skipx):
        if self.dropout_type:
            x = self.do1(x)
        skipxdo = self.do2(skipx)
        out = self.act(self.norm(self.up_conv(x)))
        xcat = torch.cat((out, skipxdo), 1)
        out = self.ops(xcat)
        out = self.act(torch.add(out, xcat))
        return out


class OutputTransition(nn.Module):
    def __init__(
            self, in_channels, out_channels, act, bias=False
    ):
        super().__init__()
        self.conv1 = nn.Conv3d(in_channels, out_channels, kernel_size=5, padding=2, bias=bias)
        self.bn1 = nn.BatchNorm3d(out_channels)
        self.conv2 = nn.Conv3d(out_channels, out_channels, kernel_size=1)
        self.act = act

    def forward(self, x):
        # convolve 32 down to 2 channels
        out = self.act(self.bn1(self.conv1(x)))
        out = self.conv2(out)
        return out


class VNet3D(nn.Module):
    """
    V-Net based on `Fully Convolutional Neural Networks for Volumetric Medical Image Segmentation
    <https://arxiv.org/pdf/1606.04797.pdf>`.
    """
    def __init__(
            self,
            in_channels=1,
            num_classes=1,
            act=nn.ELU(inplace=True),
            dropout=True,
            bias=False,
    ):
        super().__init__()
        self.relu = nn.ReLU(inplace=True)
        self.in_tr = InputTransition(in_channels, 16, self.relu, bias=bias)
        self.down_tr32 = DownTransition(16, 1, self.relu, bias=bias)
        self.down_tr64 = DownTransition(32, 2, self.relu, bias=bias)
        self.down_tr128 = DownTransition(64, 3, act, dropout=dropout, bias=bias)
        self.down_tr256 = DownTransition(128, 2, act, dropout=dropout, bias=bias)
        self.up_tr256 = UpTransition(256, 256, 2, act, dropout=dropout)
        self.up_tr128 = UpTransition(256, 128, 2, act, dropout=dropout)
        self.up_tr64 = UpTransition(128, 64, 1, self.relu)
        self.up_tr32 = UpTransition(64, 32, 1, self.relu)
        self.out_tr = OutputTransition(32, num_classes, act, bias=bias)

    def forward(self, x):
        out16 = self.in_tr(x)
        out32 = self.down_tr32(out16)
        out64 = self.down_tr64(out32)
        out128 = self.down_tr128(out64)
        out256 = self.down_tr256(out128)
        x = self.up_tr256(out256, out128)
        x = self.up_tr128(x, out64)
        x = self.up_tr64(x, out32)
        x = self.up_tr32(x, out16)
        x = self.out_tr(x)
        return x


if __name__ == '__main__':
    import torchsummary
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    # B x C x Z x Y x X
    # 4 x 1 x 64 x 64 x 64
    input = torch.ones(1, 1, 32, 32, 32).to(device)
    net = VNet3D(in_channels=1, num_classes=3)
    net = net.to(device)
    out = net(input)
    print(out.shape)
    torchsummary.summary(net, input_size=(1, 32, 32, 32))
