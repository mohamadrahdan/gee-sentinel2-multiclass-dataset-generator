import os
import argparse
import subprocess

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True, help="e.g. username/dataset-name")
    ap.add_argument("--dest", default="./data", help="download destination")
    args = ap.parse_args()

    os.makedirs(args.dest, exist_ok=True)
    cmd = ["kaggle", "datasets", "download", "-d", args.slug, "-p", args.dest, "--unzip"]
    subprocess.run(cmd, check=True)
    print(f"Downloaded & unzipped into: {args.dest}")

if __name__ == "__main__":
    main()
