"use client";
import { useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import Link from "next/link";

export default function RegisterPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [name, setName] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const router = useRouter();
  const searchParams = useSearchParams();
  const isLimit = searchParams.get("reason") === "limit";

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError("");

    const res = await fetch("/api/auth/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password, name }),
    });

    const data = await res.json();
    setLoading(false);

    if (!res.ok) {
      setError(data.error || "注册失败");
    } else {
      router.push("/login");
    }
  }

  const inputStyle = {
    padding: "10px 14px",
    border: "1px solid var(--border-dark)",
    borderRadius: 3,
    background: "var(--paper)",
    color: "var(--ink)",
    fontSize: "0.9rem",
    outline: "none",
    fontFamily: "inherit",
    width: "100%",
    boxSizing: "border-box" as const,
  };

  const labelStyle = {
    fontSize: "0.65rem",
    color: "var(--muted)",
    letterSpacing: "0.08em",
    textTransform: "uppercase" as const,
    display: "block",
    marginBottom: 4,
  };

  return (
    <main className="min-h-screen flex items-center justify-center" style={{ background: "var(--paper)" }}>
      <div style={{ width: "100%", maxWidth: 360, padding: "0 24px" }}>

        <div className="text-center" style={{ marginBottom: 32 }}>
          <Link href="/" className="font-serif" style={{ fontSize: "2.2rem", color: "var(--ink)", letterSpacing: "-0.02em", textDecoration: "none" }}>
            降<em style={{ fontStyle: "italic", color: "var(--gold)" }}>噪</em>
          </Link>
          <p className="font-mono" style={{ fontSize: "0.65rem", color: "var(--muted)", letterSpacing: "0.12em", textTransform: "uppercase", marginTop: 8 }}>
            创建账户
          </p>
        </div>

        {isLimit && (
          <div style={{ marginBottom: 20, padding: "12px 16px", background: "var(--paper-warm)", border: "1px solid var(--gold-light)", borderRadius: 4 }}>
            <p className="font-mono" style={{ fontSize: "0.68rem", color: "var(--gold)", letterSpacing: "0.04em", lineHeight: 1.6 }}>
              免费浏览已达 3 篇上限，注册后无限阅读。
            </p>
            <p className="font-mono" style={{ fontSize: "0.65rem", color: "var(--muted)", marginTop: 4 }}>
              已有账户？<Link href="/login?reason=limit" style={{ color: "var(--gold)", textDecoration: "none" }}>直接登录</Link>
            </p>
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div style={{ marginBottom: 16 }}>
            <label className="font-mono" style={labelStyle}>昵称（选填）</label>
            <input type="text" value={name} onChange={e => setName(e.target.value)} style={inputStyle} />
          </div>

          <div style={{ marginBottom: 16 }}>
            <label className="font-mono" style={labelStyle}>邮箱</label>
            <input type="email" value={email} onChange={e => setEmail(e.target.value)} required style={inputStyle} />
          </div>

          <div style={{ marginBottom: 16 }}>
            <label className="font-mono" style={labelStyle}>密码</label>
            <input type="password" value={password} onChange={e => setPassword(e.target.value)} required minLength={6} style={inputStyle} />
          </div>

          {error && (
            <p className="font-mono" style={{ fontSize: "0.65rem", color: "#b94040", marginBottom: 12 }}>{error}</p>
          )}

          <button
            type="submit"
            disabled={loading}
            className="paper-btn"
            style={{ width: "100%", justifyContent: "center", opacity: loading ? 0.6 : 1, marginTop: 8 }}
          >
            {loading ? "注册中..." : "注册"}
          </button>
        </form>

        <p className="font-mono text-center" style={{ fontSize: "0.65rem", color: "var(--muted)", marginTop: 24, letterSpacing: "0.04em" }}>
          已有账户？{" "}
          <Link href="/login" style={{ color: "var(--gold)", textDecoration: "none" }}>立即登录</Link>
        </p>

      </div>
    </main>
  );
}
