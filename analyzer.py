#!/usr/bin/env python3
"""
Log Analyzer - Simple wrapper to delegate to the proper package.
This file exists for backward compatibility with direct python analyzer.py usage.
For full functionality, use: log-analyzer <directory> or python -m log_analyzer <directory>
"""

import sys
import os

# Add the src directory to the path so we can import log_analyzer
script_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(script_dir, 'src')
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

# Delegate to the proper main entry point
if __name__ == "__main__":
    from log_analyzer.__main__ import main
    main()