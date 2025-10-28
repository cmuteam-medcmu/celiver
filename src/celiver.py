import os
import sys
import yaml
import argparse
from pathlib import Path


class CEliver:
    def __init__(self, input_path: str, output_dir: str, output_prefix: str, from_raw: bool = True, validate_path: str = None):
        if output_dir == 'pwd':
            output_dir = os.getcwd()

        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Input file {input_path} does not exist.")
        if not os.path.exists(output_dir):
            raise FileNotFoundError(f"Output directory {output_dir} does not exist.")
        if validate_path and not os.path.exists(validate_path):
            raise FileNotFoundError(f"Validation file {validate_path} does not exist.")
        
        self.input_path = input_path
        self.output_dir = output_dir
        self.output_prefix = output_prefix
        self.from_raw = from_raw
        self.validate_path = validate_path

    @classmethod
    def from_args(cls, args: argparse.Namespace):
        parser = argparse.ArgumentParser(description="CEliver Model")
        parser.add_argument('-i','--input', type=str, help='Input file path')
        parser.add_argument('-o','--outdir', type=str, default='pwd', help='Output directory')
        parser.add_argument('-p','--prefix', type=str, default='celiver', help='Output file prefix')
        parser.add_argument('-r','--fromraw', action='store_true', help='Indicate if input is raw data')
        parser.add_argument('-v','--validate', type=str, default=None, help='Validation file path')
        parser.add_argument('-c','--config', type=str, default=None, help='Configuration file path')
        args = parser.parse_args(args)

        if args.config:
            return cls.from_config(args.config)

        return cls(
            input_path=args.input,
            output_dir=args.outdir,
            output_prefix=args.prefix,
            from_raw=args.fromraw,
            validate_path=args.validate
        )
    
    @classmethod
    def from_config(cls, config_path: str):
        with open(config_path, 'r') as config_file:
            config = yaml.safe_load(config_file)
        
        input_path = config.get('input', None)
        output_dir = config.get('outdir', 'pwd')
        output_prefix = config.get('prefix', 'celiver')
        from_raw = config.get('fromraw', True)
        validate_path = config.get('validate', None)

        return cls(
            input_path=input_path,
            output_dir=output_dir,
            output_prefix=output_prefix,
            from_raw=from_raw,
            validate_path=validate_path
        )
    
    def print_settings(self):
        print(f"Loading all paths")
        print(f"\u2560\u2550 Input file: {self.input_path}")
        print(f"\u2560\u2550 Output prefix: {self.output_prefix}")
        if self.validate_path:
            print(f"\u2560\u2550 Output directory: {self.output_dir}")
            print(f"\u255A\u2550 Validation file: {self.validate_path}")
        else:
            print(f"\u255A\u2550 Output directory: {self.output_dir}")
    
    def run(self):
        import pandas as pd
        from features_2d import Extract2DFeatures

        BASE_ROOT = Path(__file__).resolve().parent.parent
        MODEL_PATH = BASE_ROOT / "src" / "model" / "CEliver_model.sav"
        SCALER_PATH = BASE_ROOT / "src" / "model" / "MinMaxScaler.sav"
        KBEST_PATH = BASE_ROOT / "src" / "model" / "KBest.sav"

        print("\nLoading dataset...")
        data = pd.read_csv(self.input_path)
        if self.from_raw:
            feature_extractor = Extract2DFeatures.from_raw(data)
        else:
            feature_extractor = Extract2DFeatures(data)
        print(f"\u255A\u2550 Dataset loaded with {data.shape[0]} samples")

        print("\nExtracting features...")
        features_df = feature_extractor.extract_features()

        print("\nLoading model and making predictions...")
        from joblib import load
        model = load(MODEL_PATH)
        scaler = load(SCALER_PATH)
        kbest = load(KBEST_PATH) 
        features_scaled = scaler.transform(features_df.iloc[:, 1:])
        features_kbest = kbest.transform(features_scaled)

        predictions = model.predict(features_kbest)
        
        if self.validate_path:
            true_labels = pd.read_csv(self.validate_path)
            from sklearn.metrics import classification_report
            print("\nValidation Report:")
            print(classification_report(true_labels, predictions))
        
        print("\nSaving predictions...")
        output_path = os.path.join(self.output_dir, f"{self.output_prefix}_predictions.csv")
        pd.DataFrame(predictions, columns=['Prediction']).to_csv(output_path, index=False)
        print(f"\u255A\u2550 Predictions saved to {output_path}")
        

def main():
    print(r"""
 ██████╗███████╗██╗     ██╗██╗   ██╗███████╗██████╗ 
██╔════╝██╔════╝██║     ██║██║   ██║██╔════╝██╔══██╗
██║     █████╗  ██║     ██║██║   ██║█████╗  ██████╔╝
██║     ██╔══╝  ██║     ██║╚██╗ ██╔╝██╔══╝  ██╔══██╗
╚██████╗███████╗███████╗██║ ╚████╔╝ ███████╗██║  ██║
 ╚═════╝╚══════╝╚══════╝╚═╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝
          
  CEliver © 2025 by Cancer Research Unit, CMUTEAM, 
    Faculty of Medicine, Chiang Mai University                                                    
    """)                                                          
                                                                        
    celiver = CEliver.from_args(sys.argv[1:])
    celiver.print_settings()
    celiver.run()

if __name__ == "__main__":
    main()