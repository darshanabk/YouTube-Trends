# **File Naming Convention**  

This document outlines the standardized file naming convention used in the repository to maintain consistency, improve file organization, and ensure seamless cross-platform compatibility.  

## **1. Source File Format**  

### **File Naming Structure:**  
`S_YYYY-MM-DD_HH_MM_SS_<record_count>_records.json`  

### **Components:**  
- **S**: Denotes the source data extracted from the YouTube API.  
- **YYYY-MM-DD_HH_MM_SS**: Timestamp of data extraction:  
  - **YYYY**: Year (four digits).  
  - **MM**: Month (two digits).  
  - **DD**: Day (two digits).  
  - **HH**: Hour (24-hour format).  
  - **MM**: Minute (two digits).  
  - **SS**: Second (two digits).  
- **<record_count>**: Number of video records retrieved during extraction.  
- **_records.json**: Specifies the file format as JSON.  

### **Example:**  
`S_2025-01-28_17_56_35_504_records.json`  

### **Purpose:**  
This convention enables efficient identification of the data source, extraction timestamp, and record count, facilitating streamlined data organization and retrieval.  

---

## **2. Data Cleaning File Format**  

### **File Naming Structure:**  
`DC_YYYY-MM-DD_HH_MM_SS_<record_count>_records.json`  

### **Components:**  
- **DC**: Denotes that the file contains cleaned data.  
- **YYYY-MM-DD_HH_MM_SS**: Timestamp indicating when the data cleaning process was performed.  
- **<record_count>**: Number of records after the cleaning process.  
- **_records.json**: Specifies that the file is in JSON format.  

### **Example:**  
`DC_2025-01-28_19_55_17_402_records.json`  

### **Purpose:**  
This standardized format ensures clarity in tracking cleaned data files, distinguishing them from raw data files while maintaining a timestamped record of processing.  

---

## **3. Feature Engineering File Format**  

### **File Naming Structure:**  
`FE_YYYY-MM-DD_HH_MM_SS_<record_count>_records.json`  

### **Components:**  
- **FE**: Represents data that has undergone the feature engineering process.  
- **YYYY-MM-DD_HH_MM_SS**: Timestamp indicating when the feature engineering process was applied.  
- **<record_count>**: Number of records after feature engineering.  
- **_records.json**: Specifies the JSON file format.  

### **Example:**  
`FE_2025-02-06_01_05_31_423_records.json`  

### **Purpose:**  
This naming convention provides clear identification of feature-engineered datasets, ensuring efficient tracking of processed files.  

---

## **4. Requirement File Format**  

### **File Naming Structure:**  
`RE_YYYY-MM-DD_HH_MM_SS_<data_description>.json`  

### **Components:**  
- **RE**: Denotes an external requirement-related data file.  
- **YYYY-MM-DD_HH_MM_SS**: Timestamp indicating when the data was extracted or generated.  
- **<data_description>**: Brief descriptor of the file content (e.g., `country_details`).  
- **.json**: Specifies that the file is in JSON format.  

### **Example:**  
`RE_2025-02-03_21_26_51_country_details.json`  

### **Purpose:**  
This format ensures systematic organization of external requirement-related files, improving accessibility and clarity in identifying dataset contents.  

---

## **Conclusion**  
Adhering to this file naming convention ensures:  
   - **Consistent** file structure across all datasets.  
   - **Improved cross-platform compatibility**, especially on Windows (avoiding unsupported characters).  
   - **Efficient identification** of data processing stages and timestamps.  
   - **Seamless tracking** of data lineage throughout extraction, cleaning, and transformation processes.
