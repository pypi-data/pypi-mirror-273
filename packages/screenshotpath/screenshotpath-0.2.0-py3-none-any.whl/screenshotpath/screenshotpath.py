#!/usr/bin/env python3
import argparse
import subprocess
import os

def main():
    """
    usage: screenshot_utility.py [-h] [--get] [--set NEW_LOCATION]

    optional arguments:
    -h, --help           show this help message and exit
    --get                Retrieve the current screenshot location
    --set NEW_LOCATION   Set a new screenshot location
    """

    parser = argparse.ArgumentParser(description="Change macOS screenshot path.")
    parser.add_argument("--get", action="store_true", help="Retrieve the current screenshot location")
    parser.add_argument('--set', help="Set a new screenshot location based on the absolute path provided.")

    args = parser.parse_args()
    # Runs the program
    if args.get:
        screenshot_location = get_screenshot_location()
        if screenshot_location:
            print("Current screenshots directory: ", screenshot_location)
    elif args.set:
        change_screenshot_location(args.location)
    else:
        print("No action specified. Use --get to retrieve the current screenshot location or --set to set a new location.")

def get_screenshot_location():
    try:
        # Run the defaults command to get the screenshot location
        result = subprocess.run(["defaults", "read", "com.apple.screencapture", "location"],
                                capture_output=True, text=True, check=True)
        
        # Extract the path from the command output
        location_path = result.stdout.strip()
        
        return location_path
    except subprocess.CalledProcessError:
        print("Error: Unable to retrieve screenshot location.")
        return None

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