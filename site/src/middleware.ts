import NextAuth from "next-auth";
import { authConfig } from "@/lib/auth.config";
import { NextResponse } from "next/server";

const { auth } = NextAuth(authConfig);

const FREE_LIMIT = 3;

export default auth((req) => {
  const isAuthenticated = !!req.auth;
  const pathname = req.nextUrl.pathname;

  if (pathname.startsWith("/content/") && !isAuthenticated) {
    const articleId = pathname.replace("/content/", "");
    const viewedCookie = req.cookies.get("viewed_articles")?.value;
    let viewed: string[] = [];
    try {
      viewed = viewedCookie ? JSON.parse(viewedCookie) : [];
    } catch {
      viewed = [];
    }

    if (!viewed.includes(articleId)) {
      if (viewed.length >= FREE_LIMIT) {
        const loginUrl = new URL("/login", req.url);
        loginUrl.searchParams.set("reason", "limit");
        return NextResponse.redirect(loginUrl);
      }
      const newViewed = [...viewed, articleId];
      const response = NextResponse.next();
      response.cookies.set("viewed_articles", JSON.stringify(newViewed), {
        maxAge: 60 * 60 * 24 * 30,
        httpOnly: true,
        path: "/",
      });
      return response;
    }
  }

  return NextResponse.next();
});

export const config = {
  matcher: ["/content/:path*"],
};
