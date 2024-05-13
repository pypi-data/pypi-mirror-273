#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import os
import json
from typing import Iterable
from xagents.loader.common import AbstractLoader, Chunk, ImageChunk, TextChunk, TableChunk, merge_chunks

def analyse_json(file_path:str, content, upload_image:bool, ocr:bool)->Iterable[Chunk]:
    for item in content:
        if not isinstance(item, dict):
            raise Exception(f"Parsing file {file_path} failed: unexpected json format.")
        try:
            if item['content_type'] == "TEXT":
                yield TextChunk(content=item['content'], page_idx=item['page_idx'])
            elif item['content_type'] == "IMAGE":
                yield ImageChunk(**item)
            elif item['content_type'] == "TABLE":
                yield TableChunk(**item)
        except:
            raise IndexError()

class JSONLoader(AbstractLoader):
    def load(self, file_path: str, upload_image=True, ocr=False, **kwargs) ->Iterable[Chunk]:
        with open(file_path, "r", encoding='utf-8') as f:
            content = json.load(f)
            if not isinstance(content, list):
                raise Exception(f"Parsing file {file_path} failed: unexpected json format.")
        
        chunks = analyse_json(file_path=file_path, content=content, upload_image=upload_image, ocr=ocr)
        yield from chunks
        


if __name__ == "__main__":
    from xagents.config import XAGENT_HOME
    loader = JSONLoader()

    file_path = os.path.join(XAGENT_HOME, "alpaca_data-0-3252-中文.json")
    chunks = loader.load(file_path=file_path)

    print(len(chunks))
    print(chunks[0])
