import collections
from PIL import Image, ImageOps
from PIL.ExifTags import TAGS
import cv2
import numpy as np
import torch
import torch.nn.functional as F

DataType: dict
BlurKernel: torch.tensor
BlurFilter: torch.nn.Conv2d
Lut: torch.tensor

def image_warp(img: np.ndarray, m: np.ndarray, dst_shape: tuple)->np.ndarray:
    """
    flags: cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP
    :param img: H,W,C or H,W
    :param m: np.ndarray, size=(3,3)
    :param dst_shape: (h,w)
    :return: H,W,C or H,W
    """
    ...

def image_rotate(img: np.ndarray, angle:int)->np.ndarray:...

def transpose_angle(img_path: str)->int:...

def inter_linear(img: torch.tensor, curve: torch.tensor)->torch.tensor:
    """
    :param img: N,C,H,W
    :param curve: N, length
    :return: N,C,H,W
    """
    ...

def yuv_loader(path:str, dtype:str)->np.ndarray:...

def nps_out2ltm_in(nps_out_path: str, height:int=2304, width: int=4096)->np.ndarray: ...

def generate_mask0(ltm_in0: np.ndarray, mask1_path: str, max_min1_path: str, height: int=2304, width: int=4096)->np.ndarray:
    """
    :param ltm_in0: H,W,C
    :param mask1_path: str
    :param max_min1_path: str
    :param height: int
    :param width: int
    :return: H,W
    """
    ...

def simulation_process_nps_out(real_shot_path: str, nps_out_path: str, mask1_path: str, max_min1_path: str, warp_matrix: np.ndarray=None, height=2304, width=4096, dst_shape=(1080, 1920))-> tuple[np.ndarray, np.ndarray]:
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
    ...






