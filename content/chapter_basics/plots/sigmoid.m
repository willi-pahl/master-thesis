% SIGMOID function.
x = -5:0.1:5;

function result = sig(x)
  result = 1./(1+ exp(-x));
endfunction

figure('Position', [10, 100, 1000, 600]);

plot (x, sig(x));
xlabel ("x");
ylabel ("sigmoid (x)");
title ("Sigmoid function");

grid on;
grid minor;

