# Cocotb Makefile for FPGA wrapper module tests
# Usage:
#   make MODULE=test_double_dabble_combo   — test combinational converter
#   make MODULE=test_seg7_mux              — test 7-seg mux driver

SIM ?= icarus
TOPLEVEL_LANG ?= verilog

RTL_DIR = $(PWD)/../rtl

# Default to combo converter test
MODULE ?= test_double_dabble_combo

ifeq ($(MODULE),test_double_dabble_combo)
  VERILOG_SOURCES = $(RTL_DIR)/double_dabble_combo.sv
  TOPLEVEL = double_dabble_combo
else ifeq ($(MODULE),test_seg7_mux)
  VERILOG_SOURCES = $(RTL_DIR)/seg7_mux.sv
  TOPLEVEL = seg7_mux
endif

include $(shell cocotb-config --makefiles)/Makefile.sim
