import numpy as np
import torch
import cv2
import os

from .utils import convert_image
    
def get_draw_preset(draw_preset: str) -> tuple:
    """获取pose绘图的预设，mmpose给定了一些常用数据集的关节点颜色和骨架颜色

    Args:
        draw_preset (str): 数据集名称

    Returns:
        tuple: 返回skeleton, kpt_color, skeleton_color
    """
    skeleton, kpt_color, skeleton_color = None, None, None
    if draw_preset == 'coco':
        skeleton = [[15, 13], [13, 11], [16, 14], [14, 12], 
                    [11, 12], [5, 11], [6, 12], [5, 6], 
                    [5, 7], [6, 8], [7, 9], [8, 10], 
                    [1, 2], [0, 1], [0, 2], [1, 3], 
                    [2, 4], [3, 5], [4, 6]]
        
        kpt_color = [[51, 153, 255], [51, 153, 255], [51, 153, 255], [51, 153, 255], 
                     [51, 153, 255], [0, 255, 0], [255, 128, 0], [0, 255, 0], 
                     [255, 128, 0], [0, 255, 0], [255, 128, 0], [0, 255, 0], 
                     [255, 128, 0], [0, 255, 0], [255, 128, 0], [0, 255, 0], 
                     [255, 128, 0]]
        
        skeleton_color = [[0, 255, 0], [0, 255, 0], [255, 128, 0], [255, 128, 0], 
                          [51, 153, 255], [51, 153, 255], [51, 153, 255], [51, 153, 255], 
                          [0, 255, 0], [255, 128, 0], [0, 255, 0], [255, 128, 0], 
                          [51, 153, 255], [51, 153, 255], [51, 153, 255], [51, 153, 255], 
                          [51, 153, 255], [51, 153, 255], [51, 153, 255]]
        
    elif draw_preset == 'sodpose':
        skeleton = [[0, 2], [0, 3], [1, 2], [1, 3], 
                    [2, 4], [3, 5], [0, 6], [6, 7], 
                    [9, 7], [8, 7], [8, 10], [9, 11], 
                    [11, 13], [10, 12], [8, 14], [9, 15], 
                    [15, 16], [14, 16], [19, 17], [17, 14], 
                    [20, 18], [18, 15]]
        
        kpt_color = [[51, 153, 255], [51, 153, 255], [51, 153, 255], [51, 153, 255], 
                    [51, 153, 255], [51, 153, 255], [51, 153, 255], [128, 128, 255], 
                    [0, 255, 0], [255, 128, 0], [0, 255, 0], [255, 128, 0], 
                    [0, 255, 0], [255, 128, 0], [0, 255, 0], [255, 128, 0], 
                    [128, 128, 255], [0, 255, 0], [255, 128, 0], [0, 255, 0], [255, 128, 0]]
        
        skeleton_color = [[51, 153, 255], [51, 153, 255], [51, 153, 255], [51, 153, 255], 
                          [51, 153, 255], [51, 153, 255], [51, 153, 255], [51, 153, 255], 
                          [51, 153, 255], [51, 153, 255], [0, 255, 0], [255, 128, 0], 
                          [255, 128, 0], [0, 255, 0], [51, 153, 255], [51, 153, 255], 
                          [51, 153, 255], [51, 153, 255], [0, 255, 0], [0, 255, 0], 
                          [255, 128, 0], [255, 128, 0]]
    
    return skeleton, kpt_color, skeleton_color

def draw_pose_in_image(img: np.array, 
                       poses: np.array,
                       save_root_dir: str = "./",
                       save_img_name: str = "origin-draw-pose-img.jpg", 
                       RGB2BGR: bool = False,
                       normlization: bool = False,
                       standardization_mean: np.array = None,
                       standardization_std: np.array = None,
                       draw_preset: str = None,
                       skeleton: np.array = None,
                       draw_point_size: int = 1,
                       draw_point_color: tuple = (0, 0, 255),
                       draw_point_thickness: int = 4,
                       draw_skeleton_color: tuple = (0, 255, 0)) -> np.array:
    """在给定的图片中绘制人体骨架图，并保存

    Args:
        img (np.array): 绘制图片，尺寸为(H, W, C)
        poses (np.array): 关节点坐标，可以是多人或单人，shape为(N, K, 3)或(K, 3)或(N, K, 2)或(K, 2)
        save_root_dir (str, optional): 绘制后图片保存的根路径. Defaults to "./".
        save_img_name (str, optional): 保存图片的名称. Defaults to "origin-draw-pose-img.jpg".
        RGB2BGR (bool, optional): 是否进行RGB2BGR的转换. Defaults to False.
        normlization (bool, optional): 是否需要逆归一化. Defaults to False.
        standardization_mean (np.array, optional): 是否需要逆标准化，需要同时传入方差和标准差的值. Defaults to None.
        standardization_std (np.array, optional): 是否需要逆标准化，需要同时传入方差和标准差的值. Defaults to None.
        draw_preset (str, optional): 绘制预测的名称，可以是coco或sodpose等. Defaults to None.
        skeleton (np.array, optional): 骨架连接数组，传参时尺寸要求为[N, 2]. Defaults to None.
        draw_point_size (int, optional): 关节点绘制大小. Defaults to 1.
        draw_point_color (tuple, optional): 关节点绘制颜色，传参时尺寸要求为[K, 3]. Defaults to (0, 0, 255).
        draw_point_thickness (int, optional): 关节点绘制粗细. Defaults to 4.
        draw_skeleton_color (tuple, optional): 骨架连接的颜色，传参时尺寸要求为[N, 3]]. Defaults to (0, 255, 0).

    Returns:
        np.array: 绘制好的图片
    """
    img = convert_image(img, RGB2BGR, normlization, standardization_mean, standardization_std)
    
    assert isinstance(poses, np.ndarray), "poses must be np.array"
    if len(poses.shape) == 2: # (K, 3) or (K, 2) -> (1, K, 3) or (1, K, 2)
        poses = poses[None, :]
    if poses.shape[2] == 3: # (N, K, 3) -> (N, K, 2) 或 (K, 3) -> (K, 2)
        poses = poses[:, :, :2]
    
    assert draw_preset in ['coco', 'sodpose', None], "draw_preset must be in ['coco', 'sodpose', None]"
    
    if draw_preset: # get preset
        skeleton, draw_point_color, draw_skeleton_color = get_draw_preset(draw_preset)
    else:
        assert skeleton is not None, "skeleton must be provided when draw_preset is None"
        
        # 要求骨架中的id从0开始排列
        min_kpt_id = np.min(skeleton.flatten())
        assert min_kpt_id == 1, "the keypoint id must be starting from 0"
        
        if isinstance(draw_point_color, tuple):
            draw_point_color = [draw_point_color for _ in range(poses.shape[1])]
        if isinstance(draw_skeleton_color, tuple):
            draw_skeleton_color = [draw_skeleton_color for _ in range(len(skeleton))]

        assert len(draw_point_color) == poses.shape[1], "the length of draw_point_color must equal to the number of keypoints"
        assert len(draw_skeleton_color) == len(skeleton), "the length of draw_skeleton_color must equal to the number of skeleton"
        
    if not os.path.isdir(save_root_dir):
        # 创建文件夹
        os.makedirs(save_root_dir)
            
    save_img_dir = os.path.join(save_root_dir, save_img_name)

    for _pose in poses:
        for i, (x, y) in enumerate(_pose): # 绘制关节点
            if x < 0 or y < 0:
                continue
                
            cv2.circle(img, (int(x), int(y)), draw_point_size, draw_point_color[i], draw_point_thickness)
            
        for i, (s, e) in enumerate(skeleton): # 绘制骨架
            cv2.line(img, (int(_pose[s][0]), int(_pose[s][1])), (int(_pose[e][0]),int(_pose[e][1])), draw_skeleton_color[i]) 
         
    cv2.imwrite(save_img_dir, img)
    
    return img