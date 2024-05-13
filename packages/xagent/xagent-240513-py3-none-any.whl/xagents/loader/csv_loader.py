#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from typing import Iterable



from xagents.config import *
from xagents.loader.common import Chunk, AbstractLoader, TableChunk, data2markdown, merge_chunks

import docx
import pandas as pd

def analyse_table(file_path, **kwargs)->Iterable[Chunk]:

    page_index = 1
    
    df:pd.DataFrame = pd.read_csv(file_path)
    # content = df.to_json()
    content = data2markdown(df)
    print('here')
    print(content)
    yield TableChunk(content=content,page_idx=page_index, data=df)

            
class CSVLoader(AbstractLoader):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


    def load(self, file_path: str, **kwargs) -> Iterable[Chunk]:
        chunks = analyse_table(file_path, **kwargs)
        chunks = merge_chunks(chunks)
        yield from chunks


if __name__ == "__main__":
    chunks = analyse_table("file_path")
    for chunk in chunks:
        print(chunk)