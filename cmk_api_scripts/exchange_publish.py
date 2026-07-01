#!/usr/bin/env python3
"""
Publish new plugin versions to the Checkmk Exchange (exchange.checkmk.com).

Reusable, stdlib-only. Logs in with the Laravel/Inertia XSRF flow, finds the
locally-newest .mkp per plugin, compares it against the version currently
published on the Exchange, and uploads a new version for every package that is
behind. Uploads go to the Exchange review queue (not instantly live).

Credentials come from the environment (never hard-coded, never committed):
    EXCHANGE_USER      e-mail / login
    EXCHANGE_PASSWORD  password  (if unset, you are prompted with getpass)

Usage:
    EXCHANGE_USER=you@example.com EXCHANGE_PASSWORD=... \
        python3 exchange_publish.py --repo /path/to/Checkmk-Checks --dry-run
    python3 exchange_publish.py --repo ... --only mysql_status
    python3 exchange_publish.py --repo ... --exclude palo_alto --limit 1
"""
import argparse
import ast
import getpass
import glob
import http.cookiejar
import json
import os
import re
import sys
import urllib.parse
import urllib.request

BASE = "https://exchange.checkmk.com"


def vkey(v):
    m = re.match(r"^(\d+)\.(\d+)(?:\.(\d+))?(?:-dev(\d+))?$", v or "")
    if not m:
        return None
    a, b, c, dv = m.groups()
    # a -dev release sorts *below* the same final release
    return (int(a), int(b), int(c or 0), 0 if dv is not None else 1,
            int(dv) if dv is not None else 0)


class Exchange:
    def __init__(self):
        self.cj = http.cookiejar.CookieJar()
        self.op = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(self.cj),
            NoRedirect(),
        )

    def _xsrf(self):
        for c in self.cj:
            if c.name == "XSRF-TOKEN":
                return urllib.parse.unquote(c.value)
        return None

    def _req(self, method, path, data=None, headers=None, follow=False):
        url = path if path.startswith("http") else BASE + path
        h = {"User-Agent": "kr-exchange-publish/1.0",
             "Accept": "application/json, text/html"}
        if headers:
            h.update(headers)
        req = urllib.request.Request(url, data=data, headers=h, method=method)
        opener = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(self.cj)) if follow else self.op
        try:
            r = opener.open(req)
            return r.getcode(), r.read(), dict(r.headers)
        except urllib.error.HTTPError as e:
            return e.code, e.read(), dict(e.headers)

    def login(self, user, password):
        self._req("GET", "/login", follow=True)          # seed cookies
        token = self._xsrf()
        if not token:
            raise RuntimeError("no XSRF-TOKEN cookie after GET /login")
        body = urllib.parse.urlencode({
            "email": user, "login": user, "password": password, "remember": "1",
        }).encode()
        code, _, _ = self._req("POST", "/login", data=body, headers={
            "X-XSRF-TOKEN": token,
            "X-Requested-With": "XMLHttpRequest",
            "Content-Type": "application/x-www-form-urlencoded",
            "Referer": BASE + "/login",
        })
        # verify
        code, html, _ = self._req("GET", "/", follow=True)
        m = re.search(r'data-page="([^"]+)"', html.decode("utf-8", "replace"))
        who = None
        if m:
            page = json.loads(__import__("html").unescape(m.group(1)))
            who = ((page.get("props", {}).get("auth") or {}).get("user") or {}).get("username")
        if not who:
            raise RuntimeError("login failed (no authenticated user in session)")
        return who

    def published(self):
        """name -> (package_id, version) for the ACTIVE package (highest ver)."""
        code, body, _ = self._req("GET", "/api/packages/all", follow=True)
        data = json.loads(body)
        best = {}
        for it in data["data"]["packages"]:
            fn = ((it.get("latest_version") or {}).get("link") or "").rsplit("/", 1)[-1]
            m = re.match(r"^(.+)-(\d[\w.\-]*)\.mkp$", fn)
            if not m:
                continue
            name, ver = m.group(1), m.group(2)
            if name not in best or (vkey(ver) or ()) > (vkey(best[name][1]) or ()):
                best[name] = (it["id"], ver)
        return best

    def upload(self, package_id, mkp_path, description):
        token = self._xsrf()
        fields = {"package_id": str(package_id), "description": description, "icon": ""}
        body, ctype = encode_multipart(fields, "mkp", mkp_path)
        code, resp, _ = self._req("POST", "/packages/versions/new", data=body, headers={
            "X-XSRF-TOKEN": token,
            "X-Requested-With": "XMLHttpRequest",
            "Content-Type": ctype,
            "Referer": BASE + "/packages/versions/new",
        })
        return code, resp


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


def encode_multipart(fields, file_field, file_path):
    boundary = "----krexch" + os.urandom(12).hex()
    nl = b"\r\n"
    buf = []
    for k, v in fields.items():
        buf.append(b"--" + boundary.encode() + nl)
        buf.append(('Content-Disposition: form-data; name="%s"' % k).encode() + nl + nl)
        buf.append(str(v).encode() + nl)
    fname = os.path.basename(file_path)
    buf.append(b"--" + boundary.encode() + nl)
    buf.append(('Content-Disposition: form-data; name="%s"; filename="%s"'
                % (file_field, fname)).encode() + nl)
    buf.append(b"Content-Type: application/octet-stream" + nl + nl)
    buf.append(open(file_path, "rb").read() + nl)
    buf.append(b"--" + boundary.encode() + b"--" + nl)
    return b"".join(buf), "multipart/form-data; boundary=" + boundary


def scan_repo(repo):
    """repo plugin name -> (newest_local_version, mkp_path), skipping archived."""
    out = {}
    for info in glob.glob(os.path.join(repo, "**/src/info"), recursive=True):
        rel = os.path.relpath(info, repo)
        if rel.startswith(("archiv/", "obsolte/")):
            continue
        try:
            d = ast.literal_eval(open(info).read())
        except Exception:
            continue
        name = d.get("name")
        plugdir = os.path.dirname(os.path.dirname(info))
        base = os.path.basename(plugdir)
        best = None
        for mk in glob.glob(os.path.join(plugdir, base + "-*.mkp")):
            mm = re.match(r"^" + re.escape(base) + r"-(\d[\w.\-]*)\.mkp$", os.path.basename(mk))
            if mm and vkey(mm.group(1)) and (best is None or vkey(mm.group(1)) > vkey(best[0])):
                best = (mm.group(1), mk)
        if name and best:
            out[name] = best
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--only", default="", help="comma list of plugin names")
    ap.add_argument("--exclude", default="", help="comma list of plugin names")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--description", default="Update to version {ver}. Checkmk 2.5 compatibility (packaging fix).")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    user = os.environ.get("EXCHANGE_USER") or input("Exchange e-mail: ").strip()
    pw = os.environ.get("EXCHANGE_PASSWORD") or getpass.getpass("Exchange password: ")

    ex = Exchange()
    who = ex.login(user, pw)
    print(f"logged in as: {who}", file=sys.stderr)

    pub = ex.published()
    local = scan_repo(args.repo)
    only = {s for s in args.only.split(",") if s}
    exclude = {s for s in args.exclude.split(",") if s}

    targets = []
    for name, (lver, mkp) in sorted(local.items()):
        if only and name not in only:
            continue
        if name in exclude or name not in pub:
            continue
        pid, pver = pub[name]
        if vkey(lver) and vkey(pver) and vkey(lver) > vkey(pver):
            targets.append((name, pid, pver, lver, mkp))
    if args.limit:
        targets = targets[:args.limit]

    print(f"\n{len(targets)} package(s) to update:\n")
    ok = err = 0
    for name, pid, pver, lver, mkp in targets:
        if args.dry_run:
            print(f"  DRY  {name:26s} id={pid:5} {pver} -> {lver}")
            continue
        desc = args.description.format(ver=lver, name=name)
        code, resp = ex.upload(pid, mkp, desc)
        snippet = resp[:180].decode("utf-8", "replace").replace("\n", " ")
        if code in (200, 201, 302, 303):
            ok += 1
            print(f"  OK   {name:26s} id={pid:5} {pver} -> {lver}  (HTTP {code})")
        else:
            err += 1
            print(f"  FAIL {name:26s} id={pid:5} -> {lver}  (HTTP {code}) {snippet}")
    if not args.dry_run:
        print(f"\ndone: {ok} uploaded, {err} failed")


if __name__ == "__main__":
    main()
