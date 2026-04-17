#!/bin/bash

# Usage: ./deploy.sh my_model.keras project_name
MODEL_NAME=$1
PROJECT_NAME=$2

if [ -z "$MODEL_NAME" ] || [ -z "$PROJECT_NAME" ]; then
    echo "Usage: ./deploy.sh <model_name.keras> <project_name>"
    exit 1
fi

echo "--- Step 1: Generating C Header and Main Logic ---"
# These scripts now use sys.argv[1] to take the model name
python3 core/generate_header.py "$MODEL_NAME"
python3 core/generate_main.py "$MODEL_NAME"

echo "--- Step 2: Creating ESP-IDF Project ---"
# Use the official toolchain to create the structure
idf.py create-project "$PROJECT_NAME"

echo "--- Step 3: Integrating Generated Files ---"
# Move files into the 'main' directory of the newly created project
mv model_data.h "$PROJECT_NAME/main/"
mv main.c "$PROJECT_NAME/main/"

echo "--- Done! ---"
echo "Project '$PROJECT_NAME' is ready."
echo "Navigate to the folder and run: cd $PROJECT_NAME && idf.py build"