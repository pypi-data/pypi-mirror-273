#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2023/12/11 15:39:40
@Author  :   ChenHao
@Contact :   jerrychen1990@gmail.com
'''


import enum
from pydantic import BaseModel, Field


from typing import List, Optional, Tuple

from xagents.loader.common import Chunk
from xagents.config import *
from langchain_core.documents import Document
from snippets import *


def get_kb_dir(kb_name) -> str:
    return os.path.join(KNOWLEDGE_BASE_DIR, kb_name)


def get_chunk_dir(kb_name) -> str:
    return os.path.join(get_kb_dir(kb_name), "chunk")


def get_origin_dir(kb_name) -> str:
    return os.path.join(get_kb_dir(kb_name), "origin")


def get_id_dir(kb_name) -> str:
    return os.path.join(get_kb_dir(kb_name), "id")


def get_inverted_id_dir(kb_name) -> str:
    return os.path.join(get_kb_dir(kb_name), "inverted_id")


def get_index_dir(kb_name, index_name="index") -> str:
    return os.path.join(get_kb_dir(kb_name), index_name)


def get_inverted_index_dir(kb_name) -> str:
    return os.path.join(get_kb_dir(kb_name), "inverted_index")


def get_config_path(kb_name) -> str:
    return os.path.join(get_kb_dir(kb_name), "config.json")


def get_chunk_path(kb_name, file_name) -> str:
    return os.path.join(get_chunk_dir(kb_name), file_name+".jsonl")


def get_status_path(kb_name) -> str:
    return os.path.join(get_kb_dir(kb_name), "status.json")


def get_origin_path(kb_name, file_name) -> str:
    return os.path.join(get_origin_dir(kb_name), file_name)


def get_id_path(kb_name, file_name) -> str:
    return os.path.join(get_id_dir(kb_name), file_name+".jsonl")


def get_inverted_id_path(kb_name, file_name) -> str:
    return os.path.join(get_inverted_id_dir(kb_name), file_name+".jsonl")


class DistanceStrategy(str, enum.Enum):
    """Enumerator of the Distance strategies for calculating distances
    between vectors."""

    EUCLIDEAN_DISTANCE = "EUCLIDEAN_DISTANCE"
    MAX_INNER_PRODUCT = "MAX_INNER_PRODUCT"


def chunk2document(chunk: Chunk, metadata: dict = dict()) -> Document:
    _metadata = copy.copy(metadata)
    if chunk.search_content:
        page_content = chunk.search_content,
        _metadata.update(content=chunk.content)
    else:
        page_content = chunk.content
    _metadata.update(page_idx=chunk.page_idx, id=chunk.id)
    return Document(page_content=page_content, metadata=_metadata)

# # 知识库中的切片
# class KBChunk(Chunk):
#     kb_name: str = Field(description="知识库名称")
#     file_name: str = Field(description="文件名称")
#     idx: int = Field(description="chunk在文档中的顺序,从0开始")

#     def to_dict(self):
#         return self.model_dump(mode="json", exclude_none=True, exclude={"kb_name", "file_name", "idx"})

#     def to_document(self) -> Document:
#         if self.search_content:
#             page_content, metadata = self.search_content, dict(content=self.content)
#         else:
#             page_content, metadata = self.content, dict()

#         metadata.update(chunk_type=self.content_type.value, idx=self.idx, page_idx=self.page_idx,
#                         kb_name=self.kb_name, file_name=self.file_name)
#         return Document(page_content=page_content, metadata=metadata)

    # @classmethod
    # def from_document(cls, document: Document):
    #     content = document.metadata.pop("content", None)
    #     item = dict(content=content, search_content=document.page_content) if content else dict(content=document.page_content)
    #     item.update(document.metadata)
    #     return cls(**item)

    # def __hash__(self) -> int:
    #     return hash((self.kb_name, self.file_name, self.idx))

    # def __eq__(self, __value: object) -> bool:
    #     return hash(self) == hash(__value)


# 召回的切片
class RecalledChunk(Chunk):
    query: str = Field(description="召回chunk的query")
    score: float = Field(description="召回chunk的分数")
    file_name: str = Field(description="知识库文件名称")
    forwards: List[Chunk] = Field(description="chunk的下文扩展", default=[])
    backwards: List[Chunk] = Field(description="chunk的上文扩展", default=[])
    index_cls: str = Field(description="索引类型", default=None)

    @classmethod
    def from_document(cls, document: Document, query: str, score: float, index_cls: str) -> "RecalledChunk":
        """从langchain的Document构造过来

        Args:
            document (Document): langchain的Document
            query (str): 相关问题
            score (float): 召回得分

        Returns:
            _type_: RecalledChunk
        """

        content = document.metadata.pop("content", None)
        item = dict(content=content, search_content=document.page_content) if content else dict(content=document.page_content)
        # logger.debug(f"meta:{document.metadata}")
        item.update(document.metadata)
        return cls(**item, query=query, score=score, index_cls=index_cls)

    def __hash__(self) -> int:
        return hash((self.file_name, self.id))

    def __eq__(self, __value: object) -> bool:
        return hash(self) == hash(__value)

    def get_content(self):
        if self.search_content:
            return self.search_content + "\n" + self.content

        return self.content

    def to_plain_text(self):
        rs = self.get_content()
        if self.backwards:
            backwards_str = "\n".join([chunk.content for chunk in self.backwards])
            rs = backwards_str + "\n" + rs
        if self.forwards:
            forwards_str = "\n".join([chunk.content for chunk in self.forwards])
            rs = rs+"\n"+forwards_str
        return rs

    def to_detail_text(self, with_context=False, max_len=None) -> str:
        backward_len = sum(len(c.content) for c in self.backwards)
        forwards_len = sum(len(c.content) for c in self.forwards)
        content = self.get_content()
        main_len = len(content)

        detail_text = f"[score={self.score:2.3f}][{main_len}字][扩展后{backward_len+main_len+forwards_len}字][类型{self.content_type.value}][第{self.page_idx}页][index:{self.idx}][相关文档: {self.file_name} ][相关问题:{self.query}]\n\n **{content}**"
        if with_context:
            backwards_str, forwards_str = self.get_contexts(max_len=max_len)
            if backwards_str:
                detail_text = backwards_str + "\n\n"+detail_text
            if forwards_str:
                detail_text = detail_text + "\n\n"+forwards_str
        return detail_text

    def get_contexts(self, max_len=None) -> Tuple[str, str]:
        backwards_str, forwards_str = "", ""
        backward_len = sum(len(c.content) for c in self.backwards)
        forwards_len = sum(len(c.content) for c in self.forwards)

        if backward_len:
            backwards_str = "\n".join([f"{chunk.content}" for idx, chunk in enumerate(self.backwards)])
            if max_len:
                backwards_str = backwards_str[:max_len]+"..."
            backwards_str = f"上文[{backward_len}]字\n\n{backwards_str}"

        if forwards_len:
            forwards_str = "\n".join([f"{chunk.content}" for idx, chunk in enumerate(self.forwards)])
            if max_len:
                forwards_str = forwards_str[:max_len]+"..."
            forwards_str = f"下文[{forwards_len}]字\n\n{forwards_str}"

        return backwards_str, forwards_str

    @property
    def total_len(self):
        return sum(len(c.content) for c in self.backwards+[self]+self.forwards)


class KnowledgeBaseInfo(BaseModel):
    name: str = Field(description="知识库名称")
    desc: str = Field(description="知识库描述")
    embedding_config: dict = Field(description="embedding模型配置")
    vecstore_config: dict | list[dict] = Field(description="向量存储配置")
    file_num: int = Field(description="知识库文件数量")


# 知识库文件类
class KnowledgeBaseFileInfo(BaseModel):
    kb_name: str = Field(description="知识库名称")
    file_name: str = Field(description="知识库文件名称")
    is_cut: bool = Field(description="是否已经切片")
    is_indexed: bool = Field(description="是否已经索引")
    chunk_num: Optional[int] = Field(description="切片数量", default=None)
