# ETL Pipeline Project

This project demonstrates a simple and practical Extract, Transform, and Load (ETL) pipeline built using Python. The pipeline connects to a public REST API, extracts user data, cleans and standardizes the records, and saves the results into structured output files.

## Project Overview

An ETL pipeline is used to move data from one source to another while preparing it for analysis or storage. In this project, the workflow is:

1. Extract: Fetch data from a remote API.
2. Transform: Clean and normalize the data into a consistent format.
3. Load: Save the cleaned data into CSV and JSON files.

This project is a beginner-friendly example of how ETL processes are designed and implemented in real-world data engineering tasks.

## What the Pipeline Does

The script in ETL.py performs the following tasks:

- Connects to the JSONPlaceholder API at https://jsonplaceholder.typicode.com/users
- Sends a request with a browser-like user-agent header
- Reads the JSON response
- Validates that the response is a list of records
- Cleans each record by:
  - converting values to the right types
  - trimming empty spaces
  - standardizing text to lowercase where needed
  - replacing missing values with placeholders like N/A
- Writes the cleaned data to:
  - cleaned_users.csv
  - cleaned_users.json

## Features

- Simple Python-based ETL workflow
- Easy-to-read and maintainable code structure
- Handles missing or inconsistent values
- Produces both CSV and JSON outputs
- Includes SSL-safe request handling for certificate-related issues

## Files in the Project

- ETL.py: Main Python script that runs the ETL pipeline
- README.md: Project documentation
- cleaned_users.csv: Output file generated in CSV format
- cleaned_users.json: Output file generated in JSON format

## How It Works

### 1. Extraction
The script uses Python’s urllib library to request data from the API. It builds a request and reads the JSON response into memory.

### 2. Transformation
Each record is cleaned and transformed into a standardized dictionary containing fields such as:

- id
- name
- username
- email
- phone
- website
- street
- city
- zipcode
- company_name
- catch_phrase

### 3. Loading
The cleaned data is saved into two output formats:

- CSV for tabular use and spreadsheets
- JSON for structured data exchange and APIs

## Requirements

To run this project, you need:

- Python 3.x
- Standard Python libraries only (csv, json, ssl, pathlib, urllib)

## How to Run

Open the project folder in your terminal and run:

```bash
python ETL.py
```

If you are using a different Python executable, you can run:

```bash
python3 ETL.py
```

## Output

After the script runs successfully, it will generate:

- cleaned_users.csv
- cleaned_users.json

These files contain the cleaned and structured version of the API data.

## Notes

The script includes basic SSL handling so it can still fetch the data in environments where certificate verification may cause issues. This makes the ETL pipeline more robust when running on different systems.

## Learning Purpose

This project is to understand:

- how ETL pipelines are built
- how Python can interact with APIs
- how data cleaning works in practice
- how to store processed data in common file formats

