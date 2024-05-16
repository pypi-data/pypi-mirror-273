import collections
import os.path
import pickle
from PIL import Image
from PIL.ExifTags import TAGS
import cv2
import numpy as np
import torch
import torch.nn.functional as F


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
Lut = torch.tensor(
    [[0.0000, 0.0117, 0.0225, 0.0342, 0.0459, 0.0566, 0.0684, 0.0801, 0.0908,
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
invGammaCurve = torch.tensor(
    [[0, 64, 128, 192, 256, 320, 384, 448, 512, 575, 639, 703, 767, 831, 895, 959, 1023, 1087, 1151, 1215, 1279, 1343,
      1407, 1471, 1535, 1598, 1662, 1726, 1790, 1854, 1918, 1982, 2046, 2138, 2231, 2324, 2417, 2510, 2603, 2696, 2789,
      2882, 2975, 3068, 3161, 3254, 3347, 3440, 3533, 3626, 3719, 3812, 3905, 3998, 4091, 4204, 4317, 4431, 4545, 4659,
      4772, 4886, 5000, 5113, 5227, 5341, 5454, 5568, 5682, 5795, 5909, 6022, 6136, 6263, 6391, 6519, 6647, 6774, 6902,
      7030, 7158, 7286, 7414, 7542, 7670, 7797, 7925, 8053, 8181, 8321, 8462, 8604, 8745, 8886, 9027, 9168, 9309, 9450,
      9591, 9732, 9873, 10014, 10156, 10301, 10452, 10604, 10756, 10907, 11059, 11210, 11362, 11514, 11665, 11816,
      11968, 12120, 12271, 12428, 12585, 12743, 12900, 13057, 13215, 13372, 13529, 13687, 13844, 14002, 14159, 14316,
      14485, 14656, 14826, 14997, 15167, 15338, 15508, 15679, 15849, 16020, 16191, 16361, 16545, 16731, 16917, 17103,
      17289, 17475, 17661, 17847, 18033, 18219, 18405, 18591, 18777, 18963, 19149, 19335, 19521, 19707, 19893, 20079,
      20265, 20451, 20644, 20839, 21034, 21229, 21424, 21619, 21814, 22009, 22203, 22398, 22596, 22801, 23005, 23210,
      23415, 23619, 23824, 24028, 24233, 24438, 24646, 24861, 25077, 25292, 25507, 25722, 25938, 26153, 26368, 26584,
      26799, 27015, 27230, 27445, 27661, 27877, 28092, 28307, 28522, 28742, 28969, 29196, 29423, 29651, 29878, 30105,
      30333, 30560, 30788, 31015, 31242, 31470, 31697, 31924, 32151, 32379, 32606, 32837, 33078, 33319, 33560, 33800,
      34041, 34282, 34522, 34763, 35004, 35245, 35485, 35726, 35967, 36207, 36448, 36688, 36933, 37189, 37445, 37700,
      37956, 38212, 38468, 38723, 38979, 39235, 39491, 39746, 40002, 40258, 40514, 40769, 41025, 41281, 41537, 41792,
      42048, 42304, 42560, 42815, 43076, 43349, 43621, 43894, 44167, 44440, 44712, 44985, 45258, 45531, 45803, 46076,
      46349, 46622, 46895, 47167, 47440, 47714, 47986, 48259, 48532, 48805, 49077, 49350, 49623, 49896, 50168, 50441,
      50714, 50987, 51264, 51556, 51848, 52141, 52433, 52725, 53018, 53310, 53602, 53894, 54187, 54479, 54771, 55063,
      55356, 55648, 55940, 56232, 56525, 56818, 57110, 57406, 57721, 58036, 58350, 58665, 58980, 59295, 59609, 59924,
      60239, 60554, 60868, 61183, 61494, 61787, 62079, 62371, 62663, 62956, 63248, 63544, 63859, 64174, 64488, 64803,
      65118, 65433, 65765, 66106, 66447, 66788, 67130, 67470, 67794, 68109, 68424, 68738, 69053, 69368, 69687, 70027,
      70368, 70710, 71050, 71391, 71728, 72044, 72358, 72672, 72988, 73303, 73617, 73948, 74290, 74631, 74971, 75312,
      75654, 75995, 76336, 76676, 77018, 77359, 77700, 78040, 78382, 78723, 79063, 79404, 79746, 80107, 80479, 80850,
      81222, 81595, 81963, 82303, 82644, 82986, 83327, 83667, 84012, 84384, 84757, 85128, 85500, 85872, 86225, 86566,
      86907, 87248, 87590, 87930, 88290, 88662, 89034, 89406, 89778, 90150, 90522, 90894, 91266, 91638, 92010, 92382,
      92754, 93126, 93498, 93870, 94242, 94614, 94987, 95358, 95730, 96102, 96473, 96846, 97218, 97590, 97962, 98336,
      98746, 99156, 99564, 99973, 100380, 100752, 101123, 101496, 101868, 102240, 102633, 103042, 103452, 103861,
      104270, 104658, 105030, 105403, 105775, 106146, 106520, 106930, 107339, 107748, 108157, 108567, 108975, 109384,
      109794, 110204, 110613, 111021, 111431, 111840, 112249, 112658, 113068, 113477, 113886, 114295, 114704, 115114,
      115523, 115932, 116341, 116751, 117159, 117568, 117978, 118388, 118797, 119205, 119615, 120024, 120433, 120842,
      121252, 121661, 122070, 122479, 122889, 123344, 123799, 124253, 124708, 125140, 125549, 125957, 126367, 126776,
      127208, 127663, 128118, 128573, 129026, 129538, 130050, 130562, 131071]], dtype=torch.float32) / 131072


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


def nps_out2ltm_in(nps_out_path: str, height:int=2304, width:int=4096):
    nps_out_img = yuv_loader(nps_out_path, dtype='uint16')
    nps_out_ds = nps_out_img[height * width:(height * width + height * (width // 2))].reshape((height // 2), width).reshape((height // 2), (width // 2), 2) / (1 << 10)
    m1 = torch.tensor(np.array([nps_out_img[0:height * width] / (1 << 10), F.interpolate(inter_linear(torch.tensor(nps_out_ds[:, :, 0], dtype=torch.float32).unsqueeze(0).unsqueeze(0), Lut), scale_factor=2, mode="nearest").detach().numpy().reshape(height * width) - 0.5, F.interpolate(inter_linear(torch.tensor(nps_out_ds[:, :, 1], dtype=torch.float32).unsqueeze(0).unsqueeze(0), Lut), scale_factor=2, mode="nearest").detach().numpy().reshape(height * width) - 0.5]), dtype=torch.float32).T
    return torch.matmul(m1, torch.tensor([[1, 0, 1.4072], [1, -0.3457, -0.7168], [1, 1.7793, 0]], dtype=torch.float32).t()).reshape(height, width, 3).numpy().clip(0,1)


def generate_mask0(ltm_in0: np.ndarray, mask1_path: str, max_min1_path: str, height:int=2304, width:int=4096):
    """
    :param ltm_in0: H,W,C
    :return: H,W
    """
    ltm_in0 = torch.tensor(ltm_in0)
    ltm_in0_y = 0.125 * ltm_in0[:, :, 0] + 0.25 * ltm_in0[:, :, 1] + 0.125 * ltm_in0[:, :, 2] + 0.5 * torch.max(ltm_in0, dim=2, keepdim=True)[0].squeeze()
    mask1 = torch.tensor(yuv_loader(mask1_path, dtype='uint16'), dtype=torch.float32).reshape(height // 4, width // 4).unsqueeze(0).unsqueeze(0) / (1 << 16)
    max_min1 = torch.tensor(yuv_loader(max_min1_path, dtype='uint8'), dtype=torch.float32).reshape(height // 4, width // 4).unsqueeze(0).unsqueeze(0) / (1 << 8)

    mask1_us4 = F.interpolate(mask1, scale_factor=4, mode='bilinear').detach().cpu()
    max_min1_us4 = F.interpolate(max_min1, scale_factor=4, mode='bilinear').detach().cpu()
    mask0 = max_min1_us4 * mask1_us4 + (torch.ones_like(max_min1_us4) - max_min1_us4) * BlurFilter(ltm_in0_y.unsqueeze(0).unsqueeze(0))
    return mask0.squeeze(0).squeeze(0).detach().numpy().clip(0,1), ltm_in0_y.numpy().clip(0,1)


def calc_ltm_misc(real_shot_path: str, nps_out_path: str, mask1_path: str, max_min1_path:str, warp_matrix: np.ndarray=None, height:int=2304, width:int=4096, dst_shape:tuple=(1080, 1920)):
    rotate_angle = transpose_angle(real_shot_path)
    ltm_input0 = nps_out2ltm_in(nps_out_path, height=height, width=width)
    mask0, ltm_input0_y = generate_mask0(ltm_input0, mask1_path, max_min1_path, height=height, width=width)
    if warp_matrix is None:
        ltm_input0, mask0, ltm_input0_y = image_rotate(ltm_input0, rotate_angle).clip(0,1), image_rotate(mask0, rotate_angle).clip(0,1), image_rotate(ltm_input0_y, rotate_angle).clip(0,1)
    else:
        ltm_input0, mask0, ltm_input0_y = image_rotate(image_warp(ltm_input0, warp_matrix, dst_shape=dst_shape), rotate_angle).clip(0,1), image_rotate(image_warp(mask0, warp_matrix, dst_shape=dst_shape), rotate_angle).clip(0,1), image_rotate(image_warp(ltm_input0_y, warp_matrix, dst_shape=dst_shape), rotate_angle).clip(0,1)
    mask = torch.from_numpy(mask0)
    ltm_input = torch.from_numpy(ltm_input0)
    ltm_input_y = torch.from_numpy(ltm_input0_y).unsqueeze(0).unsqueeze(0)
    ltm_input_linear = torch.cat([inter_linear(ltm_input[..., 0].unsqueeze(0).unsqueeze(0), invGammaCurve),
                                  inter_linear(ltm_input[..., 1].unsqueeze(0).unsqueeze(0), invGammaCurve),
                                  inter_linear(ltm_input[..., 2].unsqueeze(0).unsqueeze(0), invGammaCurve)], dim=1)
    return ltm_input_linear, ltm_input_y, mask, mask.shape

