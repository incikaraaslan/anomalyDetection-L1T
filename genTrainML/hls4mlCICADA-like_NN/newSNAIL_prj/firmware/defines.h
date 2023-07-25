#ifndef DEFINES_H_
#define DEFINES_H_

#include "ap_fixed.h"
#include "ap_int.h"
#include "nnet_utils/nnet_types.h"
#include <cstddef>
#include <cstdio>

// hls-fpga-machine-learning insert numbers
#define N_INPUT_1_1 18
#define N_INPUT_2_1 14
#define N_INPUT_3_1 1
#define OUT_HEIGHT_2 9
#define OUT_WIDTH_2 7
#define N_FILT_2 4
#define OUT_HEIGHT_2 9
#define OUT_WIDTH_2 7
#define N_FILT_2 4
#define N_SIZE_0_4 252
#define N_LAYER_5 20
#define N_LAYER_5 20
#define N_LAYER_7 1
#define N_LAYER_7 1

// hls-fpga-machine-learning insert layer-precision
typedef ap_fixed<16,6> input_t;
typedef ap_fixed<16,6> model_default_t;
typedef ap_fixed<16,6> layer2_t;
typedef ap_fixed<16,6> layer3_t;
typedef ap_fixed<18,8> conv2d_relu_table_t;
typedef ap_fixed<16,6> layer5_t;
typedef ap_uint<1> layer5_index;
typedef ap_fixed<16,6> layer6_t;
typedef ap_fixed<18,8> dense_relu_table_t;
typedef ap_fixed<16,6> layer7_t;
typedef ap_uint<1> layer7_index;
typedef ap_fixed<16,6> result_t;
typedef ap_fixed<18,8> dense_1_relu_table_t;

#endif
