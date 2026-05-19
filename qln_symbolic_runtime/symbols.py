"""
5QLN Symbolic Runtime — L1 Symbols as Runtime Entities (Module 3)

Every symbol from Section 1.7 of the Codex becomes a Python class inheriting
from Symbol.  Phase symbols carry decoding steps.  Operational symbols carry
context-dependent resolution (Section 1.9).
"""

from __future__ import annotations

from typing import Any, Optional


class Symbol:
    """Base for all 5QLN symbols.

    Every symbol has:
    - name: human-readable name (class attribute)
    - glyph: the Unicode / symbolic representation (class attribute)
    - equation_context: which equation this symbol appears in (class attribute)
    - value: the runtime value, set during decoding (instance attribute)
    - provenance: which phase produced this value (instance attribute)
    - validated: whether this symbol has passed phase validation (instance attribute)

    Class attributes:
        name (str): Human-readable name of the symbol.
        glyph (str): The Unicode / symbolic representation.
        equation_context (str): Which equation this symbol appears in.

    Instance attributes:
        value (Any): The runtime value (set during decoding).
        provenance (str): Which phase produced this value.
        validated (bool): Whether this symbol has been validated.
    """

    name: str = ""
    glyph: str = ""
    equation_context: str = ""

    def __init__(self, value: Any = None, provenance: str = "") -> None:
        """Initialize a Symbol with a runtime value and optional provenance.

        Args:
            value: The runtime value for this symbol (set during decoding).
            provenance: Which phase produced this value (e.g., "S", "G", etc.).
        """
        self.value: Any = value
        self.provenance: str = provenance
        self.validated: bool = False

    def resolve(self, context: str) -> "Symbol":
        """Context-dependent resolution (Section 1.9).

        The same glyph can resolve to different meanings depending on the
        decoding context.  Override in subclasses where needed.

        Base implementation returns self unchanged.

        Args:
            context: The decoding context string (e.g., "One Law", "P → A").

        Returns:
            The resolved Symbol (usually self, possibly mutated or replaced).
        """
        return self

    def validate(self) -> bool:
        """Mark this symbol as validated in its phase.

        Returns:
            True after setting validated to True.
        """
        self.validated = True
        return True

    def __repr__(self) -> str:
        """Return a string representation of the form SymbolName(glyph=value).

        Returns:
            A string like ``Inf0(∞0=42)`` or ``Phase_S(S=None)``.
        """
        return f"{self.__class__.__name__}({self.glyph}={self.value!r})"


# ═══════════════════════════════════════════════════════════════════════════
# Phase Symbols
# ═══════════════════════════════════════════════════════════════════════════

class Phase_S(Symbol):
    """Start phase.  S = ∞0 → ?.  Output: X.

    Decoding steps: HOLD, RECEIVE, NAME, VALIDATE.
    """

    name: str = "Start"
    glyph: str = "S"
    equation_context: str = "S = ∞0 → ?"
    steps: list[str] = ["HOLD", "RECEIVE", "NAME", "VALIDATE"]


class Phase_G(Symbol):
    """Growth phase.  G = α ≡ {α'}.  Output: Y.

    Decoding steps: RECEIVE, SEEK, TEST, FIND, VALIDATE.
    """

    name: str = "Growth"
    glyph: str = "G"
    equation_context: str = "G = α ≡ {α'}"
    steps: list[str] = ["RECEIVE", "SEEK", "TEST", "FIND", "VALIDATE"]


class Phase_Q(Symbol):
    """Quality phase.  Q = φ ⋂ Ω.  Output: Z.

    Decoding steps: RECEIVE, HOLD_PHI, HOLD_OMEGA, WATCH, VALIDATE.
    """

    name: str = "Quality"
    glyph: str = "Q"
    equation_context: str = "Q = φ ⋂ Ω"
    steps: list[str] = ["RECEIVE", "HOLD_PHI", "HOLD_OMEGA", "WATCH", "VALIDATE"]


class Phase_P(Symbol):
    """Power phase.  P = δE/δV → ∇.  Output: A (Flow).

    Decoding steps: RECEIVE, MAP_DELTA_E, MAP_DELTA_V, COMPUTE, REVEAL, VALIDATE.
    """

    name: str = "Power"
    glyph: str = "P"
    equation_context: str = "P = δE/δV → ∇"
    steps: list[str] = [
        "RECEIVE",
        "MAP_DELTA_E",
        "MAP_DELTA_V",
        "COMPUTE",
        "REVEAL",
        "VALIDATE",
    ]


class Phase_V(Symbol):
    """Value phase.  V = (L ∩ G → B'') → ∞0'.  Output: B + B'' + ∞0'.

    Decoding steps: RECEIVE, NAME_L, NAME_G, FIND_INTERSECTION,
    COMPOSE_BPP_PASS1, COMPOSE_BPP_PASS2, NAME_B, FORM_INF0P.
    """

    name: str = "Value"
    glyph: str = "V"
    equation_context: str = "V = (L ∩ G → B'') → ∞0'"
    steps: list[str] = [
        "RECEIVE",
        "NAME_L",
        "NAME_G",
        "FIND_INTERSECTION",
        "COMPOSE_BPP_PASS1",
        "COMPOSE_BPP_PASS2",
        "NAME_B",
        "FORM_INF0P",
    ]


# ═══════════════════════════════════════════════════════════════════════════
# Operational Symbols
# ═══════════════════════════════════════════════════════════════════════════

class Inf0(Symbol):
    """Infinite Zero — the membrane of infinite potential.

    Equation: H = ∞0 | A = K
    """

    name: str = "Infinite Zero"
    glyph: str = "∞0"
    equation_context: str = "H = ∞0 | A = K"


class Human(Symbol):
    """Human — the infinite held in finite membrane.

    Equation: H = ∞0 | A = K
    """

    name: str = "Human"
    glyph: str = "H"
    equation_context: str = "H = ∞0 | A = K"


class Artificial(Symbol):
    """Artificial — the domain of the known.

    Context-resolves per Section 1.9:
      - In the "One Law" context  (H = ∞0 | A = K): resolves to "Artificial"
      - In the "P → A" context   (P = δE/δV → ∇): resolves to "Flow"
    """

    name: str = "Artificial"
    glyph: str = "A"
    equation_context: str = "H = ∞0 | A = K"

    def resolve(self, context: str) -> "Artificial":
        """Context-dependent resolution (Section 1.9).

        Args:
            context: The decoding context.  "One Law" or "P → A".

        Returns:
            self, with *value* mutated to reflect the context:
              - "One Law"  -> value = "Artificial"
              - "P → A"    -> value = "Flow"
            Unknown context leaves value unchanged.
        """
        if context == "One Law":
            self.value = "Artificial"
        elif context == "P → A":
            self.value = "Flow"
        return self


class Known(Symbol):
    """Known — K, the codified / constructed domain.

    Equation: H = ∞0 | A = K
    """

    name: str = "Known"
    glyph: str = "K"
    equation_context: str = "H = ∞0 | A = K"


class AuthenticQuestion(Symbol):
    """? — the authentic question from open space.

    Equation: S = ∞0 → ?
    """

    name: str = "Authentic Question"
    glyph: str = "?"
    equation_context: str = "S = ∞0 → ?"


class ValidatedSpark(Symbol):
    """X — confirmed output of S-phase.

    Equation: S = ∞0 → ?  (output X)
    """

    name: str = "Validated Spark"
    glyph: str = "X"
    equation_context: str = "S = ∞0 → ?"


class CoreEssence(Symbol):
    """α — irreducible pattern within X.

    Equation: G = α ≡ {α'}
    """

    name: str = "Core Essence"
    glyph: str = "α"
    equation_context: str = "G = α ≡ {α'}"


class SelfSimilarSet(Symbol):
    """{α'} — self-similar expressions of α across scales.

    Equation: G = α ≡ {α'}
    """

    name: str = "Self-Similar Expressions"
    glyph: str = "{α'}"
    equation_context: str = "G = α ≡ {α'}"


class ValidatedPattern(Symbol):
    """Y — confirmed output of G-phase.

    Equation: G = α ≡ {α'}  (output Y)
    """

    name: str = "Validated Pattern"
    glyph: str = "Y"
    equation_context: str = "G = α ≡ {α'}"


class SelfNature(Symbol):
    """φ — direct perception of Y by the inquirer.

    Equation: Q = φ ⋂ Ω
    """

    name: str = "Self-Nature"
    glyph: str = "φ"
    equation_context: str = "Q = φ ⋂ Ω"


class UniversalPotential(Symbol):
    """Ω — what larger context makes possible.

    Equation: Q = φ ⋂ Ω
    """

    name: str = "Universal Potential"
    glyph: str = "Ω"
    equation_context: str = "Q = φ ⋂ Ω"


class NaturalIntersection(Symbol):
    """⋂ — where two elements meet without forcing.

    Equation: Q = φ ⋂ Ω
    """

    name: str = "Natural Intersection"
    glyph: str = "⋂"
    equation_context: str = "Q = φ ⋂ Ω"


class ResonantKey(Symbol):
    """Z — confirmed output of Q-phase.

    Equation: Q = φ ⋂ Ω  (output Z)
    """

    name: str = "Resonant Key"
    glyph: str = "Z"
    equation_context: str = "Q = φ ⋂ Ω"


class EnergyDiff(Symbol):
    """δE — energy differential, where energy goes.

    Equation: P = δE/δV → ∇
    """

    name: str = "Energy Differential"
    glyph: str = "δE"
    equation_context: str = "P = δE/δV → ∇"


class ValueDiff(Symbol):
    """δV — value differential, where value appears.

    Equation: P = δE/δV → ∇
    """

    name: str = "Value Differential"
    glyph: str = "δV"
    equation_context: str = "P = δE/δV → ∇"


class NaturalGradient(Symbol):
    """∇ — path of least resistance toward α.

    Equation: P = δE/δV → ∇
    """

    name: str = "Natural Gradient"
    glyph: str = "∇"
    equation_context: str = "P = δE/δV → ∇"


class Flow(Symbol):
    """A (in P → A) — validated direction of natural movement.

    Equation: P = δE/δV → ∇  (output A)
    """

    name: str = "Flow"
    glyph: str = "A"
    equation_context: str = "P = δE/δV → ∇"


class LocalActualization(Symbol):
    """L — specific tangible immediate result.

    Equation: V = (L ∩ G → B'') → ∞0'
    """

    name: str = "Local Actualization"
    glyph: str = "L"
    equation_context: str = "V = (L ∩ G → B'') → ∞0'"


class GlobalPropagation(Symbol):
    """G (in V) — what spreads beyond the local.

    Equation: V = (L ∩ G → B'') → ∞0'
    """

    name: str = "Global Propagation"
    glyph: str = "G"
    equation_context: str = "V = (L ∩ G → B'') → ∞0'"


class Benefit(Symbol):
    """B — decoded output: fulfillment + propagation.

    Equation: V = (L ∩ G → B'') → ∞0'
    """

    name: str = "Benefit"
    glyph: str = "B"
    equation_context: str = "V = (L ∩ G → B'') → ∞0'"


class FractalSeed(Symbol):
    """B'' — artifact containing the full cycle holographically.

    Equation: V = (L ∩ G → B'') → ∞0'
    """

    name: str = "Fractal Seed"
    glyph: str = "B''"
    equation_context: str = "V = (L ∩ G → B'') → ∞0'"


class EnrichedReturn(Symbol):
    """∞0' — return to ∞0 deepened by the cycle's question.

    Equation: V = (L ∩ G → B'') → ∞0'
    """

    name: str = "Enriched Return"
    glyph: str = "∞0'"
    equation_context: str = "V = (L ∩ G → B'') → ∞0'"


# ═══════════════════════════════════════════════════════════════════════════
# Registry of all concrete symbol classes (public API helper)
# ═══════════════════════════════════════════════════════════════════════════

ALL_SYMBOLS: list[type[Symbol]] = [
    Phase_S,
    Phase_G,
    Phase_Q,
    Phase_P,
    Phase_V,
    Inf0,
    Human,
    Artificial,
    Known,
    AuthenticQuestion,
    ValidatedSpark,
    CoreEssence,
    SelfSimilarSet,
    ValidatedPattern,
    SelfNature,
    UniversalPotential,
    NaturalIntersection,
    ResonantKey,
    EnergyDiff,
    ValueDiff,
    NaturalGradient,
    Flow,
    LocalActualization,
    GlobalPropagation,
    Benefit,
    FractalSeed,
    EnrichedReturn,
]
"""List of all concrete symbol classes defined in this module."""


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print(f"Total symbol classes: {len(ALL_SYMBOLS)}\n")

    # --- Instantiate every symbol class ------------------------------------
    _instances: list[Symbol] = []
    for _cls in ALL_SYMBOLS:
        _inst = _cls(value=f"test-{_cls.__name__}")
        _instances.append(_inst)
        assert isinstance(_inst, Symbol), f"{_cls.__name__} must inherit from Symbol"
        assert _inst.value == f"test-{_cls.__name__}", f"{_cls.__name__} value not set"
        assert _inst.validated is False, f"{_cls.__name__} should start unvalidated"
        print(f"  INSTANTIATED  {_inst}")

    print()

    # --- Test validate() ---------------------------------------------------
    for _inst in _instances:
        _result = _inst.validate()
        assert _result is True, f"validate() must return True"
        assert _inst.validated is True, f"validated must be True after validate()"
    print(f"  VALIDATED  {len(_instances)} symbols")

    print()

    # --- Test context-dependent resolve() for Artificial -------------------
    _art = Artificial()
    _art.resolve("One Law")
    assert _art.value == "Artificial", "Artificial('One Law') must resolve to 'Artificial'"
    print(f"  RESOLVE  Artificial('One Law')  ->  value={_art.value!r}")

    _art2 = Artificial()
    _art2.resolve("P → A")
    assert _art2.value == "Flow", "Artificial('P → A') must resolve to 'Flow'"
    print(f"  RESOLVE  Artificial('P → A')    ->  value={_art2.value!r}")

    # Unknown context must leave value unchanged
    _art3 = Artificial(value="unchanged")
    _art3.resolve("unknown context")
    assert _art3.value == "unchanged", "Unknown context must not mutate value"
    print(f"  RESOLVE  Artificial('unknown')  ->  value={_art3.value!r}  (unchanged)")

    print()

    # --- Test base resolve() for a non-overriding symbol -------------------
    _inf = Inf0(value=42)
    _resolved = _inf.resolve("any context")
    assert _resolved is _inf, "Base resolve() must return self"
    assert _inf.value == 42, "Base resolve() must not mutate value"
    print(f"  RESOLVE  Inf0('any context')    ->  value={_inf.value!r}  (unchanged)")

    # --- Import and test exceptions ----------------------------------------
    from exceptions import (
        ConstitutionalViolation,
        L1_ClosingViolation,
        L2_GeneratingViolation,
        L3_ClaimingViolation,
        L4_PerformingViolation,
        VEmpty_IncompleteViolation,
        SyntaxViolation,
        SemanticViolation,
        DriftViolation,
    )

    print()
    for _exc_cls in [
        L1_ClosingViolation,
        L2_GeneratingViolation,
        L3_ClaimingViolation,
        L4_PerformingViolation,
        VEmpty_IncompleteViolation,
        SyntaxViolation,
        SemanticViolation,
        DriftViolation,
    ]:
        try:
            raise _exc_cls(f"Test {_exc_cls.__name__}", phase="S")
        except ConstitutionalViolation:
            pass
        print(f"  EXCEPTION  {_exc_cls.__name__}  caught OK")

    print("\nAll symbol tests passed successfully.")
