#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import os
import docx
from typing import Iterable
from xagents.loader.common import AbstractLoader, Chunk, merge_chunks
from xagents.loader.docx_loader import analyse_page
import subprocess

def doc2docx(doc_path, docx_path):
    # 构建命令行命令
    cmd = ["soffice", "--headless", "--convert-to", "docx", "--outdir", docx_path, doc_path]
    # 执行命令
    subprocess.run(cmd)
    print(f"Converted '{doc_path}' to docx format")


class DOCLoader(AbstractLoader):
    def __init__(self, max_page:int=None, **kwargs):
        super().__init__(**kwargs)
        self.max_page = max_page
    
    def load(self, file_path: str, upload_image=True, ocr=False, **kwargs) ->Iterable[Chunk]:
        directory = os.path.dirname(file_path)
        doc2docx(file_path, directory)
        doc = docx.Document(f"{file_path}x")
        chunks = analyse_page(doc, file_name=os.path.basename(file_path), upload_image=upload_image, ocr=ocr)
        chunks = merge_chunks(chunks)
        os.remove(f"{file_path}x")  # 删除产生的中间文件 docx
        yield from chunks
        


if __name__ == "__main__":
    from xagents.config import XAGENT_HOME
    loader = DOCLoader()

    file_path = os.path.join(XAGENT_HOME, "初步设计文件.doc")
    chunks = loader.load(file_path=file_path)

    print(len(chunks))
    print(chunks[0])
