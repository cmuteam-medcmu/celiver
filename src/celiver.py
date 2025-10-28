import os
import sys
import yaml
import argparse

import numpy as np
import pandas as pd


def argument():
    argparser = argparse.ArgumentParser(description="CEliver Model")
    argparser.add_argument('-i','--input', type=str, help='Input file path')
    argparser.add_argument('-p','--prefix', type=str, default='celiver_output', help='Output file prefix')
    argparser.add_argument('-o','--outdir', type=str, default='pwd', help='Output directory')
    argparser.add_argument('-c','--config', type=str, default=None, help='Configuration file path')
    args = argparser.parse_args()

    # Setting 
    if args.config is not None:

        with open(args.config, 'r') as config_file:
            config = yaml.safe_load(config_file)

            # Use config values if provided
            if 'input' in config:
                args.input = config['input']
            if 'prefix' in config:
                args.prefix = config['prefix']
    else:
        if args.outdir == 'pwd':
            args.outdir = os.getcwd()
    
    print(f"Loading all paths")
    print(f"\u2560\u2550 Input file: {args.input}")
    print(f"\u2560\u2550 Output prefix: {args.prefix}")
    print(f"\u255A\u2550 Output directory: {args.outdir}")
    
    return args


def main():
    args = argument()

    with open(f"{args.outdir}/{args.prefix}.predict.txt", 'w') as outfile:
        outfile.write("This is a placeholder for the main CEliver functionality.\n")
        outfile.close()

if __name__ == "__main__":
    main()