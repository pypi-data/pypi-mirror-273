#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2023/12/07 17:54:34
@Author  :   ChenHao
@Contact :   jerrychen1990@gmail.com
'''

import json
import itertools
from typing import Iterable, List, Optional

from abc import abstractmethod

from pydantic import BaseModel, Field

from agit.common import LLMResp, ToolCall
from xagents.config import DEFAULT_KB_PROMPT_TEMPLATE, DEFAULT_WEB_SEARCH_KB_PROMPT_TEMPLATE, \
    DEFAULT_WEB_SEARCH_PROMPT_TEMPLATE
from xagents.kb.common import RecalledChunk
from loguru import logger


class WebPage(BaseModel):
    url: str = Field(description="网页的URL")
    content: str = Field(description="网页的内容")


class WebSearchResp(BaseModel):
    summary: str = Field(description="搜索结果的摘要")
    pages: List[WebPage] | None = Field(description="搜索结果的网页列表")


class AgentResp(LLMResp):
    references: Optional[List[RecalledChunk]] = Field(description="召回的片段")
    web_search_result: Optional[WebSearchResp] = Field(description="联网搜索的结果", default=None)

    def to_stream(self):
        if self.references:
            for reference in self.references:
                reference = json.dumps(dict(reference=reference.model_dump()), ensure_ascii=False)
                yield reference+"\n"

        if self.tool_calls:
            for tool_call in self.tool_calls:
                tool_call = json.dumps(dict(tool_call=tool_call.model_dump()), ensure_ascii=False)
                yield tool_call+"\n"
        for ele in self.content:
            ele = json.dumps(dict(content_chunk=ele), ensure_ascii=False)
            yield ele+"\n"
        if self.usage:
            yield json.dumps(dict(usage=self.usage.model_dump()), ensure_ascii=False)+"\n"

    @classmethod
    def from_stream(cls, stream: Iterable):
        references = []
        tool_calls = []

        def json_stream_gen():
            for line in stream:
                if isinstance(line, bytes):
                    line = line.decode("utf-8")
                # logger.info(f"line: {line}")
                json_line = json.loads(line)
                yield json_line

        json_stream = json_stream_gen()

        for json_line in json_stream:
            if "reference" in json_line:
                references.append(RecalledChunk.model_validate(json_line["reference"]))
            elif "tool_call" in json_line:
                tool_calls.append(ToolCall.model_validate(json_line["tool_call"]))
            else:
                content_chunk = json_line
                break
        # logger.info(f"references: {references}")
        # logger.info(f"tool_calls: {tool_calls}")
        # logger.info(f"content_chunk: {content_chunk}")

        def content_gen():
            for json_line in itertools.chain([content_chunk], json_stream):
                yield json_line.get("content_chunk", "")
        return AgentResp(references=references, tool_calls=tool_calls, content=content_gen())


class AbstractAgent:

    def __init__(self, name) -> None:
        self.name = name

    @abstractmethod
    def chat(self, message: str, stream=True, do_remember=True) -> AgentResp:
        raise NotImplementedError

    @abstractmethod
    def remember(self, role: str, message: str):
        raise NotImplementedError


class KBConfig(BaseModel):
    name: str = Field(description="知识库名称")
    prompt_template: str = Field(description="应用知识库的提示词模板, 必须包含{context}和{question}两个字段",
                                 default=DEFAULT_KB_PROMPT_TEMPLATE)


class WebSearchConfig(BaseModel):
    name: str = Field(description="应用联网搜索的名称")
    prompt_search_template: str = Field(
        description="应用联网搜索的提示词模板, 必须包含{seach_info}和{question}两个字段",
        default=DEFAULT_WEB_SEARCH_PROMPT_TEMPLATE)
    prompt_search_kb_template: str = Field(
        description="应用知识库的提示词模板, 必须包含{search_info},{context}和{question}三个字段",
        default=DEFAULT_WEB_SEARCH_KB_PROMPT_TEMPLATE)
