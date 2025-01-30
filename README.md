# lablink

## Overview

This repository contains two Python scripts that automate the extraction, processing, and mapping of laboratory data from a web-based lab index. The extracted data is transformed into a **FHIR-R4 compliant ConceptMap (JSON format)**, linking internal lab codes to LOINC codes to improve interoperability and secondary data use.

## Workflow

1. **Extract data from the internal lab index** using `lablink.py` (Web Scraping).
2. **Process the extracted data and generate a FHIR R4 ConceptMap** using `csv_to_json.py`.
3. **Use the ConceptMap for improved querying and integration with clinical data repositories**.

## Repository Contents

### 1. `lablink.py` – Web Scraper for Lab Index Data
A web scraper built using **Selenium** and **BeautifulSoup** to extract laboratory analyte data from an internal lab index website.

#### Features:
- Automates web interactions to extract **analytes**.
- Retrieves **internal lab codes**, descriptions, and corresponding **LOINC codes**.
- Saves the extracted data in a structured **CSV format**.

#### Usage:
Run the script with:
```bash
python lablink.py
```
#### Requirements:

Selenium WebDriver (Safari WebDriver is used by default).
The Lab Index URL must be correctly set in the script.
The output file path for extracted data must be specified.

### 2. csv_to_json.py – Generate a FHIR ConceptMap from CSV
Converts the extracted lab index data from CSV into a ***FHIR R4-compliant ConceptMap*** in JSON format.

#### Features:

Reads the extracted lab data from CSV.
Retrieves the LOINC Long Common Name from a reference LOINC catalog (loinc.csv).
Generates a structured FHIR ConceptMap linking internal lab codes to LOINC codes.

#### Usage:

Run the script with:
```bash
python csv_to_json.py
```
#### Requirements:

The input CSV file path must be correctly set.
The LOINC reference file (loinc.csv) should be available in the expected directory.

#### Download LOINC Data
To use csv_to_json.py, you need to download the official LOINC dataset:

Go to LOINC.org.
Download the latest LOINC_2.78.zip (or a newer version).
Extract the ZIP file and locate Loinc.csv.
Set the path to Loinc.csv in csv_to_json.py:
```bash
loinc_file_path = '/path/to/Loinc.csv'
```
#### Installation & Dependencies

Install the required dependencies using:

```bash
pip install pandas selenium beautufilsoup4
```
Ensure that:

Safari WebDriver is enabled (safaridriver --enable).
Selenium is correctly configured for web automation.

#### Results & Impact

Efficient Data Extraction: Automated retrieval of analyte data from the lab index.
Standardization: LOINC mappings improve interoperability and secondary use.
FHIR-Compliant: ConceptMap supports structured data integration.

Contact

For questions or contributions, contact:
[Benjamin Kinast]
📧 [benjamin.kinast@uksh.de]
🏥 Universitätsklinikum Schleswig-Holstein (UKSH)
