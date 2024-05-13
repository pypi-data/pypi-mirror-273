#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2024/04/12 15:02:40
@Author  :   ChenHao
@Description  :   测试loader
@Contact :   jerrychen1990@gmail.com
'''
from unittest import TestCase
from loguru import logger
from snippets import set_logger
from xagents.loader.api import load_file, parse_file
from xagents.config import *
from xagents.loader.common import *


# unit test
class TestLoader(TestCase):

    @classmethod
    def setUpClass(cls):
        set_logger("dev", __name__)
        logger.info("start test embd")

    @classmethod
    def show_chunks(cls, chunks: Iterable[Chunk]):
        image_cnt = 0
        for chunk in chunks:
            logger.info(f"page={chunk.page_idx}, type={chunk.content_type}")

            if chunk.content_type == ContentType.IMAGE:
                image_cnt += 1
                logger.info(f"image:{chunk.image_name}")
                logger.info(f"content:{chunk.content}")
                logger.info(f"url:{chunk.url}")
            if chunk.content_type == ContentType.TEXT:
                logger.info(f"text:{chunk.content}")

            if chunk.content_type == ContentType.TABLE:
                # logger.info(f"table:\n{chunk.data}")
                logger.info(f"content:\n{chunk.content}")
            logger.info("*"*40+"\n")
        return image_cnt

    def test_load_pdf(self):
        file_path = os.path.join(DATA_DIR, "kb_file", "image_table.pdf")
        chunks = load_file(file_path, end_page=5, ocr=False)
        # image_cnt = 0
        image_cnt = self.show_chunks(chunks)

        self.assertEqual(image_cnt, 4)

    def test_load_docx(self):
        file_path = os.path.join(DATA_DIR, "kb_file", "Xagents中间件.docx")
        chunks = load_file(file_path, ocr=False)
        image_cnt = self.show_chunks(chunks)

        self.assertEqual(image_cnt, 1)

    # def test_load_doc(self):
    #     file_path = os.path.join(DATA_DIR, "kb_file", "初步设计文件.doc")
    #     chunks = load_file(file_path)
    #     image_cnt = self.show_chunks(chunks)

    #     self.assertEqual(image_cnt, 6)

    def test_load_pptx(self):
        file_path = os.path.join(DATA_DIR, "kb_file", "时序数据预测.pptx")
        chunks = load_file(file_path)
        image_cnt = self.show_chunks(chunks)

        self.assertEqual(image_cnt, 18)

    def test_load_json(self):
        file_path = os.path.join(DATA_DIR, "kb_file", "alpaca_data-0-3252-中文.json")
        chunks = list(load_file(file_path))
        self.show_chunks(chunks)
        self.assertEqual(len(chunks), 7)

    def test_load_jsonl(self):
        file_path = os.path.join(DATA_DIR, "kb_file", "LICENSE.jsonl")
        chunks = list(load_file(file_path))
        self.show_chunks(chunks)
        self.assertEqual(len(chunks), 17)

    def test_load_excel(self):
        file_path = os.path.join(DATA_DIR, "kb_file", "大学综合排名2022.xlsx")
        chunks = list(load_file(file_path))

        self.show_chunks(chunks)

        self.assertEqual(len(chunks), 3)

    def test_load_txt(self):
        file_path = os.path.join(DATA_DIR, "kb_file", "requirements.txt")
        chunks = load_file(file_path)
        image_cnt = self.show_chunks(chunks)
        self.assertEqual(image_cnt, 0)
        chunks = parse_file(file_path=file_path)
        logger.info(chunks)
        self.show_chunks(chunks)
