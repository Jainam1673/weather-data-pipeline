#!/usr/bin/env python3
"""
Basic syntax validation for Mojo files
This script checks basic Mojo syntax without requiring the Mojo compiler
"""

import re
import sys

def validate_mojo_file(filepath):
    """Basic validation of Mojo file syntax"""
    try:
        with open(filepath, 'r') as f:
            content = f.read()
        
        # Basic checks
        checks = [
            (r'struct\s+\w+.*:', "Struct definitions"),
            (r'fn\s+\w+.*:', "Function definitions"),
            (r'var\s+\w+\s*:', "Variable declarations"),
        ]
        
        issues = []
        for pattern, description in checks:
            if re.search(pattern, content):
                print(f"✅ {description} found")
            else:
                print(f"ℹ️  {description} not found (may be optional)")
        
        # Check for obvious syntax errors
        if content.count('(') != content.count(')'):
            issues.append("Mismatched parentheses")
        
        if content.count('[') != content.count(']'):
            issues.append("Mismatched brackets")
            
        if content.count('{') != content.count('}'):
            issues.append("Mismatched braces")
        
        if issues:
            print(f"❌ Syntax issues found: {issues}")
            return False
        else:
            print("✅ Basic syntax validation passed")
            return True
            
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python test_mojo_syntax.py <mojo_file>")
        sys.exit(1)
    
    filepath = sys.argv[1]
    if validate_mojo_file(filepath):
        print(f"✅ {filepath} passed basic validation")
        sys.exit(0)
    else:
        print(f"❌ {filepath} failed validation")
        sys.exit(1)
