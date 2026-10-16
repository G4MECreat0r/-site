#!/usr/bin/env python3
"""登録URLのQR画像を生成する。使い方: enroll-qr.py <url> <out.png>"""
import sys, qrcode

def main() -> None:
    url, out = sys.argv[1], sys.argv[2]
    qrcode.make(url).save(out)
    print(f"[enroll-qr] 生成: {out}")

if __name__ == "__main__":
    main()
