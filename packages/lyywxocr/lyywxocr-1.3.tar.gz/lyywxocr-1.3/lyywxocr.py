import os
import json
import time
import threading
from wechat_ocr.ocr_manager import OcrManager, OCR_MAX_TASK_ID
from typing import Dict, Callable

wechat_ocr_dir = r"C:\Users\Administrator\AppData\Roaming\Tencent\WeChat\XPlugin\Plugins\WeChatOCR\7079\extracted\WeChatOCR.exe"
wechat_mmmojo_dir = r"D:\Soft\Internet\Tencent\WeChat\[3.9.10.19]"

# 用于存储回调函数返回值的共享变量
ocr_result_holder = {}
lock = threading.Lock()


        
def ocr_result_callback(img_path:str, ocr_dict:dict, debug:bool=True):
    texts = []
    if 'ocrResult' in ocr_dict:
        for result in ocr_dict['ocrResult']:
            if 'text' in result:
                texts.append(result['text'])
    #if debug: print("ocr_result:",texts)
    #用锁确保线程安全
    with lock:
        ocr_result_holder['result'] = "".join(texts)

def image_ocr(images:list, call_back_fun):
    ocr_manager = OcrManager(wechat_mmmojo_dir)
    # 设置WeChatOcr目录
    ocr_manager.SetExePath(wechat_ocr_dir)
    # 设置微信所在路径
    ocr_manager.SetUsrLibDir(wechat_mmmojo_dir)
    # 设置ocr识别结果的回调函数
    ocr_manager.SetOcrResultCallback(call_back_fun)
    # 启动ocr服务
    ocr_manager.StartWeChatOCR()
    # 开始识别图片
    for image in images:  
        print(ocr_manager.DoOCRTask(image))
    time.sleep(1)
    while ocr_manager.m_task_id.qsize() != OCR_MAX_TASK_ID:
        pass
    # 识别输出结果
    ocr_manager.KillWeChatOCR()

  
if __name__ == "__main__":
    import os

    directory = r'D:\UserData\Pictures\ocr'
    files = []

    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            files.append(os.path.join(directory, filename))
    
    result = image_ocr(files,ocr_result_callback)
    print("resultx:",ocr_result_holder['result'] if 'result' in ocr_result_holder else None)