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
    <main className="min-h-screen bg-white">
      {/* Top bar */}
      <div className="sticky top-0 z-50 glass border-b border-slate-200/40">
        <div className="container mx-auto px-5 sm:px-8 lg:px-12 py-3 flex items-center gap-3">
          <Link
            href="/"
            className="inline-flex items-center gap-1.5 text-sm text-slate-500 hover:text-slate-800 transition-colors"
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M15 18l-6-6 6-6" />
            </svg>
            返回
          </Link>
          <span className="text-slate-300">·</span>
          <span className="text-sm font-medium text-slate-700 truncate">降噪</span>
        </div>
      </div>

      {/* Hero cover image */}
      <div className="relative w-full h-[50vh] min-h-[360px] max-h-[540px] overflow-hidden bg-slate-900">
        {record.coverUrl ? (
          <>
            <img
              alt={record.title}
              src={record.coverUrl}
              className="w-full h-full object-cover"
            />
            <div className="absolute inset-0 bg-gradient-to-t from-slate-900 via-slate-900/50 to-slate-900/20" />
          </>
        ) : (
          <div className="absolute inset-0 bg-gradient-to-br from-slate-800 to-slate-900" />
        )}

        {/* Title overlay on cover */}
        <div className="absolute inset-0 flex items-end">
          <div className="container mx-auto px-5 sm:px-8 lg:px-12 pb-10 sm:pb-14">
            <div className="max-w-3xl animate-fade-in">
              {record.tags.length > 0 && (
                <div className="flex flex-wrap gap-2 mb-4">
                  {record.tags.map((tag) => (
                    <span
                      key={tag}
                      className="px-2.5 py-0.5 rounded-full text-[11px] font-medium bg-white/15 text-white/80 border border-white/10 backdrop-blur-sm"
                    >
                      {tag}
                    </span>
                  ))}
                </div>
              )}
              <h1 className="text-3xl sm:text-4xl lg:text-[2.75rem] font-bold text-white leading-tight tracking-tight mb-5">
                {record.title}
              </h1>
              <div className="flex flex-wrap items-center gap-4 text-sm">
                {guests.length > 0 && (
                  <div className="flex flex-wrap gap-x-2 text-white/70">
                    {guests.map((guest, i) => (
                      <span key={i}>
                        {guest.name}
                        {guest.role && <span className="text-white/40 text-xs ml-1">({guest.role})</span>}
                      </span>
                    ))}
                  </div>
                )}
                {record.publishDate > 0 && (
                  <span className="text-white/50">{formatDate(record.publishDate)}</span>
                )}
                {record.platform && (
                  <span className="text-white/50">{platformLabel(record.platform)}</span>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Article body: TOC left + content right */}
      <div className="container mx-auto px-5 sm:px-8 lg:px-12 py-12 sm:py-16">
        <div className="flex gap-10 items-start max-w-6xl mx-auto">
          {/* TOC sidebar - left */}
          <aside className="hidden lg:block w-56 flex-shrink-0">
            <div className="sticky top-20">
              <TableOfContents items={tocItems} />
            </div>
          </aside>

          {/* Main content */}
          <div className="flex-1 min-w-0">
            {record.sourceLink && (
              <div className="mb-8 pb-8 border-b border-slate-100">
                <a
                  href={record.sourceLink.link}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-2 text-sm text-indigo-600 hover:text-indigo-700 transition-colors"
                >
                  <span>查看原始内容</span>
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6" />
                    <polyline points="15 3 21 3 21 9" />
                    <line x1="10" y1="14" x2="21" y2="3" />
                  </svg>
                </a>
              </div>
            )}
            <article>
              <MarkdownContent content={bodyWithoutQuotes} />
            </article>
          </div>
        </div>
      </div>

      {/* Bottom nav */}
      <div className="container mx-auto px-5 sm:px-8 lg:px-12 pb-16">
        <div className="max-w-6xl mx-auto border-t border-slate-100 pt-8">
          <Link
            href="/"
            className="inline-flex items-center gap-2 text-sm text-slate-500 hover:text-slate-800 transition-colors"
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M15 18l-6-6 6-6" />
            </svg>
            查看更多内容
          </Link>
        </div>
      </div>
    </main>
  );
}
