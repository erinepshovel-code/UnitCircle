"""
UCNS bone canon registry — maps bones_v1.json closed-operator inventory
to UCNS-compatible embedding parameters.

Provides the canonical family → angular sector assignment that
BoneEmbedder implementations use to place bone events on the Möbius-cylindrical
hyperdisk at depth-1 (z=1).

Sector assignment (five equal sectors in UCNS angle space [0, 4)):
  P → 0         (sector 0 of 5)
  K → 4/5       (sector 1 of 5)
  Q → 8/5       (sector 2 of 5)
  T → 12/5      (sector 3 of 5)
  S → 16/5      (sector 4 of 5)

Within each sector, individual bones are spread evenly by their index in
the canon list (frozen v1.0.0). This gives every bone a stable, unique
UCNS angle coordinate that is derivable from the canon alone.

Collision priority (P > K > Q > T > S) is preserved: for words appearing
in multiple families, the highest-priority family's angle wins.

Depth: bones are depth-1 objects (z = 1 on the Möbius cylinder).
Zero (contact event at the Möbius twist) is z = 0.
Implementation cap: z ≤ 3. Theoretical cylinder: z ≤ 7.

Canon version: bones_v1.json v1.0.0
"""
from __future__ import annotations
from fractions import Fraction
from typing import NamedTuple

BONE_CANON_VERSION = "bones_v1.json"
BONE_CANON_SCHEMA = "edcmbone/bones_v1"

FAMILIES = ("P", "K", "Q", "T", "S")
COLLISION_PRIORITY = ("P", "K", "Q", "T", "S")  # highest first
BONE_DEPTH = 1

# UCNS angle space: [0, 4) per full traversal.
# Five equal sectors, each width 4/5.
SECTOR_WIDTH = Fraction(4, 5)
FAMILY_SECTOR_ORIGIN: dict[str, Fraction] = {
    fam: Fraction(i) * SECTOR_WIDTH for i, fam in enumerate(FAMILIES)
}

# ── Full closed-class inventory (bones_v1.json v1.0.0, frozen) ───────────────

_INVENTORY: dict[str, list[str]] = {
    "P": [
        "in","on","at","by","with","without","for","from","to","of","off",
        "into","onto","out","over","under","above","below","before","after",
        "between","among","within","beyond","through","across","against","around",
        "near","along","amid","during","via","per","upon","beneath","behind",
        "beside","besides","inside","outside","toward","towards","past",
        "than","as",
        "because","despite","except","like","unlike",
    ],
    "K": [
        "and","but","or","nor","yet","so",
        "because","although","though","since","while","whereas",
        "if","unless","until","when","whenever","where","wherever",
        "before","after","once","than","that",
        "either","neither","both","whether",
        "however","therefore","thus","moreover","instead","otherwise",
    ],
    "Q": [
        "not","no","never","none","nothing","nobody","neither","nor",
        "all","some","any","many","much","few","several",
        "most","more","less","least","enough",
        "very","too","only","just","also","even","quite","rather","almost",
        "who","what","when","where","why","how","which","whom","whose",
        "yes","yeah","yep","nope","nah","okay","ok",
    ],
    "T": [
        "am","is","are","was","were","be","been","being",
        "have","has","had",
        "do","does","did",
        "can","could","may","might","must","shall","should","will","would",
        "now","then","today","tomorrow","yesterday",
        "already","still","yet",
    ],
    "S": [
        "a","an","the",
        "this","that","these","those",
        "my","your","his","her","its","our","their",
        "mine","yours","hers","ours","theirs",
        "each","every","either","neither","some","any","no",
        "another","other","others","such","same",
        "i","me","you","he","him","she","her","it","we","us","they","them",
        "myself","yourself","yourselves","himself","herself",
        "itself","ourselves","themselves",
        "someone","somebody","something",
        "anyone","anybody","anything",
        "everyone","everybody","everything",
        "noone","nobody","nothing",
        "who","whom","whose","which","that",
        "there","here","now","then",
    ],
}

# Contraction fragments
CONTRACTION_FRAGMENTS: dict[str, str] = {
    "n't": "Q", "'t": "Q",
    "'ll": "T", "'d": "T", "'re": "T", "'m": "T", "'ve": "T", "'s": "T",
}

# Punctuation emissions: token → list of (family, count)
PUNCTUATION_EMIT: dict[str, list[tuple[str, int]]] = {
    "?": [("Q", 1)],
    "–": [("K", 1)],
    ";": [("K", 1)],
    ":": [("K", 1)],
    "—": [],
    "/": [],
}


# ── Canonical angle registry ──────────────────────────────────────────────────

class BoneAngle(NamedTuple):
    """Canonical UCNS angle for a single bone word."""
    word: str
    family: str
    sector_origin: Fraction   # family sector start in [0, 4)
    within_offset: Fraction   # position within sector
    angle: Fraction           # total angle = (sector_origin + within_offset) % 4


def _build_registry() -> dict[str, BoneAngle]:
    """Build word → BoneAngle with collision priority (P overwrites lower families)."""
    # Process lowest priority first; higher-priority family overwrites.
    reg: dict[str, BoneAngle] = {}
    for fam in reversed(COLLISION_PRIORITY):   # S, T, Q, K, P
        words = _INVENTORY[fam]
        origin = FAMILY_SECTOR_ORIGIN[fam]
        n = len(words)
        for idx, word in enumerate(words):
            offset = Fraction(idx, n) * SECTOR_WIDTH
            reg[word] = BoneAngle(
                word=word,
                family=fam,
                sector_origin=origin,
                within_offset=offset,
                angle=(origin + offset) % 4,
            )
    return reg


BONE_REGISTRY: dict[str, BoneAngle] = _build_registry()


def bone_angle(word: str) -> BoneAngle | None:
    """Canonical UCNS angle for a bone word. Returns None if open-class (flesh)."""
    return BONE_REGISTRY.get(word.lower())


def family_sector(family: str) -> Fraction:
    """Sector origin angle for a bone family."""
    return FAMILY_SECTOR_ORIGIN[family]


def bone_count() -> dict[str, int]:
    """Count of unique canonically-resolved bone words per family."""
    counts: dict[str, int] = {f: 0 for f in FAMILIES}
    for ba in BONE_REGISTRY.values():
        counts[ba.family] += 1
    return counts
