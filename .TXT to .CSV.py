import csv
from typing import Dict, TextIO

END_OF_HEADER = "*" * 25
FIELDS = [
    "RunDate", "CourtDate", "CourtTime", "CourtRoom", "Location", "DockNo", 
    "FileNo", 'CaseClassif', 'OfficerName', 'DefendName', 'AlsoKnownAs', 
    'Verdict', 'Fingerprint', 'Continue', 'BondAmount', 'Crime', 'Plea', 
    'Attorney', 'ClassOffense', 'Points', 'OffenseLevel', 'DomesticViolence', 
    'AssistantDirectorAttorney', 'Spanish'
]

def is_summary_header(line: str) -> bool:
    return len(line) > 0 and line[0] == '1' and "RUN DATE:" in line

def is_page_header(line: str) -> bool:
    return len(line) > 0 and line[0] == '1' and "RUN DATE:" not in line

def is_report_header(line: str) -> bool:
    return len(line) > 0 and line[0] != '1' and "PAGE" in line

def process_page_header(infile: TextIO) -> None:
    while True:
        line = infile.readline()
        if not line or END_OF_HEADER in line:
            break

def process_report_header(infile: TextIO, line: str) -> Dict[str, str]:
    rec = {}
    if len(line) >= 22:
        rec['RunDate'] = line[12:22].strip()

    while True:
        line = infile.readline()
        if not line:
            break
        if END_OF_HEADER in line:
            break
        elif "COURT DATE:" in line:
            rec["CourtDate"] = line[22:32].strip() if len(line) >= 32 else ""
            rec["CourtTime"] = line[44:52].strip() if len(line) >= 52 else ""
            rec["CourtRoom"] = line[78:].strip() if len(line) >= 78 else ""
        elif "LOCATION:" in line:
            rec["Location"] = line[12:28].strip() if len(line) >= 28 else ""
    return rec

def is_defend(line: str) -> bool:
    if len(line) < 6:
        return false
    try:
        int(line[0:6])
        return True
    except ValueError:
        return False

def process_offend1(line: str) -> Dict[str, str]:
    rec1 = {}
    rec1['CaseClassif'] = line[9:10] if len(line) >= 10 else ""
    rec1['Crime'] = line[11:43].strip() if len(line) >= 43 else ""
    rec1['Plea'] = "N/A"
    
    if len(line) <= 76:
        rec1['Verdict'] = "N/A"
    else:
        rec1['Verdict'] = line[70:83].strip() if len(line) >= 83 else ""
    return rec1

def process_offend2(line: str) -> Dict[str, str]:
    rec = {}
    rec['Points'] = line[17:20].strip() if len(line) >= 20 else ""
    rec['OffenseLevel'] = line[22:28].strip() if len(line) >= 28 else ""
    rec['ClassOffense'] = line[12:14].strip() if len(line) >= 14 else ""
    rec['Spanish'] = line[19:26].strip() if len(line) >= 26 else ""
    rec['AssistantDirectorAttorney'] = line[80:].strip() if len(line) >= 80 else ""
    return rec

def writtenRecord(writer: csv.DictWriter, rpt_data: dict, defend_data: dict, off_data: dict) -> None:
    rec = {}
    rec.update(rpt_data)
    rec.update(defend_data)
    rec.update(off_data)
    writer.writerow(rec)

def process_defend(line: str) -> Dict[str, str]:
    rec = {}
    rec['DockNo'] = line[0:6].strip() if len(line) >= 6 else ""
    rec['FileNo'] = line[8:19].strip() if len(line) >= 19 else ""
    rec['DefendName'] = line[19:42].strip() if len(line) >= 42 else ""
    rec['OfficerName'] = line[42:56].strip() if len(line) >= 56 else ""
    
    if len(line) > 85:
        rec['Continue'] = line[84:86].strip() if len(line) >= 86 else ""
        rec['Attorney'] = line[66:83].strip() if len(line) >= 83 else ""
    elif len(line) > 57:
        rec['Attorney'] = line[66:83].strip() if len(line) >= 83 else ""
        rec['Continue'] = line[85:87].strip() if len(line) >= 87 else ""
    else:
        rec['Attorney'] = ""
        rec['Continue'] = ""
        
    rec['Fingerprint'] = "No"
    rec['BondAmount'] = "N/A"
    return rec

def main() -> None:
    filename = input("Enter the filename (without extension): ").strip()
    file_path = filename + ".txt"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as infile, open("NewFile.csv", 'w', newline='', encoding='utf-8') as out_file:
            writer = csv.DictWriter(out_file, fieldnames=FIELDS)
            writer.writeheader()

            rpt_data = {}
            defend_data = {}
            off_data = {}

            while True:
                line = infile.readline()
                if not line or is_summary_header(line):
                    break
                elif line == "\n":
                    continue
                elif is_page_header(line):
                    process_page_header(infile)
                elif is_report_header(line):
                    rpt_data = process_report_header(infile, line)
                elif is_defend(line):
                    if len(defend_data) > 0:
                        writtenRecord(writer, rpt_data, defend_data, off_data)
                        defend_data = {}
                        off_data = {}
                    defend_data = process_defend(line)
                elif "FINGERPRINTED" in line:
                    defend_data['Fingerprint'] = 'Yes'
                elif "BOND:" in line:
                    defend_data['BondAmount'] = line[25:42].strip() if len(line) >= 42 else ""
                elif "PLEA:" in line:
                    defend_data['CaseClassif'] = line[9:10].strip() if len(line) >= 10 else ""
                    defend_data['Verdict'] = line[70:83].strip() if len(line) >= 83 else ""
                    defend_data['Plea'] = line[49:64].strip() if len(line) >= 64 else ""
                    defend_data['Crime'] = line[11:43].strip() if len(line) >= 43 else ""
                    if len(off_data) > 0:
                        writtenRecord(writer, rpt_data, defend_data, off_data)
                        off_data = {}
                    off_data = process_offend1(line)
                elif "JUDGMENT:" in line:
                    off_data['Points'] = line[17:20].strip() if len(line) >= 20 else ""
                    off_data['OffenseLevel'] = line[22:28].strip() if len(line) >= 28 else ""
                    off_data['ClassOffense'] = line[12:14].strip() if len(line) >= 14 else ""
                    off_data['DomesticViolence'] = line[35:40].strip() if len(line) >= 40 else ""
                    off_data['AssistantDirectorAttorney'] = line[80:].strip() if len(line) >= 80 else ""
                elif "SPANISH" in line:
                    off_data['Spanish'] = 'Y'
                elif "AKA:" in line:
                    off_data['AlsoKnownAs'] = line[18:].strip() if len(line) >= 18 else ""

            # Write any trailing record left over
            if len(defend_data) > 0:
                writtenRecord(writer, rpt_data, defend_data, off_data)

        print("Successfully converted file to NewFile.csv")

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' could not be found. Please check the path and try again.")

if __name__ == '__main__':
    main()
