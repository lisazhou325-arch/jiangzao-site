# Agent Skill 从使用到原理，一次讲清

> **原标题**: Agent Skill 从使用到原理，一次讲清
> **来源**: Bilibili - 马克的技术工作坊
> **时长**: 17:42
> **查看视频**: https://www.bilibili.com/video/BV1cGigBQE6n

---

## 摘要
本期视频深入解析了Anthropic最近正式发布的Agent Skill开放标准，将其从单一工具提升为AI领域的通用设计模式。视频首先通俗地将Agent Skill定义为大模型可随时查阅的“说明书”，并通过一个会议总结助手的实战案例，详细演示了如何通过编写Markdown文件来定义任务规则。随后，视频重点讲解了Skill的高级用法，包括按需加载资料的Reference和能够自动执行任务的Script，揭示了其通过“渐进式披露”机制来极致节省Token的核心原理。最后，视频对比了Agent Skill与MCP（Model Context Protocol）的区别，明确了MCP负责连接数据，而Skill负责教模型如何处理数据的互补关系。

## 亮点
- 📄 Agent Skill 本质上就是大模型的一份“说明书”，通过预设的规则文档，让模型在处理特定任务（如会议总结）时无需用户重复输入冗长的指令 [01:07]
- ⚙️ 一个标准的 Skill 文件（.md）由头部的元数据（Metadata）和正文的指令（Instruction）组成，前者用于让模型识别功能，后者用于描述具体的执行规则 [02:37]
- 🧠 Agent Skill 采用按需加载机制，模型首先只读取所有 Skill 的名称和描述，只有在确定匹配用户需求后，才会加载具体的指令内容 [04:47]
- 📉 高级功能 Reference（引用）实现了“按需中的按需”，例如只有在会议内容涉及金钱时，才会触发加载财务手册文件，极大地节省了上下文 Token [06:21]
- ⚡ 相比于 Reference 是被模型“读取”内容，Script（脚本）功能则是被模型“执行”，模型通常只关心运行结果而不占用上下文去读取代码本身 [09:07]
- 🏗️ Agent Skill 的架构采用了三层“渐进式披露”结构：始终可见的元数据层、被选中才加载的指令层，以及条件触发的资源层（Reference/Script） [10:04]
- ⚖️ Agent Skill 与 MCP 的核心区别在于：MCP 负责连接外部数据（Connect Data），而 Skill 负责教会模型如何处理这些数据（Teach what to do） [11:32]

#AgentSkill #Anthropic #ClaudeCode #MCP #AI开发

## 思考
1. **Agent Skill 和 Prompt Engineering（提示词工程）有什么本质区别？**
  - Prompt 通常是在单次对话中临时输入的，而 Agent Skill 是将这些 Prompt 结构化、持久化为标准文件（.md）。Skill 具有更高的复用性，支持按需加载和调用外部脚本，更适合构建复杂的、标准化的工作流，相当于把最佳实践固化成了“软件”。

2. **为什么有了 Reference 功能，还需要 Script 功能？**
  - Reference 适用于静态资料的查询，比如规章制度或文档，模型需要阅读内容来辅助回答。而 Script 适用于执行具体动作，比如上传文件、发送邮件或运行复杂的计算逻辑。Script 可以让 Agent 具备“手”的能力，真正去改变外部系统的状态，且通常比纯文本处理更精确、更省 Token。

## 术语解释
- **Agent Skill**: Anthropic 推出的开放标准，一种让 AI 模型学习特定任务处理流程的设计模式，通过结构化的文档教会模型“如何做某事”。
- **MCP (Model Context Protocol)**: 模型上下文协议，主要用于标准化 AI 模型连接外部数据源（如数据库、API）的方式，侧重于数据的获取。
- **Reference**: Agent Skill 的一种高级属性，指在特定条件满足时才被加载给模型的外部文件（如手册、文档），用于补充上下文信息。
- **Script**: Agent Skill 中用于执行具体操作的代码脚本（如 Python 文件），模型调用它来完成上传、计算等任务，通常只关注执行结果。
- **渐进式披露 (Progressive Disclosure)**: 视频中提到的设计理念，指信息不是一次性全部丢给模型，而是分层级（元数据 -> 指令 -> 资源）根据需求逐步加载，以最大化节省 Token 消耗。

---

**处理时间**: 2026-01-02 17:49:23 UTC
**数据来源**: BibiGPT API
**字幕质量**: 自动生成（中文）
