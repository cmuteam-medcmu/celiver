#!/bin/bash

# Set all paths
compose_path="docker-compose.yaml" 
output_dir="test" # This for testing, can be changed as needed

# Run the celiver container with input and predicted file arguments
#docker compose -f $compose_path \
    # -v $output_dir:/output \
    # run --rm \
    # celiver \
    # -i dataset/true_label.csv \
    # -p celiver \
    # -o /output

# Run the celiver container with config file argument
docker compose -f $compose_path \
    run --rm \
    -v $output_dir:/output \
    celiver \
    -c test/config.yaml \
    -o /output
