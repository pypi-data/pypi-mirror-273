import numpy as np
import cv2
import os

from .utils import convert_image
    
def draw_origin_img(img: np.array, 
                    save_root_dir: str = "./",
                    save_img_name: str = "origin-img.jpg", 
                    RGB2BGR: bool = False,
                    normlization: bool = False,
                    standardization_mean: np.array = None,
                    standardization_std: np.array = None) -> np.array:
    """绘制原始图片

    Args:
        img (np.array): 绘制图片，尺寸为(H, W, C)
        save_root_dir (str, optional): 绘制后图片保存的根路径. Defaults to "./".
        save_img_name (str, optional): 保存图片的名称. Defaults to "origin-draw-pose-img.jpg".
        RGB2BGR (bool, optional): 是否进行RGB2BGR的转换. Defaults to False.
        normlization (bool, optional): 是否需要逆归一化. Defaults to False.
        standardization_mean (np.array, optional): 是否需要逆标准化，需要同时传入方差和标准差的值. Defaults to None.
        standardization_std (np.array, optional): 是否需要逆标准化，需要同时传入方差和标准差的值. Defaults to None.

    Returns:
        np.array: 绘制好的图片
    """
    img = convert_image(img, RGB2BGR, normlization, standardization_mean, standardization_std)
    
    if not os.path.isdir(save_root_dir):
        # 创建文件夹
        os.makedirs(save_root_dir)
            
    save_img_dir = os.path.join(save_root_dir, save_img_name)

    cv2.imwrite(save_img_dir, img)
    
    return img