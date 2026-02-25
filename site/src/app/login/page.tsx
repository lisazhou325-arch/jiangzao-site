"use client";
import { useState, Suspense } from "react";
import { signIn } from "next-auth/react";
import { useRouter, useSearchParams } from "next/navigation";
import Link from "next/link";

function LoginForm() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const router = useRouter();
  const searchParams = useSearchParams();
  const isLimit = searchParams.get("reason") === "limit";

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError("");

    const res = await signIn("credentials", {
      email,
      password,
      redirect: false,
    });

    setLoading(false);

    if (res?.error) {
      setError("邮箱或密码错误");
    } else {
      router.push("/");
      router.refresh();
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
            登录账户
          </p>
        </div>

        {isLimit && (
          <div style={{ marginBottom: 20, padding: "12px 16px", background: "var(--paper-warm)", border: "1px solid var(--gold-light)", borderRadius: 4 }}>
            <p className="font-mono" style={{ fontSize: "0.68rem", color: "var(--gold)", letterSpacing: "0.04em", lineHeight: 1.6 }}>
              免费浏览已达 3 篇上限，登录后无限阅读。
            </p>
            <p className="font-mono" style={{ fontSize: "0.65rem", color: "var(--muted)", marginTop: 4 }}>
              还没有账户？<Link href="/register?reason=limit" style={{ color: "var(--gold)", textDecoration: "none" }}>免费注册</Link>
            </p>
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div style={{ marginBottom: 16 }}>
            <label className="font-mono" style={labelStyle}>邮箱</label>
            <input type="email" value={email} onChange={e => setEmail(e.target.value)} required style={inputStyle} />
          </div>

          <div style={{ marginBottom: 16 }}>
            <label className="font-mono" style={labelStyle}>密码</label>
            <input type="password" value={password} onChange={e => setPassword(e.target.value)} required style={inputStyle} />
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
            {loading ? "登录中..." : "登录"}
          </button>
        </form>

        <p className="font-mono text-center" style={{ fontSize: "0.65rem", color: "var(--muted)", marginTop: 24, letterSpacing: "0.04em" }}>
          还没有账户？{" "}
          <Link href="/register" style={{ color: "var(--gold)", textDecoration: "none" }}>立即注册</Link>
        </p>

      </div>
    </main>
  );
}

export default function LoginPage() {
  return (
    <Suspense>
      <LoginForm />
    </Suspense>
  );
}
