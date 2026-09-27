#!/usr/bin/env python3
"""Join the split parts of the beautified PPTX and verify the result."""
import hashlib
from pathlib import Path

FILENAME = "幼儿园+艺术+《藁城宫灯》+说课课件（美化版）.pptx"
PARTS = ["courseware-beautified.pptx.part0", "courseware-beautified.pptx.part1"]
SIZE = 149180781
SHA256 = "7aad71f2bf39b9501e1cf090115290b81d02de20fedae2ec42055ea2714a3de7"


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
            print(f"美化版课件已存在，校验通过：{target}")
            return
        raise SystemExit(f"已有同名文件，未覆盖：{target}")
    temp = target.with_suffix(".joining")
    try:
        with temp.open("wb") as output:
            for name in PARTS:
                output.write((root / "美化版分卷" / name).read_bytes())
        if temp.stat().st_size != SIZE or digest(temp) != SHA256:
            raise ValueError("合并后的文件不完整或校验不一致，请重新获取分卷。")
        temp.rename(target)
    finally:
        temp.unlink(missing_ok=True)
    print(f"美化版课件合并完成，SHA-256 校验通过：{target}")


if __name__ == "__main__":
    main()
