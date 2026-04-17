import sys
import tensorflow as tf
import numpy as np

if len(sys.argv) < 2:
    print("Error: Please provide a model filename.")
    sys.exit(1)

model_path = sys.argv[1]
model = tf.keras.models.load_model(model_path)

def to_q15(weights):
    # Scale float to Q1.15: val * 2^15
    q_weights = np.round(weights * 32768).astype(np.int32)
    return np.clip(q_weights, -32768, 32767).astype(np.int16)

header_file = "model1_data.h"

with open(header_file, "w") as f:
    f.write("#ifndef MODEL_DATA_H\n#define MODEL_DATA_H\n\n")
    f.write("#include <stdint.h>\n\n")
    f.write("// Weights stored in Q1.15 fixed-point format\n")
    f.write("#define FLASH_ALIGNED __attribute__((aligned(4))) __attribute__((section(\".rodata\")))\n\n")
    
    for i, layer in enumerate(model.layers):
        weights_list = layer.get_weights()
        if len(weights_list) > 0:
            weights, biases = weights_list
            
            # Convert to Q1.15
            q_weights = to_q15(weights)
            q_biases = to_q15(biases)
            
            # 1. Write Weights as a 2D Array
            # weights.shape gives (rows, cols)
            rows, cols = q_weights.shape
            f.write(f"const int16_t layer_{i}_weights[{rows}][{cols}] FLASH_ALIGNED = {{\n")
            
            for r in range(rows):
                f.write("    {" + ", ".join(map(str, q_weights[r])) + "}")
                if r < rows - 1:
                    f.write(",\n")
            f.write("\n};\n\n")
            
            # 2. Write Biases (Usually 1D in Keras, keeping as 1D)
            f.write(f"const int16_t layer_{i}_biases[{len(q_biases)}] FLASH_ALIGNED = {{\n")
            f.write("    " + ", ".join(map(str, q_biases)))
            f.write("\n};\n\n")

    f.write("#endif\n")

print(f"Fixed-point header '{header_file}' created with 2D arrays and FLASH_ALIGNED.")