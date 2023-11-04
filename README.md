This project is a Python script that converts a .txt file from the NC Judicial Court Reports into a CSV file where the data is easily read and understood. The script takes in a .txt file as input and generates a new CSV file.

To use this script, follow these steps:

    Make sure you have Python installed on your computer.
    Place the .txt file from the NC Judicial Court Reports in the same directory as the script.
    Run the script and enter the filename when prompted.
    The script will process the .txt file and generate a new CSV file named "NewFile3.csv" in the same directory.

The generated CSV file will have the following fields:

    RunDate
    CourtDate
    CourtTime
    CourtRoom
    Location
    DockNo
    FileNo
    CaseClassif
    OfficerName
    DefendName
    AlsoKnownAs
    Verdict
    Fingerprint
    Continue
    BondAmount
    Crime
    Plea
    Attorney
    ClassOffense
    Points
    OffenseLevel
    DomesticViolence
    AssistantDirectorAttorney
    Spanish

Each row in the CSV file represents a record from the NC Judicial Court Reports, with information about the run date, court date, court time, court room, location, defendant details, offense details, and other relevant information.

The script uses various functions to process different sections of the .txt file and extract the required information. It handles different types of headers, defendant information, offense information, and other relevant data.

Please note that this script is specifically designed for the NC Judicial Court Reports in a specific format. If you want to use it for other purposes or with different file formats, you may need to make modifications accordingly.
