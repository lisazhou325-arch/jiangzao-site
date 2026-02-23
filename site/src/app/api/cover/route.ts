import { NextRequest, NextResponse } from "next/server";
import { getCoverUrl } from "@/lib/feishu";

const cache = new Map<string, { buf: ArrayBuffer; ct: string; expiresAt: number }>();

export async function GET(req: NextRequest) {
  const token = req.nextUrl.searchParams.get("token");
  if (!token) return NextResponse.json({ error: "missing token" }, { status: 400 });

  const cached = cache.get(token);
  if (cached && Date.now() < cached.expiresAt) {
    return new NextResponse(cached.buf, {
      headers: { "Content-Type": cached.ct, "Cache-Control": "public, max-age=1500" },
    });
  }

  try {
    const url = await getCoverUrl(token);
    if (!url) return NextResponse.json({ error: "not found" }, { status: 404 });

    const imgRes = await fetch(url);
    if (!imgRes.ok) return NextResponse.json({ error: "fetch failed" }, { status: 502 });

    const buf = await imgRes.arrayBuffer();
    const ct = imgRes.headers.get("content-type") || "image/jpeg";
    cache.set(token, { buf, ct, expiresAt: Date.now() + 25 * 60 * 1000 });

    return new NextResponse(buf, {
      headers: { "Content-Type": ct, "Cache-Control": "public, max-age=1500" },
    });
  } catch {
    return NextResponse.json({ error: "failed" }, { status: 500 });
  }
}
