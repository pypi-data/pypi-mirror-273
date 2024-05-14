import numpy as np
import cv2
import os

from .utils import convert_image

def draw_bbox_in_image(img: np.array, 
                       bboxes: np.array, 
                       xyxy: bool = False,
                       save_root_dir: str = "./",
                       save_img_name: str = "origin-draw-bbox-img.jpg", 
                       RGB2BGR: bool = False,
                       normlization: bool = False,
                       standardization_mean: np.array = None,
                       standardization_std: np.array = None,
                       draw_bboxes_color: tuple = (0, 255, 0),
                       draw_bboxes_thickness: int = 2) -> np.array:
    """在给定的图片中绘制bbox，并保存

    Args:
        img (np.array): 绘制图片，尺寸为(H, W, C)
        bboxes (_type_): bbox坐标，可以是多个bbox，shape为(N, 4)或(4,)
        xyxy (bool, optional): 是否为左上右下坐标的格式，否则认定为左上宽高的格式. Defaults to True.
        save_root_dir (str, optional): 绘制后图片保存的根路径. Defaults to "./".
        save_img_name (str, optional): 保存图片的名称. Defaults to "origin-draw-bbox-img.jpg".
        RGB2BGR (bool, optional): 是否进行RGB2BGR的转换. Defaults to False.
        normlization (bool, optional): 是否需要逆归一化. Defaults to False.
        standardization_mean (np.array, optional): 是否需要逆标准化，需要同时传入方差和标准差的值. Defaults to None.
        standardization_std (np.array, optional): 是否需要逆标准化，需要同时传入方差和标准差的值. Defaults to None.
        draw_bboxes_color (tuple, optional): bbox绘制颜色，传参时尺寸要求为[N, 3]. Defaults to (0, 255, 0).
        draw_bboxes_thickness (int, optional): bbox绘制粗细. Defaults to 2.

    Returns:
        np.array: 绘制好的图片
    """
    
    img = convert_image(img, RGB2BGR, normlization, standardization_mean, standardization_std)
    
    assert isinstance(bboxes, np.ndarray), "bboxes must be np.array"
    if len(bboxes.shape) == 1: # (4,) -> (1, 4)
        bboxes = bboxes[None, :]
        
    assert bboxes.shape[-1] == 4, "the last dimension of bboxes must be 4. It means (x1, y1, x2, x2) or (x, y, w, h)"
    
    if not xyxy: # 将左上宽高转为左上右下
        # xywh2xyxy
        bboxes[:, 2] += bboxes[:, 0]
        bboxes[:, 3] += bboxes[:, 1]
        
    if not os.path.isdir(save_root_dir):
        # 创建文件夹
        os.makedirs(save_root_dir)
            
    save_img_dir = os.path.join(save_root_dir, save_img_name)

    if isinstance(draw_bboxes_color, tuple):
        draw_bboxes_color = [draw_bboxes_color for _ in range(bboxes.shape[0])]
    assert len(draw_bboxes_color) == bboxes.shape[0], "the length of draw_bboxes_color must equal to the number of bboxes"
    
    for i, _bbox in enumerate(bboxes):
        tl_x, tl_y, br_x, br_y = _bbox
        
        # 判断左上角和右下角是否在图像内
        if tl_x < 0 or tl_y < 0 or br_x >= img.shape[1] or br_y >= img.shape[0]:
            continue
        
        # 绘制矩形框
        cv2.rectangle(img, (int(tl_x), int(tl_y)), (int(br_x), int(br_y)), draw_bboxes_color[i], thickness=draw_bboxes_thickness)

    cv2.imwrite(save_img_dir, img)
    
    return img