import os
from typing import Iterable
from xagents.loader.common import AbstractLoader, Chunk, merge_chunks
from xagents.loader.excel_loader import analyse_table
import subprocess

def xls2xlsx(xls_path, xlsx_path):
    # 构建命令行命令
    cmd = ["soffice", "--headless", "--convert-to", "xlsx", "--outdir", xlsx_path, xls_path]
    # 执行命令
    subprocess.run(cmd)
    print(f"Converted '{xls_path}' to xlsx format")

class XLSLoader(AbstractLoader):
    def __init__(self, max_page:int=None, **kwargs):
        super().__init__(**kwargs)
        self.max_page = max_page
    
    def load(self, file_path: str, **kwargs) -> Iterable[Chunk]:
        directory = os.path.dirname(file_path)
        xls2xlsx(file_path, directory)
        chunks = analyse_table(f"{file_path}x", **kwargs)
        chunks = merge_chunks(chunks)
        # os.remove(f"{file_path}x")  # 删除产生的中间文件 xlsx
        yield from chunks


if __name__ == "__main__":
    from xagents.config import XAGENT_HOME
    loader = XLSLoader()

    file_path = os.path.join(XAGENT_HOME, "大学综合排名2022.xls")
    chunks = loader.load(file_path=file_path)

    print(len(chunks))
    print(chunks[0])