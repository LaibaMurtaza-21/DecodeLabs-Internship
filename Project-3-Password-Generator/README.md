# Project 3: Random Password Generator

A cryptographically secure password generator built in Python, developed as part of the DecodeLabs Python Programming Industrial Training Kit. Available as both a command-line tool and a Streamlit web app.

## Overview

This tool generates strong, unpredictable passwords using Python's `secrets` module rather than the standard `random` module. The distinction matters: `random` relies on the Mersenne Twister, a deterministic pseudo-random number generator that is predictable if its seed is known. `secrets` draws from the operating system's cryptographic entropy source, making it suitable for security-sensitive use cases like password and token generation.

## Features

- Cryptographically secure randomness via `secrets.choice()`
- Configurable password length (8–64 characters)
- Optional character sets: letters, digits, and symbols
- Efficient string construction using `''.join()` instead of repeated concatenation
- Input validation to prevent invalid or unsafe lengths
- Streamlit web interface with live entropy estimation and strength feedback

## Why `secrets` Instead of `random`

| | `random` | `secrets` |
|---|---|---|
| Algorithm | Mersenne Twister (deterministic PRNG) | OS-level cryptographic entropy |
| Predictable if seed is known | Yes | No |
| Suitable for passwords/tokens | No | Yes |

## Password Strength

Password strength is measured in bits of entropy:

```
E = L × log2(R)
```

Where `L` is the password length and `R` is the size of the character pool. Following NIST SP 800-63-4 (2024) guidance, this tool prioritizes length over forced complexity — a longer password with a moderate character set is generally stronger and easier to use than a short password stuffed with mandatory symbols.

## Project Structure

```
Project-3-Password-Generator/
├── password_generator.py   # Command-line version
├── streamlit_app.py        # Web app version
└── README.md
```

## Requirements

- Python 3.6+ (for the `secrets` module)
- Streamlit (only required for the web app)

Install Streamlit:

```bash
pip install streamlit
```

## Usage

### Command-line version

```bash
python password_generator.py
```

You'll be prompted for a desired password length, and a secure password will be printed to the console.

### Web app version

```bash
streamlit run streamlit_app.py
```

This opens a browser interface where you can adjust length, toggle character sets, and view an estimated entropy score with a strength rating.

## Example

```
=== DecodeLabs Secure Password Generator ===
Enter desired password length (8-64): 16

Your secure password: bME5EI2AHtDDOC6o
```

## Key Concepts Demonstrated

- Module integration (`secrets`, `string`)
- String immutability and efficient string building
- Input validation and error handling
- Basic information theory (entropy calculation)
- Building both CLI and web-based interfaces for the same core logic

## Author

Built as part of the DecodeLabs 2026 Python Industrial Training Kit.
