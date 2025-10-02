`timescale 1ns/1ps  // 設置時間單位為1ns，精度為1ps

module tb_booth();
  reg                clk;
  reg                rst_n;
  reg  signed [31:0] a; 
  reg  signed [31:0] b;
  reg                en;
  wire               done_sig;
  wire signed [63:0] product;

  booth_multiplier UUT(
    .clkSys(clk), 
    .rst_n(rst_n), 
    .en(en), 
    .a(a), 
    .b(b), 
    .product(product), 
    .done(done_sig)
  );

  initial begin
    // 設定VCD波形輸出
    $dumpfile("tb.vcd");  // 設置輸出波形文件名
    $dumpvars(1, tb_booth.UUT);  // 只包含 DUT 內的信號
    //$dumpvars(0, tb_booth);  // 輸出testbench中的所有信號

    // 初始化信號
    clk = 0;
    rst_n = 0;
    a = 0;
    b = 0;
    en = 0;
    
    // 先進行reset
    repeat(5) @(posedge clk) rst_n = 0;
    #10 rst_n = 1;  // 在10ns後啟動reset

    // 開始測試
    test(32'd1, -32'd1);
    test(-32'd2, -32'd2);
    test(32'd3, -32'd3);
    test(32'd4, -32'd4);
    test(32'd5, -32'd5);
    test(32'd6, 32'd6);
    test(-32'd7, -32'd7);
    test(32'd8, -32'd8);
    test(32'd9, -32'd9);
    test(32'd10, -32'd10);
    // 更多測試數據...
    #1000 $stop;  // 停止仿真
  end

  always #10 clk = ~clk;  // 產生時鐘信號

  // 測試任務
  task test;
    input signed [31:0] in1;
    input signed [31:0] in2;
    begin
      a = in1;
      b = in2;
      @(posedge clk) en = 1;  // 在時鐘的上升沿啟動
      @(posedge clk) en = 0;  // 下一個上升沿停止
      wait (done_sig == 1);   // 等待完成

      // 顯示輸入輸出
      $display("Test: a = %d, b = %d, product = %d, done = %b", a, b, product, done_sig);
    end
  endtask

endmodule
