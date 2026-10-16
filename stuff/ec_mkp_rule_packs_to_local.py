#!/usr/bin/env python3
"""
Turn Event Console rule packs that came with an MKP into normal local rule packs.

An MKP can ship Event Console (EC) rule packs. Checkmk installs them to
~/etc/check_mk/mkeventd.d/mkp/rule_packs/<id>.mk and only puts a placeholder
MkpRulePackProxy("<id>") into ~/etc/check_mk/mkeventd.d/wato/rules.mk. Once the
MKP is disabled or removed, those rules are gone. This script copies the rule
packs as normal, locally owned rule packs into rules.mk (the same thing the GUI
button "Customize" does, for all packs at once and also for MKPs that are not
installed on this site). Existing rule packs and rules stay as they are.

Run it as the site user (omd su <site>), so the default paths point to the site.
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
MKP_RULE_PACK_DIR = "etc/check_mk/mkeventd.d/mkp/rule_packs"
RULES_MK = "etc/check_mk/mkeventd.d/wato/rules.mk"
PACKAGES_DIR = "var/check_mk/packages_local"
HEADER = "# Written by WATO\n# encoding: utf-8\n\n"


class MkpRulePackProxy:
    """Stand-in for cmk.ec.MkpRulePackProxy, written back exactly as Checkmk does."""

    def __init__(self, id_):
        self.id_ = id_

    def __repr__(self):
        return f'{self.__class__.__name__}("{self.id_}")'


class UsageError(Exception):
    """A problem the user can fix by calling the script differently."""


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
        packs = read_mkp(path)
        if not packs:
            raise UsageError(f"{path} contains no Event Console rule packs")
        return packs
    return parse_mkp_rule_packs(path.read_text(encoding="utf-8"), path)


def stored_mkps():
    """Return [(path, packs)] for the .mkp files of this site that contain EC rule packs."""
    directory = default_dir(PACKAGES_DIR)
    result = []
    if directory and directory.is_dir():
        for file in sorted(directory.glob("*.mkp")):
            try:
                packs = read_mkp(file)
            except (OSError, SyntaxError, ValueError, KeyError, tarfile.TarError):
                continue
            if packs:
                result.append((file, packs))
    return result


def source_hint():
    """Explain what --source accepts, including what this site has to offer."""
    lines = [
        "Give --source one of these:",
        "  package name from 'mkp list'  --source vendor_ec_rules",
        "  .mkp file                     --source /tmp/vendor_ec_rules-1.0.mkp",
        "  directory of rule pack files  --source ~/etc/check_mk/mkeventd.d/mkp/rule_packs",
        "  single rule pack file         --source ~/tmp/vendor_pack.mk",
    ]
    found = stored_mkps()
    if found:
        lines.append("MKP files on this site that contain Event Console rule packs:")
        lines += [f"  {path}  (packs: {', '.join(packs)})" for path, packs in found]
    lines.append("Run with --list for an overview.")
    return "\n".join(lines)


def resolve_source(value):
    """Turn a --source value (path or package name) into an existing path."""
    path = Path(value).expanduser()
    if path.exists():
        return path
    directory = default_dir(PACKAGES_DIR)
    if "/" not in value and directory and directory.is_dir():
        matches = [
            file for file in directory.glob(f"{value}-*.mkp")
            if file.name[: -len(".mkp")].rsplit("-", 1)[0] == value
        ]
        if matches:
            newest = max(matches, key=lambda file: file.stat().st_mtime)
            if len(matches) > 1:
                print(f"note: several versions of {value} stored, using {newest.name}")
            return newest
    raise UsageError(f"--source {value}: no such file, directory or package\n{source_hint()}")


def default_sources():
    """The rule packs of the MKPs that are enabled on this site."""
    directory = default_dir(MKP_RULE_PACK_DIR)
    if directory is None:
        raise UsageError("not running as site user, so there is no default.\n" + source_hint())
    if not directory.is_dir():
        raise UsageError(
            f"{directory} does not exist: no enabled MKP on this site ships Event Console "
            "rule packs.\nIf the MKP is disabled or not installed, name it with --source.\n"
            + source_hint()
        )
    return [directory]


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


def pack_state(pack_id, rule_packs):
    """Describe how a source pack relates to the current rules.mk."""
    for rule_pack in rule_packs:
        if isinstance(rule_pack, MkpRulePackProxy):
            if rule_pack.id_ == pack_id:
                return "MKP placeholder in rules.mk, will be replaced by the full pack"
        elif rule_pack["id"] == pack_id:
            return "already a local pack in rules.mk, will be skipped (or renamed)"
    return "not in rules.mk, will be appended"


def list_overview(sources_paths, rules_mk):
    """Print what is available, so the user knows what to pass."""
    rule_packs = []
    if rules_mk and rules_mk.exists():
        rule_packs = parse_rules_mk(rules_mk.read_text(encoding="utf-8"), rules_mk)
        print(f"Rule packs in {rules_mk}:")
        for rule_pack in rule_packs:
            if isinstance(rule_pack, MkpRulePackProxy):
                print(f"  {rule_pack.id_:30} MKP placeholder (MkpRulePackProxy)")
            else:
                print(f"  {rule_pack['id']:30} local, {len(rule_pack['rules'])} rules, "
                      f"title: {rule_pack.get('title', '')}")
        print()
    for path in sources_paths:
        print(f"Rule packs in source {path}:")
        for pack_id, pack in read_source(path).items():
            print(f"  {pack_id:30} {len(pack['rules'])} rules, title: {pack.get('title', '')}")
            print(f"  {'':30} {pack_state(pack_id, rule_packs)}")
        print()
    found = stored_mkps()
    if found:
        print(f"MKP files on this site with Event Console rule packs ({default_dir(PACKAGES_DIR)}):")
        for path, packs in found:
            print(f"  {path.name:40} packs: {', '.join(packs)}")
        print("Use one of them with --source <file or package name>, check its state with 'mkp list'.")


EPILOG = r"""
what to enter for --source:
  Leave --source out to take the rule packs of all MKPs that are enabled on
  this site. Otherwise give one of these (repeat --source for several):

    package name as shown by "mkp list"
        --source vendor_ec_rules
        uses ~/var/check_mk/packages_local/vendor_ec_rules-<version>.mkp,
        works for enabled and disabled packages
    path to an .mkp file (only read, nothing gets installed)
        --source /tmp/vendor_ec_rules-1.0.mkp
    directory with rule pack files
        --source ~/etc/check_mk/mkeventd.d/mkp/rule_packs  (the default)
    single rule pack file (contains mkp_rule_packs['<id>'] = {...})
        --source ~/tmp/vendor_pack.mk

where to find package names and rule pack IDs:
  python3 ec_mkp_rule_packs_to_local.py --list
                                    everything below in one overview
  mkp list                          all packages and whether they are enabled
  mkp show <package>                section "Event Console rule packs" lists the
                                    rule pack files of the package as <id>.mk
  ls ~/var/check_mk/packages_local  the stored .mkp files
  The rule pack ID for --pack is that file name without .mk (also shown as ID
  in Setup > Event Console).

typical procedure (as site user, "omd su <site>"):
  1. python3 ec_mkp_rule_packs_to_local.py --list
  2. python3 ec_mkp_rule_packs_to_local.py --dry-run
     shows per pack: replace, append, rename or skip. Nothing is written.
  3. python3 ec_mkp_rule_packs_to_local.py
     rules.mk is copied to rules.mk.bak-<timestamp> before it is written.
  4. Setup > Event Console: the packs now show as "modified, packaged".
     Activate changes. The EC only reloads its rules if an EC change is
     pending; if there is none, create one (e.g. "Reset all rule hit counters").
  5. Disable or remove the MKP: mkp disable <package>
     The migrated rule packs stay. Do not click "Reset to MKP" before that,
     and do not install the MKP again afterwards.

examples:
  # all rule packs of the enabled MKPs, show only
  python3 ec_mkp_rule_packs_to_local.py --dry-run

  # a disabled or not installed MKP, only one of its packs
  python3 ec_mkp_rule_packs_to_local.py --source /tmp/vendor_ec_rules-1.0.mkp --pack vendor_pack

  # write the result to a separate file to review it first
  python3 ec_mkp_rule_packs_to_local.py --source vendor_ec_rules --output ~/tmp/rules.mk.new

  # merge into the rules.mk of another site (copy), keep packs with a clashing ID
  python3 ec_mkp_rule_packs_to_local.py -s /tmp/vendor_ec_rules-1.0.mkp -r /tmp/rules.mk --rename-conflicts

what happens with conflicts:
  A pack that is already a local pack with the same content is skipped, so the
  script can run several times. A different local pack with the same ID is not
  touched, the source pack is skipped (with --rename-conflicts it is added as
  <id>_migrated). Rule IDs must be unique across all packs: a rule whose ID is
  used in another pack gets the suffix _migrated. Every rename is printed.
  Files are only parsed, never executed, and nothing gets deleted.
"""


def main():
    """Command line entry point."""
    parser = argparse.ArgumentParser(
        description=__doc__, epilog=EPILOG, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "-s", "--source", action="append", metavar="MKP|PACKAGE|DIR|FILE",
        help="where the rule packs come from: package name from 'mkp list', path to an .mkp "
             "file, directory of rule pack files or a single <id>.mk (repeatable). "
             "Default: the packs of all enabled MKPs (~/etc/check_mk/mkeventd.d/mkp/rule_packs). "
             "See 'what to enter for --source' below",
    )
    parser.add_argument(
        "-r", "--rules-mk", type=Path, metavar="FILE",
        default=default_dir(RULES_MK),
        help="the rules.mk the packs are added to. Default: the EC rules of this site "
             "(~/etc/check_mk/mkeventd.d/wato/rules.mk)",
    )
    parser.add_argument(
        "-o", "--output", type=Path, metavar="FILE",
        help="write the result to this file instead of changing --rules-mk, "
             "e.g. ~/tmp/rules.mk.new to review it first",
    )
    parser.add_argument(
        "-p", "--pack", action="append", metavar="ID",
        help="only migrate this rule pack ID, e.g. --pack vendor_pack (repeatable). "
             "Default: all packs of the sources. IDs are shown by --list",
    )
    parser.add_argument(
        "-l", "--list", action="store_true",
        help="only show the rule packs in rules.mk and in the sources, and the MKP files "
             "of this site that contain EC rule packs. Changes nothing",
    )
    parser.add_argument(
        "-n", "--dry-run", action="store_true",
        help="only show what would change, write nothing",
    )
    parser.add_argument(
        "--rename-conflicts", action="store_true",
        help="if a different local pack already uses the ID, add the source pack under "
             "<id>_migrated instead of skipping it",
    )
    parser.add_argument(
        "--suffix", default="_migrated", metavar="TEXT",
        help="suffix for renamed pack and rule IDs (default: _migrated)",
    )
    parser.add_argument(
        "--pretty", action=argparse.BooleanOptionalAction, default=None,
        help="write one entry per line (--pretty) or one long line (--no-pretty). "
             "Default: keep the style of the existing rules.mk",
    )
    args = parser.parse_args()

    if args.rules_mk is None:
        parser.error("not running as site user, so give the target with --rules-mk FILE "
                     "(or run it after 'omd su <site>')")
    args.rules_mk = args.rules_mk.expanduser()
    if args.source:
        sources_paths = [resolve_source(value) for value in args.source]
    elif args.list:
        directory = default_dir(MKP_RULE_PACK_DIR)
        sources_paths = [directory] if directory and directory.is_dir() else []
    else:
        sources_paths = default_sources()

    if args.list:
        list_overview(sources_paths, args.rules_mk)
        return

    if not args.rules_mk.exists():
        print(f"note: {args.rules_mk} does not exist yet, it will be created")

    sources = {}
    for path in sources_paths:
        sources.update(read_source(path))
    if args.pack:
        missing = set(args.pack) - set(sources)
        if missing:
            raise UsageError(
                f"rule pack ID(s) not found in the sources: {', '.join(sorted(missing))}\n"
                f"available: {', '.join(sources) or 'none'}"
            )
        sources = {k: v for k, v in sources.items() if k in args.pack}
    if not sources:
        raise UsageError("no Event Console rule packs found in the sources\n" + source_hint())

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
        print(f"remaining MKP placeholders: {', '.join(left)}")

    target = (args.output or args.rules_mk).expanduser()
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
    if args.output:
        print(f"Review it, then copy it to {args.rules_mk} to use it.")
    elif target == default_dir(RULES_MK):
        print("Next: Setup > Event Console, activate changes (see step 4 in --help), "
              "then disable the MKP (step 5).")


if __name__ == "__main__":
    try:
        main()
    except UsageError as error:
        sys.exit(f"error: {error}")
    except (OSError, SyntaxError, ValueError, KeyError, tarfile.TarError) as error:
        sys.exit(f"error: {error}")
