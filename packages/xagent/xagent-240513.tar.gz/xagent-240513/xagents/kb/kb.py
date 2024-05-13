#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2024/03/19 15:45:46
@Author  :   ChenHao
@Description  :   
@Contact :   jerrychen1990@gmail.com
'''
import copy
import os
import re
from typing import List, Type
from loguru import logger
from xagents.kb.kb_file import KnowledgeBaseFile
from xagents.kb.vector_store import XES, LocalVecStore, XVecStore, get_vecstore_cls
from xagents.loader.common import Chunk, ContentType
from xagents.model.api import get_embd_model, get_rerank_model
from xagents.kb.common import KnowledgeBaseInfo, RecalledChunk, chunk2document, get_chunk_dir, get_chunk_path, get_config_path, get_index_dir, get_kb_dir, get_origin_dir, get_status_path
from snippets import load, log_cost_time, dump, jload, jdump


class KnowledgeBase():

    def __init__(self, name: str, desc, embedding_config: dict, vecstore_config: dict | List[dict]):
        self.name = name
        self.desc = desc
        self.embedding_config = embedding_config
        self.vecstore_config = vecstore_config if isinstance(vecstore_config, list) else [vecstore_config]
        self.indexes = []
        self._build_dirs()
        self._save_config()

    @classmethod
    def from_config(cls, config: dict | str):
        if isinstance(config, str):
            # logger.info(f"{config=}")
            config = jload(config)
        logger.debug(f"{config=}")
        return cls(**config)

    def _get_config(self) -> dict:
        return dict(name=self.name, desc=self.desc, embedding_config=self.embedding_config, vecstore_config=self.vecstore_config)

    def get_info(self) -> KnowledgeBaseInfo:
        """返回知识库的信息

        Returns:
            dict: 知识库信息
        """
        file_num = len(list(self.list_kb_files()))
        return KnowledgeBaseInfo(**self._get_config(), file_num=file_num)

    def _build_dirs(self):
        self.kb_dir = get_kb_dir(self.name)
        self.origin_dir = get_origin_dir(self.name)

        self.chunk_dir = get_chunk_dir(self.name)
        self.config_path = get_config_path(self.name)
        self.status_path = get_status_path(self.name)

        os.makedirs(self.origin_dir, exist_ok=True)
        os.makedirs(self.chunk_dir, exist_ok=True)
        if not os.path.exists(self.config_path):
            jdump(dict(), self.status_path)

    def _save_config(self):
        dump(self._get_config(), self.config_path)

    def get_indexes(self) -> List[XVecStore]:
        """
        初始化向量存储、ES存储
        """
        if not self.indexes:
            for index_config in self.vecstore_config:
                config = copy.copy(index_config)
                vecstore_cls: Type[XVecStore] = get_vecstore_cls(config.pop("cls"))
                if vecstore_cls.is_local():
                    local_dir = get_index_dir(kb_name=self.name, index_name=f"{vecstore_cls.__name__}_index")
                    config.update(local_dir=local_dir)

                if vecstore_cls.need_embd():
                    embedding_model = get_embd_model(self.embedding_config)
                    config.update(embedding=embedding_model)
                if vecstore_cls == XES:
                    if "es_index" not in config:
                        config.update(es_index=f"{self.name}")

                logger.debug(f"creating index:{vecstore_cls} with config:{config}")
                index = vecstore_cls.from_config(config)
                self.indexes.append(index)
        return self.indexes

    def list_kb_files(self) -> List[KnowledgeBaseFile]:
        kb_files = []
        for file_name in os.listdir(self.origin_dir):
            kb_file = KnowledgeBaseFile(kb_name=self.name, file_name=file_name)
            kb_files.append(kb_file)
        return kb_files

    def remove_kb_file(self, kb_file: KnowledgeBaseFile):
        """
        删除文档
        """
        assert kb_file.kb_name == self.name
        # 从索引中删除
        self.remove_kb_file_from_index(kb_file=kb_file)
        # 删除kb文件
        kb_file.delete()

    def remove_kb_file_from_index(self, kb_file: KnowledgeBaseFile):
        ids = kb_file.get_chunk_ids()
        self.remove_chunks_from_index(ids)

    def remove_chunks_from_index(self, chunk_ids):
        for index in self.get_indexes():
            logger.info(f"deleting {len(chunk_ids)} chunks from index:{index}")
            index.delete(chunk_ids)
            if index.is_local():
                index.save()

    def add_chunks2index(self, chunks: List[Chunk], meta_info: dict, do_save=False, batch_size=16):
        indexes = self.get_indexes()
        chunks = [chunk for chunk in chunks if chunk.content]
        documents = [chunk2document(chunk, meta_info) for chunk in chunks]

        ids = [chunk.id for chunk in chunks]
        # 添加新的index
        for index in indexes:
            embd_model = index.embeddings
            if embd_model:
                if hasattr(embd_model, "batch_size"):
                    logger.debug(f"setting embedding model batch size to {batch_size}")
                    setattr(embd_model, "batch_size", batch_size)
                else:
                    logger.warning(f"{embd_model.__class__} has no attribute batch_size, set to default value {batch_size}")
            logger.debug(f"updating {len(ids)} documents to index:{index}")
            index.delete(ids=ids)
            index.add_documents(documents=documents, ids=ids)

            if index.is_local() and do_save:
                logger.info(f"saving to index dir:{index.local_dir}")
                index.save()

    def add_kb_file2index(self,  kb_file: KnowledgeBaseFile, do_save=False, batch_size=16):
        if not kb_file.is_cut:
            logger.warning(f"{kb_file.file_name} is not cut, please cut it first")
            return
        chunks = kb_file.list_chunks()
        kb_file.set_index_status(False)
        self.add_chunks2index(chunks=chunks, meta_info=dict(file_name=kb_file.file_name), do_save=do_save, batch_size=batch_size)
        kb_file.set_index_status(True)

    @log_cost_time(name="rebuild_index")
    def rebuild_index(self, batch_size: int):
        """
        重新构建向量知识库
        """
        indexes = self.get_indexes()
        kb_files = self.list_kb_files()
        for kb_file in kb_files:
            self.add_kb_file2index(kb_file=kb_file, do_save=False, batch_size=batch_size)
        for index in indexes:
            if isinstance(index, LocalVecStore):
                index.save()

    def delete(self):
        """删除知识库"""
        for index in self.get_indexes():
            index.delete_all()
        import shutil
        shutil.rmtree(path=self.kb_dir)

    @log_cost_time(name="kb_search")
    def search(self, query: str, top_k: int = 3, score_threshold: float = None,
               do_split_query=False, file_names: List[str] = None, rerank_config: dict = {},
               do_expand=False, expand_len: int = 500, forward_rate: float = 0.5) -> List[RecalledChunk]:
        """知识库检索

        Args:
            query (str): 待检索的query
            top_k (int, optional): 返回多少个chunk. Defaults to 3.
            score_threshold (float, optional): 召回的chunk相似度阈值. Defaults to None.
            do_split_query (bool, optional): 是否按照？切分query并分别召回. Defaults to False.
            file_names (List[str], optional): 按照名称过滤需要召回的片段所在的文件. Defaults to None.
            do_expand (bool, optional): 返回的chunk是否做上下文扩展. Defaults to False.
            expand_len (int, optional): 上下文扩展后的chunk字符长度（do_expand=True时生效）. Defaults to 500.
            forward_rate (float, optional): 上下文扩展时向下文扩展的比率（do_expand=True时生效）. Defaults to 0.5.

        Returns:
            List[RecalledChunk]: 相关的切片，按照score降序
        """
        recalled_chunks = []
        # 切分query
        queries = split_query(query, do_split_query)

        # 过滤条件
        _filter = dict()
        if file_names:
            _filter = dict(file_name=file_names)

        # 每个子query做检索
        indexes = self.get_indexes()
        for query in queries:

            for index in indexes:
                score_threshold = index.convert_score(score_threshold)
                logger.debug(f"searching {query} with vecstore_cls: {index.__class__.__name__}, {_filter=}, {top_k=}, {score_threshold=}")
                docs_with_score = index.similarity_search_with_score(query, k=top_k, score_threshold=score_threshold, filter=_filter)
                logger.debug(f"{docs_with_score=}")
                tmp_recalled_chunks = [RecalledChunk.from_document(d, score=index.convert_score(
                    s), query=query, index_cls=index.__class__.__name__) for d, s in docs_with_score]
                recalled_chunks.extend(tmp_recalled_chunks)

        # 去重，避免召回相同切片
        origin_recall_num = len(recalled_chunks)
        recalled_chunks = list(sorted(set(recalled_chunks), key=lambda x: x.score, reverse=True))
        logger.info(f"{len(recalled_chunks)} distinct recalled from {len(queries)} queries and {len(indexes)} indexes, {origin_recall_num-len(recalled_chunks)} duplicated")

        # 精排
        if rerank_config:
            recalled_chunks = rerank(recalled_chunks, rerank_config)
        recalled_chunks = recalled_chunks[:top_k]
        logger.info(f"get {len(recalled_chunks)} reranked chunks after sort")

        # 上下文扩展
        if do_expand:
            logger.info("expanding recalled chunks")
            for chunk in recalled_chunks:
                expand_chunk(chunk, self.name, expand_len, forward_rate)

        return recalled_chunks


def rerank(recalled_chunks: List[RecalledChunk], rerank_config: dict) -> List[RecalledChunk]:
    """重排序
    Args:
        recalled_chunks (List[RecalledChunk]): 待排序的切片

    Returns:
        List[RecalledChunk]: 排序后的切片
    """
    # logger.debug("reranking...")
    rerank_model = get_rerank_model(rerank_config)
    if rerank_model:
        logger.info("reranking chunks with rerank model")
        for chunk in recalled_chunks:
            similarity = rerank_model.cal_similarity(chunk.query, chunk.content)
            chunk.score = similarity

    recalled_chunks.sort(key=lambda x: x.score, reverse=True)
    return recalled_chunks


def split_query(query: str, do_split_query=False) -> List[str]:
    """切割query"""
    if do_split_query:
        rs = [e.strip() for e in re.split("\?|？", query) if e.strip()]
        logger.debug(f"split origin query into {len(rs)} queries")

        return rs
    else:
        # 不需要切分也转成list形式，方便后续统一处理
        return [query]


# 扩展上下文到给定的长度
# TODO 扩展时，避免重复的chunk
def expand_chunk(chunk: RecalledChunk, kb_name: str, expand_len: int, forward_rate=0.5) -> RecalledChunk:
    logger.debug(f"expanding chunk {chunk}")
    chunk_path = get_chunk_path(kb_name, chunk.file_name)
    chunk_dicts = load(chunk_path)
    chunk_idx = None

    for idx, ele in enumerate(chunk_dicts):
        if ele["id"] == chunk.id:
            chunk_idx = idx
            break

    if chunk_idx is None:
        logger.warning(f"chunk {chunk} not found in {chunk_path}")
        return chunk

    to_expand = expand_len - len(chunk.content)
    if to_expand <= 0:
        return chunk

    forward_len = int(to_expand * forward_rate)
    backward_len = to_expand - forward_len
    logger.debug(f"expand chunk with :{forward_len=}, {backward_len=}, origin_len:{len(chunk.content)}")
    backwards, forwards = [], []

    # 查找前面的chunk
    idx = chunk_idx-1
    while idx >= 0:
        if backward_len <= 0:
            break
        tmp_chunk = copy.copy(chunk_dicts[idx])
        if tmp_chunk["content_type"] == ContentType.TEXT:
            chunk_len = min(len(tmp_chunk["content"]), backward_len)
            tmp_chunk["content"] = tmp_chunk["content"][-chunk_len:]
            to_add: Chunk = Chunk(**tmp_chunk)
            backwards.append(to_add)
            backward_len -= chunk_len
        idx -= 1

    backwards.reverse()

    idx = chunk_idx + 1
    # logger.debug(f"{idx=}, {len(chunk_dicts)=}, {forward_len=}")
    while idx < len(chunk_dicts):
        if forward_len <= 0:
            break

        tmp_chunk = copy.copy(chunk_dicts[idx])
        if tmp_chunk["content_type"] == ContentType.TEXT:
            chunk_len = min(len(tmp_chunk["content"]), forward_len)
            tmp_chunk["content"] = tmp_chunk["content"][:chunk_len]
            to_add: Chunk = Chunk(**tmp_chunk)
            forwards.append(to_add)
            forward_len -= chunk_len
        idx += 1

    chunk.backwards = backwards
    chunk.forwards = forwards
    logger.debug(f"expand done with {len(backwards)} backward chunks and {len(forwards)} forward chunks, total_len:{chunk.total_len}")

    return chunk
