"use client";

import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import type { Components } from "react-markdown";
import React from "react";
import { slugify } from "./toc-utils";

function childrenToText(children: React.ReactNode): string {
  if (typeof children === "string") return children;
  if (Array.isArray(children)) return children.map(childrenToText).join("");
  if (React.isValidElement(children) && children.props) {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const props = children.props as any;
    if (props.children) {
      return childrenToText(props.children);
    }
  }
  return String(children ?? "");
}

const components: Components = {
  h1: ({ children }) => {
    const text = childrenToText(children);
    return (
      <h1 id={slugify(text)} className="font-serif mt-10 mb-4" style={{ fontSize: "1.6rem", fontWeight: 400, color: "var(--ink)", letterSpacing: "-0.02em", lineHeight: 1.25 }}>
        {children}
      </h1>
    );
  },
  h2: ({ children }) => {
    const text = childrenToText(children);
    return (
      <h2
        id={slugify(text)}
        className="font-serif mt-12 mb-5"
        style={{
          fontSize: "1.35rem",
          fontWeight: 700,
          color: "var(--ink)",
          letterSpacing: "-0.01em",
          lineHeight: 1.4,
          padding: "0.75rem 1rem",
          borderLeft: "4px solid var(--gold)",
          background: "linear-gradient(to right, rgba(160,133,90,0.07), transparent)",
          borderRadius: "0 4px 4px 0",
        }}
      >
        {children}
      </h2>
    );
  },
  h3: ({ children }) => {
    const text = childrenToText(children);
    return (
      <h3
        id={slugify(text)}
        className="font-serif mt-9 mb-3"
        style={{
          fontSize: "1.12rem",
          fontWeight: 600,
          color: "var(--ink)",
          paddingLeft: "0.75rem",
          borderLeft: "3px solid var(--border-dark)",
        }}
      >
        {children}
      </h3>
    );
  },
  blockquote: ({ children }) => (
    <blockquote className="paper-quote my-6 not-italic">
      {children}
    </blockquote>
  ),
};

export function MarkdownContent({ content }: { content: string }) {
  const bodyContent = content.replace(/^#\s+.+\n/, "");
  return (
    <article
      className="prose max-w-none prose-p:leading-[1.9] prose-li:leading-[1.8]"
      style={{ color: "var(--ink-light)", fontFamily: "'PingFang SC', 'Noto Sans SC', system-ui, sans-serif" }}
    >
      <ReactMarkdown remarkPlugins={[remarkGfm]} components={components}>
        {bodyContent}
      </ReactMarkdown>
    </article>
  );
}
