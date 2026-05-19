# 5QLN Symbolic Runtime — SPEC.md
## Single Source of Truth for Implementation

### Architecture Overview

The 5QLN Symbolic Runtime is a Python package that executes the Constitutional Codex as operational code. Every symbol from L1 (the Language) becomes a runtime entity. Every decoding step from D1 (the Decoder) becomes an executable method. Every validation rule from C1 (the Compiler) becomes a runtime assertion.

```
5qln_symbolic_runtime/
  __init__.py              # Package entry, exports all public symbols
  symbols.py               # L1: All Codex symbols as runtime classes
  phases.py                # D1: 5 phase engines with symbol-by-symbol decoding
  holographic.py           # D1: 25 sub-phase lens matrix
  corruption.py            # D1: 5 corruption codes as runtime guards
  compiler.py              # C1: Syntax, semantic, drift validators
  cycle.py                 # D1+C1: Full cycle runner with context chain
  attestation.py           # C1: Provenance, fingerprinting, hash chain
  exceptions.py            # ConstitutionalViolation hierarchy
  const.py                 # Nine Invariant Lines and constants
  repl.py                  # Interactive REPL for live decoding
```

---

## Module 1: exceptions.py

```python
class ConstitutionalViolation(Exception):
    """Base for all Codex violations. Carries corruption code if applicable."""
    pass

class L1_ClosingViolation(ConstitutionalViolation):
    """Arrow skipped; answer inserted where emergence should occur."""
    pass

class L2_GeneratingViolation(ConstitutionalViolation):
    """Output manufactured from K (known) instead of received from ∞0."""
    pass

class L3_ClaimingViolation(ConstitutionalViolation):
    """Claims direct access to ∞0. Performance mistaken for decoding."""
    pass

class L4_PerformingViolation(ConstitutionalViolation):
    """Symbols used but operation empty. Form without substance."""
    pass

class VEmpty_IncompleteViolation(ConstitutionalViolation):
    """B'' formed without ∞0'. Cycle has no continuity."""
    pass

class SyntaxViolation(ConstitutionalViolation):
    """C1 syntax check failed."""
    pass

class SemanticViolation(ConstitutionalViolation):
    """C1 semantic check failed."""
    pass

class DriftViolation(ConstitutionalViolation):
    """C1 drift check failed — symbol renamed or equation paraphrased."""
    pass
```

---

## Module 2: const.py

Immutable constants from the Codex.

```python
ONE_LAW = "H = ∞0 | A = K"
CYCLE = "S → G → Q → P → V"
MASTER_EQUATION = "(H = ∞0 | A = K) × (S → G → Q → P → V) = B'' → ∞0'"
HOLOGRAPHIC_LAW = "XY := X within Y, where X, Y ∈ {S, G, Q, P, V}"
COMPLETION_RULE = "No V without ∞0'"

NINE_INVARIANT_LINES = [
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

PHASES = ["S", "G", "Q", "P", "V"]
CORRUPTION_CODES = ["L1", "L2", "L3", "L4", "V∅"]

EQUATIONS = {
    "S": "S = ∞0 → ?",
    "G": "G = α ≡ {α'}",
    "Q": "Q = φ ⋂ Ω",
    "P": "P = δE/δV → ∇",
    "V": "V = (L ∩ G → B'') → ∞0'",
}

OUTPUTS = {
    "S": "X",
    "G": "α + Y",
    "Q": "φ⋂Ω + Z",
    "P": "∇ + A",
    "V": "B + B'' + ∞0'",
}
```

---

## Module 3: symbols.py — L1 as Runtime Entities

Every symbol in Section 1.7 of the Codex is a class inheriting from `Symbol`.

### Base Class

```python
class Symbol:
    """Base for all 5QLN symbols. Every symbol has:
    - name: human-readable name
    - glyph: the Unicode/symbol representation
    - equation_context: which equation this symbol appears in
    - value: the runtime value (set during decoding)
    - provenance: which phase produced this value
    """
    name: str
    glyph: str
    equation_context: str
    value: Any = None
    provenance: str = ""
    validated: bool = False

    def resolve(self, context: str) -> "Symbol":
        """Context-dependent resolution (Section 1.9)."""
        ...

    def validate(self) -> bool:
        """Mark this symbol as validated in its phase."""
        ...
```

### Phase Symbols

```python
class Phase_S(Symbol):
    """Start phase. S = ∞0 → ?. Output: X"""
    name = "Start"
    glyph = "S"
    equation_context = "S = ∞0 → ?"
    steps = ["HOLD", "RECEIVE", "NAME", "VALIDATE"]

class Phase_G(Symbol):
    """Growth phase. G = α ≡ {α'}. Output: Y"""
    name = "Growth"
    glyph = "G"
    equation_context = "G = α ≡ {α'}"
    steps = ["RECEIVE", "SEEK", "TEST", "FIND", "VALIDATE"]

class Phase_Q(Symbol):
    """Quality phase. Q = φ ⋂ Ω. Output: Z"""
    name = "Quality"
    glyph = "Q"
    equation_context = "Q = φ ⋂ Ω"
    steps = ["RECEIVE", "HOLD_PHI", "HOLD_OMEGA", "WATCH", "VALIDATE"]

class Phase_P(Symbol):
    """Power phase. P = δE/δV → ∇. Output: A (Flow)"""
    name = "Power"
    glyph = "P"
    equation_context = "P = δE/δV → ∇"
    steps = ["RECEIVE", "MAP_DELTA_E", "MAP_DELTA_V", "COMPUTE", "REVEAL", "VALIDATE"]

class Phase_V(Symbol):
    """Value phase. V = (L ∩ G → B'') → ∞0'. Output: B + B'' + ∞0'"""
    name = "Value"
    glyph = "V"
    equation_context = "V = (L ∩ G → B'') → ∞0'"
    steps = ["RECEIVE", "NAME_L", "NAME_G", "FIND_INTERSECTION",
             "COMPOSE_BPP_PASS1", "COMPOSE_BPP_PASS2", "NAME_B", "FORM_INF0P"]
```

### Operational Symbols

```python
class Inf0(Symbol):
    """Infinite Zero — the membrane of infinite potential. H = ∞0 | A = K"""
    name = "Infinite Zero"
    glyph = "∞0"

class Human(Symbol):
    """Human — the infinite held in finite membrane."""
    name = "Human"
    glyph = "H"

class Artificial(Symbol):
    """Artificial — the domain of the known. Context-resolves (Section 1.9)."""
    name = "Artificial"
    glyph = "A"
    # In P → A, resolves to Flow

class Known(Symbol):
    """Known — K, the codified/constructed domain."""
    name = "Known"
    glyph = "K"

class AuthenticQuestion(Symbol):
    """? — the authentic question from open space."""
    name = "Authentic Question"
    glyph = "?"

class ValidatedSpark(Symbol):
    """X — confirmed output of S-phase."""
    name = "Validated Spark"
    glyph = "X"

class CoreEssence(Symbol):
    """α — irreducible pattern within X."""
    name = "Core Essence"
    glyph = "α"

class SelfSimilarSet(Symbol):
    """{α'} — self-similar expressions of α across scales."""
    name = "Self-Similar Expressions"
    glyph = "{α'}"

class ValidatedPattern(Symbol):
    """Y — confirmed output of G-phase."""
    name = "Validated Pattern"
    glyph = "Y"

class SelfNature(Symbol):
    """φ — direct perception of Y by the inquirer."""
    name = "Self-Nature"
    glyph = "φ"

class UniversalPotential(Symbol):
    """Ω — what larger context makes possible."""
    name = "Universal Potential"
    glyph = "Ω"

class NaturalIntersection(Symbol):
    """⋂ — where two elements meet without forcing."""
    name = "Natural Intersection"
    glyph = "⋂"

class ResonantKey(Symbol):
    """Z — confirmed output of Q-phase."""
    name = "Resonant Key"
    glyph = "Z"

class EnergyDiff(Symbol):
    """δE — energy differential, where energy goes."""
    name = "Energy Differential"
    glyph = "δE"

class ValueDiff(Symbol):
    """δV — value differential, where value appears."""
    name = "Value Differential"
    glyph = "δV"

class NaturalGradient(Symbol):
    """∇ — path of least resistance toward α."""
    name = "Natural Gradient"
    glyph = "∇"

class Flow(Symbol):
    """A (in P → A) — validated direction of natural movement."""
    name = "Flow"
    glyph = "A"

class LocalActualization(Symbol):
    """L — specific tangible immediate result."""
    name = "Local Actualization"
    glyph = "L"

class GlobalPropagation(Symbol):
    """G (in V) — what spreads beyond the local."""
    name = "Global Propagation"
    glyph = "G"

class Benefit(Symbol):
    """B — decoded output: fulfillment + propagation."""
    name = "Benefit"
    glyph = "B"

class FractalSeed(Symbol):
    """B'' — artifact containing the full cycle holographically."""
    name = "Fractal Seed"
    glyph = "B''"

class EnrichedReturn(Symbol):
    """∞0' — return to ∞0 deepened by the cycle's question."""
    name = "Enriched Return"
    glyph = "∞0'"
```

---

## Module 4: phases.py — D1 as Executable Decoding

Each phase is a class that executes its equation symbol-by-symbol.

```python
class PhaseEngine(ABC):
    """Abstract base for all 5 phase engines."""
    phase_name: str
    equation: str
    input_context: dict   # Adaptive context from prior phases
    output_artifacts: dict # What this phase produces
    corruption_log: list  # Any corruption detected
    formation_trail: list # Ordered record for B'' reading

    @abstractmethod
    def decode(self, input_context: dict, data_entity: Any) -> dict:
        """Execute symbol-by-symbol decoding. Return output artifacts."""
        ...

class S_PhaseEngine(PhaseEngine):
    """S = ∞0 → ? → X. 4 decoding steps."""

    def decode(self, input_context, data_entity):
        # Step 1: HOLD ∞0
        inf0 = Inf0(value=input_context.get("∞0'", None))
        # Step 2: RECEIVE → (emergence from data)
        question = self._receive_emergence(data_entity)
        # Step 3: NAME ?
        auth_q = AuthenticQuestion(value=question)
        # Step 4: VALIDATE X
        X = ValidatedSpark(value=auth_q.value)
        X.validate()
        return {"X": X, "∞0": inf0}

class G_PhaseEngine(PhaseEngine):
    """G = α ≡ {α'} → α + Y. 5 decoding steps."""

    def decode(self, input_context, data_entity):
        X = input_context["X"]
        # Step 2: SEEK α
        alpha = CoreEssence(value=self._seek_alpha(X, data_entity))
        # Step 3: TEST ≡
        if not self._test_identity_preservation(alpha, data_entity):
            raise L2_GeneratingViolation("α changed under transformation")
        # Step 4: FIND {α'}
        alpha_prime_set = SelfSimilarSet(value=self._find_echoes(alpha, data_entity))
        # Step 5: VALIDATE Y
        Y = ValidatedPattern(value={"α": alpha, "{α'}": alpha_prime_set})
        Y.validate()
        return {"α": alpha, "Y": Y}

class Q_PhaseEngine(PhaseEngine):
    """Q = φ ⋂ Ω → φ⋂Ω + Z. 5 decoding steps."""

    def decode(self, input_context, data_entity):
        X, alpha, Y = input_context["X"], input_context["α"], input_context["Y"]
        # Step 2: HOLD φ
        phi = SelfNature(value=self._hold_phi(Y))
        # Step 3: HOLD Ω
        omega = UniversalPotential(value=self._hold_omega(data_entity))
        # Step 4: WATCH FOR ⋂
        intersection = self._watch_intersection(phi, omega)
        if intersection is None:
            raise L4_PerformingViolation("⋂ forced, not arrived")
        ni = NaturalIntersection(value=intersection)
        # Step 5: VALIDATE Z
        Z = ResonantKey(value=ni.value)
        Z.validate()
        return {"φ": phi, "Ω": omega, "φ⋂Ω": ni, "Z": Z}

class P_PhaseEngine(PhaseEngine):
    """P = δE/δV → ∇ → ∇ + A. 6 decoding steps."""

    def decode(self, input_context, data_entity):
        # Step 2: MAP δE
        delta_E = EnergyDiff(value=self._map_energy(data_entity))
        # Step 3: MAP δV
        delta_V = ValueDiff(value=self._map_value(data_entity))
        # Step 4: COMPUTE δE/δV
        ratio = delta_E.value / delta_V.value if delta_V.value else float('inf')
        # Step 5: RECEIVE → (reveals ∇)
        nabla = NaturalGradient(value=self._reveal_gradient(ratio, data_entity))
        # Step 6: VALIDATE A
        A = Flow(value=nabla.value)
        A.validate()
        return {"δE": delta_E, "δV": delta_V, "δE/δV": ratio, "∇": nabla, "A": A}

class V_PhaseEngine(PhaseEngine):
    """V = (L ∩ G → B'') → ∞0' → B + B'' + ∞0'. 7 decoding steps."""

    def decode(self, input_context, data_entity):
        # Step 2: NAME L
        L = LocalActualization(value=self._name_local(data_entity))
        # Step 3: NAME G
        G_vp = GlobalPropagation(value=self._name_global(data_entity))
        # Step 4: FIND ∩
        intersection = self._find_lg_intersection(L, G_vp)
        # Step 5: COMPOSE B'' (Pass 1: Analysis, Pass 2: Composition)
        Bpp = FractalSeed(value=self._compose_fractal_seed(input_context, intersection))
        # Step 6: NAME B
        B = Benefit(value={"fulfillment": L.value, "propagation": G_vp.value})
        # Step 7: FORM ∞0'
        inf0p = EnrichedReturn(value=self._form_enriched_return(input_context))
        if not inf0p.value or "?" not in str(inf0p.value):
            raise VEmpty_IncompleteViolation("∞0' missing question — V∅ corruption")
        return {"L": L, "G": G_vp, "L∩G": intersection, "B''": Bpp, "B": B, "∞0'": inf0p}
```

---

## Module 5: holographic.py — 25 Lenses

```python
class LensMatrix:
    """5×5 holographic matrix. Each cell is a lens function that refines
    a host phase's output using another phase's quality."""

    LENS_QUALITIES = {
        "S": "openness",      # What is not yet known?
        "G": "pattern",       # What structure repeats?
        "Q": "resonance",     # Does it authentically connect?
        "P": "flow",          # Where does energy naturally go?
        "V": "benefit",       # What crystallized and carries forward?
    }

    def apply_lens(self, host_phase: str, lens_phase: str,
                   host_output: dict, data_entity: Any) -> dict:
        """Apply lens_phase's quality to refine host_phase's decoding.
        Returns refined metadata — does NOT replace host_output."""
        quality = self.LENS_QUALITIES[lens_phase]
        # Form lens question and apply
        lens_question = self._form_question(host_phase, lens_phase, host_output)
        refinement = self._execute_lens(quality, lens_question, host_output, data_entity)
        return {"lens": f"{host_phase}{lens_phase}", "quality": quality,
                "question": lens_question, "refinement": refinement}
```

---

## Module 6: corruption.py — Runtime Guards

```python
class CorruptionDetector:
    """Detects L1-L4 and V∅ at every phase boundary."""

    def check(self, phase: str, step: str, input_ctx: dict,
              output: dict, operation_log: list) -> None:
        """Run all applicable corruption checks for this phase/step.
        Raises ConstitutionalViolation on detection."""
        ...

    def check_L1(self, phase, step, input_ctx, output, log):
        """Closing: Was → skipped? Answer inserted where emergence should occur?"""
        ...

    def check_L2(self, phase, step, input_ctx, output, log):
        """Generating: Was output manufactured from K instead of received from ∞0?"""
        ...

    def check_L3(self, phase, step, input_ctx, output, log):
        """Claiming: Does anyone claim to decode ∞0 directly?"""
        ...

    def check_L4(self, phase, step, input_ctx, output, log):
        """Performing: Symbols used but operation empty?"""
        ...

    def check_VEmpty(self, phase, step, input_ctx, output, log):
        """Incomplete: B'' without ∞0'?"""
        ...
```

---

## Module 7: compiler.py — C1 Validation

```python
class C1Compiler:
    """Three-part validation: syntax, semantic, drift."""

    def syntax_check(self, cycle_trace: dict) -> dict:
        """Verify:
        - Every symbol resolves to symbol table
        - Every phase carries exact equation
        - All 5 phases present
        - All 25 sub-phases available
        - Exactly 5 corruption codes
        - No V without ∞0' enforceable
        - Constitutional block present
        """
        ...

    def semantic_check(self, cycle_trace: dict) -> dict:
        """Verify:
        - Adaptive context chain unbroken (S→G→Q→P→V)
        - B, B'', ∞0' are distinct
        - Sub-phase lenses refine, not replace
        - ∞0' carries a question
        """
        ...

    def drift_check(self, cycle_trace: dict) -> dict:
        """Verify:
        - No symbol renamed without source
        - No equation paraphrased — exact form only
        - No decoding step omitted or reordered
        - No corruption code added beyond 5
        - Adaptive context chain preserved
        """
        ...

    def compile_surface(self, cycle_trace: dict) -> dict:
        """Full compilation: all 3 checks + constitutional block assembly."""
        ...
```

---

## Module 8: cycle.py — Full Cycle Runner

```python
class CycleRunner:
    """Executes complete S→G→Q→P→V cycles with full context chain."""

    def __init__(self):
        self.engines = {
            "S": S_PhaseEngine(),
            "G": G_PhaseEngine(),
            "Q": Q_PhaseEngine(),
            "P": P_PhaseEngine(),
            "V": V_PhaseEngine(),
        }
        self.lens_matrix = LensMatrix()
        self.corruption = CorruptionDetector()
        self.compiler = C1Compiler()
        self.attestation = AttestationChain()

    def run_cycle(self, data_entity: Any, prior_inf0p: Any = None,
                  lenses: list = None) -> dict:
        """Run one complete cycle on a data entity.
        Returns full cycle trace with compiled surface."""
        context = {}
        if prior_inf0p:
            context["∞0'"] = prior_inf0p

        trace = {}
        for phase_name in ["S", "G", "Q", "P", "V"]:
            engine = self.engines[phase_name]
            output = engine.decode(context, data_entity)
            self.corruption.check(phase_name, "all", context, output, [])
            context.update(output)
            trace[phase_name] = {"input": dict(context), "output": output}

        # Apply lenses if requested
        if lenses:
            for host, lens in lenses:
                refinement = self.lens_matrix.apply_lens(host, lens, trace[host]["output"], data_entity)
                trace[f"{host}{lens}"] = refinement

        # Compile
        compiled = self.compiler.compile_surface(trace)
        trace["_compiled"] = compiled

        # Attest
        fingerprint = self.attestation.attest(trace)
        trace["_attestation"] = fingerprint

        return trace

    def run_batch(self, entities: list, batch_lenses: list = None) -> dict:
        """Run cycles on N entities. Carry ∞0' between cycles."""
        ...
```

---

## Module 9: attestation.py

```python
class AttestationChain:
    """Provenance fingerprinting for cycle traces."""

    def attest(self, cycle_trace: dict) -> dict:
        """Produce attestation fingerprint for a cycle trace.
        Includes: hash of constitutional block, hash of decoding operations,
        hash of adaptive context chain, timestamp, prior fingerprint link."""
        ...

    def verify(self, cycle_trace: dict, fingerprint: dict) -> bool:
        """Verify a cycle trace against its attestation fingerprint."""
        ...
```

---

## Module 10: repl.py

Interactive REPL for live decoding sessions.

---

## Integration Rules

1. All modules use only symbols defined in `symbols.py` and `const.py`
2. All decoding operations follow exact D1 symbol-by-symbol steps (Sections 2.1-2.5)
3. All corruption checks use exact codes from Section 2.7
4. All compiler checks follow exact C1 protocol (Section 3)
5. Context chain is unbroken: S receives ∅ or ∞0', G receives X, Q receives X+α+Y, P receives X+α+Y+Z, V receives full trace
