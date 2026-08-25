# Medium Priority Enhancements Design
**Date**: 2026-08-26

## Overview
This document outlines the implementation plan for four medium priority enhancements to the log analyzer project:
1. Documentation completion (docs/ directory)
2. Proper test organization and unit test creation
3. Directory read permission checking
4. Log file cleanup mechanism

## 1. Documentation Completion

### Problem
The docs/ directory exists but is empty. While README.md and CHANGELOG.md have been updated, separate documentation files are needed for better organization.

### Solution
Create three documentation files in the docs/ directory:

#### docs/usage.md
- Command line interface reference
- Detailed usage examples
- Feature explanations
- Output format descriptions

#### docs/api_reference.md
- Auto-generated or manually curated API reference
- Module-by-module breakdown
- Function signatures and descriptions
- Based on existing docstrings

#### docs/release_notes.md
- Versioned release notes
- Summarized changes from CHANGELOG.md
- Upgrade instructions if needed

### Implementation Approach
- Create usage.md by expanding README.md with more detailed examples
- Create api_reference.md by extracting and formatting docstrings from all modules
- Create release_notes.md as a condensed version of CHANGELOG.md with version grouping

## 2. Test Organization and Unit Tests

### Problem
Test files are mixed in the project root and tests/ directory lacks proper unit test structure. While test data has been organized into tests/test_formats/, no actual test modules (using pytest/unittest) exist.

### Solution
Create proper unit test modules in the tests/ directory:

#### tests/test_csv_handler.py
- Test CSV header detection logic
- Test various CSV formats (with/without headers, different delimiters)
- Test edge cases (empty files, malformed data)

#### tests/test_json_handler.py
- Test JSON Lines parsing resilience
- Test JSON array parsing
- Test invalid line handling
- Test message/level extraction

#### tests/test_text_handler.py
- Test plain text log processing
- Test ERROR/WARNING detection

#### tests/test_advanced_analyzer.py
- Test time series analysis functions
- Test error pattern detection
- Test anomaly detection algorithms
- Test correlation analysis

#### tests/test_main.py
- Test command line argument parsing
- Test main function integration
- Test output formatting options

### Implementation Approach
- Use unittest framework (standard library) to avoid external dependencies
- Each test file follows standard unittest TestCase structure
- Test data sourced from tests/test_formats/ directory
- Mock log_and_print function where needed for testing

## 3. Directory Read Permission Checking

### Problem
The code checks directory existence with os.path.isdir() but does not verify read permissions, leading to confusing error messages when accessing restricted directories.

### Solution
Add read permission check after directory existence check in src/log_analyzer/__main__.py:

```python
if not os.path.isdir(directory):
    log_and_print(f"Hata: {directory} geçerli bir dizin değil")
    return

# Add read permission check
if not os.access(directory, os.R_OK):
    log_and_print(f"Hata: {directory} dizinine okuma izni yok")
    return
```

### Expected Behavior
- Clear error message when directory lacks read permissions
- Consistent exit behavior (function returns early)
- Improved user experience for permission-related issues

## 4. Log File Cleanup Mechanism

### Problem
Each run creates a new timestamped log file (analyzer_YYYYMMDD_HHMMSS.log) but old files are never deleted, potentially consuming disk space over time.

### Solution
Add a log cleanup function in src/log_analyzer/analyzer_core.py that runs before creating a new log file:

ptpython
def cleanup_old_logs(keep_count=5):
    """Cleanup old log files, keeping only the most recent ones.
    
    Args:
        keep_count: Number of recent log files to keep (default: 5)
    """
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # Find all analyzer_*.log files
        log_files = []
        for f in os.listdir(script_dir):
            if f.startswith('analyzer_') and f.endswith('.log'):
                log_files.append(f)
        
        # Sort by modification time (oldest first)
        log_files.sort(key=lambda x: os.path.getmtime(os.path.join(script_dir, x)))
        
        # Remove excess files
        if len(log_files) > keep_count:
            files_to_remove = log_files[:-keep_count]
            for f in files_to_remove:
                try:
                    os.remove(os.path.join(script_dir, f))
                except OSError:
                    # Ignore errors during cleanup
                    pass
    except Exception:
        # If cleanup fails, continue without it
        pass
```

Then call this function in main() before opening the log file:

```python
# Cleanup old log files before creating new one
cleanup_old_logs(keep_count=5)
```

### Implementation Approach
- Keep the 5 most recent log files by default
- Silent failure approach - if cleanup fails for any reason, continue normally
- Only removes files matching the analyzer_*.log pattern
- Uses modification time for sorting (most reliable)

## Files to Modify/Create

### New Files to Create:
1. docs/usage.md
2. docs/api_reference.md  
3. docs/release_notes.md
4. tests/test_csv_handler.py
5. tests/test_json_handler.py
6. tests/test_text_handler.py
7. tests/test_advanced_analyzer.py
8. tests/test_main.py
9. tests/test_formats/ (already exists with test data)

### Files to Modify:
1. src/log_analyzer/__main__.py - Add read permission check
2. src/log_analyzer/analyzer_core.py - Add cleanup_old_logs function and call it

## Testing Strategy
- Manual verification of each feature
- Unit tests for new functionality
- Integration testing to ensure existing functionality remains intact
- Permission testing by simulating restricted directory access
- Log cleanup verification by running multiple times and checking file count

## Dependencies
All enhancements use only Python standard library modules, maintaining the project's zero-dependency goal.