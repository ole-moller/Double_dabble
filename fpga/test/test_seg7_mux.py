import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, RisingEdge

# 7-seg LUT (active-high gfedcba) — must match seg7_mux.sv
SEG_LUT = {
    0: 0b0111111,
    1: 0b0000110,
    2: 0b1011011,
    3: 0b1001111,
    4: 0b1100110,
    5: 0b1101101,
    6: 0b1111101,
    7: 0b0000111,
    8: 0b1111111,
    9: 0b1101111,
}

# DIV constant from seg7_mux.sv
DIV = 9000


@cocotb.test()
async def test_digit_cycling(dut):
    """Verify that the mux cycles through hundreds, tens, ones."""
    clock = Clock(dut.clk, 37, units="ns")  # ~27 MHz
    cocotb.start_soon(clock.start())

    # Reset
    dut.rst_n.value = 0
    dut.hundreds.value = 2
    dut.tens.value = 5
    dut.ones.value = 5
    await ClockCycles(dut.clk, 3)
    dut.rst_n.value = 1
    await RisingEdge(dut.clk)

    # After reset, sel=0 → hundreds digit
    # Wait for outputs to register (1 cycle after counter loads)
    await ClockCycles(dut.clk, 2)

    # Check hundreds digit (sel=0): dig_n=110, seg shows digit 2 inverted
    assert int(dut.dig_n.value) == 0b110, f"Expected dig_n=110, got {int(dut.dig_n.value):03b}"
    expected_seg = (~SEG_LUT[2]) & 0x7F
    assert int(dut.seg_n.value) == expected_seg, (
        f"Hundreds: expected seg_n=0x{expected_seg:02x}, got 0x{int(dut.seg_n.value):02x}"
    )

    # Advance to tens digit (DIV cycles for counter rollover + 1 for register)
    await ClockCycles(dut.clk, DIV)
    assert int(dut.dig_n.value) == 0b101, f"Expected dig_n=101, got {int(dut.dig_n.value):03b}"
    expected_seg = (~SEG_LUT[5]) & 0x7F
    assert int(dut.seg_n.value) == expected_seg, (
        f"Tens: expected seg_n=0x{expected_seg:02x}, got 0x{int(dut.seg_n.value):02x}"
    )

    # Advance to ones digit
    await ClockCycles(dut.clk, DIV)
    assert int(dut.dig_n.value) == 0b011, f"Expected dig_n=011, got {int(dut.dig_n.value):03b}"
    expected_seg = (~SEG_LUT[5]) & 0x7F
    assert int(dut.seg_n.value) == expected_seg, (
        f"Ones: expected seg_n=0x{expected_seg:02x}, got 0x{int(dut.seg_n.value):02x}"
    )

    # Advance back to hundreds — verify wrap-around
    await ClockCycles(dut.clk, DIV)
    assert int(dut.dig_n.value) == 0b110, f"Expected dig_n=110 after wrap, got {int(dut.dig_n.value):03b}"

    dut._log.info("Digit cycling test passed")


@cocotb.test()
async def test_all_segments(dut):
    """Verify 7-seg encoding for digits 0-9 on the hundreds position."""
    clock = Clock(dut.clk, 37, units="ns")
    cocotb.start_soon(clock.start())

    dut.tens.value = 0
    dut.ones.value = 0

    for d in range(10):
        dut.rst_n.value = 0
        dut.hundreds.value = d
        await ClockCycles(dut.clk, 3)
        dut.rst_n.value = 1
        # Wait for sel=0 output to register
        await ClockCycles(dut.clk, 2)

        expected_seg = (~SEG_LUT[d]) & 0x7F
        assert int(dut.seg_n.value) == expected_seg, (
            f"Digit {d}: expected seg_n=0x{expected_seg:02x}, got 0x{int(dut.seg_n.value):02x}"
        )

    dut._log.info("All segment encodings passed")
