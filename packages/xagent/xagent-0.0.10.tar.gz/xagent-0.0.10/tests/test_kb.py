#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2024/04/24 10:36:09
@Author  :   ChenHao
@Description  : 知识库管理相关单测
@Contact :   jerrychen1990@gmail.com
'''

import os
from typing import List
from unittest import TestCase
from loguru import logger
from xagents.loader.common import Chunk, ContentType
from xagents.kb.common import DistanceStrategy, RecalledChunk
from xagents.config import DATA_DIR
from snippets import set_logger
from xagents.kb.api import add_chunks, create_knowledge_base, create_kb_file, delete_chunks, delete_kb_file, delete_knowledge_base, list_chunks, list_kb_files, search_knowledge_base, update_chunk

kb_name = "ut_kb"
kb_file_names = ["requirements.txt", "Xagents中间件.docx", "image_table.pdf"]
to_delete_kb_file_name = "Xagents中间件.docx"

def show_recall_chunks(recall_chunks:List[RecalledChunk]):
    for i, chunk in enumerate(recall_chunks):
        print(f"{i}: {chunk.to_plain_text()}")

# unit test
class TestKB(TestCase):

    @classmethod
    def setUpClass(cls):
        set_logger("dev", __name__)
        logger.info("start test KnowledgeBase")

    def test1_create_kb(self):
        vecstore_config = [dict(cls='XFAISS', distance_strategy=DistanceStrategy.MAX_INNER_PRODUCT)
                                                        # dict(cls="XES", es_url='http://localhost:9200')
                                                        ]
        kb  = create_knowledge_base(name=kb_name, desc="kb for unit test",
                                     embedding_config=dict(cls="ZhipuEmbedding"),
                                     vecstore_config = vecstore_config)

        kb_info = kb.get_info()
        logger.info(f"kb info: {kb_info}")

    def test2_add_kb_file(self):
        for kb_file_name in kb_file_names:
            kb_file_path = os.path.join(DATA_DIR, "kb_file", kb_file_name)
            kb_file = create_kb_file(kb_name=kb_name, file=kb_file_path)
            kb_file_info = kb_file.get_info()
            logger.info(f"kb file info: {kb_file_info}")
            
    def test3_list_kb_files(self):
        kb_files = list_kb_files(kb_name=kb_name)
        self.assertEqual(len(kb_files), len(kb_file_names))

        for kb_file in kb_files:
            kb_file_info = kb_file.get_info()
            logger.info(f"kb file info: {kb_file_info}")
            
    
    def test4_chunk_crud(self):
        chunks = list_chunks(kb_name=kb_name, file_name=to_delete_kb_file_name)
        logger.info(chunks[:2])
        logger.info(len(chunks))
        chunk = chunks[0]
        delete_chunks(kb_name=kb_name, file_name=to_delete_kb_file_name, chunk_ids=[chunk.id])
        chunks = list_chunks(kb_name=kb_name, file_name=to_delete_kb_file_name)
        logger.info(len(chunks))
        chunk = chunks[0]
        chunk.content = "updated_content"
        update_chunk(kb_name=kb_name, file_name=to_delete_kb_file_name, chunk=chunk)
        new_chunks = [Chunk.from_dict(dict(content="new_content", content_type=ContentType.TEXT))]
        add_chunks(kb_name=kb_name, file_name=to_delete_kb_file_name, chunks=new_chunks, idx=3)
        
        chunks = list_chunks(kb_name=kb_name, file_name=to_delete_kb_file_name)
        logger.info(len(chunks))
        for i, chunk in enumerate(chunks[:5]):
            logger.info(f"{i}: {chunk}")
    
            

            
    def test5_search_kb(self):
        query = "python-snippets"
        recall_chunks = search_knowledge_base(name=kb_name, query=query, top_k=5)
        show_recall_chunks(recall_chunks)
        
        query = "updated_content?new_content"
        recall_chunks = search_knowledge_base(name=kb_name, query=query, top_k=2)
        show_recall_chunks(recall_chunks)
        
        
        
    def test6_delete_kb_file(self):
        msg = delete_kb_file(kb_name=kb_name, file_name=to_delete_kb_file_name)
        logger.info(f"delete kb file: {msg}")
        
    def test7_delete_kb(self):
        msg = delete_knowledge_base(name=kb_name)
        logger.info(f"delete kb: {msg}")
