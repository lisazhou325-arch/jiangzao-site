import path from "node:path";
import { defineConfig } from "prisma/config";
import { config } from "dotenv";

config({ path: path.join(process.cwd(), ".env.local") });

const isProd = !!process.env.TURSO_DATABASE_URL;

export default defineConfig(
  isProd
    ? {
        datasource: {
          adapter: async () => {
            const { PrismaLibSql } = await import("@prisma/adapter-libsql");
            return new PrismaLibSql({
              url: process.env.TURSO_DATABASE_URL!,
              authToken: process.env.TURSO_AUTH_TOKEN,
            });
          },
        },
      }
    : {
        datasource: {
          url: `file:${path.join(process.cwd(), "prisma/dev.db")}`,
        },
      }
);
