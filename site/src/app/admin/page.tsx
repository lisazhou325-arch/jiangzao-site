import { auth } from "@/lib/auth";
import { prisma } from "@/lib/db";
import { redirect } from "next/navigation";
import Link from "next/link";

export default async function AdminPage() {
  const session = await auth();

  if (!session?.user) redirect("/login");
  if ((session.user as any).role !== "ADMIN") redirect("/");

  const views = await prisma.viewCount.findMany({
    orderBy: { count: "desc" },
  });

  const totalViews = views.reduce((sum, v) => sum + v.count, 0);

  return (
    <main className="min-h-screen" style={{ background: "var(--paper)" }}>

      {/* Nav */}
      <div className="sticky top-0 z-50 paper-nav">
        <div className="container mx-auto px-6 sm:px-10 lg:px-16 py-3 flex items-center justify-between">
          <Link href="/" className="paper-btn">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M15 18l-6-6 6-6" />
            </svg>
            返回
          </Link>
          <span className="font-serif" style={{ fontSize: "1.2rem", color: "var(--ink)", letterSpacing: "-0.02em" }}>
            降<em style={{ fontStyle: "italic", color: "var(--gold)" }}>噪</em>
          </span>
        </div>
      </div>

      <div className="container mx-auto px-6 sm:px-10 lg:px-16 py-12">

        {/* Header */}
        <div style={{ borderBottom: "2px solid var(--ink)", paddingBottom: "1.5rem", marginBottom: "2rem" }}>
          <h1 className="font-serif" style={{ fontSize: "2.5rem", fontWeight: 400, letterSpacing: "-0.02em", color: "var(--ink)" }}>
            后台管理
          </h1>
          <p className="font-mono" style={{ fontSize: "0.65rem", color: "var(--muted)", letterSpacing: "0.08em", textTransform: "uppercase", marginTop: 8 }}>
            文章浏览统计
          </p>
        </div>

        {/* Stats */}
        <div className="flex gap-6 mb-10">
          <div className="paper-card" style={{ padding: "1.25rem 1.75rem" }}>
            <p className="font-mono" style={{ fontSize: "0.6rem", color: "var(--muted)", letterSpacing: "0.1em", textTransform: "uppercase", marginBottom: 6 }}>总浏览量</p>
            <p className="font-serif" style={{ fontSize: "2.5rem", color: "var(--ink)", lineHeight: 1 }}>{totalViews}</p>
          </div>
          <div className="paper-card" style={{ padding: "1.25rem 1.75rem" }}>
            <p className="font-mono" style={{ fontSize: "0.6rem", color: "var(--muted)", letterSpacing: "0.1em", textTransform: "uppercase", marginBottom: 6 }}>已记录文章</p>
            <p className="font-serif" style={{ fontSize: "2.5rem", color: "var(--ink)", lineHeight: 1 }}>{views.length}</p>
          </div>
        </div>

        {/* Table */}
        {views.length === 0 ? (
          <p className="font-mono" style={{ fontSize: "0.75rem", color: "var(--muted)", letterSpacing: "0.06em" }}>暂无浏览数据</p>
        ) : (
          <div style={{ border: "1px solid var(--border)", borderRadius: 6, overflow: "hidden" }}>
            <table style={{ width: "100%", borderCollapse: "collapse" }}>
              <thead>
                <tr style={{ background: "var(--paper-warm)", borderBottom: "1px solid var(--border)" }}>
                  <th className="font-mono" style={{ padding: "10px 16px", textAlign: "left", fontSize: "0.6rem", color: "var(--muted)", letterSpacing: "0.1em", textTransform: "uppercase", fontWeight: 500 }}>文章标题</th>
                  <th className="font-mono" style={{ padding: "10px 16px", textAlign: "right", fontSize: "0.6rem", color: "var(--muted)", letterSpacing: "0.1em", textTransform: "uppercase", fontWeight: 500, whiteSpace: "nowrap" }}>浏览次数</th>
                  <th className="font-mono" style={{ padding: "10px 16px", textAlign: "right", fontSize: "0.6rem", color: "var(--muted)", letterSpacing: "0.1em", textTransform: "uppercase", fontWeight: 500, whiteSpace: "nowrap" }}>最近更新</th>
                </tr>
              </thead>
              <tbody>
                {views.map((v, i) => (
                  <tr
                    key={v.id}
                    style={{
                      borderBottom: i < views.length - 1 ? "1px solid var(--border)" : "none",
                      background: i % 2 === 0 ? "var(--paper)" : "var(--paper-warm)",
                    }}
                  >
                    <td style={{ padding: "12px 16px" }}>
                      <Link
                        href={`/content/${v.articleId}`}
                        style={{ color: "var(--ink-light)", textDecoration: "none", fontSize: "0.88rem" }}
                      >
                        {v.title || v.articleId}
                      </Link>
                    </td>
                    <td className="font-mono" style={{ padding: "12px 16px", textAlign: "right", fontSize: "0.85rem", color: "var(--gold)", fontWeight: 600 }}>
                      {v.count}
                    </td>
                    <td className="font-mono" style={{ padding: "12px 16px", textAlign: "right", fontSize: "0.65rem", color: "var(--muted)" }}>
                      {new Date(v.updatedAt).toLocaleDateString("zh-CN")}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

      </div>
    </main>
  );
}
