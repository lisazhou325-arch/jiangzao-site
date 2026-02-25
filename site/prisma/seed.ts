import { PrismaClient } from "@prisma/client";
import { PrismaLibSql } from "@prisma/adapter-libsql";
import bcrypt from "bcryptjs";
import path from "path";

const adapter = new PrismaLibSql({
  url: process.env.TURSO_DATABASE_URL ?? `file:${path.join(process.cwd(), "prisma/dev.db")}`,
  authToken: process.env.TURSO_AUTH_TOKEN,
});
const prisma = new PrismaClient({ adapter } as any);

async function main() {
  const adminPassword = await bcrypt.hash("123", 10);
  await prisma.user.upsert({
    where: { email: "admin@jiangzao.com" },
    update: { password: adminPassword },
    create: {
      email: "admin@jiangzao.com",
      password: adminPassword,
      name: "管理员",
      role: "ADMIN",
    },
  });

  const guestPassword = await bcrypt.hash("123", 10);
  await prisma.user.upsert({
    where: { email: "guest@jiangzao.com" },
    update: { password: guestPassword },
    create: {
      email: "guest@jiangzao.com",
      password: guestPassword,
      name: "访客",
      role: "USER",
    },
  });

  console.log("✓ 管理员：admin@jiangzao.com / 123");
  console.log("✓ 访客：  guest@jiangzao.com / 123");
}

main()
  .catch(console.error)
  .finally(() => prisma.$disconnect());
