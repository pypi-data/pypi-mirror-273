#!/usr/bin/env python3
import argparse
import subprocess
import os

def main():
    parser = argparse.ArgumentParser(description="Change macOS screenshot path.")
    # Required:
    requiredNamed = parser.add_argument_group('required named arguments')
    requiredNamed.add_argument('location', 
                               help="the absolute path to your screenshot location (will be prompted to create directory if path not found)")

    args = parser.parse_args()
    # Runs the program
    change_screenshot_location(args.location)

def change_screenshot_location(new_path):
    # Check if the directory exists
    if not os.path.exists(new_path):
        # Ask the user if they want to create the directory
        user_input = input(f"The directory {new_path} does not exist. Do you want to create it? (y/[N]): ")
        if user_input.lower() != 'y':
            print("Directory not created. Exiting without changing screenshot location.")
            return
        try:
            # Create the directory
            os.makedirs(new_path, exist_ok=True)
            print(f"Directory {new_path} created.")
        except OSError as e:
            print(f"Failed to create directory: {e}")
            return

    try:
        # Change the default screenshot location
        subprocess.run([
            'defaults', 'write', 'com.apple.screencapture', 'location', new_path
        ], check=True)

        # Restart the SystemUIServer to apply changes
        subprocess.run(['killall', 'SystemUIServer'], check=True)

        print(f"Screenshot location changed to {new_path}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()