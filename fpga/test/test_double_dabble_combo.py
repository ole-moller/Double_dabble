import cocotb
from cocotb.triggers import Timer


def expected_bcd(val):
    """Convert integer to 12-bit packed BCD {hundreds, tens, ones}."""
    h = val // 100
    t = (val % 100) // 10
    o = val % 10
    return (h << 8) | (t << 4) | o


@cocotb.test()
async def test_all_values(dut):
    """Verify combinational BCD conversion for all 256 input values."""
    for i in range(256):
        dut.bin.value = i
        await Timer(1, units="ns")
        result = int(dut.bcd.value)
        expected = expected_bcd(i)
        assert result == expected, (
            f"bin={i}: got bcd=0x{result:03x}, expected 0x{expected:03x}"
        )
    dut._log.info("All 256 values passed")
