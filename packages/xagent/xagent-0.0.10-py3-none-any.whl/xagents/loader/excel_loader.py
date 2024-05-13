#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from typing import Iterable



from xagents.config import *
from xagents.loader.common import Chunk, AbstractLoader, TableChunk, data2markdown, merge_chunks

import pandas as pd

def analyse_table(file_path, **kwargs)->Iterable[Chunk]:

    xl = pd.ExcelFile(file_path)
    for name in xl.sheet_names:
        df:pd.DataFrame = pd.read_excel(xl, name)

        page_index = 1
        
        # content = df.to_json()
        content = data2markdown(df)
        yield TableChunk(content=content,page_idx=page_index, data=df)
        page_index+=1

            
class EXCELLoader(AbstractLoader):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


    def load(self, file_path: str, **kwargs) -> Iterable[Chunk]:
        #TODO 缺少页码控制
        chunks = analyse_table(file_path, **kwargs)
        chunks = merge_chunks(chunks)
        yield from chunks


if __name__ == "__main__":
    chunks = analyse_table("data/kb_file/大学综合排名2022.xlsx")
    for chunk in chunks:
        print(chunk)