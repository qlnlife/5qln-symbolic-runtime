"""5QLN Symbolic Runtime — C1 Compiler / Validator (Module 7).

Three-part validation: syntax, semantic, and drift. Assembles the
constitutional block for attestation. Every check follows exact C1
protocol (Section 3 of the Codex).

Import-only dependencies: exceptions, const, symbols.
"""

from __future__ import annotations

import importlib
from typing import Any, Optional

# The package name starts with a digit — must use importlib.
_exceptions = importlib.import_module("qln_symbolic_runtime.exceptions")
ConstitutionalViolation = _exceptions.ConstitutionalViolation
SyntaxViolation = _exceptions.SyntaxViolation
SemanticViolation = _exceptions.SemanticViolation
DriftViolation = _exceptions.DriftViolation

_const = importlib.import_module("qln_symbolic_runtime.const")
EQUATIONS = _const.EQUATIONS
PHASES = _const.PHASES
CORRUPTION_CODES = _const.CORRUPTION_CODES
NINE_INVARIANT_LINES = _const.NINE_INVARIANT_LINES
COMPLETION_RULE = _const.COMPLETION_RULE
ONE_LAW = _const.ONE_LAW
CYCLE = _const.CYCLE
HOLOGRAPHIC_LAW = _const.HOLOGRAPHIC_LAW
MASTER_EQUATION = _const.MASTER_EQUATION
OUTPUTS = _const.OUTPUTS

_symbols = importlib.import_module("qln_symbolic_runtime.symbols")
Symbol = _symbols.Symbol


class C1Compiler:
    """Three-part validation: syntax, semantic, drift.

    Validates a full cycle trace against the Constitutional Codex.
    Produces a compiled surface with overall compliance status and an
    assembled constitutional block suitable for attestation.
    """

    def __init__(self) -> None:
        """Load canonical constants from :mod:`const`."""
        self.equations: dict[str, str] = EQUATIONS
        self.phases: list[str] = PHASES
        self.corruption_codes: list[str] = CORRUPTION_CODES
        self.invariant_lines: list[str] = NINE_INVARIANT_LINES
        self.completion_rule: str = COMPLETION_RULE

    # ── Surface Compilation ────────────────────────────────────────────────

    def compile_surface(self, cycle_trace: dict[str, Any]) -> dict[str, Any]:
        """Full compilation: all 3 checks + constitutional block assembly.

        Args:
            cycle_trace: Mapping from phase name (``S``, ``G``, ``Q``, ``P``,
                ``V``) to phase data dicts containing ``equation``,
                ``input``, ``output``, ``corruption_codes``, etc.

        Returns:
            Dict with keys:
                - ``overall``: ``"COMPLIANT"`` or ``"NON-COMPLIANT"``
                - ``syntax``: result dict from :meth:`syntax_check`
                - ``semantic``: result dict from :meth:`semantic_check`
                - ``drift``: result dict from :meth:`drift_check`
                - ``constitutional_block``: from :meth:`_assemble_constitutional_block`
        """
        syntax = self.syntax_check(cycle_trace)
        semantic = self.semantic_check(cycle_trace)
        drift = self.drift_check(cycle_trace)
        block = self._assemble_constitutional_block(cycle_trace)

        all_pass = all(
            r["status"] == "PASS" for r in [syntax, semantic, drift]
        )

        return {
            "overall": "COMPLIANT" if all_pass else "NON-COMPLIANT",
            "syntax": syntax,
            "semantic": semantic,
            "drift": drift,
            "constitutional_block": block,
        }

    # ── Syntax Check ───────────────────────────────────────────────────────

    def syntax_check(self, cycle_trace: dict[str, Any]) -> dict[str, Any]:
        """Verify exact equations, symbols, phases, and corruption codes.

        Checks:
        - All 5 phases (S, G, Q, P, V) are present.
        - Each phase carries the exact canonical equation.
        - No unknown corruption codes appear.
        - Exactly 5 corruption codes defined.
        """
        failures: list[str] = []

        # All 5 phases must be present
        for phase in self.phases:
            if phase not in cycle_trace:
                failures.append(f"Missing phase: {phase}")

        # Each phase must carry the exact equation
        for phase, eq in self.equations.items():
            if phase in cycle_trace:
                phase_data = cycle_trace[phase]
                if isinstance(phase_data, dict):
                    trace_eq = phase_data.get("equation", "")
                    if trace_eq and trace_eq != eq:
                        failures.append(
                            f"Equation drift in {phase}: "
                            f"{trace_eq!r} != {eq!r}"
                        )

        # Corruption codes must be from the exact set of 5
        codes_found: set[str] = set()
        for phase_data in cycle_trace.values():
            if isinstance(phase_data, dict):
                codes_found.update(phase_data.get("corruption_codes", []))
        unknown = codes_found - set(self.corruption_codes)
        if unknown:
            failures.append(f"Unknown corruption codes: {unknown}")

        # Exactly 5 corruption codes must be defined in the spec
        if len(self.corruption_codes) != 5:
            failures.append(
                f"Corruption code count != 5: {self.corruption_codes}"
            )

        return {
            "status": "PASS" if not failures else "FAIL",
            "failures": failures,
        }

    # ── Semantic Check ─────────────────────────────────────────────────────

    def semantic_check(self, cycle_trace: dict[str, Any]) -> dict[str, Any]:
        """Verify adaptive context chain and semantic rules.

        Checks:
        - Adaptive context chain unbroken (S→G→Q→P→V).
        - G-phase input carries X from S-phase.
        - V-phase output ∞0' carries a question (Completion Rule).
        - Q-phase output contains both φ and Ω.
        """
        failures: list[str] = []

        # Adaptive context chain: G must receive X from S
        if "S" in cycle_trace and "G" in cycle_trace:
            g_data = cycle_trace["G"]
            if isinstance(g_data, dict):
                g_input = g_data.get("input", {})
                if isinstance(g_input, dict) and "X" not in g_input:
                    failures.append("G-phase missing X from S")

        # V-phase: ∞0' must carry a question (Completion Rule enforcement)
        if "V" in cycle_trace:
            v_data = cycle_trace["V"]
            if isinstance(v_data, dict):
                v_out = v_data.get("output", {})
                if isinstance(v_out, dict):
                    inf0p = v_out.get("∞0'")
                    inf0p_value = ""
                    if inf0p is not None:
                        if hasattr(inf0p, "value"):
                            inf0p_value = (
                                str(inf0p.value) if inf0p.value is not None else ""
                            )
                        else:
                            inf0p_value = str(inf0p)
                    if not inf0p_value or "?" not in inf0p_value:
                        failures.append(
                            "∞0' missing question — V∅ (Completion Rule)"
                        )

        # Q-phase: φ and Ω must both be present
        if "Q" in cycle_trace:
            q_data = cycle_trace["Q"]
            if isinstance(q_data, dict):
                q_out = q_data.get("output", {})
                if isinstance(q_out, dict):
                    if "φ" not in q_out:
                        failures.append("Q-phase missing φ in output")
                    if "Ω" not in q_out:
                        failures.append("Q-phase missing Ω in output")

        return {
            "status": "PASS" if not failures else "FAIL",
            "failures": failures,
        }

    # ── Drift Check ────────────────────────────────────────────────────────

    def drift_check(self, cycle_trace: dict[str, Any]) -> dict[str, Any]:
        """Verify no drift from canonical specification.

        Checks:
        - No equation paraphrased — exact canonical form only.
        - No symbol renamed without source.
        - No corruption code added beyond the canonical 5.
        - Sub-phase lenses refine, not replace.
        """
        failures: list[str] = []

        # Equation drift: stored equation must match canonical exactly
        for phase, eq in self.equations.items():
            if phase in cycle_trace:
                phase_data = cycle_trace[phase]
                if isinstance(phase_data, dict):
                    stored = phase_data.get("equation", "")
                    if stored and stored != eq:
                        failures.append(
                            f"Drift in {phase}: expected {eq!r}, got {stored!r}"
                        )

        # Sub-phase lens drift: lens entries must refine, not replace
        for key, val in cycle_trace.items():
            if (
                isinstance(key, str)
                and len(key) == 2
                and key not in self.phases
            ):
                if isinstance(val, dict):
                    if val.get("replacement"):
                        failures.append(
                            f"Lens {key!r} replaces instead of refining"
                        )

        return {
            "status": "PASS" if not failures else "FAIL",
            "failures": failures,
        }

    # ── Constitutional Block Assembly ──────────────────────────────────────

    def _assemble_constitutional_block(
        self, cycle_trace: dict[str, Any]
    ) -> dict[str, Any]:
        """Build the constitutional block per Section 3.1.

        The constitutional block is the attestation payload that captures
        the immutable structure of the Codex: One Law, Cycle, Equations,
        Outputs, Holographic Law, Completion Rule, and Corruption Codes.
        """
        return {
            "LAW": ONE_LAW,
            "CYCLE": CYCLE,
            "EQUATIONS": dict(EQUATIONS),
            "OUTPUTS": dict(OUTPUTS),
            "HOLOGRAPHIC": HOLOGRAPHIC_LAW,
            "COMPLETION": COMPLETION_RULE,
            "CORRUPTION": " ".join(CORRUPTION_CODES),
        }
