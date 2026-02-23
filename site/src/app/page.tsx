import { getRecordsWithCovers } from "@/lib/feishu";
import { ContentGrid } from "@/lib/content-grid";

export const revalidate = 3600;

export default async function HomePage() {
  const records = await getRecordsWithCovers();
  const published = records
    .filter((r) => r.status === "已发布")
    .sort((a, b) => b.publishDate - a.publishDate);

  const today = new Date();
  const issueNo = `Issue ${String(today.getFullYear()).slice(2)}·${String(today.getMonth() + 1).padStart(2, "0")}`;

  // Serialize only what the client component needs
  const clientRecords = published.map((r) => ({
    id: r.id,
    title: r.title,
    guests: r.guests,
    platform: r.platform,
    publishDate: r.publishDate,
    coverFileToken: r.coverFileToken,
    tags: r.tags,
  }));

  return (
    <main className="min-h-screen" style={{ background: "var(--paper)" }}>

      {/* Masthead */}
      <header className="container mx-auto px-6 sm:px-10 lg:px-16 pt-12 pb-0 animate-fade-up">

        {/* Top strip */}
        <div className="flex items-center justify-between pb-3 mb-0" style={{ borderBottom: "1px solid var(--border)" }}>
          <span className="font-mono" style={{ fontSize: "0.6rem", letterSpacing: "0.12em", textTransform: "uppercase", color: "var(--muted)" }}>
            AI 精选 · 人工策展
          </span>
          <span className="font-mono" style={{ fontSize: "0.6rem", letterSpacing: "0.12em", textTransform: "uppercase", color: "var(--muted)" }}>
            {issueNo}
          </span>
          <span className="font-mono" style={{ fontSize: "0.6rem", letterSpacing: "0.12em", textTransform: "uppercase", color: "var(--muted)" }}>
            {published.length} 篇精选
          </span>
        </div>

        {/* Title */}
        <div className="py-10 sm:py-14 text-center" style={{ borderBottom: "2px solid var(--ink)" }}>
          <h1
            className="font-serif"
            style={{
              fontSize: "clamp(4.5rem, 14vw, 10rem)",
              fontWeight: 400,
              lineHeight: 1,
              letterSpacing: "-0.03em",
              color: "var(--ink)",
            }}
          >
            降<em style={{ fontStyle: "italic", color: "var(--gold)" }}>噪</em>
          </h1>
          <p style={{ marginTop: "1rem", fontSize: "0.85rem", color: "var(--muted)", letterSpacing: "0.05em" }}>
            从海量信息中过滤噪音，获取优质访谈里的深度洞察
          </p>
        </div>

      </header>

      {/* Content grid */}
      <div className="container mx-auto px-6 sm:px-10 lg:px-16 py-12 sm:py-16">

        {/* Section label */}
        <div className="flex items-center gap-4 mb-8">
          <span className="font-mono" style={{ fontSize: "0.6rem", letterSpacing: "0.15em", textTransform: "uppercase", color: "var(--muted)" }}>
            最新内容
          </span>
          <div className="flex-1" style={{ height: 1, background: "var(--border)" }} />
        </div>

        <ContentGrid records={clientRecords} />

      </div>

      {/* Footer */}
      <footer className="container mx-auto px-6 sm:px-10 lg:px-16 pb-12">
        <div style={{ borderTop: "2px solid var(--ink)", paddingTop: "1.5rem" }}>
          <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
            <span className="font-serif" style={{ fontSize: "1.5rem", color: "var(--ink)", letterSpacing: "-0.02em" }}>
              降<em style={{ fontStyle: "italic", color: "var(--gold)" }}>噪</em>
            </span>
            <div className="flex items-center gap-3">
              <a href="#" className="paper-btn">关于</a>
              <a href="#" className="paper-btn">联系</a>
            </div>
          </div>
        </div>
      </footer>

    </main>
  );
}
