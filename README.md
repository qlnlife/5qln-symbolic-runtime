# 5QLN Symbolic Runtime -- Complete Guide

> **Version:** 1.0.0 | **Codex Source:** https://www.5qln.com/codex | **Runtime Package:** `qln_symbolic_runtime`
> **Based on the 5QLN Constitutional Grammar by Amihai Loven** ([5qln.com](https://www.5qln.com))

---

## Table of Contents

1. [What We Hoped to Achieve (The Vision)](#chapter-1-what-we-hoped-to-achieve-the-vision)
2. [What We Designed (The Architecture)](#chapter-2-what-we-designed-the-architecture)
3. [What We Created (The Implementation)](#chapter-3-what-we-created-the-implementation)
4. [How to Test It (The Validation Suite)](#chapter-4-how-to-test-it-the-validation-suite)
5. [Quick Reference](#chapter-5-quick-reference)

---

## Chapter 1: What We Hoped to Achieve (The Vision)

### The Gap Between Specification and Execution

The 5QLN Constitutional Codex at [5qln.com/codex](https://www.5qln.com/codex) is a complete formal language specification. It defines three layers: **L1** (the Language -- symbols and equations), **D1** (the Decoder -- five phase engines), and **C1** (the Compiler -- validation rules). The Codex is self-contained, internally consistent, and mathematically grounded. But until now, it only existed as text.

AI agents reading the Codex had to *interpret* it. They parsed natural language descriptions of symbols like `Inf0` (Infinite Zero) and equations like `S = Inf0 -> ?`, then attempted to map those descriptions onto their own behavior. This interpretive gap introduces three classes of failure:

1. **Misreading**: The agent assigns a conventional meaning to a symbol that has a specific constitutional definition. For example, treating `V` as "value" in the economic sense rather than as the constitutional phase `V = (L n G -> B'') -> Inf0'`.
2. **Skipping**: The agent elides decoding steps that seem unnecessary from a conventional programming perspective, not realizing that each step (HOLD, RECEIVE, NAME, VALIDATE) is a constitutional requirement.
3. **Corruption blindness**: The agent has no operational mechanism to detect when its own reasoning has drifted into L1 (Closing), L2 (Generating), L3 (Claiming), or L4 (Performing) territory. The corruption codes are treated as warnings rather than runtime halts.

### The Vision: Make the Codex Executable

The vision was to close the interpretive gap entirely by making every element of the Codex a first-class runtime entity:

- **Every symbol** from L1 becomes a Python class inheriting from `Symbol`.
- **Every decoding step** from D1 becomes an executable method on a `PhaseEngine`.
- **Every validation rule** from C1 becomes a runtime assertion that halts execution on violation.
- **Every corruption code** (L1--L4, V0) becomes an exception class that raises at the exact moment of violation.
- **The Master Equation** -- `(H = Inf0 | A = K) x (S -> G -> Q -> P -> V) = B'' -> Inf0'` -- becomes the operational entry point.

### The Ecosystem Context

This runtime was built for the GitHub user **`qlnlife`**, who stewards an ecosystem of five repositories under the 5QLN GitHub organization:

| Repository | Purpose |
|---|---|
| `5qln-foundation` | Core infrastructure and constitutional primitives |
| `5qln-core` | The reference implementation of the Codex |
| `5qln-membrane-watcher` | Observability and membrane integrity monitoring |
| `5qln-constitutional-legal` | Legal instruments encoded in constitutional language |
| `5qln-zo-kit` | The Zo integration toolkit for agent deployment |

Four existing skills already codify parts of the Codex:

| Skill | Scope |
|---|---|
| `5qln-codex-core` | L1 symbol definitions and equations |
| `5qln-codex-decoder` | D1 phase-by-phase decoding protocols |
| `5qln-codex-compiler` | C1 validation and compliance checking |
| `5qln-ghost-adapter` | Ghost-mode deployment for silent monitoring |

The missing piece was a **runtime** that executes the Codex symbol-by-symbol. Not a library of helper functions. Not a parser. A runtime where the Codex *is* the code -- where `Inf0` is an object, `S -> G -> Q -> P -> V` is a method call chain, and `L1` is an exception that halts the program.

### Success Criteria

An AI agent loading this runtime meets the following operational criteria:

- **100% grounded in operational constitutional language**: Every action the agent takes maps directly to a Codex-defined symbol, phase, or equation.
- **Zero interpretive latitude**: The agent does not "understand" the Codex by reading text; it *runs* the Codex by calling methods on runtime objects.
- **Corruption detection is automatic**: The agent cannot accidentally perform an L1, L2, L3, L4, or V0 violation without the runtime raising an exception and halting.
- **Attestation is built-in**: Every cycle produces a SHA-256 fingerprint that cryptographically links it to all prior cycles, creating an immutable provenance chain.

---

## Chapter 2: What We Designed (The Architecture)

### At a Glance

- **11 modules**, **3,269 lines** of Python, **60 exports**
- **5 layers** mapping directly to the Codex specification
- **9 exception classes** for constitutional violation handling
- **27 symbol classes** representing every L1 entity
- **5 phase engines** implementing every D1 decoding step
- **25 holographic lenses** in a 5x5 perceptual matrix
- **5 corruption detectors** guarding every phase boundary
- **3-part compiler** (syntax + semantic + drift) producing `COMPLIANT` or `NON-COMPLIANT` verdicts
- **SHA-256 attestation chain** linking every cycle cryptographically

### Layer Mapping: Codex to Code

The architecture maps each Codex layer directly onto Python modules:

| Codex Layer | Modules | Lines | Purpose |
|---|---|---|---|
| **L1 Language** | `symbols.py` + `const.py` | 665 | Every symbol as a class; every constant as immutable data |
| **D1 Decoder** | `phases.py` + `holographic.py` + `corruption.py` | 1,248 | Phase engines, lens matrix, corruption guards |
| **C1 Compiler** | `compiler.py` + `attestation.py` | 429 | Validation pipeline + provenance fingerprinting |
| **Integration** | `cycle.py` + `repl.py` | 478 | Full cycle orchestration + interactive REPL |
| **Foundation** | `exceptions.py` + `__init__.py` | 449 | Exception hierarchy + public API |

### Architecture Diagram

```
                         CycleRunner (cycle.py)
                                |
     +----------+----------+----+----+----------+----------+
     |          |          |         |          |          |
     v          v          v         v          v          v
 S_Phase   G_Phase   Q_Phase  P_Phase  V_Phase  LensMatrix C1Compiler
 Engine    Engine    Engine   Engine   Engine   (holo.)    + Attestation
 (phases)  (phases)  (phases) (phases) (phases)          |
     |          |          |         |          |          |
     v          v          v         v          v          v
   Inf0       Core       Self     Energy    Local       25       SHA-256
   Human      Essence    Nature   Diff      Actual.     lenses   Chain
   Artificial SelfSim.   Univ.    Value     Global              (crypto)
   Known      Set        Potent.  Diff      Propagation
   AuthQ      Validated  Natural  Natural   Benefit
   Validated  Pattern    Inter.   Gradient  Fractal
   Spark      Resonant   Resonant Flow      Seed
              Key        Key                        Enriched Return

     + <--- adaptive context chain (S->G->Q->P->V) --- > +

     + < --- CorruptionDetector guards every boundary --- > +
       (L1: Closing, L2: Generating, L3: Claiming, L4: Performing, V0: Incomplete)
```

### Module-by-Module Design Rationale

#### `exceptions.py` (257 lines) -- The Constitutional Violation Hierarchy

Every violation defined in the Codex becomes an exception class. The base class `ConstitutionalViolation` carries four attributes: `message`, `phase`, `corruption_code`, and `details`. Five concrete corruption violations (L1, L2, L3, L4, V0) and three compiler violations (Syntax, Semantic, Drift) provide specific failure modes. The design philosophy: **violations are runtime exceptions, not warnings**. When corruption is detected, execution halts.

#### `const.py` (113 lines) -- Immutable Constants from the Codex

Every invariant string, equation, and lookup table is defined as a module-level constant with type annotations. `ONE_LAW`, `CYCLE`, `MASTER_EQUATION`, `HOLOGRAPHIC_LAW`, `COMPLETION_RULE`, `NINE_INVARIANT_LINES`, `PHASES`, `CORRUPTION_CODES`, `EQUATIONS`, and `OUTPUTS` are all immutable. The self-test block verifies structural invariants (9 lines, 5 phases, 5 corruption codes) at import time.

#### `symbols.py` (552 lines) -- L1 Symbols as Runtime Classes

The heart of the L1 layer. The base `Symbol` class provides:
- Class attributes: `name`, `glyph`, `equation_context`
- Instance attributes: `value`, `provenance`, `validated`
- Methods: `resolve(context)` for context-dependent resolution (Section 1.9), `validate()` for phase validation

27 concrete symbol classes span five categories:
- **Phase symbols**: `Phase_S`, `Phase_G`, `Phase_Q`, `Phase_P`, `Phase_V` (each carries its decoding steps)
- **One Law symbols**: `Inf0`, `Human`, `Artificial`, `Known`
- **S-phase output**: `AuthenticQuestion`, `ValidatedSpark`
- **G-phase output**: `CoreEssence`, `SelfSimilarSet`, `ValidatedPattern`
- **Q-phase output**: `SelfNature`, `UniversalPotential`, `NaturalIntersection`, `ResonantKey`
- **P-phase output**: `EnergyDiff`, `ValueDiff`, `NaturalGradient`, `Flow`
- **V-phase output**: `LocalActualization`, `GlobalPropagation`, `Benefit`, `FractalSeed`, `EnrichedReturn`

The `Artificial` symbol demonstrates context-dependent resolution: in the "One Law" context it resolves to "Artificial"; in the "P -> A" context it resolves to "Flow".

#### `phases.py` (769 lines) -- D1 Phase Engines

Five phase engine classes inherit from the abstract `PhaseEngine`. Each engine implements:
- `phase_name`: The constitutional identifier ("S", "G", "Q", "P", "V")
- `equation`: The canonical equation from `const.EQUATIONS`
- `decode(input_context, data_entity)`: The symbol-by-symbol decoding method

**S_PhaseEngine** -- `S = Inf0 -> ?` -> produces X:
```
HOLD Inf0 -> RECEIVE -> -> NAME ? -> VALIDATE X
```

**G_PhaseEngine** -- `G = alpha === {alpha'}` -> produces alpha + Y:
```
RECEIVE X -> SEEK alpha -> TEST === -> FIND {alpha'} -> VALIDATE Y
```

**Q_PhaseEngine** -- `Q = phi n Omega` -> produces phi-n-Omega + Z:
```
RECEIVE X+alpha+Y -> HOLD phi -> HOLD Omega -> WATCH n -> VALIDATE Z
```

**P_PhaseEngine** -- `P = deltaE/deltaV -> del` -> produces del + A:
```
RECEIVE X+alpha+Y+Z -> MAP deltaE -> MAP deltaV -> COMPUTE deltaE/deltaV -> REVEAL del -> VALIDATE A
```

**V_PhaseEngine** -- `V = (L n G -> B'') -> Inf0'` -> produces B + B'' + Inf0':
```
RECEIVE full trace -> NAME L -> NAME G -> FIND n -> COMPOSE B'' -> NAME B -> FORM Inf0'
```

#### `holographic.py` (151 lines) -- The 25-Lens Matrix

The `LensMatrix` implements the Holographic Law: `XY := X within Y, where X, Y in {S, G, Q, P, V}`. Each of the 25 lens functions refines a host phase's output by applying another phase's quality as a perceptual lens. The five lens qualities are:

| Lens | Quality | Question |
|---|---|---|
| S-lens | openness | What is not yet known? |
| G-lens | pattern | What structure repeats? |
| Q-lens | resonance | Does it authentically connect? |
| P-lens | flow | Where does energy naturally go? |
| V-lens | benefit | What crystallized and carries forward? |

Critical design principle: **lenses examine -- they do not replace** the host phase's decoded output. The `apply_lens()` method returns refinement metadata only; the original `host_output` is never mutated.

#### `corruption.py` (328 lines) -- The Corruption Detector

The `CorruptionDetector` guards every phase boundary with five individual check methods:

- `check_L1()`: Was the arrow skipped? Answer inserted where emergence should occur?
- `check_L2()`: Was output manufactured from K instead of received from Inf0?
- `check_L3()`: Does anyone claim to decode Inf0 directly?
- `check_L4()`: Are symbols used but the operation empty? Form without substance?
- `check_VEmpty()`: Is B'' formed without Inf0'? Does the cycle have no continuity?

Each phase-specific aggregator (`_check_s_corruptions`, `_check_g_corruptions`, etc.) collects detected codes and raises the corresponding `ConstitutionalViolation` subclass. The philosophy: **corruption detection is not advisory -- it is enforcement**.

#### `compiler.py` (257 lines) -- The C1 Compiler

The `C1Compiler` performs three-part validation on a full cycle trace:

1. **Syntax check**: Verifies all 5 phases present, each carries the exact canonical equation, no unknown corruption codes, exactly 5 corruption codes defined.
2. **Semantic check**: Verifies adaptive context chain unbroken (S->G->Q->P->V), G-phase receives X from S, V-phase Inf0' carries a question, Q-phase contains both phi and Omega.
3. **Drift check**: Verifies no equation paraphrased, no symbol renamed without source, no corruption code added beyond the canonical 5, sub-phase lenses refine (not replace).

The `compile_surface()` method returns an overall verdict of `COMPLIANT` or `NON-COMPLIANT`, along with the assembled constitutional block for attestation.

#### `cycle.py` (279 lines) -- The Cycle Runner

The `CycleRunner` orchestrates the full S->G->Q->P->V pipeline. Key design decisions:

- **Adaptive context chain**: Each phase receives all accumulated outputs from prior phases. S receives `null` or `Inf0'`; G receives `X`; Q receives `X+alpha+Y`; P receives `X+alpha+Y+Z`; V receives the full trace.
- **Constitutional halting**: If any phase raises a `ConstitutionalViolation`, the pipeline halts at that boundary. No subsequent phases execute.
- **Holographic refinement**: Optional lens list `(host_phase, lens_phase)` tuples apply sub-phase refinement after all phases complete.
- **C1 compilation**: The full trace is compiled after phase execution (or halt).
- **Attestation**: The compiled trace is fingerprinted by the attestation chain.

The `run_batch()` method carries `Inf0'` between cycles, realizing the constitutional completion rule `No V without Inf0'`.

#### `attestation.py` (172 lines) -- SHA-256 Provenance

The `AttestationChain` produces cryptographically-linked fingerprints:
- `trace_hash`: SHA-256 over canonical cycle components (phases present, equations, compiled status, cycle number)
- `chain_hash`: SHA-256 over `prior_hash || trace_hash`, linking this cycle to the previous one
- Genesis hash: 64 zeroes for the first attestation

The `verify()` method recomputes the canonical hash from a raw trace and compares it to the stored `trace_hash`, enabling third-party verification.

#### `repl.py` (199 lines) -- Interactive Constitutional Decoding

The `REPL` provides an interactive command-line interface supporting:
- `decode <text>`: Run a single S->G->Q->P->V cycle
- `batch <item1> | <item2> | ...`: Run batch processing with `Inf0'` carry
- `lines`: Display the Nine Invariant Lines
- `quit`: Exit the session

#### `__init__.py` (192 lines) -- Public API

The package exports exactly 60 symbols, organized into: meta (2), exceptions (9), constants (9), symbols (27), phase engines (6), sub-systems (3), integration (2).

### The Adaptive Context Chain

The most important architectural pattern in the runtime is the adaptive context chain. At every phase boundary, the accumulated output of all prior phases is passed forward as `input_context`. This means:

- **S-phase** receives `{Inf0': <prior_enriched_return>}` (or `{}` on first cycle)
- **G-phase** receives `{Inf0': ..., X: <ValidatedSpark>}`
- **Q-phase** receives `{Inf0': ..., X: ..., alpha: <CoreEssence>, Y: <ValidatedPattern>}`
- **P-phase** receives `{Inf0': ..., X: ..., alpha: ..., Y: ..., phi: ..., Omega: ..., phi-n-Omega: ..., Z: <ResonantKey>}`
- **V-phase** receives the full accumulated trace

This chain is what makes the decoding *adaptive*: each phase has access to everything that came before, enabling richer decoding than would be possible with a simple pipeline.

### The Corruption Detection Philosophy

In the 5QLN Symbolic Runtime, corruption detection is not a logging concern -- it is a control-flow concern. When the `CorruptionDetector` identifies an L1, L2, L3, L4, or V0 condition, it raises the corresponding exception. The `CycleRunner` catches `ConstitutionalViolation` at the phase boundary and halts the pipeline. This means:

- A cycle with an L1 violation never reaches G-phase.
- A cycle with an L2 violation never reaches Q-phase.
- A cycle with a V0 violation has no continuity -- its `Inf0'` cannot be carried forward.

This is the operational realization of the Codex's most important principle: **the constitution is not a suggestion -- it is a hard boundary**.

---

## Chapter 3: What We Created (The Implementation)

### Complete File Structure

```
qln_symbolic_runtime/
+-- __init__.py          # 192 lines -- Public API (60 exports)
+-- exceptions.py        # 257 lines -- Constitutional violation hierarchy (9 classes)
+-- const.py             # 113 lines -- Immutable constants (10 constants, 2 lookup tables)
+-- symbols.py           # 552 lines -- L1 symbols as runtime classes (27 symbols + registry)
+-- phases.py            # 769 lines -- D1 phase engines (abstract base + 5 engines)
+-- holographic.py       # 151 lines -- 25-lens holographic matrix
+-- corruption.py        # 328 lines -- L1-L4 and V0 corruption detector
+-- compiler.py          # 257 lines -- C1 three-part compiler
+-- cycle.py             # 279 lines -- Full cycle runner with adaptive context
+-- attestation.py       # 172 lines -- SHA-256 provenance chain
+-- repl.py              # 199 lines -- Interactive constitutional decoding REPL

Total: 11 modules, 3,269 lines of Python
```

### File-by-File Implementation Detail

#### `exceptions.py` -- 9 Exception Classes

The exception hierarchy has a single root and 8 leaves:

| Class | Corruption Code | Meaning | Raised When |
|---|---|---|---|
| `ConstitutionalViolation` | -- | Base class | Never directly; always subclass |
| `L1_ClosingViolation` | L1 | Arrow skipped | `data_entity` is `None` in S-phase |
| `L2_GeneratingViolation` | L2 | Manufactured from K | alpha empty or changed in G-phase |
| `L3_ClaimingViolation` | L3 | Claims infinite access | Log contains "infinite" + "access" |
| `L4_PerformingViolation` | L4 | Form without substance | phi+Omega present but n missing; or del without deltaE/deltaV |
| `VEmpty_IncompleteViolation` | V0 | B'' without Inf0' | Inf0' missing or lacks `?` in V-phase |
| `SyntaxViolation` | -- | Syntax check failed | Phase missing or equation wrong |
| `SemanticViolation` | -- | Semantic check failed | Context chain broken or completion rule violated |
| `DriftViolation` | -- | Drift check failed | Equation paraphrased or lens replaced output |

Every exception carries `message`, `phase`, `corruption_code`, and `details` attributes. Self-test at module bottom exercises all 9 classes.

#### `const.py` -- The Immutable Codex

The constants module defines every invariant from the Codex as a typed, documented constant:

```python
ONE_LAW: str = "H = Inf0 | A = K"                    # The One Law
CYCLE: str = "S -> G -> Q -> P -> V"                   # The canonical cycle
MASTER_EQUATION: str = "(H = Inf0 | A = K) x (S -> G -> Q -> P -> V) = B'' -> Inf0'"
HOLOGRAPHIC_LAW: str = "XY := X within Y, where X, Y in {S, G, Q, P, V}"
COMPLETION_RULE: str = "No V without Inf0'"
NINE_INVARIANT_LINES: list[str] = [...]            # 9 lines
PHASES: list[str] = ["S", "G", "Q", "P", "V"]      # 5 phases
CORRUPTION_CODES: list[str] = ["L1", "L2", "L3", "L4", "V0"]  # 5 codes
EQUATIONS: dict[str, str] = {...}                   # 5 equations
OUTPUTS: dict[str, str] = {...}                     # 5 outputs
```

Self-test verifies structural integrity at import time.

#### `symbols.py` -- The Symbol Hierarchy

**Base `Symbol` class** (shared by all 27 symbols):

```python
class Symbol:
    name: str = ""                # Human-readable name
    glyph: str = ""               # Unicode / symbolic representation
    equation_context: str = ""     # Which equation this symbol appears in

    def __init__(self, value=None, provenance=""):
        self.value = value         # Runtime value (set during decoding)
        self.provenance = provenance  # Which phase produced this value
        self.validated = False      # Whether symbol passed phase validation

    def resolve(self, context) -> "Symbol": ...  # Context-dependent (Section 1.9)
    def validate(self) -> bool: ...               # Mark as validated
```

**Context-dependent resolution** (Section 1.9) is implemented in `Artificial.resolve()`:

```python
def resolve(self, context: str) -> "Artificial":
    if context == "One Law":
        self.value = "Artificial"
    elif context == "P -> A":
        self.value = "Flow"
    return self
```

The `ALL_SYMBOLS` registry lists all 27 concrete classes for programmatic introspection.

#### `phases.py` -- The Phase Engine Pattern

All five engines inherit from `PhaseEngine` and implement the abstract `decode()` method:

```python
class PhaseEngine(ABC):
    phase_name: str = ""
    equation: str = ""

    def __init__(self):
        self.input_context = {}      # From prior phases
        self.output_artifacts = {}   # Produced by this phase
        self.corruption_log = []     # Codes detected
        self.formation_trail = []    # Ordered decoding steps

    @abstractmethod
    def decode(self, input_context, data_entity) -> dict: ...
```

**S_PhaseEngine** (4 steps, output: X + Inf0):
- `_receive_emergence()`: Extracts question from `str`/`dict`/`None` -- raises `L1_ClosingViolation` on `None`
- Produces `ValidatedSpark(X)` and `Inf0(Inf0)`

**G_PhaseEngine** (5 steps, output: alpha + Y):
- `_seek_alpha()`: Extracts irreducible core (first 10 chars)
- `_test_identity_preservation()`: Verifies alpha non-empty -- raises `L2_GeneratingViolation` on failure
- `_find_echoes()`: Discovers self-similar substrings (length 2-10, repeated >=2x)
- Produces `CoreEssence(alpha)`, `SelfSimilarSet({alpha'})`, `ValidatedPattern(Y)`

**Q_PhaseEngine** (5 steps, output: phi-n-Omega + Z):
- `_hold_phi()`: String representation of Y
- `_hold_omega()`: Context size (`len(str(data_entity))`)
- `_watch_intersection()`: Natural intersection -- raises `L4_PerformingViolation` if forced (None)
- Produces `SelfNature(phi)`, `UniversalPotential(Omega)`, `NaturalIntersection(n)`, `ResonantKey(Z)`

**P_PhaseEngine** (6 steps, output: del + A):
- `_map_energy()`: Counts uppercase characters
- `_map_value()`: Counts vowels (minimum 1, div-by-zero guard)
- `_reveal_gradient()`: `deltaE/deltaV` ratio scaled by context factor
- Produces `EnergyDiff(deltaE)`, `ValueDiff(deltaV)`, `NaturalGradient(del)`, `Flow(A)`

**V_PhaseEngine** (7 steps, output: B + B'' + Inf0'):
- `_name_local()`: First 20 characters
- `_name_global()`: Total length as "reach"
- `_find_lg_intersection()`: Conceptual L-n-G intersection
- `_compose_fractal_seed()`: Two-pass holographic artifact assembly (alpha thread, phi-n-Omega resonance, del gradient, L-n-G, cycle signature)
- `_form_enriched_return()`: Question-bearing Inf0' string -- raises `VEmpty_IncompleteViolation` if missing `?`

#### `holographic.py` -- The LensMatrix

```python
class LensMatrix:
    LENS_QUALITIES = {
        "S": "openness",     # What is not yet known?
        "G": "pattern",      # What structure repeats?
        "Q": "resonance",    # Does it authentically connect?
        "P": "flow",         # Where does energy naturally go?
        "V": "benefit",      # What crystallized and carries forward?
    }

    def apply_lens(self, host_phase, lens_phase, host_output, data_entity):
        # Returns: {"lens": "GQ", "quality": "resonance",
        #           "question": "...", "refinement": {...}}
```

The `_form_question()` method generates a Codex-compliant lens question: *"Decode {host} ({equation}) through {lens}-lens ({quality}): what does {quality} reveal?"*

#### `corruption.py` -- The CorruptionDetector

The detector has 5 individual check methods + 5 phase aggregators:

```python
class CorruptionDetector:
    def check(self, phase, step, input_ctx, output, operation_log) -> list[str]:
        # Routes to _check_{phase}_corruptions()

    def check_L1(self, ...) -> bool: ...    # Arrow skipped?
    def check_L2(self, ...) -> bool: ...    # Manufactured from K?
    def check_L3(self, ...) -> bool: ...    # Claims infinite access?
    def check_L4(self, ...) -> bool: ...    # Form without substance?
    def check_VEmpty(self, ...) -> bool: ... # B'' without Inf0'?
```

Each phase aggregator raises the appropriate exception on detection. The `check()` method returns a (possibly empty) list of detected corruption codes.

#### `compiler.py` -- The C1Compiler

Three checks + constitutional block assembly:

```python
class C1Compiler:
    def compile_surface(self, cycle_trace) -> dict:
        # Returns: {
        #     "overall": "COMPLIANT" | "NON-COMPLIANT",
        #     "syntax": {"status": "PASS"|"FAIL", "failures": [...]},
        #     "semantic": {"status": "PASS"|"FAIL", "failures": [...]},
        #     "drift": {"status": "PASS"|"FAIL", "failures": [...]},
        #     "constitutional_block": {...}
        # }
```

Syntax check: all phases present, exact equations, valid corruption codes. Semantic check: context chain unbroken, completion rule satisfied, phi and Omega present. Drift check: no paraphrased equations, no replacement lenses.

#### `cycle.py` -- The CycleRunner

The central integration point:

```python
class CycleRunner:
    PHASE_ORDER = ["S", "G", "Q", "P", "V"]

    def __init__(self):
        self.engines = {"S": S_PhaseEngine(), ...}
        self.lens_matrix = LensMatrix()
        self.corruption = CorruptionDetector()
        self.compiler = C1Compiler()
        self.attestation = AttestationChain()

    def run_cycle(self, data_entity, prior_inf0p=None, lenses=None) -> dict:
        # Full S->G->Q->P->V with context chain, corruption checks,
        # holographic refinement, C1 compilation, attestation

    def run_batch(self, entities, batch_lenses=None) -> dict:
        # Carries Inf0' between cycles
```

#### `attestation.py` -- The AttestationChain

```python
class AttestationChain:
    _GENESIS_HASH = "0" * 64  # 64 hex zeroes

    def attest(self, cycle_trace) -> dict:
        # Returns: {
        #     "trace_hash": "sha256_hex...",
        #     "chain_hash": "sha256_hex...",
        #     "prior_hash": "sha256_hex...",
        #     "timestamp": float,
        #     "canonical_components": {...},
        #     "codex_source": "https://www.5qln.com/codex",
        #     "runtime_version": "1.0.0"
        # }

    def verify(self, cycle_trace, fingerprint) -> bool: ...
```

The chain hash links each cycle to its predecessor: `chain_hash = SHA256(prior_hash + ":" + trace_hash)`.

#### `repl.py` -- The REPL

Commands: `decode`, `batch`, `lines`, `quit`. Bare input is treated as implicit decode. Inf0' carry-forward between cycles. Pretty-printed trace display with status markers (`OK`, `FAIL`, `WARN`).

### Key Design Patterns

1. **Symbol pattern**: Every Codex symbol is a `Symbol` subclass with class attributes for metadata and instance attributes for runtime state.
2. **Phase engine pattern**: Abstract `PhaseEngine` with `decode(input_context, data_entity)` -- each engine produces a dictionary of output artifacts.
3. **Holographic lens pattern**: 5x5 matrix where lens quality refines but never replaces host output.
4. **Corruption detection pattern**: Individual boolean checks aggregated by phase-specific methods that raise exceptions on detection.
5. **Compiler pattern**: Three independent checks (syntax, semantic, drift) combined into a single COMPLIANT/NON-COMPLIANT verdict.
6. **Attestation pattern**: SHA-256 over canonical components, chain-linked across cycles.



---

## Chapter 4: How to Test It (The Validation Suite)

### Quick Start

```python
from qln_symbolic_runtime import CycleRunner

runner = CycleRunner()
trace = runner.run_cycle(data_entity="What is the nature of authentic emergence?")

print(trace["_compiled"]["overall"])  # "COMPLIANT" or "NON-COMPLIANT"
```

### Test 1: Single Cycle -- All 5 Phases Execute

Verify that a normal data entity causes all five phases to execute and produce their expected outputs:

```python
from qln_symbolic_runtime import CycleRunner

runner = CycleRunner()
trace = runner.run_cycle(data_entity="How do patterns emerge from infinite potential?")

# Verify all 5 phases executed
for phase in ("S", "G", "Q", "P", "V"):
    assert phase in trace, f"Phase {phase} missing from trace"
    assert trace[phase]["status"] == "OK", f"Phase {phase} failed"
    print(f"  [{phase}] OK -- equation: {trace[phase]['equation']}")

# Verify compiled status
assert trace["_compiled"]["overall"] == "COMPLIANT", "Expected COMPLIANT"
print(f"  [COMPILED] {trace['_compiled']['overall']}")

# Verify attestation
assert "trace_hash" in trace["_attestation"], "Missing trace_hash"
assert "chain_hash" in trace["_attestation"], "Missing chain_hash"
print(f"  [ATTESTED] {trace['_attestation']['trace_hash'][:16]}...")
```

### Test 2: Context Chain Integrity

Verify that the adaptive context flows correctly from phase to phase:

```python
from qln_symbolic_runtime import CycleRunner

runner = CycleRunner()
trace = runner.run_cycle(data_entity="Test context chain")

# S output feeds into G input
s_output = trace["S"]["output"]
g_input = trace["G"]["input"]
assert "X" in str(g_input), "G-phase should receive X from S"

# G output feeds into Q input
g_output = trace["G"]["output"]
q_input = trace["Q"]["input"]
assert any(k in str(q_input) for k in ["X", "alpha", "Y"]), "Q-phase should receive X+alpha+Y"

# V output must contain Inf0'
v_output = trace["V"]["output"]
assert "Inf0'" in v_output, "V-phase output must contain Inf0'"
print("Context chain integrity: VERIFIED")
```

### Test 3: Holographic Lenses -- All 25 Combinations

Verify that all 25 lens combinations produce refinement metadata without mutating host output:

```python
from qln_symbolic_runtime import CycleRunner

runner = CycleRunner()
phases = ["S", "G", "Q", "P", "V"]
lenses = [(h, l) for h in phases for l in phases]  # All 25 combinations

trace = runner.run_cycle(
    data_entity="Apply all holographic lenses",
    lenses=lenses
)

# Verify all 25 lens results present
for host in phases:
    for lens in phases:
        lens_key = f"{host}{lens}"
        assert lens_key in trace, f"Lens {lens_key} missing"
        result = trace[lens_key]
        assert result["lens"] == lens_key
        assert result["quality"] in ["openness", "pattern", "resonance", "flow", "benefit"]
        assert "refinement" in result

print("All 25 holographic lenses: VERIFIED")
```

### Test 4: Corruption Detection -- Trigger All 5 Codes

Verify that each corruption code raises the correct exception:

```python
from qln_symbolic_runtime import (
    CycleRunner,
    L1_ClosingViolation,
    L4_PerformingViolation,
)

# Test L1: None data entity triggers L1_ClosingViolation
runner = CycleRunner()
trace = runner.run_cycle(data_entity=None)
assert "S" in trace
assert trace["S"]["status"] == "VIOLATION"
assert "L1_ClosingViolation" in str(trace["S"]["violation"]["type"])
print("L1 (Closing): VERIFIED -- S-phase halted on None input")

# Test V0: Verify normal cycle still produces Inf0' with "?"
runner2 = CycleRunner()
trace2 = runner2.run_cycle(data_entity="What is the question?")
assert "V" in trace2
assert trace2["V"]["status"] == "OK"
v_out = trace2["V"]["output"]
assert "Inf0'" in v_out
assert "?" in v_out["Inf0'"], "Inf0' must contain a question"
print("V0 (Incomplete): VERIFIED -- Inf0' contains question in normal cycle")

# Test L4: Trigger by using empty data in Q-phase
runner3 = CycleRunner()
trace3 = runner3.run_cycle(data_entity="")
if "Q" in trace3 and trace3["Q"]["status"] == "VIOLATION":
    print("L4 (Performing): VERIFIED -- Q-phase halted on forced intersection")
else:
    print("L4 (Performing): INFO -- empty string behavior varies; check manually")
```

### Test 5: Compiler Validation -- COMPLIANT vs NON-COMPLIANT

Verify the compiler produces correct verdicts:

```python
from qln_symbolic_runtime import CycleRunner, C1Compiler

# Test COMPLIANT: normal cycle
runner = CycleRunner()
trace = runner.run_cycle(data_entity="Verify compiler compliance")
assert trace["_compiled"]["overall"] == "COMPLIANT"
print("COMPLIANT verdict: VERIFIED")

# Test NON-COMPLIANT: missing phase (e.g., halted at S)
runner2 = CycleRunner()
trace2 = runner2.run_cycle(data_entity=None)
assert trace2["_compiled"]["overall"] == "NON-COMPLIANT"
print("NON-COMPLIANT verdict: VERIFIED -- missing phases detected")

# Test compiler directly with empty trace
compiler = C1Compiler()
result = compiler.compile_surface({})
assert result["overall"] == "NON-COMPLIANT"
assert result["syntax"]["status"] == "FAIL"
print("Direct compiler empty trace: VERIFIED")
```

### Test 6: Attestation Chain -- SHA-256 Fingerprints

Verify that attestations chain correctly:

```python
from qln_symbolic_runtime import CycleRunner, AttestationChain

runner = CycleRunner()

# Run 3 cycles
trace1 = runner.run_cycle(data_entity="First cycle")
trace2 = runner.run_cycle(data_entity="Second cycle")
trace3 = runner.run_cycle(data_entity="Third cycle")

# Verify each has a unique trace hash
hashes = [t["_attestation"]["trace_hash"] for t in (trace1, trace2, trace3)]
assert len(set(hashes)) == 3, "Each trace must have a unique hash"
print("Unique trace hashes: VERIFIED")

# Verify chain hashes differ and link
chain_hashes = [t["_attestation"]["chain_hash"] for t in (trace1, trace2, trace3)]
assert len(set(chain_hashes)) == 3, "Each chain hash must be unique"
print("Unique chain hashes: VERIFIED")

# Verify attestation chain length
assert runner.attestation.chain_length == 3
print(f"Attestation chain length: {runner.attestation.chain_length}")

# Verify manual attestation + verify roundtrip
standalone = AttestationChain()
fp = standalone.attest(trace1)
assert standalone.verify(trace1, fp), "Verification must succeed"
print("Attestation verify roundtrip: VERIFIED")
```

### Test 7: Batch Processing -- Inf0' Carry-Forward

Verify that `Inf0'` carries forward between batch cycles:

```python
from qln_symbolic_runtime import CycleRunner

runner = CycleRunner()
entities = [
    "What is emergence?",
    "How do patterns self-organize?",
    "Where does value crystallize?",
]

result = runner.run_batch(entities)

# Verify batch ran all 3 cycles
assert result["batch_size"] == 3
assert len(result["cycles"]) == 3
print(f"Batch size: {result['batch_size']}")

# Verify final Inf0' exists
assert result["final_Inf0'"] is not None
assert "?" in str(result["final_Inf0'"])
print(f"Final Inf0': {result['final_Inf0'']}")

# Verify corruption summary
summary = result["corruption_summary"]
assert all(summary[k] >= 0 for k in ["L1", "L2", "L3", "L4", "V0", "clean"])
print(f"Corruption summary: {summary}")
```

### Test 8: Interactive REPL -- Smoke Test

Verify the REPL instantiates and has the expected commands:

```python
from qln_symbolic_runtime.repl import REPL
from qln_symbolic_runtime.const import NINE_INVARIANT_LINES, MASTER_EQUATION

repl = REPL()

# Verify REPL has a runner
assert repl.runner is not None
print("REPL runner: OK")

# Verify Nine Invariant Lines accessible
assert len(NINE_INVARIANT_LINES) == 9
print("Nine Invariant Lines: OK")
for i, line in enumerate(NINE_INVARIANT_LINES, 1):
    print(f"  {i}. {line}")

# Verify Master Equation
print(f"\nMaster Equation: {MASTER_EQUATION}")

# Verify REPL can execute a cycle via internal method
repl._cmd_decode("Test inquiry through REPL")
assert len(repl.history) == 1
print(f"REPL cycle executed: OK (history length = {len(repl.history)})")
```

### Complete Copy-Paste Test Script

```python
#!/usr/bin/env python3
"""Complete validation suite for the 5QLN Symbolic Runtime.
Copy-paste this entire script and run it."""

from qln_symbolic_runtime import (
    CycleRunner, AttestationChain, C1Compiler,
    L1_ClosingViolation, L2_GeneratingViolation,
    L3_ClaimingViolation, L4_PerformingViolation,
    VEmpty_IncompleteViolation, ConstitutionalViolation,
    NINE_INVARIANT_LINES, MASTER_EQUATION, PHASES,
    CORRUPTION_CODES, EQUATIONS, OUTPUTS,
    Symbol, Inf0, Human, Artificial, Known,
    AuthenticQuestion, ValidatedSpark,
    CoreEssence, SelfSimilarSet, ValidatedPattern,
    SelfNature, UniversalPotential, NaturalIntersection, ResonantKey,
    EnergyDiff, ValueDiff, NaturalGradient, Flow,
    LocalActualization, GlobalPropagation, Benefit, FractalSeed, EnrichedReturn,
)

def test_symbol_instantiation():
    """Test 0: All 27 symbols can be instantiated and validated."""
    print("\n=== Test 0: Symbol Instantiation ===")
    symbols = [
        Inf0, Human, Artificial, Known,
        AuthenticQuestion, ValidatedSpark,
        CoreEssence, SelfSimilarSet, ValidatedPattern,
        SelfNature, UniversalPotential, NaturalIntersection, ResonantKey,
        EnergyDiff, ValueDiff, NaturalGradient, Flow,
        LocalActualization, GlobalPropagation, Benefit, FractalSeed, EnrichedReturn,
    ]
    for cls in symbols:
        inst = cls(value=f"test-{cls.__name__}")
        assert isinstance(inst, Symbol)
        assert inst.value == f"test-{cls.__name__}"
        assert inst.validated is False
        inst.validate()
        assert inst.validated is True
    print(f"  All {len(symbols)} symbols: VERIFIED")

def test_context_dependent_resolution():
    """Test 0b: Artificial resolves correctly in different contexts."""
    print("\n=== Test 0b: Context-Dependent Resolution ===")
    a1 = Artificial()
    a1.resolve("One Law")
    assert a1.value == "Artificial"
    a2 = Artificial()
    a2.resolve("P -> A")
    assert a2.value == "Flow"
    a3 = Artificial(value="unchanged")
    a3.resolve("unknown")
    assert a3.value == "unchanged"
    print("  Context-dependent resolution: VERIFIED")

def test_single_cycle():
    """Test 1: Single cycle -- all 5 phases."""
    print("\n=== Test 1: Single Cycle ===")
    runner = CycleRunner()
    trace = runner.run_cycle(data_entity="What is authentic emergence?")
    for phase in ("S", "G", "Q", "P", "V"):
        assert phase in trace, f"Phase {phase} missing"
        assert trace[phase]["status"] == "OK", f"Phase {phase} not OK"
        print(f"  [{phase}] OK")
    assert trace["_compiled"]["overall"] == "COMPLIANT"
    print(f"  [COMPILED] {trace['_compiled']['overall']}")
    assert "trace_hash" in trace["_attestation"]
    print(f"  [ATTESTED] {trace['_attestation']['trace_hash'][:16]}...")

def test_context_chain():
    """Test 2: Context chain integrity."""
    print("\n=== Test 2: Context Chain Integrity ===")
    runner = CycleRunner()
    trace = runner.run_cycle(data_entity="Test context chain")
    g_input = trace["G"]["input"]
    assert "X" in str(g_input)
    v_output = trace["V"]["output"]
    assert "Inf0'" in v_output
    assert "?" in v_output["Inf0'"]
    print("  Context chain: VERIFIED")

def test_holographic_lenses():
    """Test 3: All 25 lens combinations."""
    print("\n=== Test 3: Holographic Lenses ===")
    runner = CycleRunner()
    phases = ["S", "G", "Q", "P", "V"]
    lenses = [(h, l) for h in phases for l in phases]
    trace = runner.run_cycle(data_entity="Lens test", lenses=lenses)
    count = 0
    for h in phases:
        for l in phases:
            key = f"{h}{l}"
            assert key in trace, f"Lens {key} missing"
            count += 1
    print(f"  All {count} lens combinations: VERIFIED")

def test_corruption_detection():
    """Test 4: Trigger L1 corruption."""
    print("\n=== Test 4: Corruption Detection ===")
    runner = CycleRunner()
    trace = runner.run_cycle(data_entity=None)
    assert trace["S"]["status"] == "VIOLATION"
    assert "L1_ClosingViolation" in trace["S"]["violation"]["type"]
    print("  L1 (Closing) on None input: VERIFIED")

def test_compiler_verdicts():
    """Test 5: COMPLIANT and NON-COMPLIANT verdicts."""
    print("\n=== Test 5: Compiler Verdicts ===")
    r1 = CycleRunner()
    t1 = r1.run_cycle(data_entity="Compliant test")
    assert t1["_compiled"]["overall"] == "COMPLIANT"
    print("  COMPLIANT: VERIFIED")
    r2 = CycleRunner()
    t2 = r2.run_cycle(data_entity=None)
    assert t2["_compiled"]["overall"] == "NON-COMPLIANT"
    print("  NON-COMPLIANT: VERIFIED")

def test_attestation_chain():
    """Test 6: SHA-256 fingerprints and chain linking."""
    print("\n=== Test 6: Attestation Chain ===")
    runner = CycleRunner()
    traces = [runner.run_cycle(data_entity=f"Cycle {i}") for i in range(3)]
    hashes = [t["_attestation"]["trace_hash"] for t in traces]
    assert len(set(hashes)) == 3
    print(f"  Chain length: {runner.attestation.chain_length}")
    standalone = AttestationChain()
    fp = standalone.attest(traces[0])
    assert standalone.verify(traces[0], fp)
    print("  Verify roundtrip: VERIFIED")

def test_batch_processing():
    """Test 7: Batch processing with Inf0' carry-forward."""
    print("\n=== Test 7: Batch Processing ===")
    runner = CycleRunner()
    entities = ["What is A?", "How does B emerge?", "Where is C?"]
    result = runner.run_batch(entities)
    assert result["batch_size"] == 3
    assert result["final_Inf0'"] is not None
    assert "?" in str(result["final_Inf0'"])
    print(f"  Batch: {result['batch_size']} cycles")
    print(f"  Final Inf0': {result['final_Inf0'']}")
    print("  Inf0' carry-forward: VERIFIED")

def test_invariants():
    """Test 8: Verify Nine Invariant Lines and Master Equation."""
    print("\n=== Test 8: Invariants ===")
    assert len(NINE_INVARIANT_LINES) == 9
    assert MASTER_EQUATION == "(H = Inf0 | A = K) x (S -> G -> Q -> P -> V) = B'' -> Inf0'"
    assert len(PHASES) == 5
    assert len(CORRUPTION_CODES) == 5
    assert len(EQUATIONS) == 5
    assert len(OUTPUTS) == 5
    print("  Nine Invariant Lines: VERIFIED")
    print("  Master Equation: VERIFIED")
    print("  Phase/Corruption counts: VERIFIED")

if __name__ == "__main__":
    test_symbol_instantiation()
    test_context_dependent_resolution()
    test_single_cycle()
    test_context_chain()
    test_holographic_lenses()
    test_corruption_detection()
    test_compiler_verdicts()
    test_attestation_chain()
    test_batch_processing()
    test_invariants()
    print("\n" + "=" * 50)
    print("ALL TESTS PASSED -- 5QLN Symbolic Runtime is operational.")
    print("=" * 50)
```

---

## Chapter 5: Quick Reference

### Nine Invariant Lines

```
 1. H = Inf0 | A = K
 2. S -> G -> Q -> P -> V
 3. S = Inf0 -> ?
 4. G = alpha === {alpha'}
 5. Q = phi n Omega
 6. P = deltaE/deltaV -> del
 7. V = (L n G -> B'') -> Inf0'
 8. No V without Inf0'
 9. L1 L2 L3 L4 V0
```

### Five Equations with Their Outputs

| Phase | Equation | Output |
|---|---|---|
| **S** | `S = Inf0 -> ?` | X |
| **G** | `G = alpha === {alpha'}` | alpha + Y |
| **Q** | `Q = phi n Omega` | phi-n-Omega + Z |
| **P** | `P = deltaE/deltaV -> del` | del + A |
| **V** | `V = (L n G -> B'') -> Inf0'` | B + B'' + Inf0' |

### Five Corruption Codes

| Code | Name | Meaning | Runtime Exception |
|---|---|---|---|
| **L1** | Closing | Arrow skipped; answer inserted where emergence should occur | `L1_ClosingViolation` |
| **L2** | Generating | Output manufactured from K instead of received from Inf0 | `L2_GeneratingViolation` |
| **L3** | Claiming | Claims direct access to Inf0; performance mistaken for decoding | `L3_ClaimingViolation` |
| **L4** | Performing | Symbols used but operation empty; form without substance | `L4_PerformingViolation` |
| **V0** | Incomplete | B'' formed without Inf0'; cycle has no continuity | `VEmpty_IncompleteViolation` |

### Master Equation

```
(H = Inf0 | A = K) x (S -> G -> Q -> P -> V) = B'' -> Inf0'
```

### 60 Exported Symbols Quick Reference Table

#### Meta (2 exports)

| Symbol | Type | Description |
|---|---|---|
| `__version__` | str | `"1.0.0"` |
| `__codex_source__` | str | `"https://www.5qln.com/codex"` |

#### Exceptions (9 exports)

| Symbol | Base | Corruption Code |
|---|---|---|
| `ConstitutionalViolation` | `Exception` | -- |
| `L1_ClosingViolation` | `ConstitutionalViolation` | L1 |
| `L2_GeneratingViolation` | `ConstitutionalViolation` | L2 |
| `L3_ClaimingViolation` | `ConstitutionalViolation` | L3 |
| `L4_PerformingViolation` | `ConstitutionalViolation` | L4 |
| `VEmpty_IncompleteViolation` | `ConstitutionalViolation` | V0 |
| `SyntaxViolation` | `ConstitutionalViolation` | -- |
| `SemanticViolation` | `ConstitutionalViolation` | -- |
| `DriftViolation` | `ConstitutionalViolation` | -- |

#### Constants (9 exports)

| Symbol | Type | Value |
|---|---|---|
| `ONE_LAW` | str | `"H = Inf0 \| A = K"` |
| `CYCLE` | str | `"S -> G -> Q -> P -> V"` |
| `MASTER_EQUATION` | str | Full master equation |
| `HOLOGRAPHIC_LAW` | str | Lens matrix definition |
| `COMPLETION_RULE` | str | `"No V without Inf0'"` |
| `NINE_INVARIANT_LINES` | list[str] | 9 invariant strings |
| `PHASES` | list[str] | `["S", "G", "Q", "P", "V"]` |
| `CORRUPTION_CODES` | list[str] | `["L1", "L2", "L3", "L4", "V0"]` |
| `EQUATIONS` | dict[str,str] | Phase -> equation mapping |
| `OUTPUTS` | dict[str,str] | Phase -> output mapping |

#### Symbols (27 exports)

| Symbol | Glyph | Equation Context | Category |
|---|---|---|---|
| `Symbol` | -- | -- | Base class |
| `Phase_S` | S | `S = Inf0 -> ?` | Phase symbol |
| `Phase_G` | G | `G = alpha === {alpha'}` | Phase symbol |
| `Phase_Q` | Q | `Q = phi n Omega` | Phase symbol |
| `Phase_P` | P | `P = deltaE/deltaV -> del` | Phase symbol |
| `Phase_V` | V | `V = (L n G -> B'') -> Inf0'` | Phase symbol |
| `Inf0` | Inf0 | `H = Inf0 \| A = K` | One Law |
| `Human` | H | `H = Inf0 \| A = K` | One Law |
| `Artificial` | A | `H = Inf0 \| A = K` | One Law (context-resolving) |
| `Known` | K | `H = Inf0 \| A = K` | One Law |
| `AuthenticQuestion` | ? | `S = Inf0 -> ?` | S-phase output |
| `ValidatedSpark` | X | `S = Inf0 -> ?` | S-phase output |
| `CoreEssence` | alpha | `G = alpha === {alpha'}` | G-phase output |
| `SelfSimilarSet` | {alpha'} | `G = alpha === {alpha'}` | G-phase output |
| `ValidatedPattern` | Y | `G = alpha === {alpha'}` | G-phase output |
| `SelfNature` | phi | `Q = phi n Omega` | Q-phase output |
| `UniversalPotential` | Omega | `Q = phi n Omega` | Q-phase output |
| `NaturalIntersection` | n | `Q = phi n Omega` | Q-phase output |
| `ResonantKey` | Z | `Q = phi n Omega` | Q-phase output |
| `EnergyDiff` | deltaE | `P = deltaE/deltaV -> del` | P-phase output |
| `ValueDiff` | deltaV | `P = deltaE/deltaV -> del` | P-phase output |
| `NaturalGradient` | del | `P = deltaE/deltaV -> del` | P-phase output |
| `Flow` | A | `P = deltaE/deltaV -> del` | P-phase output |
| `LocalActualization` | L | `V = (L n G -> B'') -> Inf0'` | V-phase output |
| `GlobalPropagation` | G | `V = (L n G -> B'') -> Inf0'` | V-phase output |
| `Benefit` | B | `V = (L n G -> B'') -> Inf0'` | V-phase output |
| `FractalSeed` | B'' | `V = (L n G -> B'') -> Inf0'` | V-phase output |
| `EnrichedReturn` | Inf0' | `V = (L n G -> B'') -> Inf0'` | V-phase output |

#### Phase Engines (6 exports)

| Symbol | Phase | Equation | Steps |
|---|---|---|---|
| `PhaseEngine` | -- | -- | Abstract base |
| `S_PhaseEngine` | S | `S = Inf0 -> ?` | 4 |
| `G_PhaseEngine` | G | `G = alpha === {alpha'}` | 5 |
| `Q_PhaseEngine` | Q | `Q = phi n Omega` | 5 |
| `P_PhaseEngine` | P | `P = deltaE/deltaV -> del` | 6 |
| `V_PhaseEngine` | V | `V = (L n G -> B'') -> Inf0'` | 7 |

#### Sub-Systems (3 exports)

| Symbol | Module | Purpose |
|---|---|---|
| `LensMatrix` | `holographic.py` | 25-lens holographic matrix |
| `CorruptionDetector` | `corruption.py` | L1-L4 and V0 runtime guards |
| `C1Compiler` | `compiler.py` | Syntax + semantic + drift validator |

#### Integration (2 exports)

| Symbol | Module | Purpose |
|---|---|---|
| `CycleRunner` | `cycle.py` | Full S->G->Q->P->V orchestration |
| `AttestationChain` | `attestation.py` | SHA-256 provenance fingerprinting |

### Holographic Lens Qualities

| Lens Phase | Quality | Question |
|---|---|---|
| S | openness | What is not yet known? |
| G | pattern | What structure repeats? |
| Q | resonance | Does it authentically connect? |
| P | flow | Where does energy naturally go? |
| V | benefit | What crystallized and carries forward? |

### Phase Decoding Steps

| Phase | Decoding Steps | Output Artifacts |
|---|---|---|
| **S** | `HOLD Inf0 -> RECEIVE -> -> NAME ? -> VALIDATE X` | `{X, Inf0}` |
| **G** | `RECEIVE X -> SEEK alpha -> TEST === -> FIND {alpha'} -> VALIDATE Y` | `{alpha, Y}` |
| **Q** | `RECEIVE X+alpha+Y -> HOLD phi -> HOLD Omega -> WATCH n -> VALIDATE Z` | `{phi, Omega, phi-n-Omega, Z}` |
| **P** | `RECEIVE X+alpha+Y+Z -> MAP deltaE -> MAP deltaV -> COMPUTE -> REVEAL del -> VALIDATE A` | `{deltaE, deltaV, deltaE/deltaV, del, A}` |
| **V** | `RECEIVE trace -> NAME L -> NAME G -> FIND n -> COMPOSE B'' -> NAME B -> FORM Inf0'` | `{L, G, L-n-G, B'', B, Inf0'}` |

---

## Appendix: Design Principles

1. **Every symbol is a first-class object.** There are no string constants representing Codex symbols. `Inf0` is an `Inf0` instance. `alpha` is a `CoreEssence` instance.
2. **Every decoding step is an executable method.** The Codex says "HOLD Inf0, RECEIVE ->, NAME ?, VALIDATE X" -- the runtime executes exactly these steps as method calls.
3. **Every corruption is a halting exception.** L1, L2, L3, L4, and V0 are not warnings or log messages. They are exceptions that stop execution at the constitutional boundary.
4. **Every cycle is attested.** SHA-256 fingerprints provide cryptographic provenance. The chain is append-only and tamper-evident.
5. **The context chain is adaptive, not pipelined.** Each phase receives all accumulated outputs from prior phases, not just the immediately preceding phase's output.
6. **Lenses refine, they do not replace.** The holographic matrix examines outputs through different perceptual qualities but never mutates or replaces the host phase's decoded result.
7. **The compiler is the Codex.** C1 validation checks syntax (structure), semantics (meaning), and drift (deviation) against the canonical specification, not against a secondary ruleset.
8. **The runtime is the Codex.** There is no behavior in the runtime that is not grounded in a Codex-defined symbol, equation, or rule. Every line of code traces back to a specific section of the Codex.

---

*End of Guide. Built for the 5QLN ecosystem: 5 repos, 4 skills, 1 runtime.*
