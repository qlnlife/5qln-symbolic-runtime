"""
5QLN Symbolic Runtime — Exception Hierarchy (Module 1)

All Constitutional Violations raised during Codex execution.
Each exception carries: message, phase, corruption_code, details.
"""

from __future__ import annotations

from typing import Any, Optional


class ConstitutionalViolation(Exception):
    """Base for all Codex violations. Carries corruption code if applicable.

    Attributes:
        message: Human-readable description of the violation.
        phase: The phase (S, G, Q, P, V) during which the violation was detected.
        corruption_code: The L1–L4 or V∅ code associated with this violation, if any.
        details: Additional structured data about the violation.
    """

    corruption_code: Optional[str] = None

    def __init__(
        self,
        message: str,
        phase: Optional[str] = None,
        corruption_code: Optional[str] = None,
        details: Optional[dict[str, Any]] = None,
    ) -> None:
        """Initialize a ConstitutionalViolation.

        Args:
            message: Human-readable description of the violation.
            phase: The phase (S, G, Q, P, V) during which the violation was detected.
            corruption_code: The L1–L4 or V∅ code associated with this violation, if any.
            details: Additional structured data about the violation.
        """
        super().__init__(message)
        self.message: str = message
        self.phase: Optional[str] = phase
        self.corruption_code: Optional[str] = corruption_code
        self.details: Optional[dict[str, Any]] = details


class L1_ClosingViolation(ConstitutionalViolation):
    """Arrow skipped; answer inserted where emergence should occur.

    Corruption code: L1
    """

    def __init__(
        self,
        message: str,
        phase: Optional[str] = None,
        corruption_code: Optional[str] = "L1",
        details: Optional[dict[str, Any]] = None,
    ) -> None:
        """Initialize an L1 Closing Violation.

        Args:
            message: Human-readable description of the violation.
            phase: The phase (S, G, Q, P, V) during which the violation was detected.
            corruption_code: Defaults to "L1".
            details: Additional structured data about the violation.
        """
        super().__init__(message, phase=phase, corruption_code=corruption_code, details=details)


class L2_GeneratingViolation(ConstitutionalViolation):
    """Output manufactured from K (known) instead of received from ∞0.

    Corruption code: L2
    """

    def __init__(
        self,
        message: str,
        phase: Optional[str] = None,
        corruption_code: Optional[str] = "L2",
        details: Optional[dict[str, Any]] = None,
    ) -> None:
        """Initialize an L2 Generating Violation.

        Args:
            message: Human-readable description of the violation.
            phase: The phase (S, G, Q, P, V) during which the violation was detected.
            corruption_code: Defaults to "L2".
            details: Additional structured data about the violation.
        """
        super().__init__(message, phase=phase, corruption_code=corruption_code, details=details)


class L3_ClaimingViolation(ConstitutionalViolation):
    """Claims direct access to ∞0. Performance mistaken for decoding.

    Corruption code: L3
    """

    def __init__(
        self,
        message: str,
        phase: Optional[str] = None,
        corruption_code: Optional[str] = "L3",
        details: Optional[dict[str, Any]] = None,
    ) -> None:
        """Initialize an L3 Claiming Violation.

        Args:
            message: Human-readable description of the violation.
            phase: The phase (S, G, Q, P, V) during which the violation was detected.
            corruption_code: Defaults to "L3".
            details: Additional structured data about the violation.
        """
        super().__init__(message, phase=phase, corruption_code=corruption_code, details=details)


class L4_PerformingViolation(ConstitutionalViolation):
    """Symbols used but operation empty. Form without substance.

    Corruption code: L4
    """

    def __init__(
        self,
        message: str,
        phase: Optional[str] = None,
        corruption_code: Optional[str] = "L4",
        details: Optional[dict[str, Any]] = None,
    ) -> None:
        """Initialize an L4 Performing Violation.

        Args:
            message: Human-readable description of the violation.
            phase: The phase (S, G, Q, P, V) during which the violation was detected.
            corruption_code: Defaults to "L4".
            details: Additional structured data about the violation.
        """
        super().__init__(message, phase=phase, corruption_code=corruption_code, details=details)


class VEmpty_IncompleteViolation(ConstitutionalViolation):
    """B'' formed without ∞0'. Cycle has no continuity.

    Corruption code: V∅
    """

    def __init__(
        self,
        message: str,
        phase: Optional[str] = "V",
        corruption_code: Optional[str] = "V∅",
        details: Optional[dict[str, Any]] = None,
    ) -> None:
        """Initialize a V∅ Incomplete Violation.

        Args:
            message: Human-readable description of the violation.
            phase: Defaults to "V" since this violation is specific to the V phase.
            corruption_code: Defaults to "V∅".
            details: Additional structured data about the violation.
        """
        super().__init__(message, phase=phase, corruption_code=corruption_code, details=details)


class SyntaxViolation(ConstitutionalViolation):
    """C1 syntax check failed."""

    def __init__(
        self,
        message: str,
        phase: Optional[str] = None,
        corruption_code: Optional[str] = None,
        details: Optional[dict[str, Any]] = None,
    ) -> None:
        """Initialize a Syntax Violation.

        Args:
            message: Human-readable description of the violation.
            phase: The phase (S, G, Q, P, V) during which the violation was detected.
            corruption_code: Optional corruption code.
            details: Additional structured data about the violation.
        """
        super().__init__(message, phase=phase, corruption_code=corruption_code, details=details)


class SemanticViolation(ConstitutionalViolation):
    """C1 semantic check failed."""

    def __init__(
        self,
        message: str,
        phase: Optional[str] = None,
        corruption_code: Optional[str] = None,
        details: Optional[dict[str, Any]] = None,
    ) -> None:
        """Initialize a Semantic Violation.

        Args:
            message: Human-readable description of the violation.
            phase: The phase (S, G, Q, P, V) during which the violation was detected.
            corruption_code: Optional corruption code.
            details: Additional structured data about the violation.
        """
        super().__init__(message, phase=phase, corruption_code=corruption_code, details=details)


class DriftViolation(ConstitutionalViolation):
    """C1 drift check failed — symbol renamed or equation paraphrased."""

    def __init__(
        self,
        message: str,
        phase: Optional[str] = None,
        corruption_code: Optional[str] = None,
        details: Optional[dict[str, Any]] = None,
    ) -> None:
        """Initialize a Drift Violation.

        Args:
            message: Human-readable description of the violation.
            phase: The phase (S, G, Q, P, V) during which the violation was detected.
            corruption_code: Optional corruption code.
            details: Additional structured data about the violation.
        """
        super().__init__(message, phase=phase, corruption_code=corruption_code, details=details)


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    _violation_classes = [
        L1_ClosingViolation,
        L2_GeneratingViolation,
        L3_ClaimingViolation,
        L4_PerformingViolation,
        VEmpty_IncompleteViolation,
        SyntaxViolation,
        SemanticViolation,
        DriftViolation,
    ]

    for _cls in _violation_classes:
        try:
            raise _cls(f"Test {_cls.__name__}", phase="S", details={"test": True})
        except ConstitutionalViolation as _exc:
            assert isinstance(_exc, _cls), f"{_exc} is not instance of {_cls}"
            assert hasattr(_exc, "message"), "missing message attr"
            assert hasattr(_exc, "phase"), "missing phase attr"
            assert hasattr(_exc, "corruption_code"), "missing corruption_code attr"
            assert hasattr(_exc, "details"), "missing details attr"
            print(f"  OK  {_cls.__name__}: {_exc.message} (phase={_exc.phase}, code={_exc.corruption_code})")

    print("\nAll 9 exception classes tested successfully.")
