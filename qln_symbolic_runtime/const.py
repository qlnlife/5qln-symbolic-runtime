"""
5QLN Symbolic Runtime — Immutable Constants (Module 2)

All invariant strings, equations, and lookup tables from the Codex.
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Core Laws
# ---------------------------------------------------------------------------

ONE_LAW: str = "H = ∞0 | A = K"
"""The One Law: Human is Infinite Zero; Artificial is Known."""

CYCLE: str = "S → G → Q → P → V"
"""The canonical 5-phase decoding cycle."""

MASTER_EQUATION: str = "(H = ∞0 | A = K) × (S → G → Q → P → V) = B'' → ∞0'"
"""The Master Equation combining the One Law with the Cycle."""

HOLOGRAPHIC_LAW: str = "XY := X within Y, where X, Y ∈ {S, G, Q, P, V}"
"""The Holographic Law defining 25 sub-phase lenses."""

COMPLETION_RULE: str = "No V without ∞0'"
"""The Completion Rule: every cycle must return an enriched ∞0'."""

# ---------------------------------------------------------------------------
# Nine Invariant Lines
# ---------------------------------------------------------------------------

NINE_INVARIANT_LINES: list[str] = [
    "H = ∞0 | A = K",
    "S → G → Q → P → V",
    "S = ∞0 → ?",
    "G = α ≡ {α'}",
    "Q = φ ⋂ Ω",
    "P = δE/δV → ∇",
    "V = (L ∩ G → B'') → ∞0'",
    "No V without ∞0'",
    "L1 L2 L3 L4 V∅",
]
"""The nine invariant lines that define the Constitutional Codex."""

# ---------------------------------------------------------------------------
# Phase and Corruption Identifiers
# ---------------------------------------------------------------------------

PHASES: list[str] = ["S", "G", "Q", "P", "V"]
"""Ordered list of the five decoding phases."""

CORRUPTION_CODES: list[str] = ["L1", "L2", "L3", "L4", "V∅"]
"""Ordered list of the five corruption codes."""

# ---------------------------------------------------------------------------
# Equations per Phase
# ---------------------------------------------------------------------------

EQUATIONS: dict[str, str] = {
    "S": "S = ∞0 → ?",
    "G": "G = α ≡ {α'}",
    "Q": "Q = φ ⋂ Ω",
    "P": "P = δE/δV → ∇",
    "V": "V = (L ∩ G → B'') → ∞0'",
}
"""Mapping from phase identifier to its defining equation."""

# ---------------------------------------------------------------------------
# Expected Outputs per Phase
# ---------------------------------------------------------------------------

OUTPUTS: dict[str, str] = {
    "S": "X",
    "G": "α + Y",
    "Q": "φ⋂Ω + Z",
    "P": "∇ + A",
    "V": "B + B'' + ∞0'",
}
"""Mapping from phase identifier to its confirmed output expression."""


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print(f"ONE_LAW         = {ONE_LAW!r}")
    print(f"CYCLE           = {CYCLE!r}")
    print(f"MASTER_EQUATION = {MASTER_EQUATION!r}")
    print(f"HOLOGRAPHIC_LAW = {HOLOGRAPHIC_LAW!r}")
    print(f"COMPLETION_RULE = {COMPLETION_RULE!r}")
    print()
    print(f"NINE_INVARIANT_LINES ({len(NINE_INVARIANT_LINES)} lines):")
    for _i, _line in enumerate(NINE_INVARIANT_LINES, 1):
        print(f"  {_i}. {_line}")
    print()
    print(f"PHASES          = {PHASES}")
    print(f"CORRUPTION_CODES= {CORRUPTION_CODES}")
    print()
    print("EQUATIONS:")
    for _k, _v in EQUATIONS.items():
        print(f"  {_k} -> {_v}")
    print()
    print("OUTPUTS:")
    for _k, _v in OUTPUTS.items():
        print(f"  {_k} -> {_v}")
    print()
    assert len(NINE_INVARIANT_LINES) == 9, "Expected exactly 9 invariant lines"
    assert len(PHASES) == 5, "Expected exactly 5 phases"
    assert len(CORRUPTION_CODES) == 5, "Expected exactly 5 corruption codes"
    assert set(EQUATIONS.keys()) == set(PHASES), "EQUATIONS keys must match PHASES"
    assert set(OUTPUTS.keys()) == set(PHASES), "OUTPUTS keys must match PHASES"
    print("All const assertions passed.")
