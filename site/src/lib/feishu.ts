const FEISHU_APP_ID = process.env.FEISHU_APP_ID!;
const FEISHU_APP_SECRET = process.env.FEISHU_APP_SECRET!;
const FEISHU_BITABLE_APP_TOKEN = process.env.FEISHU_BITABLE_APP_TOKEN!;
const FEISHU_TABLE_ID = process.env.FEISHU_TABLE_ID!;

let cachedToken: { token: string; expiresAt: number } | null = null;

export async function getAccessToken(): Promise<string> {
  if (cachedToken && Date.now() < cachedToken.expiresAt) {
    return cachedToken.token;
  }
  const res = await fetch(
    "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        app_id: FEISHU_APP_ID,
        app_secret: FEISHU_APP_SECRET,
      }),
    }
  );
  const data = await res.json();
  if (data.code !== 0) throw new Error(`Feishu auth failed: ${data.msg}`);
  cachedToken = {
    token: data.tenant_access_token,
    expiresAt: Date.now() + (data.expire - 60) * 1000,
  };
  return cachedToken.token;
}

export interface ContentRecord {
  id: string;
  title: string;
  guests: string;
  sourceLink: { link: string; text: string } | null;
  publishDate: number;
  platform: string;
  coverFileToken: string | null;
  coverUrl?: string;
  tags: string[];
  body: string;
  quotes: string[];
  status: string;
}

function parseRecord(item: Record<string, unknown>): ContentRecord {
  const f = item.fields as Record<string, unknown>;
  const coverArr = f["封面图"] as Array<{ file_token: string }> | undefined;
  const link = f["原内容链接"] as { link: string; text: string } | undefined;
  const tags = (f["标签"] as string[] | undefined) || [];
  const quotes: string[] = [];
  for (let i = 1; i <= 5; i++) {
    const q = f[`金句${i}`] as string | undefined;
    if (q) quotes.push(q);
  }
  return {
    id: item.record_id as string,
    title: (f["标题"] as string) || "",
    guests: (f["嘉宾"] as string) || "",
    sourceLink: link || null,
    publishDate: (f["发布时间"] as number) || 0,
    platform: (f["平台来源"] as string) || "",
    coverFileToken: coverArr?.[0]?.file_token || null,
    tags,
    body: (f["摘要正文"] as string) || "",
    quotes,
    status: (f["状态"] as string) || "",
  };
}
export async function getRecords(): Promise<ContentRecord[]> {
  let token = await getAccessToken();
  const records: ContentRecord[] = [];
  let pageToken: string | undefined;
  let retried = false;

  do {
    const url = new URL(
      `https://open.feishu.cn/open-apis/bitable/v1/apps/${FEISHU_BITABLE_APP_TOKEN}/tables/${FEISHU_TABLE_ID}/records`
    );
    url.searchParams.set("page_size", "100");
    if (pageToken) url.searchParams.set("page_token", pageToken);

    const res = await fetch(url.toString(), {
      headers: { Authorization: `Bearer ${token}` },
    });
    const data = await res.json();

    // Retry once if token expired
    if (data.code !== 0 && data.msg?.includes("access token") && !retried) {
      cachedToken = null;
      token = await getAccessToken();
      retried = true;
      continue;
    }
    if (data.code !== 0) throw new Error(`Feishu records failed: ${data.msg}`);

    for (const item of data.data.items || []) {
      records.push(parseRecord(item));
    }
    pageToken = data.data.has_more ? data.data.page_token : undefined;
  } while (pageToken);

  return records;
}

export async function getRecord(id: string): Promise<ContentRecord> {
  let token = await getAccessToken();
  let res = await fetch(
    `https://open.feishu.cn/open-apis/bitable/v1/apps/${FEISHU_BITABLE_APP_TOKEN}/tables/${FEISHU_TABLE_ID}/records/${id}`,
    { headers: { Authorization: `Bearer ${token}` } }
  );
  let data = await res.json();

  // Retry once if token expired
  if (data.code !== 0 && data.msg?.includes("access token")) {
    cachedToken = null;
    token = await getAccessToken();
    res = await fetch(
      `https://open.feishu.cn/open-apis/bitable/v1/apps/${FEISHU_BITABLE_APP_TOKEN}/tables/${FEISHU_TABLE_ID}/records/${id}`,
      { headers: { Authorization: `Bearer ${token}` } }
    );
    data = await res.json();
  }

  if (data.code !== 0) throw new Error(`Feishu record failed: ${data.msg}`);
  return parseRecord(data.data.record);
}

export async function getCoverUrl(fileToken: string): Promise<string> {
  try {
    const token = await getAccessToken();
    const res = await fetch(
      `https://open.feishu.cn/open-apis/drive/v1/medias/batch_get_tmp_download_url?file_tokens=${fileToken}`,
      { headers: { Authorization: `Bearer ${token}` } }
    );
    const data = await res.json();
    if (data.code !== 0) {
      console.warn(`Feishu cover warning: ${data.msg}`);
      return "";
    }
    const urls = data.data?.tmp_download_urls;
    if (!urls || urls.length === 0) return "";
    return urls[0].tmp_download_url || "";
  } catch (e) {
    console.warn(`Feishu cover error: ${e}`);
    return "";
  }
}

export async function getRecordWithCover(
  id: string
): Promise<ContentRecord> {
  const record = await getRecord(id);
  if (record.coverFileToken) {
    record.coverUrl = await getCoverUrl(record.coverFileToken);
  }
  return record;
}

// Shared cover URL cache (token -> { url, expiresAt })
const coverUrlCache = new Map<string, { url: string; expiresAt: number }>();

export async function getRecordsWithCovers(): Promise<ContentRecord[]> {
  const records = await getRecords();
  const fileTokens = records
    .map((r) => r.coverFileToken)
    .filter(Boolean) as string[];

  if (fileTokens.length > 0) {
    const token = await getAccessToken();
    const params = fileTokens.map((t) => `file_tokens=${t}`).join("&");
    const res = await fetch(
      `https://open.feishu.cn/open-apis/drive/v1/medias/batch_get_tmp_download_url?${params}`,
      { headers: { Authorization: `Bearer ${token}` } }
    );
    const data = await res.json();
    if (data.code === 0 && data.data?.tmp_download_urls) {
      const expiresAt = Date.now() + 25 * 60 * 1000;
      for (const item of data.data.tmp_download_urls) {
        coverUrlCache.set(item.file_token, { url: item.tmp_download_url, expiresAt });
      }
      for (const record of records) {
        if (record.coverFileToken) {
          record.coverUrl = coverUrlCache.get(record.coverFileToken)?.url || "";
        }
      }
    }
  }
  return records;
}
