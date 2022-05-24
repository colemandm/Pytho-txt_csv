#Final Project CIS-3680
#@Author's Dylan Coleman, Bennett Gungor, Jeffrey Cansler
 #Jeff Starts
import csv
 
END_OF_HEADER = "*" * 25
FIELDS = ["RunDate", "CourtDate", "CourtTime", "CourtRoom", "Location", "DockNo", "FileNo", 
'CaseClassif', 'OfficerName', 'DefendName', 'AlsoKnownAs', 'Verdict', 'Fingerprint', 'Continue', 
'BondAmount', 'Crime', 'Plea', 'Attorney', 'ClassOffense', 'Points', 'OffenseLevel',
 'DomesticViolence', 'AssistantDirectorAttorney', 'Spanish']
 
def is_summary_header(line):
    return line[0] == '1' and "RUN DATE:" in line
 
def is_page_header(line):
    return line[0] == '1' and "RUN DATE:" not in line
 
def is_report_header(line):
    return line[0] != '1' and "PAGE   1" in line
 
def process_page_header(infile):
    while True:
        line = infile.readline()
       
        if END_OF_HEADER in line:
            break
 
def process_report_header(infile, line):
    rec = {}
 
    rec['RunDate'] = line[12:22].strip()
 
    while True:
        line = infile.readline()
       
        if END_OF_HEADER in line:
            break
        elif "COURT DATE:" in line:
            rec["CourtDate"] = line[22:32].strip()
            rec["CourtTime"] = line[44:52].strip()
            rec["CourtRoom"] = line[78:].strip()
        elif "LOCATION:" in line:
            rec["Location"] = line[12:28].strip()
    return rec
 # Jeff End
def is_defend(line):
    try:
        int(line[0:6])
        return True
    except ValueError:
        return False
 
def process_offend1(line):
    rec1 = {}
    rec1['CaseClassif'] = line[9:10]
    rec1['Crime'] = line[11:43].strip()
    rec1['Plea'] = "N/A"
    if len(line) < 76:
        rec1['Verdict'] = "N/A"
    elif len(line) > 76:
        rec1['Verdict'] = line[70:83].strip()
    return rec1
 
def process_offend2(line):
    rec = {}
    rec['AssistantDirectorAttorney'] = line[80:].strip()
    rec['OffenseLevel'] = line[22:28].strip()
    rec['Judgement'] = line[49:75].strip()
    rec['Points'] = line[17:20].strip()
    rec['ClassOffense'] = line[12:14].strip()
    rec['Spanish'] = line[19:26].strip()
    rec['AssistantDirectorAttorney'] = line[80:].strip()

    return rec
 
def writtenRecord(writer, rpt_data, defend_data, off_data):
    rec = {}
    rec.update(rpt_data)
    rec.update(defend_data)
    rec.update(off_data)
    writer.writerow(rec)
 
def process_defend(line):
    rec = {}
    rec['DockNo'] = line[0:6].strip()
    rec['FileNo'] = line[8:19].strip()
    rec['DefendName'] = line[19:42].strip()
    rec['OfficerName'] = line[42:56].strip()
    if len(line) > 85:
        rec['Continue'] = line[84:86].strip()
        rec['Attorney'] = line[66:83].strip()
    elif len(line) > 57:
        rec['Attorney'] = line[66:83].strip()
        rec['Continue'] = line[85:87].strip()
    elif len(line) < 57:
        rec['Attorney'] = ""
        rec['Continue'] = ""
    rec['Fingerprint'] = "No"
    rec['BondAmount'] = "N/A"
    return rec
 
def main():
    filename = input("Enter the filename: ")
    sub = filename + ".txt"
    infile = open(sub, 'r')
    out_file = open ("NewFile3.csv", 'w')
    writer = csv.DictWriter(out_file, FIELDS)
    writer.writeheader()
 
    rpt_data = {}
    defend_data = {}
    off_data = {}
 
    while True:
        line = infile.readline()
        if line == "" or is_summary_header(line):
            break
        elif line == "\n":
            pass
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
            defend_data['BondAmount'] = line[25:42].strip()
        elif "PLEA:" in line:
            defend_data['CaseClassif'] = line[9:10].strip()
            defend_data['Verdict'] = line[70:83].strip()
            defend_data['Plea'] = line[49:64].strip()
            defend_data['Crime'] = line[11:43].strip()
            if len(off_data) > 0:
                writtenRecord(writer, rpt_data, defend_data, off_data)
                off_data = {}
            off_data = process_offend1(line)
        elif "PLEA:" in line:
            off_data['CaseClassif'] = line[9:10].strip()
            off_data['Verdict'] = line[70:83].strip()
            off_data['Plea'] = line[49:64].strip()
            if len(off_data) > 0:
                off_data = process_offend2(line)
        elif "JUDGMENT:" in line:
            off_data['Points'] = line[17:20].strip()
            off_data['OffenseLevel'] = line[22:28].strip()
            off_data['ClassOffense'] = line[12:14].strip()
            off_data['DomesticViolence'] = line[35:40].strip()
            off_data['AssistantDirectorAttorney'] = line[80:].strip()
        elif "SPANISH" in line:
            off_data['Spanish'] = 'Y'
        elif "AKA:" in line:
            off_data['AlsoKnownAs'] = line[18:].strip()

        else:
            print(line, end="")

    infile.close()
 
if __name__ == '__main__':
    main()