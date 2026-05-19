"""
cycle.py — Full Cycle Runner (Module 8)

Executes complete S→G→Q→P→V cycles with full adaptive context chain.
Integrates: phases, holographic lensing, corruption detection, C1 compilation,
and attestation into a single operational pipeline.

Part of the 5QLN Symbolic Runtime.
"""

from typing import Any, Dict, List, Optional, Tuple

from qln_symbolic_runtime.phases import (
    PhaseEngine,
    S_PhaseEngine,
    G_PhaseEngine,
    Q_PhaseEngine,
    P_PhaseEngine,
    V_PhaseEngine,
)
from qln_symbolic_runtime.holographic import LensMatrix
from qln_symbolic_runtime.corruption import CorruptionDetector
from qln_symbolic_runtime.compiler import C1Compiler
from qln_symbolic_runtime.attestation import AttestationChain
from qln_symbolic_runtime.exceptions import (
    ConstitutionalViolation,
    VEmpty_IncompleteViolation,
)


class CycleRunner:
    """Executes complete S→G→Q→P→V cycles with full adaptive context chain.

    A CycleRunner orchestrates the five phase engines in strict constitutional
    order, maintaining adaptive context (the ∞0' carry) between phases and
    across batch runs.  It wires together:

    - **Phase engines** (S, G, Q, P, V) for symbol-by-symbol decoding
    - **LensMatrix** for holographic sub-phase refinement
    - **CorruptionDetector** for L1–L4 and V∅ runtime guards
    - **C1Compiler** for syntax, semantic, and drift validation
    - **AttestationChain** for SHA-256 provenance fingerprinting

    The context chain follows the invariant:
    ``S receives ∅ or ∞0' → G receives X → Q receives X+α+Y → P receives
    X+α+Y+Z → V receives full trace``.

    Attributes:
        engines: Mapping of phase name → :class:`PhaseEngine` instance.
        lens_matrix: Shared holographic lens matrix.
        corruption: Shared corruption detector.
        compiler: Shared C1 compiler.
        attestation: Shared attestation chain.
    """

    # Canonical phase order — fixed by the Constitutional Codex.
    PHASE_ORDER: List[str] = ["S", "G", "Q", "P", "V"]

    def __init__(self) -> None:
        """Initialise all engines and sub-systems."""
        self.engines: Dict[str, PhaseEngine] = {
            "S": S_PhaseEngine(),
            "G": G_PhaseEngine(),
            "Q": Q_PhaseEngine(),
            "P": P_PhaseEngine(),
            "V": V_PhaseEngine(),
        }
        self.lens_matrix: LensMatrix = LensMatrix()
        self.corruption: CorruptionDetector = CorruptionDetector()
        self.compiler: C1Compiler = C1Compiler()
        self.attestation: AttestationChain = AttestationChain()
        self._cycle_count: int = 0
        self._history: List[Dict[str, Any]] = []

    # ------------------------------------------------------------------ #
    # Single-cycle execution
    # ------------------------------------------------------------------ #

    def run_cycle(
        self,
        data_entity: Any,
        prior_inf0p: Any = None,
        lenses: Optional[List[Tuple[str, str]]] = None,
    ) -> Dict[str, Any]:
        """Run one complete S→G→Q→P→V cycle on *data_entity*.

        The method walks through the five phase engines in constitutional
        order.  At each boundary it:

        1. Records the input context.
        2. Calls ``engine.decode(context, data_entity)``.
        3. Catches any :class:`ConstitutionalViolation` and halts the
           pipeline, logging the violation detail.
        4. Runs the corruption detector.
        5. Updates the shared *context* dict with the phase output so
            the next phase receives the adaptive context chain.

        After all phases (or an early halt) the trace is:

        - Optionally refined by holographic lenses.
        - Compiled by the C1 compiler.
        - Fingerprinted by the attestation chain.

        Args:
            data_entity: The inquiry / data to decode.  May be any type.
            prior_inf0p: Enriched return (``∞0'``) from a previous cycle.
                When provided it is injected into the initial context so
                that the S-phase receives it as a seed.
            lenses: Optional list of ``(host_phase, lens_phase)`` tuples.
                Each requests a holographic lens refinement of *host_phase*
                through the quality of *lens_phase*.

        Returns:
            Full cycle trace dictionary containing per-phase I/O, corruption
            codes, compiled surface, attestation fingerprint, and metadata.
        """
        context: Dict[str, Any] = {}
        if prior_inf0p is not None:
            context["∞0'"] = prior_inf0p

        trace: Dict[str, Any] = {
            "_meta": {
                "cycle_number": self._cycle_count + 1,
                "data_entity": str(data_entity)[:200],
                "input_∞0'": str(prior_inf0p)[:200] if prior_inf0p is not None else None,
            }
        }

        for phase_name in self.PHASE_ORDER:
            engine = self.engines[phase_name]

            # Record the adaptive context *as seen* by this phase.
            phase_input = dict(context)

            try:
                output = engine.decode(context, data_entity)
            except ConstitutionalViolation as exc:
                trace[phase_name] = {
                    "input": phase_input,
                    "output": {},
                    "violation": {
                        "type": type(exc).__name__,
                        "message": str(exc),
                        "corruption_code": getattr(exc, "corruption_code", None),
                    },
                    "status": "VIOLATION",
                }
                break  # Halt pipeline — constitutional boundary reached.

            # ------------------------------------------------------------------
            # Corruption checks
            # ------------------------------------------------------------------
            try:
                corruption_codes = self.corruption.check(
                    phase_name, "all", phase_input, output, []
                )
            except Exception:  # pragma: no cover — defensive
                corruption_codes = []

            trace[phase_name] = {
                "input": {k: str(v)[:100] for k, v in phase_input.items()},
                "output": {k: str(v)[:200] for k, v in output.items()},
                "corruption_codes": corruption_codes,
                "equation": getattr(engine, "equation", ""),
                "status": "OK" if not corruption_codes else "CORRUPTION_DETECTED",
            }

            # Advance the adaptive context chain.
            context.update(output)

        # ------------------------------------------------------------------ #
        # Holographic lens refinement
        # ------------------------------------------------------------------ #
        if lenses:
            for host, lens in lenses:
                if host in trace and "output" in trace[host]:
                    refinement = self.lens_matrix.apply_lens(
                        host, lens, trace[host]["output"], data_entity
                    )
                    trace[f"{host}{lens}"] = refinement

        # ------------------------------------------------------------------ #
        # C1 Compilation
        # ------------------------------------------------------------------ #
        try:
            compiled = self.compiler.compile_surface(trace)
            trace["_compiled"] = compiled
        except Exception as exc:  # pragma: no cover
            trace["_compiled"] = {"error": str(exc), "overall": "ERROR"}

        # ------------------------------------------------------------------ #
        # Attestation fingerprint
        # ------------------------------------------------------------------ #
        try:
            fingerprint = self.attestation.attest(trace)
            trace["_attestation"] = fingerprint
        except Exception as exc:  # pragma: no cover
            trace["_attestation"] = {"error": str(exc)}

        self._cycle_count += 1
        self._history.append(trace)

        return trace

    # ------------------------------------------------------------------ #
    # Batch execution
    # ------------------------------------------------------------------ #

    def run_batch(
        self,
        entities: List[Any],
        batch_lenses: Optional[List[Tuple[str, str]]] = None,
    ) -> Dict[str, Any]:
        """Run cycles on *N* entities, carrying ∞0' between cycles.

        Each entity is decoded in order.  When a cycle completes
        successfully (V-phase status ``OK``), its ``∞0'`` output is
        extracted and passed as *prior_inf0p* to the next cycle,
        realising the constitutional completion rule
        ``No V without ∞0'``.

        Args:
            entities: Ordered list of data entities to decode.
            batch_lenses: Optional lens list applied to every cycle.

        Returns:
            Aggregated result dict with individual cycle traces, a
            corruption summary, and the final ``∞0'`` value.
        """
        results: List[Dict[str, Any]] = []
        current_inf0p: Any = None

        for entity in entities:
            trace = self.run_cycle(
                entity,
                prior_inf0p=current_inf0p,
                lenses=batch_lenses,
            )
            results.append(trace)

            # Carry ∞0' forward if V-phase completed cleanly.
            if "V" in trace and trace["V"].get("status") == "OK":
                v_out = trace.get("V", {}).get("output", {})
                inf0p_str = v_out.get("∞0'", "")
                current_inf0p = inf0p_str if inf0p_str else None

        return {
            "batch_size": len(entities),
            "cycles": results,
            "final_∞0'": current_inf0p,
            "corruption_summary": self._summarize_corruptions(results),
        }

    # ------------------------------------------------------------------ #
    # Helpers
    # ------------------------------------------------------------------ #

    def _summarize_corruptions(self, results: List[Dict[str, Any]]) -> Dict[str, int]:
        """Count corruption codes across all cycle results.

        Args:
            results: List of cycle trace dicts returned by :meth:`run_cycle`.

        Returns:
            Dict mapping each corruption code (``L1``, ``L2``, ``L3``,
            ``L4``, ``V∅``) plus a ``clean`` key to occurrence counts.
        """
        summary: Dict[str, int] = {"L1": 0, "L2": 0, "L3": 0, "L4": 0, "V∅": 0, "clean": 0}
        for result in results:
            for phase in self.PHASE_ORDER:
                if phase not in result:
                    continue
                codes = result[phase].get("corruption_codes", [])
                if not codes:
                    summary["clean"] += 1
                for code in codes:
                    if code in summary:
                        summary[code] += 1
        return summary
