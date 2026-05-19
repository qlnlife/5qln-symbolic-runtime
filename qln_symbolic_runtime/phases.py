"""
5QLN Symbolic Runtime — D1 Decoding Engine (phases.py)

Five phase engine classes, all inheriting from the abstract ``PhaseEngine``.
Each engine executes its Constitutional equation symbol-by-symbol,
producing validated output artifacts that feed the adaptive context chain.

Phases:
    S_PhaseEngine — S = ∞0 → ? → X
    G_PhaseEngine — G = α ≡ {α'} → α + Y
    Q_PhaseEngine — Q = φ ⋂ Ω → φ⋂Ω + Z
    P_PhaseEngine — P = δE/δV → ∇ → ∇ + A
    V_PhaseEngine — V = (L ∩ G → B'') → ∞0' → B + B'' + ∞0'
"""

from __future__ import annotations

import re
from abc import ABC, abstractmethod
from typing import Any

from .const import EQUATIONS
from .exceptions import (
    L1_ClosingViolation,
    L2_GeneratingViolation,
    L4_PerformingViolation,
    VEmpty_IncompleteViolation,
)
from .symbols import (
    AuthenticQuestion,
    Benefit,
    CoreEssence,
    EnrichedReturn,
    EnergyDiff,
    Flow,
    FractalSeed,
    GlobalPropagation,
    Inf0,
    LocalActualization,
    NaturalGradient,
    NaturalIntersection,
    ResonantKey,
    SelfNature,
    SelfSimilarSet,
    UniversalPotential,
    ValidatedPattern,
    ValidatedSpark,
    ValueDiff,
)


# ---------------------------------------------------------------------------
# Abstract base
# ---------------------------------------------------------------------------

class PhaseEngine(ABC):
    """Abstract base for all 5 phase engines.

    Attributes:
        phase_name: The phase identifier (``"S"``, ``"G"``, …).
        equation: The Constitutional equation for this phase.
        input_context: Adaptive context inherited from prior phases.
        output_artifacts: Symbols produced by this phase's decode run.
        corruption_log: Corruption codes detected during decoding.
        formation_trail: Ordered record of decoding steps for B'' reading.
    """

    phase_name: str = ""
    equation: str = ""

    def __init__(self) -> None:
        self.input_context: dict[str, Any] = {}
        self.output_artifacts: dict[str, Any] = {}
        self.corruption_log: list[str] = []
        self.formation_trail: list[dict[str, Any]] = []

    def _log_step(self, step: str, detail: Any) -> None:
        """Append an entry to the formation trail.

        Args:
            step: Human-readable step name.
            detail: Arbitrary data produced by the step.
        """
        self.formation_trail.append({"step": step, "detail": detail})

    @abstractmethod
    def decode(self, input_context: dict[str, Any], data_entity: Any) -> dict[str, Any]:
        """Execute symbol-by-symbol decoding for this phase.

        Args:
            input_context: Mutable context map from all prior phases.
            data_entity: The raw data being decoded.

        Returns:
            Dictionary of output artifacts produced by this phase.
        """
        ...

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(phase={self.phase_name!r})"


# ---------------------------------------------------------------------------
# S-phase engine  —  S = ∞0 → ? → X
# ---------------------------------------------------------------------------

class S_PhaseEngine(PhaseEngine):
    """S-phase: HOLD ∞0, RECEIVE →, NAME ?, VALIDATE X.

    Decoding steps:
        1. HOLD ∞0   — Inf0 from prior context (or None).
        2. RECEIVE → — Extract authentic question from *data_entity*.
        3. NAME ?    — Wrap in AuthenticQuestion.
        4. VALIDATE X — Produce ValidatedSpark.

    Output artifacts: ``{"X": X, "∞0": inf0}``

    Raises:
        L1_ClosingViolation: If *data_entity* is ``None`` (arrow skipped).
    """

    phase_name = "S"
    equation = EQUATIONS["S"]

    # -- internal helpers --------------------------------------------------

    def _receive_emergence(self, data_entity: Any) -> str:
        """Extract the authentic question from *data_entity*.

        Rules:
            * ``str``   — treat as the raw question directly.
            * ``dict``  — look for ``"question"`` then ``"text"`` key.
            * ``None``  — raise :class:`L1_ClosingViolation`.
            * other     — convert with ``str()``.

        Args:
            data_entity: Raw inbound data.

        Returns:
            The extracted question string.

        Raises:
            L1_ClosingViolation: If *data_entity* is ``None``.
        """
        if data_entity is None:
            raise L1_ClosingViolation(
                "Arrow skipped — no emergence received (data_entity is None)"
            )
        if isinstance(data_entity, str):
            return data_entity
        if isinstance(data_entity, dict):
            for key in ("question", "text"):
                if key in data_entity:
                    val = data_entity[key]
                    return val if isinstance(val, str) else str(val)
            # dict present but no recognised key — stringify it
            return str(data_entity)
        return str(data_entity)

    # -- decode ------------------------------------------------------------

    def decode(
        self,
        input_context: dict[str, Any],
        data_entity: Any,
    ) -> dict[str, Any]:
        """Execute S-phase decoding."""
        self.input_context = dict(input_context)
        self.formation_trail = []
        self.corruption_log = []

        # 1. HOLD ∞0
        inf0 = Inf0(value=input_context.get("∞0'", None))
        inf0.provenance = "S-phase HOLD"
        self._log_step("HOLD ∞0", inf0)

        # 2. RECEIVE →
        question = self._receive_emergence(data_entity)
        self._log_step("RECEIVE →", question)

        # 3. NAME ?
        auth_q = AuthenticQuestion(value=question)
        auth_q.provenance = "S-phase NAME"
        self._log_step("NAME ?", auth_q)

        # 4. VALIDATE X
        X = ValidatedSpark(value=auth_q.value)
        X.provenance = "S-phase VALIDATE"
        X.validate()
        self._log_step("VALIDATE X", X)

        self.output_artifacts = {"X": X, "∞0": inf0}
        return self.output_artifacts


# ---------------------------------------------------------------------------
# G-phase engine  —  G = α ≡ {α'} → α + Y
# ---------------------------------------------------------------------------

class G_PhaseEngine(PhaseEngine):
    """G-phase: RECEIVE X, SEEK α, TEST ≡, FIND {α'}, VALIDATE Y.

    Decoding steps:
        1. RECEIVE X — Spark from S-phase context.
        2. SEEK α    — Extract irreducible core from *data_entity*.
        3. TEST ≡    — Verify α persists across transformations.
        4. FIND {α'} — Discover self-similar expressions.
        5. VALIDATE Y — Produce ValidatedPattern.

    Output artifacts: ``{"α": alpha, "Y": Y}``

    Raises:
        L2_GeneratingViolation: If TEST ≡ fails (α empty or changed).
    """

    phase_name = "G"
    equation = EQUATIONS["G"]

    # -- internal helpers --------------------------------------------------

    def _seek_alpha(self, X: ValidatedSpark, data_entity: Any) -> str:
        """Extract irreducible core (α) from *data_entity*.

        For strings: returns the first 10 characters as the core theme,
        or the full string if shorter.

        Args:
            X: The validated spark from S-phase.
            data_entity: Raw inbound data.

        Returns:
            The irreducible core string.
        """
        raw = str(data_entity) if data_entity is not None else str(X.value)
        return raw[:10] if len(raw) >= 10 else raw

    def _test_identity_preservation(
        self,
        alpha: CoreEssence,
        data_entity: Any,
    ) -> bool:
        """Check whether α persists across transformations.

        For now: validates that α is non-empty.

        Args:
            alpha: The core essence to test.
            data_entity: Raw inbound data (for future richer checks).

        Returns:
            ``True`` if α is preserved, ``False`` otherwise.
        """
        val = alpha.value
        return val is not None and str(val).strip() != ""

    def _find_echoes(self, alpha: CoreEssence, data_entity: Any) -> list[str]:
        """Find self-similar expressions ({α'}) of α within *data_entity*.

        For strings: returns all repeated substrings of length ≥ 2 found
        in *data_entity*.

        Args:
            alpha: The core essence whose echoes to seek.
            data_entity: Raw inbound data.

        Returns:
            List of self-similar substring expressions.
        """
        raw = str(data_entity) if data_entity is not None else ""
        if not raw:
            return []
        seen: set[str] = set()
        echoes: list[str] = []
        # Find all substrings of length 2..min(10, len(raw))
        max_len = min(10, len(raw))
        for length in range(2, max_len + 1):
            for start in range(len(raw) - length + 1):
                sub = raw[start:start + length]
                # Count occurrences
                if sub not in seen and raw.count(sub) > 1:
                    seen.add(sub)
                    echoes.append(sub)
        return echoes

    # -- decode ------------------------------------------------------------

    def decode(
        self,
        input_context: dict[str, Any],
        data_entity: Any,
    ) -> dict[str, Any]:
        """Execute G-phase decoding."""
        self.input_context = dict(input_context)
        self.formation_trail = []
        self.corruption_log = []

        # 1. RECEIVE X
        X = input_context.get("X")
        self._log_step("RECEIVE X", X)

        # 2. SEEK α
        alpha = CoreEssence(value=self._seek_alpha(X, data_entity))
        alpha.provenance = "G-phase SEEK"
        self._log_step("SEEK α", alpha)

        # 3. TEST ≡
        if not self._test_identity_preservation(alpha, data_entity):
            self.corruption_log.append("L2")
            raise L2_GeneratingViolation("α changed under transformation")
        self._log_step("TEST ≡", "passed")

        # 4. FIND {α'}
        alpha_set = SelfSimilarSet(value=self._find_echoes(alpha, data_entity))
        alpha_set.provenance = "G-phase FIND"
        self._log_step("FIND {α'}", alpha_set)

        # 5. VALIDATE Y
        Y = ValidatedPattern(value={"α": alpha, "{α'}": alpha_set})
        Y.provenance = "G-phase VALIDATE"
        Y.validate()
        self._log_step("VALIDATE Y", Y)

        self.output_artifacts = {"α": alpha, "Y": Y}
        return self.output_artifacts


# ---------------------------------------------------------------------------
# Q-phase engine  —  Q = φ ⋂ Ω → φ⋂Ω + Z
# ---------------------------------------------------------------------------

class Q_PhaseEngine(PhaseEngine):
    """Q-phase: RECEIVE X+α+Y, HOLD φ, HOLD Ω, WATCH ⋂, VALIDATE Z.

    Decoding steps:
        1. RECEIVE X + α + Y — from context.
        2. HOLD φ   — Direct perception (string repr of Y).
        3. HOLD Ω   — Universal potential (context size of data).
        4. WATCH ⋂  — Natural intersection of φ and Ω.
        5. VALIDATE Z — Produce ResonantKey.

    Output artifacts: ``{"φ": phi, "Ω": omega, "φ⋂Ω": ni, "Z": Z}``

    Raises:
        L4_PerformingViolation: If the intersection is forced (None).
    """

    phase_name = "Q"
    equation = EQUATIONS["Q"]

    # -- internal helpers --------------------------------------------------

    def _hold_phi(self, Y: ValidatedPattern) -> str:
        """Hold direct perception (φ) of *Y*.

        For now: returns the string representation of Y's value.

        Args:
            Y: The validated pattern from G-phase.

        Returns:
            The held φ value as a string.
        """
        return str(Y.value) if Y is not None else ""

    def _hold_omega(self, data_entity: Any) -> int:
        """Hold universal potential (Ω) from *data_entity*.

        For now: returns ``len(str(data_entity))`` as context size.

        Args:
            data_entity: Raw inbound data.

        Returns:
            The context-size integer.
        """
        return len(str(data_entity)) if data_entity is not None else 0

    def _watch_intersection(self, phi: str, omega: int) -> str | None:
        """Watch for the natural intersection (⋂) of φ and Ω.

        If both φ and omega are non-empty / positive, returns their
        conceptual intersection.  If either is empty, returns ``None``
        (no forced intersection).

        Args:
            phi: The held φ value (string).
            omega: The held Ω value (integer context size).

        Returns:
            A string describing the intersection, or ``None``.
        """
        if phi and omega > 0:
            return f"intersection_of_{len(phi)}_phi_and_{omega}_omega"
        return None

    # -- decode ------------------------------------------------------------

    def decode(
        self,
        input_context: dict[str, Any],
        data_entity: Any,
    ) -> dict[str, Any]:
        """Execute Q-phase decoding."""
        self.input_context = dict(input_context)
        self.formation_trail = []
        self.corruption_log = []

        # 1. RECEIVE X + α + Y
        X = input_context.get("X")
        alpha = input_context.get("α")
        Y = input_context.get("Y")
        self._log_step("RECEIVE X+α+Y", {"X": X, "α": alpha, "Y": Y})

        # 2. HOLD φ
        phi = SelfNature(value=self._hold_phi(Y))
        phi.provenance = "Q-phase HOLD φ"
        self._log_step("HOLD φ", phi)

        # 3. HOLD Ω
        omega = UniversalPotential(value=self._hold_omega(data_entity))
        omega.provenance = "Q-phase HOLD Ω"
        self._log_step("HOLD Ω", omega)

        # 4. WATCH FOR ⋂
        intersection = self._watch_intersection(phi.value, omega.value)
        if intersection is None:
            self.corruption_log.append("L4")
            raise L4_PerformingViolation("⋂ forced, not arrived")
        ni = NaturalIntersection(value=intersection)
        ni.provenance = "Q-phase WATCH ⋂"
        self._log_step("WATCH ⋂", ni)

        # 5. VALIDATE Z
        Z = ResonantKey(value=ni.value)
        Z.provenance = "Q-phase VALIDATE"
        Z.validate()
        self._log_step("VALIDATE Z", Z)

        self.output_artifacts = {"φ": phi, "Ω": omega, "φ⋂Ω": ni, "Z": Z}
        return self.output_artifacts


# ---------------------------------------------------------------------------
# P-phase engine  —  P = δE/δV → ∇ → ∇ + A
# ---------------------------------------------------------------------------

class P_PhaseEngine(PhaseEngine):
    """P-phase: RECEIVE X+α+Y+Z, MAP δE, MAP δV, COMPUTE, RECEIVE ∇, VALIDATE A.

    Decoding steps:
        1. RECEIVE X + α + Y + Z — from context.
        2. MAP δE  — Energy / friction mapping.
        3. MAP δV  — Value mapping.
        4. COMPUTE δE/δV — ratio with div-by-zero guard.
        5. RECEIVE → (reveals ∇) — gradient derivation.
        6. VALIDATE A — Produce Flow.

    Output artifacts:
        ``{"δE": delta_E, "δV": delta_V, "δE/δV": ratio, "∇": nabla, "A": A}``
    """

    phase_name = "P"
    equation = EQUATIONS["P"]

    # -- internal helpers --------------------------------------------------

    def _map_energy(self, data_entity: Any) -> int:
        """Map energy (δE) from *data_entity*.

        For strings: counts uppercase characters as "energy".

        Args:
            data_entity: Raw inbound data.

        Returns:
            Energy count (integer).
        """
        raw = str(data_entity) if data_entity is not None else ""
        return sum(1 for ch in raw if ch.isupper())

    def _map_value(self, data_entity: Any) -> int:
        """Map value (δV) from *data_entity*.

        For strings: counts vowels as "value".

        Args:
            data_entity: Raw inbound data.

        Returns:
            Value count (integer, ≥ 1 to avoid div-by-zero).
        """
        raw = str(data_entity) if data_entity is not None else ""
        count = sum(1 for ch in raw.lower() if ch in "aeiou")
        return max(count, 1)  # guard against div-by-zero

    def _reveal_gradient(self, ratio: float, data_entity: Any) -> float:
        """Reveal the natural gradient (∇) from the δE/δV ratio.

        The gradient is the ratio scaled by a context factor derived
        from *data_entity*.

        Args:
            ratio: The computed δE/δV ratio.
            data_entity: Raw inbound data.

        Returns:
            The gradient as a float.
        """
        raw = str(data_entity) if data_entity is not None else ""
        context_factor = len(raw) / 100.0 if raw else 1.0
        return ratio * context_factor

    # -- decode ------------------------------------------------------------

    def decode(
        self,
        input_context: dict[str, Any],
        data_entity: Any,
    ) -> dict[str, Any]:
        """Execute P-phase decoding."""
        self.input_context = dict(input_context)
        self.formation_trail = []
        self.corruption_log = []

        # 1. RECEIVE X + α + Y + Z
        received = {
            "X": input_context.get("X"),
            "α": input_context.get("α"),
            "Y": input_context.get("Y"),
            "Z": input_context.get("Z"),
        }
        self._log_step("RECEIVE X+α+Y+Z", received)

        # 2. MAP δE
        delta_E = EnergyDiff(value=self._map_energy(data_entity))
        delta_E.provenance = "P-phase MAP δE"
        self._log_step("MAP δE", delta_E)

        # 3. MAP δV
        delta_V = ValueDiff(value=self._map_value(data_entity))
        delta_V.provenance = "P-phase MAP δV"
        self._log_step("MAP δV", delta_V)

        # 4. COMPUTE δE/δV
        ratio = (
            delta_E.value / delta_V.value
            if delta_V.value
            else float("inf")
        )
        self._log_step("COMPUTE δE/δV", ratio)

        # 5. RECEIVE → (reveals ∇)
        gradient = self._reveal_gradient(ratio, data_entity)
        nabla = NaturalGradient(value=gradient)
        nabla.provenance = "P-phase REVEAL ∇"
        self._log_step("REVEAL ∇", nabla)

        # 6. VALIDATE A
        A = Flow(value=nabla.value)
        A.provenance = "P-phase VALIDATE"
        A.validate()
        self._log_step("VALIDATE A", A)

        self.output_artifacts = {
            "δE": delta_E,
            "δV": delta_V,
            "δE/δV": ratio,
            "∇": nabla,
            "A": A,
        }
        return self.output_artifacts


# ---------------------------------------------------------------------------
# V-phase engine  —  V = (L ∩ G → B'') → ∞0' → B + B'' + ∞0'
# ---------------------------------------------------------------------------

class V_PhaseEngine(PhaseEngine):
    """V-phase: NAME L, NAME G, FIND ∩, COMPOSE B'', NAME B, FORM ∞0'.

    Decoding steps:
        1. RECEIVE full trace — all prior context.
        2. NAME L   — Local actualization from *data_entity*.
        3. NAME G   — Global propagation from *data_entity*.
        4. FIND ∩   — Intersection of L and G.
        5. COMPOSE B'' — Two-pass fractal seed composition.
        6. NAME B   — Benefit from L + G.
        7. FORM ∞0' — Enriched return (must contain ``"?"``).

    Output artifacts:
        ``{"L": L, "G": G_vp, "L∩G": lg_intersection,
           "B''": Bpp, "B": B, "∞0'": inf0p}``

    Raises:
        VEmpty_IncompleteViolation: If ∞0' is missing or has no ``"?"``.
    """

    phase_name = "V"
    equation = EQUATIONS["V"]

    # -- internal helpers --------------------------------------------------

    def _name_local(self, data_entity: Any) -> str:
        """Name the local actualization (L).

        For strings: returns the first 20 characters.

        Args:
            data_entity: Raw inbound data.

        Returns:
            The local result string.
        """
        raw = str(data_entity) if data_entity is not None else ""
        return raw[:20] if raw else ""

    def _name_global(self, data_entity: Any) -> int:
        """Name the global propagation (G).

        For strings: returns total length as "reach".

        Args:
            data_entity: Raw inbound data.

        Returns:
            The global reach integer.
        """
        raw = str(data_entity) if data_entity is not None else ""
        return len(raw)

    def _find_lg_intersection(
        self,
        L: LocalActualization,
        G_vp: GlobalPropagation,
    ) -> str:
        """Find the intersection (L ∩ G) of local and global.

        For now: returns a conceptual intersection string.

        Args:
            L: Local actualization symbol.
            G_vp: Global propagation symbol.

        Returns:
            A string describing the L∩G intersection.
        """
        l_val = str(L.value) if L.value is not None else ""
        g_val = G_vp.value if G_vp.value is not None else 0
        return f"L_local_{len(l_val)}_intersects_G_global_{g_val}"

    def _compose_fractal_seed(
        self,
        context: dict[str, Any],
        intersection: str,
    ) -> dict[str, Any]:
        """Compose the fractal seed (B'') in two passes.

        Pass 1: Extract α thread, φ⋂Ω, and ∇ from *context*.
        Pass 2: Assemble an artifact dict that carries the full cycle.

        Args:
            context: The full adaptive context from all prior phases.
            intersection: The L∩G intersection string.

        Returns:
            Dictionary containing the holographic cycle artifact.
        """
        # Pass 1 — extract threads
        alpha = context.get("α")
        phi_cap_omega = context.get("φ⋂Ω")
        nabla = context.get("∇")

        alpha_value = alpha.value if alpha is not None else None
        phi_omega_value = phi_cap_omega.value if phi_cap_omega is not None else None
        nabla_value = nabla.value if nabla is not None else None

        # Pass 2 — compose artifact
        artifact: dict[str, Any] = {
            "α_thread": alpha_value,
            "φ⋂Ω_resonance": phi_omega_value,
            "∇_gradient": nabla_value,
            "L∩G": intersection,
            "cycle": "S → G → Q → P → V",
        }
        return artifact

    def _form_enriched_return(self, context: dict[str, Any]) -> str:
        """Form the enriched return (∞0').

        Must produce a string containing ``"?"`` (a question) to satisfy
        the completion rule ``"No V without ∞0'"``.

        Args:
            context: The full adaptive context.

        Returns:
            A question-bearing string for ∞0'.
        """
        # Try to derive a question from prior context
        auth_q = None
        X = context.get("X")
        if X is not None and hasattr(X, "value"):
            auth_q = X.value

        if auth_q:
            return f"Having explored '{auth_q}', what remains unseen?"
        return "What question does the cycle itself ask?"

    # -- decode ------------------------------------------------------------

    def decode(
        self,
        input_context: dict[str, Any],
        data_entity: Any,
    ) -> dict[str, Any]:
        """Execute V-phase decoding."""
        self.input_context = dict(input_context)
        self.formation_trail = []
        self.corruption_log = []

        # 1. RECEIVE full trace
        self._log_step("RECEIVE full trace", list(input_context.keys()))

        # 2. NAME L
        L = LocalActualization(value=self._name_local(data_entity))
        L.provenance = "V-phase NAME L"
        self._log_step("NAME L", L)

        # 3. NAME G
        G_vp = GlobalPropagation(value=self._name_global(data_entity))
        G_vp.provenance = "V-phase NAME G"
        self._log_step("NAME G", G_vp)

        # 4. FIND ∩
        lg_intersection = self._find_lg_intersection(L, G_vp)
        self._log_step("FIND L∩G", lg_intersection)

        # 5. COMPOSE B''
        bpp_value = self._compose_fractal_seed(input_context, lg_intersection)
        Bpp = FractalSeed(value=bpp_value)
        Bpp.provenance = "V-phase COMPOSE B''"
        self._log_step("COMPOSE B''", Bpp)

        # 6. NAME B
        B = Benefit(value={"fulfillment": L.value, "propagation": G_vp.value})
        B.provenance = "V-phase NAME B"
        self._log_step("NAME B", B)

        # 7. FORM ∞0'
        inf0p_value = self._form_enriched_return(input_context)
        inf0p = EnrichedReturn(value=inf0p_value)
        inf0p.provenance = "V-phase FORM ∞0'"
        self._log_step("FORM ∞0'", inf0p)

        if not inf0p.value or "?" not in str(inf0p.value):
            self.corruption_log.append("V∅")
            raise VEmpty_IncompleteViolation(
                "∞0' missing question — V∅ corruption"
            )

        self.output_artifacts = {
            "L": L,
            "G": G_vp,
            "L∩G": lg_intersection,
            "B''": Bpp,
            "B": B,
            "∞0'": inf0p,
        }
        return self.output_artifacts
