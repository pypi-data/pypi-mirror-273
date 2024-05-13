import os
import pptx
from typing import Iterable
from xagents.loader.common import AbstractLoader, Chunk, merge_chunks
from xagents.loader.pptx_loader import analyse_slide
import subprocess

def ppt2pptx(ppt_path, pptx_path):
    # 构建命令行命令
    cmd = ["soffice", "--headless", "--convert-to", "pptx", "--outdir", pptx_path, ppt_path]
    # 执行命令
    subprocess.run(cmd)
    print(f"Converted '{ppt_path}' to pptx format")

class PPTLoader(AbstractLoader):
    def __init__(self, max_page:int=None, **kwargs):
        super().__init__(**kwargs)
        self.max_page = max_page
    
    def load(self, file_path: str, upload_image=True, ocr=False, **kwargs) ->Iterable[Chunk]:
        directory = os.path.dirname(file_path)
        ppt2pptx(file_path, directory)
        ppt = pptx.Presentation(f"{file_path}x")
        chunks = analyse_slide(ppt, file_name=os.path.basename(file_path), upload_image=upload_image, ocr=ocr)
        chunks = merge_chunks(chunks)
        os.remove(f"{file_path}x")  # 删除产生的中间文件 pptx
        yield from chunks


if __name__ == "__main__":
    from xagents.config import XAGENT_HOME
    loader = PPTLoader()

    file_path = os.path.join(XAGENT_HOME, "英语诗歌.ppt")
    chunks = loader.load(file_path=file_path)

    print(len(chunks))
    print(chunks[0])