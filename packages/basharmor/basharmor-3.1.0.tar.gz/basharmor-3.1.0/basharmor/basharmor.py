import subprocess
import sys
import argparse
import base64
from .obsf import encrypt_file


    






def run_bash_script(file_name):
    try:
        subprocess.run([".load", file_name], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error during Bash script execution: {e}")

def obfuscate_script(file_name):
    # Implement the obfuscation logic here
    # This is just a placeholder function
    print(f"Obfuscating the bash script: {file_name}")

def main():
    parser = argparse.ArgumentParser(description="Bash Armor: A tool to execute bash scripts with armor.")
    parser.add_argument("file_name", nargs='?', help="Name of the bash script to execute")
    parser.add_argument("--enc", action="store_true", help="Run the bash script")
    parser.add_argument("--obfuscate", action="store_true", help="Obfuscate the bash script")
    parser.add_argument("--helpinfo", action="store_true", help="Show help information and exit")
    parser.add_argument("--version", action="store_true", help="Show version information and exit")
    parser.add_argument("--about", action="store_true", help="Show about information and exit")
    args = parser.parse_args()

    if args.helpinfo:
        parser.print_help()
        sys.exit()

    if args.version:
        print("Bash Armor version 3.0.0 lts")
        sys.exit()

    if args.about:
        print("Bash Armor is a tool to execute bash scripts with armor.")
        print("Don't forget to donate for me. Dana ID: 085876736579")
        print("Author: Aji permana")
        sys.exit()

    if args.enc:
        if not args.file_name:
            print("Error: Please provide the file name.")
            sys.exit(1)
        print("Encrypting the bash script...")
        run_bash_script(args.file_name)
        sys.exit()

    if args.obfuscate:
        if not args.file_name:
            print("Error: Please provide the file name.")
            sys.exit(1)
        encrypt_file(args.file_name, args.file_name)
        sys.exit()

if __name__ == "__main__":
    main()

