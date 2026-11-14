#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import base64
import re
import requests
from pathlib import Path
from urllib.parse import unquote

SOURCES_FILE = Path("sources.txt")
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; SubMerger/1.0)"
}

def is_base64(s: str) -> bool:
    s = s.strip().replace("\n", "").replace("\r", "")
    if len(s) % 4 != 0:
        return False
    try:
        base64.b64decode(s, validate=True)
        return True
    except Exception:
        return False

def decode_content(content: bytes) -> str:
    text = content.decode("utf-8", errors="ignore").strip()
    if is_base64(text):
        try:
            decoded = base64.b64decode(text).decode("utf-8", errors="ignore")
            return decoded
        except Exception:
            pass
    return text

def extract_nodes(text: str) -> list[str]:
    """提取 vmess/vless/trojan/ss 等节点"""
    nodes = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        # 支持直接的协议链接
        if re.match(r"^(vmess|vless|trojan|ss|ssr|hysteria2|hy2|tuic)://", line, re.I):
            nodes.append(line)
        # 有些是 url 编码过的
        elif "%" in line and ("vmess" in line.lower() or "vless" in line.lower()):
            try:
                decoded = unquote(line)
                if re.match(r"^(vmess|vless|trojan|ss)://", decoded, re.I):
                    nodes.append(decoded)
            except Exception:
                pass
    return nodes

def main():
    if not SOURCES_FILE.exists():
        print("sources.txt 不存在")
        return

    sources = [line.strip() for line in SOURCES_FILE.read_text(encoding="utf-8").splitlines() if line.strip() and not line.startswith("#")]
    
    all_nodes = []
    session = requests.Session()
    session.headers.update(HEADERS)

    print(f"开始拉取 {len(sources)} 个源...")

    for url in sources:
        try:
            print(f"  拉取: {url}")
            resp = session.get(url, timeout=20)
            resp.raise_for_status()
            text = decode_content(resp.content)
            nodes = extract_nodes(text)
            print(f"    → 得到 {len(nodes)} 个节点")
            all_nodes.extend(nodes)
        except Exception as e:
            print(f"    × 失败: {e}")

    # 去重（保持顺序）
    seen = set()
    unique_nodes = []
    for node in all_nodes:
        if node not in seen:
            seen.add(node)
            unique_nodes.append(node)

    print(f"\n去重后共 {len(unique_nodes)} 个节点")

    # 保存明文
    plain_path = OUTPUT_DIR / "all.txt"
    plain_path.write_text("\n".join(unique_nodes) + "\n", encoding="utf-8")

    # 保存 base64
    b64_content = base64.b64encode("\n".join(unique_nodes).encode("utf-8")).decode("utf-8")
    b64_path = OUTPUT_DIR / "all_base64.txt"
    b64_path.write_text(b64_content, encoding="utf-8")

    print(f"已生成:\n  {plain_path}\n  {b64_path}")

if __name__ == "__main__":
    main()
