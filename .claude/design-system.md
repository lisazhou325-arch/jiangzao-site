# 降噪网站设计规范 — Paper 纸质卡片风格

## 设计理念

报纸/杂志质感，温暖克制。米白纸张底色 + 深棕近黑文字 + 暖金强调色，衬线字体做标题，等宽字体做标签，整体传递「精选、可信赖、有温度」的内容平台气质。

---

## 色彩系统

| 变量 | 色值 | 用途 |
|------|------|------|
| `--paper` | `#fdfcf8` | 主背景 |
| `--paper-warm` | `#f5f0e8` | 卡片占位、引用背景 |
| `--paper-dark` | `#ede9e0` | 图片占位背景 |
| `--ink` | `#1a1612` | 主文字、标题、粗横线 |
| `--ink-light` | `#3d3530` | 正文内容 |
| `--muted` | `#8a7d6e` | 辅助文字、标签、日期 |
| `--gold` | `#a0855a` | 强调色：斜体标题、左边框、引号 |
| `--gold-light` | `#c4a882` | 金色浅版：大引号装饰 |
| `--border` | `#e0dcd0` | 普通边框 |
| `--border-dark` | `#c8c4b8` | hover 边框 |

---

## 字体

| 用途 | 字体 | CSS 变量 |
|------|------|----------|
| 展示标题（Logo、大标题、卡片标题） | Instrument Serif (Google Fonts) | `var(--font-serif)` |
| 标签、日期、徽章、按钮、目录标题 | JetBrains Mono (Google Fonts) | `var(--font-mono)` |
| 正文内容 | PingFang SC / Noto Sans SC / system-ui | — |

**关键排版规则：**
- 大标题：`font-weight: 400`，`letter-spacing: -0.03em`，斜体"噪"字用 `color: var(--gold)`
- 卡片标题：Instrument Serif，`font-weight: 400`，`letter-spacing: -0.01em`
- 所有标签/元数据：JetBrains Mono，`font-size: 0.6rem`，`letter-spacing: 0.1em`，`text-transform: uppercase`

---

## 阴影系统

```css
--shadow-sm: 0 1px 4px rgba(26,22,18,0.06);
--shadow-md: 0 4px 16px rgba(26,22,18,0.08);
--shadow-lg: 0 8px 32px rgba(26,22,18,0.1);
```

---

## 核心组件

### 卡片 `.paper-card`
- 背景：`var(--paper)`，边框：`1px solid var(--border)`，圆角：`8px`
- hover：`box-shadow: var(--shadow-lg)`，`transform: translateY(-4px)`，边框变深
- 图片比例：`3:2`

### 标签 `.paper-tag`
- 背景：`var(--paper-warm)`，边框：`1px solid var(--border)`，圆角：`2px`
- 字体：JetBrains Mono，`0.6rem`，uppercase

### 徽章 `.paper-badge`
- 同标签样式，带 `display: inline-flex`，可内嵌小圆点

### 按钮 `.paper-btn`
- 默认：白底 + 深色边框，hover：背景变 `var(--ink)`，文字变 `var(--paper)`
- `.paper-btn-gold`：金色边框版本

### 金句引用 `.paper-quote`
- 左边框：`3px solid var(--gold)`
- 背景：`var(--paper-warm)`，圆角右侧：`6px`
- `::before` 大引号：Instrument Serif，`3.5rem`，`color: var(--gold-light)`，`opacity: 0.5`

### 导航栏 `.paper-nav`
- 毛玻璃：`background: rgba(253,252,248,0.94)`，`backdrop-filter: blur(12px)`
- 底部：`1px solid var(--border)`

### 分割线
- `.rule-heavy`：`border-top: 2px solid var(--ink)` — 用于 Hero 标题下方
- `.rule-light`：`border-top: 1px solid var(--border)` — 用于内容分区

---

## 首页结构

```
顶部信息条（三列：AI精选·人工策展 / Issue编号 / 篇数）
  ↓ border-bottom: 1px
大标题「降噪」（Instrument Serif，超大，斜体金色"噪"）
  ↓ border-bottom: 2px solid var(--ink)
Section Label + 横线
内容网格（3列，gap-8）
Footer（rule-heavy + Logo + 按钮）
```

---

## 详情页结构

```
sticky 导航栏（返回按钮 + 品牌名）
封面图（21:9，圆角8px，渐变遮罩，标题/嘉宾/日期叠加）
  ↓ 正文区域（max-w-6xl，TOC左侧 + 内容右侧）
    源链接按钮
    金句区块（paper-quote）
    文章正文（prose，h2带上边框线）
底部导航（rule-heavy + 返回链接）
```

---

## 动画

```css
/* 页面入场 */
.animate-fade-up: fadeUp 0.65s cubic-bezier(0.16, 1, 0.3, 1)
  from: opacity:0, translateY(18px)

/* 卡片入场（stagger） */
.animate-card-in: cardIn 0.5s cubic-bezier(0.16, 1, 0.3, 1)
  delay: index * 55ms
  from: opacity:0, translateY(12px)
```

---

## 实现文件

| 文件 | 职责 |
|------|------|
| `site/src/app/globals.css` | CSS 变量、工具类、组件样式 |
| `site/src/app/layout.tsx` | 引入 Instrument Serif + JetBrains Mono |
| `site/src/app/page.tsx` | 首页：报头 + 网格 |
| `site/src/app/content/[id]/page.tsx` | 详情页：封面 + 正文 |
| `site/src/lib/markdown.tsx` | Markdown 渲染：衬线标题 + paper-quote |
| `site/src/lib/toc.tsx` | 目录：金色左边框指示活跃项 |
