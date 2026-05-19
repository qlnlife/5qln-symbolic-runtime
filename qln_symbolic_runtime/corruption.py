"""5QLN Symbolic Runtime — Corruption Detector (Module 6).

Detects L1-L4 and V∅ at every phase boundary.
Each check method returns a boolean indicating whether the specific
corruption was detected. Phase-specific aggregators collect codes and
raise ConstitutionalViolation on critical detections.

Import-only dependencies: exceptions, const, symbols.
"""

from __future__ import annotations

import importlib
from typing import Any, Optional

# The package name starts with a digit — must use importlib.
_exceptions = importlib.import_module("qln_symbolic_runtime.exceptions")
L1_ClosingViolation = _exceptions.L1_ClosingViolation
L2_GeneratingViolation = _exceptions.L2_GeneratingViolation
L3_ClaimingViolation = _exceptions.L3_ClaimingViolation
L4_PerformingViolation = _exceptions.L4_PerformingViolation
VEmpty_IncompleteViolation = _exceptions.VEmpty_IncompleteViolation
ConstitutionalViolation = _exceptions.ConstitutionalViolation

_const = importlib.import_module("qln_symbolic_runtime.const")
CORRUPTION_CODES = _const.CORRUPTION_CODES


class CorruptionDetector:
    """Detects L1-L4 and V∅ at every phase boundary.

    The detector runs all applicable corruption checks for a given phase
    and step. Individual ``check_*`` methods return booleans; the phase-level
    ``_check_*_corruptions`` methods collect detected codes and raise the
    corresponding :class:`ConstitutionalViolation` subclasses.
    """

    # ── Public API ─────────────────────────────────────────────────────────

    def check(
        self,
        phase: str,
        step: str,
        input_ctx: dict[str, Any],
        output: dict[str, Any],
        operation_log: list[Any],
    ) -> list[str]:
        """Run all applicable corruption checks for this phase/step.

        Args:
            phase: One of ``S``, ``G``, ``Q``, ``P``, ``V``.
            step: The current decoding step name (e.g. ``RECEIVE``, ``VALIDATE``).
            input_ctx: Adaptive context received from prior phases.
            output: Symbols produced by the current phase step.
            operation_log: Ordered log of operations performed so far.

        Returns:
            List of detected corruption-code strings (empty if clean).

        Raises:
            L1_ClosingViolation: On L1 detection (S-phase).
            L2_GeneratingViolation: On L2 detection (G-phase).
            L3_ClaimingViolation: On L3 detection (any phase).
            L4_PerformingViolation: On L4 detection (Q, P, V phases).
            VEmpty_IncompleteViolation: On V∅ detection (V-phase).
        """
        detected: list[str] = []

        if phase == "S":
            detected.extend(
                self._check_s_corruptions(step, input_ctx, output, operation_log)
            )
        elif phase == "G":
            detected.extend(
                self._check_g_corruptions(step, input_ctx, output, operation_log)
            )
        elif phase == "Q":
            detected.extend(
                self._check_q_corruptions(step, input_ctx, output, operation_log)
            )
        elif phase == "P":
            detected.extend(
                self._check_p_corruptions(step, input_ctx, output, operation_log)
            )
        elif phase == "V":
            detected.extend(
                self._check_v_corruptions(step, input_ctx, output, operation_log)
            )

        return detected

    # ── Individual Corruption Checks ───────────────────────────────────────

    def check_L1(
        self,
        phase: str,
        step: str,
        input_ctx: dict[str, Any],
        output: dict[str, Any],
        log: list[Any],
    ) -> bool:
        """L1 Closing: Was → skipped? Answer inserted where emergence should occur?

        Detects if output ``X`` was manufactured without going through the
        emergence protocol (``∞0'`` absent from input and no operations
        recorded in the log). L1 means the arrow from ``?`` to ``X`` was
        bypassed.
        """
        if output.get("X") and not input_ctx.get("∞0'") and not log:
            return True
        return False

    def check_L2(
        self,
        phase: str,
        step: str,
        input_ctx: dict[str, Any],
        output: dict[str, Any],
        log: list[Any],
    ) -> bool:
        """L2 Generating: Was output manufactured from K instead of received from ∞0?

        Detects if symbol values (especially ``α``) appear in output without
        a prior context chain (``X`` from S-phase must precede ``α`` in
        G-phase).
        """
        if phase == "G" and "α" in output:
            alpha = output["α"]
            alpha_value: Any = (
                alpha.value if hasattr(alpha, "value") else alpha
            )
            if alpha_value and not input_ctx.get("X"):
                return True
        return False

    def check_L3(
        self,
        phase: str,
        step: str,
        input_ctx: dict[str, Any],
        output: dict[str, Any],
        log: list[Any],
    ) -> bool:
        """L3 Claiming: Does anyone claim to decode ∞0 directly?

        Scans *operation_log* for entries that linguistically claim infinite
        access — a confusion of performance with decoding.
        """
        for entry in log:
            entry_str = str(entry).lower()
            if "infinite" in entry_str and "access" in entry_str:
                return True
        return False

    def check_L4(
        self,
        phase: str,
        step: str,
        input_ctx: dict[str, Any],
        output: dict[str, Any],
        log: list[Any],
    ) -> bool:
        """L4 Performing: Symbols used but operation empty?

        **Phase Q:** ``φ`` and ``Ω`` present in output but their natural
        intersection (``φ⋂Ω``) is missing — the symbols were held but never
        allowed to meet.

        **Phase P:** ``∇`` is present but the energy/value mapping
        (``δE``, ``δV``) that produced it is absent — form without substance.
        """
        if phase == "Q":
            phi = output.get("φ")
            omega = output.get("Ω")
            intersection = output.get("φ⋂Ω")
            if phi and omega and not intersection:
                return True

        if phase == "P":
            nabla = output.get("∇")
            delta_E = output.get("δE")
            delta_V = output.get("δV")
            if nabla and (not delta_E or not delta_V):
                return True

        return False

    def check_VEmpty(
        self,
        phase: str,
        step: str,
        input_ctx: dict[str, Any],
        output: dict[str, Any],
        log: list[Any],
    ) -> bool:
        """V∅ Incomplete: B'' formed without ∞0'?

        In V-phase, the FractalSeed (``B''``) must carry an enriched return
        (``∞0'``) that contains a question (``?``). If ``B''`` exists but
        ``∞0'`` is missing or lacks the question, the cycle has no continuity.
        """
        if phase == "V":
            bpp = output.get("B''")
            inf0p = output.get("∞0'")
            inf0p_value_str = ""
            if inf0p is not None:
                if hasattr(inf0p, "value"):
                    inf0p_value_str = str(inf0p.value) if inf0p.value is not None else ""
                else:
                    inf0p_value_str = str(inf0p)
            if bpp and (not inf0p or not inf0p_value_str or "?" not in inf0p_value_str):
                return True
        return False

    # ── Phase-level Aggregation ────────────────────────────────────────────

    def _check_s_corruptions(
        self,
        step: str,
        input_ctx: dict[str, Any],
        output: dict[str, Any],
        log: list[Any],
    ) -> list[str]:
        """Run all corruption checks applicable to S-phase."""
        detected: list[str] = []
        if self.check_L1("S", step, input_ctx, output, log):
            detected.append("L1")
            raise L1_ClosingViolation(
                f"S-phase step {step!r}: X manufactured without emergence — L1"
            )
        if self.check_L3("S", step, input_ctx, output, log):
            detected.append("L3")
            raise L3_ClaimingViolation(
                f"S-phase step {step!r}: claims direct infinite access — L3"
            )
        return detected

    def _check_g_corruptions(
        self,
        step: str,
        input_ctx: dict[str, Any],
        output: dict[str, Any],
        log: list[Any],
    ) -> list[str]:
        """Run all corruption checks applicable to G-phase."""
        detected: list[str] = []
        if self.check_L2("G", step, input_ctx, output, log):
            detected.append("L2")
            raise L2_GeneratingViolation(
                f"G-phase step {step!r}: α manufactured from K, not received from ∞0 — L2"
            )
        if self.check_L3("G", step, input_ctx, output, log):
            detected.append("L3")
            raise L3_ClaimingViolation(
                f"G-phase step {step!r}: claims direct infinite access — L3"
            )
        return detected

    def _check_q_corruptions(
        self,
        step: str,
        input_ctx: dict[str, Any],
        output: dict[str, Any],
        log: list[Any],
    ) -> list[str]:
        """Run all corruption checks applicable to Q-phase."""
        detected: list[str] = []
        if self.check_L4("Q", step, input_ctx, output, log):
            detected.append("L4")
            raise L4_PerformingViolation(
                f"Q-phase step {step!r}: φ and Ω present but ⋂ missing — L4"
            )
        if self.check_L3("Q", step, input_ctx, output, log):
            detected.append("L3")
            raise L3_ClaimingViolation(
                f"Q-phase step {step!r}: claims direct infinite access — L3"
            )
        return detected

    def _check_p_corruptions(
        self,
        step: str,
        input_ctx: dict[str, Any],
        output: dict[str, Any],
        log: list[Any],
    ) -> list[str]:
        """Run all corruption checks applicable to P-phase."""
        detected: list[str] = []
        if self.check_L4("P", step, input_ctx, output, log):
            detected.append("L4")
            raise L4_PerformingViolation(
                f"P-phase step {step!r}: ∇ present but δE/δV mapping missing — L4"
            )
        if self.check_L3("P", step, input_ctx, output, log):
            detected.append("L3")
            raise L3_ClaimingViolation(
                f"P-phase step {step!r}: claims direct infinite access — L3"
            )
        return detected

    def _check_v_corruptions(
        self,
        step: str,
        input_ctx: dict[str, Any],
        output: dict[str, Any],
        log: list[Any],
    ) -> list[str]:
        """Run all corruption checks applicable to V-phase."""
        detected: list[str] = []
        if self.check_VEmpty("V", step, input_ctx, output, log):
            detected.append("V∅")
            raise VEmpty_IncompleteViolation(
                f"V-phase step {step!r}: B'' without ∞0' — cycle has no continuity — V∅"
            )
        if self.check_L4("V", step, input_ctx, output, log):
            bpp = output.get("B''")
            intersection = output.get("L∩G")
            if bpp and not intersection:
                detected.append("L4")
                raise L4_PerformingViolation(
                    f"V-phase step {step!r}: B'' composed but L∩G missing — L4"
                )
        if self.check_L3("V", step, input_ctx, output, log):
            detected.append("L3")
            raise L3_ClaimingViolation(
                f"V-phase step {step!r}: claims direct infinite access — L3"
            )
        return detected
