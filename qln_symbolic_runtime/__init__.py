"""
5QLN Symbolic Runtime — Execute the Constitutional Codex as operational code.

Every symbol from L1 (the Language) is a runtime entity.
Every decoding step from D1 (the Decoder) is an executable method.
Every validation rule from C1 (the Compiler) is a runtime assertion.

Usage::

    from qln_symbolic_runtime import CycleRunner
    runner = CycleRunner()
    trace = runner.run_cycle(data_entity="Your inquiry here")

Modules
-------
- **exceptions** — Constitutional violation hierarchy.
- **const** — Immutable constants from the Codex.
- **symbols** — L1 symbols as runtime classes.
- **phases** — D1 phase engines with symbol-by-symbol decoding.
- **holographic** — 25 sub-phase lens matrix.
- **corruption** — L1–L4 and V∅ runtime guards.
- **compiler** — C1 syntax, semantic, and drift validators.
- **cycle** — Full cycle runner with adaptive context chain.
- **attestation** — SHA-256 provenance fingerprinting.
- **repl** — Interactive command-line interface.
"""

__version__ = "1.0.0"
__codex_source__ = "https://www.5qln.com/codex"

# ------------------------------------------------------------------ #
# Exceptions
# ------------------------------------------------------------------ #
from qln_symbolic_runtime.exceptions import (
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

# ------------------------------------------------------------------ #
# Constants
# ------------------------------------------------------------------ #
from qln_symbolic_runtime.const import (
    ONE_LAW,
    CYCLE,
    MASTER_EQUATION,
    HOLOGRAPHIC_LAW,
    COMPLETION_RULE,
    NINE_INVARIANT_LINES,
    PHASES,
    CORRUPTION_CODES,
    EQUATIONS,
    OUTPUTS,
)

# ------------------------------------------------------------------ #
# Symbols
# ------------------------------------------------------------------ #
from qln_symbolic_runtime.symbols import (
    Symbol,
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
)

# ------------------------------------------------------------------ #
# Phase engines
# ------------------------------------------------------------------ #
from qln_symbolic_runtime.phases import (
    PhaseEngine,
    S_PhaseEngine,
    G_PhaseEngine,
    Q_PhaseEngine,
    P_PhaseEngine,
    V_PhaseEngine,
)

# ------------------------------------------------------------------ #
# Supporting sub-systems
# ------------------------------------------------------------------ #
from qln_symbolic_runtime.holographic import LensMatrix
from qln_symbolic_runtime.corruption import CorruptionDetector
from qln_symbolic_runtime.compiler import C1Compiler

# ------------------------------------------------------------------ #
# Integration layer (Modules 8–10)
# ------------------------------------------------------------------ #
from qln_symbolic_runtime.cycle import CycleRunner
from qln_symbolic_runtime.attestation import AttestationChain

# ------------------------------------------------------------------ #
# Public API
# ------------------------------------------------------------------ #
__all__ = [
    # Meta
    "__version__",
    "__codex_source__",
    # Exceptions
    "ConstitutionalViolation",
    "L1_ClosingViolation",
    "L2_GeneratingViolation",
    "L3_ClaimingViolation",
    "L4_PerformingViolation",
    "VEmpty_IncompleteViolation",
    "SyntaxViolation",
    "SemanticViolation",
    "DriftViolation",
    # Constants
    "ONE_LAW",
    "CYCLE",
    "MASTER_EQUATION",
    "HOLOGRAPHIC_LAW",
    "COMPLETION_RULE",
    "NINE_INVARIANT_LINES",
    "PHASES",
    "CORRUPTION_CODES",
    "EQUATIONS",
    "OUTPUTS",
    # Symbols
    "Symbol",
    "Phase_S",
    "Phase_G",
    "Phase_Q",
    "Phase_P",
    "Phase_V",
    "Inf0",
    "Human",
    "Artificial",
    "Known",
    "AuthenticQuestion",
    "ValidatedSpark",
    "CoreEssence",
    "SelfSimilarSet",
    "ValidatedPattern",
    "SelfNature",
    "UniversalPotential",
    "NaturalIntersection",
    "ResonantKey",
    "EnergyDiff",
    "ValueDiff",
    "NaturalGradient",
    "Flow",
    "LocalActualization",
    "GlobalPropagation",
    "Benefit",
    "FractalSeed",
    "EnrichedReturn",
    # Phase engines
    "PhaseEngine",
    "S_PhaseEngine",
    "G_PhaseEngine",
    "Q_PhaseEngine",
    "P_PhaseEngine",
    "V_PhaseEngine",
    # Sub-systems
    "LensMatrix",
    "CorruptionDetector",
    "C1Compiler",
    # Integration layer
    "CycleRunner",
    "AttestationChain",
]
