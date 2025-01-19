# YouTube Video Data Extraction and GitHub Automation

This project is an **ongoing effort** to build a pipeline that extracts top video details from YouTube using the YouTube Data API, processes the data, and pushes it to a GitHub repository. The goal is to automate the process of fetching, analyzing, and storing data for insights into video trends over different time periods.

## Features

1. **YouTube Data Extraction**:
   - Fetch top videos based on keywords using the YouTube Data API.
   - Extract details like video title, channel name, view count, likes, comments, and tags.

2. **Data Storage**:
   - Save extracted data into JSON files with timestamps for record-keeping.

3. **GitHub Integration**:
   - Automatically push the extracted JSON files to a GitHub repository.
   - Maintain a structured directory system in the repository for organized data storage.

4. **Error Handling**:
   - Ensures smooth operation by handling API and GitHub errors.

## Tools and Technologies

- **YouTube Data API**: Fetch video details.
- **Python Libraries**:
  - `pandas`: For data processing.
  - `re` and `datetime`: For string and date manipulations.
  - `shutil` and `os`: For file and directory operations.
  - `git` and `Repo`: For executing Git commands.
- **Kaggle Secrets**: Manage sensitive API keys and repository credentials securely.
- **GitHub**: Store and manage extracted data.
