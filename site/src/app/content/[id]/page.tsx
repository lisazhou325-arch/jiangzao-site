import { getRecordWithCover, getRecords } from "@/lib/feishu";
import { MarkdownContent } from "@/lib/markdown";
import { TableOfContents } from "@/lib/toc";
import { extractToc } from "@/lib/toc-utils";
import Link from "next/link";

export const revalidate = 3600;

export async function generateStaticParams() {
  const records = await getRecords();
  return records.map((r) => ({ id: r.id }));
}

function formatDate(ts: number): string {
  if (!ts) return "";
  const d = new Date(ts);
  return `${d.getFullYear()}年${d.getMonth() + 1}月${d.getDate()}日`;
}

function parseGuests(raw: string): { name: string; role: string }[] {
  if (!raw) return [];
  return raw.split(/[,，]/).map((g) => {
    const match = g.trim().match(/^(.+?)\s*[（(](.+?)[）)]$/);
    if (match) return { name: match[1].trim(), role: match[2].trim() };
    return { name: g.trim(), role: "" };
  });
}

function platformLabel(p: string): string {
  const map: Record<string, string> = {
    YOUTUBE: "YouTube", BILIBILI: "Bilibili",
    "B站": "Bilibili", 小宇宙: "小宇宙", Youtube: "YouTube",
  };
  return map[p] || p;
}

function stripQuotesSection(body: string): string {
  let result = body.replace(/\n## 金句[^\n]*\n[\s\S]*?(?=\n## |\n# |$)/, "");
  result = result.replace(/^金句精选\n[\s\S]*?(?=\n---\n)/, "");
  result = result.replace(/\n金句精选\n[\s\S]*?(?=\n---\n)/, "");
  return result;
}

export default async function ContentPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  const record = await getRecordWithCover(id);
  const guests = parseGuests(record.guests);
  const bodyWithoutQuotes = stripQuotesSection(record.body);
  const tocItems = extractToc(bodyWithoutQuotes);

  return (
    <main className="min-h-screen" style={{ background: "var(--paper)" }}>

      {/* Top nav */}
      <div className="sticky top-0 z-50 paper-nav">
        <div className="container mx-auto px-6 sm:px-10 lg:px-16 py-3 flex items-center justify-between">
          <Link href="/" className="paper-btn">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M15 18l-6-6 6-6" />
            </svg>
            返回
          </Link>
          <span
            className="font-serif"
            style={{ fontSize: "1.2rem", color: "var(--ink)", letterSpacing: "-0.02em" }}
          >
            降<em style={{ fontStyle: "italic", color: "var(--gold)" }}>噪</em>
          </span>
        </div>
      </div>

      {/* Cover */}
      <div className="container mx-auto px-6 sm:px-10 lg:px-16 pt-8">
        <div
          className="relative w-full overflow-hidden animate-fade-up"
          style={{
            aspectRatio: "21/9",
            maxHeight: 460,
            borderRadius: 8,
            background: "var(--paper-warm)",
            border: "1px solid var(--border)",
          }}
        >
          {record.coverFileToken ? (
            <>
              <img
                alt={record.title}
              src={`/api/cover?token=${record.coverFileToken}`}
                className="w-full h-full object-cover"
                style={{ opacity: 0.88 }}
              />
              <div
                className="absolute inset-0"
                style={{ background: "linear-gradient(to top, rgba(26,22,18,0.72) 0%, rgba(26,22,18,0.15) 55%, transparent 100%)" }}
              />
            </>
          ) : (
            <div className="absolute inset-0 flex items-center justify-center">
              <span className="font-serif" style={{ fontSize: "5rem", color: "var(--gold-light)", opacity: 0.3 }}>◇</span>
            </div>
          )}

          {/* Overlay */}
          <div className="absolute inset-0 flex items-end">
            <div className="px-8 sm:px-10 pb-8 sm:pb-10 w-full">
              {record.tags.length > 0 && (
                <div className="flex flex-wrap gap-2 mb-3">
                  {record.tags.map((tag) => (
                    <span
                      key={tag}
                      className="font-mono"
                      style={{
                        display: "inline-block",
                        padding: "2px 8px",
                        border: "1px solid rgba(253,252,248,0.3)",
                        borderRadius: 2,
                        fontSize: "0.6rem",
                        letterSpacing: "0.08em",
                        textTransform: "uppercase",
                        color: "rgba(253,252,248,0.7)",
                        background: "rgba(253,252,248,0.08)",
                        backdropFilter: "blur(4px)",
                      }}
                    >
                      {tag}
                    </span>
                  ))}
                </div>
              )}
              <h1
                className="font-serif"
                style={{
                  fontSize: "clamp(1.6rem, 3.5vw, 2.8rem)",
                  fontWeight: 400,
                  lineHeight: 1.2,
                  color: "var(--paper)",
                  letterSpacing: "-0.02em",
                  maxWidth: "75%",
                }}
              >
                {record.title}
              </h1>
              <div className="flex flex-wrap items-center gap-4 mt-3">
                {guests.map((guest, i) => (
                  <span key={i} className="font-mono" style={{ fontSize: "0.68rem", color: "rgba(253,252,248,0.6)", letterSpacing: "0.04em" }}>
                    {guest.name}
                    {guest.role && <span style={{ opacity: 0.5 }}> · {guest.role}</span>}
                  </span>
                ))}
                {record.publishDate > 0 && (
                  <span className="font-mono" style={{ fontSize: "0.65rem", color: "rgba(253,252,248,0.45)", letterSpacing: "0.06em" }}>
                    {formatDate(record.publishDate)}
                  </span>
                )}
                {record.platform && (
                  <span className="font-mono" style={{ fontSize: "0.65rem", color: "rgba(253,252,248,0.45)", letterSpacing: "0.06em" }}>
                    {platformLabel(record.platform)}
                  </span>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Article */}
      <div className="container mx-auto px-6 sm:px-10 lg:px-16 py-12 sm:py-16">
        <div className="max-w-6xl mx-auto flex gap-10 items-start">

          {/* Floating TOC - sticky on left */}
          {tocItems.length > 0 && (
            <aside className="hidden xl:block w-48 flex-shrink-0">
              <div className="sticky top-20">
                <TableOfContents items={tocItems} />
              </div>
            </aside>
          )}

          {/* Content */}
          <div className="flex-1 min-w-0 max-w-3xl">

            {record.sourceLink && (
              <div className="mb-8">
                <a
                  href={record.sourceLink.link}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="paper-btn-gold"
                >
                  <span>查看原始内容</span>
                  <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6" />
                    <polyline points="15 3 21 3 21 9" />
                    <line x1="10" y1="14" x2="21" y2="3" />
                  </svg>
                </a>
              </div>
            )}

            {/* Quotes */}
            {record.quotes.length > 0 && (
              <div className="mb-12 space-y-4">
                {record.quotes.map((q, i) => (
                  <div key={i} className="paper-quote">
                    <p className="font-serif" style={{ fontSize: "1rem", lineHeight: 1.8, color: "var(--ink-light)", fontStyle: "italic" }}>
                      {q}
                    </p>
                  </div>
                ))}
              </div>
            )}

            {/* Article body */}
            <div style={{ borderTop: "2px solid var(--ink)", paddingTop: "2rem" }}>
              <MarkdownContent content={bodyWithoutQuotes} />
            </div>
          </div>
        </div>
      </div>

      {/* Bottom */}
      <div className="container mx-auto px-6 sm:px-10 lg:px-16 pb-16">
        <div className="max-w-6xl mx-auto flex items-center justify-between" style={{ borderTop: "1px solid var(--border)", paddingTop: "2rem" }}>
          <Link href="/" className="paper-btn">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M15 18l-6-6 6-6" />
            </svg>
            查看更多内容
          </Link>
          <span className="font-serif" style={{ fontSize: "0.9rem", color: "var(--muted)", fontStyle: "italic" }}>降噪</span>
        </div>
      </div>

    </main>
  );
}
