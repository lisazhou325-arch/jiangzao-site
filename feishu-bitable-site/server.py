import json
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from pathlib import Path
import yaml
import requests

ROOT_DIR = Path(__file__).resolve().parent
CONFIG_PATH = ROOT_DIR.parent / ".claude" / "skills" / "content-curator" / "config" / "sources.yaml"
INDEX_PATH = ROOT_DIR / "index.html"
FEISHU_BASE = "https://open.feishu.cn/open-apis"

access_token = None
token_expires_at = 0


def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    feishu = config.get("api_keys", {}).get("feishu", {})
    return feishu.get("app_id"), feishu.get("app_secret"), feishu.get("bitable_app_token"), feishu.get("table_id")


def get_access_token():
    global access_token, token_expires_at
    if time.time() < token_expires_at:
        return access_token
    app_id, app_secret, _, _ = load_config()
    resp = requests.post(
        f"{FEISHU_BASE}/auth/v3/tenant_access_token/internal",
        json={"app_id": app_id, "app_secret": app_secret},
        timeout=10,
    )
    data = resp.json()
    if data.get("code") != 0:
        raise Exception(data.get("msg", "Auth failed"))
    access_token = data["tenant_access_token"]
    token_expires_at = time.time() + data["expire"] - 60
    return access_token


def list_records():
    _, _, app_token, table_id = load_config()
    items = []
    page_token = None
    while True:
        params = {"page_size": 100}
        if page_token:
            params["page_token"] = page_token
        resp = requests.get(
            f"{FEISHU_BASE}/bitable/v1/apps/{app_token}/tables/{table_id}/records",
            headers={"Authorization": f"Bearer {get_access_token()}"},
            params=params,
            timeout=30,
        )
        data = resp.json()
        if data.get("code") != 0:
            raise Exception(data.get("msg", "List records failed"))
        block = data.get("data", {})
        items.extend(block.get("items", []))
        if not block.get("has_more"):
            break
        page_token = block.get("page_token")
    return items


def normalize_records(records):
    normalized = []
    for record in records:
        fields = record.get("fields", {})
        title = fields.get("标题") or fields.get("title") or ""
        platform = fields.get("平台来源") or fields.get("platform") or ""
        link_field = fields.get("原内容链接") or fields.get("url") or {}
        if isinstance(link_field, dict):
            url = link_field.get("link") or link_field.get("url") or ""
        else:
            url = link_field or ""
        cover_field = fields.get("封面图") or []
        cover_token = ""
        if isinstance(cover_field, list) and cover_field:
            cover_token = cover_field[0].get("file_token") or ""
        tags = fields.get("标签") or fields.get("tags") or []
        if tags is None:
            tags = []
        if isinstance(tags, str):
            tags = [t.strip() for t in tags.split(",") if t.strip()]
        guests = fields.get("嘉宾") or fields.get("guest") or ""
        published_at = fields.get("发布时间") or fields.get("published_at") or 0
        quotes = [fields.get(f"金句{i}") for i in range(1, 6)]
        quotes = [q for q in quotes if q]
        summary = fields.get("摘要正文") or fields.get("summary") or ""
        normalized.append(
            {
                "id": record.get("record_id", ""),
                "title": title,
                "platform": platform,
                "url": url,
                "cover_token": cover_token,
                "tags": tags,
                "guests": guests,
                "published_at": published_at,
                "quotes": quotes,
                "summary": summary,
            }
        )
    normalized.sort(key=lambda x: x.get("published_at") or 0, reverse=True)
    return normalized


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/":
            self.serve_index()
            return
        if parsed.path == "/api/records":
            self.serve_records()
            return
        if parsed.path == "/api/cover":
            self.serve_cover(parsed)
            return
        self.send_response(404)
        self.end_headers()

    def serve_index(self):
        if not INDEX_PATH.exists():
            self.send_response(500)
            self.end_headers()
            return
        content = INDEX_PATH.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def serve_records(self):
        try:
            records = list_records()
            normalized = normalize_records(records)
            payload = json.dumps({"records": normalized}, ensure_ascii=False).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)
        except Exception as exc:
            payload = json.dumps({"error": str(exc)}, ensure_ascii=False).encode("utf-8")
            self.send_response(500)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)

    def serve_cover(self, parsed):
        params = parse_qs(parsed.query)
        token = params.get("file_token", [""])[0]
        if not token:
            self.send_response(400)
            self.end_headers()
            return
        resp = requests.get(
            f"{FEISHU_BASE}/drive/v1/medias/{token}/download",
            headers={"Authorization": f"Bearer {get_access_token()}"},
            timeout=30,
            allow_redirects=True,
        )
        if resp.status_code >= 400:
            self.send_response(502)
            self.end_headers()
            return
        content = resp.content
        self.send_response(200)
        self.send_header("Content-Type", resp.headers.get("Content-Type", "application/octet-stream"))
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)


def run():
    server = HTTPServer(("0.0.0.0", 5174), Handler)
    server.serve_forever()


if __name__ == "__main__":
    run()
