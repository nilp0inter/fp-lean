# HTML -> Typst conversion report

## Deliverables

- Converter: `typst/convert.py` (Python 3.14, standard library only; calls pandoc once for math)
- Generated source: `typst/book.typ` (1.9 MB, 9,736 lines)
- PDF: `typst/fp-lean.pdf` (**394 pages**, 5,991,608 bytes / 5.99 MB)
- Compile log: `typst/compile-book.log` (0 bytes; zero errors, zero warnings)
- Representative PNGs:
  - `typst/book-pages/page-1.png` (p. 1, title page)
  - `typst/book-pages/page-3.png` (p. 3, contents)
  - `typst/book-pages/page-11.png` (p. 11, chapter 1 opener)
  - `typst/book-pages/page-13.png` (p. 13, code-heavy page)
  - `typst/book-pages/page-14.png` (p. 14, error message page)
  - `typst/book-pages/page-171.png` (p. 171, the "On the other hand, bind" paragraph; the old defect page reflowed here)
  - `typst/book-pages/page-174.png` (p. 174, eval-steps page)
  - `typst/book-pages/feature-file.png` (p. 77, `#lean-file` blocks)
  - `typst/book-pages/feature-eq.png` (p. 206, `={ ... }=` eq-step reasons)
  - `typst/book-pages/feature-terminal.png` (p. 70, label `terminal` transcript)
  - `typst/book-pages/feature-eval.png` (p. 167, `⟹` eval-steps)
  - Earlier supplemental renders: `page-60.png`, `page-68.png`, `page-71.png`,
    `page-78.png`, `page-92.png`, `page-95.png`, `page-96.png`, `page-165.png`,
    `page-172.png`
- Machine-readable counts: `typst/conversion-stats.json`
- PDF text extraction used for spot checks: `typst/fp-lean.txt`

Compile command (from the repository root):

```text
nix run nixpkgs#typst -- compile --root . --font-path book/static/fonts \
  typst/book.typ typst/fp-lean.pdf
```

## Acceptance counts

| Item | HTML count | Emitted count | Delta |
|---|---:|---:|---:|
| Chapters / top-level entries | 13 (9 numbered + 4 unnumbered) | 13 | 0 |
| Section pages | 57 | 57 | 0 |
| Content headings (`h1`-`h4`) | 395 (excluding root `Contents`, title, search, find) | 395 | 0 |
| `lean-input` blocks | 1270 | 1270 (+12 plain `<pre>` via `lean-input(..., lang:"plain")`) | 0 |
| Information output | 191 | 191 | 0 |
| Error output | 194 | 194 | 0 |
| Warning output | 4 | 4 | 0 |
| `eval-steps` | 32 | 32 | 0 |
| `eq-steps` | 5 | 5 | 0 |
| `example-file` | 12 | 12 `lean-file` calls | 0 |
| Content tables (`table.tabular`) | 6 | 6 | 0 |
| Math snippets | 132 | 132 (69 unique) | 0 |
| Terminal/transcript blocks | 16 | 16 | 0 |
| Block quotes | 1 | 1 | 0 |
| Labels | 947 content ids | 947 unique `#label(...)` calls | 0 |
| Internal links | 0 dropped | 0 dropped | 0 |

Heading breakdown in the generated Typst source:
`level 1: 13`, `level 2: 81`, `level 3: 232`, `level 4: 64`, `level 5: 5`.
The 395 content headings match the HTML after excluding the skipped root `Contents`
heading, the title-page heading, and the two utility pages.

## Source mapping

- Page order comes from `nav#toc` in the root `index.html`; chapter pages are merged with
  their `ol.section-toc` child pages.
- Chapter-page `h1` -> level 1; section-page `h1` -> level 2; nested `h2` -> level 3,
  `h3` -> level 4, `h4` -> level 5. Single-page front matter/interludes use
  `h1 -> 1`, `h2 -> 2`, etc.
- Introduction, Acknowledgments, and both interludes are wrapped in `#unnumbered[...]`.
- Leading heading numbers (`1.`, `1.1.`, etc. plus U+00A0) are stripped; Typst numbers
  headings. Every original heading id is attached via `#label("...")`.
- All 947 content ids were globally unique, so no namespacing was needed. There were no
  label collisions.
- Code uses the template's pre-tokenized form. The token map is the one from
  `html-structure.md`: keyword->kw, sort->type, upper-case const->type, otherwise
  const->plain, anon-ctor->op, number/level-const->number, string/char->string,
  comments->comment, brackets/separators->punct, operators/delimiters/level-op->op,
  var/unknown/wildcard/module-name/level-var->plain, `inter-text`->ws.
- `.hover-info`, `input` controls, and `.tactic-state` popups are dropped. Visible
  `pre.lean-output` messages and visible case labels/conclusions are kept; proof-state
  lines are reconstructed as `name : type` and `⊢ type`.
- `eval-steps` emit a centered `⟹` between blocks. `eq-steps` reasons are emitted as
  `={ reason }=` lines.
- `example-file` -> `#lean-file(name, code)`.
- Shell/transcript blocks -> `lean-output(..., label: "terminal", lang: "plain")` with
  `$ ` prompts where CSS supplied them.
- Tables -> `#table(columns: n, table.header(...), ...)`; cells are traversed inline.
- Math: all 132 snippets were batched through pandoc in one invocation. One hand-fix was
  needed: the display `cases` formula received explicit `med` spacing and quoted
  `if`/`contains`/`OP`/`otherwise`; Pandoc's `times`, `mono(...)`, `upright(...)`,
  `lr(|...|)`, and literal `{...}` output was verified to render correctly in Typst and
  left as produced.
- Inline code is rendered as `#raw("...")`; inline highlighted Lean code therefore uses
  the template's uniform inline-code chip rather than per-token colors. This is the main
  visual deviation from the HTML.
- Final template update: inline code now uses a breakable `highlight` instead of
  unbreakable boxes. The full book was recompiled with the updated template; long inline
  code spans no longer force stretched inter-word spacing. This reflow reduced the final
  book from 401 to 394 pages. The "On the other hand, bind" paragraph moved from the old
  p. 174 to p. 171; `page-171.png` confirms its spacing is now even.
- Token-level ids are attached immediately after their containing code block (or after
  inline code) as zero-width labeled boxes. This preserves link targets, but a link to a
  token jumps to the end of its code block rather than to the exact glyph.
- External non-doc links are `#link("url")[...]`; internal links resolve through the
  HTML `<base>` and become `#link(label("id"))[...]`. Documentation links wrapped around
  code tokens are dropped, keeping the token text.

## Dropped or intentionally omitted

- Search page, search index/assets, `find/` redirect, permalinks, prev/next navigation,
  sidebar TOC, canonical/trailing-slash scripts, Plausible analytics, and TOC resizing
  controls: all shell/navigation, not book content.
- Hidden hover tooltips and interactive tactic-state popups (see above).
- The HTML title page, copyright page, and full contents page are replaced by the
  template's generated title page, copyright page, and TOC.
- Plain `<pre>` content (other languages and program output) is emitted as unhighlighted
  `lean-input(..., lang:"plain")`; it is not syntax-highlighted.
- No footnotes, figures, SVGs, or index entries existed in the HTML, so none are emitted.

## Spot checks against the HTML

1. **1.1 Evaluating Expressions (PDF p. 7-10, PNG p. 11/13/14).** The HTML input blocks
   became highlighted `lean-input` blocks; the `⟹` eval steps are present; the
   `Could not synthesize ...` message appears as an `ERROR` block; inline `#eval` and
   `String.append` are inline code chips. The HTML `<code class="hl lean block">` /
   `<pre class="lean-output error">` sequence is preserved in order.
2. **Interlude: Propositions, Proofs, and Indexing (PDF p. 90, PNG p. 92/96).** The
   four-column/three-column content table is rendered through `table.header`, with Lean
   snippets in cells kept as inline code. The interlude is unnumbered and starts with the
   accent rule rather than a chapter number, matching `#unnumbered`.
3. **4.3 Example: Arithmetic in Monads (PDF p. 171, PNG p. 171).** The display `cases`
   formula from raw TeX is rendered as a centered Typst display equation with the two
   cases, `if`/`contains`/`OP`/`otherwise` upright. The surrounding `Reader` code blocks
   preserve indentation and token coloring.

## PDF text checks

`pdftotext` over the final PDF found zero occurrences of `<span`, `</`, `&lt;`, `&gt;`,
`&amp;`, `\begin`, `\mathrm`, `\mathtt`, `\left`, `\frac`, `href=`, or `class=`.
The compile log is empty, so there were no "label not found" or other Typst warnings.

## Environment deviations

- Pandoc 3.7.0.2 via `nix run nixpkgs#pandoc`; Typst 0.15.1 via
  `nix run nixpkgs#typst`.
- Conversion itself is pure Python 3.14 standard library; no pip/uv packages.
- No tracked repository files or `typst/template.typ` were modified.
