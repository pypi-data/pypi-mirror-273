#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import os
import jsonlines
from typing import Iterable
from xagents.loader.common import AbstractLoader, Chunk, merge_chunks
from xagents.loader.json_loader import analyse_json

class JSONLLoader(AbstractLoader):
    def load(self, file_path: str, upload_image=True, ocr=False, **kwargs) -> Iterable[Chunk]:
        with open(file_path, "r", encoding='utf-8') as f:
            content = jsonlines.Reader(f)
        
            chunks = analyse_json(file_path=file_path, content=content, upload_image=upload_image, ocr=ocr)
            yield from chunks



if __name__ == "__main__":
    from xagents.config import XAGENT_HOME
    loader = JSONLLoader()

    file_path = os.path.join(XAGENT_HOME, "")
    chunks = loader.load(file_path=file_path)

    print(len(chunks))
    print(chunks[0])
