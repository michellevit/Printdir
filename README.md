# Printdir

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python)
![Windows](https://img.shields.io/badge/Windows-Supported-0078D6?style=flat-square&logo=windows)
![Clipboard](https://img.shields.io/badge/Clipboard-Copy--Ready-4caf50?style=flat-square)

A tiny tool that prints a clean, shareable folder tree for your projects.

- Type a **full/relative path**, or just a **project name** (it searches your `Coding_Projects` folder).
- Skips heavy/noisy stuff like `node_modules`, `.next`, `dist`, etc.
- Outputs to the console **and** copies to your clipboard (Unicode-safe).

## Table of Contents

- [Getting Started](#getting-started)
- [Usag](#usage)
- [Example Output](#example-output)
- [Notes](#notes)
- [Credits](#credits)

## Getting Started

Clone/download the repo and run on Windows

```powershell
# Double-click:
print_dir.bat

# Or from a terminal in the repo folder:
python print_dir.py
```

_Requires Python (3.10+). If you don’t have it: https://www.python.org/downloads/_

## Usage

- When prompted, enter either:

  - A full path
    - Example: `C:\Users\Michelle\Documents\Coding_Projects\fennec-animation`
  - A project name
    - Example:
      `fennec-animation`
    - \_**Note**: this will search inside C:\Users\Michelle\Documents\Coding_Projects

- The output is:
  - Printed in the CMD window
  - Copied to your clipboard automatically.

## Example Output

```cmd
|-- my-project
  └── .gitignore
  └── README.md
  |-- app
    └── page.tsx
  |-- components
    |-- Button
      └── Button.tsx
    └── Header.tsx
  |-- public
    └── favicon.ico
  └── package.json
(Copied to clipboard)

Done. Press any key to close.

```

## Notes

This tool is currently **tailored to my local development setup**:

- By default, when you enter only a **project name** (instead of a full path), Printdir searches in: `C\Users\Michelle\Documents\Coding_Projects`

- This matches my own folder structure for storing projects.

- The search is **case-insensitive** and also ignores differences in spaces, underscores, and dashes.
- For example:  
  `My-Project`, `my_project`, and `my project` will all match the same folder.

**If you want to use Printdir on another system**, edit the `DEFAULT_BASE_DIR` in `print_dir.py` t

## Credits

Michelle Flandin  
ChatGPT
