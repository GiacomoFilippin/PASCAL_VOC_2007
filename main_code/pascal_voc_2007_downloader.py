"""
Utility script to fetch the PASCAL VOC 2007 dataset via Kaggle and place it under data/processed.
- Requires kagglehub (`pip install kagglehub`).
- Will create data/processed if missing.
- Copies extracted contents; skips files that already exist.
"""
from __future__ import annotations

import os
import shutil
import tarfile
import zipfile
from pathlib import Path

import kagglehub

DATASET_SLUG = "zaraks/pascal-voc-2007"
TARGET_SUBDIR = Path("data") / "processed"
EXPECTED_FILES = [
    "pascal_train2007.json",
    "pascal_val2007.json",
    "pascal_test2007.json",
]


def find_repo_root(start: Path | None = None) -> Path:
    start = (start or Path.cwd()).resolve()
    for candidate in [start, *start.parents]:
        if (candidate / "data" / "processed").exists():
            return candidate
    return Path.cwd().resolve()


def _copy_contents(src: Path, dst: Path) -> None:
    dst.mkdir(parents=True, exist_ok=True)
    for item in src.iterdir():
        dest_item = dst / item.name
        if item.is_dir():
            if not dest_item.exists():
                shutil.copytree(item, dest_item)
        else:
            if not dest_item.exists():
                shutil.copy2(item, dest_item)


def _extract_if_archive(archive_path: Path) -> Path:
    base = archive_path.parent
    if archive_path.suffix.lower() == ".zip":
        with zipfile.ZipFile(archive_path, "r") as z:
            z.extractall(base)
    else:
        try:
            with tarfile.open(archive_path, "r:*") as t:
                t.extractall(base)
        except tarfile.TarError:
            pass
    return base


def download_and_place() -> Path:
    repo_root = find_repo_root()
    target_dir = repo_root / TARGET_SUBDIR
    target_dir.mkdir(parents=True, exist_ok=True)

    print(f"Repo root: {repo_root}")
    print(f"Target dir: {target_dir}")

    download_path = Path(kagglehub.dataset_download(DATASET_SLUG, force_download=False))
    print(f"Downloaded to: {download_path}")

    if download_path.is_file():
        extracted_base = _extract_if_archive(download_path)
        _copy_contents(extracted_base, target_dir)
    else:
        _copy_contents(download_path, target_dir)

    missing = [f for f in EXPECTED_FILES if not (target_dir / f).exists()]
    if missing:
        print("Warning: missing files after copy:", missing)
    else:
        print("All expected JSON files present:", ", ".join(EXPECTED_FILES))

    return target_dir


def main() -> None:
    download_and_place()


if __name__ == "__main__":
    main()
