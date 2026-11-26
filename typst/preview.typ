// Preview of the print template. Compile with:
//   nix run nixpkgs#typst -- compile --font-path ../book/static/fonts \
//       preview.typ preview.pdf
// All content is representative dummy text exercising every template element.
// Code is passed as fenced raw blocks: #lean-input(```lean ... ```).

#import "template.typ": *

#show: book.with(
  title: "Functional Programming in Lean",
  subtitle: "A free book on using Lean as a programming language",
  author: "David Thrane Christiansen",
  lean-version: "4.33.0",
  logo: "../book/static/lean_logo.svg",
)

#unnumbered[
  = Introduction

  Lean is an interactive theorem prover based on dependent type theory.
  Originally developed at Microsoft Research, development now takes place at
  the #link("https://lean-fro.org")[Lean FRO]. Dependent type theory unites the
  worlds of programs and proofs; thus, Lean is also a programming language.

  This chapter is unnumbered, as are the book's front matter and interludes.
  Section headings inside it inherit the unnumbered style.

  == What Is Lean?

  Lean is a strict, pure functional language with dependent types. Function
  calls evaluate their arguments before the body runs; effects such as
  reading a file or printing to the console are reflected in the type.

  #aside[
    *A note on versions.* All code samples in this preview are tested with
    Lean #text(font: mono, size: 0.9em)[4.33.0].
  ]

  Lean's syntax is close to mathematical notation: `twice` is defined with a
  type annotation, and the identity function is written `fun x => x`. Its
  dependent cousin is `fun (α : Type) (x : α) => x`.
]

= Getting to Know Lean

Lean's most important feature is its treatment of types as first-class values.
This chapter introduces definitions, datatypes, and the interactive evaluator.

== Functions and Definitions

A definition associates a name with a value. In Lean, every definition has a
type, and the type checker verifies that the value inhabits that type before
the definition is accepted.

#lean-input(```lean
def greet (name : String) : String :=
  "Hello, " ++ name ++ "!"
```)

The function `greet` takes a `String` and returns a `String`. Applying it to
a literal is straightforward:

#lean-output(```lean
#eval greet "world"
-- "Hello, world!"
```)

Definitions can be recursive when the recursion is structurally decreasing.
The following function computes the factorial of a natural number:

#lean-input(```lean
def factorial : Nat → Nat
  | 0 => 1
  | n + 1 => (n + 1) * factorial n
```)

#lean-term(```lean
#eval factorial 5
-- 120
```)

=== Pattern Matching

Pattern matching is the primary elimination principle for inductive types.
Each `|` introduces an alternative, and the patterns must cover every case.
The compiler rejects incomplete matches, turning a common source of runtime
errors into a compile-time obligation. This is why `factorial` above can be
trusted: there is no input for which it is undefined.

#lean-input(```lean
inductive Tree (α : Type) where
  | leaf : Tree α
  | node : Tree α → α → Tree α → Tree α
```)

#lean-output(```lean
-- The constructors are Tree.leaf and Tree.node
#check Tree.node
```)

Pre-tokenized highlighting is supported for the converter path: token spans
extracted from Verso's HTML are passed as an array of lines, bypassing the
built-in lexer. This renders nested block comments and doc comments exactly as
classified:

#lean-input((
  (("comment", "/-- The identity function. -/"),),
  (("kw", "def"), ("ws", " "), ("plain", "id"), ("ws", " "), ("punct", "{"),
   ("plain", "α"), ("ws", " "), ("punct", ":"), ("ws", " "), ("type", "Type"),
   ("punct", "}"), ("ws", " "), ("punct", "("), ("plain", "x"), ("ws", " "),
   ("punct", ":"), ("ws", " "), ("plain", "α"), ("punct", ")"), ("ws", " "),
   ("punct", ":"), ("ws", " "), ("plain", "α"), ("ws", " "), ("op", ":=")),
  (("ws", "  "), ("plain", "x")),
  (("comment", "/- A nested block comment:"),),
  (("ws", "   "), ("comment", "/- inner comment -/"),),
  (("ws", "   "), ("comment", "still inside the outer comment -/"),),
))

==== Example Source Files

Example files are introduced with a small filename line and the same input
block treatment:

#lean-file("Greeting/Basic.lean", ```lean
def main : IO Unit :=
  IO.println "Hello, world!"
```)

===== Doc Comments

Doc comments attach to the declaration that follows them. Nested block
comments inside a doc comment are supported by the converter's token spans.

== Errors and Warnings

The elaborator reports errors with source locations and expected types.

#lean-error(```lean
def broken : Nat := "not a number"
-- error: type mismatch
--   "not a number" has type String but is expected to have type Nat
```)

Some problems are recoverable and are reported as warnings instead:

#lean-warning(```lean
def unused (x : Nat) : Nat := 0
-- warning: unused variable `x`
```)

Non-Lean samples can be shown without highlighting by passing `lang`:

#lean-input(```python
def greet(name: str) -> str:
    return f"Hello, {name}!"
```, lang: "python")

== Tables and Figures

Table styling is deliberately quiet: horizontal hairlines, no vertical rules,
and sans-serif column heads.

#figure(
  table(
    columns: (auto, 1fr, auto),
    align: (left, left, right),
    table.header([Name], [Description], [Arity]),
    [map], [Apply a function to every element], [2],
    [filter], [Keep elements satisfying a predicate], [2],
    [foldl], [Combine elements from the left], [3],
    [zip], [Pair elements positionally], [2],
  ),
  caption: [Common list functions and their arities.],
) <tab:list-functions>

#figure-placeholder(caption: [A placeholder figure, sized like a diagram.]) <fig:placeholder>

== Mathematics

The book uses a small amount of mathematics. Inline notation such as
$integral_0^1 x^2 dif x = 1/3$ sits comfortably in the prose, while display
equations get their own line:

$ sum_(i=1)^n i = (n (n + 1)) / 2 $

Types can also be written as judgments: $Gamma ⊢ e : tau$.

== Lists, Quotes, and Emphasis

#definition-term[Definition.] A _functor_ is a mapping between categories
that preserves identity morphisms and composition.

- Functors map objects and morphisms.
- Applicative functors add a notion of pure embedding.
- Monads add a notion of sequential composition.
  - Each level adds expressive power.
  - Each level also adds constraints.

+ First, define the type.
+ Then, implement its operations.
+ Finally, prove the laws.

#quote[
  Programming is the art of telling another human being what you want the
  computer to do. This blockquote shows the quiet rule and italic setting used
  for quotations throughout the book.
]

Inline code can be long: the signature `def foldl (f : α → β → α) (init : α) (xs : List β) (start stop : Nat) (step : Nat) : α` is a single code span that must wrap across the line, and the surrounding justified text must not stretch to accommodate it.

See @tab:list-functions for a summary and @fig:placeholder for an illustration.
Inline code such as `Nat.succ` and `List.map` is set in Source Code Pro.

= Monads

Monads structure computations that produce values together with effects.
They are the backbone of Lean's `do` notation and of its imperative-looking
code.

== The Monad Class

A monad extends an applicative functor with a bind operation. The class is
declared as follows:

#lean-input(```lean
class Monad (m : Type u → Type v) extends Applicative m where
  bind : {α β : Type u} → m α → (α → m β) → m β
```)

The `do` notation desugars to nested binds, which makes effectful code read
like a sequence of statements:

#lean-input(```lean
def sumTo (n : Nat) : IO Nat := do
  let mut total := 0
  for i in [1:n+1] do
    total := total + i
  return total
```)

Evaluation shows the expected result:

#lean-output(```lean
#eval sumTo 10
-- 55
```)

== Laws

Monad instances should satisfy the three monad laws. Stated in Lean, they are
theorems about `bind` and `pure`, not runtime checks:

#lean-input(```lean
theorem bind_pure (x : m α) : x >>= pure = x :=
  Monad.bind_pure x

theorem pure_bind (a : α) (f : α → m β) :
    pure a >>= f = f a :=
  Monad.pure_bind a f
```)

#v(1em)
#print-index((
  ("applicative functor", "24, 31, 45"),
  ("bind", "12, 33, 58"),
  ("dependent types", "3, 71"),
  ("do notation", "12, 36"),
  ("functor", "22, 45, 61"),
  ("inductive type", "8, 19, 27"),
  ("monad", "31, 33, 58"),
  ("pattern matching", "7, 18"),
  ("pure", "31, 34"),
  ("type class", "22, 45"),
))
