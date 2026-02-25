"use client";
import { useSession, signOut } from "next-auth/react";
import Link from "next/link";

export function AuthNav() {
  const { data: session } = useSession();

  if (session?.user) {
    const role = (session.user as any).role;
    const name = session.user.name || session.user.email;
    return (
      <div className="flex items-center gap-3">
        <span className="font-mono" style={{ fontSize: "0.6rem", color: "var(--muted)", letterSpacing: "0.08em" }}>
          {name}
        </span>
        {role === "ADMIN" && (
          <Link href="/admin" className="paper-btn">后台</Link>
        )}
        <button onClick={() => signOut({ callbackUrl: "/" })} className="paper-btn">
          退出
        </button>
      </div>
    );
  }

  return (
    <div className="flex items-center gap-2">
      <Link href="/register" className="paper-btn">注册</Link>
      <Link href="/login" className="paper-btn">登录</Link>
    </div>
  );
}
