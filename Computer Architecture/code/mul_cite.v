
// XOR 
module xor2 (input wire i0, i1, output wire o);
  assign o = i0 ^ i1; // 輸出為 i0 和 i1 的異或結果
endmodule

// full_adder
module fa ( input wire i0, i1, cin, output wire sum, cout);
    assign sum = i0 ^ i1 ^ cin; // 總和位
    assign cout = (i0 & i1) | (i1 & cin) | (cin & i0); // 進位位
endmodule


// 16 位元 Booth 乘法器
module eight_bit_adder_subractor(
    input wire cin,                 // cin=1 表示減法 (補碼加法)，cin=0 表示加法
    input wire [7:0] i0, i1,       // 兩個 8 位元輸入
    output wire [7:0] sum);

	wire [7:0] temp;
	wire [7:0] int_ip;              // 中間處理後的輸入 i1，可能經過補碼轉換
	
	// 當 cin=1 時，對 i1 取 1 的補碼；否則保持 i1 不變
    xor2 x0 (i1[0], cin, int_ip[0]);
    xor2 x1 (i1[1], cin, int_ip[1]);
    xor2 x2 (i1[2], cin, int_ip[2]);
    xor2 x3 (i1[3], cin, int_ip[3]);
    xor2 x4 (i1[4], cin, int_ip[4]);
    xor2 x5 (i1[5], cin, int_ip[5]);
    xor2 x6 (i1[6], cin, int_ip[6]);
    xor2 x7 (i1[7], cin, int_ip[7]);
    
    // 將 i0 和處理後的 int_ip 相加，考慮進位 cin
	fa fa1(i0[0], int_ip[0], cin,     sum[0], temp[0]);
	fa fa2(i0[1], int_ip[1], temp[0], sum[1], temp[1]);
	fa fa3(i0[2], int_ip[2], temp[1], sum[2], temp[2]);
	fa fa4(i0[3], int_ip[3], temp[2], sum[3], temp[3]);
	fa fa5(i0[4], int_ip[4], temp[3], sum[4], temp[4]);
	fa fa6(i0[5], int_ip[5], temp[4], sum[5], temp[5]);
	fa fa7(i0[6], int_ip[6], temp[5], sum[6], temp[6]);
	fa fa8(i0[7], int_ip[7], temp[6], sum[7], cout);
	
endmodule

// Booth Algorithm
module booth_substep(
    input wire signed [7:0] acc,    // 累加器當前值 (8 MSB 的初始值)
    input wire signed [7:0] Q,      // Q 的當前值 (最初是乘數)
    input wire signed q0,           // Q 的上一位 (q-1)
    input wire signed [7:0] multiplicand, // 被乘數
    output reg signed [7:0] next_acc,   // 下一個累加器的值 (8 MSB)
    output reg signed [7:0] next_Q,     // 下一個 Q 的值 (8 LSB)
    output reg q0_next);                // 下一個 q-1 的值
    
	wire [7:0] addsub_temp;             // 暫存加法或減法的結果
	
	// 加法器/減法器：當 Q[0] 與 q0 不相等時計算加法或減法結果
	eight_bit_adder_subractor myadd(Q[0], acc, multiplicand, addsub_temp);
	
	// 根據 Booth 條件判斷並更新累加器和 Q 的值
	always @(*) begin	
		if(Q[0] == q0) begin
            // Q[0] == q0，不進行加減法，僅進行算術右移
            q0_next = Q[0];
            next_Q = Q >> 1;          // Q 右移一位
            next_Q[7] = acc[0];       // 最高位用 acc 的最低位補充
            next_acc = acc >> 1;      // 累加器右移一位
            if (acc[7] == 1)          // 保持符號位
                next_acc[7] = 1;
		end

		else begin
            // Q[0] != q0，執行加減法後再進行右移
            q0_next = Q[0];
            next_Q = Q >> 1;
            next_Q[7] = addsub_temp[0];
            next_acc = addsub_temp >> 1;
            if (addsub_temp[7] == 1)  // 保持符號位
                next_acc[7] = 1;
		end			
end	
endmodule

// Booth 乘法器模組：實現 8 位元乘法，產生 16 位元結果
module booth_multiplier(
    input signed[7:0] multiplier, multiplicand, // 輸入的 8 位元乘數和被乘數
    output signed [15:0] product);             // 16 位元輸出結果

	wire signed [7:0] Q[0:6];                   // 8 位元 Q 陣列，儲存中間結果
	wire signed [7:0] acc[0:7];                 // 8 位元累加器陣列
	wire signed[7:0] q0;                        // Q 的上一位 (q-1)
	wire qout;                                  // 無符號進位位
	
	assign acc[0] = 8'b00000000;                // 初始化累加器為 0
	
	// 按步驟進行 Booth 演算法的操作
	booth_substep step1(acc[0], multiplier, 1'b0, multiplicand, acc[1],        Q[0],         q0[1]);
	booth_substep step2(acc[1], Q[0],      q0[1], multiplicand, acc[2],        Q[1],         q0[2]);
	booth_substep step3(acc[2], Q[1],      q0[2], multiplicand, acc[3],        Q[2],         q0[3]);
	booth_substep step4(acc[3], Q[2],      q0[3], multiplicand, acc[4],        Q[3],         q0[4]);
	booth_substep step5(acc[4], Q[3],      q0[4], multiplicand, acc[5],        Q[4],         q0[5]);
	booth_substep step6(acc[5], Q[4],      q0[5], multiplicand, acc[6],        Q[5],         q0[6]);
	booth_substep step7(acc[6], Q[5],      q0[6], multiplicand, acc[7],        Q[6],         q0[7]);
	booth_substep step8(acc[7], Q[6],      q0[7], multiplicand, product[15:8], product[7:0], qout);
	
	 
endmodule
