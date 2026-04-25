# UCNS — Current Completeness Frontier (through v0.9.0)

**Status:** frontier summary of what is currently defended, what is oracle-only, and what currently fails.  
**Scope:** compresses the proven/defended milestones across the v0.6.x–v0.9.0 line.  
**Accreditation:** GPT generated from context provided by Grok, Claude as prompted by Erin Spencer.

---

## hmm

This document does **not** replace the detailed v0.3/v0.4/v0.5/v0.6 specs.  
It records the current theorem frontier honestly.

The current state separates into four layers:

1. depth-1 results that are defended,
2. a depth-2 oracle result that is defended,
3. the full frozen depth-2 domain, which is not solved,
4. carrier widening, which is not solved.

---

# 1. Defended Results

## 1.1 Flat kernel defended

The flat paired UCNS kernel is defended for its stated scope.

This includes:

- paired traversal objects,
- external zero,
- intrinsic/declared carrier split,
- ordered-concatenation multiplication,
- normalization,
- sequence-sensitive equivalence,
- flat factor search,
- content-level disk-flip symmetry rather than sequence-level disk-flip symmetry.

## 1.2 Depth-1 restricted completeness defended

The depth-1 restricted completeness theorem is defended on its frozen domain.

That is the strongest general completeness result currently established.

## 1.3 Depth-2 oracle defended

The smallest frozen depth-2 oracle is GREEN.

There is a frozen theorem for that oracle class:

\[
\texttt{factor\_search}
\text{ returns the correct factorization}
\iff
P \text{ is seq-composite in the oracle class.}
\]

This is a **restricted theorem**. It does not extend to the full frozen depth-2 domain.

---

# 2. Current Failure Boundary

## 2.1 Full frozen depth-2 domain is not solved

After the final push on the frozen depth-2 domain, the tested depth-2 cases still fail as a class.

The depth-2 oracle remains GREEN, but the full domain does not.

So the current honest statement is:

- depth-2 oracle theorem: holds,
- full frozen depth-2 domain: not yet complete.

## 2.2 Carrier widening is not solved

Carrier widening beyond the defended small-carrier domain also fails on tested widened cases.

So the honest state is:

- widening does not rescue the recursive completeness problem,
- the bottleneck is the recursive payload / quotient layer,
- not merely insufficient carrier coverage.

---

# 3. Root Cause Frontier

The main bottleneck is the recursive payload layer.

The currently frozen failure analysis identifies the need for:

\[
\text{host recovery}
\to
\text{payload system construction}
\to
\text{global witness verification}
\]

That is, a true staged recursive factorization / quotient architecture.

The existing quotient engine is strong enough for:

- depth-1,
- the frozen depth-2 oracle,

but not strong enough for:

- the full frozen depth-2 domain,
- widened-carrier recursive search.

---

# 4. Current Theorem Frontier

## 4.1 What is currently justified

The following claims are justified:

### A. Flat theorem frontier
Flat kernel algebra and factorization results hold on the frozen flat scope.

### B. Depth-1 completeness frontier
Restricted completeness holds on the defended depth-1 domain.

### C. Depth-2 oracle frontier
Restricted completeness holds on the frozen smallest depth-2 oracle class.

## 4.2 What is **not** currently justified

The following stronger claims are **not** currently justified:

### A. Full depth-2 completeness
\[
\texttt{factor\_search}
\text{ is complete on the whole frozen depth-2 domain}
\]

### B. Widened-carrier completeness
\[
\texttt{factor\_search}
\text{ is complete after widening } n_{\min}
\]

### C. General recursive completeness
\[
\texttt{factor\_search}
\text{ is complete for arbitrary finite depth}
\]

None of these should be claimed at the current frontier.

---

# 5. Recommended Boundary Statement

The clean present-tense statement is:

> UCNS currently has a defended flat kernel, a defended depth-1 restricted completeness theorem, and a defended depth-2 oracle theorem. The full frozen depth-2 domain and carrier-widened recursive domain remain unsolved. The active bottleneck is the recursive payload / witness-matrix layer.

---

# 6. Recommended Next Work

## 6.1 If preserving results is the goal

Freeze the frontier here and move to other work.

This preserves the real theorems already earned.

## 6.2 If pushing recursion is the goal

The next honest line of work is **not more widening**.

It is a structural redesign of the recursive factorization layer:

- staged host-first reconstruction,
- coupled payload-system solving,
- witness-matrix consistency,
- non-atomic recursive payload descent.

That redesign should be treated as a fresh branch rather than a minor widening patch.

---

# 7. Compression

The present UCNS completeness frontier is:

- **green:** flat
- **green:** depth-1 restricted theorem
- **green:** depth-2 oracle only
- **red:** full frozen depth-2 domain
- **red:** carrier widening

That is the current honest frontier.

---

**Accreditation:** GPT generated from context provided by Grok, Claude as prompted by Erin Spencer.
