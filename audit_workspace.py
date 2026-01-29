import os
import re

# Configurations
TARGET_EXTENSIONS = {'.py', '.jl'}
INDENT_SIZE = 4

def audit_file(filepath):
    issues = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f, 1):
            # 1. Check for Tabs
            if '\t' in line:
                issues.append(f"Line {i}: Contains TAB character (Use 4 spaces instead).")

            # 2. Check 4-Space Indentation
            stripped = line.lstrip(' ')
            indent_count = len(line) - len(stripped)
            if indent_count % INDENT_SIZE != 0:
                issues.append(f"Line {i}: Indentation of {indent_count} is not a multiple of {INDENT_SIZE}.")

            # 3. Naming Convention Audit (Regex for Snake Case & your GIS prefixes)
            # Detects variable assignments: name = value
            assignment = re.match(r'^\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*=', line)
            if assignment:
                var_name = assignment.group(1)
                
                # Check for CamelCase in variables (should be snake_case)
                if any(c.isupper() for c in var_name) and '_' not in var_name:
                    # Exception: Python/Julia Classes/Types usually use PascalCase
                    if not line.strip().startswith(('class ', 'struct ')):
                        issues.append(f"Line {i}: Variable '{var_name}' should use snake_case.")

    return issues

def run_audit(directory):
    print(f"--- Auditing Workspace: {directory} ---")
    for root, _, files in os.walk(directory):
        for file in files:
            ext = os.path.splitext(file)[1]
            if ext in TARGET_EXTENSIONS:
                print(f"\nAuditing file: {file}")
                path = os.path.join(root, file)
                file_issues = audit_file(path)
                if file_issues:
                    print(f"\n[!] {file} ({ext})")
                    for issue in file_issues:
                        print(f"    - {issue}")

if __name__ == "__main__":
    # Runs in the current directory
    run_audit('.')