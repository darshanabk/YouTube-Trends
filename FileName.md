# Source File Format

## File Format:
The raw data files in the repository follow a specific format to maintain consistency and organization for easy identification and future use.

### Structure:
S_YYYY-MM-DD_HH:MM:SS_<record_count>_records.json

### Components:
1. **S** - Represents the source of the data (i.e., YouTube API data).
2. **YYYY-MM-DD_HH:MM:SS** - The timestamp when the data was extracted and saved:
   - **YYYY**: Four-digit year
   - **MM**: Two-digit month
   - **DD**: Two-digit day
   - **HH**: Two-digit hour (24-hour format)
   - **MM**: Two-digit minute
   - **SS**: Two-digit second
3. **<record_count>** - The total count of video records retrieved during that data extraction.
4. **_records.json** - Indicates that the file contains video records in JSON format.

### Example:
S_2025-01-28_17:56:35_504_records.json

- **S**: Denotes that the file is from the YouTube data source.
- **2025-01-28_17:56:35**: Timestamp of data extraction (28th January 2025, 17:56:35).
- **504**: Number of video records in this extraction.
- **_records.json**: File format for raw video records.

### Purpose:
This naming convention helps in identifying the source, timestamp, and the number of records in each file. It aids in organizing and accessing raw data for future processing and analysis.

---
# DataCleaning File Format

### File Format:

**Structure:**  
`DC_YYYY-MM-DD_HH:MM:SS_<record_count>_records.json`

### Components:

- **DC**: Represents that this file is from the **Data Cleaning** process.  
- **YYYY-MM-DD_HH:MM:SS**: The timestamp when the data cleaning was performed:  
  - **YYYY**: Four-digit year.  
  - **MM**: Two-digit month.  
  - **DD**: Two-digit day.  
  - **HH**: Two-digit hour (24-hour format).  
  - **MM**: Two-digit minute.  
  - **SS**: Two-digit second.  
- **<record_count>**: The total count of video records after the cleaning process.  
- **_records.json**: Indicates the file format containing the cleaned video records in JSON format.  


### Example:

**File Name:**  
`DC_2025-01-28_19:55:17_402_records.json`  

**Explanation:**  
- **DC**: Denotes the file is from the Data Cleaning stage.  
- **2025-01-28_19:55:17**: Indicates the timestamp of data cleaning (28th January 2025, 19:55:17).  
- **402**: The number of records remaining after the cleaning process.  
- **_records.json**: File format for cleaned video records in JSON format.  

### Purpose:

This naming convention ensures consistency and clarity, making it easier to distinguish between raw and cleaned data files, track the time of cleaning, and identify the count of processed records.

---
# Requirement File Format

## File Format:
The raw data files follow a structured format to maintain consistency and organization, ensuring easy identification and future use.

### Structure:
RE_YYYY-MM-DD_HH:MM:SS_<data_description>.json

### Components:
1. **RE** - Represents an external requirement source for the project.
2. **YYYY-MM-DD_HH:MM:SS** - The timestamp when the data was extracted and saved:
   - **YYYY**: Four-digit year
   - **MM**: Two-digit month
   - **DD**: Two-digit day
   - **HH**: Two-digit hour (24-hour format)
   - **MM**: Two-digit minute
   - **SS**: Two-digit second
3. **<data_description>** - A short description of the data contained in the file (e.g., `country_details` for country information).
4. **.json** - Denotes that the file contains data in JSON format.

### Example:
RE_2025-02-03_21:26:51_country_details.json

- **RE**: Indicates that the file pertains to an external requirement source for the project.
- **2025-02-03_21:26:51**: Timestamp of data extraction (3rd February 2025, 21:26:51).
- **country_details**: Describes that the file contains country information.
- **.json**: File format for the data in JSON.

### Purpose:
This naming convention helps identify the external requirement source, timestamp, and content of each file. It provides clarity in organizing and accessing the data for future analysis or processing.


