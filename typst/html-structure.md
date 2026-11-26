# HTML structure of the generated *Functional Programming in Lean* book

This report describes the static HTML produced by:

```text
cd book
lake exe fp-lean --depth 2 --without-html-single --verbose
```

Output root: `book/_out/html-multi/`.

All class names, element names, attributes, and snippets below were verified in the
generated files, not inferred from the Lean sources. Feature counts are across the 73
generated `index.html` pages. HTML snippets are excerpts: long attribute values,
irrelevant siblings, and repeated token wrappers are sometimes elided, but the quoted
element names, classes, and attribute names are exact.

## 1. Output layout

The output is a directory-per-page static site. Every page is
`<directory>/index.html`; internal links use the directory URL with a trailing slash
and a fragment, never an `.html` filename.

Root-level files and directories:

```text
index.html                         title page + full table of contents
Introduction/                      front matter
Acknowledgments/                   front matter
Getting-to-Know-Lean/              chapter 1
Hello___-World___/                 chapter 2
Interlude___-Propositions___-Proofs___-and-Indexing/
Overloading-and-Type-Classes/      chapter 3
Monads/                            chapter 4
Functors___-Applicative-Functors___-and-Monads/  chapter 5
Monad-Transformers/                chapter 6
Programming-with-Dependent-Types/  chapter 7
Interlude___-Tactics___-Induction___-and-Proofs/
Programming___-Proving___-and-Performance/       chapter 8
Next-Steps/                        chapter 9
search/                            search UI, JavaScript-only
find/                              cross-reference redirect page, JavaScript-only
-verso-data/                       KaTeX, Tippy, Popper assets
-verso-search/                     search JS/CSS and index shards
-verso-docs.json                   numeric hover IDs -> HTML doc snippets
xref.json                          cross-reference database used by find/
book.css                           active generated stylesheet
verso-vars.css                     active CSS variables/theme overrides
toc-resize.js                      table-of-contents resizer
static/                            copied extra assets: logo, theme, fonts
```

(`-verso-data` and `-verso-search` start with a hyphen; quote them in shell commands.)

### 1.1 Page tree and book order

The order below is the order of `nav#toc` in `index.html`. Indentation means the second
page is a child page generated for a depth-2 section.

```text
index.html                                      Functional Programming in Lean (title page + contents)
Introduction/index.html                         Introduction
Acknowledgments/index.html                      Acknowledgments
Getting-to-Know-Lean/index.html                 1. Getting to Know Lean
  Getting-to-Know-Lean/Evaluating-Expressions/index.html          1.1. Evaluating Expressions
  Getting-to-Know-Lean/Types/index.html                            1.2. Types
  Getting-to-Know-Lean/Functions-and-Definitions/index.html        1.3. Functions and Definitions
  Getting-to-Know-Lean/Structures/index.html                       1.4. Structures
  Getting-to-Know-Lean/Datatypes-and-Patterns/index.html           1.5. Datatypes and Patterns
  Getting-to-Know-Lean/Polymorphism/index.html                     1.6. Polymorphism
  Getting-to-Know-Lean/Characters___-Strings___-and-Slices/index.html  1.7. Characters, Strings, and Slices
  Getting-to-Know-Lean/Additional-Conveniences/index.html         1.8. Additional Conveniences
  Getting-to-Know-Lean/Summary/index.html                          1.9. Summary
Hello___-World___/index.html                    2. Hello, World!
  Hello___-World___/Running-a-Program/index.html                  2.1. Running a Program
  Hello___-World___/Step-By-Step/index.html                       2.2. Step By Step
  Hello___-World___/Starting-a-Project/index.html                 2.3. Starting a Project
  Hello___-World___/Worked-Example___--cat/index.html             2.4. Worked Example: cat
  Hello___-World___/Additional-Conveniences/index.html            2.5. Additional Conveniences
  Hello___-World___/Summary/index.html                            2.6. Summary
Interlude___-Propositions___-Proofs___-and-Indexing/index.html     Interlude: Propositions, Proofs, and Indexing
Overloading-and-Type-Classes/index.html          3. Overloading and Type Classes
  Overloading-and-Type-Classes/Positive-Numbers/index.html         3.1. Positive Numbers
  Overloading-and-Type-Classes/Type-Classes-and-Polymorphism/index.html  3.2. Type Classes and Polymorphism
  Overloading-and-Type-Classes/Controlling-Instance-Search/index.html    3.3. Controlling Instance Search
  Overloading-and-Type-Classes/Arrays-and-Indexing/index.html             3.4. Arrays and Indexing
  Overloading-and-Type-Classes/Standard-Classes/index.html                3.5. Standard Classes
  Overloading-and-Type-Classes/Coercions/index.html                       3.6. Coercions
  Overloading-and-Type-Classes/Additional-Conveniences/index.html         3.7. Additional Conveniences
  Overloading-and-Type-Classes/Summary/index.html                         3.8. Summary
Monads/index.html                                4. Monads
  Monads/One-API___-Many-Applications/index.html                          4.1. One API, Many Applications
  Monads/The-Monad-Type-Class/index.html                                  4.2. The Monad Type Class
  Monads/Example___-Arithmetic-in-Monads/index.html                       4.3. Example: Arithmetic in Monads
  Monads/do--Notation-for-Monads/index.html                               4.4. do -Notation for Monads
  Monads/The-IO-Monad/index.html                                          4.5. The IO Monad
  Monads/Additional-Conveniences/index.html                               4.6. Additional Conveniences
  Monads/Summary/index.html                                               4.7. Summary
Functors___-Applicative-Functors___-and-Monads/index.html        5. Functors, Applicative Functors, and Monads
  Functors___-Applicative-Functors___-and-Monads/Structures-and-Inheritance/index.html  5.1. Structures and Inheritance
  Functors___-Applicative-Functors___-and-Monads/Applicative-Functors/index.html        5.2. Applicative Functors
  Functors___-Applicative-Functors___-and-Monads/The-Applicative-Contract/index.html    5.3. The Applicative Contract
  Functors___-Applicative-Functors___-and-Monads/Alternatives/index.html                5.4. Alternatives
  Functors___-Applicative-Functors___-and-Monads/Universes/index.html                   5.5. Universes
  Functors___-Applicative-Functors___-and-Monads/The-Complete-Definitions/index.html    5.6. The Complete Definitions
  Functors___-Applicative-Functors___-and-Monads/Summary/index.html                     5.7. Summary
Monad-Transformers/index.html                    6. Monad Transformers
  Monad-Transformers/Combining-IO-and-Reader/index.html                    6.1. Combining IO and Reader
  Monad-Transformers/A-Monad-Construction-Kit/index.html                   6.2. A Monad Construction Kit
  Monad-Transformers/Ordering-Monad-Transformers/index.html                6.3. Ordering Monad Transformers
  Monad-Transformers/More-do-Features/index.html                           6.4. More do Features
  Monad-Transformers/Additional-Conveniences/index.html                    6.5. Additional Conveniences
  Monad-Transformers/Summary/index.html                                    6.6. Summary
Programming-with-Dependent-Types/index.html      7. Programming with Dependent Types
  Programming-with-Dependent-Types/Indexed-Families/index.html                          7.1. Indexed Families
  Programming-with-Dependent-Types/The-Universe-Design-Pattern/index.html               7.2. The Universe Design Pattern
  Programming-with-Dependent-Types/Worked-Example___-Typed-Queries/index.html           7.3. Worked Example: Typed Queries
  Programming-with-Dependent-Types/Indices___-Parameters___-and-Universe-Levels/index.html  7.4. Indices, Parameters, and Universe Levels
  Programming-with-Dependent-Types/Pitfalls-of-Programming-with-Dependent-Types/index.html  7.5. Pitfalls of Programming with Dependent Types
  Programming-with-Dependent-Types/Summary/index.html                                   7.6. Summary
Interlude___-Tactics___-Induction___-and-Proofs/index.html        Interlude: Tactics, Induction, and Proofs
Programming___-Proving___-and-Performance/index.html  8. Programming, Proving, and Performance
  Programming___-Proving___-and-Performance/Tail-Recursion/index.html                    8.1. Tail Recursion
  Programming___-Proving___-and-Performance/Proving-Equivalence/index.html               8.2. Proving Equivalence
  Programming___-Proving___-and-Performance/Arrays-and-Termination/index.html            8.3. Arrays and Termination
  Programming___-Proving___-and-Performance/More-Inequalities/index.html                 8.4. More Inequalities
  Programming___-Proving___-and-Performance/Bounded-Numbers/index.html                   8.5. Bounded Numbers
  Programming___-Proving___-and-Performance/Insertion-Sort-and-Array-Mutation/index.html 8.6. Insertion Sort and Array Mutation
  Programming___-Proving___-and-Performance/Special-Types/index.html                     8.7. Special Types
  Programming___-Proving___-and-Performance/Summary/index.html                           8.8. Summary
Next-Steps/index.html                            9. Next Steps
search/index.html                                Search (utility)
find/index.html                                  Cross-Reference Redirection (utility)
```

In total there are 71 book pages (1 root, 2 front matter pages, 11
chapter/interlude pages, 57 section pages) plus 2 utility pages, for 73 `index.html`
files.

The 9 numbered chapters are interleaved with 2 unnumbered interludes; interludes do not
consume chapter numbers. Front matter (`Introduction`, `Acknowledgments`) is unnumbered.

### 1.2 Page types

| Page type | Detection | Content |
|---|---|---|
| Root index | `index.html` at output root | `div.titlepage` plus `ol.section-toc` with the whole book |
| Chapter page | `main section > h1` plus `ol.section-toc` | Chapter title, chapter introduction, list of child section pages |
| Section page | `main section > h1` (numbered `x.y`) plus nested `h2`/`h3`/`h4` | Section body; deeper headings remain on this page |
| Single-page front matter/interlude | `h1` plus `h2`s, no `ol.section-toc` | Entire chapter on one page |
| Utility | `search/`, `find/` | JavaScript UI/redirect only |

`Main.lean` uses `htmlDepth := 2`; depth-2 sections become separate pages. The
Introduction and both interludes use `htmlSplit := .never` in their source metadata, so
their `h2` sections stay on one page.

## 2. Common page shell

Every page has the same outer structure. `html` and `body` have no attributes (no
`lang`, no classes). A typical page starts:

```html
<!DOCTYPE html><html><head>...
<base href="./../../"/>
<meta charset="utf-8"/>
<meta name="viewport" content="height=device-height, width=device-width, ..."/>
<title>Evaluating Expressions</title>
<link rel="stylesheet" href="book.css"/>
<link rel="stylesheet" href="verso-vars.css"/>
...
</head><body>
<header>
  <div class="header-logo-wrapper">
    <a href="" id="logo"><img src="static/lean_logo.svg"/></a>
  </div>
  <div class="header-title-wrapper">
    <a class="header-title" href=""><h1>Functional Programming in Lean</h1></a>
  </div>
</header>
<label for="toggle-toc" id="toggle-toc-click">
  <span class="line line1"></span><span class="line line2"></span><span class="line line3"></span>
</label>
<div class="with-toc">
  <div class="toc-backdrop" onclick="document.getElementById('toggle-toc-click')?.click()"></div>
  <nav id="toc">...</nav>
  <div class="toc-resize-handle"></div>
  <main>
    <div class="content-wrapper">...</div>
  </main>
</div>
</body></html>
```

Key points:

- `<base href>` is essential. It is depth-specific:
  - root `index.html`: `<base href="./"/>`
  - depth-1 page, e.g. `Introduction/index.html`: `<base href="./../"/>`
  - depth-2 page, e.g. `Getting-to-Know-Lean/Evaluating-Expressions/index.html`:
    `<base href="./../../"/>`

  All internal `href`s are written as if from the site root (for example
  `Getting-to-Know-Lean/Types/#getting-to-know-types`), and `<base>` makes them resolve
  correctly. A parser that resolves relative to the page path will break.
- The page has **three `h1` elements**: the header title, the sidebar title, and the
  content heading. Across the 73 pages there are 219 `h1` elements (3 per page). To get
  the page heading, always select `main section h1`, not the first `h1`.
- `nav#toc` contains the sidebar, split TOCs, and the footer links. The footer is not in
  `main`; it is `div.last > ul#meta-links` inside the sidebar:
  `<li><a href="https://github.com/leanprover/fp-lean">Source Code</a></li>` and
  `<li><a href="https://github.com/leanprover/fp-lean/issues">Report Issues</a></li>`.
- The content wrapper has previous/next navigation twice, before and after the content:
  `<nav class="prev-next-buttons">` with `<a class="local-button active" rel="prev|next">`,
  `<span class="arrow">←</span>`, and `<span class="where">3.8. Summary</span>`.

Content lives at:

```html
<main>
  <div class="content-wrapper">
    <nav class="prev-next-buttons">...</nav>
    <section> ... page heading and body ... </section>
    <nav class="prev-next-buttons">...</nav>
  </div>
</main>
```

`<section>` elements have no `class` and no `id`. Section identity is carried by the
heading inside:

```html
<section>
  <h1 id="evaluating">1.1. Evaluating Expressions<span class="permalink-widget inline">...</span></h1>
  <p>...</p>
  <div class="paragraph">...</div>
  <section>
    <h2 id="evaluating-messages">1.1.1. Messages You May Meet<span class="permalink-widget inline">...</span></h2>
    ...
  </section>
</section>
```

Use `main section h1` through `main section h4` for the heading tree. `h5`/`h6` do not
occur. Counts across the book: 238 `h2`, 83 `h3`, 5 `h4`.

### 2.1 Headings and numbering

The heading text contains the section number as a plain text node, followed by a
non-breaking space (`U+00A0`, visible as `&#160;` in the source), the title, and a
permalink span. For example:

```html
<h1 id="monads">4. Monads<span class="permalink-widget inline"><a href="find/?domain=Verso.Genre.Manual.section&amp;name=monads" title="Permalink">🔗</a></span></h1>
<h1 id="evaluating">1.1. Evaluating Expressions<span class="permalink-widget inline"><a href="find/?domain=Verso.Genre.Manual.section&amp;name=evaluating" title="Permalink">🔗</a></span></h1>
<h1 id="props-proofs-indexing">Interlude: Propositions, Proofs, and Indexing<span class="permalink-widget inline">...</span></h1>
```

There is no separate `<span class="number">` inside content headings; that class appears
only in the TOC (`span.number`), as in:

```html
<a href="Monads/One-API___-Many-Applications/#monad-api-examples"><span class="number">4.1.</span> One API, Many Applications</a>
```

Unnumbered TOC entries use an empty `<span class="unnumbered"></span>` instead. Heading
numbers are therefore easiest to recover from the TOC (`nav#toc` or
`ol.section-toc`), or by parsing the leading text of the heading. The page `<title>` is
only the title, without the number:

```html
<title>Evaluating Expressions</title>
```

Headings can contain inline markup, including highlighted Lean code:

```html
<h1 id="monad-do-notation">4.4. <code class="hl lean inline" data-lean-context="examples"><span class="keyword token" data-binding="">do</span></code>-Notation for Monads<span class="permalink-widget inline">...</span></h1>
```

So heading extraction must preserve inline children, not just call `get_text()`.

IDs are stable anchor targets. They come either from explicit `tag := "..."` metadata or
from Verso's generated hierarchical slug. Examples of both:

```text
id="monads"                                  explicit tag
id="getting-to-know-types"                   explicit tag
id="Functional-Programming-in-Lean--Introduction"          generated
id="Functional-Programming-in-Lean--Introduction--Release-history--October___-2025"  generated
```

Preserve IDs exactly, including case and underscores; do not re-slug them.

## 3. Prose blocks

Ordinary paragraphs are `<p>`. A Verso paragraph that contains following code or output
is wrapped in a grouping `<div class="paragraph">`; the actual prose remains a `<p>`
inside it:

```html
<div class="paragraph">
  <p>To ask Lean to evaluate an expression, write
    <code class="hl lean inline" data-lean-context="examples">...</code> before it ...
  </p>
  <code class="hl lean block" data-lean-context="examples">...</code>
  <pre class="hl lean lean-output information">...</pre>
</div>
```

`div.paragraph` is a layout grouping, not a semantic paragraph. There are 221 of them.
There are also `<p>` elements that are direct children of sections. For conversion,
traverse blocks in document order and treat `div.paragraph` as transparent.

Other prose elements:

- Emphasis: `<em>...</em>` (319 occurrences).
- Unordered lists: `<ul><li>...</li></ul>`; ordered lists: `<ol><li>...</li></ol>`.
- Page/section contents list: `<ol class="section-toc">`, with each `<li>` containing a
  link and either `<span class="number">` or `<span class="unnumbered">`. Nine pages use
  it: the root index and the eight chapter pages whose sections are split into pages.
- Technical terms:
  - definition: `<span class="def-technical-term" id="--tech-term-string-slices"><em>string slices</em></span>`
  - reference: `<a class="technical-term" href="Getting-to-Know-Lean/Characters___-Strings___-and-Slices/#--tech-term-string-slices">string slices</a>`
- Blockquote (only one in the book):

```html
<blockquote><p>Programs must be written for people to read, and only incidentally for machines to execute.</p></blockquote>
```

There is no attribution/citation element inside it.

## 4. Lean code

### 4.1 Input code blocks

Lean input is **not** `pre > code`. It is a block-level `<code>` element:

```html
<code class="hl lean block" data-lean-context="examples">
  <span class="keyword token" data-binding="kw-occ-Lean.Parser.Command.classTk-416">class</span>
  <span class="inter-text"> </span>
  <span class="const token" data-binding="const-Class.Monad" data-verso-hover="864">Monad</span>
  ...
</code>
```

- Classes are exactly `hl lean block`.
- Every Lean code element in this book has `data-lean-context="examples"` (6222
  occurrences across input and inline code).
- Newlines and indentation are literal text inside `span.inter-text` children. For
  example, `block.get_text()` for a class declaration begins
  `'class Monad (m : Type → Type) where\npure : α → m α\nbind : ...'`.
- `code.hl.lean.block` is styled `display:block; white-space:pre`, so it looks like a
  `<pre>` block.
- Tokens may be wrapped in `<a>` elements (Lean reference docs or internal definition
  links); the token span itself is always inside the anchor.
- Some tokens carry `id` attributes that are cross-reference targets, e.g.
  `<span class="const token" ... id="Validate___ok">ok</span>`.
- Hidden hover content may be present inside a token wrapper. See 4.5.

Inline Lean code uses the same markup with `inline` instead of `block`:

```html
<code class="hl lean inline" data-lean-context="examples"><span class="keyword token" data-binding="">do</span></code>
```

There are 1270 block input elements and 4952 inline highlighted Lean elements.

### 4.2 Syntax-highlight token classes

A token always has the `token` class plus one or more category classes. Class order in
the HTML is not significant; test membership in the class set. Whitespace between
tokens is a `<span class="inter-text">` (42658 occurrences) and is **not** a token.

| Class set (examples) | Token kind | Example text |
|---|---|---|
| `keyword token` | Lean keyword / command keyword | `class`, `def`, `if`, `then`, `else`, `by`, `fun`, `instance`, `abbrev`, `structure`, `import` |
| `const token` | constant, definition, constructor, or identifier | `Monad`, `String.append`, `Validate`, `Nat`, `Option`, `pure`, `bind` |
| `var token` | variable / binder | `m`, `α`, `x`, `s` |
| `sort token` | sort/type keyword | `Type`, `Prop` |
| `literal number token` | numeric literal | `1`, `999` |
| `literal string token` | string literal | `"Hello, Lean!"`, `"FIRM"` |
| `literal string interpolation token` | interpolation piece of a string | `"Must be no later than {` |
| `literal char token` | character literal | `'!'` |
| `punctuation bracket token` | brackets | `(`, `)`, `{`, `}`, `[`, `]` |
| `punctuation operator token` | operators | `+`, `*`, `→`, `>>=`, `//` |
| `punctuation separator token` | separators | `,` |
| `built-in delim token` | built-in delimiter | `:=`, `:` |
| `unknown token` | unclassified token / fallback | `<$>`, `→`, `sorry` |
| `wildcard token` | wildcard | `_` |
| `anon-ctor const token` | anonymous constructor | `⟨` |
| `module-name token` | module name | `Greeting` |
| `comment delimiter token` | comment delimiter | `--` |
| `comment line token` | comment text | ` This version uses ...` |
| `level-var token` | universe-level variable | `u` |
| `level-const token` | universe-level constant | `1` |
| `level-op token` | universe-level operator | `max`, `imax` |

The generated CSS gives some classes default styling: keywords are bold, variables are
italic, and literals/unknown/punctuation/delimiters are normal weight. Colors are
controlled by CSS variables and are mostly inherited/currentColor in this output. For
Typst conversion, class membership is more useful than color: map `keyword` to bold,
`var` to italic (if desired), and otherwise preserve monospace text. Do not drop
`inter-text`; it carries the spaces and newlines that make the code readable.

Counts of the common token classes across the book (order-independent combinations):

```text
const token                       22098
var token                         16019
bracket punctuation token          6361
built-in delim token               6151
unknown token                      5971
keyword token                      4388
operator punctuation token         2460
literal number token               1396
sort token                          893
punctuation separator token         813
literal string token                781
anon-ctor const token               210
wildcard token                      199
level-var token                     170
literal string interpolation token  101
level-const token                    56
level-op token                       30
literal char token                   13
comment delimiter token               9
comment line token                    9
module-name token                     1
```

### 4.3 Lean output, information, error, and warning blocks

Visible Lean messages are `<pre>` blocks with `hl lean lean-output` plus a severity
class. Severity is on the `<pre>`, not on the inner message:

Information/output:

```html
<pre class="hl lean lean-output information"><span class="verso-message"><span class="text"></span><span class="text">3</span></span></pre>
```

Error:

```html
<pre class="hl lean lean-output error"><span class="verso-message"><span class="text"></span><span class="text">don't know how to synthesize placeholder</span><span class="text">
</span><span class="text">context:</span>...<span class="goal">...</span></span></pre>
```

Warning:

```html
<pre class="hl lean lean-output warning"><span class="verso-message"><span class="text"></span><span class="text">declaration uses `</span><span class="highlighted"><span class="unknown token" data-binding="">sorry</span></span><span class="text">`</span></span></pre>
```

Message contents are built from:

- `<span class="text">` for literal message text (including newlines),
- `<span class="highlighted">` around pretty-printed Lean terms, which contain the same
  syntax token spans as input code,
- `<span class="verso-message">` as the outer message wrapper.

Counts: 191 `information`, 194 `error`, and 4 `warning` visible output blocks.

There is no `pre.lean-output.success` or plain-output variant in this book. The classification
is always one of `information`, `warning`, `error`.

### 4.4 Proof-state markup inside messages

Error messages and some outputs contain structured proof states. These are not syntax
tokens; they are formatting spans that a converter should use to reconstruct lines:

```html
<span class="goal">
  <span class="hypotheses">
    <span class="hypothesis">
      <span class="name"><span class="var token">β</span> <span class="var token">α</span></span>
      <span class="colon">:</span>
      <span class="type"><span class="sort token">Type</span></span>
    </span>
    ...
  </span>
  <span class="conclusion">
    <span class="prefix">⊢ </span>
    <span class="type">Pair α β</span>
  </span>
</span>
```

Relevant classes:

- `goal`, `hypotheses`, `hypothesis`, `name`, `colon`, `type`
- `conclusion`, `prefix` (the `⊢ ` prefix)
- `labeled-case`, `case-label`, `goal-name` for named cases
- `tactic`, `tactic-state` for proof states attached to `by`

For print, render hypotheses as separate lines, the colon as the separator, and the
conclusion after a `⊢` prefix. The HTML currently relies on CSS for layout (see 4.6).

### 4.5 Hidden hover tooltips and docstrings

There are two independent hover mechanisms, both HTML/JS-only:

1. **Inline message tooltips** for tokens with Lean feedback:

```html
<span class="has-info information" data-verso-hover="7">
  <span class="hover-container">
    <span class="hover-info messages">
      <code class="verso-message information">
        <span class="text"></span><span class="text">Validate.ok { name := "David", birthYear := 1984 }</span>
      </code>
    </span>
  </span>
  <a href="https://lean-lang.org/doc/reference/4.33.0/Interacting-with-Lean/#Lean___Parser___Command___eval" ...>
    <span class="keyword token" data-binding="...">#eval</span>
  </a>
</span>
```

The visible severity is on `span.has-info` (`information`, `warning`, or `error`) and
the message severity is repeated on `code.verso-message`. The `.hover-info` content is
hidden until hover by CSS/JS. It may duplicate a visible `pre.lean-output` block. A naive
`get_text()` on a code block includes this hidden text, which corrupts the code; strip
`.hover-info` (or at least do not use descendants of it for visible code text).

2. **Documentation hover for identifiers** with no inline message text. A token can have
just `data-verso-hover="864"`; the tooltip HTML lives in `-verso-docs.json` under the
numeric key `"864"`. Example value:

```html
<code>Monad {α β : Type} (m : Type → Type) : Type</code>
```

Those docs are also HTML-only and are not needed for a static print conversion.

### 4.6 Proof-state toggles and case labels

Some `by` tokens are interactive. The pattern is:

```html
<span class="tactic">
  <label for="tactic-state-..."><span class="keyword token">by</span></label>
  <input class="tactic-toggle" id="tactic-state-..." type="checkbox"/>
  <span class="tactic-state">
    <span class="goal">...</span>
  </span>
</span>
```

Named cases use:

```html
<span class="labeled-case">
  <label class="case-label">
    <input checked="checked" id="--verso-unique-256" type="checkbox"/>
    <span class="goal-name" for="--verso-unique-256">zero</span>
  </label>
  <span class="conclusion">...</span>
</span>
```

The checkbox/label controls are interactive; `.tactic-state` and collapsed case bodies
are hidden until checked. The DOM contains the full proof state. For print, either
expand them or drop them deliberately; do not let `get_text()` pull them into the
surrounding code without handling the controls.

### 4.7 Evaluation and equational-reasoning steps

`div.eval-steps` contains a sequence of Lean input blocks:

```html
<div class="eval-steps">
  <code class="hl lean block" data-lean-context="examples">id &lt;$&gt; Pair.mk x y</code>
  <code class="hl lean block" data-lean-context="examples">Pair.mk x ( id y )</code>
  <code class="hl lean block" data-lean-context="examples">Pair.mk x y</code>
</div>
```

The downward arrow is a CSS pseudo-element, not text in the HTML:

```css
.eval-steps .hl.lean.block:not(:last-child)::after {
  content: "⟹";
  display: block;
  ...
}
```

`div.eq-steps` contains alternating code blocks and `<div class="reason">` blocks:

```html
<div class="eq-steps">
  <code class="hl lean block" data-lean-context="examples">pure id &gt;&gt;= ...</code>
  <div class="reason"><p>pure is a left identity of &gt;&gt;=</p></div>
  <code class="hl lean block" data-lean-context="examples">...</code>
  ...
</div>
```

The `={ ... }=` braces around reasons are also CSS pseudo-elements (`content: "={"` and
`content: "}="`). A text-only extraction loses both the eval arrows and the eq-reason
braces; add them explicitly for print. There are 32 `eval-steps` and 5 `eq-steps`
blocks.

### 4.8 Example files, shell commands, and REPL interactions

These are typed `<div>`/`<code>` structures, not `<pre>` blocks and not JavaScript
widgets, but they need block-aware handling because their line breaks are implied by CSS
`display: block` rather than by newline text.

Example source file (12 occurrences):

```html
<div class="example-file">File: <code>Greeting/Basic.lean</code><code class="line">def hello := "world"</code></div>
```

Each source line is a separate `<code class="line">` with no newline text between them.
CSS counters add line numbers (`::before { content: counter(linenumber) }`); those numbers
are not in the HTML text. A converter must insert a newline per `.line` and optionally
synthesize line numbers.

Shell command block (5 occurrences):

```html
<div class="shell-command block">
  <code class="command"><code class="prompt">$ </code>lean --run Hello.lean</code>
</div>
```

Command transcript (6 occurrences):

```html
<div class="shell-commands">
  <code class="command">countdown</code>
  <code class="output">5
4
...
</code>
</div>
```

The `$ ` prompt for `.shell-commands .command` and `span.shell-command.inline` is added
by CSS `::before`; it is not in the text. (`div.shell-command.block` includes an explicit
`<code class="prompt">$ </code>`.)

REPL interaction (5 occurrences):

```html
<div class="interaction">
  <code class="output">How would you like to be addressed?
</code>
  <code class="input">David
</code>
  <code class="output">Hello, David!
</code>
</div>
```

`.interaction > *` is `display: inline`; the code elements are inline chunks of a terminal
transcript. `.input` is styled bold/blue and `.output` normal. Inline shell commands use
`<span class="shell-command inline"><code class="command">lean --run HelloName.lean</code></span>`.

### 4.9 Plain `<pre>` and plain `<code>`

Not all code is Lean-highlighted:

- Plain inline `<code>`: 605 occurrences. Used for non-Lean identifiers, filenames,
  option names, plain technical text, etc. Example: `<code>Hello, world!</code>`.
- Plain `<pre>`: 12 occurrences. Used for other-language source code (Java, C#, Python,
  Racket) and program output, with no CSS class. Example:

```html
<pre>abstract class Bool {}
class True : Bool {}
class False : Bool {}
</pre>
```

These have no syntax highlighting and no token spans.

## 5. Links and cross-references

### 5.1 Internal links

Internal links are root-relative directory URLs with a fragment, resolved through
`<base>`:

```html
<a href="Monads/Example___-Arithmetic-in-Monads/#nondeterministic-search">evaluating arithmetic expressions in a variety of monads</a>
<a href="Overloading-and-Type-Classes/Arrays-and-Indexing/#overloading-indexing">parameter to <code class="hl lean inline" ...>GetElem</code></a>
```

- No `.html` suffix.
- A trailing `/` before the fragment denotes the page directory.
- The fragment targets a heading `id` or a code-token `id`.
- Some internal links are wrapped around code tokens and carry a title:

```html
<a href="Functors___-Applicative-Functors___-and-Monads/Applicative-Functors/#Validate___ok" title="Definition of example">
  <span class="const token" data-binding="const-Validate.ok" data-verso-hover="1142">ok</span>
</a>
```

- Heading IDs and code-definition IDs are unique within each page (verified: zero
  duplicate IDs across all pages).
- All 4595 internal `href`s (including fragments) resolve to an existing page and an
  existing `id` in this build.

### 5.2 External links

External links are ordinary absolute URLs with no special classes:

```html
<a href="https://lean-lang.org/doc/reference/4.33.0/Functors___-Monads-and--do--Notation/#Monad___mk"
   title="Documentation for Monad in Lean Language Reference">...</a>
<a href="https://lean-fro.org">Lean FRO</a>
<a href="http://creativecommons.org/licenses/by/4.0/" rel="license"><img .../></a>
```

In code, documentation links are wrapped around tokens and use
`title="Documentation for <name> in Lean Language Reference"`. They are external links,
not internal cross-references, and can be stripped or converted to plain code for print.
The reference version is `4.33.0` (the examples toolchain version), even though the book
itself is built with `4.36.0-rc2`.

### 5.3 Permalinks and the `find/` redirect

Every heading has a permalink widget:

```html
<span class="permalink-widget inline">
  <a href="find/?domain=Verso.Genre.Manual.section&amp;name=monads" title="Permalink">🔗</a>
</span>
```

`find/index.html` is a JavaScript redirect page using `xref.json`; the permalink is not a
direct page URL. For print, drop the `🔗` widget and use the heading `id` as the label
instead.

### 5.4 Previous/next navigation

Each page has two identical `<nav class="prev-next-buttons">` blocks. They use:

```html
<a class="local-button active" href="Overloading-and-Type-Classes/Summary/#type-classes-summary"
   rel="prev" title="3.8. Summary">
  <span class="arrow">←</span><span class="where">3.8. Summary</span>
</a>
```

`rel="prev"`/`rel="next"` and `title` give the target title. Ignore these for content;
they are redundant with the TOC.

## 6. Tables

There are two kinds of `<table>` in the output.

### 6.1 Navigation tables (the vast majority)

There are 190 navigation tables inside `nav#toc`. They have no class and use row/cell
classes:

```html
<table>
  <tr class="numbered">
    <td class="num">1.</td>
    <td><a href="Getting-to-Know-Lean/#getting-to-know">Getting to Know Lean</a></td>
  </tr>
  <tr class="current numbered">...</tr>
  <tr class="unnumbered">...</tr>
</table>
```

These are sidebar TOC data, not book content. Ignore them when converting `main`.

### 6.2 Content tables

Six tables are actual book content. They use `class="tabular"` and contain `<thead>`,
`<th>`, and `<td>` elements. Cells contain `<p>` wrappers:

```html
<table class="tabular">
  <thead>
    <tr><th><p>Connective</p></th><th><p>Lean Syntax</p></th><th><p>Evidence</p></th></tr>
  </thead>
  <tr>
    <td><p>True</p></td>
    <td><p><code class="hl lean inline" ...>...</code></p></td>
    <td><p>...</p></td>
  </tr>
</table>
```

There are no `<caption>` elements, no cell classes, and no alignment classes in the
generated content tables. Table cells can contain inline code, math, and links; traverse
them normally.

## 7. Math

Math is raw TeX inside `<code>` elements, rendered in the browser by KaTeX:

Inline:

```html
<code class="math inline">15 - 6</code>
```

Display:

```html
<code class="math display">
     λ e .
     \begin{cases}
     h(f(e), g(e)) &amp; \mathrm{if}\ e\ \mathrm{contains}\ (\mathrm{OP}, h) \\
     0 &amp; \mathrm{otherwise}
     \end{cases}
   </code>
```

There are 127 `code.math.inline` and 5 `code.math.display` elements. The static HTML
contains **no server-rendered `.katex` spans and no MathML**. At runtime, the page loads:

```html
<script defer="defer" src="-verso-data/katex/katex.js"></script>
<script defer="defer" src="-verso-data/katex/math.js"></script>
<link rel="stylesheet" href="-verso-data/katex/katex.css"/>
```

and `math.js` does:

```js
for (const m of root.querySelectorAll(".math.inline")) {
    katex.render(m.textContent, m, { throwOnError: false, displayMode: false });
}
for (const m of root.querySelectorAll(".math.display")) {
    katex.render(m.textContent, m, { throwOnError: false, displayMode: true });
}
```

So a print pipeline must read the TeX from `textContent` (after HTML entity decoding)
and convert it itself; it cannot rely on rendered math in the files. Math is never an
image. Display math is still inside a paragraph-level `<code>` element, with literal
newlines and indentation in its text.

## 8. Figures and images

There are no `<figure>`, `<figcaption>`, or `<svg>` elements in the book content, and no
diagrams. Across 73 pages there are 74 `<img>` elements:

- 73 copies of the site logo:
  `<img src="static/lean_logo.svg"/>`, inside `header .header-logo-wrapper a#logo`.
- 1 Creative Commons badge on the `Introduction` page:
  `<img alt="Creative Commons License" src="https://i.creativecommons.org/l/by/4.0/88x31.png" style="border-width:0"/>`,
  inside `<a href="http://creativecommons.org/licenses/by/4.0/" rel="license">`.

A print conversion therefore needs no figure/asset layout machinery for this book, but
should keep the logo/CC badge handling separate from content.

## 9. Footnotes and index entries

Neither feature is used in this book:

- No `<sup>` elements.
- No elements with `footnote` in a class, id, or href.
- No alphabetical index page and no index-entry markup. Occurrences of the word "index"
  are chapter titles/paths such as `Indexing` and `#overloading-indexing`.

A converter can omit both features for the current build.

## 10. Static assets, CSS, and fonts

### 10.1 Active stylesheets and scripts

The page shell links:

```html
<link rel="stylesheet" href="book.css"/>
<link rel="stylesheet" href="verso-vars.css"/>
<link rel="stylesheet" href="-verso-search/search-box.css"/>
...
<link rel="stylesheet" href="-verso-data/tippy-border.css"/>
<link rel="stylesheet" href="-verso-data/katex/katex.css"/>
```

`book.css` (about 24 KB) contains the generated layout and `.hl.lean`/`.lean-output`
styles. `verso-vars.css` (about 5 KB) defines CSS variables and defaults, including
Helvetica-family text and monospace code.

The pages also contain many inline `<style>` blocks with the bulk of the Lean-code
highlighting and manual-specific CSS, and inline `<script>` blocks for canonical URL
redirects, trailing-slash redirects, TOC width persistence, hover/tactic handling, and
Plausible analytics. These are duplicated on every page.

### 10.2 Extra `static/` assets

`static/` is copied from `book/static/`:

```text
static/lean_logo.svg
static/theme.css
static/fonts/noto-sans-mono/
static/fonts/source-code-pro/
static/fonts/source-sans/
static/fonts/source-serif/
```

`static/lean_logo.svg` is used by every page. `static/theme.css` contains the intended
Source Sans 3 / Source Code Pro font-family variables and manual-specific rules.

**Important CSS quirk:** the configured `extraCss` paths are emitted as literal text in
`<style>` elements, not as stylesheet links or inlined CSS. The generated pages contain:

```html
<style>/static/theme.css</style>
<style>/static/fonts/source-code-pro/source-code-pro.css</style>
<style>/static/fonts/source-serif/source-serif-text.css</style>
<style>/static/fonts/source-sans/source-sans-3.css</style>
<style>/static/fonts/noto-sans-mono/noto-sans-mono.css</style>
```

Their text content is just the path string, so these rules are **not applied**. There is
no `@font-face` rule in `book.css`, and the active font variables remain the defaults in
`verso-vars.css` (Helvetica/Arial/monospace). The font files and their CSS are still
present in `static/` and can be linked explicitly by a later Typst/print pipeline if the
intended typography is wanted.

### 10.3 Font inventory

Under `static/fonts/`, counting by final filename suffix:

| Family | TTF | OTF | WOFF | WOFF2 |
|---|---:|---:|---:|---:|
| `source-serif` | 12 | 12 | 24 | 24 |
| `source-sans` | 16 | 16 | 32 | 32 |
| `source-code-pro` | 14 | 14 | 28 | 32 |
| `noto-sans-mono` | 1 | 0 | 0 | 0 |
| **static total** | **43** | **42** | **84** | **88** |

The `source-*` directories also contain subdirectories `TTF/`, `OTF/`, `WOFF/`, and
`WOFF2/`, plus variable-font files such as
`source-sans/VF/SourceSans3VF-Upright.ttf`. The `.css` files use the formats in this
order: WOFF2, WOFF, OTF, TTF. Examples:

```css
src: url('./WOFF2/TTF/SourceSerif4-ExtraLight.ttf.woff2') format('woff2'),
     url('./WOFF/OTF/SourceSerif4-ExtraLight.otf.woff') format('woff'),
     url('./OTF/SourceSerif4-ExtraLight.otf') format('opentype'),
     url('./TTF/SourceSerif4-ExtraLight.ttf') format('truetype');
```

`noto-sans-mono` has one variable TTF:
`static/fonts/noto-sans-mono/NotoSansMono-VariableFont_wdth,wght.ttf`.

KaTeX has a separate font set under `-verso-data/katex/fonts/`: 20 TTF, 20 WOFF, and 20
WOFF2 files (60 total; no OTF), referenced by `-verso-data/katex/katex.css`.

The site-wide font assets are therefore available in all four formats (TTF, OTF, WOFF,
WOFF2), but only the KaTeX fonts are actually referenced by active CSS in the current
build.

### 10.4 Other static data

- `-verso-search/` contains `elasticlunr.min.js`, `fuzzysort.min.js`, search CSS, search
  page code, `searchIndex.js` (about 3.4 MB), and many `searchIndex_<n>.<hash>.js`
  shards. It is only for the search UI.
- `-verso-data/` contains KaTeX (`katex.js`, `math.js`, `katex.css`, `fonts/`) and
  Tippy/Popper (`popper.min.js`, `tippy-bundle.umd.min.js`, `tippy-border.css`).
- `-verso-docs.json` maps numeric hover IDs to HTML doc snippets.
- `xref.json` (about 3 MB) is the cross-reference database used by `find/index.html`.

## 11. HTML-only content and print handling

| Feature | Markup / mechanism | Print recommendation |
|---|---|---|
| KaTeX math | `code.math.inline` / `code.math.display` with raw TeX; `math.js` renders on `DOMContentLoaded` | Read TeX and convert to native math; do not expect `.katex` in the files |
| Inline Lean message tooltips | `span.has-info.{information,warning,error}`, `span.hover-info.messages`, `code.verso-message` | Strip `.hover-info` from visible code; use visible `pre.lean-output` blocks for messages |
| Docstring tooltips | `data-verso-hover="<n>"` + `-verso-docs.json` | Ignore for print |
| Proof-state toggles | `span.tactic`, `input.tactic-toggle`, `span.tactic-state`, `label.case-label`, `span.labeled-case` | Hidden by default; expand or drop deliberately. Controls themselves are not content |
| Eval-step arrows | `div.eval-steps`; CSS `::after { content: "⟹" }` | Insert `⟹` between blocks explicitly |
| Eq-step reason braces | `div.eq-steps`, `div.reason`; CSS `::before`/`::after` `{` `}=` | Insert `={ ... }=` explicitly |
| Example-file line numbers | `div.example-file > code.line`; CSS counter | Add newlines per `.line` and optionally line numbers |
| Shell prompts | `.command::before { content: "$ " }`; block form has explicit `<code class="prompt">$ </code>` | Insert `$ ` explicitly for inline/transcript commands |
| REPL chunks | `div.interaction` with `code.output`/`code.input`, inline display | Treat as sequential terminal transcript lines |
| Search UI | `search/`, `-verso-search/`, search scripts | Omit entirely |
| Permalinks / find redirect | `span.permalink-widget`, `find/?domain=...&name=...`, `xref.json` | Omit; use heading IDs as labels |
| Canonical/trailing-slash redirects | inline `<script>` at start of `<head>` | Omit |
| Analytics | Plausible `<script>` | Omit |
| TOC resizing/burger | `toc-resize.js`, `input#toggle-toc`, `label#toggle-toc-click`, `span.line.line1/2/3` | Omit |
| Sidebar/prev-next | `nav#toc`, `div.last`, `nav.prev-next-buttons` | Omit from content; use TOC/heading tree for order |
| Duplicated shell assets | every page repeats the same header, sidebar, CSS, and JS | Extract content once per page; do not concatenate page shells |

The canonical/trailing-slash scripts and the search assets mean the site is not fully
functional when opened as bare `file://` URLs without JS, but the book text and visible
Lean output blocks are present in the static HTML.

## 12. Recommended extraction order for HTML -> Typst

1. Determine the page depth from the path, read `<base href>`, and resolve every
   `href` against it. Append `index.html` for directory paths when reading local files.
2. Select `main > div.content-wrapper > section` as the content root. Ignore
   `header`, `label#toggle-toc-click`, `nav#toc`, `div.toc-backdrop`,
   `div.toc-resize-handle`, both `nav.prev-next-buttons`, and `div.last`.
3. Walk the section tree in document order. For each `h1`-`h4`, strip
   `span.permalink-widget`, preserve inline children (including `code.hl.lean.inline`),
   and use the heading `id` as the label. Derive hierarchy from heading level plus page
   type, or reconstruct it from `nav#toc`/`ol.section-toc`.
4. Handle block elements in this priority order:
   - `div.eval-steps` and `div.eq-steps` before their child code blocks;
   - `div.example-file` before its `code.line` children;
   - `div.shell-command`, `div.shell-commands`, `div.interaction` before their
     `code.command`/`prompt`/`input`/`output` children;
   - `pre.hl.lean.lean-output` as a visible message block;
   - `code.hl.lean.block` as Lean input;
   - `code.math.display` / `code.math.inline`;
   - `table.tabular`;
   - `blockquote`;
   - plain `pre` and plain `code`;
   - otherwise `<p>`, lists, and inline content.
5. For code text, remove `.hover-info`, `input`, and control labels from consideration;
   preserve `span.inter-text` whitespace/newlines. For code tokens, use the class set to
   decide bold/italic/normal, but keep the text exactly.
6. For messages, use `pre.lean-output.{information,warning,error}` and its
   `span.verso-message` structure. Reconstruct proof-state lines from `goal`,
   `hypotheses`, `hypothesis`, `name`, `colon`, `type`, `conclusion`, `prefix`.
7. Resolve internal links to labels by page path + fragment; drop external docs links or
   keep them as URL footnotes; drop `find/` permalinks.
8. Do not emit `search/`, `find/`, `-verso-data/`, `-verso-search/`, `xref.json`,
   `-verso-docs.json`, `toc-resize.js`, or the page shell.

## 13. Build provenance and verification

- Output: `book/_out/html-multi/`, 73 `index.html` pages (71 book pages + `search` and
  `find` utility pages).
- Build command: `cd book && lake exe fp-lean --depth 2 --without-html-single --verbose`.
- Examples build: 82 jobs + 30 jobs, about 145 s.
- Book build: 965 Lean jobs plus HTML generation, about 540 s total.
- Toolchains: book `leanprover/lean4:v4.36.0-rc2`; examples
  `leanprover/lean4:4.33.0`.
- Logs: `typst/build-examples.log`, `typst/build-book.log`.
- NixOS deviations from CI: used `nix shell nixpkgs#gcc nixpkgs#gnumake nixpkgs#pkg-config`
  to provide `cc`/`make`; used the system Python 3.14.10 rather than CI's pinned 3.15.0;
  installed elan under `~/.elan` with its official installer. No tracked repository
  source files were changed.
- Verification performed on the generated output:
  - `index.html` and all chapter/section pages exist.
  - 73 `index.html` pages total.
  - 4,595 internal hrefs checked, 0 missing pages/anchors.
  - Zero duplicate element ids on any page.
  - Feature counts above (code blocks, messages, tokens, tables, math, images) were
    collected from all 73 pages.
