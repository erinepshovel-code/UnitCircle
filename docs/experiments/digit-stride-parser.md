# Digit-stride parser experiment

## Definition

For a source number `x`, base `b`, and selector value `n`, write the fractional
base-`b` digits as:

```text
d_1 d_2 d_3 ...
```

The digit-stride row is:

```text
W_{n,b}(x) = d_n d_{2n} d_{3n} ... d_{n^2}
```

The row has exactly `n` landed numerals and ends at fractional digit position
`n^2`. This is a positional sampler, not a variable-length chunk parser.

## Selector regions

The experiment separates the selector set into three regions:

```text
fib_only   = Fibonacci numbers greater than 5 that are not prime
prime_only = primes greater than 5 that are not Fibonacci numbers
bridge     = numbers greater than 5 that are both Fibonacci and prime
```

The first bridge rows are:

```text
13, 89, 233, ...
```

Bridge rows are not contrast evidence. For any source number and any base,
`W_{13,b}` is the same row under the Fibonacci parser and the prime parser
because both parsers land on the same positions:

```text
13, 26, 39, ..., 169
```

## Base-agnostic versus base-parametric

Base-agnostic structure:

- the selector value `n`;
- the landed-position set `{n, 2n, ..., n^2}`;
- bridge membership such as `13 in Fibonacci ∩ Prime`;
- disjointness of distinct prime rows in this parser window.

Base-parametric observations:

- the landed numerals themselves;
- the word `W_{n,b}(x)`;
- residues of that word modulo `360`, `2880`, or another modulus;
- entropy and phase/coherence statistics.

The decimal observation `W_{13,10}(pi) = 7878083465579` is therefore a datum, not
the invariant. The invariant is that row `13` is a bridge row in every base.

## Script

```bash
python scripts/digit_stride_experiment.py --self-check
```

Run the default experiment over `pi` and `phi`, bases `2,3,5,7,10,11,13,16`,
selector values through `89`, and projection moduli `360,2880,359`:

```bash
python scripts/digit_stride_experiment.py --out-dir data/digit_stride
```

Run a compact base-10 check through the first bridge row:

```bash
python scripts/digit_stride_experiment.py \
  --sources pi,phi \
  --bases 10 \
  --max-n 13 \
  --word-limit -1 \
  --out-dir data/digit_stride_w13
```

Use a larger bridge horizon:

```bash
python scripts/digit_stride_experiment.py \
  --sources pi,phi,e,sqrt2 \
  --bases 2,3,5,7,10,11,13,16 \
  --max-n 233 \
  --word-limit 256 \
  --out-dir data/digit_stride_233
```

## Outputs

The script writes:

```text
data/digit_stride/rows.csv
```

One row per `(source, base, n)` with:

- `membership`: `fib_only`, `prime_only`, or `bridge`;
- `length`: equal to `n`;
- `final_position`: equal to `n^2`;
- `word`: the landed numeral word, optionally truncated;
- `word_sha256`: stable identity for the full word;
- `digit_entropy_norm`: digit entropy divided by `log(base)`;
- `digit_phase_R`: unit-circle concentration of landed digits;
- `transition_coherence`: unit-circle coherence of successive digit changes;
- `residue_mod_360`, `residue_mod_2880`, `residue_mod_359`, etc.

```text
data/digit_stride/source_comparisons.csv
```

Pairwise source comparisons within each `(base, n)` row, including exact digit
match counts and match rate.

```text
data/digit_stride/manifest.json
```

Run metadata, selector summary, and deterministic self-check values.

## Tests

```bash
python -m unittest tests/test_digit_stride_experiment.py
```

The tests check:

- bridge rows `13, 89, 233`;
- `W_13` positions `13, 26, ..., 169`;
- `13` as bridge, `8` as Fibonacci-only, `7` as prime-only;
- disjointness of small distinct prime rows;
- known base-10 `W_13` values for `pi` and `phi`.

## hmmm

The experiment is now set up to prevent the false binary. Rows can be Fibonacci-only,
prime-only, or bridge. A bridge-row anomaly does not distinguish the two selectors;
it marks the intersection where both selectors touched the same source positions.
