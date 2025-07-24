import argparse
from pathlib import Path
import shutil
import sys

def copy_selected_files(input_folder_path: str):
    input_path = Path(input_folder_path).resolve()

    if not input_path.is_dir():
        raise ValueError(f"Input path '{input_folder_path}' is not a valid directory.")

    parts = input_path.parts
    if "CS+_CCRL" not in parts:
        raise ValueError("The input path does not contain 'CS+_CCRL'.")

    build_index = parts.index("CS+_CCRL")
    output_path = Path(*parts[:build_index - 2]) / "output_files"
    destination_path = output_path / input_path.name

    # Clear destination if it exists
    if destination_path.exists():
        print(f"Destination '{destination_path}' already exists. Replacing it.")
        shutil.rmtree(destination_path)

    destination_path.mkdir(parents=True, exist_ok=True)

    # Copy only *.rbin or *production.hex
    matched_files = list(input_path.rglob("*.rbin")) + list(input_path.rglob("*production.hex"))

    if not matched_files:
        print("No .rbin or production.hex files found.")
        return

    for file in matched_files:
        rel_path = file.relative_to(input_path)
        target_file_path = destination_path / rel_path
        target_file_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(file, target_file_path)

    print(f"Copied {len(matched_files)} file(s) to: {destination_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Copy only .rbin or *production.hex files to output_files folder.")
    parser.add_argument("input_folder", help="Full path of the folder to be copied.")
    args = parser.parse_args()

    try:
        copy_selected_files(args.input_folder)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
