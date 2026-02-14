import { getRecordsWithCovers } from "@/lib/feishu";
import Link from "next/link";

export const revalidate = 3600;

function formatDate(ts: number): string {
  if (!ts) return "";
  const d = new Date(ts);
  return `${d.getFullYear()}/${String(d.getMonth() + 1).padStart(2, "0")}/${String(d.getDate()).padStart(2, "0")}`;
}

const tagColors = [
  "bg-stone-100 text-stone-600",
  "bg-amber-50 text-amber-700",
  "bg-indigo-50 text-indigo-600",
  "bg-emerald-50 text-emerald-700",
  "bg-rose-50 text-rose-600",
  "bg-cyan-50 text-cyan-700",
  "bg-violet-50 text-violet-600",
  "bg-teal-50 text-teal-700",
];

function getTagColor(index: number): string {
  return tagColors[index % tagColors.length];
}

function platformIcon(p: string): string {
  if (p === "YOUTUBE" || p === "Youtube") return "▶";
  if (p === "BILIBILI" || p === "B站") return "▷";
  if (p === "小宇宙") return "◉";
  return "◈";
}

function platformLabel(p: string): string {
  const map: Record<string, string> = {
    YOUTUBE: "YouTube", Youtube: "YouTube",
    BILIBILI: "Bilibili", "B站": "Bilibili",
    小宇宙: "小宇宙",
  };
  return map[p] || p;
}

export default async function HomePage() {
  const records = await getRecordsWithCovers();
  const published = records
    .filter((r) => r.status === "已发布")
    .sort((a, b) => b.publishDate - a.publishDate);

  return (
    <main className="min-h-screen bg-[#fafaf9]">
      {/* Hero */}
      <header className="relative overflow-hidden noise">
        <div className="absolute inset-0 bg-gradient-to-br from-stone-900 via-stone-800 to-neutral-900" />
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top_right,rgba(99,102,241,0.15),transparent_60%)]" />
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_bottom_left,rgba(168,85,247,0.1),transparent_60%)]" />
        <div className="relative container mx-auto px-5 sm:px-8 lg:px-12 py-20 sm:py-28">
          <div className="max-w-3xl mx-auto text-center animate-fade-in">
            <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-white/[0.08] border border-white/[0.08] text-stone-400 text-xs tracking-widest uppercase mb-8">
              <span className="w-1.5 h-1.5 bg-emerald-400 rounded-full animate-pulse" />
              AI 精选内容
            </div>
            <h1 className="text-5xl sm:text-6xl lg:text-7xl font-bold text-white tracking-tight leading-[1.1] mb-6">
              降噪
            </h1>
            <p className="text-lg sm:text-xl text-stone-400 max-w-xl mx-auto leading-relaxed">
              从海量信息中过滤噪音，5 分钟获取优质访谈里的深度洞察。
            </p>
            <div className="mt-10 flex items-center justify-center gap-6 text-sm text-stone-500">
              <span>{published.length} 篇精选</span>
              <span className="w-px h-4 bg-stone-700" />
              <span>AI + 人工策展</span>
            </div>
          </div>
        </div>
        <div className="absolute bottom-0 left-0 right-0 h-24 bg-gradient-to-t from-[#fafaf9] to-transparent" />
      </header>

      {/* Content Grid */}
      <div className="container mx-auto px-5 sm:px-8 lg:px-12 py-12 sm:py-16">
        <div className="mb-10">
          <h2 className="text-sm font-medium tracking-widest uppercase text-stone-400">
            最新内容
          </h2>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5 sm:gap-6">
          {published.map((r, index) => (
            <Link
              key={r.id}
              href={`/content/${r.id}`}
              className="group bg-white rounded-2xl overflow-hidden border border-stone-200/60 card-hover animate-slide-up"
              style={{ animationDelay: `${index * 60}ms` }}
            >
              {/* Cover */}
              <div className="relative aspect-[16/10] bg-stone-100 overflow-hidden">
                {r.coverUrl ? (
                  <img
                    src={r.coverUrl}
                    alt={r.title}
                    className="w-full h-full object-cover group-hover:scale-[1.04] transition-transform duration-700 ease-out"
                  />
                ) : (
                  <div className="absolute inset-0 flex items-center justify-center bg-gradient-to-br from-stone-50 to-stone-100">
                    <div className="text-4xl text-stone-300">◇</div>
                  </div>
                )}
                {r.platform && (
                  <div className="absolute top-3 left-3 z-10">
                    <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-black/60 backdrop-blur-md text-white text-[11px] font-medium">
                      {platformIcon(r.platform)} {platformLabel(r.platform)}
                    </span>
                  </div>
                )}
              </div>

              {/* Body */}
              <div className="p-5 sm:p-6">
                {/* Tags */}
                {r.tags.length > 0 && (
                  <div className="flex flex-wrap gap-1.5 mb-3">
                    {r.tags.slice(0, 2).map((tag, i) => (
                      <span
                        key={tag}
                        className={`px-2 py-0.5 rounded-full text-[11px] font-medium ${getTagColor(i)}`}
                      >
                        {tag}
                      </span>
                    ))}
                  </div>
                )}

                {/* Title */}
                <h3 className="text-[15px] font-semibold text-stone-800 leading-snug line-clamp-2 group-hover:text-indigo-600 transition-colors duration-200 mb-3">
                  {r.title}
                </h3>

                {/* Meta */}
                <div className="flex items-center gap-3 text-xs text-stone-400">
                  {r.guests && (
                    <span className="truncate max-w-[140px]">
                      {r.guests.split(/[,，]/)[0].replace(/\s*[（(].+?[）)]/, "")}
                    </span>
                  )}
                  {r.guests && r.publishDate > 0 && (
                    <span className="w-0.5 h-0.5 rounded-full bg-stone-300" />
                  )}
                  {r.publishDate > 0 && (
                    <span>{formatDate(r.publishDate)}</span>
                  )}
                </div>
              </div>
            </Link>
          ))}
        </div>

        {published.length === 0 && (
          <div className="text-center py-24">
            <div className="text-5xl mb-6 text-stone-300">◇</div>
            <h3 className="text-base font-medium text-stone-500 mb-2">暂无内容</h3>
            <p className="text-sm text-stone-400">敬请期待更多精选内容</p>
          </div>
        )}
      </div>

      {/* Footer */}
      <footer className="border-t border-stone-200/60 mt-12 py-10">
        <div className="container mx-auto px-5 sm:px-8 lg:px-12">
          <div className="flex flex-col sm:flex-row items-center justify-between gap-4 text-xs text-stone-400">
            <div className="flex items-center gap-2">
              <span className="font-semibold text-stone-600">降噪</span>
              <span className="text-stone-300">·</span>
              <span>AI精选内容平台</span>
            </div>
            <div className="flex items-center gap-5">
              <a href="#" className="hover:text-stone-600 transition-colors">关于</a>
              <a href="#" className="hover:text-stone-600 transition-colors">联系</a>
            </div>
          </div>
        </div>
      </footer>
    </main>
  );
}
