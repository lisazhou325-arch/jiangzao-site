import { PrismaClient } from "@prisma/client";
import { PrismaLibSql } from "@prisma/adapter-libsql";
import bcrypt from "bcryptjs";
import path from "path";

const adapter = new PrismaLibSql({
  url: `file:${path.join(process.cwd(), "prisma/dev.db")}`,
});
const prisma = new PrismaClient({ adapter } as any);

async function main() {
  // 管理员：豆沙
  const adminPassword = await bcrypt.hash("dousha2024", 10);
  await prisma.user.upsert({
    where: { email: "dousha@jiangzao.com" },
    update: {},
    create: {
      email: "dousha@jiangzao.com",
      password: adminPassword,
      name: "豆沙",
      role: "ADMIN",
    },
  });

  // 测试普通用户
  const testPassword = await bcrypt.hash("test123456", 10);
  await prisma.user.upsert({
    where: { email: "test@jiangzao.com" },
    update: {},
    create: {
      email: "test@jiangzao.com",
      password: testPassword,
      name: "测试用户",
      role: "USER",
    },
  });

  console.log("✓ 管理员账户：dousha@jiangzao.com / dousha2024");
  console.log("✓ 测试账户：  test@jiangzao.com / test123456");
}

main()
  .catch(console.error)
  .finally(() => prisma.$disconnect());
