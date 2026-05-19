"""
attestation.py — Provenance Fingerprinting (Module 9)

Provides SHA-256 based attestation of cycle traces, producing
verifiable fingerprints that chain across sequential cycles.

Part of the 5QLN Symbolic Runtime.
"""

from __future__ import annotations

import hashlib
import json
import time
from typing import Any, Dict, List, Optional


class AttestationChain:
    """Provenance fingerprinting for cycle traces.

    Each attestation produces a cryptographically-linked fingerprint
    that includes:

    - **trace_hash**: SHA-256 over the canonical cycle components.
    - **chain_hash**: SHA-256 over ``prior_hash || trace_hash``,
      cryptographically linking this cycle to the previous one.
    - **canonical_components**: The exact fields that entered the hash,
      enabling third-party verification.
    - **timestamp**: Wall-clock time at attestation (informational).
    - **codex_source** and **runtime_version**: Attribution metadata.

    The chain is append-only; once a hash is written it becomes the
    ``_prior_hash`` for the next attestation.  This creates a simple
    tamper-evident log of cycle execution.

    Attributes:
        _chain: Ordered list of every fingerprint produced.
        _prior_hash: The ``chain_hash`` of the most recent attestation,
            or 64 zeroes for the genesis attestation.
    """

    _GENESIS_HASH: str = "0" * 64

    def __init__(self) -> None:
        """Start a new attestation chain with the genesis hash."""
        self._chain: List[Dict[str, Any]] = []
        self._prior_hash: str = self._GENESIS_HASH

    # ------------------------------------------------------------------ #
    # Core API
    # ------------------------------------------------------------------ #

    def attest(self, cycle_trace: Dict[str, Any]) -> Dict[str, Any]:
        """Produce an attestation fingerprint for *cycle_trace*.

        The method:

        1. Extracts the *canonical* subset of the trace (the fields
           that are constitutionally significant).
        2. Serialises them deterministically (sorted keys JSON).
        3. Computes **trace_hash** = SHA-256(canonical).
        4. Computes **chain_hash** = SHA-256(``prior_hash:trace_hash``).
        5. Appends the fingerprint to the internal chain and advances
           ``_prior_hash``.

        Args:
            cycle_trace: Full trace dict returned by
                :meth:`CycleRunner.run_cycle`.

        Returns:
            Fingerprint dict with ``trace_hash``, ``chain_hash``,
            ``prior_hash``, ``timestamp``, ``canonical_components``,
            ``codex_source``, and ``runtime_version``.
        """
        canonical = self._extract_canonical(cycle_trace)

        # Deterministic serialisation for hash stability.
        canonical_str = json.dumps(canonical, sort_keys=True, separators=(",", ":"))
        trace_hash = hashlib.sha256(canonical_str.encode("utf-8")).hexdigest()

        # Chain hash links to prior attestation.
        chain_input = f"{self._prior_hash}:{trace_hash}"
        chain_hash = hashlib.sha256(chain_input.encode("utf-8")).hexdigest()

        fingerprint: Dict[str, Any] = {
            "trace_hash": trace_hash,
            "chain_hash": chain_hash,
            "prior_hash": self._prior_hash,
            "timestamp": time.time(),
            "canonical_components": canonical,
            "codex_source": "https://www.5qln.com/codex",
            "runtime_version": "1.0.0",
        }

        self._prior_hash = chain_hash
        self._chain.append(fingerprint)

        return fingerprint

    def verify(
        self,
        cycle_trace: Dict[str, Any],
        fingerprint: Dict[str, Any],
    ) -> bool:
        """Verify *cycle_trace* against its *fingerprint*.

        Re-computes the canonical hash from the raw trace and compares
        it to the ``trace_hash`` stored in the fingerprint.

        Args:
            cycle_trace: The original (or independently obtained) trace.
            fingerprint: Fingerprint dict previously returned by
                :meth:`attest`.

        Returns:
            ``True`` if the trace matches the fingerprint exactly;
            ``False`` otherwise.
        """
        canonical = self._extract_canonical(cycle_trace)
        canonical_str = json.dumps(canonical, sort_keys=True, separators=(",", ":"))
        computed_hash = hashlib.sha256(canonical_str.encode("utf-8")).hexdigest()
        return computed_hash == fingerprint.get("trace_hash")

    # ------------------------------------------------------------------ #
    # Introspection helpers
    # ------------------------------------------------------------------ #

    @property
    def chain_length(self) -> int:
        """Number of attestations produced so far."""
        return len(self._chain)

    @property
    def latest_hash(self) -> str:
        """The current prior hash (will be used for the next attestation)."""
        return self._prior_hash

    # ------------------------------------------------------------------ #
    # Internal
    # ------------------------------------------------------------------ #

    def _extract_canonical(self, trace: Dict[str, Any]) -> Dict[str, Any]:
        """Extract the constitutionally-significant fields for hashing.

        Only the following fields are considered canonical:

        - Which phases executed successfully.
        - The exact equation associated with each phase.
        - The overall compiled status.
        - The cycle number.

        Deliberately excluded: per-phase output values (too volatile),
        timestamps, full attestation blocks.

        Args:
            trace: Cycle trace dict.

        Returns:
            Dict suitable for deterministic JSON serialisation.
        """
        return {
            "phases_present": [
                p for p in ("S", "G", "Q", "P", "V") if p in trace
            ],
            "equations": {
                p: trace[p].get("equation", "")
                for p in ("S", "G", "Q", "P", "V")
                if p in trace
            },
            "compiled_status": trace.get("_compiled", {}).get("overall", "UNKNOWN"),
            "cycle_number": trace.get("_meta", {}).get("cycle_number", 0),
        }
