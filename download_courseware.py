#!/usr/bin/env python3
"""Download and verify the unchanged original PPTX from this repository's release."""
import hashlib
import os
from pathlib import Path
import tempfile
import urllib.request

URL = "https://github.com/tatumvance6345-code/claude-/releases/download/gaocheng-source-v1/courseware.pptx"
FILENAME = "幼儿园+艺术+《藁城宫灯》+说课课件.pptx"
SIZE = 159872542
SHA256 = "3f69d2e9a1765994232dcb91f12ff6842bedee9618d37fa1b2ea99b2a2d1133b"


def digest(path):
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def main():
    root = Path(__file__).resolve().parent
    target = root / FILENAME
    if target.exists():
        if target.stat().st_size == SIZE and digest(target) == SHA256:
            print(f"原课件已存在，校验通过：{target}")
            return
        raise SystemExit(f"已有同名文件，未覆盖：{target}")
    handle, temp_name = tempfile.mkstemp(prefix="courseware-", suffix=".download", dir=root)
    temp = Path(temp_name)
    try:
        request = urllib.request.Request(URL, headers={"User-Agent": "Courseware-Download"})
        with os.fdopen(handle, "wb") as output, urllib.request.urlopen(request, timeout=120) as response:
            for block in iter(lambda: response.read(1024 * 1024), b""):
                output.write(block)
        if temp.stat().st_size != SIZE or digest(temp) != SHA256:
            raise ValueError("下载文件不完整或校验不一致，请重新下载。")
        temp.rename(target)
    finally:
        temp.unlink(missing_ok=True)
    print(f"原课件下载完成，SHA-256 校验通过：{target}")


if __name__ == "__main__":
    main()
