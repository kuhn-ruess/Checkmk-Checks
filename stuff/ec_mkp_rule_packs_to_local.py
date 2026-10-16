#!/usr/bin/env python3
"""
Convert Event Console rule packs shipped by an MKP into normal, locally owned
rule packs inside an existing rules.mk (etc/check_mk/mkeventd.d/wato/rules.mk).

Sources (--source, repeatable):
  * an .mkp file (its "ec_rule_packs" part is read, nothing gets installed)
  * a directory with exported rule packs (default: ~/etc/check_mk/mkeventd.d/mkp/rule_packs)
  * a single exported rule pack file (<id>.mk containing mkp_rule_packs['<id>'] = {...})

What happens per rule pack:
  * a MkpRulePackProxy("<id>") in rules.mk is replaced in place by the full rule pack,
    exactly like "customize" in the GUI does (Checkmk writes the same)
  * a pack that is not referenced yet is appended at the end
  * a pack that is already present as local pack (same content) is skipped
  * a different local pack with the same ID is left alone, the source pack is skipped;
    with --rename-conflicts it is added as <id>_migrated (_migrated_2, ...)
  * rule IDs that already exist in other packs get the same suffix (the Event Console
    requires rule IDs to be unique across all packs)

Files are parsed, never executed. Before writing, rules.mk is copied to
rules.mk.bak-<timestamp> (that name is not picked up by the Event Console).
"""

import argparse
import ast
import io
import os
import pprint
import shutil
import sys
import tarfile
import time
from pathlib import Path

EC_PART = "ec_rule_packs"
HEADER = "# Written by WATO\n# encoding: utf-8\n\n"


class MkpRulePackProxy:
    """Stand-in for cmk.ec.MkpRulePackProxy, written back exactly as Checkmk does."""

    def __init__(self, id_):
        self.id_ = id_

    def __repr__(self):
        return f'{self.__class__.__name__}("{self.id_}")'


def default_dir(*parts):
    """Return a path below the current site, or None outside of a site."""
    root = os.environ.get("OMD_ROOT")
    return Path(root, *parts) if root else None


def parse_mkp_rule_packs(text, origin):
    """Parse an exported rule pack file into {id: rule_pack}."""
    packs = {}
    for node in ast.parse(text, filename=str(origin)).body:
        if (
            isinstance(node, ast.Assign)
            and len(node.targets) == 1
            and isinstance(node.targets[0], ast.Subscript)
            and isinstance(node.targets[0].value, ast.Name)
            and node.targets[0].value.id == "mkp_rule_packs"
        ):
            pack = ast.literal_eval(node.value)
            packs[pack["id"]] = pack
        else:
            raise ValueError(f"{origin}: unexpected statement in line {node.lineno}")
    return packs


def _parse_pack_list(node, origin):
    """Turn the list expression of rules.mk into rule packs and proxies."""
    if not isinstance(node, ast.List):
        raise ValueError(f"{origin}: rule_packs is not a plain list (line {node.lineno})")
    result = []
    for elt in node.elts:
        if (
            isinstance(elt, ast.Call)
            and isinstance(elt.func, ast.Name)
            and elt.func.id == "MkpRulePackProxy"
            and len(elt.args) == 1
            and not elt.keywords
        ):
            result.append(MkpRulePackProxy(ast.literal_eval(elt.args[0])))
        else:
            result.append(ast.literal_eval(elt))
    return result


def parse_rules_mk(text, origin):
    """Parse rules.mk; refuse anything that is not a rule_packs assignment."""
    rule_packs = []
    for node in ast.parse(text, filename=str(origin)).body:
        if isinstance(node, ast.AugAssign) and isinstance(node.op, ast.Add):
            target, value = node.target, node.value
        elif isinstance(node, ast.Assign) and len(node.targets) == 1:
            target, value = node.targets[0], node.value
            rule_packs = []
        else:
            raise ValueError(f"{origin}: unexpected statement in line {node.lineno}, not touching it")
        if not (isinstance(target, ast.Name) and target.id == "rule_packs"):
            raise ValueError(f"{origin}: unexpected statement in line {node.lineno}, not touching it")
        rule_packs.extend(_parse_pack_list(value, origin))
    return rule_packs


def read_mkp(path):
    """Read the EC rule packs from an .mkp file without installing it."""
    packs = {}
    with tarfile.open(path, "r:*") as mkp:
        try:
            member = mkp.getmember(f"{EC_PART}.tar")
        except KeyError:
            return packs
        inner = io.BytesIO(mkp.extractfile(member).read())
    with tarfile.open(fileobj=inner) as part:
        for member in part.getmembers():
            if member.isfile() and member.name.endswith(".mk"):
                text = part.extractfile(member).read().decode("utf-8")
                packs.update(parse_mkp_rule_packs(text, f"{path}:{member.name}"))
    return packs


def read_source(path):
    """Read rule packs from an .mkp, a rule pack directory or a single .mk file."""
    if path.is_dir():
        packs = {}
        for file in sorted(path.glob("*.mk")):
            packs.update(parse_mkp_rule_packs(file.read_text(encoding="utf-8"), file))
        return packs
    if path.suffix == ".mkp":
        return read_mkp(path)
    return parse_mkp_rule_packs(path.read_text(encoding="utf-8"), path)


def free_id(wanted, taken, suffix):
    """Return wanted, or wanted+suffix(+_n) if it is already taken."""
    if wanted not in taken:
        return wanted
    candidate = f"{wanted}{suffix}"
    counter = 2
    while candidate in taken:
        candidate = f"{wanted}{suffix}_{counter}"
        counter += 1
    return candidate


def same_content(a, b):
    """Compare two rule packs, ignoring rule IDs (they may have been renamed)."""
    def strip(pack):
        return {**pack, "rules": [{k: v for k, v in r.items() if k != "id"} for r in pack["rules"]]}
    return strip(a) == strip(b)


def merge(rule_packs, sources, known_mkp_packs, suffix, rename_conflicts):
    """Merge source packs into rule_packs, return the change log."""
    log = []
    proxy_index = {rp.id_: i for i, rp in enumerate(rule_packs) if isinstance(rp, MkpRulePackProxy)}
    real_packs = {rp["id"]: rp for rp in rule_packs if not isinstance(rp, MkpRulePackProxy)}

    def rule_ids_except(skip_index):
        """All rule IDs in use, ignoring the pack at skip_index."""
        ids = set()
        for i, rp in enumerate(rule_packs):
            if i == skip_index:
                continue
            if isinstance(rp, MkpRulePackProxy):
                rp = known_mkp_packs.get(rp.id_, {"rules": []})
            ids.update(rule["id"] for rule in rp["rules"])
        return ids

    for pack_id, source in sources.items():
        pack = {**source, "rules": [dict(rule) for rule in source["rules"]]}
        if pack_id in real_packs:
            if same_content(real_packs[pack_id], source):
                log.append(f"skip     {pack_id}: already present as local pack")
                continue
            if not rename_conflicts:
                log.append(f"skip     {pack_id}: a different local pack with this ID exists "
                           "(use --rename-conflicts to add it under a new ID)")
                continue
            taken = set(proxy_index) | {
                rp["id"] for rp in rule_packs if not isinstance(rp, MkpRulePackProxy)
            }
            pack["id"] = free_id(pack_id, taken, suffix)
            log.append(f"rename   {pack_id} -> {pack['id']}: a different pack with this ID exists")

        index = proxy_index.get(pack_id) if pack["id"] == pack_id else None
        used = rule_ids_except(index)
        for rule in pack["rules"]:
            new_id = free_id(rule["id"], used, suffix)
            if new_id != rule["id"]:
                log.append(f"rename   rule {rule['id']} -> {new_id} in pack {pack['id']}")
                rule["id"] = new_id
            used.add(new_id)

        count = len(pack["rules"])
        if index is not None:
            rule_packs[index] = pack
            log.append(f"replace  {pack_id}: MKP proxy -> local pack ({count} rules)")
        else:
            rule_packs.append(pack)
            log.append(f"append   {pack['id']}: new local pack ({count} rules)")
        real_packs[pack["id"]] = pack
    return log


def render(rule_packs, pretty):
    """Render rules.mk the way cmk.ec.save_rule_packs() does."""
    text = pprint.pformat(rule_packs) if pretty else repr(rule_packs)
    return f"{HEADER}rule_packs += \\\n{text}\n"


def write_with_backup(path, content):
    """Back up the existing file and replace it atomically."""
    backup = None
    if path.exists():
        backup = path.with_name(f"{path.name}.bak-{time.strftime('%Y%m%d-%H%M%S')}")
        shutil.copy2(path, backup)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f".{path.name}.new-{os.getpid()}")
    tmp.write_text(content, encoding="utf-8")
    if backup:
        shutil.copymode(backup, tmp)
    os.replace(tmp, path)
    return backup


def main():
    """Command line entry point."""
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "-s", "--source", action="append", type=Path,
        help=".mkp file, rule pack directory or exported <id>.mk (repeatable, "
             "default: ~/etc/check_mk/mkeventd.d/mkp/rule_packs)",
    )
    parser.add_argument(
        "-r", "--rules-mk", type=Path,
        default=default_dir("etc/check_mk/mkeventd.d/wato/rules.mk"),
        help="rules.mk to merge into (default: ~/etc/check_mk/mkeventd.d/wato/rules.mk)",
    )
    parser.add_argument("-o", "--output", type=Path, help="write the result here instead of --rules-mk")
    parser.add_argument("-p", "--pack", action="append", help="only migrate these rule pack IDs (repeatable)")
    parser.add_argument(
        "--rename-conflicts", action="store_true",
        help="add packs whose ID is already used by a different local pack under a new ID",
    )
    parser.add_argument("--suffix", default="_migrated", help="suffix for colliding IDs (default: _migrated)")
    parser.add_argument(
        "--pretty", action=argparse.BooleanOptionalAction, default=None,
        help="pretty print the output (default: keep the style of the existing file)",
    )
    parser.add_argument("-n", "--dry-run", action="store_true", help="only show what would change")
    args = parser.parse_args()

    if args.rules_mk is None:
        parser.error("not running in a site, --rules-mk is required")
    sources_paths = args.source or [default_dir("etc/check_mk/mkeventd.d/mkp/rule_packs")]
    if None in sources_paths:
        parser.error("not running in a site, --source is required")

    sources = {}
    for path in sources_paths:
        sources.update(read_source(path))
    if args.pack:
        missing = set(args.pack) - set(sources)
        if missing:
            sys.exit(f"rule pack(s) not found in the sources: {', '.join(sorted(missing))}")
        sources = {k: v for k, v in sources.items() if k in args.pack}
    if not sources:
        sys.exit("no Event Console rule packs found in the sources")

    text = args.rules_mk.read_text(encoding="utf-8") if args.rules_mk.exists() else ""
    rule_packs = parse_rules_mk(text, args.rules_mk)
    pretty = args.pretty if args.pretty is not None else (not text or "\n " in text)

    known_mkp_packs = dict(sources)
    mkp_dir = args.rules_mk.parent.parent / "mkp" / "rule_packs"
    if mkp_dir.is_dir():
        known_mkp_packs = {**read_source(mkp_dir), **sources}

    log = merge(rule_packs, sources, known_mkp_packs, args.suffix, args.rename_conflicts)
    for line in log:
        print(line)

    left = [rp.id_ for rp in rule_packs if isinstance(rp, MkpRulePackProxy)]
    if left:
        print(f"remaining MKP proxies: {', '.join(left)}")

    target = args.output or args.rules_mk
    if args.dry_run:
        print(f"dry run, {target} not written")
        return
    if all(line.startswith("skip") for line in log):
        print("nothing to do")
        return
    backup = write_with_backup(target, render(rule_packs, pretty))
    if backup:
        print(f"backup: {backup}")
    print(f"written: {target}")
    print("Activate changes afterwards (Setup > Event Console) so the Event Console loads it.")


if __name__ == "__main__":
    try:
        main()
    except (OSError, SyntaxError, ValueError, KeyError, tarfile.TarError) as error:
        sys.exit(f"error: {error}")
