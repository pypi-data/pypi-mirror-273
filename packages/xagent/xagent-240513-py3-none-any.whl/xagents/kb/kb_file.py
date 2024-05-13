#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2024/03/19 16:10:35
@Author  :   ChenHao
@Description  :  知识库文件类
@Contact :   jerrychen1990@gmail.com
'''


# 知识库文件类
import os
from loguru import logger
from typing import List
from xagents.kb.common import KnowledgeBaseFileInfo, get_chunk_path, get_origin_path, get_status_path
from xagents.loader.api import parse_file
from xagents.loader.common import Chunk
from snippets import dump, load, jload, jdump


class KnowledgeBaseFile:
    def __init__(self, kb_name: str, file_name: str):
        self.kb_name = kb_name
        self.file_name = file_name
        self.chunk_path = get_chunk_path(self.kb_name, self.file_name)
        self.origin_path = get_origin_path(self.kb_name, self.file_name)

    @property
    def is_cut(self) -> bool:
        return os.path.exists(self.chunk_path)

    @property
    def chunk_num(self) -> int:
        if not self.is_cut:
            return 0
        chunks = load(self.chunk_path)
        return len(chunks)

    def set_index_status(self, is_indexed: bool):
        logger.debug(f"setting {self.file_name}'s is_indexed value to {is_indexed}")
        status_path = get_status_path(self.kb_name)
        status = jload(status_path)
        if self.file_name not in status:
            status[self.file_name] = {}
        status[self.file_name]["indexed"] = is_indexed
        # logger.debug(f"{status=}")
        jdump(status, status_path)

    @property
    def is_indexed(self) -> bool:
        status_path = get_status_path(self.kb_name)
        rs = jload(status_path).get(self.file_name, {}).get("indexed", False)
        return rs

    def get_info(self):
        return KnowledgeBaseFileInfo(kb_name=self.kb_name, file_name=self.file_name, is_cut=self.is_cut, chunk_num=self.chunk_num, is_indexed=self.is_indexed)

    def cut(self, *args, **kwargs) -> List[Chunk]:
        logger.info(f"start cut file: {self.file_name}")
        chunks: List[Chunk] = parse_file(file_path=self.origin_path, *args, **kwargs)
        self._save_chunks(chunks=chunks)
        return len(chunks)

    def _save_chunks(self, chunks: List[Chunk]):
        chunk_json = [chunk.to_json() for chunk in chunks]
        dump(chunk_json, self.chunk_path)
        return chunks

    def list_chunks(self) -> List[Chunk]:
        """
        从切片文件加载切片
        """
        if not self.is_cut:
            return []

        chunk_dicts = load(self.chunk_path)
        logger.debug(f"loaded {len(chunk_dicts)} chunks from {self.chunk_path}")
        chunks = [Chunk.from_dict(ele) for ele in chunk_dicts]
        return chunks

    def get_chunk_ids(self) -> List[str]:
        chunks = self.list_chunks()
        chunk_ids = [c.id for c in chunks]
        return chunk_ids

    def get_chunk(self, idx: int) -> Chunk:
        chunks = self.list_chunks()
        if idx < 0 or idx >= len(chunks):
            raise Exception(f"chunk index out of range, idx: {idx}, len: {len(chunks)}")
        return chunks[idx]

    def add_chunks(self, chunks: List[Chunk], idx: int = None):
        origin_chunks = self.list_chunks()
        if idx is None:
            idx = len(chunks)
        chunks = origin_chunks[:idx] + chunks + origin_chunks[idx:]
        self._save_chunks(chunks)

    def delete_chunks(self, ids: List[str]):
        chunks = self.list_chunks()
        remain_chunks = [c for c in chunks if c.id not in ids]
        self._save_chunks(remain_chunks)

    def update_chunk(self, chunk: Chunk) -> bool:
        # do delete

        chunks = self.list_chunks()
        for idx, c in enumerate(chunks):
            if c.id == chunk.id:
                chunks[idx] = chunk
                break
        self._save_chunks(chunks)

    def delete(self):
        """
        删除知识库文档
        """
        for path in [self.origin_path, self.chunk_path]:
            if os.path.exists(path):
                os.remove(path)
