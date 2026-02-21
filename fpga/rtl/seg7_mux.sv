`default_nettype none

// 3-digit multiplexed 7-segment driver for common-anode displays.
// Cycles through hundreds/tens/ones at ~1kHz from a 27MHz clock.
// Accent segments and digit strobes are active-low.
module seg7_mux (
    input  wire        clk,      // 27 MHz
    input  wire        rst_n,
    input  wire [3:0]  hundreds,
    input  wire [3:0]  tens,
    input  wire [3:0]  ones,
    output reg  [6:0]  seg_n,    // active-low segment cathodes (gfedcba)
    output reg  [2:0]  dig_n     // active-low digit anodes
);

    // 27_000_000 / 3 / 1000 = 9000 counts per digit at ~1kHz refresh
    localparam DIV = 9000;

    reg [13:0] cnt;
    reg [1:0]  sel;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            cnt <= 0;
            sel <= 0;
        end else if (cnt == DIV - 1) begin
            cnt <= 0;
            sel <= (sel == 2'd2) ? 2'd0 : sel + 2'd1;
        end else begin
            cnt <= cnt + 1;
        end
    end

    // Select current BCD digit
    reg [3:0] digit;
    always @(*) begin
        case (sel)
            2'd0: digit = hundreds;
            2'd1: digit = tens;
            2'd2: digit = ones;
            default: digit = 4'd0;
        endcase
    end

    // 7-segment decode (active-high gfedcba, then invert for common anode)
    reg [6:0] seg_lut;
    always @(*) begin
        case (digit)
            4'd0:    seg_lut = 7'b0111111;
            4'd1:    seg_lut = 7'b0000110;
            4'd2:    seg_lut = 7'b1011011;
            4'd3:    seg_lut = 7'b1001111;
            4'd4:    seg_lut = 7'b1100110;
            4'd5:    seg_lut = 7'b1101101;
            4'd6:    seg_lut = 7'b1111101;
            4'd7:    seg_lut = 7'b0000111;
            4'd8:    seg_lut = 7'b1111111;
            4'd9:    seg_lut = 7'b1101111;
            default: seg_lut = 7'b0000000;
        endcase
    end

    // Invert for common-anode (active-low outputs)
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            seg_n <= 7'h7F;
            dig_n <= 3'b111;
        end else begin
            seg_n <= ~seg_lut;
            case (sel)
                2'd0: dig_n <= 3'b110;
                2'd1: dig_n <= 3'b101;
                2'd2: dig_n <= 3'b011;
                default: dig_n <= 3'b111;
            endcase
        end
    end

endmodule
