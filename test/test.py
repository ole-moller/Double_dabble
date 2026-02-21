# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    # Set the clock period to 10 us for simulation speed
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 1)
    dut.rst_n.value = 1

    dut._log.info("Test Double Dabble behavior")


    # Test conversion of 0
    dut.ui_in.value  = 0
    dut.uio_in.value = 0

    # Wait for four clock cycles to see separator
    await ClockCycles(dut.clk, 4)
    # Separator in 7-segment
    assert dut.uo_out.value == 0b10000000
    
    # Wait for four clock cycles to see hundreds
    await ClockCycles(dut.clk, 4)
    # Hundreds = 0 in 7-segment
    assert dut.uo_out.value == 0b00111111
    # BCD tens and ones only 0*16+0 = 0
    assert dut.uio_out.value == 0

    # Wait for four clock cycles to see tens
    await ClockCycles(dut.clk, 4)
    # Tens = 0 in 7-segment
    assert dut.uo_out.value == 0b00111111
    # BCD tens and ones are unchanged
    assert dut.uio_out.value == 0
   
    # Wait for four clock cycles to see ones
    await ClockCycles(dut.clk, 4)
    # Hundreds = 0 in 7-segment
    assert dut.uo_out.value == 0b00111111
    # BCD tens and ones are unchanged
    assert dut.uio_out.value == 0

    # ------------------------------------

    # Test conversion of 12
    dut.ui_in.value  = 12
    dut.uio_in.value = 0

    # Wait for four clock cycles to see separator
    await ClockCycles(dut.clk, 4)
    # Separator in 7-segment
    assert dut.uo_out.value == 0b10000000
    
    # Wait for four clock cycles to see hundreds
    await ClockCycles(dut.clk, 4)
    # Hundreds = 0 in 7-segment
    assert dut.uo_out.value == 0b00111111
    # BCD tens and ones only 1*16+2 = 18
    assert dut.uio_out.value == 18

    # Wait for four clock cycles to see tens
    await ClockCycles(dut.clk, 4)
    # Tens = 1 in 7-segment
    assert dut.uo_out.value == 0b00000110
    # BCD tens and ones are unchanged
    assert dut.uio_out.value == 18
   
    # Wait for four clock cycles to see ones
    await ClockCycles(dut.clk, 4)
    # Ones = 2 in 7-segment
    assert dut.uo_out.value == 0b01011011
    # BCD tens and ones are unchanged
    assert dut.uio_out.value == 18

    # ------------------------------------

    # Test conversion of 77
    dut.ui_in.value  = 77
    dut.uio_in.value = 0

    # Wait for four clock cycles to see separator
    await ClockCycles(dut.clk, 4)
    # Separator in 7-segment
    assert dut.uo_out.value == 0b10000000
 
    # Wait for four clock cycles to see hundreds
    await ClockCycles(dut.clk, 4)
    # Hundreds = 0 in 7-segment
    assert dut.uo_out.value == 0b00111111
    # BCD tens and ones only 7*16+7 = 119
    assert dut.uio_out.value == 119

    # Wait for four clock cycles to see tens
    await ClockCycles(dut.clk, 4)
    # Tens = 7 in 7-segment
    assert dut.uo_out.value == 0b00000111
    # BCD tens and ones are unchanged
    assert dut.uio_out.value == 119
   
    # Wait for four clock cycles to see ones
    await ClockCycles(dut.clk, 4)
    # Ones = 7 in 7-segment
    assert dut.uo_out.value == 0b00000111
    # BCD tens and ones are unchanged
    assert dut.uio_out.value == 119

    # ------------------------------------

    # Test conversion of 167
    dut.ui_in.value  = 167
    dut.uio_in.value = 0

    # Wait for four clock cycles to see separator
    await ClockCycles(dut.clk, 4)
    # Separator in 7-segment
    assert dut.uo_out.value == 0b10000000
    
    # Wait for four clock cycles to see hundreds
    await ClockCycles(dut.clk, 4)
    # Hundreds = 1 in 7-segment
    assert dut.uo_out.value == 0b00000110
    # BCD tens and ones only 6*16+7 = 103
    assert dut.uio_out.value == 103

    # Wait for four clock cycles to see tens
    await ClockCycles(dut.clk, 4)
    # Tens = 6 in 7-segment
    assert dut.uo_out.value == 0b1111101
    # BCD tens and ones are unchanged
    assert dut.uio_out.value == 103
   
    # Wait for four clock cycles to see ones
    await ClockCycles(dut.clk, 4)
    # Ones = 7 in 7-segment
    assert dut.uo_out.value == 0b00000111
    # BCD tens and ones are unchanged
    assert dut.uio_out.value == 103

    # ------------------------------------

    # Test conversion of 189
    dut.ui_in.value  = 189
    dut.uio_in.value = 0
    print("Testing " dut.ui_in.value)
  
    # Wait for four clock cycles to see separator
    await ClockCycles(dut.clk, 4)
    # Separator in 7-segment
    assert dut.uo_out.value == 0b10000000
    
    # Wait for four clock cycles to see hundreds
    await ClockCycles(dut.clk, 4)
    # Hundreds = 1 in 7-segment
    assert dut.uo_out.value == 0b00000110
    # BCD tens and ones 8*16+9 = 137
    assert dut.uio_out.value == 137

    # Wait for four clock cycles to see tens
    await ClockCycles(dut.clk, 4)
    # Tens = 8 in 7-segment
    assert dut.uo_out.value == 0b01111111
    # BCD tens and ones are unchanged
    assert dut.uio_out.value == 137

    # Wait for four clock cycles to see ones
    await ClockCycles(dut.clk, 4)
    # Ones = 9 in 7-segment
    assert dut.uo_out.value == 0b01101111
    # BCD tens and ones only are unchanged
    assert dut.uio_out.value == 137
   
    # ------------------------------------
   
    # Test conversion of 243
    dut.ui_in.value  = 243
    dut.uio_in.value = 0

    # Wait for four clock cycles to see separator
    await ClockCycles(dut.clk, 4)
    # Separator in 7-segment
    assert dut.uo_out.value == 0b10000000

    # Wait for four clock cycles to see hundreds
    await ClockCycles(dut.clk, 4)
    # Hundreds = 2 in 7-segment
    assert dut.uo_out.value == 0b01011011
    # BCD tens and ones only 4*16+3 = 67
    assert dut.uio_out.value == 67

    # Wait for four clock cycles to see tens
    await ClockCycles(dut.clk, 4)
    # Tens = 4 in 7-segment
    assert dut.uo_out.value == 0b01100110
    # BCD tens and ones are unchanged
    assert dut.uio_out.value == 67
   
    # Wait for four clock cycles to see ones
    await ClockCycles(dut.clk, 4)
    # Ones = 3 in 7-segment
    assert dut.uo_out.value == 0b01001111
    # BCD tens and ones are unchanged
    assert dut.uio_out.value == 67

    # ------------------------------------
   
    # Test conversion of 255
    dut.ui_in.value  = 255
    dut.uio_in.value = 0

    # Wait for four clock cycles to see separator
    await ClockCycles(dut.clk, 4)
    # Separator in 7-segment
    assert dut.uo_out.value == 0b10000000
    
    # Wait for four clock cycles to see hundreds
    await ClockCycles(dut.clk, 4)
    # Hundreds = 2 in 7-segment
    assert dut.uo_out.value == 0b01011011
    # BCD tens and ones only 5*16+5 = 85
    assert dut.uio_out.value == 85

    # Wait for four clock cycles to see tens
    await ClockCycles(dut.clk, 4)
    # Tens = 5 in 7-segment
    assert dut.uo_out.value == 0b1101101
    # BCD tens and ones only are unchanges
    assert dut.uio_out.value == 85
   
    # Wait for four clock cycles to see ones
    await ClockCycles(dut.clk, 4)
    # Ones = 5 in 7-segment
    assert dut.uo_out.value == 0b01101101
    # BCD tens and ones only are unchanged
    assert dut.uio_out.value == 85

    # ------------------------------------

    # Wait for four clock cycles to see separator
    await ClockCycles(dut.clk, 4)
    # Separator in 7-segment
    assert dut.uo_out.value == 0b10000000
    # BCD tens and ones only are unchanged
    assert dut.uio_out.value == 85
