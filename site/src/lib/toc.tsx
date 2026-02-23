"use client";

import { useEffect, useState } from "react";
import type { TocItem } from "./toc-utils";

export function TableOfContents({ items }: { items: TocItem[] }) {
  const [activeId, setActiveId] = useState<string>("");

  useEffect(() => {
    const headings = items
      .map((item) => document.getElementById(item.id))
      .filter(Boolean) as HTMLElement[];
    if (headings.length === 0) return;

    const observer = new IntersectionObserver(
      (entries) => {
        for (const entry of entries) {
          if (entry.isIntersecting) {
            setActiveId(entry.target.id);
            break;
          }
        }
      },
      { rootMargin: "-80px 0px -60% 0px", threshold: 0 }
    );
    headings.forEach((h) => observer.observe(h));
    return () => observer.disconnect();
  }, [items]);

  if (items.length === 0) return null;

  return (
    <nav className="floating-toc">
      <div
        className="font-mono mb-3"
        style={{
          fontSize: "0.55rem",
          letterSpacing: "0.15em",
          textTransform: "uppercase",
          color: "var(--muted)",
          paddingBottom: "8px",
          borderBottom: "1px solid var(--border)",
        }}
      >
        目录
      </div>
      <ul className="space-y-0.5">
        {items.map((item) => (
          <li key={item.id}>
            <a
              href={`#${item.id}`}
              className="toc-link"
              data-active={activeId === item.id ? "true" : undefined}
              style={{
                paddingLeft: item.level === 3 ? "14px" : "8px",
              }}
            >
              {item.text}
            </a>
          </li>
        ))}
      </ul>
    </nav>
  );
}
