#!/bin/bash

# Set the path to your docker-compose file
compose_path="./docker-compose.yaml"
output_dir="./test"

# Run the celiver container with input and predicted file arguments
#docker compose -f $compose_path \
    # -v $output_dir:/output \
    # -v $(pwd):/app \
    # run --rm \
    # celiver \
    # -i dataset/true_label.csv \
    # -p predicted \
    # -o /output

# Run the celiver container with config file argument
docker compose -f $compose_path \
    run --rm \
    -v $output_dir:/output \
    -v $(pwd):/app \
    celiver \
    -c test_config.yaml \
    -o /output
