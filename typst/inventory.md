# Typst Book Production Inventory

Repository: `fp-lean` (Functional Programming in Lean)
Date: 2026-11-24

## 1. Tooling

| Tool | Status | Version / path |
| --- | --- | --- |
| `typst` | not installed globally; available through Nix | `typst 0.15.1 (9dfd3a08)` via `nix run nixpkgs#typst --` |
| `python3` | installed | 3.14.10 (`/etc/profiles/per-user/nil/bin/python3`) |
| `pandoc` | absent | — |
| `uv` | absent | — |

NixOS convention: no global installs. All Typst builds in this directory use
`nix run nixpkgs#typst -- compile ...` and the bundled fonts:

```
# from the repository root
nix run nixpkgs#typst -- compile --root .. --font-path book/static/fonts \
    typst/preview.typ typst/preview.pdf
```

Typst 0.15.1 supports SVG images natively (verified with `book/static/lean_logo.svg`),
TTF/OTF fonts, and outline-entry `fill()` for dotted leaders.

## 2. Fonts

`book/static/fonts/` contains four families, each shipped as **TTF, OTF, WOFF and WOFF2**.
Typst loads the TTF/OTF files; WOFF/WOFF2 are web formats and are not used.

| Family | Directory | Usable files | Typst family name |
| --- | --- | --- | --- |
| Source Serif 4 | `book/static/fonts/source-serif/TTF` (also `OTF/`) | `SourceSerif4-{Regular,It,Bold,Semibold,Light,…}.ttf` | `Source Serif 4` |
| Source Sans 3 | `book/static/fonts/source-sans/TTF` (variable `VF/`) | `SourceSans3-{Regular,It,Bold,Semibold,Medium,…}.ttf` | `Source Sans 3` |
| Source Code Pro | `book/static/fonts/source-code-pro/TTF` | `SourceCodePro-{Regular,It,Bold,Semibold,…}.ttf` | `Source Code Pro` |
| Noto Sans Mono | `book/static/fonts/noto-sans-mono` | `NotoSansMono-VariableFont_wdth,wght.ttf` | `Noto Sans Mono` |

Verification: `nix run nixpkgs#typst -- fonts --font-path book/static/fonts` lists
`Source Serif 4`, `Source Sans 3`, `Source Code Pro`, `Noto Sans Mono` (plus system fonts).
All required faces exist as first-class TTF/OTF; no conversion or nixpkgs font package needed.
Exact paths used by the template's recommended build command:

- `book/static/fonts/source-serif/TTF/SourceSerif4-Regular.ttf`
- `book/static/fonts/source-serif/TTF/SourceSerif4-It.ttf`
- `book/static/fonts/source-sans/TTF/SourceSans3-Regular.ttf`
- `book/static/fonts/source-code-pro/TTF/SourceCodePro-Regular.ttf`

## 3. Content inventory

### 3.1 Chapter list and order (`book/FPLean.lean` includes)

| # | Source | Title | Numbered |
| --- | --- | --- | --- |
| — | `FPLean/Intro.lean` | Introduction | no (`number := false`, `htmlSplit := .never`) |
| — | `FPLean/Acks.lean` | Acknowledgments | no |
| 1 | `FPLean/GettingToKnow.lean` | Getting to Know Lean | yes |
| 2 | `FPLean/HelloWorld.lean` | Hello, World! | yes |
| — | `FPLean/PropsProofsIndexing.lean` | Interlude: Propositions, Proofs, and Indexing | no |
| 3 | `FPLean/TypeClasses.lean` | Overloading and Type Classes | yes |
| 4 | `FPLean/Monads.lean` | Monads | yes |
| 5 | `FPLean/FunctorApplicativeMonad.lean` | Functors, Applicative Functors, and Monads | yes |
| 6 | `FPLean/MonadTransformers.lean` | Monad Transformers | yes |
| 7 | `FPLean/DependentTypes.lean` | Programming with Dependent Types | yes |
| — | `FPLean/TacticsInductionProofs.lean` | Interlude: Tactics, Induction, and Proofs | no |
| 8 | `FPLean/ProgramsProofs.lean` | Programming, Proving, and Performance | yes |
| 9 | `FPLean/NextSteps.lean` | Next Steps | yes |

`FPLean/Examples.lean`, `FPLean/Meta.lean` and `FPLean/Basic.lean` are support modules
(role expanders, example harness), not book chapters. Front-matter chapters and the two
interludes do not consume chapter numbers.

Per-chapter size (words in sources, all fenced blocks):

| Chapter | Files | Words | Fences |
| --- | ---: | ---: | ---: |
| Intro | 1 | 1 629 | 10 |
| Acks | 1 | 354 | 0 |
| GettingToKnow | 9 | 20 319 | 558 |
| HelloWorld | 6 | 9 194 | 130 |
| PropsProofsIndexing | 1 | 3 172 | 68 |
| TypeClasses | 8 | 16 922 | 386 |
| Monads | 6 | 11 613 | 308 |
| FunctorApplicativeMonad | 8 | 14 622 | 296 |
| MonadTransformers | 6 | 15 897 | 334 |
| DependentTypes | 6 | 19 554 | 384 |
| TacticsInductionProofs | 1 | 3 657 | 74 |
| ProgramsProofs | 8 | 21 819 | 448 |
| NextSteps | 1 | 463 | 0 |

Total ≈ 137 000 words (~380–450 book pages at 11 pt).

### 3.2 Fenced code blocks (whole book)

| Fence kind | Count | Meaning |
| --- | ---: | --- |
| plain ``` | 1 555 | Lean input, no anchor |
| `anchor` | 1 027 | anchored Lean input (referenced from prose) |
| `anchorError` | 194 | Lean error output |
| `anchorInfo` | 191 | Lean info/output |
| `anchorTerm` | 45 | anchored term / example |
| `anchorEvalSteps` | 32 | multi-step evaluation output |
| `module` | 11 | module declaration |
| `file` | 8 | file content |
| `commands` | 7 | command transcript |
| `anchorEqSteps` | 5 | equality-step transcript |
| `anchorEvalStep` | 5 | single evaluation step |
| `interaction` | 5 | REPL/transcript |
| `plainFile` | 4 | plain file |
| `anchorWarning` | 4 | Lean warning output |
| `command`, `commandOut` | 3 each | command and its output |
| `CSharp` | 2 | C# sample |
| `includePython` | 2 | Python sample |
| `fsharp`, `fsharpError` | 1 each | F# sample / error |
| `typescript` | 1 | TypeScript sample |

Mapping for Typst: everything except `*Error`, `*Warning`, `*Info`, `*Steps`, `*Out`
is Lean input; transcript/output kinds map to `lean-output`; errors to `lean-error`;
warnings to `lean-warning`.

### 3.3 Inline roles (prose only, fenced code excluded)

| Role | Uses | Example |
| --- | ---: | --- |
| `{lit}` | 477 | `{lit}`Vect α 0`` — literal/term |
| `{kw}` | 472 | `{kw}`#print`` — keyword/command |
| `{moduleName}` | 199 | `{moduleName}`List`` |
| `{moduleTerm}` | 89 | `{moduleTerm}`"Hello, world!"`` |
| `{tactic}` | 52 | `{tactic}`decide`` |
| `{CSharp}` | 32 | `{CSharp}`$`` |
| `{deftech}` | 24 | `{deftech}_universes à la Russell_` (definition-like emphasis) |
| `{c}` | 11 | `{c}`if`` |
| `{Kotlin}` | 8 | `{Kotlin}`T??`` |
| `{java}` | 6 | `{java}`byte`` |
| `{python}` | 4 | `{python}`f`-strings` |
| `{typescript}`, `{tech}` | 3 each | `{typescript}`Nat``, `{tech}[string slices]` |
| `{cpp}`, `{command}`, `{commandLine}`, `{commandOut}` | 2–5 | shell/command snippets |
| `{fsharp}`, `{rust}`, `{creativeCommons}`, `{versionString}` | 1 each | license badge, Lean version |

Cross-references: `{ref "tag"}[link text]` — 67 occurrences. Anchors: `{anchorName tag}` /
`{anchorTerm tag}` used as inline anchors.

Block kinds: `:::paragraph` (221, structural wrapper), `:::table +header` (6 real tables;
24 Markdown pipe-tables overall). No admonition blocks, no footnotes.

### 3.4 Mathematics

Math is present and written with Verso's backtick-delimited TeX syntax:

- Inline: `` $`...` `` — 128 occurrences.
- Display: `` $$`...` `` — 5 occurrences (all in `DependentTypes/UniversePattern.lean`).
- Example inline: ``$`\{ x, y \}` ``; display:
  ``$$`\left| \left( \left( \mathtt{Bool} \times \mathtt{Bool} \right) \rightarrow \mathtt{Bool} \right) \rightarrow \mathtt{Bool} \right|` ``.
- Also `\begin{cases}` inside a display block (`Monads/Arithmetic.lean`).

Consequence: the Typst template must ship a math sample and a math font fallback;
Typst's native math is a good match for this lightweight notation.

### 3.5 Images and figures

- No figures or content images are referenced by the text.
- Only asset: `book/static/lean_logo.svg` (300×150, monochrome Lean logo) — usable
  directly by Typst 0.15 for the title page.
- The one `<img>` occurrence is the external CC badge embedded in the HTML
  `creativeCommons` block extension (`https://i.creativecommons.org/l/by/4.0/88x31.png`);
  it is not a book figure. The Typst copyright page should typeset the CC BY 4.0 notice
  as text instead.
- No raster assets, no SVG/PNG assets under `book/` or `examples/` referenced by prose.

## 4. Book metadata

- **Title:** Functional Programming in Lean
- **Author:** David Thrane Christiansen
- **Copyright:** Microsoft Corporation 2023 and Lean FRO, LLC 2023–2026
  (`book/FPLean.lean`)
- **License:** Creative Commons Attribution 4.0 International (CC BY 4.0).
  Full legal text: `LICENSE-ASSETS`. In-book notice:
  `book/FPLean/Intro.lean` → `# License` section, which embeds the `creativeCommons`
  block extension and links to the source repository.
- **Lean version:** `examples/lean-toolchain` → `leanprover/lean4:4.33.0`.
  The book prints it through a custom `{versionString}` role that reads that file and
  drops the `leanprover/lean4:` prefix, rendering `4.33.0` as inline code.
- **Source repository:** `https://github.com/leanprover/fp-lean/`

## 5. Production implications

1. Use the bundled TTF/OTF fonts via `--font-path book/static/fonts`; no downloads.
2. 1 555 + 1 027 Lean input blocks dominate the layout — code needs to be compact,
   breakable, and visually calm. Output/error/warning need distinct, print-safe tints.
3. Syntax highlighting cannot come from Verso's HTML spans; a converter must emit
   highlighted token runs to the template helpers (palette defined in `template.typ`).
4. 128 inline math snippets require a math font; Typst's default New Computer Modern
   Math is available and pairs acceptably with Source Serif.
5. No figure pipeline is needed; the title page is the only place for the Lean logo.
6. Cross-references are numerous (67); generated Typst can use native `<label>` /
   `@ref` links, which print as text, not colored URLs.
