#!/usr/bin/env python3
"""Fetch a public video using yt-dlp, with a small Bilibili API fallback."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import urllib.parse
import urllib.request
from pathlib import Path


USER_AGENT = "Mozilla/5.0"


def bvid_from_url(value: str) -> str | None:
    match = re.search(r"\b(BV[0-9A-Za-z]{10})\b", value)
    return match.group(1) if match else None


def request_json(url: str, params: dict[str, object]) -> dict:
    target = f"{url}?{urllib.parse.urlencode(params)}"
    request = urllib.request.Request(
        target,
        headers={"User-Agent": USER_AGENT, "Referer": "https://www.bilibili.com/"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def fetch_bilibili(bvid: str, output_dir: Path) -> Path:
    view = request_json("https://api.bilibili.com/x/web-interface/view", {"bvid": bvid})
    if view.get("code") != 0:
        raise RuntimeError(f"Bilibili metadata failed: {view.get('message')}")
    metadata = view["data"]
    play = request_json(
        "https://api.bilibili.com/x/player/playurl",
        {"bvid": bvid, "cid": metadata["cid"], "qn": 64, "fnval": 0},
    )
    urls = play.get("data", {}).get("durl", [])
    if play.get("code") != 0 or not urls:
        raise RuntimeError(f"Bilibili play URL failed: {play.get('message')}")

    video = output_dir / "video.mp4"
    command = [
        "curl", "-L", "--fail", "--retry", "5", "--retry-all-errors",
        "-A", USER_AGENT, "-e", "https://www.bilibili.com/",
        urls[0]["url"], "-o", str(video),
    ]
    subprocess.run(command, check=True)
    (output_dir / "metadata.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return video


def fetch_ytdlp(url: str, output_dir: Path) -> Path:
    executable = shutil.which("yt-dlp") or str(Path.home() / ".local/bin/yt-dlp")
    if not Path(executable).exists():
        raise RuntimeError("yt-dlp is not installed")
    template = output_dir / "video.%(ext)s"
    subprocess.run(
        [executable, "--no-playlist", "--merge-output-format", "mp4", "-o", str(template), url],
        check=True,
    )
    candidates = sorted(output_dir.glob("video.*"))
    if not candidates:
        raise RuntimeError("yt-dlp completed without a video file")
    video = candidates[0]
    target = output_dir / "video.mp4"
    if video != target:
        video.rename(target)
    return target


def self_test() -> None:
    assert bvid_from_url("https://www.bilibili.com/video/BV1AmJG6tERv") == "BV1AmJG6tERv"
    assert bvid_from_url("https://v.douyin.com/example/") is None
    print("self-test: ok")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("url", nargs="?")
    parser.add_argument("--output-dir", default="/tmp/strategy-video")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return 0
    if not args.url:
        parser.error("url is required")

    output_dir = Path(args.output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    bvid = bvid_from_url(args.url)
    try:
        video = fetch_bilibili(bvid, output_dir) if bvid else fetch_ytdlp(args.url, output_dir)
    except Exception as exc:
        print(f"fetch failed: {exc}", file=sys.stderr)
        print("Resolve the Douyin short link and search for a verified same-source mirror.", file=sys.stderr)
        return 1
    print(video)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

