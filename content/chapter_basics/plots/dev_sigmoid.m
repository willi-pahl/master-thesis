% SIGMOID function.
##
#
# <include>activation_functions.m</include>
#
x = -5:0.1:5;

function result = sig(x)
  result = 1./(1+ exp(-x));
endfunction

function result = dev_sig(x)
  result = sig(x).*(1 - sig(x))
endfunction

figure('Position', [10, 100, 1000, 600]);

plot (x, dev_sig(x));
xlabel ("x");
ylabel ("sig' (x)");
title ("Sigmoid dervation function");

grid on;
grid minor;

