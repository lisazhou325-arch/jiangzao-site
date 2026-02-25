"use client";
import { useSession, signOut } from "next-auth/react";
import Link from "next/link";

export function AuthNav() {
  const { data: session } = useSession();

  if (session?.user) {
    return (
      <div className="flex items-center gap-2">
        {(session.user as any).role === "ADMIN" && (
          <Link href="/admin" className="paper-btn">后台</Link>
        )}
        <button onClick={() => signOut({ callbackUrl: "/" })} className="paper-btn">
          退出
        </button>
      </div>
    );
  }

  return <Link href="/login" className="paper-btn">登录</Link>;
}
