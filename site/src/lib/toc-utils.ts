export interface TocItem {
  id: string;
  text: string;
  level: 2 | 3;
}

export function slugify(text: string): string {
  return text
    .toLowerCase()
    .replace(/[^\w\u4e00-\u9fff\s-]/g, "")
    .replace(/\s+/g, "-")
    .trim();
}

export function extractToc(content: string): TocItem[] {
  const items: TocItem[] = [];
  const lines = content.split("\n");
  for (const line of lines) {
    const m2 = line.match(/^##\s+(.+)$/);
    if (m2) {
      items.push({ id: slugify(m2[1]), text: m2[1], level: 2 });
      continue;
    }
    const m3 = line.match(/^###\s+(.+)$/);
    if (m3) {
      items.push({ id: slugify(m3[1]), text: m3[1], level: 3 });
    }
  }
  return items;
}
