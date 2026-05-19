#!/usr/bin/env python3
"""
5QLN Symbolic Runtime Installer & Validator
============================================
Installs, validates, and tests the 5QLN Symbolic Runtime.
Run: python3 install.py
"""

from __future__ import annotations

import functools
import glob
import os
import subprocess
import sys
import time
import traceback
from typing import Any, Callable, Dict, List, Tuple

# ---------------------------------------------------------------------------
# ANSI colour helpers
# ---------------------------------------------------------------------------

GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"


def _green(text: str) -> str:
    return f"{GREEN}{text}{RESET}"


def _red(text: str) -> str:
    return f"{RED}{text}{RESET}"


def _yellow(text: str) -> str:
    return f"{YELLOW}{text}{RESET}"


def _cyan(text: str) -> str:
    return f"{CYAN}{text}{RESET}"


def _bold(text: str) -> str:
    return f"{BOLD}{text}{RESET}"


def check_mark(ok: bool) -> str:
    return _green("✓") if ok else _red("✗")


# ---------------------------------------------------------------------------
# Test result accumulator
# ---------------------------------------------------------------------------

TEST_RESULTS: List[Dict[str, str]] = []


def record(name: str, passed: bool, details: str = "") -> bool:
    """Record a test result and print it."""
    status = _green("PASS") if passed else _red("FAIL")
    symbol = check_mark(passed)
    print(f"  {symbol} {name:<50s} {status}")
    if details:
        print(f"      {details}")
    TEST_RESULTS.append({"name": name, "status": "PASS" if passed else "FAIL", "details": details})
    return passed


def section(title: str) -> None:
    """Print a section header."""
    print(f"\n{_bold('─' * 70)}")
    print(f"  {_bold(title)}")
    print(f"{_bold('─' * 70)}")


# ---------------------------------------------------------------------------
# 1. Banner
# ---------------------------------------------------------------------------

def print_banner() -> None:
    """Print a professional banner."""
    print()
    print(_bold("╔" + "═" * 68 + "╗"))
    print(_bold("║" + "  5QLN Symbolic Runtime — Installer & Validator".ljust(68) + "║"))
    print(_bold("║" + "  " + "─" * 64 + "  ║"))
    print(_bold("║" + f"  Version        : 1.0.0".ljust(68) + "║"))
    print(_bold("║" + f"  Codex Source   : https://www.5qln.com/codex".ljust(68) + "║"))
    print(_bold("║" + f"  Python         : {sys.version}".ljust(68) + "║"))
    print(_bold("║" + f"  Platform       : {sys.platform}".ljust(68) + "║"))
    print(_bold("╚" + "═" * 68 + "╝"))
    print()


# ---------------------------------------------------------------------------
# 2. Environment Check
# ---------------------------------------------------------------------------

def test_environment() -> bool:
    """Verify Python >= 3.8, package directory, and 11 modules."""
    section("2. Environment Check")
    all_ok = True

    # Python version
    py_ok = sys.version_info >= (3, 8)
    detail = f"Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    record(f"Python >= 3.8", py_ok, detail)
    all_ok &= py_ok

    # Package directory
    pkg_dir = os.path.join(os.path.dirname(__file__), "qln_symbolic_runtime")
    dir_ok = os.path.isdir(pkg_dir)
    record(f"Package directory exists", dir_ok, pkg_dir)
    all_ok &= dir_ok

    # Count 11 Python modules
    modules = sorted(glob.glob(os.path.join(pkg_dir, "*.py")))
    # Exclude __pycache__ and count only .py files
    module_names = [os.path.basename(m) for m in modules]
    count_ok = len(module_names) == 11
    record(f"11 Python modules found", count_ok, f"Found {len(module_names)}: {', '.join(module_names)}")
    all_ok &= count_ok

    # Check each expected module
    expected = [
        "__init__.py",
        "exceptions.py",
        "const.py",
        "symbols.py",
        "phases.py",
        "holographic.py",
        "corruption.py",
        "compiler.py",
        "cycle.py",
        "attestation.py",
        "repl.py",
    ]
    for mod in expected:
        mod_ok = os.path.isfile(os.path.join(pkg_dir, mod))
        record(f"  Module: {mod}", mod_ok)
        all_ok &= mod_ok

    return all_ok


# ---------------------------------------------------------------------------
# 3. Import Test
# ---------------------------------------------------------------------------

def test_import() -> bool:
    """Import qln_symbolic_runtime and verify exports."""
    section("3. Import Test")
    all_ok = True

    try:
        import qln_symbolic_runtime as qsr

        # Version
        ver_ok = qsr.__version__ == "1.0.0"
        record(f"__version__ == '1.0.0'", ver_ok, qsr.__version__)
        all_ok &= ver_ok

        # Codex source
        src_ok = qsr.__codex_source__ == "https://www.5qln.com/codex"
        record(f"__codex_source__ == 'https://www.5qln.com/codex'", src_ok, qsr.__codex_source__)
        all_ok &= src_ok

        # All 60 exports
        exports = getattr(qsr, "__all__", [])
        exports_ok = len(exports) == 60
        record(f"60 exports in __all__", exports_ok, f"Found {len(exports)} exports")
        all_ok &= exports_ok

        # Check each export
        missing = []
        for name in exports:
            if not hasattr(qsr, name):
                missing.append(name)
        exports_found_ok = len(missing) == 0
        record(f"All exports importable", exports_found_ok,
               f"Missing: {missing}" if missing else f"All {len(exports)} exports present")
        all_ok &= exports_found_ok

    except Exception as exc:
        record(f"Import qln_symbolic_runtime", False, f"{type(exc).__name__}: {exc}")
        all_ok = False

    return all_ok


# ---------------------------------------------------------------------------
# 4. Symbol Table Test
# ---------------------------------------------------------------------------

def test_symbols() -> bool:
    """Test that every Codex symbol is a runtime entity."""
    section("4. Symbol Table Test")
    all_ok = True

    try:
        from qln_symbolic_runtime.symbols import ALL_SYMBOLS, Artificial, Symbol

        # Instantiate every Symbol subclass
        instances = []
        for cls in ALL_SYMBOLS:
            try:
                inst = cls(value=f"test-{cls.__name__}")
                instances.append((cls, inst))
            except Exception as exc:
                record(f"Instantiate {cls.__name__}", False, str(exc))
                all_ok = False

        inst_ok = len(instances) == len(ALL_SYMBOLS)
        record(f"Instantiate all {len(ALL_SYMBOLS)} symbol classes", inst_ok,
               f"{len(instances)}/{len(ALL_SYMBOLS)} instantiated")
        all_ok &= inst_ok

        # Verify name, glyph, equation_context
        attr_ok = True
        for cls, inst in instances:
            if not getattr(cls, "name", ""):
                attr_ok = False
                break
            if not getattr(cls, "glyph", ""):
                attr_ok = False
                break
            if not getattr(cls, "equation_context", ""):
                attr_ok = False
                break
        record(f"All symbols have name/glyph/equation_context", attr_ok)
        all_ok &= attr_ok

        # Test Artificial.resolve() — "One Law" → "Artificial"
        art1 = Artificial()
        art1.resolve("One Law")
        art1_ok = art1.value == "Artificial"
        record(f"Artificial.resolve('One Law') → 'Artificial'", art1_ok, f"got: {art1.value!r}")
        all_ok &= art1_ok

        # Test Artificial.resolve() — "P → A" → "Flow"
        art2 = Artificial()
        art2.resolve("P → A")
        art2_ok = art2.value == "Flow"
        record(f"Artificial.resolve('P → A') → 'Flow'", art2_ok, f"got: {art2.value!r}")
        all_ok &= art2_ok

        # Verify validate() sets validated = True
        val_ok = True
        for cls, inst in instances:
            result = inst.validate()
            if not result or not inst.validated:
                val_ok = False
                break
        record(f"validate() sets validated = True", val_ok)
        all_ok &= val_ok

    except Exception as exc:
        record(f"Symbol table test", False, f"{type(exc).__name__}: {exc}")
        traceback.print_exc()
        all_ok = False

    return all_ok


# ---------------------------------------------------------------------------
# 5. Constants Test
# ---------------------------------------------------------------------------

def test_constants() -> bool:
    """Test that Nine Invariant Lines are exact."""
    section("5. Constants Test")
    all_ok = True

    try:
        from qln_symbolic_runtime.const import (
            ONE_LAW, CYCLE, NINE_INVARIANT_LINES, EQUATIONS, CORRUPTION_CODES,
        )

        # ONE_LAW
        ol_ok = ONE_LAW == "H = ∞0 | A = K"
        record(f"ONE_LAW == 'H = ∞0 | A = K'", ol_ok, f"got: {ONE_LAW!r}")
        all_ok &= ol_ok

        # CYCLE
        cy_ok = CYCLE == "S → G → Q → P → V"
        record(f"CYCLE == 'S → G → Q → P → V'", cy_ok, f"got: {CYCLE!r}")
        all_ok &= cy_ok

        # NINE_INVARIANT_LINES has 9 entries
        nil_ok = len(NINE_INVARIANT_LINES) == 9
        record(f"NINE_INVARIANT_LINES has 9 entries", nil_ok, f"got: {len(NINE_INVARIANT_LINES)}")
        all_ok &= nil_ok

        # EQUATIONS has 5 entries
        eq_ok = len(EQUATIONS) == 5
        record(f"EQUATIONS has 5 entries", eq_ok, f"got: {len(EQUATIONS)}")
        all_ok &= eq_ok

        # Exact equation strings
        expected_equations = {
            "S": "S = ∞0 → ?",
            "G": "G = α ≡ {α'}",
            "Q": "Q = φ ⋂ Ω",
            "P": "P = δE/δV → ∇",
            "V": "V = (L ∩ G → B'') → ∞0'",
        }
        eq_exact_ok = EQUATIONS == expected_equations
        record(f"EQUATIONS match exact strings", eq_exact_ok)
        all_ok &= eq_exact_ok

        # CORRUPTION_CODES has 5 codes: L1, L2, L3, L4, V∅
        cc_ok = len(CORRUPTION_CODES) == 5
        record(f"CORRUPTION_CODES has 5 codes", cc_ok, f"got: {CORRUPTION_CODES}")
        all_ok &= cc_ok

        expected_codes = ["L1", "L2", "L3", "L4", "V∅"]
        cc_exact_ok = CORRUPTION_CODES == expected_codes
        record(f"CORRUPTION_CODES == [L1, L2, L3, L4, V∅]", cc_exact_ok)
        all_ok &= cc_exact_ok

    except Exception as exc:
        record(f"Constants test", False, f"{type(exc).__name__}: {exc}")
        traceback.print_exc()
        all_ok = False

    return all_ok


# ---------------------------------------------------------------------------
# 6. Single Cycle Test
# ---------------------------------------------------------------------------

def test_single_cycle() -> bool:
    """The core test — full S→G→Q→P→V cycle."""
    section("6. Single Cycle Test")
    all_ok = True

    try:
        from qln_symbolic_runtime.cycle import CycleRunner

        runner = CycleRunner()
        trace = runner.run_cycle("What is the nature of authentic inquiry?")

        # All 5 phases present
        phases_present = [p for p in ("S", "G", "Q", "P", "V") if p in trace]
        phases_ok = len(phases_present) == 5
        record(f"All 5 phases present in trace", phases_ok,
               f"Present: {phases_present}")
        all_ok &= phases_ok

        # Each phase has status "OK"
        status_ok = True
        for phase in ("S", "G", "Q", "P", "V"):
            if phase in trace:
                if trace[phase].get("status") != "OK":
                    status_ok = False
                    break
            else:
                status_ok = False
                break
        record(f"Each phase has status 'OK'", status_ok)
        all_ok &= status_ok

        # _compiled["overall"] == "COMPLIANT"
        compiled = trace.get("_compiled", {})
        comp_ok = compiled.get("overall") == "COMPLIANT"
        record(f"_compiled['overall'] == 'COMPLIANT'", comp_ok,
               f"got: {compiled.get('overall')!r}")
        all_ok &= comp_ok

        # _attestation has trace_hash and chain_hash
        att = trace.get("_attestation", {})
        att_ok = "trace_hash" in att and "chain_hash" in att
        record(f"_attestation has trace_hash and chain_hash", att_ok,
               f"trace_hash: {att.get('trace_hash', 'MISSING')[:16]}...")
        all_ok &= att_ok

    except Exception as exc:
        record(f"Single cycle test", False, f"{type(exc).__name__}: {exc}")
        traceback.print_exc()
        all_ok = False

    return all_ok


# ---------------------------------------------------------------------------
# 7. Adaptive Context Chain Test
# ---------------------------------------------------------------------------

def test_adaptive_context() -> bool:
    """Verify adaptive context chain across phases."""
    section("7. Adaptive Context Chain Test")
    all_ok = True

    try:
        from qln_symbolic_runtime.cycle import CycleRunner

        runner = CycleRunner()
        trace = runner.run_cycle("What is the nature of authentic inquiry?")

        # G-phase receives X from S
        g_input = trace.get("G", {}).get("input", {})
        g_has_x = "X" in g_input
        record(f"G-phase receives X from S", g_has_x, f"G input keys: {list(g_input.keys())}")
        all_ok &= g_has_x

        # Q-phase receives X + α + Y from S and G
        q_input = trace.get("Q", {}).get("input", {})
        q_has_all = all(k in q_input for k in ("X", "α", "Y"))
        record(f"Q-phase receives X + α + Y from S and G", q_has_all,
               f"Q input keys: {list(q_input.keys())}")
        all_ok &= q_has_all

        # P-phase receives full context from S, G, Q
        p_input = trace.get("P", {}).get("input", {})
        p_has_all = all(k in p_input for k in ("X", "α", "Y", "Z"))
        record(f"P-phase receives X + α + Y + Z", p_has_all,
               f"P input keys: {list(p_input.keys())}")
        all_ok &= p_has_all

        # V-phase receives full trace
        v_input = trace.get("V", {}).get("input", {})
        v_has_context = len(v_input) >= 4  # Should have X, α, Y, Z, φ, etc.
        record(f"V-phase receives full context", v_has_context,
               f"V input keys: {list(v_input.keys())}")
        all_ok &= v_has_context

    except Exception as exc:
        record(f"Adaptive context test", False, f"{type(exc).__name__}: {exc}")
        traceback.print_exc()
        all_ok = False

    return all_ok


# ---------------------------------------------------------------------------
# 8. Holographic Lens Test (25 lenses)
# ---------------------------------------------------------------------------

def test_holographic_lenses() -> bool:
    """Apply all 25 lens combinations."""
    section("8. Holographic Lens Test (25 lenses)")
    all_ok = True

    try:
        from qln_symbolic_runtime.holographic import LensMatrix
        from qln_symbolic_runtime.const import PHASES

        lm = LensMatrix()
        phases = PHASES  # ["S", "G", "Q", "P", "V"]
        required_keys = {"lens", "quality", "question", "refinement"}

        lens_count = 0
        unique_questions: set[str] = set()

        for host in phases:
            for lens in phases:
                try:
                    result = lm.apply_lens(host, lens, {"test": "output"}, "test entity")
                    lens_count += 1
                    has_keys = required_keys.issubset(result.keys())
                    if not has_keys:
                        record(f"Lens {host}{lens} has required keys", False,
                               f"Missing: {required_keys - result.keys()}")
                        all_ok = False
                    unique_questions.add(result.get("question", ""))
                except Exception as exc:
                    record(f"Lens {host}{lens}", False, str(exc))
                    all_ok = False

        count_ok = lens_count == 25
        record(f"25 lens combinations applied", count_ok, f"Applied: {lens_count}")
        all_ok &= count_ok

        uq_ok = len(unique_questions) == 25
        record(f"25 unique lens questions generated", uq_ok,
               f"Unique questions: {len(unique_questions)}")
        all_ok &= uq_ok

    except Exception as exc:
        record(f"Holographic lens test", False, f"{type(exc).__name__}: {exc}")
        traceback.print_exc()
        all_ok = False

    return all_ok


# ---------------------------------------------------------------------------
# 9. Corruption Detection Test
# ---------------------------------------------------------------------------

def test_corruption_detection() -> bool:
    """Verify all 5 corruption violation types can be caught."""
    section("9. Corruption Detection Test")
    all_ok = True

    try:
        from qln_symbolic_runtime.exceptions import (
            L1_ClosingViolation,
            L2_GeneratingViolation,
            L3_ClaimingViolation,
            L4_PerformingViolation,
            VEmpty_IncompleteViolation,
        )

        # L1
        l1_ok = False
        try:
            raise L1_ClosingViolation("Test L1", phase="S")
        except L1_ClosingViolation:
            l1_ok = True
        record(f"L1_ClosingViolation catchable", l1_ok)
        all_ok &= l1_ok

        # L2
        l2_ok = False
        try:
            raise L2_GeneratingViolation("Test L2", phase="G")
        except L2_GeneratingViolation:
            l2_ok = True
        record(f"L2_GeneratingViolation catchable", l2_ok)
        all_ok &= l2_ok

        # L3
        l3_ok = False
        try:
            raise L3_ClaimingViolation("Test L3", phase="Q")
        except L3_ClaimingViolation:
            l3_ok = True
        record(f"L3_ClaimingViolation catchable", l3_ok)
        all_ok &= l3_ok

        # L4
        l4_ok = False
        try:
            raise L4_PerformingViolation("Test L4", phase="P")
        except L4_PerformingViolation:
            l4_ok = True
        record(f"L4_PerformingViolation catchable", l4_ok)
        all_ok &= l4_ok

        # V∅
        ve_ok = False
        try:
            raise VEmpty_IncompleteViolation("Test V∅", phase="V")
        except VEmpty_IncompleteViolation:
            ve_ok = True
        record(f"VEmpty_IncompleteViolation catchable", ve_ok)
        all_ok &= ve_ok

    except Exception as exc:
        record(f"Corruption detection test", False, f"{type(exc).__name__}: {exc}")
        traceback.print_exc()
        all_ok = False

    return all_ok


# ---------------------------------------------------------------------------
# 10. Batch Processing Test
# ---------------------------------------------------------------------------

def test_batch_processing() -> bool:
    """Test ∞0' carry-forward across batch runs."""
    section("10. Batch Processing Test (∞0' carry-forward)")
    all_ok = True

    try:
        from qln_symbolic_runtime.cycle import CycleRunner

        runner = CycleRunner()
        entities = ["What is truth?", "How do we know?", "What carries forward?"]
        batch = runner.run_batch(entities)

        # batch_size == 3
        bs_ok = batch.get("batch_size") == 3
        record(f"batch_size == 3", bs_ok, f"got: {batch.get('batch_size')}")
        all_ok &= bs_ok

        # All cycles completed
        cycles = batch.get("cycles", [])
        all_completed = len(cycles) == 3
        record(f"All 3 cycles completed", all_completed, f"Cycles: {len(cycles)}")
        all_ok &= all_completed

        # Final ∞0' is not None (carry-forward worked)
        final_inf0p = batch.get("final_∞0'")
        carry_ok = final_inf0p is not None
        record(f"final_∞0' is not None (carry-forward)", carry_ok,
               f"final_∞0': {str(final_inf0p)[:80]!r}")
        all_ok &= carry_ok

    except Exception as exc:
        record(f"Batch processing test", False, f"{type(exc).__name__}: {exc}")
        traceback.print_exc()
        all_ok = False

    return all_ok


# ---------------------------------------------------------------------------
# 11. Attestation Chain Test
# ---------------------------------------------------------------------------

def test_attestation_chain() -> bool:
    """Verify attestation hashes differ and verify() works."""
    section("11. Attestation Chain Test")
    all_ok = True

    try:
        from qln_symbolic_runtime.cycle import CycleRunner
        from qln_symbolic_runtime.attestation import AttestationChain

        runner = CycleRunner()

        # Run 2 cycles
        trace1 = runner.run_cycle("First inquiry?")
        trace2 = runner.run_cycle("Second inquiry?")

        att1 = trace1.get("_attestation", {})
        att2 = trace2.get("_attestation", {})

        # Chain hashes differ
        ch1 = att1.get("chain_hash", "")
        ch2 = att2.get("chain_hash", "")
        diff_ok = ch1 != ch2 and ch1 != "" and ch2 != ""
        record(f"Chain hashes differ (linked)", diff_ok,
               f"ch1: {ch1[:16]}...  ch2: {ch2[:16]}...")
        all_ok &= diff_ok

        # AttestationChain.verify() returns True for valid trace
        chain = AttestationChain()
        # Attest the first trace
        fp1 = chain.attest(trace1)
        verify_ok = chain.verify(trace1, fp1)
        record(f"AttestationChain.verify() returns True", verify_ok)
        all_ok &= verify_ok

    except Exception as exc:
        record(f"Attestation chain test", False, f"{type(exc).__name__}: {exc}")
        traceback.print_exc()
        all_ok = False

    return all_ok


# ---------------------------------------------------------------------------
# 12. REPL Test
# ---------------------------------------------------------------------------

def test_repl() -> bool:
    """Verify REPL can be instantiated (without blocking)."""
    section("12. REPL Test")
    all_ok = True

    try:
        from qln_symbolic_runtime.repl import REPL

        repl = REPL()
        inst_ok = repl is not None
        record(f"REPL instantiated", inst_ok)
        all_ok &= inst_ok

        # Verify it has a runner
        runner_ok = hasattr(repl, "runner") and repl.runner is not None
        record(f"REPL has runner", runner_ok)
        all_ok &= runner_ok

        # Verify start() method exists (don't call it — it blocks)
        start_ok = hasattr(repl, "start") and callable(getattr(repl, "start"))
        record(f"REPL has start() method", start_ok)
        all_ok &= start_ok

    except Exception as exc:
        record(f"REPL test", False, f"{type(exc).__name__}: {exc}")
        traceback.print_exc()
        all_ok = False

    return all_ok


# ---------------------------------------------------------------------------
# 13. Summary Report
# ---------------------------------------------------------------------------

def print_summary() -> bool:
    """Print the final summary table."""
    section("13. Summary Report")

    passed = sum(1 for r in TEST_RESULTS if r["status"] == "PASS")
    failed = sum(1 for r in TEST_RESULTS if r["status"] == "FAIL")
    total = passed + failed

    # Group by section (each section function prints its own section header)
    # Here we just print the aggregate table
    print(f"\n  {_bold('Test Results Table')}")
    print(f"  {_bold('─' * 66)}")
    print(f"  {'Test':<50s} {'Status':<8s} Details")
    print(f"  {'─' * 66}")
    for r in TEST_RESULTS:
        status_str = _green("PASS") if r["status"] == "PASS" else _red("FAIL")
        detail = r["details"][:40] if r["details"] else ""
        print(f"  {r['name']:<50s} {status_str:<8s} {detail}")
    print(f"  {'─' * 66}")

    # Totals
    if failed == 0:
        total_str = _green(f"{passed}/{total} PASSED")
    else:
        total_str = f"{_green(f'{passed} passed')}, {_red(f'{failed} failed')}  /  {total} total"

    print(f"\n  {_bold('Total:')}  {total_str}")

    # Next steps
    print(f"\n  {_bold('Next Steps:')}")
    print(f"    {_green('→')} Import:  from qln_symbolic_runtime import CycleRunner")
    print(f"    {_green('→')} Run:     runner = CycleRunner(); trace = runner.run_cycle('Your inquiry?')")
    print(f"    {_green('→')} Batch:   runner.run_batch(['Q1?', 'Q2?', 'Q3?'])")
    print(f"    {_green('→')} REPL:    python -m qln_symbolic_runtime.repl")
    print(f"    {_green('→')} Codex:   https://www.5qln.com/codex")
    print()

    return failed == 0


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    """Run all installer tests and return exit code."""
    t0 = time.time()
    print_banner()

    results = []
    results.append(test_environment())
    results.append(test_import())
    results.append(test_symbols())
    results.append(test_constants())
    results.append(test_single_cycle())
    results.append(test_adaptive_context())
    results.append(test_holographic_lenses())
    results.append(test_corruption_detection())
    results.append(test_batch_processing())
    results.append(test_attestation_chain())
    results.append(test_repl())

    all_passed = print_summary()

    elapsed = time.time() - t0
    print(f"  Time: {elapsed:.2f}s")

    if all_passed:
        print(f"\n  {_green('✓ All tests passed — 5QLN Symbolic Runtime is ready!')}\n")
        return 0
    else:
        print(f"\n  {_red('✗ Some tests failed — review the output above.')}\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
