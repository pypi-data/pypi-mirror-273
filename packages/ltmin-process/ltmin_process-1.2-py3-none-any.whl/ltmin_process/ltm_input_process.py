import collections
from PIL import Image, ImageOps
from PIL.ExifTags import TAGS
import cv2
import numpy as np
import torch
import torch.nn.functional as F

# const
DataType = {
    'uint8': np.uint8,
    'uint16': np.uint16,
    'uint32': np.uint32,
    'int8': np.int8,
    'int16': np.int16,
    'int32': np.int32,
}
BlurKernel = torch.tensor([
    1, 1, 1, 1, 1,
    1, 1, 2, 1, 1,
    1, 2, 4, 2, 1,
    1, 1, 2, 1, 1,
    1, 1, 1, 1, 1
]).reshape(5, 5) / 32
BlurFilter = torch.nn.Conv2d(in_channels=1, out_channels=1, kernel_size=(5,5), padding=2, stride=1, padding_mode='reflect', bias=False)
BlurFilter.weight.data = BlurKernel.unsqueeze(0).unsqueeze(0)
Lut = torch.tensor([[0.0000, 0.0117, 0.0225, 0.0342, 0.0459, 0.0566, 0.0684, 0.0801, 0.0908,
                     0.1025, 0.1143, 0.1250, 0.1367, 0.1484, 0.1592, 0.1709, 0.1826, 0.1943,
                     0.2051, 0.2168, 0.2285, 0.2393, 0.2510, 0.2627, 0.2734, 0.2852, 0.2969,
                     0.3076, 0.3193, 0.3311, 0.3418, 0.3535, 0.3652, 0.3760, 0.3877, 0.3994,
                     0.4102, 0.4180, 0.4248, 0.4307, 0.4355, 0.4395, 0.4434, 0.4473, 0.4512,
                     0.4541, 0.4570, 0.4609, 0.4629, 0.4658, 0.4688, 0.4717, 0.4736, 0.4766,
                     0.4785, 0.4814, 0.4834, 0.4854, 0.4873, 0.4902, 0.4922, 0.4941, 0.4961,
                     0.4980, 0.5000, 0.5020, 0.5039, 0.5059, 0.5078, 0.5098, 0.5127, 0.5146,
                     0.5166, 0.5186, 0.5215, 0.5234, 0.5264, 0.5283, 0.5312, 0.5342, 0.5371,
                     0.5391, 0.5430, 0.5459, 0.5488, 0.5527, 0.5566, 0.5605, 0.5645, 0.5693,
                     0.5752, 0.5820, 0.5898, 0.6006, 0.6123, 0.6240, 0.6348, 0.6465, 0.6582,
                     0.6689, 0.6807, 0.6924, 0.7031, 0.7148, 0.7266, 0.7373, 0.7490, 0.7607,
                     0.7715, 0.7832, 0.7949, 0.8057, 0.8174, 0.8291, 0.8408, 0.8516, 0.8633,
                     0.8750, 0.8857, 0.8975, 0.9092, 0.9199, 0.9316, 0.9434, 0.9541, 0.9658,
                     0.9775, 0.9883, 0.9990]])


def image_warp(img, m, dst_shape):
    """
    flags: cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP
    :param img: H,W,C or H,W
    :param m: np.ndarray, size=(3,3)
    :param dst_shape: (h,w)
    :return: H,W,C or H,W
    """
    return cv2.warpPerspective(img.copy(), m, dsize=(dst_shape[1], dst_shape[0]), flags=17)


def image_rotate(img, angle):
    def rot90(_img):
        return np.rot90(_img)
    img = np.array(img) if img is not np.ndarray else img
    times = int(angle/90)
    for _ in range(times):
        img = rot90(img)
    return img


def transpose_angle(img_path: str):
    """
    Counterclockwise 1:default, 2:left-to-right mirror, 3:rotate 180, 4:top-to-bottom mirror, 5:top-to-left mirror, 6:rotate 270, 7:top-to-right mirror, 8:rotate 90
    :return:int
    """
    ExifTags = collections.namedtuple('ExifTags', ['ID', 'Name'])
    rotation = {'direction': 'Counterclockwise', 1: 0, 8: 90, 3: 180, 6: 270}
    img = Image.open(img_path)
    exif = img._getexif() if hasattr(img, '_getexif') else None
    angle = 0
    if exif is None:
        # print(f'{img} Could not read exif data')
        return angle
    tag_tuple = (ExifTags(tag_id, TAGS.get(tag_id, tag_id)) for tag_id in exif)
    for tag in tag_tuple:
        if tag.Name == 'Orientation':
            angle = rotation[exif[tag.ID]]
            break
    return angle


def inter_linear(img, curve):
    """
    :param img: N,C,H,W
    :param curve: N,length
    :return: N,C,H,W
    """
    src = img.permute(0, 2, 3, 1).contiguous() * 2. - 1.
    src_img = torch.cat((src, torch.zeros_like(src)), dim=-1)
    target = curve.unsqueeze(2).unsqueeze(2).permute(0, 2, 3, 1).contiguous()
    output = F.grid_sample(target, src_img, align_corners=True, padding_mode='border')
    return output


def yuv_loader(path, dtype='uint16'):
    return np.fromfile(path, dtype=DataType[dtype])


def nps_out2ltm_in(nps_out_path: str, height=2304, width=4096):
    nps_out_img = yuv_loader(nps_out_path, dtype='uint16')
    nps_out_ds = nps_out_img[height * width:(height * width + height * (width // 2))].reshape((height // 2), width).reshape((height // 2), (width // 2), 2) / (1 << 10)
    m1 = torch.tensor(np.array([nps_out_img[0:height * width] / (1 << 10), F.interpolate(inter_linear(torch.tensor(nps_out_ds[:, :, 0], dtype=torch.float32).unsqueeze(0).unsqueeze(0), Lut), scale_factor=2, mode="nearest").detach().numpy().reshape(height * width) - 0.5, F.interpolate(inter_linear(torch.tensor(nps_out_ds[:, :, 1], dtype=torch.float32).unsqueeze(0).unsqueeze(0), Lut), scale_factor=2, mode="nearest").detach().numpy().reshape(height * width) - 0.5]), dtype=torch.float32).T
    return torch.matmul(m1, torch.tensor([[1, 0, 1.4072], [1, -0.3457, -0.7168], [1, 1.7793, 0]], dtype=torch.float32).t()).reshape(height, width, 3).numpy()


def generate_mask0(ltm_in0: np.ndarray, mask1_path: str, max_min1_path: str, height=2304, width=4096):
    """
    :param ltm_in0: H,W,C
    :param mask1_path: str
    :param max_min1_path: str
    :param height: int
    :param width: int
    :return: H,W
    """
    ltm_in0 = torch.tensor(ltm_in0)
    ltm_in0_y = 0.125 * ltm_in0[:, :, 0] + 0.25 * ltm_in0[:, :, 1] + 0.125 * ltm_in0[:, :, 2] + 0.5 * torch.max(ltm_in0, dim=2, keepdim=True)[0].squeeze()
    mask1 = torch.tensor(yuv_loader(mask1_path, dtype='uint16'), dtype=torch.float32).reshape(height // 4, width // 4).unsqueeze(0).unsqueeze(0) / (1 << 16)
    max_min1 = torch.tensor(yuv_loader(max_min1_path, dtype='uint8'), dtype=torch.float32).reshape(height // 4, width // 4).unsqueeze(0).unsqueeze(0) / (1 << 8)

    mask1_us4 = F.interpolate(mask1, scale_factor=4, mode='bilinear').detach().cpu()
    max_min1_us4 = F.interpolate(max_min1, scale_factor=4, mode='bilinear').detach().cpu()
    mask0 = max_min1_us4 * mask1_us4 + (torch.ones_like(max_min1_us4) - max_min1_us4) * BlurFilter(ltm_in0_y.unsqueeze(0).unsqueeze(0))
    return mask0.squeeze(0).squeeze(0).detach().numpy().astype(np.float32)


def simulation_process_nps_out(real_shot_path: str, nps_out_path: str, mask1_path: str, max_min1_path:str, warp_matrix: np.ndarray=None, height=2304, width=4096, dst_shape=(1080, 1920)):
    """
    :param real_shot_path: str, for image rotate correction
    :param nps_out_path: str
    :param mask1_path: str
    :param max_min1_path: str
    :param warp_matrix: np.ndarray
    :param height: int
    :param width: int
    :param dst_shape: tuple(h, w)
    :return:ltm_in_pass0, mask_pass0
    """
    rotate_angle = transpose_angle(real_shot_path)
    ltm_input0 = nps_out2ltm_in(nps_out_path, height=height, width=width)
    mask0 = generate_mask0(ltm_input0, mask1_path, max_min1_path, height=height, width=width)
    if warp_matrix is None:
        return image_rotate(ltm_input0, rotate_angle), image_rotate(mask0, rotate_angle)
    return image_rotate(image_warp(ltm_input0, warp_matrix, dst_shape=dst_shape), rotate_angle), image_rotate(image_warp(mask0, warp_matrix, dst_shape=dst_shape), rotate_angle)

