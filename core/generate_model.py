import sys
import tensorflow as tf
import numpy as np

if len(sys.argv) < 2:
    print("Error: Please provide a model filename.")
    sys.exit(1)

model_path = sys.argv[1]
model = tf.keras.models.load_model(model_path)

def generate_main_c(model, filename="main.c"):
    with open(filename, "w") as f:
        # 1. Write Headers
        f.write('#include <stdio.h>\n#include "esp_log.h"\n#include "esp_dsp.h"\n#include "model_data.h"\n#include <string.h>\n\n')
        f.write('static const char *TAG = "TINYML_INFERENCE";\n\n')
        f.write('void app_main(void) {\n')
        f.write('    ESP_LOGI(TAG, "Starting generated neural network...");\n\n')

        # 2. Dynamic Buffer Allocation (RAM)
        f.write('    // --- RAM Buffers ---\n')
        
        # We need to track dimensions to create buffers between layers
        layer_dims = []
        for i, layer in enumerate(model.layers):
            if len(layer.get_weights()) > 0:
                w, b = layer.get_weights()
                # In Keras Dense: w.shape is (input_dim, output_dim)
                layer_dims.append((w.shape[0], w.shape[1]))

        # Create buffers: we need an input for the first layer and outputs for all
        f.write(f'    int16_t x0[1][{layer_dims[0][0]}] = {{0}}; // Input\n')
        for i, dims in enumerate(layer_dims):
            f.write(f'    int16_t x{i+1}[1][{dims[1]}]; // Output of Layer {i}\n')
            f.write(f'    int16_t y{i+1}[1][{dims[1]}]; // After Bias {i}\n')
        
        f.write('\n    // --- Inference Pipeline ---\n')

        # 3. Generate Layer Calls
        current_input = "x0"
        for i, (in_dim, out_dim) in enumerate(layer_dims):
            f.write(f'    // Layer {i}: Dense ({in_dim} -> {out_dim})\n')
            
            # Matrix Multiplication
            f.write(f'    dspm_mult_s16((int16_t*){current_input}, (int16_t*)layer_{i}_weights, (int16_t*)x{i+1}, 1, {in_dim}, {out_dim}, 15);\n')
            
            # Bias Add
            f.write(f'    dsps_add_s16((int16_t*)x{i+1}, (int16_t*)layer_{i}_biases, (int16_t*)y{i+1}, {out_dim}, 1, 1, 1, 0);\n')
            
            # ReLU Activation
            f.write(f'    for(int i = 0; i < {out_dim}; i++) {{ if(y{i+1}[0][i] < 0) y{i+1}[0][i] = 0; }}\n')
            
            # The output of this layer is the input for the next
            current_input = f"y{i+1}"
            f.write('\n')

        f.write(f'    ESP_LOGI(TAG, "Inference Complete. Final Output: %d", {current_input}[0][0]);\n')
        f.write('}\n')

generate_main_c(model)
print("main.c generated successfully.")
