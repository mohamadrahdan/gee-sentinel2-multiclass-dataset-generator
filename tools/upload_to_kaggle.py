import os
import argparse
import subprocess
from pathlib import Path

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True, help="username/dataset-name")
    ap.add_argument("--dir", default="./outputs", help="folder to upload")
    ap.add_argument("--title", default="GEE S2 Multiclass Dataset", help="dataset title")
    ap.add_argument("--public", action="store_true", help="make dataset public")
    ap.add_argument("--init", action="store_true", help="create dataset first time")
    ap.add_argument("--message", default="update dataset", help="version message")
    args = ap.parse_args()

    Path(args.dir).mkdir(parents=True, exist_ok=True)

    if args.init:
        # Initial create
        visibility = "public" if args.public else "private"
        cmd = [
            "kaggle", "datasets", "create",
            "-p", args.dir,
            "-u", args.slug,
            "-t", args.title,
            "-r", "zip",
            "-w", visibility
        ]
        subprocess.run(cmd, check=True)
        print("Dataset created on Kaggle.")
    else:
        # New version
        cmd = [
            "kaggle", "datasets", "version",
            "-p", args.dir,
            "-m", args.message,
            "-r", "zip"
        ]
        subprocess.run(cmd, check=True)
        print("Dataset version uploaded.")

if __name__ == "__main__":
    main()
