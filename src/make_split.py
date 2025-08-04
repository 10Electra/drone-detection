import os
import sys
import shutil
import argparse
from pathlib import Path

"""Short script to help me build a YOLO-friendly datset from FRED"""

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--subdir_pair", required=True,
                    help="format IMAGES:LABELS e.g. RGB:RGB_YOLO")
    ap.add_argument("--split_file", required=True)
    ap.add_argument("--dest", required=True)
    ap.add_argument("--link", action="store_true",
                    help="symlink instead of copy to save disk")
    ap.add_argument("--relative", action="store_true",
                    help="make relative symlinks (implies --link)")
    args = ap.parse_args()
    if args.relative:
        args.link = True

    img_sub, lbl_sub = args.subdir_pair.split(":")
    root = Path(args.root)
    dest_img = Path(args.dest) / "images" / Path(args.split_file).stem
    dest_lbl = Path(args.dest) / "labels" / Path(args.split_file).stem
    dest_img.mkdir(parents=True, exist_ok=True)
    dest_lbl.mkdir(parents=True, exist_ok=True)

    ids = [line.strip().rstrip("/") for line in open(args.split_file)]
    for cid in ids:
        src_img_dir = root / cid / img_sub
        src_lbl_dir = root / cid / lbl_sub
        if not src_img_dir.exists():
            print(f"[WARN] {src_img_dir} missing; skipped", file=sys.stderr)
            continue
        for img_path in src_img_dir.iterdir():
            if not img_path.is_file():
                continue
            stem = img_path.stem
            lbl_path = src_lbl_dir / (stem + ".txt")
            if not lbl_path.exists():
                print(f"[WARN] label missing for {img_path}", file=sys.stderr)
                continue
            new_name = f"{cid}_{img_path.name}"
            tgt_img = dest_img / new_name
            tgt_lbl = dest_lbl / (cid + "_" + stem + ".txt")

            if args.link:
                def _link(src, dst):
                    if args.relative:
                        rel = os.path.relpath(src, start=dst.parent)
                        os.symlink(rel, dst)
                    else:
                        os.symlink(src, dst)
                _link(img_path, tgt_img)
                _link(lbl_path, tgt_lbl)
            else:
                shutil.copy2(img_path, tgt_img)
                shutil.copy2(lbl_path, tgt_lbl)

if __name__ == "__main__":
    main()
