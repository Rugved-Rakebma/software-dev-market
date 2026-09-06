#!/usr/bin/env python3
"""rnd — the CLI spine of the rnd plugin.

One binary owns every schema and every gate. Artifacts are legitimate only
because a program reads them back; this is that program.

Subcommands
-----------
  fm          query design records + backlog items by frontmatter
  anchors     the anchor gate: every `path:Symbol` in living docs resolves
              (--audit: anchors that resolve but contradict their prose;
               --fix/--dry-run: mechanical migration off line anchors;
               --suggest: candidates for banned anchors)
  affected    reverse index: which living docs cite these source files
              (fast text scan — the drift hook's engine)
  docs-check  diff each configured surface doc against the real surface
  standards   verify docs/**/CLAUDE.md match the plugin canon outside
              binding regions (--write: generate, preserving bindings)
  backlog     new / close — id sequencing and frontmatter stamping in code
  record      new — dated design record in docs/design/
  init        scaffold .rnd/ (config seed + backlog dirs)

Design rules inherited from the field (manifested-reality-agent's
arch_check.py, vault-x's _common.py):
  - anchors live ONLY in inline code spans; fenced blocks are illustrative
  - banned shapes are tested before the anchor shape, so a line anchor is
    reported as a line anchor rather than an unresolved symbol
  - symbols come from real parsers (ast for Python), never a grep of source —
    a name in a docstring must not count as a definition
  - frontmatter is parsed with an anchored regex, never split("---")
  - ONE date format (YYYY-MM-DD), ONE enum per key, defined here only

No dependencies beyond the standard library. Python 3.9+.
Exit codes: 0 clean · 1 findings/drift · 2 argparse · 3 usage or config error.
"""
from __future__ import annotations

import argparse
import ast
import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import date as _date
from functools import lru_cache
from pathlib import Path

# --------------------------------------------------------------------------- #
# Roots
# --------------------------------------------------------------------------- #

PLUGIN_ROOT = Path(__file__).resolve().parent.parent
TEMPLATES = PLUGIN_ROOT / "templates"

E_FINDINGS, E_USAGE = 1, 3  # 2 belongs to argparse


def repo_root(start: Path | None = None) -> Path:
    """The consuming repo: nearest ancestor holding .git or .rnd (cwd-based —
    this script lives in the plugin cache, never in the repo it serves)."""
    p = (start or Path.cwd()).resolve()
    for cand in (p, *p.parents):
        if (cand / ".git").exists() or (cand / ".rnd").is_dir():
            return cand
    return p


REPO = repo_root()

LIVING_ROOTS = ("docs/living/architecture", "docs/living/operations")
DATE_FMT = "%Y-%m-%d"


def today() -> str:
    return _date.today().strftime(DATE_FMT)


def slugify(text: str, limit: int = 60) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return s[:limit].rstrip("-") or "untitled"


# --------------------------------------------------------------------------- #
# Frontmatter — anchored parse, schemas defined once
# --------------------------------------------------------------------------- #

FM_RE = re.compile(r"\A---[ \t]*\r?\n(.*?)\r?\n---[ \t]*\r?\n", re.DOTALL)

BACKLOG_KINDS = ("bug", "debt", "feat", "perf")
BACKLOG_STATUS = ("open", "closed")
RECORD_KINDS = ("design", "decision")
RECORD_STATUS = ("live", "superseded")


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """(data, body). Minimal YAML subset: `key: value`, `key: [a, b]`,
    block lists. No external YAML dependency; the CLI authors every file it
    reads, so the subset is closed."""
    m = FM_RE.match(text)
    if not m:
        return {}, text
    data: dict = {}
    current_list: list | None = None
    for raw in m.group(1).splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if raw.lstrip().startswith("- ") and current_list is not None:
            current_list.append(raw.lstrip()[2:].strip().strip("\"'"))
            continue
        km = re.match(r"^([\w-]+)\s*:\s*(.*)$", raw)
        if not km:
            current_list = None
            continue
        key, val = km.group(1), km.group(2).strip()
        if val == "":
            data[key] = current_list = []
        elif val.startswith("[") and val.endswith("]"):
            inner = val[1:-1].strip()
            data[key] = (
                [v.strip().strip("\"'") for v in inner.split(",")] if inner else []
            )
            current_list = None
        else:
            data[key] = val.strip("\"'")
            current_list = None
    return data, text[m.end():]


def dump_frontmatter(data: dict) -> str:
    lines = ["---"]
    for k, v in data.items():
        if isinstance(v, list):
            if not v:
                lines.append(f"{k}: []")
            else:
                lines.append(f"{k}:")
                lines.extend(f"  - {item}" for item in v)
        else:
            lines.append(f"{k}: {v}")
    lines.append("---")
    return "\n".join(lines) + "\n"


def _check_enum(data: dict, key: str, allowed: tuple, where: str, errs: list) -> None:
    v = data.get(key)
    if v is not None and v not in allowed:
        errs.append(f"{where}: {key} '{v}' not in {allowed}")


def validate_backlog(data: dict, where: str) -> list[str]:
    errs: list[str] = []
    for req in ("id", "kind", "status", "opened"):
        if req not in data:
            errs.append(f"{where}: missing '{req}'")
    _check_enum(data, "kind", BACKLOG_KINDS, where, errs)
    _check_enum(data, "status", BACKLOG_STATUS, where, errs)
    if data.get("id") and not re.fullmatch(r"[A-Z]+-\d{3}", data["id"]):
        errs.append(f"{where}: id '{data['id']}' not KIND-NNN")
    if data.get("status") == "closed" and "resolution" not in data:
        errs.append(f"{where}: closed without resolution")
    return errs


def validate_record(data: dict, where: str) -> list[str]:
    errs: list[str] = []
    for req in ("kind", "date", "status"):
        if req not in data:
            errs.append(f"{where}: missing '{req}'")
    _check_enum(data, "kind", RECORD_KINDS, where, errs)
    _check_enum(data, "status", RECORD_STATUS, where, errs)
    return errs


# --------------------------------------------------------------------------- #
# config.toml — tiny reader for the closed subset the seed template emits
# --------------------------------------------------------------------------- #


def load_config() -> dict:
    """Parse .rnd/config.toml. Tries tomllib (3.11+); falls back to a reader
    for the exact subset the seed template uses: [section], [[section]],
    key = "str" | ["a", "b"]."""
    path = REPO / ".rnd" / "config.toml"
    if not path.is_file():
        return {}
    text = path.read_text(encoding="utf-8")
    try:
        import tomllib  # type: ignore

        return tomllib.loads(text)
    except ModuleNotFoundError:
        pass
    cfg: dict = {}
    target: dict = cfg
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        m = re.match(r"^\[\[([\w.-]+)\]\]$", line)
        if m:
            cfg.setdefault(m.group(1), [])
            target = {}
            cfg[m.group(1)].append(target)
            continue
        m = re.match(r"^\[([\w.-]+)\]$", line)
        if m:
            target = cfg.setdefault(m.group(1), {})
            continue
        m = re.match(r"^([\w-]+)\s*=\s*(.+)$", line)
        if not m:
            continue
        key, val = m.group(1), m.group(2).strip()
        if val.startswith("[") and val.endswith("]"):
            inner = val[1:-1].strip()
            target[key] = (
                [v.strip().strip("\"'") for v in inner.split(",")] if inner else []
            )
        else:
            target[key] = val.strip("\"'")
    return cfg


# --------------------------------------------------------------------------- #
# Symbol resolvers — registry keyed by suffix; stdlib only
# --------------------------------------------------------------------------- #


class _PySymbols(ast.NodeVisitor):
    """Every name a doc may anchor to. Nested defs count — closures are often
    exactly what a reader wants to look up. Constants only at module/class
    level: collecting them inside a function made every local citable."""

    def __init__(self) -> None:
        self.names: set[str] = set()
        self.dotted: set[str] = set()
        self._class_stack: list[str] = []

    def _record(self, name: str) -> None:
        self.names.add(name)
        if self._class_stack:
            self.dotted.add(f"{self._class_stack[-1]}.{name}")

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        self._record(node.name)
        self._class_stack.append(node.name)
        self.generic_visit(node)
        self._class_stack.pop()

    def _visit_func(self, node) -> None:
        self._record(node.name)
        saved, self._class_stack = self._class_stack, []
        self.generic_visit(node)
        self._class_stack = saved

    visit_FunctionDef = _visit_func
    visit_AsyncFunctionDef = _visit_func

    def visit_Assign(self, node: ast.Assign) -> None:
        for t in node.targets:
            if isinstance(t, ast.Name):
                self._record(t.id)
        self.generic_visit(node)

    def visit_AnnAssign(self, node: ast.AnnAssign) -> None:
        if isinstance(node.target, ast.Name):
            self._record(node.target.id)
        self.generic_visit(node)


def _py_symbols(path: Path) -> tuple[frozenset, frozenset] | None:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except (OSError, SyntaxError, ValueError):
        return None
    v = _PySymbols()
    v.visit(tree)
    return frozenset(v.names), frozenset(v.dotted)


#: Brace-language declarations. Each entry: (regex with a `name` group).
_KT_DECL = re.compile(
    r"^\s*(?:@\w+\s+)*(?:public|private|protected|internal|open|abstract|final|sealed|"
    r"inner|data|inline|suspend|override|expect|actual|const|lateinit|\s)*"
    r"(?:class|object|interface|fun|val|var|enum\s+class|typealias)\s+"
    r"(?:<[^>]*>\s*)?(?:[\w.]+\.)?(?P<name>\w+)"
)
_TS_DECL = re.compile(
    r"^\s*(?:export\s+)?(?:default\s+)?(?:declare\s+)?(?:abstract\s+)?(?:async\s+)?"
    r"(?:class|function\*?|interface|enum|type|const|let|var|namespace)\s+(?P<name>\w+)"
)
_TS_METHOD = re.compile(
    r"^\s+(?:public\s+|private\s+|protected\s+|static\s+|readonly\s+|async\s+|get\s+|set\s+)*"
    r"(?P<name>\w+)\s*(?:<[^>]*>)?\s*\([^;]*$"
)
_SWIFT_DECL = re.compile(
    r"^\s*(?:@\w+(?:\([^)]*\))?\s+)*(?:public|private|fileprivate|internal|open|static|"
    r"final|override|mutating|\s)*"
    r"(?:class|struct|enum|protocol|extension|func|var|let|typealias|actor)\s+(?P<name>[\w.]+)"
)
_GO_DECL = re.compile(
    r"^\s*(?:func\s+(?:\([^)]*\)\s*)?|type\s+|var\s+|const\s+)(?P<name>\w+)"
)
_RS_DECL = re.compile(
    r"^\s*(?:pub(?:\([^)]*\))?\s+)?(?:async\s+)?(?:unsafe\s+)?"
    r"(?:fn|struct|enum|trait|impl|mod|const|static|type)\s+(?P<name>\w+)"
)

_CONTAINER_KW = re.compile(
    r"\b(class|object|interface|struct|enum|protocol|extension|trait|impl|namespace|actor)\b"
)


def _brace_symbols(path: Path, decl_res: tuple) -> tuple[frozenset, frozenset] | None:
    """Regex symbol collection for brace languages, with one level of
    container nesting tracked by brace depth so `Owner.member` resolves.
    ~95% accurate by design; a miss degrades to a finding a human reviews,
    never a silent pass (the anchor still fails as unresolved)."""
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    names: set[str] = set()
    dotted: set[str] = set()
    stack: list[tuple[str, int]] = []  # (container name, depth at open)
    depth = 0
    in_block_comment = False
    for raw in text.splitlines():
        line = raw
        if in_block_comment:
            if "*/" in line:
                line = line.split("*/", 1)[1]
                in_block_comment = False
            else:
                continue
        if "/*" in line and "*/" not in line.split("/*", 1)[1]:
            line, in_block_comment = line.split("/*", 1)[0], True
        line = line.split("//", 1)[0]
        if not line.strip():
            depth += raw.count("{") - raw.count("}")
            continue
        matched_name = ""
        for dr in decl_res:
            m = dr.match(line)
            if m:
                matched_name = m.group("name")
                break
        if matched_name:
            names.add(matched_name)
            if stack:
                dotted.add(f"{stack[-1][0]}.{matched_name}")
            if _CONTAINER_KW.search(line.split(matched_name)[0] + " "):
                stack.append((matched_name, depth))
        depth += line.count("{") - line.count("}")
        while stack and depth <= stack[-1][1]:
            stack.pop()
    return frozenset(names), frozenset(dotted)


_RESOLVERS = {
    ".py": _py_symbols,
    ".kt": lambda p: _brace_symbols(p, (_KT_DECL,)),
    ".kts": lambda p: _brace_symbols(p, (_KT_DECL,)),
    ".ts": lambda p: _brace_symbols(p, (_TS_DECL, _TS_METHOD)),
    ".tsx": lambda p: _brace_symbols(p, (_TS_DECL, _TS_METHOD)),
    ".js": lambda p: _brace_symbols(p, (_TS_DECL, _TS_METHOD)),
    ".jsx": lambda p: _brace_symbols(p, (_TS_DECL, _TS_METHOD)),
    ".swift": lambda p: _brace_symbols(p, (_SWIFT_DECL,)),
    ".go": lambda p: _brace_symbols(p, (_GO_DECL,)),
    ".rs": lambda p: _brace_symbols(p, (_RS_DECL,)),
}


@lru_cache(maxsize=None)
def symbols_of(path: Path) -> tuple[frozenset, frozenset] | None:
    """(names, Owner.member names), or None when no resolver exists / file is
    unparsable — None means 'cannot judge the symbol', so only the path is
    checked. A resolver miss must degrade to file-level, never false-fail."""
    fn = _RESOLVERS.get(path.suffix)
    return fn(path) if fn else None


def _symbol_exists(target: Path, name: str) -> bool:
    found = symbols_of(target)
    if found is None:
        return False
    names, dotted = found
    return name in names or name in dotted


@lru_cache(maxsize=None)
def _py_def_lines(path: Path) -> tuple:
    """(line, qualified name) per def/class/constant — --suggest/--fix only.
    Python-only: line-anchor migration is where the ast precision pays."""
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except (OSError, SyntaxError, ValueError):
        return ()
    out: list[tuple[int, str]] = []

    def start_of(node) -> int:
        decs = getattr(node, "decorator_list", [])
        return min([node.lineno] + [d.lineno for d in decs]) if decs else node.lineno

    def walk(node, prefix: str, in_func: bool) -> None:
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                out.append((start_of(child), f"{prefix}{child.name}"))
                walk(child, prefix, True)
                continue
            if isinstance(child, ast.ClassDef):
                name = f"{prefix}{child.name}"
                out.append((start_of(child), name))
                walk(child, f"{name}.", in_func)
                continue
            if not in_func:
                if isinstance(child, ast.Assign):
                    for t in child.targets:
                        if isinstance(t, ast.Name):
                            out.append((child.lineno, f"{prefix}{t.id}"))
                elif isinstance(child, ast.AnnAssign) and isinstance(
                    child.target, ast.Name
                ):
                    out.append((child.lineno, f"{prefix}{child.target.id}"))
            walk(child, prefix, in_func)

    walk(tree, "", False)
    return tuple(sorted(out))


def enclosing_symbol(path: Path, line: int) -> str:
    best = ""
    for lineno, name in _py_def_lines(path):
        if lineno <= line:
            best = name
        else:
            break
    return best


# --------------------------------------------------------------------------- #
# Anchor grammar
# --------------------------------------------------------------------------- #

FENCE = re.compile(r"^\s*(```|~~~)")
CODE_SPAN = re.compile(r"`([^`\n]+)`")

FILE_SUFFIXES = (
    ".py", ".kt", ".kts", ".ts", ".tsx", ".js", ".jsx", ".swift", ".go", ".rs",
    ".md", ".yaml", ".yml", ".json", ".jsonl", ".toml", ".txt", ".sh", ".cfg",
    ".gradle", ".xml", ".sql",
)
_SUFFIX_ALT = "|".join(re.escape(s) for s in FILE_SUFFIXES)

ANCHOR = re.compile(
    r"^(?P<path>[\w./-]+(?:" + _SUFFIX_ALT + r")|justfile|Makefile)"
    r"(?::(?P<symbol>[\w.\-]+))?$"
)
LINE_ANCHOR = re.compile(
    r"^(?:[\w./-]+(?:" + _SUFFIX_ALT + r")|justfile|Makefile)?:\d+(?:[-,]\d+)*$"
)
SYMBOL_THEN_LINE = re.compile(r"^[\w.]+\s+:\d+(?:[-,]\d+)*$")

_EXCLUDED_DIR_NAMES = {
    ".git", "node_modules", "__pycache__", ".venv", "venv", "build", "dist",
    ".gradle", "target", ".next", ".rnd", "Pods", "DerivedData",
}


@lru_cache(maxsize=1)
def _repo_files() -> tuple:
    """Every candidate source file. git ls-files when possible (fast, respects
    .gitignore); os.walk with exclusions otherwise."""
    try:
        out = subprocess.run(
            ["git", "-C", str(REPO), "ls-files", "-z"],
            capture_output=True, text=True, timeout=10,
        )
        if out.returncode == 0:
            return tuple(
                REPO / f for f in out.stdout.split("\0") if f and (REPO / f).is_file()
            )
    except (OSError, subprocess.SubprocessError):
        pass
    found: list[Path] = []
    for p in REPO.rglob("*"):
        if p.is_file() and not (set(p.parts) & _EXCLUDED_DIR_NAMES):
            found.append(p)
    return tuple(found)


def resolve(path_str: str, *, lenient: bool, prefer: str = "") -> Path | None:
    """Strict: repo-relative hit only. Lenient: suffix-match the WHOLE path
    (basename matching conflates siblings); `prefer` breaks remaining ties by
    exact parent-directory comparison."""
    p = REPO / path_str
    if p.is_file():
        return p
    if not lenient:
        return None
    want = "/" + path_str.lstrip("./")
    hits = [f for f in _repo_files() if str(f).endswith(want)]
    if len(hits) == 1:
        return hits[0]
    if len(hits) > 1 and prefer:
        want_dir = REPO / prefer
        narrowed = [f for f in hits if f.parent == want_dir]
        if len(narrowed) == 1:
            return narrowed[0]
    return None


def doc_package_hint(doc: Path) -> str:
    counts: dict[str, int] = {}
    try:
        text = doc.read_text(encoding="utf-8")
    except OSError:
        return ""
    for span in CODE_SPAN.findall(text):
        cand = span.strip().split(":")[0]
        if "/" not in cand:
            continue
        got = resolve(cand, lenient=True)
        if got is None:
            continue
        parent = str(got.parent)
        counts[parent] = counts.get(parent, 0) + 1
    if not counts:
        return ""
    top = max(counts.items(), key=lambda kv: kv[1])[0]
    return top.replace(str(REPO) + "/", "")


def is_citation(span: str) -> bool:
    """A code citation vs a filename mentioned as data. ALL-CAPS head = env
    var; placeholder shapes = artifact patterns; bare names must resolve."""
    head = span.split(":")[0]
    if head.split("/")[0].isupper() and "/" in head:
        return False
    if re.search(r"NNN|<[^>]*>|\{[^}]*\}|\*", head):
        return False
    if head in ("justfile", "Makefile"):
        return True
    if any(head.endswith(s) for s in FILE_SUFFIXES if s != ".md") and "/" in head:
        return True
    if "/" in head:
        return True
    return resolve(head, lenient=True) is not None


@dataclass
class Problem:
    doc: Path
    line: int
    anchor: str
    reason: str
    hint: str = ""


def _living_docs(roots: list[str]) -> list[Path]:
    docs: list[Path] = []
    for r in roots:
        p = (REPO / r) if not Path(r).is_absolute() else Path(r)
        if p.is_dir():
            # CLAUDE.md quotes banned forms in order to ban them.
            docs.extend(d for d in sorted(p.rglob("*.md")) if d.name != "CLAUDE.md")
        elif p.is_file():
            docs.append(p)
    return docs


# --------------------------------------------------------------------------- #
# anchors — check / suggest / audit / fix
# --------------------------------------------------------------------------- #


def check_doc(doc: Path, *, suggest: bool) -> list[Problem]:
    problems: list[Problem] = []
    hint = doc_package_hint(doc)
    seen: dict[str, int] = {}
    in_fence = False
    for n, raw in enumerate(doc.read_text(encoding="utf-8").splitlines(), start=1):
        if FENCE.match(raw):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        for span in CODE_SPAN.findall(raw):
            span = span.strip()
            if LINE_ANCHOR.match(span) or SYMBOL_THEN_LINE.match(span):
                h = _suggest(span, raw) if suggest else ""
                problems.append(Problem(doc, n, span, "line anchor (banned)", h))
                continue
            m = ANCHOR.match(span)
            if not m or not is_citation(span):
                continue
            path_str, symbol = m.group("path"), m.group("symbol")
            target = resolve(path_str, lenient=False)
            if target is None:
                loose = resolve(path_str, lenient=True, prefer=hint)
                problems.append(Problem(
                    doc, n, span, "path does not exist (must be repo-relative)",
                    f"did you mean {loose.relative_to(REPO)}?" if loose else "",
                ))
                continue
            if symbol is not None:
                found = symbols_of(target)
                if found is not None:
                    names, dotted = found
                    if symbol not in names and symbol not in dotted:
                        problems.append(Problem(
                            doc, n, span, f"no symbol `{symbol}` in that file"
                        ))
                        continue
                # Reuse census (only resolvable symbol anchors count).
                seen[span] = seen.get(span, 0) + 1
    for anchor_text, count in seen.items():
        if count >= 3:
            problems.append(Problem(
                doc, 0, anchor_text,
                f"anchor reused {count}x in one doc (3+ is a defect — "
                "claims are being attached to a symbol that merely resolves)",
            ))
    return problems


def _suggest(span: str, context_line: str) -> str:
    path_str, _, tail = span.partition(":")
    if not path_str:
        return "(bare line anchor — file implied by the section; resolve by hand)"
    if " " in path_str:
        path_str = path_str.split()[0]
        return f"prose names `{path_str}` — anchor the file that defines it"
    target = resolve(path_str, lenient=True)
    if target is None:
        return "(unresolvable path)"
    rel = target.relative_to(REPO)
    try:
        line = int(re.split(r"[-,]", tail)[0])
    except ValueError:
        return f"{rel}:?"
    sym = enclosing_symbol(target, line) if target.suffix == ".py" else ""
    named = re.findall(r"`([A-Za-z_][\w.]*)`", context_line)
    doc_names = [c for c in named if c != span]
    extra = f"  · prose names: {', '.join(doc_names[:4])}" if doc_names else ""
    return f"{rel}:{sym or '?'}{extra}"


def audit_doc(doc: Path) -> list[Problem]:
    """Anchors that RESOLVE but contradict the prose beside them. The
    identifier nearest an anchor is the doc's own claim about what it points
    at; when that identifier exists in the target and differs from the anchor's
    symbol, the anchor is the suspect."""
    problems: list[Problem] = []
    in_fence = False
    for n, raw in enumerate(doc.read_text(encoding="utf-8").splitlines(), start=1):
        if FENCE.match(raw):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        spans = [(m.start(), m.group(1).strip()) for m in CODE_SPAN.finditer(raw)]
        for i, (_, span) in enumerate(spans):
            m = ANCHOR.match(span)
            if not m or not m.group("symbol") or not is_citation(span):
                continue
            target = resolve(m.group("path"), lenient=False)
            if target is None or target.suffix not in _RESOLVERS:
                continue
            symbol = m.group("symbol")
            order = list(reversed(spans[:i])) + spans[i + 1:]
            tried = 0
            for _, prev in order:
                if tried >= 3:
                    break
                cand = re.sub(r"\(.*\)$", "", prev).rstrip("()")
                if not re.fullmatch(r"[A-Za-z_][\w.]*", cand):
                    continue
                tried += 1
                if cand == symbol or cand == symbol.rsplit(".", 1)[-1]:
                    break
                if _symbol_exists(target, cand):
                    problems.append(Problem(
                        doc, n, span,
                        f"prose says `{cand}`, anchor says `{symbol}`",
                        raw.strip()[:150],
                    ))
                    break
                elsewhere = [
                    f for f in _repo_files()
                    if f.suffix == target.suffix and f.name == target.name
                    and f != target and _symbol_exists(f, cand)
                ]
                if elsewhere:
                    problems.append(Problem(
                        doc, n, span,
                        f"WRONG FILE? `{cand}` is not in {target.relative_to(REPO)} "
                        f"but IS in {elsewhere[0].relative_to(REPO)}",
                        raw.strip()[:150],
                    ))
                    break
    return problems


@dataclass
class Fix:
    doc: Path
    line: int
    before: str
    after: str
    confidence: str  # agreed | prose | line | rooted
    note: str = ""


FILE_IN_LINE = re.compile(
    r"`([\w./-]+(?:" + _SUFFIX_ALT + r"))(?::[\w.\-]+)?`"
)


def fix_doc(doc: Path) -> tuple[str, list[Fix], list[Problem]]:
    """Rewrite one doc's anchors: root well-formed anchors to repo-relative
    paths; migrate line anchors to symbols. Prose wins over the cited line —
    the line is the thing that rotted."""
    fixes: list[Fix] = []
    manual: list[Problem] = []
    out_lines: list[str] = []
    hint = doc_package_hint(doc)
    in_fence = False
    file_ctx: Path | None = None

    for n, raw in enumerate(doc.read_text(encoding="utf-8").splitlines(), start=1):
        if FENCE.match(raw):
            in_fence = not in_fence
            out_lines.append(raw)
            continue
        if in_fence:
            out_lines.append(raw)
            continue

        for cand in FILE_IN_LINE.findall(raw):
            got = resolve(cand, lenient=True, prefer=hint)
            if got is not None:
                file_ctx = got

        spans = [(m.start(), m.group(1).strip()) for m in CODE_SPAN.finditer(raw)]
        new = raw

        def preceding_name(idx: int, tgt: Path) -> str:
            for _, prev in reversed(spans[:idx]):
                cand = prev.rstrip("()")
                if not re.fullmatch(r"[A-Za-z_][\w.]*", cand):
                    continue
                return cand if _symbol_exists(tgt, cand) else ""
            return ""

        for span_idx, (_, span) in enumerate(spans):
            banned = bool(LINE_ANCHOR.match(span) or SYMBOL_THEN_LINE.match(span))
            m = ANCHOR.match(span)

            if not banned and m:
                if not is_citation(span):
                    continue
                path_str, symbol = m.group("path"), m.group("symbol")
                if resolve(path_str, lenient=False) is not None:
                    continue
                got = resolve(path_str, lenient=True, prefer=hint)
                if got is None:
                    manual.append(Problem(doc, n, span, "unresolvable path"))
                    continue
                rel = got.relative_to(REPO)
                after = f"{rel}:{symbol}" if symbol else str(rel)
                new = new.replace(f"`{span}`", f"`{after}`")
                fixes.append(Fix(doc, n, span, after, "rooted"))
                continue

            if not banned:
                continue

            head, _, tail = span.partition(":")
            named_symbol = ""
            if " " in head:
                named_symbol, head = head.split()[0], ""
            target = resolve(head, lenient=True, prefer=hint) if head else file_ctx
            if target is None:
                manual.append(
                    Problem(doc, n, span, "no file context for a bare line anchor")
                )
                continue
            rel = target.relative_to(REPO)
            if named_symbol:
                if not _symbol_exists(target, named_symbol):
                    manual.append(Problem(
                        doc, n, span,
                        f"prose names `{named_symbol}`, absent from {rel}",
                    ))
                    continue
                after = f"{rel}:{named_symbol}"
                new = new.replace(f"`{span}`", f"`{after}`")
                fixes.append(Fix(doc, n, span, after, "agreed"))
                continue
            try:
                line_no = int(re.split(r"[-,]", tail)[0])
            except ValueError:
                manual.append(Problem(doc, n, span, "unparsable line anchor"))
                continue

            if target.suffix != ".py" or not enclosing_symbol(target, line_no):
                after = str(rel)
                new = new.replace(f"`{span}`", f"`{after}`")
                fixes.append(Fix(
                    doc, n, span, after, "agreed",
                    "no enclosing symbol — file-level anchor",
                ))
                continue
            at_line = enclosing_symbol(target, line_no)
            named = preceding_name(span_idx, target)
            tail_of = at_line.rsplit(".", 1)[-1] if at_line else ""
            if named and (named == at_line or named == tail_of):
                chosen, conf, note = at_line, "agreed", ""
            elif named:
                chosen, conf = named, "prose"
                note = (
                    f"line {line_no} sits in `{at_line}` — ROTTED"
                    if at_line and at_line != named else ""
                )
            elif at_line:
                chosen, conf, note = at_line, "line", "no name in prose to corroborate"
            else:
                manual.append(
                    Problem(doc, n, span, "no symbol found at or before that line")
                )
                continue
            after = f"{rel}:{chosen}"
            new = new.replace(f"`{span}`", f"`{after}`")
            fixes.append(Fix(doc, n, span, after, conf, note))

        out_lines.append(new)

    return "\n".join(out_lines) + "\n", fixes, manual


def cmd_anchors(args) -> int:
    roots = args.paths or list(LIVING_ROOTS)
    docs = _living_docs(roots)
    if not docs:
        print(f"anchors: no docs under {', '.join(roots)} — nothing to check.")
        return 0

    if args.audit:
        found: list[Problem] = []
        for doc in docs:
            found.extend(audit_doc(doc))
        for pr in found:
            print(f"{pr.doc.relative_to(REPO)}:{pr.line}  {pr.reason}")
            if pr.hint:
                print(f"    {pr.hint}")
        print(f"\naudit: {len(found)} suspect anchor(s) across {len(docs)} doc(s).")
        return 0

    if args.fix or args.dry_run:
        all_fixes: list[Fix] = []
        all_manual: list[Problem] = []
        write = args.fix and not args.dry_run
        for doc in docs:
            text, fixes, manual = fix_doc(doc)
            all_fixes.extend(fixes)
            all_manual.extend(manual)
            if write and fixes:
                doc.write_text(text, encoding="utf-8")
        tiers: dict[str, list[Fix]] = {"agreed": [], "prose": [], "line": [], "rooted": []}
        for f in all_fixes:
            tiers[f.confidence].append(f)
        print(f"{'APPLIED' if write else 'DRY RUN'} — {len(all_fixes)} anchor(s) rewritten\n")
        print(f"  agreed  {len(tiers['agreed']):>4}   prose and cited line name the same symbol")
        print(f"  rooted  {len(tiers['rooted']):>4}   already a symbol anchor, path made repo-relative")
        print(f"  prose   {len(tiers['prose']):>4}   took the name the prose gives — REVIEW")
        print(f"  line    {len(tiers['line']):>4}   took the symbol at the cited line — REVIEW")
        for tier in ("prose", "line"):
            if not tiers[tier]:
                continue
            print(f"\n--- {tier} ({len(tiers[tier])}) ---")
            for f in tiers[tier]:
                print(f"  {f.doc.name}:{f.line}  `{f.before}` -> `{f.after}`"
                      + (f"   [{f.note}]" if f.note else ""))
        if all_manual:
            print(f"\n--- MANUAL ({len(all_manual)}) ---")
            for p in all_manual:
                print(f"  {p.doc.name}:{p.line}  `{p.anchor}`  — {p.reason}")
        return 0

    problems: list[Problem] = []
    for doc in docs:
        problems.extend(check_doc(doc, suggest=args.suggest))
    if not problems:
        print(f"anchors: {len(docs)} doc(s), every anchor resolves.")
        return 0
    by_doc: dict[Path, list[Problem]] = {}
    for p in problems:
        by_doc.setdefault(p.doc, []).append(p)
    for doc, items in by_doc.items():
        print(f"\n{doc.relative_to(REPO)}  ({len(items)})")
        for p in items:
            loc = f":{p.line:<4}" if p.line else " doc "
            print(f"  {loc} `{p.anchor}`  — {p.reason}")
            if p.hint:
                print(f"        → {p.hint}")
    print(f"\nanchors: {len(problems)} problem(s) across {len(by_doc)} doc(s).")
    print("Standard: docs/living/architecture/CLAUDE.md — `path:Symbol`, never `path:line`.")
    return E_FINDINGS


# --------------------------------------------------------------------------- #
# affected — the drift hook's engine. Text scan only; must stay fast.
# --------------------------------------------------------------------------- #


def cmd_affected(args) -> int:
    targets: list[str] = []
    for f in args.files:
        p = Path(f)
        try:
            rel = str(p.resolve().relative_to(REPO))
        except ValueError:
            rel = f
        targets.append(rel)
    hits: list[tuple[Path, str, str]] = []
    for root in LIVING_ROOTS:
        d = REPO / root
        if not d.is_dir():
            continue
        for doc in sorted(d.rglob("*.md")):
            if doc.name == "CLAUDE.md":
                continue
            try:
                text = doc.read_text(encoding="utf-8")
            except OSError:
                continue
            in_fence = False
            found_anchors: set[str] = set()
            for raw in text.splitlines():
                if FENCE.match(raw):
                    in_fence = not in_fence
                    continue
                if in_fence:
                    continue
                for span in CODE_SPAN.findall(raw):
                    span = span.strip()
                    m = ANCHOR.match(span)
                    if not m:
                        continue
                    path_part = m.group("path")
                    for t in targets:
                        if path_part == t or t.endswith("/" + path_part):
                            found_anchors.add(span)
            for a in sorted(found_anchors):
                hits.append((doc, a, ""))
    if not hits:
        return 0
    by_doc: dict[Path, list[str]] = {}
    for doc, anchor_text, _ in hits:
        by_doc.setdefault(doc, []).append(anchor_text)
    for doc, anchors_list in by_doc.items():
        print(f"{doc.relative_to(REPO)} ⇒ {', '.join(anchors_list[:6])}"
              + (f" (+{len(anchors_list) - 6} more)" if len(anchors_list) > 6 else ""))
    return 0


# --------------------------------------------------------------------------- #
# docs-check — surface diff via config bindings
# --------------------------------------------------------------------------- #


def cmd_docs_check(args) -> int:
    cfg = load_config()
    surfaces = cfg.get("surfaces", [])
    if isinstance(surfaces, dict):
        surfaces = [surfaces]
    if not surfaces:
        print("docs-check: no [[surfaces]] bindings in .rnd/config.toml — "
              "nothing to diff. Add one per surface doc (name, command, doc, pattern).")
        return 0
    total = 0
    for s in surfaces:
        name = s.get("name", "?")
        command, doc_rel, pattern = s.get("command"), s.get("doc"), s.get("pattern")
        if not (command and doc_rel and pattern):
            print(f"[{name}] incomplete binding (need command, doc, pattern) — skipped")
            continue
        doc_path = REPO / doc_rel
        if not doc_path.is_file():
            print(f"[{name}] doc {doc_rel} does not exist")
            total += 1
            continue
        try:
            out = subprocess.run(
                command, shell=True, capture_output=True, text=True,
                cwd=str(REPO), timeout=60,
            )
        except subprocess.SubprocessError as e:
            print(f"[{name}] enumeration command failed: {e}")
            total += 1
            continue
        if out.returncode != 0:
            print(f"[{name}] enumeration command exited {out.returncode}: "
                  f"{out.stderr.strip()[:200]}")
            total += 1
            continue
        registered = {ln.strip() for ln in out.stdout.splitlines() if ln.strip()}
        try:
            doc_text = doc_path.read_text(encoding="utf-8")
        except OSError as e:
            print(f"[{name}] cannot read doc: {e}")
            total += 1
            continue
        documented = set(re.findall(pattern, doc_text, re.MULTILINE))
        undocumented = sorted(registered - documented)
        ghosts = sorted(documented - registered)
        if not undocumented and not ghosts:
            print(f"[{name}] {len(registered)} registered · {len(documented)} "
                  f"documented · in sync")
            continue
        print(f"[{name}] {len(registered)} registered · {len(documented)} documented")
        for u in undocumented:
            print(f"  UNDOCUMENTED  {u}")
        for g in ghosts:
            print(f"  GHOST         {g}  (documented, not registered)")
        total += len(undocumented) + len(ghosts)
    if total:
        print(f"\ndocs-check: {total} finding(s).")
        return E_FINDINGS
    print("\ndocs-check: every configured surface is in sync.")
    return 0


# --------------------------------------------------------------------------- #
# standards — canon vs repo, binding regions preserved
# --------------------------------------------------------------------------- #

BINDING_OPEN = re.compile(r"<!--\s*rnd:binding\s+([\w-]+)\s*-->")
BINDING_CLOSE = re.compile(r"<!--\s*/rnd:binding\s*-->")

_STANDARDS_MAP = {
    "docs-CLAUDE.md": "docs/CLAUDE.md",
    "living-CLAUDE.md": "docs/living/CLAUDE.md",
    "architecture-CLAUDE.md": "docs/living/architecture/CLAUDE.md",
    "operations-CLAUDE.md": "docs/living/operations/CLAUDE.md",
    "doctrine-CLAUDE.md": "docs/living/doctrine/CLAUDE.md",
}


def _segment(text: str) -> list[tuple[str, str]]:
    """Split into [('canon', text) | ('binding:NAME', text)] segments."""
    segments: list[tuple[str, str]] = []
    kind, buf, bname = "canon", [], ""
    for line in text.splitlines(keepends=True):
        mo = BINDING_OPEN.search(line)
        mc = BINDING_CLOSE.search(line)
        if kind == "canon" and mo:
            buf.append(line)  # the marker line itself is canon
            segments.append(("canon", "".join(buf)))
            kind, buf, bname = "binding", [], mo.group(1)
            continue
        if kind == "binding" and mc:
            segments.append((f"binding:{bname}", "".join(buf)))
            kind, buf, bname = "canon", [line], ""
            continue
        buf.append(line)
    segments.append((kind if kind == "canon" else f"binding:{bname}", "".join(buf)))
    return segments


def cmd_standards(args) -> int:
    canon_dir = TEMPLATES / "standards"
    if not canon_dir.is_dir():
        print(f"standards: canon templates missing at {canon_dir}", file=sys.stderr)
        return E_USAGE

    if args.write:
        written = []
        for tmpl_name, repo_rel in _STANDARDS_MAP.items():
            tmpl = canon_dir / tmpl_name
            if not tmpl.is_file():
                continue
            dest = REPO / repo_rel
            if tmpl_name == "doctrine-CLAUDE.md" and not dest.parent.is_dir():
                authority = (load_config().get("doctrine") or {}).get("authority", "")
                if not authority:
                    continue  # doctrine tier only when an authority is bound
            canon_text = tmpl.read_text(encoding="utf-8")
            if dest.is_file():
                # Preserve existing binding contents by name.
                existing = {
                    k.split(":", 1)[1]: v
                    for k, v in _segment(dest.read_text(encoding="utf-8"))
                    if k.startswith("binding:")
                }
                out_parts: list[str] = []
                for k, v in _segment(canon_text):
                    if k.startswith("binding:"):
                        out_parts.append(existing.get(k.split(":", 1)[1], v))
                    else:
                        out_parts.append(v)
                new_text = "".join(out_parts)
            else:
                new_text = canon_text
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(new_text, encoding="utf-8")
            written.append(repo_rel)
        for w in written:
            print(f"wrote {w}")
        print(f"standards: {len(written)} file(s) written. Fill the binding regions.")
        return 0

    drift = 0
    for tmpl_name, repo_rel in _STANDARDS_MAP.items():
        tmpl, dest = canon_dir / tmpl_name, REPO / repo_rel
        if not tmpl.is_file() or not dest.is_file():
            continue
        canon_segs = [s for s in _segment(tmpl.read_text(encoding="utf-8"))]
        repo_segs = [s for s in _segment(dest.read_text(encoding="utf-8"))]
        canon_canon = [s for s in canon_segs if s[0] == "canon"]
        repo_canon = [s for s in repo_segs if s[0] == "canon"]
        canon_bnames = [s[0] for s in canon_segs if s[0].startswith("binding:")]
        repo_bnames = [s[0] for s in repo_segs if s[0].startswith("binding:")]
        if canon_bnames != repo_bnames:
            print(f"{repo_rel}: binding regions differ from canon "
                  f"({repo_bnames} vs {canon_bnames})")
            drift += 1
            continue
        if len(canon_canon) != len(repo_canon):
            print(f"{repo_rel}: canon structure differs (segment count)")
            drift += 1
            continue
        for (ck, cv), (rk, rv) in zip(canon_canon, repo_canon):
            if cv != rv:
                for i, (cl, rl) in enumerate(
                    zip(cv.splitlines() + [""], rv.splitlines() + [""])
                ):
                    if cl != rl:
                        print(f"{repo_rel}: drift outside binding regions —")
                        print(f"  canon: {cl[:100]!r}")
                        print(f"  repo:  {rl[:100]!r}")
                        break
                drift += 1
                break
    if drift:
        print(f"\nstandards: {drift} file(s) drifted from canon. "
              "Edits belong in the plugin's templates, or inside a binding region.")
        return E_FINDINGS
    print("standards: every standards file matches canon.")
    return 0


# --------------------------------------------------------------------------- #
# fm — frontmatter query
# --------------------------------------------------------------------------- #

DEFAULT_FM_ROOTS = (".rnd/backlog", "docs/design")


def _fm_files(roots: list[str]) -> list[Path]:
    files: list[Path] = []
    for r in roots:
        p = REPO / r
        if p.is_dir():
            files.extend(
                f for f in sorted(p.rglob("*.md")) if f.name != "CLAUDE.md"
            )
        elif p.is_file():
            files.append(p)
    return files


def cmd_fm(args) -> int:
    roots = args.paths or list(DEFAULT_FM_ROOTS)
    rows: list[tuple[Path, dict]] = []
    for f in _fm_files(roots):
        try:
            data, _ = parse_frontmatter(f.read_text(encoding="utf-8"))
        except OSError:
            continue
        if not data:
            continue
        if args.kind and data.get("kind") != args.kind:
            continue
        if args.status and data.get("status") != args.status:
            continue
        skip = False
        for cond in args.where or []:
            if "=" not in cond:
                print(f"fm: --where wants key=value, got {cond!r}", file=sys.stderr)
                return E_USAGE
            k, v = cond.split("=", 1)
            got = data.get(k)
            if isinstance(got, list):
                if v not in got:
                    skip = True
                    break
            elif got != v:
                skip = True
                break
        if skip:
            continue
        rows.append((f, data))
    if args.json:
        print(json.dumps(
            [{"path": str(p.relative_to(REPO)), **d} for p, d in rows], indent=2,
        ))
        return 0
    if not rows:
        print("fm: no matches.")
        return 0
    for p, d in rows:
        ident = d.get("id") or d.get("date") or ""
        bits = [str(p.relative_to(REPO)), ident,
                d.get("kind", ""), d.get("status", "")]
        print("  ".join(b for b in bits if b))
    return 0


# --------------------------------------------------------------------------- #
# backlog — new / close
# --------------------------------------------------------------------------- #


def _backlog_dir() -> Path:
    return REPO / ".rnd" / "backlog"


def _ensure_rnd() -> None:
    (_backlog_dir() / "closed").mkdir(parents=True, exist_ok=True)
    cfg = REPO / ".rnd" / "config.toml"
    if not cfg.is_file():
        seed = TEMPLATES / "config.toml"
        if seed.is_file():
            cfg.write_text(seed.read_text(encoding="utf-8"), encoding="utf-8")


def cmd_backlog_new(args) -> int:
    if args.kind not in BACKLOG_KINDS:
        print(f"backlog: kind must be one of {BACKLOG_KINDS}", file=sys.stderr)
        return E_USAGE
    _ensure_rnd()
    prefix = args.kind.upper()
    highest = 0
    for f in _backlog_dir().rglob("*.md"):
        m = re.match(rf"^{prefix}-(\d{{3}})", f.name)
        if m:
            highest = max(highest, int(m.group(1)))
    new_id = f"{prefix}-{highest + 1:03d}"
    fm = {
        "id": new_id,
        "kind": args.kind,
        "status": "open",
        "opened": today(),
        "files": args.files or [],
        "seen": "1",
        "last-seen": today(),
    }
    errs = validate_backlog(fm, new_id)
    if errs:
        print("\n".join(errs), file=sys.stderr)
        return E_USAGE
    body_tmpl = TEMPLATES / "backlog-item.md"
    body = ""
    if body_tmpl.is_file():
        _, body = parse_frontmatter(body_tmpl.read_text(encoding="utf-8"))
    body = body.replace("<title>", args.title)
    path = _backlog_dir() / f"{new_id}-{slugify(args.title)}.md"
    path.write_text(dump_frontmatter(fm) + (body or f"\n# {args.title}\n"),
                    encoding="utf-8")
    print(f"{new_id}  {path.relative_to(REPO)}")
    return 0


def cmd_backlog_close(args) -> int:
    bdir = _backlog_dir()
    matches = [
        f for f in bdir.glob("*.md") if f.name.startswith(args.id.upper() + "-")
        or parse_frontmatter(f.read_text(encoding="utf-8"))[0].get("id")
        == args.id.upper()
    ]
    if not matches:
        print(f"backlog: no open item {args.id}", file=sys.stderr)
        return E_USAGE
    if len(matches) > 1:
        print(f"backlog: {args.id} is ambiguous: "
              f"{[m.name for m in matches]}", file=sys.stderr)
        return E_USAGE
    src = matches[0]
    data, body = parse_frontmatter(src.read_text(encoding="utf-8"))
    data["status"] = "closed"
    data["closed"] = today()
    data["resolution"] = args.resolution
    errs = validate_backlog(data, src.name)
    if errs:
        print("\n".join(errs), file=sys.stderr)
        return E_USAGE
    dest = bdir / "closed" / src.name
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(dump_frontmatter(data) + body, encoding="utf-8")
    src.unlink()
    print(f"closed {data['id']} → {dest.relative_to(REPO)}")
    return 0


# --------------------------------------------------------------------------- #
# record — dated design record
# --------------------------------------------------------------------------- #


def cmd_record_new(args) -> int:
    if args.kind not in RECORD_KINDS:
        print(f"record: kind must be one of {RECORD_KINDS}", file=sys.stderr)
        return E_USAGE
    design_dir = REPO / "docs" / "design"
    design_dir.mkdir(parents=True, exist_ok=True)
    fm = {"kind": args.kind, "date": today(), "status": "live", "refs": []}
    errs = validate_record(fm, args.title)
    if errs:
        print("\n".join(errs), file=sys.stderr)
        return E_USAGE
    tmpl = TEMPLATES / "design-record.md"
    body = ""
    if tmpl.is_file():
        _, body = parse_frontmatter(tmpl.read_text(encoding="utf-8"))
    body = body.replace("<title>", args.title)
    path = design_dir / f"{today()}-{slugify(args.title)}.md"
    if path.exists():
        print(f"record: {path.relative_to(REPO)} already exists", file=sys.stderr)
        return E_USAGE
    path.write_text(dump_frontmatter(fm) + (body or f"\n# {args.title}\n"),
                    encoding="utf-8")
    print(str(path.relative_to(REPO)))
    return 0


# --------------------------------------------------------------------------- #
# init
# --------------------------------------------------------------------------- #


def cmd_init(args) -> int:
    _ensure_rnd()
    print(f"initialized .rnd/ at {REPO}")
    print("next: `rnd standards --write` scaffolds docs/ standards; "
          "fill the binding regions in .rnd/config.toml and docs/**/CLAUDE.md.")
    return 0


# --------------------------------------------------------------------------- #
# main
# --------------------------------------------------------------------------- #


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="rnd", description=__doc__.split("\n")[0],
    )
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("fm", help="query records + backlog by frontmatter")
    p.add_argument("paths", nargs="*", help=f"roots (default: {DEFAULT_FM_ROOTS})")
    p.add_argument("--kind")
    p.add_argument("--status")
    p.add_argument("--where", action="append", metavar="key=value")
    p.add_argument("--json", action="store_true")
    p.set_defaults(fn=cmd_fm)

    p = sub.add_parser("anchors", help="the anchor gate")
    p.add_argument("paths", nargs="*", help=f"doc roots (default: {LIVING_ROOTS})")
    p.add_argument("--audit", action="store_true",
                   help="anchors that resolve but contradict their prose")
    p.add_argument("--fix", action="store_true", help="rewrite anchors in place")
    p.add_argument("--dry-run", action="store_true", help="show what --fix would do")
    p.add_argument("--suggest", action="store_true",
                   help="print candidates for banned anchors")
    p.set_defaults(fn=cmd_anchors)

    p = sub.add_parser("affected", help="living docs citing these source files")
    p.add_argument("files", nargs="+")
    p.set_defaults(fn=cmd_affected)

    p = sub.add_parser("docs-check", help="surface docs vs the real surface")
    p.set_defaults(fn=cmd_docs_check)

    p = sub.add_parser("standards", help="docs standards vs plugin canon")
    p.add_argument("--write", action="store_true",
                   help="generate standards files, preserving binding regions")
    p.set_defaults(fn=cmd_standards)

    p = sub.add_parser("backlog", help="backlog item operations")
    bsub = p.add_subparsers(dest="bcmd", required=True)
    b = bsub.add_parser("new")
    b.add_argument("kind", choices=BACKLOG_KINDS)
    b.add_argument("title")
    b.add_argument("--files", nargs="*")
    b.set_defaults(fn=cmd_backlog_new)
    b = bsub.add_parser("close")
    b.add_argument("id")
    b.add_argument("--resolution", required=True)
    b.set_defaults(fn=cmd_backlog_close)

    p = sub.add_parser("record", help="dated design record operations")
    rsub = p.add_subparsers(dest="rcmd", required=True)
    r = rsub.add_parser("new")
    r.add_argument("title")
    r.add_argument("--kind", default="design", choices=RECORD_KINDS)
    r.set_defaults(fn=cmd_record_new)

    p = sub.add_parser("init", help="scaffold .rnd/")
    p.set_defaults(fn=cmd_init)

    args = ap.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
