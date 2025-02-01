# YouTube Video Data Extraction and GitHub Automation
<p align="left">
  <img src="https://github.com/darshanabk/YouTubeFoodChannelAnalysis/blob/main/youtube.png" width="400" title="hover text">
</p>

This project is **an ongoing** initiative to develop a pipeline that retrieves the top video details based on specific keywords, sorted by the most viewed count, from YouTube using the YouTube Data API. The pipeline processes the data and uploads it to a GitHub repository, aiming to automate the fetching, analysis, and storage of data for actionable insights.

## Source - Layer -1 Raw data
- **Code Implementation** :
  - [View Script](https://github.com/darshanabk/YouTubeFoodChannelAnalysis/blob/main/sourcedaily.ipynb)
  - This script contains the logic for data extraction and processing.
- **Extracted Data**      :
  - [Raw Data Collection](https://github.com/darshanabk/YouTubeFoodChannelAnalysis/tree/main/Source/Daily)
  - This directory stores the JSON files with extracted raw data.

### 1. Features:
   - **YouTube Data Extraction**:
      - Fetch top videos based on keywords using the YouTube Data API.
      - Extract details like video title, channel name, view count, likes, comments, and tags.
   
   - **Data Storage**:
      - Save extracted data into JSON files with timestamps for record-keeping.
   
   - **GitHub Integration**:
      - Automatically push the extracted JSON files to a GitHub repository.
      - Maintain a structured directory system in the repository for organized data storage.
   
   - **Error Handling**:
      - Ensures smooth operation by handling API and GitHub errors.
   
   - **Tools and Technologies**:
      - **YouTube Data API**: Fetch video details.
      - **Python Libraries**:
        - `pandas`: For data processing.
        - `re` and `datetime`: For string and date manipulations.
        - `shutil` and `os`: For file and directory operations.
        - `git` and `Repo`: For executing Git commands.
        - `pytz` and `timedelta`: For handling time zones and time differences.
        - `IPython.display`: For displaying JSON responses in Jupyter Notebooks.
      - **Kaggle Secrets**: Manage sensitive API keys and repository credentials securely.
      - **GitHub**: Store and manage extracted data.
###  2. Additional Libraries:
   - `from googleapiclient.discovery import build`: For interacting with the YouTube API.
   - `from kaggle_secrets import UserSecretsClient`: For securely managing API keys in Kaggle.
