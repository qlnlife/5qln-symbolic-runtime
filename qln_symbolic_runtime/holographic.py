"""
5QLN Symbolic Runtime — D1 Holographic Lens Matrix (holographic.py)

The 5×5 holographic matrix defined by:
    ``XY := X within Y, where X, Y ∈ {S, G, Q, P, V}``

Each of the 25 lens functions refines a host phase's output by applying
another phase's quality as a perceptual lens.  Lenses *examine* — they do
**not** replace the host phase's decoded output.

Lens qualities (from the Codex, Section 2.6):
    * S-lens → openness   : What is not yet known?
    * G-lens → pattern    : What structure repeats?
    * Q-lens → resonance  : Does it authentically connect?
    * P-lens → flow       : Where does energy naturally go?
    * V-lens → benefit    : What crystallized and carries forward?
"""

from __future__ import annotations

from typing import Any

from .const import EQUATIONS


# ---------------------------------------------------------------------------
# LensMatrix
# ---------------------------------------------------------------------------

class LensMatrix:
    """5×5 holographic matrix. 25 lens functions.

    Attributes:
        LENS_QUALITIES: Mapping from phase glyph to its perceptual quality.

    Example::

        lm = LensMatrix()
        result = lm.apply_lens("G", "Q", host_output, data_entity)
        # result["lens"]  == "GQ"
        # result["quality"] == "resonance"
    """

    LENS_QUALITIES: dict[str, str] = {
        "S": "openness",
        "G": "pattern",
        "Q": "resonance",
        "P": "flow",
        "V": "benefit",
    }

    # -- public API --------------------------------------------------------

    def apply_lens(
        self,
        host_phase: str,
        lens_phase: str,
        host_output: dict[str, Any],
        data_entity: Any,
    ) -> dict[str, Any]:
        """Apply *lens_phase*'s quality to refine *host_phase*'s output.

        The lens examines the host output through a different perceptual
        quality and returns **refinement metadata only** — the original
        ``host_output`` is never mutated or replaced.

        Args:
            host_phase: The phase whose output is being examined
                (one of ``S, G, Q, P, V``).
            lens_phase: The phase whose quality is used as the lens
                (one of ``S, G, Q, P, V``).
            host_output: The decoded output dictionary from *host_phase*.
            data_entity: The raw data entity being decoded.

        Returns:
            Dictionary with keys:
                * ``"lens"``        — e.g. ``"GQ"``
                * ``"quality"``     — the lens quality name
                * ``"question"``    — the lens question formed
                * ``"refinement"``  — the refinement result dict

        Raises:
            KeyError: If *host_phase* or *lens_phase* is not a valid
                phase glyph.
        """
        quality: str = self.LENS_QUALITIES[lens_phase]
        question: str = self._form_question(
            host_phase, lens_phase, host_output
        )
        refinement: dict[str, Any] = self._execute_lens(
            quality, question, host_output, data_entity
        )
        return {
            "lens": f"{host_phase}{lens_phase}",
            "quality": quality,
            "question": question,
            "refinement": refinement,
        }

    # -- internal helpers --------------------------------------------------

    def _form_question(
        self,
        host: str,
        lens: str,
        output: dict[str, Any],
    ) -> str:
        """Form the lens question per Section 2.6 of the Codex.

        Args:
            host: Host phase glyph.
            lens: Lens phase glyph.
            output: Host phase output (for future context-aware questions).

        Returns:
            The lens question string.
        """
        quality: str = self.LENS_QUALITIES[lens]
        host_eq: str = EQUATIONS.get(host, "")
        return (
            f"Decode {host} ({host_eq}) through {lens}-lens ({quality}): "
            f"what does {quality} reveal?"
        )

    def _execute_lens(
        self,
        quality: str,
        question: str,
        output: dict[str, Any],
        entity: Any,
    ) -> dict[str, Any]:
        """Execute the lens — return a refinement dict.

        This is the default implementation.  Future versions may
        specialise per quality (openness, pattern, resonance, flow,
        benefit) by dispatching to quality-specific handlers.

        Args:
            quality: The lens quality being applied.
            question: The lens question formed by ``_form_question``.
            output: The host phase output under examination.
            entity: The raw data entity.

        Returns:
            A dictionary describing the refinement.
        """
        return {
            "quality_applied": quality,
            "lens_question": question,
            "refinement": "examined",
        }
