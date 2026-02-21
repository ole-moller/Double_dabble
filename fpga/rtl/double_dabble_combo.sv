`default_nettype none

// Standalone combinational double-dabble binary-to-BCD converter.
// Extracted from tt_um_ole_double_dabble for use in FPGA wrapper
// where all 3 BCD digits are needed simultaneously.
module double_dabble_combo (
    input  wire [7:0]  bin,
    output wire [11:0] bcd  // {hundreds[3:0], tens[3:0], ones[3:0]}
);

    localparam N = 8;
    localparam M = 3;

    wire [4*M-1:0] bcd_reg [0:N];
    assign bcd_reg[0] = {4*M{1'b0}};

    genvar i, j;
    generate
        for (i = 0; i < N; i = i + 1) begin : outer_loop
            wire [4*M-1:0] temp_bcd;
            for (j = 0; j < M; j = j + 1) begin : inner_loop
                wire [3:0] corr_digit;
                assign corr_digit = (bcd_reg[i][4*j+3 -: 4] >= 4'd5) ? 4'd3 : 4'd0;
                assign temp_bcd[4*j+3 -: 4] = bcd_reg[i][4*j+3 -: 4] + corr_digit;
            end
            assign bcd_reg[i+1] = {temp_bcd[4*M-2:0], bin[N-1-i]};
        end
    endgenerate

    assign bcd = bcd_reg[N];

endmodule
