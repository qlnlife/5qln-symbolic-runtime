"""
repl.py — Interactive 5QLN Constitutional Decoding REPL (Module 10)

Usage::

    python -m qln_symbolic_runtime.repl

Provides an interactive command-line interface for live 5QLN decoding
sessions.  Supports single-cycle decoding, batch processing, viewing
the Nine Invariant Lines, and ∞0' carry-forward between cycles.

Part of the 5QLN Symbolic Runtime.
"""

from typing import Any, Dict, List, Optional

from qln_symbolic_runtime.cycle import CycleRunner
from qln_symbolic_runtime.const import NINE_INVARIANT_LINES, MASTER_EQUATION


class REPL:
    """Interactive 5QLN Constitutional Decoding REPL.

    Commands
    --------
    ``decode <text>``
        Run a single S→G→Q→P→V cycle on *text*.  Equivalent to typing
        the text without a command prefix.

    ``batch <item1> | <item2> | ...``
        Run a batch of cycles, carrying ``∞0'`` between items.

    ``lines``
        Display the Nine Invariant Lines of the Constitutional Codex.

    ``quit`` (or Ctrl-D / Ctrl-C)
        Exit the REPL.

    Attributes:
        runner: The shared :class:`CycleRunner` instance.
        history: Ordered list of all traces produced this session.
        current_inf0p: The latest ``∞0'`` value for adaptive carry.
    """

    def __init__(self) -> None:
        """Create a new REPL session with a fresh runner."""
        self.runner: CycleRunner = CycleRunner()
        self.history: List[Dict[str, Any]] = []
        self.current_inf0p: Optional[str] = None

    # ------------------------------------------------------------------ #
    # Main loop
    # ------------------------------------------------------------------ #

    def start(self) -> None:
        """Start the interactive read-eval-print loop.

        Blocks until the user issues ``quit`` or sends EOF / interrupt.
        """
        self._print_banner()

        while True:
            try:
                cmd = input("5QLN> ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nExiting.")
                break

            if not cmd:
                continue
            if cmd == "quit":
                break
            elif cmd == "lines":
                self._cmd_lines()
            elif cmd.startswith("decode "):
                self._cmd_decode(cmd[7:].strip())
            elif cmd.startswith("batch "):
                raw = cmd[6:]
                items = [s.strip() for s in raw.split("|") if s.strip()]
                if items:
                    self._cmd_batch(items)
                else:
                    print("  [Usage: batch <item1> | <item2> | ...]")
            else:
                # Bare input — treat as implicit decode.
                self._cmd_decode(cmd)

        self._print_footer()

    # ------------------------------------------------------------------ #
    # Banner / footer
    # ------------------------------------------------------------------ #

    def _print_banner(self) -> None:
        """Display the welcome banner."""
        print("=" * 60)
        print("5QLN Symbolic Runtime — Constitutional Decoding REPL")
        print("Codex: https://www.5qln.com/codex")
        print("=" * 60)
        print(f"\nMaster Equation: {MASTER_EQUATION}")
        print("\nNine Invariant Lines loaded.  Type 'lines' to view.")
        print("Type 'decode <your inquiry>' to run a cycle.")
        print("Type 'batch <item1> | <item2> | ...' for batch processing.")
        print("Type 'quit' to exit.\n")

    def _print_footer(self) -> None:
        """Display the exit footer."""
        cycles = self.runner._cycle_count
        print(f"\nSession complete — {cycles} cycle(s) executed.")
        print("=" * 60)

    # ------------------------------------------------------------------ #
    # Commands
    # ------------------------------------------------------------------ #

    def _cmd_lines(self) -> None:
        """Display the Nine Invariant Lines."""
        for i, line in enumerate(NINE_INVARIANT_LINES, 1):
            print(f"  {i}. {line}")

    def _cmd_decode(self, entity: str) -> None:
        """Run a single decode cycle on *entity*."""
        trace = self.runner.run_cycle(entity, prior_inf0p=self.current_inf0p)
        self.history.append(trace)
        self._display_trace(trace)

        # Carry ∞0' forward if V-phase completed successfully.
        if "V" in trace and trace["V"].get("status") == "OK":
            v_out = trace.get("V", {}).get("output", {})
            self.current_inf0p = v_out.get("∞0'", self.current_inf0p)

    def _cmd_batch(self, items: List[str]) -> None:
        """Run a batch decode on *items*."""
        result = self.runner.run_batch(items)
        print(f"\n--- Batch: {result['batch_size']} entities ---")
        for i, trace in enumerate(result["cycles"]):
            label = items[i][:50]
            print(f"\n[{i + 1}] {label}")
            self._display_trace(trace, compact=True)
        print(f"\nCorruption summary: {result['corruption_summary']}")
        self.history.extend(result["cycles"])

        # Update current_inf0p from the final trace if possible.
        final_trace = result["cycles"][-1] if result["cycles"] else None
        if final_trace and "V" in final_trace:
            v_out = final_trace.get("V", {}).get("output", {})
            if v_out.get("∞0'"):
                self.current_inf0p = v_out["∞0'"]

    # ------------------------------------------------------------------ #
    # Display helpers
    # ------------------------------------------------------------------ #

    def _display_trace(
        self,
        trace: Dict[str, Any],
        compact: bool = False,
    ) -> None:
        """Pretty-print a cycle trace.

        Args:
            trace: Cycle trace dict.
            compact: If ``True``, suppress per-phase output details.
        """
        for phase in ("S", "G", "Q", "P", "V"):
            if phase not in trace:
                continue
            data = trace[phase]
            status = data.get("status", "?")
            if status == "OK":
                marker = "OK"
            elif status == "VIOLATION":
                marker = "FAIL"
            else:
                marker = "WARN"
            print(f"  [{marker}] {phase}: {status}")

            if not compact and "output" in data:
                for key, value in data["output"].items():
                    print(f"      {key} = {value}")

        compiled = trace.get("_compiled", {})
        if compiled:
            overall = compiled.get("overall", "N/A")
            print(f"  [COMPILED: {overall}]")

        attestation = trace.get("_attestation", {})
        if attestation and "trace_hash" in attestation:
            short_hash = attestation["trace_hash"][:12]
            print(f"  [ATTESTED: {short_hash}...]")


def main() -> None:
    """Entry-point for ``python -m qln_symbolic_runtime.repl``."""
    REPL().start()


if __name__ == "__main__":
    main()
