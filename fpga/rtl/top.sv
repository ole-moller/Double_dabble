`default_nettype none

// Tang Nano 9K FPGA top-level wrapper for tt_um_ole_double_dabble.
// Provides UART register map for host control and a multiplexed
// 3-digit 7-segment display for live BCD output.
module top (
    input  wire       clk_27m,   // 27 MHz crystal
    input  wire       btn_rst_n, // Active-low reset button (directly usable)
    input  wire       uart_rx,
    output wire       uart_tx,
    output wire [6:0] seg_n,     // 7-seg cathodes (active-low, shared)
    output wire [2:0] dig_n      // Digit anodes (active-low, one per display)
);

    // --------------------------------------------------------
    // Reset synchronizer
    // --------------------------------------------------------
    reg [1:0] rst_sync;
    wire rst_n = rst_sync[1];

    always @(posedge clk_27m or negedge btn_rst_n) begin
        if (!btn_rst_n)
            rst_sync <= 2'b00;
        else
            rst_sync <= {rst_sync[0], 1'b1};
    end

    // --------------------------------------------------------
    // UART register map (directly instantiated stub)
    // reg[0] = binary input  (R/W)
    // reg[1] = uo_out        (R)
    // reg[2] = uio_out       (R)
    // --------------------------------------------------------
    wire [7:0] reg0_bin;       // written by host via UART
    wire [7:0] tt_uo_out;
    wire [7:0] tt_uio_out;

    uart_reg_map u_uart (
        .clk    (clk_27m),
        .rst_n  (rst_n),
        .rx     (uart_rx),
        .tx     (uart_tx),
        .reg0   (reg0_bin),
        .reg1   (tt_uo_out),
        .reg2   (tt_uio_out)
    );

    // --------------------------------------------------------
    // Tiny Tapeout module (unchanged)
    // --------------------------------------------------------
    wire [7:0] tt_uio_in = 8'h00;

    tt_um_ole_double_dabble u_tt (
        .ui_in   (reg0_bin),
        .uo_out  (tt_uo_out),
        .uio_in  (tt_uio_in),
        .uio_out (tt_uio_out),
        .uio_oe  (),            // not used on FPGA
        .ena     (1'b1),
        .clk     (clk_27m),
        .rst_n   (rst_n)
    );

    // --------------------------------------------------------
    // Standalone combinational BCD converter (all 3 digits)
    // --------------------------------------------------------
    wire [11:0] bcd_full;

    double_dabble_combo u_bcd (
        .bin (reg0_bin),
        .bcd (bcd_full)
    );

    // --------------------------------------------------------
    // Multiplexed 7-segment display driver
    // --------------------------------------------------------
    seg7_mux u_seg7 (
        .clk      (clk_27m),
        .rst_n    (rst_n),
        .hundreds (bcd_full[11:8]),
        .tens     (bcd_full[7:4]),
        .ones     (bcd_full[3:0]),
        .seg_n    (seg_n),
        .dig_n    (dig_n)
    );

endmodule
