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
