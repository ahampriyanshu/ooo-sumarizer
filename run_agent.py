#!/usr/bin/env python3
"""
Wrapper script to run the OOO Summarizer Agent without asyncio cleanup errors
"""

import subprocess
import sys
import os

def main():
    """Run the agent with stderr redirected to suppress cleanup errors"""
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    main_script = os.path.join(script_dir, "main.py")
    
    # Run the main script with stderr redirected to suppress asyncio cleanup errors
    result = subprocess.run([sys.executable, main_script], 
                          stderr=subprocess.DEVNULL,
                          text=True)
    
    # Exit with the same code
    sys.exit(result.returncode)

if __name__ == "__main__":
    main()
