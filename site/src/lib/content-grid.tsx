"use client";

import { useState, useMemo } from "react";
import Link from "next/link";

interface ContentItem {
  id: string;
  title: string;
  guests: string;
  platform: string;
  publishDate: number;
  coverFileToken?: string | null;
  tags: string[];
}

function formatDate(ts: number): string {
  if (!ts) return "";
  const d = new Date(ts);
  return `${d.getFullYear()}/${String(d.getMonth() + 1).padStart(2, "0")}/${String(d.getDate()).padStart(2, "0")}`;
}

function platformLabel(p: string): string {
  const map: Record<string, string> = {
    YOUTUBE: "YouTube", Youtube: "YouTube",
    BILIBILI: "Bilibili", "B站": "Bilibili",
    小宇宙: "小宇宙",
  };
  return map[p] || p;
}

const TAG_SYSTEM = [
  { key: null, label: "All" },
  { key: "__new__", label: "New" },
  { key: "AI Coding", label: "AI Coding" },
  { key: "AI Products", label: "AI Products" },
  { key: "AI Organization", label: "AI Organization" },
  { key: "AI Business", label: "AI Business" },
  { key: "AI Principles", label: "AI Principles" },
  { key: "Personal Productivity", label: "Personal Productivity" },
  { key: "Physical AI", label: "Physical AI" },
];

export function ContentGrid({ records }: { records: ContentItem[] }) {
  const [activeTag, setActiveTag] = useState<string | null>(null);
  const [search, setSearch] = useState("");

  // Filter records
  const filtered = useMemo(() => {
    let result = records;
    if (activeTag === "__new__") {
      // Show latest 5
      result = result.slice(0, 5);
    } else if (activeTag) {
      result = result.filter((r) => r.tags.includes(activeTag));
    }
    if (search.trim()) {
      const q = search.trim().toLowerCase();
      result = result.filter(
        (r) =>
          r.title.toLowerCase().includes(q) ||
          r.guests.toLowerCase().includes(q) ||
          r.tags.some((t) => t.toLowerCase().includes(q))
      );
    }
    return result;
  }, [records, activeTag, search]);

  return (
    <>
      {/* Search box */}
      <div className="mb-6">
        <div className="relative">
          <svg
            className="absolute left-3 top-1/2 -translate-y-1/2"
            width="15" height="15" viewBox="0 0 24 24" fill="none"
            stroke="var(--muted)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"
          >
            <circle cx="11" cy="11" r="8" />
            <path d="M21 21l-4.35-4.35" />
          </svg>
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="搜索标题、嘉宾、标签..."
            className="w-full font-mono"
            style={{
              padding: "10px 12px 10px 36px",
              fontSize: "0.78rem",
              border: "1px solid var(--border)",
              borderRadius: "4px",
              background: "var(--paper-warm)",
              color: "var(--ink)",
              outline: "none",
              letterSpacing: "0.02em",
            }}
            onFocus={(e) => (e.target.style.borderColor = "var(--gold)")}
            onBlur={(e) => (e.target.style.borderColor = "var(--border)")}
          />
        </div>
      </div>

      {/* Tag filters */}
      <div className="flex flex-wrap gap-2 mb-10">
        {TAG_SYSTEM.map((t) => (
          <button
            key={t.label}
            onClick={() => setActiveTag(activeTag === t.key ? null : t.key)}
            className={activeTag === t.key ? "paper-tag-active" : "paper-tag-filter"}
          >
            {t.label}
          </button>
        ))}
      </div>

      {/* Results count */}
      {(activeTag || search.trim()) && (
        <div className="mb-6">
          <span className="font-mono" style={{ fontSize: "0.6rem", color: "var(--muted)", letterSpacing: "0.1em" }}>
            {filtered.length} 篇结果
            {activeTag && <> · 标签: {activeTag}</>}
            {search.trim() && <> · 关键词: {search.trim()}</>}
          </span>
        </div>
      )}

      {/* Card grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6 sm:gap-8">
        {filtered.map((r, i) => (
          <Link
            key={r.id}
            href={`/content/${r.id}`}
            className="paper-card animate-card-in block"
            style={{ animationDelay: `${i * 60}ms` }}
          >
            {/* Cover */}
            <div className="relative overflow-hidden" style={{ aspectRatio: "16/9", background: "var(--paper-dark)" }}>
              {r.coverFileToken ? (
                <img
                  src={`/api/cover?token=${r.coverFileToken}`}
                  alt={r.title}
                  className="w-full h-full object-cover"
                  style={{ transition: "transform 0.5s ease" }}
                  onMouseOver={(e) => (e.currentTarget.style.transform = "scale(1.04)")}
                  onMouseOut={(e) => (e.currentTarget.style.transform = "scale(1)")}
                />
              ) : (
                <div className="w-full h-full flex items-center justify-center">
                  <span className="font-serif" style={{ fontSize: "2.5rem", color: "var(--border-dark)" }}>◇</span>
                </div>
              )}
              {/* Platform badge */}
              <span
                className="absolute top-3 left-3 font-mono"
                style={{
                  fontSize: "0.55rem", letterSpacing: "0.1em", textTransform: "uppercase",
                  padding: "3px 8px", background: "rgba(253,252,248,0.92)", borderRadius: "2px",
                  color: "var(--ink-light)", backdropFilter: "blur(4px)",
                }}
              >
                {platformLabel(r.platform)}
              </span>
            </div>

            {/* Info */}
            <div className="p-5">
              <time className="font-mono block mb-2" style={{ fontSize: "0.6rem", color: "var(--muted)", letterSpacing: "0.08em" }}>
                {formatDate(r.publishDate)}
              </time>
              <h2 className="font-serif" style={{ fontSize: "1.05rem", fontWeight: 400, lineHeight: 1.4, color: "var(--ink)", letterSpacing: "-0.01em" }}>
                {r.title}
              </h2>
              {r.guests && (
                <p className="mt-2 font-mono" style={{ fontSize: "0.65rem", color: "var(--gold)", letterSpacing: "0.05em" }}>
                  {r.guests.split(/[,，]/)[0].trim()}
                </p>
              )}
              {r.tags.length > 0 && (
                <div className="flex flex-wrap gap-1.5 mt-3">
                  {r.tags.slice(0, 2).map((tag) => (
                    <span key={tag} className="paper-tag">{tag}</span>
                  ))}
                </div>
              )}
            </div>
          </Link>
        ))}
      </div>

      {filtered.length === 0 && (
        <div className="text-center py-24">
          <p className="font-serif" style={{ fontSize: "3rem", color: "var(--border-dark)" }}>◇</p>
          <p className="font-mono mt-4" style={{ fontSize: "0.7rem", color: "var(--muted)", letterSpacing: "0.1em", textTransform: "uppercase" }}>
            {records.length === 0 ? "暂无内容，敬请期待" : "没有匹配的内容"}
          </p>
        </div>
      )}
    </>
  );
}
