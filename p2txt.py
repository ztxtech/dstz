import os
import glob
import shutil
import argparse


def export_package_code_to_txt(package_path, output_file):
    """
    Export all code from a specified Python package to a single text file.

    Parameters:
    - package_path (str): The path to the Python package.
    - output_file (str): The path to the output text file.
    """
    # Ensure the output directory exists
    output_dir = os.path.dirname(output_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Use glob to iterate through all .py files in the package path
    python_files = glob.glob(os.path.join(package_path, '**', '*.py'), recursive=True)

    with open(output_file, 'w', encoding='utf-8') as outfile:
        for file_path in python_files:
            # Read each file's content and write to the output file
            with open(file_path, 'r', encoding='utf-8') as infile:
                # Prefix each file's content with its name for reference
                outfile.write(f"--- {os.path.basename(file_path)} ---\n")
                shutil.copyfileobj(infile, outfile)
                # Separate contents of different files with blank lines
                outfile.write("\n\n")


def main():
    # Create argument parser
    parser = argparse.ArgumentParser(description="Export all Python code from a package to a text file.")
    parser.add_argument("package_path", help="Path to the Python package.")
    parser.add_argument("output_file", help="Path to the output text file.")

    args = parser.parse_args()

    export_package_code_to_txt(args.package_path, args.output_file)
    print("Export completed.")


if __name__ == "__main__":
    main()
