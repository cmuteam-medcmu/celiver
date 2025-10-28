import os
import sys
import argparse

import numpy as np
import pandas as pd

def main():
    with open("output.txt", "w") as f:
        f.write("Hello from Docker!")

if __name__ == "__main__":
    main()