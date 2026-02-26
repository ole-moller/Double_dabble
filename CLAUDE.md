# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Tiny Tapeout design implementing a **Double Dabble** binary-to-BCD converter in SystemVerilog. Converts an 8-bit binary input to 3 BCD digits displayed sequentially on a 7-segment display (hundreds, tens, ones) separated by a decimal point. Part of the DTU Tiny Tapeout February 2026 submission.

Top-level module: `tt_um_ole_double_dabble`

## Build & Test

Run cocotb tests (requires icarus verilog and cocotb installed):
```
cd test && make
```

Clean and re-run:
```
cd test && make clean && make
```

Gate-level simulation (requires PDK):
```
cd test && make GATES=yes
```

## Architecture

The design has two main parts in `src/double_dabble.sv`:

1. **Combinational BCD conversion**: `generate` loops unroll the Double Dabble algorithm across 8 iterations. Each iteration shifts a 12-bit register left, injects the next input bit, and adds 3 to any BCD nibble >= 5. Purely combinational — no clock needed.

2. **Sequential display FSM**: 4-state machine (`IDLE`→`HUNDREDS`→`TENS`→`ONES`→`IDLE`) clocked by `clk4` (main clock ÷ 4). `IDLE` outputs decimal point separator; other states output BCD digits on 7-segment. FSM resets to `IDLE` on `bin_change` or `rst_n`.

## I/O Mapping (Tiny Tapeout conventions)

| TT Port | Signal | Description |
|---------|--------|-------------|
| `ui_in[7:0]` | `bin` | Binary input |
| `uo_out[6:0]` | `segments` | 7-segment (active high, gfedcba) |
| `uo_out[7]` | `separator` | Decimal point |
| `uio_out[7:0]` | `bcd[7:0]` | Packed BCD tens+ones |
| `uio_oe` | `0xFF` | Bidirectional always output |

## Test Structure

- `test/tb.v` — Verilog testbench wrapper instantiating `tt_um_ole_double_dabble`
- `test/test.py` — Cocotb tests verifying conversion of 0, 12, 77, 167, 189, 243, 255
- `test/Makefile` — Standard TT cocotb Makefile (icarus default)

Each display state lasts 4 base clock cycles (due to ÷4 divider). A full separator→hundreds→tens→ones cycle = 16 clock cycles.
