NC Judicial Report Parser (.TXT to .CSV)

A robust Python utility designed to parse unstructured, legacy text flat-files from North Carolina Judicial Court Reports and transform them into clean, structured, and machine-readable CSV datasets.

Government and legacy enterprise systems frequently output multi-page reports in rigid, fixed-width text formats (`.txt`) that are difficult to query or analyze. This script acts as a data pipeline parser that tracks state across file blocks, extracts complex multi-line entities (such as court headers, defendant metadata, pleas, and judgments), and maps them into a uniform tabular structure.

Features
- Stateful Line-by-Line Parsing:** Utilizes custom conditional routing and state-tracking loops to handle multi-line records where data spans across various nested sections.
- Defensive Error Handling:** Includes robust string boundary checking (`len()` guards) to prevent index-out-of-bounds exceptions when parsing malformed or truncated text lines.
- Structured Dictionary Mapping:** Leverages Python's `csv.DictWriter` to ensure keys match a strict, predefined schema, maintaining clean column alignment in the output file.
- Exception Safety:** Gracefully handles missing files and encoding edge cases with descriptive console feedback.

Project Structure
```
├── .TXT to .CSV.py    # Main script containing parsing logic and file stream handlers
└── README.md          # Project documentation
```

Requirements
- Python 3.x (No external third-party dependencies required; built entirely with standard libraries).

Usage
- Ensure your target text file is placed in the same directory as the script.

Run the script from your terminal:
-> python ".TXT to .CSV.py"
Enter the filename when prompted (without the .txt extension).

The script will process the records and generate a clean NewFile.csv in the working directory.

Output Schema
- The generated CSV maps out the following extracted fields:

Administrative: RunDate, CourtDate, CourtTime, CourtRoom, Location
Defendant Info: DockNo, FileNo, CaseClassif, OfficerName, DefendName, AlsoKnownAs, Fingerprint, Continue, Attorney
Offense & Judgement: Verdict, BondAmount, Crime, Plea, ClassOffense, Points, OffenseLevel, DomesticViolence, AssistantDirectorAttorney, Spanish
