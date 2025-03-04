# YouTube Video Data Extraction and GitHub Automation | ![Open Source](https://img.shields.io/badge/Open%20Source-Yes-brightgreen)

<p align="left">
  <img src="https://github.com/darshanabk/YouTubeFoodChannelAnalysis/blob/main/youtube_icon.png" width="1000" height = "500" title="hover text">
</p>

## [Check out DevOps YouTube Trends](https://devops-youtube-trends.streamlit.app/)
## **Overview**
This project is an ongoing initiative aimed at developing an automated pipeline to extract and process video data from YouTube based on specific keywords. Leveraging the YouTube Data API, the pipeline retrieves the most-viewed videos matching the criteria and systematically stores the data in a GitHub repository. The goal is to automate data retrieval, analysis, and storage, enabling actionable insights.


## Project Scope
- **Detailed Project Scope**:
  - [View Scope](https://github.com/darshanabk/YouTubeFoodChannelAnalysis/blob/main/ProjectScope.md)
 
## **Workflow**
  - **Source**: Kaggle -> Google Cloud Console (YouTube Data API v3) -> Data Extraction -> GitHub Automation
      
  - **Data Cleaning**: Kaggle -> Fetch Source File from GitHub -> Data Cleaning -> GitHub Automation
  
  - **Requirement**: Kaggle -> Fetch ISO Code from Rest API -> Process -> GitHub Automation
  
  - **Feature Engineering**: Kaggle Fetch Data Cleaning and Requirement Files -> Process -> GitHub Automation
  
  - **Streamlit**: Streamlit Cloud -> Fetch Processed File from GitHub -> Process and Visualize on Streamlit -> Deployed App

Every process fetches the most recent file to ensure up-to-date data. The process runs daily for real-time data.

## **Source**
#### Code Implementation
- **Data Extraction Script**:
  - [View Script](https://github.com/darshanabk/YouTubeFoodChannelAnalysis/blob/main/sourcedaily.ipynb)
  - This script implements the logic for extracting and processing YouTube video data.
#### Extracted Data
- **Raw Data Repository**:
  - [View Data](https://github.com/darshanabk/YouTubeFoodChannelAnalysis/tree/main/Source/Daily)
  - This directory contains JSON files storing raw extracted data, which are updated daily.

<!-- ### 1. Features:
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
   - `from kaggle_secrets import UserSecretsClient`: For securely managing API keys in Kaggle. -->

## **Data Cleaning**
#### Code Implementation
- **Data Cleaning Script**:
  - [View Script](https://github.com/darshanabk/YouTubeFoodChannelAnalysis/blob/main/dataCleaning.ipynb)
  - This script performs data preprocessing and ensures data consistency.

#### Processed Data
- **Cleaned Data Repository**:
  - [View Data](https://github.com/darshanabk/YouTubeFoodChannelAnalysis/tree/main/DataCleaning/Daily)
  - This directory stores cleaned JSON files, updated daily.

## **Requirements**
#### Code Implementation
- **Requirement Extraction Script**:
  - [View Script](https://github.com/darshanabk/YouTubeFoodChannelAnalysis/blob/main/country-codes-iso-3166-1-alpha-2-continent-code.ipynb)
  - This script extracts and processes required metadata.

#### Extracted Data
- **Requirement Data Repository**:
  - [View Data](https://github.com/darshanabk/YouTubeFoodChannelAnalysis/tree/main/Requirement/Daily)
  - This directory stores structured requirement data in JSON format.

## **Feature Engineering**
#### Code Implementation
- **Feature Engineering Script**:
  - [View Script](https://github.com/darshanabk/YouTubeFoodChannelAnalysis/blob/main/country-codes-iso-3166-1-alpha-2-continent-code.ipynb)
  - This script processes cleaned data for feature extraction.

#### Engineered Data
- **Processed Feature Repository**:
  - [View Data](https://github.com/darshanabk/YouTubeFoodChannelAnalysis/tree/main/Requirement/Daily)
  - This directory contains feature-engineered data stored in JSON format.
 
## **Streamlit**
#### Code Implementation
- **Streamlit App Script**:
  - [View Script](https://github.com/darshanabk/DevOps-YouTube-Trends/blob/main/Streamlit/Streamlit.py)
  - This script visualizes processed data using interactive charts and dashboards.

#### Deployment
- **Live App**:
  - [View App](https://devops-youtube-trends.streamlit.app/)
  - The app fetches the latest processed data from GitHub and presents dynamic visualizations.

This project ensures efficient and automated extraction, processing, and storage of YouTube video data, making it a valuable resource for content trend analysis.

## License

 This project uses a dual-license approach:  

**1. Non-Code Content License**

This project’s documentation, descriptions, and visualizations are licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License (CC BY-NC-ND 4.0).  
  - You must provide appropriate credit.  
  - The content may not be used for commercial purposes.  
  - Redistribution is allowed only in its original form without modifications.  

For more details, visit: [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/) 

**2. Source Code License**

The source code of this project is licensed under the Mozilla Public License 2.0 (MPL-2.0).  
  - You may modify and distribute the code, but any modified files must also be licensed under MPL-2.0.  
  - Only MPL-licensed files must remain open-source if used with proprietary software.  
  - The code is provided as-is, without any guarantees or warranty.  

For more details, visit: [MPL-2.0](https://www.mozilla.org/en-US/MPL/2.0/)



  

### 🤝 How to Support  
If you'd like to show your support, you can:  
- ⭐ Star this repository  
- 💪 Sponsor via GitHub  
- 🔗 Share this project with others  

Your encouragement will inspire me to continue building and enhancing this project!  
