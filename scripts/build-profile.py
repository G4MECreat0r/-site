#!/usr/bin/env python3
"""テンプレートから enrollment.mobileconfig を生成する。"""
import os, pathlib, re, sys, uuid

ROOT = pathlib.Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "profiles" / "enrollment.mobileconfig.tmpl"


def env(name: str, default: str | None = None, required: bool = False) -> str:
    v = os.environ.get(name, default)
    if required and not v:
        sys.exit(f"[build-profile] 環境変数が未設定: {name}")
    return v or ""


def main() -> None:
    mdm_url = env("MDM_SERVER_URL", required=True).rstrip("/")
    scep_url = env("SCEP_URL", f"{mdm_url}/scep").rstrip("/")
    challenge = env("SCEP_CHALLENGE", required=True)
    topic = env("TOPIC", required=True)
    org = env("ORG_NAME", "MDM")
    ident = env("IDENTIFIER_PREFIX", "com.%s.profile" % (re.sub(r"[^a-z0-9]", "", org.lower()) or "mdm"))
    out = pathlib.Path(env("OUTPUT", str(ROOT / "site" / "enroll" / "enrollment.mobileconfig")))

    values = {
        "ORG_NAME": org,
        "IDENTIFIER_PREFIX": ident,
        "PROFILE_NAME": env("PROFILE_NAME", "Device Enrollment"),
        "PROFILE_DESCRIPTION": env("PROFILE_DESCRIPTION", "Managed device enrollment"),
        "MDM_URL": mdm_url,
        "SCEP_URL": scep_url,
        "SCEP_CHALLENGE": challenge,
        "TOPIC": topic,
        "PROFILE_UUID": str(uuid.uuid4()).upper(),
        "SCEP_UUID": str(uuid.uuid4()).upper(),
        "MDM_UUID": str(uuid.uuid4()).upper(),
    }

    xml = TEMPLATE.read_text(encoding="utf-8")
    for k, v in values.items():
        xml = xml.replace("{{%s}}" % k, v)

    leftovers = set(re.findall(r"\{\{(\w+)\}\}", xml))
    if leftovers:
        sys.exit(f"[build-profile] 未置換のプレースホルダ: {sorted(leftovers)}")

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(xml, encoding="utf-8")
    print(f"[build-profile] 生成: {out}")


if __name__ == "__main__":
    main()
