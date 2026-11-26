// ============================================================================
// Functional Programming in Lean — print book template
//
// Build (fonts + preview), from the repository root:
//   nix run nixpkgs#typst -- compile --root .. --font-path book/static/fonts \
//       typst/preview.typ typst/preview.pdf
//
// API (see bottom for a compact reference):
//   #book(title, subtitle, author, lean-version, body)
//   #unnumbered[...]                       // front matter / interlude chapters
//   #lean-input(code, lang: "lean")
//   #lean-file(name, code, lang: "lean")    // filename line + input block
//   #lean-output(code, label: "output")
//   #lean-error(code, label: "error")
//   #lean-warning(code, label: "warning")
//   #lean-term(code, label: "term")
//   #index-item(term, pages)
//   #print-index(((term, pages), ...))
//
// `code` for every lean-* helper is one of:
//   1. a string:        #lean-input("def x := 1")
//   2. a fenced block:  #lean-input(```lean ... ```)
//   3. pre-tokenized:   #lean-input((
//                         (("kw", "def"), ("ws", " "), ("plain", "x")),
//                         (("ws", "  "), ("op", ":="), ("ws", " "), ("number", "1")),
//                       ))
//      An array of lines; each line is an array of (kind, text) pairs.
//      Kinds: "kw", "tactic", "string", "comment", "number", "type", "op",
//      "punct", "ws", "plain". This bypasses the built-in Lean lexer, so
//      nested /- -/ and doc /-- -/ comments supplied by the converter are
//      rendered exactly as classified.
// ============================================================================

// ---------------------------------------------------------------------------
// Palette
// ---------------------------------------------------------------------------
#let ink        = rgb("#181B21")
#let ink-soft   = rgb("#3D444E")
#let muted      = rgb("#6B7480")
#let faint      = rgb("#9AA3AE")
#let accent     = rgb("#1E5A8A")
#let accent-soft = rgb("#DCE7F1")
#let accent-wash = rgb("#F2F6FA")
#let rule       = rgb("#D5DBE3")
#let code-bg    = rgb("#F6F7F9")
#let code-rule  = rgb("#2E6C9E")

// Syntax colours: low-saturation, print-safe.
#let syn-kw      = rgb("#6E3A94")
#let syn-tactic  = rgb("#116A5B")
#let syn-string  = rgb("#A34227")
#let syn-comment = rgb("#7A828D")
#let syn-number  = rgb("#8A5A00")
#let syn-type    = rgb("#1B5688")
#let syn-op      = rgb("#5A6472")
#let syn-error   = rgb("#8E2F20")
#let warn-ink    = rgb("#8A6212")

#let err-bg   = rgb("#FCF1EF")
#let err-rule = rgb("#B4432F")
#let warn-bg  = rgb("#FDF7E9")
#let warn-rule = rgb("#B98724")

// ---------------------------------------------------------------------------
// Typography
// ---------------------------------------------------------------------------
#let serif = ("Source Serif 4", "Libertinus Serif", "DejaVu Serif")
#let sans  = ("Source Sans 3", "DejaVu Sans")
#let mono  = ("Source Code Pro", "Noto Sans Mono", "DejaVu Sans Mono")

#let page-w = 185mm
#let page-h = 260mm
#let text-w = 143mm

#let body-size = 10.5pt

// ---------------------------------------------------------------------------
// State
// ---------------------------------------------------------------------------
#let front = state("front-matter", true)

// ---------------------------------------------------------------------------
// Running heads / folios
// ---------------------------------------------------------------------------
#let running-head(book-title: "") = context {
  if front.get() { return }
  let p = counter(page).get().first()
  let opener = query(heading.where(level: 1)).any(h => h.location().page() == here().page())
  if opener or p <= 1 { return }
  let chapters = query(heading.where(level: 1).before(here()))
  let sections = query(heading.where(level: 2).before(here()))
  let chapter = if chapters.len() > 0 { chapters.last().body } else { book-title }
  let section = if sections.len() > 0 { sections.last().body } else { chapter }
  let even = calc.even(p)
  set text(font: sans, size: 7.8pt, fill: muted, tracking: 0.55pt)
  block(width: 100%, above: 0pt, below: 0pt)[
    #align(if even { left } else { right }, if even { chapter } else { section })
    #v(3.2pt)
    #line(length: 100%, stroke: 0.45pt + rule)
  ]
}

#let folio() = context {
  let fmt = if front.get() { "i" } else { "1" }
  let even = calc.even(counter(page).get().first())
  set text(font: sans, size: 8.8pt, fill: muted)
  block(width: 100%, above: 0pt, below: 0pt)[
    #align(if even { left } else { right }, counter(page).display(fmt))
  ]
}

// ---------------------------------------------------------------------------
// Code rendering
//
// A small Lean-aware lexer runs inside Typst so a converter can pass plain
// source strings. Whitespace is laid out explicitly to keep indentation.
// ---------------------------------------------------------------------------
#let lean-keywords = (
  "abbrev", "axiom", "by", "catch", "class", "def", "deriving", "do", "else",
  "end", "example", "exists", "extends", "for", "forall", "from", "fun",
  "have", "if", "import", "in", "include", "inductive", "instance", "let",
  "local", "macro", "match", "mutual", "namespace", "noncomputable", "notation",
  "omit", "opaque", "open", "partial", "private", "protected", "public",
  "repeat", "return", "section", "set_option", "show", "structure", "syntax",
  "then", "theorem", "throw", "try", "universe", "unsafe", "using", "variable",
  "where", "while", "with", "lemma", "attribute", "export", "initialize",
  "elab", "macro_rules", "infix", "infixl", "infixr", "prefix", "postfix",
  "scoped", "break", "continue", "unless", "finally", "termination_by",
  "decreasing_by", "simp", "at", "generalizing", "renaming", "hint",
)
#let lean-tactics = (
  "apply", "assumption", "cases", "constructor", "contradiction", "decide",
  "exact", "first", "focus", "have", "induction", "injection", "intro",
  "intros", "left", "rfl", "right", "rw", "simp", "simp_all", "sorry",
  "subst", "trivial", "unfold", "use", "omega", "linarith", "norm_num",
  "ring", "field_simp", "aesop", "tauto", "done", "skip", "next", "case",
  "all_goals", "any_goals", "try", "repeat", "conv", "calc", "ext", "funext",
  "split", "left", "right", "exfalso", "by_contra", "contrapose", "push_neg",
)

#let is-digit(c) = c >= "0" and c <= "9"
#let is-lower(c) = c >= "a" and c <= "z"
#let is-upper(c) = c >= "A" and c <= "Z"
#let is-alpha(c) = is-lower(c) or is-upper(c)
#let is-space(c) = c == " " or c == "\t"
#let op-chars = "+-*/=<>|&^%$#@~\\:,;()[]{}.!?".clusters()
#let is-op(c) = op-chars.contains(c)

#let syn-colour(kind) = {
  if kind == "kw" { syn-kw }
  else if kind == "tactic" { syn-tactic }
  else if kind == "string" { syn-string }
  else if kind == "comment" { syn-comment }
  else if kind == "number" { syn-number }
  else if kind == "type" { syn-type }
  else if kind == "op" { syn-op }
  else { ink }
}

// Tokenise one line into (kind, text) pairs.
#let tokenize-line(line, lang: "lean") = {
  if lang != "lean" { return (("plain", line),) }
  let chars = line.clusters()
  let n = chars.len()
  let toks = ()
  let i = 0
  while i < n {
    let c = chars.at(i)
    let buf = c
    i += 1
    if c == "-" and i < n and chars.at(i) == "-" {
      while i < n {
        buf += chars.at(i)
        i += 1
      }
      toks.push(("comment", buf))
    } else if c == "\"" {
      let done = false
      while i < n and not done {
        let d = chars.at(i)
        buf += d
        i += 1
        if d == "\\" and i < n {
          buf += chars.at(i)
          i += 1
        } else if d == "\"" {
          done = true
        }
      }
      toks.push(("string", buf))
    } else if is-digit(c) {
      while i < n and {
        let d = chars.at(i)
        is-digit(d) or d == "." or d == "_"
      } {
        buf += chars.at(i)
        i += 1
      }
      toks.push(("number", buf))
    } else if is-space(c) {
      while i < n and is-space(chars.at(i)) {
        buf += chars.at(i)
        i += 1
      }
      toks.push(("ws", buf))
    } else if is-alpha(c) or c == "_" or "αβγδελστ".contains(c) {
      while i < n and {
        let d = chars.at(i)
        is-alpha(d) or is-digit(d) or "_'!?.".contains(d)
      } {
        buf += chars.at(i)
        i += 1
      }
      let kind = if lean-keywords.contains(buf) or buf == "λ" { "kw" }
        else if lean-tactics.contains(buf) { "tactic" }
        else if is-upper(buf.first()) { "type" }
        else { "plain" }
      toks.push((kind, buf))
    } else if is-op(c) {
      toks.push((if "()[]{},;".contains(c) { "punct" } else { "op" }, buf))
    } else {
      toks.push(("plain", buf))
    }
  }
  toks
}

#let render-tokens(toks, size: 8.4pt) = {
  let parts = ()
  for (kind, t) in toks {
    if kind == "ws" {
      if t.len() <= 1 {
        parts.push(text(" "))
      } else {
        parts.push(h(0.6 * size * t.len()))
      }
    } else if kind == "comment" {
      parts.push(text(fill: syn-comment, style: "italic", t))
    } else if kind == "punct" {
      parts.push(text(fill: ink-soft, t))
    } else {
      parts.push(text(fill: syn-colour(kind), t))
    }
  }
  parts.join()
}

/// Accepts a plain string or a fenced raw block (```lean ... ```).
#let source-text(code) = if type(code) == type("") { code } else { code.text }

/// `code` may be:
///  - a string,
///  - a fenced raw block,
///  - an array of lines, each an array of (kind, text) pairs, where kind is
///    one of "kw", "tactic", "string", "comment", "number", "type", "op",
///    "punct", "ws", "plain". Pre-tokenized lines bypass the built-in lexer.
#let code-lines(code, lang: "lean", size: 8.4pt) = {
  let pretokenized = type(code) == type(())
  let lines = if pretokenized { code } else { source-text(code).trim("\n").split("\n") }
  let rendered = ()
  for (idx, line) in lines.enumerate() {
    let toks = if pretokenized { line } else { tokenize-line(line, lang: lang) }
    rendered.push(render-tokens(toks, size: size))
    if idx < lines.len() - 1 { rendered.push(linebreak()) }
  }
  set text(font: mono, size: size, lang: "en", hyphenate: false)
  set par(justify: false, leading: 0.52em)
  rendered.join()
}

#let lean-code-block(code, lang: "lean", label: none, file: none, fill: code-bg,
                     bar: code-rule, label-colour: muted, text-size: 8.4pt) = {
  block(
    width: 100%,
    breakable: true,
    fill: fill,
    stroke: (left: 2.2pt + bar),
    inset: (left: 9pt, right: 8pt, top: 6.5pt, bottom: 6.5pt),
    radius: (right: 1.5pt),
    above: 1.15em,
    below: 1.15em,
  )[
    #if label != none [
      #text(font: sans, size: 6.9pt, fill: label-colour, tracking: 1.1pt)[#upper(label)]
      #v(2.2pt)
    ]
    #if file != none [
      #text(font: sans, size: 6.6pt, fill: faint, tracking: 1.1pt)[FILE]
      #h(0.65em)
      #text(font: sans, size: 7.7pt, fill: muted, file)
      #v(2.8pt)
    ]
    #code-lines(code, lang: lang, size: text-size)
  ]
}

/// Lean source input (default helper for ```lean / ```anchor / ``` blocks).
#let lean-input(code, lang: "lean", label: none) = lean-code-block(code, lang: lang, label: label)

/// An example source file: filename line above a lean-input-style block.
/// `code` accepts a string, a raw block, or a pre-tokenized line array.
#let lean-file(name, code, lang: "lean") = lean-code-block(code, lang: lang, file: name)

/// Evaluator output / info block: muted, no tinted background.
#let lean-output(code, label: "output", lang: "lean") = lean-code-block(
  code, lang: lang, label: label, fill: rgb("#FBFBFC"),
  bar: rgb("#C3CAD4"), label-colour: muted, text-size: 8.2pt)

/// Error block.
#let lean-error(code, label: "error", lang: "lean") = lean-code-block(
  code, lang: lang, label: label, fill: err-bg,
  bar: err-rule, label-colour: syn-error)

/// Warning block.
#let lean-warning(code, label: "warning", lang: "lean") = lean-code-block(
  code, lang: lang, label: label, fill: warn-bg,
  bar: warn-rule, label-colour: warn-ink)

/// Terms / evaluation steps, shown like output but with a neutral rule.
#let lean-term(code, label: "term", lang: "lean") = lean-code-block(
  code, lang: lang, label: label, fill: accent-wash,
  bar: accent-soft, label-colour: muted)

// ---------------------------------------------------------------------------
// Title page and copyright page
// ---------------------------------------------------------------------------
#let title-page(title, subtitle, author, lean-version, logo) = page(
  header: none, footer: none, numbering: none,
  margin: (inside: 23mm, outside: 19mm, top: 24mm, bottom: 22mm),
)[
  #set text(font: serif, fill: ink)
  #v(14mm)
  #align(center)[
    #if logo != none {
      image(logo, width: 46mm)
    } else {
      text(font: sans, size: 34pt, weight: "semibold", fill: accent)[λ]
    }
  ]
  #v(12mm)
  #align(center)[
    #block(width: 62mm, height: 0.8pt, fill: rule)
  ]
  #v(10mm)
  #align(center)[
    #text(font: serif, size: 25pt, weight: "semibold", tracking: -0.2pt, title)
  ]
  #if subtitle != none [
    #v(5mm)
    #align(center)[
      #text(font: serif, size: 12.5pt, style: "italic", fill: ink-soft, subtitle)
    ]
  ]
  #v(16mm)
  #align(center)[
    #text(font: sans, size: 12pt, weight: "medium", tracking: 0.7pt, author)
  ]
  #v(1fr)
  #align(center)[
    #block(width: 62mm, height: 0.6pt, fill: rule)
    #v(4mm)
    #text(font: sans, size: 8.5pt, fill: muted, tracking: 0.9pt)[#upper("Lean " + lean-version)]
    #v(1.6mm)
    #text(font: sans, size: 8.5pt, fill: muted, tracking: 0.9pt)[FREE EDITION · CC BY 4.0]
  ]
]

#let copyright-page(year: "2026", lean-version: "4.33.0") = page(
  header: none, footer: none, numbering: none,
  margin: (inside: 23mm, outside: 19mm, top: 24mm, bottom: 22mm),
)[
  #v(1fr)
  #block(width: 84mm)[
    #set text(font: serif, size: 8.5pt, fill: ink-soft)
    #set par(leading: 0.62em)
    #text(font: sans, size: 8pt, weight: "semibold", tracking: 0.8pt, fill: ink)[
      FUNCTIONAL PROGRAMMING IN LEAN
    ]
    #v(3mm)
    Copyright © Microsoft Corporation 2023 and Lean FRO, LLC 2023–#year.
    #v(2mm)
    This work is licensed under the Creative Commons Attribution 4.0
    International License (CC BY 4.0). You are free to share and adapt the
    material for any purpose, provided you give appropriate credit, link to
    the license, and indicate if changes were made.
    #v(2mm)
    License: https://creativecommons.org/licenses/by/4.0/legalcode
    #v(2mm)
    Source: https://github.com/leanprover/fp-lean/
    #v(2mm)
    Code samples tested with Lean #lean-version. Typeset in Source Serif 4,
    Source Sans 3, and Source Code Pro.
  ]
]

// ---------------------------------------------------------------------------
// Headings
// ---------------------------------------------------------------------------
#let chapter-title(it) = {
  pagebreak(weak: true)
  block(width: 100%, breakable: false, above: 0pt, below: 2.4em)[
    #v(8mm)
    #if it.numbering != none [
      #context {
        let n = counter(heading).get().first()
        text(font: sans, size: 64pt, weight: "light", fill: accent-soft,
          tracking: -1.5pt, if n < 10 { "0" + str(n) } else { str(n) })
      }
      #v(-6mm)
    ] else [
      #block(width: 9mm, height: 2pt, fill: accent)
      #v(5mm)
    ]
    #text(font: sans, size: 26pt, weight: "semibold", fill: ink,
      tracking: -0.2pt, it.body)
    #v(4mm)
    #block(width: 28mm, height: 1.4pt, fill: accent)
  ]
}

#let section-title(it) = block(above: 1.7em, below: 0.75em, sticky: true)[
  #if it.numbering != none [
    #context text(font: sans, size: 9pt, weight: "semibold", fill: accent,
      tracking: 0.4pt)[#counter(heading).display()]
    #h(0.7em)
  ]
  #text(font: sans, size: 13.5pt, weight: "semibold", fill: ink, it.body)
]

#let subsection-title(it) = block(above: 1.35em, below: 0.55em, sticky: true)[
  #text(font: sans, size: 10.8pt, weight: "semibold", style: "italic",
    fill: accent, it.body)
]

#let subsubsection-title(it) = block(above: 1.1em, below: 0.45em, sticky: true)[
  #text(font: sans, size: 10pt, weight: "semibold", fill: ink, it.body)
]

#let heading-level-5(it) = block(above: 0.95em, below: 0.35em, sticky: true)[
  #text(font: sans, size: 9.5pt, style: "italic", fill: muted, it.body)
]

// ---------------------------------------------------------------------------
// Main book wrapper
// ---------------------------------------------------------------------------
#let book(title: none, subtitle: none, author: none,
          lean-version: "4.33.0", logo: none, body) = {
  set document(title: title, author: author)
  set page(
    width: page-w, height: page-h,
    margin: (inside: 23mm, outside: 19mm, top: 21mm, bottom: 21mm),
    numbering: none,
    header: running-head(book-title: title),
    footer: folio(),
  )
  set text(font: serif, size: body-size, fill: ink, lang: "en", hyphenate: true)
  set par(justify: true, leading: 0.66em, spacing: 0.95em, first-line-indent: 0pt)
  set heading(numbering: "1.1")
  set list(marker: [•], spacing: 0.5em, indent: 1.25em)
  set enum(spacing: 0.5em, indent: 1.35em)
  set quote(block: true)
  set figure(gap: 0.9em)

  show heading.where(level: 1): chapter-title
  show heading.where(level: 2): section-title
  show heading.where(level: 3): subsection-title
  show heading.where(level: 4): subsubsection-title
  show heading.where(level: 5): heading-level-5

  // Inline code: quiet tinted chip that may break across lines.
  show raw.where(block: false): it => highlight(
    fill: rgb("#F1F3F6"),
    extent: 2pt,
    top-edge: 0.62em,
    bottom-edge: 0.12em,
    text(font: mono, size: 0.88em, fill: ink-soft, it.text),
  )

  show link: it => {
    let external = type(it.dest) == type("") and it.dest.starts-with("http")
    if external {
      underline(stroke: 0.45pt + accent-soft, offset: 2.4pt, text(fill: ink, it.body))
    } else {
      text(fill: ink, it.body)
    }
  }
  show quote.where(block: true): it => block(
    width: 100%,
    inset: (left: 12pt, right: 4pt, top: 2pt, bottom: 2pt),
    stroke: (left: 2pt + accent-soft),
    above: 1.25em, below: 1.25em,
  )[
    #set text(fill: ink-soft, style: "italic")
    #set par(justify: false)
    #it.body
  ]

  show table: set table(
    stroke: (x: none, y: 0.45pt + rule),
    inset: (x: 7pt, y: 4.8pt),
  )
  show table.cell.where(y: 0): set text(font: sans, size: 9pt, weight: "semibold")
  show table: it => block(
    width: 100%,
    stroke: (top: 0.8pt + rule, bottom: 0.8pt + rule),
    inset: (top: 3pt, bottom: 3pt),
    above: 1.1em, below: 0.5em,
  )[#it]

  show figure: it => block(width: 100%, above: 1.3em, below: 1.3em)[
    #align(center, it.body)
    #v(3pt)
    #align(center)[
      #set text(font: sans, size: 8.6pt, fill: muted)
      #it.caption
    ]
  ]
  show figure.caption: it => {
    text(weight: "semibold", fill: accent)[#it.supplement #it.numbering]
    text(" — ")
    it.body
  }

  show math.equation: set text(font: ("New Computer Modern Math", "Source Serif 4"))

  // Title matter.
  title-page(title, subtitle, author, lean-version, logo)
  copyright-page(lean-version: lean-version)

  // Table of contents (front matter, roman folios).
  page(header: none, footer: folio())[
    #v(6mm)
    #text(font: sans, size: 22pt, weight: "semibold", fill: ink)[Contents]
    #v(2mm)
    #block(width: 22mm, height: 1.4pt, fill: accent)
    #v(10mm)
    #set text(font: serif, size: 10pt)
    #show outline.entry: it => {
      let lvl = it.level
      block(
        width: 100%,
        above: if lvl == 1 { 0.85em } else { 0.02em },
        below: if lvl == 1 { 0.35em } else { 0.02em },
        inset: if lvl == 1 { (left: 0pt) } else { (left: 1.7em) },
      )[
        #grid(
          columns: (auto, 1fr, auto),
          column-gutter: 6pt,
          align: (left + bottom, bottom, right + bottom),
          if lvl == 1 {
            text(font: sans, size: 11pt, weight: "semibold")[
              #if it.element.numbering != none [#it.prefix()#h(0.7em)]
              #it.body()
            ]
          } else {
            text(font: serif, size: 9.7pt, fill: ink-soft)[
              #if it.element.numbering != none [#it.prefix()#h(0.6em)]
              #it.body()
            ]
          },
          text(fill: faint, box(width: 100%, height: 1em, clip: true, range(240).map(_ => ".").join())),
          if lvl == 1 {
            text(font: sans, size: 9.2pt, fill: muted)[#it.page()]
          } else {
            text(font: serif, size: 9pt, fill: muted)[#it.page()]
          },
        )
      ]
    }
    #outline(title: none, depth: 2)
  ]

  // Main matter: leave the TOC page, then restart the page counter.
  pagebreak(weak: true)
  counter(page).update(1)
  front.update(false)
  body
}

/// Mark a chapter as unnumbered (front matter or interludes). Place around the
/// chapter content so section headings inside it are unnumbered as well.
#let unnumbered(body) = {
  set heading(numbering: none)
  body
}

// ---------------------------------------------------------------------------
// Index helpers
// ---------------------------------------------------------------------------
#let index-item(term, pages) = grid(
  columns: (auto, 1fr, auto),
  column-gutter: 4pt,
  align: (left + bottom, bottom, right + bottom),
  term,
  text(fill: faint, box(width: 1fr, repeat[.])),
  text(font: sans, size: 9pt, fill: ink-soft, pages),
)

/// entries: array of (term, pages) pairs. Balanced two-column index layout.
#let print-index(entries) = {
  let n = entries.len()
  let mid = calc.ceil(n / 2)
  let column(items) = stack(
    spacing: 0.55em,
    ..items.map(((term, pages)) => index-item(term, pages)),
  )
  block(width: 100%, above: 1.2em, below: 1.2em)[
    #set par(justify: false, leading: 0.6em)
    #grid(
      columns: (1fr, 1fr),
      column-gutter: 12mm,
      column(entries.slice(0, mid)),
      if mid < n { column(entries.slice(mid)) },
    )
  ]
}

// ---------------------------------------------------------------------------
// Small conveniences used by generated documents
// ---------------------------------------------------------------------------
#let definition-term(body) = text(weight: "semibold", fill: ink, body)
#let aside(body) = block(
  width: 100%, fill: accent-wash, inset: 9pt, radius: 2pt,
  above: 1.1em, below: 1.1em,
)[#set text(size: 9.5pt); #body]

#let figure-placeholder(width: 100%, height: 42mm, caption: none) = figure(
  rect(width: width, height: height, fill: accent-wash, stroke: 0.5pt + rule,
    radius: 2pt, align(center + horizon, text(font: sans, size: 8.5pt, fill: faint)[figure])),
  caption: caption,
)
