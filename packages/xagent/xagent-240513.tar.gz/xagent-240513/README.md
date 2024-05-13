# XAgents

XAgents项目为在大模型服务基础上的中间件，为了避免各个业务线重复开发，提供统一的程序接口，快速支持各种业务的需求

## 主要能力

- 接入各种模型服务，包括zhipu sdk, 本地LLM，embedding模型，rerank模型，NLU模型等
- 知识库的管理
- RAG的能力
- 工具调用的能力

具体设计参考[设计文档](https://zhipu-ai.feishu.cn/docx/Y78IdJZSmoESK0x0HZpc7vrWnde)

## 接入方式

### python SDK（python程序快速接入）

#### install

基于python3.10以上版本
  `pip install -U xagent`

#### http Service

开发环境: 117.50.174.44:8001

测试环境: http://hz-model.bigmodel.cn/xagent/docs
生产环境: http://hz-model.bigmodel.cn/xagent/docs



测试代码

```shell
curl -X 'POST' \
  'http://localhost:8001/kb/list' \
  -H 'accept: application/json' \
  -H 'Authorization: Basic emhpcHU6emhpcHU=' \
  -d ''
```

具体接口文档参考 http://hz-model.bigmodel.cn/xagent/docs

### 相关文档
- [Release Note](https://zhipu-ai.feishu.cn/docx/QXwtddguRomAnjxUFdFch9pGndb?from=from_copylink)
- [开发规范](https://zhipu-ai.feishu.cn/docx/M4lKdfMbKoAQNAxGAjxcZDH3nBe?from=from_copylink)
- [部署方案](https://zhipu-ai.feishu.cn/docx/JzkzdgFiZolcgCxG5tacennWn1k?from=from_copylink)
- [示例请求](https://zhipu-ai.feishu.cn/docx/QrnrdOj6Mo7MzwxrpJgc4kIZnfb?from=from_copylink)

