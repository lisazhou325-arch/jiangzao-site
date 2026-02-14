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
    <nav className="w-full">
      <div className="text-[11px] font-medium tracking-widest uppercase text-stone-400 mb-4">
        目录
      </div>
      <ul className="space-y-0.5 border-l border-stone-200">
        {items.map((item) => (
          <li key={item.id}>
            <a
              href={`#${item.id}`}
              className={`block text-[13px] leading-7 transition-colors duration-150 ${
                item.level === 3 ? "pl-5" : "pl-3"
              } ${
                activeId === item.id
                  ? "text-indigo-600 border-l-2 border-indigo-500 -ml-px font-medium"
                  : "text-stone-400 hover:text-stone-600"
              }`}
            >
              {item.text}
            </a>
          </li>
        ))}
      </ul>
    </nav>
  );
}
