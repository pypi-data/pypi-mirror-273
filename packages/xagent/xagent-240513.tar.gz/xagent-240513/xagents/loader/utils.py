#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2024/04/25 13:55:58
@Author  :   ChenHao
@Description  :   load过程中的工具类
@Contact :   jerrychen1990@gmail.com
'''

from loguru import logger
from minio import Minio
from xagents.config import *



def create_minio_client():
    return Minio(MINIO_URL,
                 access_key=MINIO_ACCESS_KEY,
                 secret_key=MINIO_SECRET_KEY,
                 secure=False)


def upload_to_minio(file_path, bucket_name="xagent") -> str:
    try:
        # 使用 fput_object 上传文件
        minioClient = create_minio_client()
        object_name = os.path.basename(file_path)
        minioClient.fput_object(bucket_name, object_name, file_path)        
        logger.info(f'Successfully uploaded {object_name} to {bucket_name}/{object_name}')
        url = minioClient.presigned_get_object(bucket_name, object_name)
        return url
    except Exception as err:
        logger.exception(err)
        return None
    

def image2text(image_path):
    from cnocr import CnOcr
    ocr = CnOcr(det_model_name='ch_PP-OCRv3_det')  # model_name 参考 https://gitee.com/cyahua/cnocr
    text = ocr.ocr(image_path)
    content = ','.join(item['text'] for item in text)
    return content


if __name__ == "__main__":
    file_path = os.path.join(DATA_DIR, "image_table_pages-page1-image0.png")
    url = upload_to_minio(file_path)
    print(url)
   
