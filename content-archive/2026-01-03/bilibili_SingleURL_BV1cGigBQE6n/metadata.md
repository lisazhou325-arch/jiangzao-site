---
id: "BV1cGigBQE6n"
title: "Agent Skill 从使用到原理，一次讲清"
platform: "bilibili"
url: "https://www.bilibili.com/video/BV1cGigBQE6n"
published_at: "2026-01-03"
processed_at: "2026-01-02T17:49:23.368679Z"
duration: "17:42"
duration_seconds: 1062

uploader: "马克的技术工作坊"
uid: "1815948385"

cover_url: "http://i1.hdslb.com/bfs/archive/a70af317a725a3cbd1ad7d94e0ecb2d3eb679fd1.jpg"

transcript_language: "zh-Hans"
transcript_source: "bibigpt"

synced_to_feishu: false
---

# Agent Skill 从使用到原理，一次讲清

## 摘要
本期视频深入解析了Anthropic最近正式发布的Agent Skill开放标准，将其从单一工具提升为AI领域的通用设计模式。视频首先通俗地将Agent Skill定义为大模型可随时查阅的“说明书”，并通过一个会议总结助手的实战案例，详细演示了如何通过编写Markdown文件来定义任务规则。随后，视频重点讲解了Skill的高级用法，包括按需加载资料的Reference和能够自动执行任务的Script，揭示了其通过“渐进式披露”机制来极致节省Token的核心原理。最后，视频对比了Agent Skill与MCP（Model Context Protocol）的区别，明确了MCP负责连接数据，而Skill负责教模型如何处理数据的互补关系。

## 亮点
- 📄 Agent Skill 本质上就是大模型的一份“说明书”，通过预设的规则文档，让模型在处理特定任务（如会议总结）时无需用户重复输入冗长的指令 [01:07]
- ⚙️ 一个标准的 Skill 文件（.md）由头部的元数据（Metadata）和正文的指令（Instruction）组成，前者用于让模型识别功能，后者用于描述具体...

(查看 rewritten.md 获取完整摘要)
