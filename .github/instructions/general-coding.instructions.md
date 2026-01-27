---
applyTo: "**"
---
# General Coding Standards

## Code indentation

- Always use 4 spaces for indentation
- Avoid using tabs for indentation
- Ensure consistent indentation across all files
- Use a linter to enforce indentation rules

## Code formatting

- Use a linter to enforce code formatting rules
- Always add spaces around operators, including `=`, `+`, `-`, `*`, `/`, and `%`. Apply this rule on everything, including pasting code snippets, even if the original code does not have spaces around operators.
- Always add spaces after commas in lists, dictionaries, and function arguments
- Always use docstrings for all private and public functions and classes and follow the google-style docstring format as described below in the docstrings section.
- In Python, use `is` for comparison to `None` (e.g., `if variable is None:`)
- In Python, use `==` for comparison to other values (e.g., `if variable == value:`)
- In Python, use `with` statements for file handling to ensure proper resource management
- In Python, use `enumerate()` for iterating over lists with index
- In Python, use `zip()` for iterating over multiple lists in parallel
- In Python, use list comprehensions for creating lists from existing lists
- In Python, use `set()` for creating sets from existing lists
- In Python, use `dict()` for creating dictionaries from existing lists.
- Always wrap lines in code.
- Do not break lines longer than 79 characters.
- Do not break long strings into multiple lines.
- Do not break long comma separated lists into multiple lines.
- Do not break long comma separated dictionary lists into multiple lines.
- Always add spaces after commas in lists, dictionaries, and function arguments.

## Naming conventions

- Use snake_case for Python variables, functions, modules, dictionaries, pandas data frames, numpy, arrays, and methods
- Use PascalCase for Python classes or class names, components, interfaces, type aliases, and exceptions
- Use ALL_CAPS for constants and globals (e.g., `MAX_LENGTH`)
- Prefix private class members with an underscore (e.g., `_privateMember`)

## Error handling

- Use `try-catch` blocks for async operations and handle errors gracefully
- Implement proper error boundaries in React components to catch rendering errors
- Always log errors with contextual information.

## Docstrings

- Use google-style docstrings for all private and public functions and classes
- Include a brief summary of the function or class at the beginning of the docstring, followed by more detailed information if necessary
- Add sections for Args, Returns, Raises, Examples, and Note as needed.
- Include parameter types, return types, and a description of the function's purpose.
- Try to keep docstrings concise and informative

