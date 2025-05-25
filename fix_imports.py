#!/usr/bin/env python3
"""Fix imports in copied SystemAIR API files."""

import os
import re


def fix_imports(directory):
    """Fix imports in all Python files in the directory."""
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Replace imports
                new_content = re.sub(
                    r'from systemair_api\.', 
                    r'from ....api.', 
                    content
                )
                
                # Prevent over-dotting in __init__.py files
                new_content = re.sub(
                    r'from ....api\.api\.', 
                    r'from ...api.', 
                    new_content
                )
                new_content = re.sub(
                    r'from ....api\.auth\.', 
                    r'from ...auth.', 
                    new_content
                )
                new_content = re.sub(
                    r'from ....api\.models\.', 
                    r'from ...models.', 
                    new_content
                )
                new_content = re.sub(
                    r'from ....api\.utils\.', 
                    r'from ...utils.', 
                    new_content
                )
                
                # Special case for __init__.py files
                if file == '__init__.py':
                    new_content = re.sub(
                        r'from ....api\.', 
                        r'from ..', 
                        new_content
                    )
                
                # Special case for main files
                if root.endswith('api'):
                    new_content = re.sub(
                        r'from ....api\.', 
                        r'from .', 
                        new_content
                    )
                
                # Write changes
                if new_content != content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Fixed imports in {file_path}")


if __name__ == "__main__":
    fix_imports('/Users/henningberge/PycharmProjects/SystemAIR-API/custom_components/systemair/api')