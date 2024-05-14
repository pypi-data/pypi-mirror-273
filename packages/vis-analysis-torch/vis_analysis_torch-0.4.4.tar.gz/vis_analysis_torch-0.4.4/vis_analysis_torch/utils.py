import numpy as np
import cv2

def convert_mmpose_datasets_info(keypoint_info: dict, 
                                 skeleton_info: dict) -> tuple:
    """将mmpose中的datasets_info中的keypoint_info和skeleton_info提取其中的skeleton, kpt_color, skeleton_color信息

    Args:
        keypoint_info (_type_): _description_
        skeleton_info (_type_): _description_

    Returns:
        tuple: 返回skeleton, kpt_color, skeleton_color
    """
    # 创建映射字典，将关节点名字与关节点的id号进行对应，以便skeleton_info中信息的提取
    keypoint_id_map = {info['name']: info['id'] for info in keypoint_info.values()}

    # 提取关节点颜色
    kpt_color = []
    for kpt in keypoint_info.values():
        kpt_color.append(kpt['color'])
        
    # 1. 提取骨架连接情况，转为关节点id之间的连接；
    # 2. 提取骨架颜色
    skeleton = []
    skeleton_color = []
    for link_info in skeleton_info.values():
        skeleton.append([keypoint_id_map[link_info['link'][0]], keypoint_id_map[link_info['link'][1]]])
        skeleton_color.append(link_info['color'])
    
    return skeleton, kpt_color, skeleton_color

def convert_image(img: np.array,
                  RGB2BGR: bool = False,
                  normlization: bool = False,
                  standardization_mean: np.array = None,
                  standardization_std: np.array = None,) -> np.array:
    """对img进行处理，包括RGB2BGR、normlization、standardization

    Args:
        img (np.array): 图片，尺寸为(H, W, C)
        RGB2BGR (bool, optional): 将颜色通道从RGB转为BGR. Defaults to False.
        normlization (bool, optional): 归一化操作，将图片像素值从[0,1]区间映射到[0,255]. Defaults to False.
        standardization_mean (np.array, optional): 标准化操作的均值，需要同时存在均值和方差时才能计算. Defaults to None.
        standardization_std (np.array, optional): 标准化操作的方差，需要同时存在均值和方差时才能计算. Defaults to None.

    Returns:
        np.array: 返回处理好的图片
    """
    if normlization:
        img = img * 255
    
    assert img.shape[2] == 3, "the last dimension of img must be 3. It means color channel"
    assert (standardization_mean is None and standardization_std is None) \
        or (standardization_mean is not None and standardization_std is not None), "standardization_mean and standardization_std must be None or not None at the same time"
        
    if standardization_mean is not None and standardization_std is not None:
        img = img * standardization_std + standardization_mean
    
    if RGB2BGR:
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        
    return img