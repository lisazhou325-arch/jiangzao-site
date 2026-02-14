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
      <h1 id={slugify(text)} className="text-2xl font-bold mt-12 mb-5 text-stone-900 tracking-tight">
        {children}
      </h1>
    );
  },
  h2: ({ children }) => {
    const text = childrenToText(children);
    return (
      <h2 id={slugify(text)} className="text-xl font-bold mt-14 mb-4 text-stone-900 tracking-tight flex items-center gap-3">
        <span className="inline-block w-0.5 h-5 rounded-full bg-indigo-400 shrink-0" />
        {children}
      </h2>
    );
  },
  h3: ({ children }) => {
    const text = childrenToText(children);
    return (
      <h3 id={slugify(text)} className="text-lg font-semibold mt-10 mb-3 text-stone-800 tracking-tight">
        {children}
      </h3>
    );
  },
  blockquote: ({ children }) => (
    <blockquote className="border-l-2 border-indigo-300 bg-indigo-50/40 rounded-r-lg pl-4 pr-4 py-3 my-5 text-stone-600 not-italic text-[15px] leading-relaxed">
      {children}
    </blockquote>
  ),
};

export function MarkdownContent({ content }: { content: string }) {
  const bodyContent = content.replace(/^#\s+.+\n/, "");
  return (
    <article className="prose prose-stone prose-lg max-w-none prose-headings:font-bold prose-headings:tracking-tight prose-p:text-stone-600 prose-p:leading-[1.8] prose-li:text-stone-600 prose-strong:text-stone-800 prose-a:text-indigo-600 prose-a:no-underline hover:prose-a:underline">
      <ReactMarkdown remarkPlugins={[remarkGfm]} components={components}>
        {bodyContent}
      </ReactMarkdown>
    </article>
  );
}
