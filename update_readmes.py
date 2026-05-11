#!/usr/bin/env python3
"""Inject Checkmk compatibility badges into each plugin README and keep
`version.usable_until` in sync inside the per-plugin info/info.json files."""
import ast
import json
import re
import urllib.parse
from pathlib import Path

REPO = Path(__file__).resolve().parent
START = "<!-- compatibility-badges:start -->"
END = "<!-- compatibility-badges:end -->"


def badge(label, message, color):
    label_e = urllib.parse.quote(label)
    msg_e = urllib.parse.quote(message)
    return f"![{label}](https://img.shields.io/badge/{label_e}-{msg_e}-{color})"


def detect_max(info):
    """Plugins on the new API (cmk_addons_plugins / cmk_plugins) still load on
    Checkmk 2.5; legacy-API plugins (checks/, web/) stop at 2.4."""
    files = info.get("files") or {}
    if "cmk_addons_plugins" in files or "cmk_plugins" in files:
        return "2.5"
    return "2.4"


def patch_info(info_path, max_ver):
    """Set `version.usable_until` in a Python-literal info file. Replace None
    with the value, insert the key after `version.packaged` if missing, leave
    existing non-None values alone."""
    text = info_path.read_text(encoding="utf-8")
    if re.search(r"'version\.usable_until'\s*:\s*None", text):
        new = re.sub(
            r"('version\.usable_until'\s*:\s*)None",
            rf"\1'{max_ver}'",
            text,
            count=1,
        )
    elif "'version.usable_until'" in text:
        return False
    else:
        # Has trailing comma + newline (not the last dict entry)
        m = re.search(
            r"^(\s*)'version\.packaged'\s*:\s*[^\n]*,\s*\n",
            text,
            flags=re.MULTILINE,
        )
        if m:
            indent = m.group(1)
            new = text[: m.end()] + f"{indent}'version.usable_until': '{max_ver}',\n" + text[m.end():]
        else:
            # Last entry: `'version.packaged': 'X.Y.Z'}` — splice before `}`
            m = re.search(
                r"^(\s*)('version\.packaged'\s*:\s*[^\n}]+?)(\s*\})",
                text,
                flags=re.MULTILINE,
            )
            if not m:
                return False
            indent = m.group(1)
            new = (
                text[: m.start(3)]
                + f",\n{indent}'version.usable_until': '{max_ver}'"
                + text[m.start(3):]
            )
    if new == text:
        return False
    info_path.write_text(new, encoding="utf-8")
    return True


def sync_info_json(plugin_dir, info):
    """Rewrite info.json from the updated info dict if the file exists."""
    info_json = plugin_dir / "src" / "info.json"
    if not info_json.exists():
        return False
    new = json.dumps(info, ensure_ascii=False)
    old = info_json.read_text(encoding="utf-8")
    if new == old:
        return False
    info_json.write_text(new, encoding="utf-8")
    return True


def build_block(info):
    min_ver = info.get("version.min_required") or "n/a"
    max_ver = info.get("version.usable_until") or detect_max(info)
    packaged = info.get("version.packaged") or "n/a"
    badges = " ".join([
        badge("Checkmk min", min_ver, "2f4f4f"),
        badge("Checkmk max", max_ver, "informational"),
        badge("packaged", packaged, "blue"),
    ])
    return f"{START}\n{badges}\n{END}"


def inject(readme_text, block, title):
    if START in readme_text and END in readme_text:
        return re.sub(
            re.escape(START) + r".*?" + re.escape(END),
            block,
            readme_text,
            count=1,
            flags=re.DOTALL,
        )
    # Try to inject after first H1
    m = re.search(r"^(#\s+.+?)\n", readme_text, flags=re.MULTILINE)
    if m:
        idx = m.end()
        return readme_text[:idx] + "\n" + block + "\n" + readme_text[idx:]
    # No H1: prepend with title
    return f"# {title}\n\n{block}\n\n{readme_text}"


def create(info, block):
    title = info.get("title", info.get("name", "Plugin"))
    desc = info.get("description", "").rstrip()
    return f"# {title}\n\n{block}\n\n{desc}\n"


def main():
    infos = sorted(REPO.glob("*/src/info"))
    created = []
    updated = []
    info_patched = []
    for info_path in infos:
        plugin_dir = info_path.parent.parent
        try:
            info = ast.literal_eval(info_path.read_text())
        except Exception as e:
            print(f"SKIP {plugin_dir.name}: {e}")
            continue
        existing = info.get("version.usable_until")
        if not existing:
            max_ver = detect_max(info)
            if patch_info(info_path, max_ver):
                info_patched.append(plugin_dir.name)
                info = ast.literal_eval(info_path.read_text())
            sync_info_json(plugin_dir, info)
        readme = plugin_dir / "README.md"
        block = build_block(info)
        title = info.get("title", info.get("name", plugin_dir.name))
        if readme.exists():
            old = readme.read_text()
            new = inject(old, block, title)
            if new != old:
                readme.write_text(new)
                updated.append(plugin_dir.name)
        else:
            readme.write_text(create(info, block))
            created.append(plugin_dir.name)
    print(f"Created {len(created)}:")
    for n in created:
        print(f"  + {n}")
    print(f"Updated {len(updated)}:")
    for n in updated:
        print(f"  ~ {n}")
    print(f"Patched info {len(info_patched)}:")
    for n in info_patched:
        print(f"  i {n}")


if __name__ == "__main__":
    main()
