import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import gaussian_filter1d
import json
import os

def load_json_logs(json_logs, key):
    ap_lists = [[] for _ in json_logs]
    
    for i, json_log in enumerate(json_logs):
        with open(json_log, 'r') as log_file:
            for line in log_file:
                log = json.loads(line.strip())
                # skip lines without `epoch` field
                if key not in log:
                    continue
                ap_lists[i].append(log[key])
                
    return ap_lists

def draw_ap_curve(json_file: list[str], 
                  key: str, 
                  legend: list[str], 
                  save_root_dir: str, 
                  save_img_name: str,
                  val_stride: list[int] = 1,
                  gaussian_filter1d_sigma = None):
    
    if isinstance(json_file, str):
        json_file = [json_file]
    if isinstance(legend, str):
        legend = [legend]
    if isinstance(val_stride, int):
        val_stride = [val_stride for _ in range(len(json_file))]
    
    len_json_file = len(json_file)
    len_legend = len(legend)
    len_val_stride = len(val_stride)
    
    # 上述五个参数的长度必须相等
    assert len_json_file == len_legend == len_val_stride, \
        "The length of the three parameters (json_file, legend, val_stride) must be equal"
    
    # 提供的数据
    ap_lists = load_json_logs(json_file, key)
    
    # 设置标题和标签
    plt.xlabel('epoch')
    plt.ylabel('mAP')
    
    # 显示图例
    plt.legend()

    markers = ['o', 'v', '^', '<', '>', 's', 'p', 'P', '*', 'h', 'H', '+', 'x', 'X', 'D', 'd', '|', '_', '.', ',']
    linestyles = ['-', '--', '-.', ':']
    
    for i, _ap in enumerate(ap_lists):
        if gaussian_filter1d_sigma is not None:
            _ap = gaussian_filter1d(_ap, sigma=gaussian_filter1d_sigma)
        _stride = val_stride[i]
        _legend = legend[i]
        _marker = markers[i % len(markers)]
        _linestyle = linestyles[i % len(linestyles)]
        plt.plot(np.arange(1, len(_ap) * _stride + 1, _stride), _ap, marker=_marker, linestyle=_linestyle, label=_legend)
    
    if not os.path.isdir(save_root_dir):
        # 创建文件夹
        os.makedirs(save_root_dir)
            
    save_img_dir = os.path.join(save_root_dir, save_img_name)
    
    # 显示图形
    plt.savefig(save_img_dir, bbox_inches = 'tight')