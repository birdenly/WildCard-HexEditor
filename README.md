# WildCard HexEditor

A command-line program for finding and replacing hex patterns in any file with support for wildcard matching. This doesn't make backups of the older file, this was made for Nucleus Co-op, where files are copied over to another folder to not affect the main files.

## Overview

This allows you to search for and replace specific byte sequences in any file using hexadecimal notation. The main feature is **wildcard pattern matching** using `??` to match any single byte.

### Key Features

- **Wildcard Hex Search**: Use `??` to match any byte in your search pattern
- **Flexible Replacement**: Replace patterns with specific hex values or convert numeric/string values to hex
- **Occurrence Control**: Replace all occurrences or target a specific occurrence number
- **Little-Endian Support**: Automatic conversion of integers to little-endian hexadecimal format
- **Logging**: Logs are created besides the executable.

## Installation

1. Clone or download the repository:
   ```bash
   git clone https://github.com/birdenly/WildCard-HexEditor.git
   cd WildCard-HexEditor
   ```

2. Ensure Python is installed.

OR

1. Download the executable from the release tab.

## Usage


```bash
python WildCard-HexEditor.py <file_path> <search_pattern> <replace_pattern> [occurrence]
```


```bash
WildCard-HexEditor.exe <file_path> <search_pattern> <replace_pattern> [occurrence]
```

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `file_path` | string | Path to the binary file to modify |
| `search_pattern` | string | Hexadecimal pattern to search for (space-separated bytes, use `??` for wildcards) |
| `replace_pattern` | string | Hexadecimal pattern to replace with (supports `"value"` syntax for auto-conversion) |
| `occurrence` | integer (optional) | Replace only the nth occurrence. If omitted, replaces all matches |

### Examples

#### Replace all occurrences of a specific hex pattern

```bash
python WildCard-HexEditor.py myfile.bin "FF 00 FF" "00 00 00"
```

Replaces every instance of `FF 00 FF` with `00 00 00`.

#### Use wildcards to match any byte

```bash
python WildCard-HexEditor.py myfile.bin "FF ?? FF" "00 00 00"
```

Matches any byte sequence where the first byte is `FF`, any byte follows, and the last byte is `FF`.
#### Replace only a specific occurrence

```bash
python WildCard-HexEditor.py myfile.bin "AA BB CC" "11 22 33" 2
```

Replaces only the 2nd occurrence of `AA BB CC` with `11 22 33`.

#### Auto-convert numeric values

```bash
python WildCard-HexEditor.py myfile.bin "01 ?? ?? 00 00 ?? ?? 01" "01 \"1920\" 00 00 \"1080\" 01"
```

Will edit the file to support 1920x1080 resolution.

## Output and Logging

The tool generates a log file (`HexFindReplace.log`) in the current working directory containing debug information in case of problems.