import { NextRequest, NextResponse } from "next/server";
import { prisma } from "@/lib/db";
import bcrypt from "bcryptjs";

export async function POST(req: NextRequest) {
  const { email, password, name } = await req.json();

  if (!email || !password) {
    return NextResponse.json({ error: "邮箱和密码不能为空" }, { status: 400 });
  }

  const existing = await prisma.user.findUnique({ where: { email } });
  if (existing) {
    return NextResponse.json({ error: "该邮箱已注册" }, { status: 400 });
  }

  const hashed = await bcrypt.hash(password, 10);
  const count = await prisma.user.count();

  const user = await prisma.user.create({
    data: {
      email,
      password: hashed,
      name: name || null,
      role: count === 0 ? "ADMIN" : "USER",
    },
  });

  return NextResponse.json({ success: true, id: user.id });
}
