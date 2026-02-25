import { NextRequest, NextResponse } from "next/server";
import { prisma } from "@/lib/db";

export async function POST(req: NextRequest) {
  const { articleId, title } = await req.json();
  if (!articleId) {
    return NextResponse.json({ error: "missing articleId" }, { status: 400 });
  }

  await prisma.viewCount.upsert({
    where: { articleId },
    update: { count: { increment: 1 }, title },
    create: { articleId, title, count: 1 },
  });

  return NextResponse.json({ success: true });
}

export async function GET() {
  const views = await prisma.viewCount.findMany({
    orderBy: { count: "desc" },
  });
  return NextResponse.json(views);
}
