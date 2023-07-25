#include <iostream>

#include "myproject.h"
#include "parameters.h"

void myproject(
    input_t conv2d_input[N_INPUT_1_1*N_INPUT_2_1*N_INPUT_3_1],
    result_t layer8_out[N_LAYER_7]
) {

    // hls-fpga-machine-learning insert IO
    #pragma HLS ARRAY_RESHAPE variable=conv2d_input complete dim=0
    #pragma HLS ARRAY_PARTITION variable=layer8_out complete dim=0
    #pragma HLS INTERFACE ap_vld port=conv2d_input,layer8_out 
    #pragma HLS DATAFLOW 

#ifndef __SYNTHESIS__
    static bool loaded_weights = false;
    if (!loaded_weights) {
        // hls-fpga-machine-learning insert load weights
        nnet::load_weights_from_txt<model_default_t, 36>(w2, "w2.txt");
        nnet::load_weights_from_txt<model_default_t, 4>(b2, "b2.txt");
        nnet::load_weights_from_txt<model_default_t, 5040>(w5, "w5.txt");
        nnet::load_weights_from_txt<model_default_t, 20>(b5, "b5.txt");
        nnet::load_weights_from_txt<model_default_t, 20>(w7, "w7.txt");
        nnet::load_weights_from_txt<model_default_t, 1>(b7, "b7.txt");
        loaded_weights = true;
    }
#endif

    // ****************************************
    // NETWORK INSTANTIATION
    // ****************************************

    // hls-fpga-machine-learning insert layers

    layer2_t layer2_out[OUT_HEIGHT_2*OUT_WIDTH_2*N_FILT_2];
    #pragma HLS ARRAY_PARTITION variable=layer2_out complete dim=0
    nnet::conv_2d_cl<input_t, layer2_t, config2>(conv2d_input, layer2_out, w2, b2); // conv2d

    layer3_t layer3_out[OUT_HEIGHT_2*OUT_WIDTH_2*N_FILT_2];
    #pragma HLS ARRAY_PARTITION variable=layer3_out complete dim=0
    nnet::relu<layer2_t, layer3_t, relu_config3>(layer2_out, layer3_out); // conv2d_relu

    auto& layer4_out = layer3_out;
    layer5_t layer5_out[N_LAYER_5];
    #pragma HLS ARRAY_PARTITION variable=layer5_out complete dim=0
    nnet::dense<layer3_t, layer5_t, config5>(layer4_out, layer5_out, w5, b5); // dense

    layer6_t layer6_out[N_LAYER_5];
    #pragma HLS ARRAY_PARTITION variable=layer6_out complete dim=0
    nnet::relu<layer5_t, layer6_t, relu_config6>(layer5_out, layer6_out); // dense_relu

    layer7_t layer7_out[N_LAYER_7];
    #pragma HLS ARRAY_PARTITION variable=layer7_out complete dim=0
    nnet::dense<layer6_t, layer7_t, config7>(layer6_out, layer7_out, w7, b7); // dense_1

    nnet::relu<layer7_t, result_t, relu_config8>(layer7_out, layer8_out); // dense_1_relu

}
