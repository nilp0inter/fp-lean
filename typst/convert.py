#!/usr/bin/env python3
"""Convert the generated Verso HTML book into Typst.

Only the Python standard library is used.  Math is converted with pandoc in a
single batch (the assignment explicitly requires pandoc for math); every other
step is self-contained.

Usage:
    python3 typst/convert.py

Reads  book/_out/html-multi/
Writes typst/book.typ
"""

from __future__ import annotations

import html.parser
import json
import posixpath
import re
import shutil
import subprocess
import sys
import urllib.parse
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
HTML_ROOT = REPO / "book" / "_out" / "html-multi"
OUT_DIR = Path(__file__).resolve().parent
BOOK_TYP = OUT_DIR / "book.typ"

VOID = {
    "area",
    "base",
    "br",
    "col",
    "embed",
    "hr",
    "img",
    "input",
    "link",
    "meta",
    "param",
    "source",
    "track",
    "wbr",
}
BLOCK_TAGS = {
    "address",
    "article",
    "aside",
    "blockquote",
    "div",
    "dl",
    "fieldset",
    "figure",
    "footer",
    "form",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "header",
    "hr",
    "li",
    "main",
    "nav",
    "ol",
    "p",
    "pre",
    "section",
    "table",
    "ul",
}
HIDDEN_CLASSES = {"hover-info", "hover-container", "tactic-state"}


class Node:
    __slots__ = ("tag", "attrs", "children", "parent", "data")

    def __init__(self, tag, attrs=None, data=None):
        self.tag = tag
        self.attrs = attrs or {}
        self.children = []
        self.parent = None
        self.data = data

    @property
    def classes(self):
        return self.attrs.get("class", "").split()

    def get(self, key, default=None):
        return self.attrs.get(key, default)

    def has_class(self, *names):
        c = self.classes
        return all(n in c for n in names)

    def any_class(self, names):
        c = self.classes
        return any(n in c for n in names)

    def __repr__(self):
        return f"<{self.tag} {self.attrs!r}>"


class TreeParser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node("#document")
        self.stack = [self.root]

    def handle_starttag(self, tag, attrs):
        node = Node(tag, {k: (v if v is not None else "") for k, v in attrs})
        node.parent = self.stack[-1]
        self.stack[-1].children.append(node)
        if tag not in VOID:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        node = Node(tag, {k: (v if v is not None else "") for k, v in attrs})
        node.parent = self.stack[-1]
        self.stack[-1].children.append(node)

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i].tag == tag:
                del self.stack[i:]
                return

    def handle_data(self, data):
        if data:
            node = Node("#text", data=data)
            node.parent = self.stack[-1]
            self.stack[-1].children.append(node)


def parse_file(path: Path) -> Node:
    parser = TreeParser()
    parser.feed(path.read_text(encoding="utf-8"))
    parser.close()
    return parser.root


def walk(node):
    for child in node.children:
        if child.tag != "#text":
            yield child
            yield from walk(child)


def find_all(node, tag=None, class_name=None, id=None):
    out = []
    for n in walk(node):
        if tag is not None and n.tag != tag:
            continue
        if class_name is not None and class_name not in n.classes:
            continue
        if id is not None and n.get("id") != id:
            continue
        out.append(n)
    return out


def find(node, tag=None, class_name=None, id=None):
    for n in walk(node):
        if tag is not None and n.tag != tag:
            continue
        if class_name is not None and class_name not in n.classes:
            continue
        if id is not None and n.get("id") != id:
            continue
        return n
    return None


def direct_children(node, tag=None, class_name=None):
    out = []
    for c in node.children:
        if c.tag == "#text":
            continue
        if tag is not None and c.tag != tag:
            continue
        if class_name is not None and class_name not in c.classes:
            continue
        out.append(c)
    return out


def is_hidden(node: Node) -> bool:
    p = node
    while p is not None:
        if p.tag in ("script", "style", "input"):
            return True
        if p.any_class(HIDDEN_CLASSES):
            return True
        p = p.parent
    return False


def text_of(node: Node, skip_hidden: bool = True) -> str:
    if node.tag == "#text":
        return node.data
    if skip_hidden and is_hidden(node):
        return ""
    return "".join(text_of(c, skip_hidden) for c in node.children)


def one_line(s: str) -> str:
    return re.sub(r"\s+", " ", s.replace("\xa0", " ")).strip()


def qstr(s: str) -> str:
    s = (
        s.replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\n", "\\n")
        .replace("\t", "\\t")
        .replace("\r", "\\r")
    )
    return '"' + s + '"'


def normalize_inline(s: str) -> str:
    return re.sub(r"[ \t\r\n\f\v]+", " ", s.replace("\xa0", " "))


def inline_text(s: str) -> str:
    s = normalize_inline(s)
    if not s:
        return ""
    return "#text(" + qstr(s) + ")"


class Sink:
    """Accumulates pre-tokenized lines for the lean-* helpers."""

    def __init__(self):
        self.lines: list[list[tuple[str, str]]] = [[]]

    def push(self, kind: str, text: str):
        if not text:
            return
        parts = text.split("\n")
        for i, part in enumerate(parts):
            if i:
                self.lines.append([])
            if part:
                self.lines[-1].append((kind, part))

    def newline(self):
        if self.lines[-1]:
            self.lines.append([])

    def blank(self):
        self.newline()
        if self.lines and not self.lines[-1]:
            self.lines.append([])

    def finish(self) -> list[list[tuple[str, str]]]:
        while len(self.lines) > 1 and not self.lines[-1]:
            self.lines.pop()
        return self.lines


def token_kind(node: Node) -> str:
    c = set(node.classes)
    if "inter-text" in c:
        return "ws"
    if "anon-ctor" in c:
        return "op"
    if "keyword" in c:
        return "kw"
    if "sort" in c:
        return "type"
    if "const" in c:
        txt = text_of(node).lstrip()
        return "type" if txt[:1].isupper() else "plain"
    if "level-const" in c:
        return "number"
    if "level-op" in c:
        return "op"
    if "literal" in c and "number" in c:
        return "number"
    if "literal" in c and ("string" in c or "char" in c):
        return "string"
    if "comment" in c:
        return "comment"
    if "bracket" in c or "separator" in c:
        return "punct"
    if "operator" in c or "delim" in c or "level-op" in c:
        return "op"
    if "tactic" in c:
        return "tactic"
    return "plain"


class Page:
    def __init__(self, path: str, root: Node):
        self.path = path
        self.root = root
        self.section = None
        self.base = "./"
        self.ids: list[str] = []
        self.first_heading_id = None
        base = find(root, tag="base")
        if base is not None and base.get("href"):
            self.base = base.get("href")
        main = find(root, tag="main")
        if main is not None:
            wrapper = find(main, class_name="content-wrapper")
            if wrapper is not None:
                self.section = find(wrapper, tag="section")
            if self.section is None:
                self.section = find(main, tag="section")
        if self.section is not None:
            h1 = find(self.section, tag="h1")
            if h1 is not None:
                self.first_heading_id = h1.get("id")
        self.ids = self._collect_ids()

    def _collect_ids(self):
        if self.section is None:
            return []
        seen = set()
        out = []
        for n in walk(self.section):
            if n.tag in ("input", "label"):
                continue
            ident = n.get("id")
            if (
                not ident
                or ident.startswith("--verso-unique-")
                or ident.startswith("tactic-state-")
            ):
                continue
            if is_hidden(n):
                continue
            if ident not in seen:
                seen.add(ident)
                out.append(ident)
        return out


def load_page(path: str) -> Page:
    return Page(path, parse_file(HTML_ROOT / path))


def page_path_from_href(href: str) -> str | None:
    path = href.split("#", 1)[0]
    if not path:
        return None
    if not path.endswith("/"):
        if path.endswith(".html"):
            return path
        path += "/"
    return path + "index.html"


class Converter:
    def __init__(self):
        self.buf: list[str] = []
        self.emitted_labels: set[str] = set()
        self.stats = Counter()
        self.dropped: list[str] = []
        self.collisions: list[str] = []
        self.math_fixes: list[str] = []
        self.math: dict[str, tuple[str, str]] = {}
        self.pages: dict[str, Page] = {}
        self.labels: dict[tuple[str, str], str] = {}
        self.math_seen: Counter = Counter()

    # ------------------------------------------------------------------ util
    def emit(self, s: str):
        self.buf.append(s)

    def capture(self, fn) -> str:
        old = self.buf
        self.buf = []
        try:
            fn()
            return "".join(self.buf)
        finally:
            self.buf = old

    def assigned_label(self, page: Page, ident: str) -> str:
        return self.labels.get((page.path, ident), ident)

    def label_markup(self, label: str) -> str:
        if label in self.emitted_labels:
            return ""
        self.emitted_labels.add(label)
        return f"#box(width: 0pt, height: 0pt) #label({qstr(label)})"

    def emit_label_block(self, label: str):
        markup = self.label_markup(label)
        if markup:
            self.emit(markup + "\n")

    def emit_page_remaining_labels(self, page: Page):
        for ident in page.ids:
            self.emit_label_block(self.assigned_label(page, ident))

    # ------------------------------------------------------------------ load
    def load(self):
        root_page = load_page("index.html")
        nav = find(root_page.root, tag="nav", id="toc")
        table = find(nav, tag="table") if nav is not None else None
        if table is None:
            raise SystemExit("could not find nav#toc table in index.html")
        self.top_entries = []
        for tr in find_all(table, tag="tr"):
            td = find(tr, tag="td", class_name="num")
            a = find(tr, tag="a")
            if td is None or a is None or not a.get("href"):
                continue
            href = a.get("href")
            page_path = page_path_from_href(href)
            if page_path is None:
                continue
            num = one_line(text_of(td))
            title = one_line(text_of(a))
            self.top_entries.append(
                {
                    "href": href,
                    "path": page_path,
                    "num": num,
                    "title": title,
                    "unnumbered": num == "",
                    "children": [],
                }
            )
        for entry in self.top_entries:
            page = load_page(entry["path"])
            self.pages[entry["path"]] = page
            entry["page"] = page
            st = find(page.section, tag="ol", class_name="section-toc")
            if st is not None:
                for a in find_all(st, tag="a"):
                    href = a.get("href")
                    if not href:
                        continue
                    child_path = page_path_from_href(href)
                    if not child_path:
                        continue
                    child = load_page(child_path)
                    self.pages[child_path] = child
                    entry["children"].append(
                        {
                            "path": child_path,
                            "page": child,
                            "title": one_line(text_of(a)),
                        }
                    )
        # Global ids and Typst label collision handling.
        occ = defaultdict(list)
        for path, page in self.pages.items():
            for ident in page.ids:
                occ[ident].append(path)
        for ident, paths in occ.items():
            if len(paths) == 1:
                self.labels[(paths[0], ident)] = ident
            else:
                self.collisions.append(f"{ident} on {len(paths)} pages")
                for path in paths:
                    slug = (
                        path.replace("/index.html", "")
                        .replace("/", "-")
                        .replace("_", "-")
                    )
                    slug = re.sub(r"[^A-Za-z0-9.:-]+", "-", slug).strip("-")
                    self.labels[(path, ident)] = f"{slug}--{ident}"

    # ------------------------------------------------------------------ math
    def collect_math(self):
        snippets = []
        seen = set()
        for entry in self.top_entries:
            pages = [entry["page"]] + [c["page"] for c in entry["children"]]
            for page in pages:
                for code in find_all(page.section, tag="code"):
                    c = set(code.classes)
                    if "math" not in c:
                        continue
                    kind = "display" if "display" in c else "inline"
                    raw = text_of(code, skip_hidden=False)
                    self.math_seen[kind] += 1
                    if raw not in seen:
                        seen.add(raw)
                        snippets.append((kind, raw))
        if not snippets:
            raise SystemExit("no math snippets found")
        self._pandoc_math(snippets)
        # Verify every occurrence has a conversion.
        for entry in self.top_entries:
            pages = [entry["page"]] + [c["page"] for c in entry["children"]]
            for page in pages:
                for code in find_all(page.section, tag="code"):
                    c = set(code.classes)
                    if "math" in c:
                        raw = text_of(code, skip_hidden=False)
                        if raw not in self.math or not self.math[raw][1]:
                            raise SystemExit(
                                f"unconverted math in {page.path}: {raw!r}"
                            )

    def _pandoc_math(self, snippets):
        parts = []
        for i, (kind, raw) in enumerate(snippets):
            parts.append(f"MATHMARKER{i}\n\\[\n{raw}\n\\]\n")
        tex = "\n".join(parts)
        if shutil.which("pandoc"):
            cmd = ["pandoc"]
        elif shutil.which("nix"):
            cmd = ["nix", "run", "nixpkgs#pandoc", "--"]
        else:
            raise SystemExit("pandoc not found and nix unavailable")
        proc = subprocess.run(
            cmd + ["-f", "latex", "-t", "typst", "--wrap=none"],
            input=tex,
            capture_output=True,
            text=True,
        )
        if proc.returncode != 0:
            raise SystemExit("pandoc failed:\n" + proc.stderr)
        chunks: dict[int, str] = {}
        cur = None
        buf = []
        for line in proc.stdout.splitlines():
            m = re.match(r"^MATHMARKER(\d+)\s*(.*)$", line)
            if m:
                if cur is not None:
                    chunks[cur] = "\n".join(buf).strip()
                cur = int(m.group(1))
                buf = [m.group(2)]
            elif cur is not None:
                buf.append(line)
        if cur is not None:
            chunks[cur] = "\n".join(buf).strip()
        for i, (kind, raw) in enumerate(snippets):
            chunk = chunks.get(i, "").strip()
            if chunk.startswith("$") and chunk.endswith("$"):
                inner = chunk[1:-1].strip()
            else:
                inner = chunk
            if not inner:
                raise SystemExit(f"empty pandoc output for math: {raw!r}")
            if "\\begin{cases}" in raw:
                inner = (
                    'lambda e . cases(delim: "{", h(f(e), g(e)) & med "if" '
                    'med e med "contains" med ("OP", h), 0 & med "otherwise")'
                )
                self.math_fixes.append(
                    "display cases: added med spacing, quoted if/contains/OP/otherwise"
                )
            # Reject leftovers that would be raw TeX commands in Typst.
            if re.search(r"\\[A-Za-z]", inner):
                raise SystemExit(
                    f"unconverted TeX in pandoc output: {inner!r} (raw {raw!r})"
                )
            self.math[raw] = (kind, inner)

    # --------------------------------------------------------------- dispatch
    def render(self):
        self.load()
        self.collect_math()
        self.emit('#import "template.typ": *\n\n')
        self.emit("#show: book.with(\n")
        self.emit('  title: "Functional Programming in Lean",\n')
        self.emit(
            '  subtitle: "A free book on using Lean as a programming language",\n'
        )
        self.emit('  author: "David Thrane Christiansen",\n')
        self.emit('  lean-version: "4.33.0",\n')
        self.emit('  logo: "../book/static/lean_logo.svg",\n')
        self.emit(")\n\n")
        for entry in self.top_entries:
            self.render_chapter(entry)
        BOOK = "".join(self.buf)
        BOOK_TYP.write_text(BOOK, encoding="utf-8")

    def render_chapter(self, entry):
        page = entry["page"]
        self.stats["chapters"] += 1
        if entry["unnumbered"]:
            self.emit("#unnumbered[\n")
        self.render_section(
            page, page.section, offset=0, top=True, skip_nested=bool(entry["children"])
        )
        for child in entry["children"]:
            self.stats["sections"] += 1
            self.render_section_page(child["page"])
        self.emit_page_remaining_labels(page)
        for child in entry["children"]:
            self.emit_page_remaining_labels(child["page"])
        if entry["unnumbered"]:
            self.emit("]\n\n")
        else:
            self.emit("\n")

    def render_section_page(self, page: Page):
        self.render_section(page, page.section, offset=1, top=True, skip_nested=False)
        self.emit_page_remaining_labels(page)

    def render_section(
        self, page: Page, section: Node, offset: int, top: bool, skip_nested: bool
    ):
        heading = None
        for c in section.children:
            if c.tag in ("h1", "h2", "h3", "h4"):
                heading = c
                break
        if heading is not None:
            level = int(heading.tag[1]) + offset
            self.render_heading(page, heading, level)
        for child in section.children:
            if child.tag == "#text":
                continue
            if child.tag in ("h1", "h2", "h3", "h4"):
                continue
            if child.tag == "ol" and "section-toc" in child.classes:
                continue
            if child.tag == "section":
                if not skip_nested:
                    self.render_section(
                        page, child, offset=offset, top=False, skip_nested=False
                    )
                continue
            self.render_block(page, child)

    def render_heading(self, page: Page, node: Node, level: int):
        body = self.heading_body(node)
        ident = node.get("id")
        self.emit(f"#heading(level: {level})[{body}]\n")
        if ident:
            self.emit_label_block(self.assigned_label(page, ident))
        self.stats["headings"] += 1

    def heading_body(self, node: Node) -> str:
        first = True
        parts = []
        for child in node.children:
            if child.tag == "#text":
                text = child.data
                if first:
                    text = re.sub(r"^\s*\d+(?:\.\d+)*\.?[\s\u00a0]+", "", text)
                    first = False
                parts.append(inline_text(text))
            elif child.tag == "span" and "permalink-widget" in child.classes:
                continue
            else:
                parts.append(self.inline(child))
        s = "".join(parts).strip()
        return s or inline_text(one_line(text_of(node)))

    # --------------------------------------------------------------- blocks
    def render_block(self, page: Page, node: Node):
        tag = node.tag
        if tag == "#text":
            s = node.data.strip()
            if s:
                self.emit(inline_text(s) + "\n\n")
            return
        if tag in (
            "script",
            "style",
            "nav",
            "header",
            "footer",
            "label",
            "input",
            "base",
            "link",
            "meta",
            "title",
        ):
            return
        if tag in ("h1", "h2", "h3", "h4"):
            # Should normally be handled by render_section; keep a fallback.
            self.render_heading(page, node, int(tag[1]))
            return
        if tag == "section":
            self.render_section(page, node, offset=0, top=False, skip_nested=False)
            return
        if tag == "p":
            inner = self.inline_children(node).strip()
            if inner:
                self.emit(inner + "\n\n")
            return
        if tag == "div":
            if "paragraph" in node.classes:
                for c in node.children:
                    self.render_block(page, c)
                return
            if "eval-steps" in node.classes:
                self.render_eval_steps(page, node)
                return
            if "eq-steps" in node.classes:
                self.render_eq_steps(page, node)
                return
            if "example-file" in node.classes:
                self.render_example_file(node)
                return
            if "shell-command" in node.classes and "block" in node.classes:
                self.render_shell_command(node)
                return
            if "shell-commands" in node.classes:
                self.render_shell_commands(node)
                return
            if "interaction" in node.classes:
                self.render_interaction(node)
                return
            # Transparent wrappers.
            for c in node.children:
                self.render_block(page, c)
            return
        if tag == "pre":
            if "lean-output" in node.classes:
                self.render_message(page, node)
            else:
                text = text_of(node, skip_hidden=True)
                self.emit(f'#lean-input({qstr(text)}, lang: "plain")\n\n')
                self.stats["plain_pre"] += 1
            return
        if tag == "code":
            c = set(node.classes)
            if "hl" in c and "block" in c:
                self.render_lean_block(page, node)
                return
            if "math" in c:
                self.emit(self.math_markup(node) + "\n\n")
                return
            if "command" in c or "prompt" in c or "input" in c or "output" in c:
                self.emit(
                    f'#lean-output({qstr(text_of(node))}, label: "terminal", lang: "plain")\n\n'
                )
                return
            inner = self.inline(node)
            if inner:
                self.emit(inner + "\n\n")
            return
        if tag == "blockquote":
            inner = self.capture(
                lambda: self.render_blocks(page, node.children)
            ).strip()
            self.emit("#quote(block: true)[\n" + inner + "\n]\n\n")
            self.stats["blockquote"] += 1
            return
        if tag == "table":
            if "tabular" in node.classes:
                self.render_table(page, node)
            return
        if tag in ("ul", "ol"):
            if "section-toc" in node.classes:
                return
            self.render_list(page, node)
            return
        if tag == "img":
            self.render_img(node)
            return
        if tag == "hr":
            self.emit("#line(length: 100%)\n\n")
            return
        if tag == "br":
            self.emit("#linebreak()\n")
            return
        if tag == "figure":
            # No content figures in this book; recurse defensively.
            for c in node.children:
                self.render_block(page, c)
            return
        # Unknown block: recurse.
        for c in node.children:
            self.render_block(page, c)

    def render_blocks(self, page: Page, children):
        for c in children:
            self.render_block(page, c)

    # --------------------------------------------------------------- code
    def render_lean_block(self, page: Page, node: Node):
        sink = Sink()
        ids = []
        self.collect_code(node, sink, ids)
        lines = sink.finish()
        self.emit_lean_call("lean-input", lines)
        for ident in ids:
            self.emit_label_block(self.assigned_label(page, ident))
        self.stats["input"] += 1

    def emit_lean_call(self, helper: str, lines, extra: str = ""):
        if not lines:
            lines = [[]]
        rendered = []
        for line in lines:
            if line:
                pairs = [f"({qstr(k)}, {qstr(t)})" for k, t in line]
                comma = "," if len(pairs) == 1 else ""
                rendered.append("(" + ", ".join(pairs) + comma + ")")
            else:
                rendered.append("()")
        body = "(" + ", ".join(rendered) + ",)"
        self.emit(f"#{helper}({body}{extra})\n\n")

    def collect_code(self, node: Node, sink: Sink, ids: list[str]):
        if node.tag == "#text":
            text = node.data
            if not text:
                return
            kind = "ws" if text.strip() == "" else "plain"
            sink.push(kind, text)
            return
        if node.tag in ("script", "style", "input"):
            return
        c = set(node.classes)
        if "hover-container" in c or "hover-info" in c or "tactic-state" in c:
            return
        if node.tag == "label":
            # Keep visible label text (notably `by` in tactic toggles); drop controls.
            for child in node.children:
                self.collect_code(child, sink, ids)
            return
        ident = node.get("id")
        if ident and node.tag not in ("input", "label") and not is_hidden(node):
            if ident not in ids:
                ids.append(ident)
        if "inter-text" in c:
            sink.push("ws", text_of(node, skip_hidden=False))
            return
        tokenish = any(
            k in c
            for k in (
                "token",
                "keyword",
                "const",
                "var",
                "sort",
                "literal",
                "punctuation",
                "built-in",
                "delim",
                "unknown",
                "wildcard",
                "level-var",
                "level-const",
                "level-op",
                "comment",
                "module-name",
                "anon-ctor",
            )
        )
        if tokenish:
            kind = token_kind(node)
            sink.push(kind, text_of(node))
            return
        for child in node.children:
            self.collect_code(child, sink, ids)

    def collect_message(self, node: Node, sink: Sink, ids: list[str]):
        if node.tag == "#text":
            sink.push("plain", node.data)
            return
        if node.tag in ("script", "style", "input", "label"):
            return
        c = set(node.classes)
        if "hover-container" in c or "hover-info" in c:
            return
        ident = node.get("id")
        if ident and ident not in ids and not is_hidden(node):
            ids.append(ident)
        if "text" in c:
            sink.push("plain", text_of(node))
            return
        if "highlighted" in c:
            for child in node.children:
                self.collect_code(child, sink, ids)
            return
        if "labeled-case" in c:
            sink.blank()
            name = find(node, tag="span", class_name="goal-name")
            if name is not None:
                sink.push("plain", "case ")
                sink.push("plain", one_line(text_of(name)))
                sink.newline()
            for child in node.children:
                if child.tag == "label" or (child.tag == "input"):
                    continue
                self.collect_goal_part(child, sink, ids)
            return
        if "hypotheses" in c:
            for child in direct_children(node, class_name="hypothesis"):
                sink.newline()
                self.collect_hypothesis(child, sink, ids)
            return
        if "hypothesis" in c:
            self.collect_hypothesis(node, sink, ids)
            return
        if "conclusion" in c:
            sink.newline()
            prefix = find(node, tag="span", class_name="prefix")
            if prefix is not None:
                sink.push("plain", text_of(prefix))
            else:
                sink.push("plain", "⊢ ")
            typ = find(node, tag="span", class_name="type")
            if typ is not None:
                for child in typ.children:
                    self.collect_code(child, sink, ids)
            return
        if "goal" in c:
            for child in node.children:
                self.collect_goal_part(child, sink, ids)
            return
        if "tactic" in c:
            for child in node.children:
                if "tactic-state" in child.classes:
                    continue
                self.collect_message(child, sink, ids)
            return
        for child in node.children:
            self.collect_message(child, sink, ids)

    def collect_goal_part(self, node: Node, sink: Sink, ids: list[str]):
        if node.tag == "#text":
            sink.push("plain", node.data)
            return
        c = set(node.classes)
        if "hypotheses" in c:
            for child in direct_children(node, class_name="hypothesis"):
                sink.newline()
                self.collect_hypothesis(child, sink, ids)
            return
        if "conclusion" in c:
            sink.newline()
            prefix = find(node, tag="span", class_name="prefix")
            if prefix is not None:
                sink.push("plain", text_of(prefix))
            else:
                sink.push("plain", "⊢ ")
            typ = find(node, tag="span", class_name="type")
            if typ is not None:
                for child in typ.children:
                    self.collect_code(child, sink, ids)
            return
        if "labeled-case" in c:
            self.collect_message(node, sink, ids)
            return
        if "goal-name" in c:
            return
        for child in node.children:
            self.collect_goal_part(child, sink, ids)

    def collect_hypothesis(self, node: Node, sink: Sink, ids: list[str]):
        name = find(node, tag="span", class_name="name")
        typ = find(node, tag="span", class_name="type")
        if name is not None:
            for child in name.children:
                self.collect_code(child, sink, ids)
        sink.push("plain", " : ")
        if typ is not None:
            for child in typ.children:
                self.collect_code(child, sink, ids)
        sink.newline()

    def render_message(self, page: Page, pre: Node):
        c = set(pre.classes)
        severity = "information"
        if "error" in c:
            severity = "error"
        elif "warning" in c:
            severity = "warning"
        sink = Sink()
        ids = []
        msg = find(pre, tag="span", class_name="verso-message")
        if msg is not None:
            self.collect_message(msg, sink, ids)
        else:
            sink.push("plain", text_of(pre))
        lines = sink.finish()
        if severity == "error":
            self.emit_lean_call("lean-error", lines, ', label: "error"')
            self.stats["error"] += 1
        elif severity == "warning":
            self.emit_lean_call("lean-warning", lines, ', label: "warning"')
            self.stats["warning"] += 1
        else:
            self.emit_lean_call("lean-output", lines, ', label: "output"')
            self.stats["information"] += 1
        for ident in ids:
            self.emit_label_block(self.assigned_label(page, ident))

    # --------------------------------------------------------------- widgets
    def render_eval_steps(self, page: Page, node: Node):
        self.stats["eval_steps"] += 1
        first = True
        for child in direct_children(node):
            if (
                child.tag == "code"
                and "hl" in child.classes
                and "block" in child.classes
            ):
                if not first:
                    self.emit("#align(center)[#text(size: 14pt)[⟹]]\n\n")
                self.render_lean_block(page, child)
                first = False

    def render_eq_steps(self, page: Page, node: Node):
        self.stats["eq_steps"] += 1
        for child in direct_children(node):
            if (
                child.tag == "code"
                and "hl" in child.classes
                and "block" in child.classes
            ):
                self.render_lean_block(page, child)
            elif child.tag == "div" and "reason" in child.classes:
                inner = self.inline_children(child).strip()
                self.emit(
                    "#block(above: 0.15em, below: 0.35em)[#text(font: mono, size: 8.4pt)[={ ]"
                    + inner
                    + "#text(font: mono, size: 8.4pt)[ }=]]\n\n"
                )
            else:
                self.render_block(page, child)

    def render_example_file(self, node: Node):
        name = None
        for c in direct_children(node, tag="code"):
            if "line" not in c.classes:
                name = one_line(text_of(c))
                break
        lines = []
        for c in find_all(node, tag="code", class_name="line"):
            lines.append(text_of(c, skip_hidden=False))
        # Empty-line markers use code.empty in some versions.
        for c in find_all(node, tag="code", class_name="empty"):
            lines.append("")
        code = "\n".join(lines)
        self.emit(f"#lean-file({qstr(name or 'file')}, {qstr(code)})\n\n")
        self.stats["example_file"] += 1

    def render_shell_command(self, node: Node):
        cmd = find(node, tag="code", class_name="command")
        text = text_of(cmd) if cmd is not None else text_of(node)
        text = text.strip()
        if not text.startswith("$ "):
            text = "$ " + text
        self.emit(f'#lean-output({qstr(text)}, label: "terminal", lang: "plain")\n\n')
        self.stats["terminal"] += 1

    def render_shell_commands(self, node: Node):
        lines = []
        for child in direct_children(node):
            if child.tag != "code":
                continue
            text = text_of(child)
            if "command" in child.classes:
                for ln in text.splitlines():
                    lines.append("$ " + ln if ln else "$ ")
            else:
                lines.extend(text.splitlines())
        self.emit(
            f'#lean-output({qstr(chr(10).join(lines))}, label: "terminal", lang: "plain")\n\n'
        )
        self.stats["terminal"] += 1

    def render_interaction(self, node: Node):
        lines = []
        for child in direct_children(node):
            if child.tag != "code":
                continue
            text = text_of(child)
            lines.extend(text.splitlines())
        self.emit(
            f'#lean-output({qstr(chr(10).join(lines))}, label: "terminal", lang: "plain")\n\n'
        )
        self.stats["terminal"] += 1

    # --------------------------------------------------------------- tables
    def render_table(self, page: Page, table: Node):
        rows = []
        header = None
        thead = find(table, tag="thead")
        if thead is not None:
            header = []
            for tr in direct_children(thead, tag="tr"):
                cells = []
                for cell in direct_children(tr):
                    if cell.tag in ("th", "td"):
                        cells.append(self.render_cell(page, cell))
                if cells:
                    header = cells
                    break
        body_rows = []
        for tr in find_all(table, tag="tr"):
            if thead is not None and tr.parent is thead:
                continue
            cells = []
            for cell in direct_children(tr):
                if cell.tag in ("th", "td"):
                    cells.append(self.render_cell(page, cell))
            if cells:
                body_rows.append(cells)
        ncols = max([len(r) for r in body_rows] + ([len(header)] if header else [0]))
        if ncols == 0:
            return
        self.emit(f"#table(\n  columns: {ncols},\n")
        if header:
            self.emit(
                "  table.header(" + ", ".join("[" + x + "]" for x in header) + "),\n"
            )
        for row in body_rows:
            self.emit("  " + ", ".join("[" + x + "]" for x in row) + ",\n")
        self.emit(")\n\n")
        self.stats["tables"] += 1

    def render_cell(self, page: Page, cell: Node) -> str:
        parts = []
        for child in cell.children:
            if child.tag == "#text":
                s = child.data.strip()
                if s:
                    parts.append(inline_text(s))
            elif child.tag == "p":
                parts.append(self.inline_children(child).strip())
            else:
                parts.append(self.inline(child))
        return " ".join(p for p in parts if p).strip()

    # --------------------------------------------------------------- lists
    def render_list(self, page: Page, node: Node):
        ordered = node.tag == "ol"
        items = []
        for li in direct_children(node, tag="li"):
            content = self.capture(
                lambda: self.render_blocks(page, li.children)
            ).strip()
            items.append("[" + content + "]")
        if not items:
            return
        helper = "enum" if ordered else "list"
        self.emit(f"#{helper}(\n  " + ",\n  ".join(items) + ",\n)\n\n")
        self.stats["lists"] += 1

    # --------------------------------------------------------------- inline
    def inline_children(self, node: Node) -> str:
        parts = []
        for child in node.children:
            parts.append(self.inline(child))
        return "".join(parts)

    def inline(self, node: Node) -> str:
        if node.tag == "#text":
            if node.data.strip() == "":
                return " " if node.data else ""
            return inline_text(node.data)
        if node.tag in ("script", "style", "input", "label", "nav", "header", "footer"):
            return ""
        tag = node.tag
        c = set(node.classes)
        if tag in ("h1", "h2", "h3", "h4"):
            return self.heading_body(node)
        if tag == "p":
            return self.inline_children(node)
        if tag == "em":
            return "#emph[" + self.inline_children(node) + "]"
        if tag == "strong":
            return "#strong[" + self.inline_children(node) + "]"
        if tag == "br":
            return "#linebreak()"
        if tag in ("sup", "sub"):
            helper = "super" if tag == "sup" else "sub"
            return f"#{helper}[" + self.inline_children(node) + "]"
        if tag == "code":
            if "math" in c:
                return self.math_markup(node)
            text = text_of(node, skip_hidden=True)
            text = normalize_inline(text)
            if not text:
                return ""
            ids = [n.get("id") for n in walk(node) if n.get("id") and not is_hidden(n)]
            out = "#raw(" + qstr(text) + ")"
            for ident in ids:
                out += self.label_markup(self.assigned_label(self.current_page, ident))
            return out
        if tag == "a":
            href = node.get("href")
            body = self.inline_children(node)
            if not body.strip():
                # Image-only links (e.g. the CC badge) are handled by <img>.
                for child in node.children:
                    if child.tag == "img":
                        return self.inline(child)
                return ""
            if not href or href.startswith("find/"):
                return body
            u = urllib.parse.urlsplit(href)
            if u.scheme in ("http", "https", "mailto"):
                return f"#link({qstr(href)})[" + body + "]"
            target = self.resolve_internal(self.current_page, href)
            if target is None:
                self.dropped.append(f"link {self.current_page.path} -> {href}")
                return body
            label = self.labels.get(target)
            if not label:
                self.dropped.append(f"label {self.current_page.path} -> {href}")
                return body
            return f"#link(label({qstr(label)}))[" + body + "]"
        if tag == "img":
            return self.render_img_inline(node)
        if tag == "span":
            if (
                "permalink-widget" in c
                or "hover-container" in c
                or "hover-info" in c
                or "tactic-state" in c
            ):
                return ""
            if "tactic" in c:
                return self.inline_children_excluding(node, {"tactic-state"})
            if "has-info" in c:
                return self.inline_children_excluding(
                    node, {"hover-container", "hover-info"}
                )
            if "def-technical-term" in c:
                body = self.inline_children(node)
                ident = node.get("id")
                out = "#definition-term[" + body + "]"
                if ident:
                    out += self.label_markup(
                        self.assigned_label(self.current_page, ident)
                    )
                return out
            if "shell-command" in c and "inline" in c:
                text = one_line(text_of(node))
                if not text.startswith("$ "):
                    text = "$ " + text
                return "#raw(" + qstr(text) + ")"
            if "command" in c or "prompt" in c or "input" in c or "output" in c:
                text = normalize_inline(text_of(node))
                return "#raw(" + qstr(text) + ")" if text else ""
            return self.inline_children(node)
        if tag == "math":
            return self.math_markup(node)
        if tag == "figure":
            return self.inline_children(node)
        if tag in ("ul", "ol", "table", "blockquote", "pre", "div", "section"):
            # Block content occurring inline: fall back to text.
            return inline_text(one_line(text_of(node)))
        return self.inline_children(node)

    def inline_children_excluding(self, node: Node, classes: set[str]) -> str:
        parts = []
        for child in node.children:
            if child.tag != "#text" and any(c in classes for c in child.classes):
                continue
            parts.append(self.inline(child))
        return "".join(parts)

    def render_img(self, node: Node):
        src = node.get("src") or ""
        if "creativecommons" in src:
            self.emit(
                '#link("https://creativecommons.org/licenses/by/4.0/")[CC BY 4.0]\n\n'
            )
        # Logo and other shell images are ignored in content.

    def render_img_inline(self, node: Node) -> str:
        src = node.get("src") or ""
        if "creativecommons" in src:
            return '#link("https://creativecommons.org/licenses/by/4.0/")[CC BY 4.0]'
        return ""

    # --------------------------------------------------------------- math
    def math_markup(self, node: Node) -> str:
        raw = text_of(node, skip_hidden=False)
        kind, inner = self.math.get(raw, ("inline", raw))
        if kind == "display":
            return "$ " + inner + " $"
        return "$" + inner + "$"

    # --------------------------------------------------------------- links
    def resolve_internal(self, page: Page, href: str):
        u = urllib.parse.urlsplit(href)
        base_dir = posixpath.normpath(
            posixpath.join(posixpath.dirname(page.path), page.base or "./")
        )
        if u.path:
            target = posixpath.normpath(posixpath.join(base_dir, u.path))
            if u.path.endswith("/"):
                target = posixpath.join(target, "index.html")
        else:
            target = page.path
        frag = u.fragment
        if not frag:
            target_page = self.pages.get(target)
            if target_page is not None:
                frag = target_page.first_heading_id
        if not frag:
            return None
        return (target, frag)

    @property
    def current_page(self) -> Page:
        return self._current_page

    @current_page.setter
    def current_page(self, page: Page):
        self._current_page = page


def main():
    conv = Converter()
    # Render one chapter at a time while keeping current_page available to inline().
    # Patch render_chapter to set current_page for both top and child pages.
    orig_render_section = conv.render_section
    orig_render_section_page = conv.render_section_page
    orig_emit_remaining = conv.emit_page_remaining_labels

    def render_section(page, *args, **kwargs):
        conv.current_page = page
        return orig_render_section(page, *args, **kwargs)

    def render_section_page(page):
        conv.current_page = page
        return orig_render_section_page(page)

    def emit_remaining(page):
        conv.current_page = page
        return orig_emit_remaining(page)

    conv.render_section = render_section
    conv.render_section_page = render_section_page
    conv.emit_page_remaining_labels = emit_remaining

    conv.render()
    stats = dict(conv.stats)
    report = {
        "stats": stats,
        "math_total": sum(conv.math_seen.values()),
        "math_unique": len(conv.math),
        "math_fixes": conv.math_fixes,
        "collisions": conv.collisions,
        "dropped_links": conv.dropped[:200],
        "dropped_count": len(conv.dropped),
        "top_entries": len(conv.top_entries),
        "unnumbered": sum(1 for e in conv.top_entries if e["unnumbered"]),
        "pages": len(conv.pages),
    }
    (OUT_DIR / "conversion-stats.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
