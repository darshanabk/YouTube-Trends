

def FetchLatestFile():
    # Load environment variables from .env file
    load_dotenv()

    # Access sensitive data from environment variables
    owner = os.getenv('REPO_OWNER')
    repo = os.getenv('REPO_NAME')
    directory = os.getenv('DIRECTORY_RELATIVE_PATH_FEATURE')
    token = os.getenv('TOKEN')
    files, latest_file = "", ""

    # GitHub API URL to list files in the directory
    url = f'https://api.github.com/repos/{owner}/{repo}/contents/{directory}'

    # Headers for authentication
    headers = {
        'Authorization': f'token {token}'
    }

    # Fetch the directory contents
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        files = response.json()
        # print(files)
        # Filter the list to only include files (not subdirectories)
        files = [file for file in files if file['type'] == 'file']
        # print(files)
        if files:
            # Sort files by updated_at timestamp in descending order to get the latest file
            latest_file = sorted(files, key=lambda x: x['name'], reverse=True)[0]

            print(f"Latest file: {latest_file['name']}")
            # print(f"URL: {latest_file['html_url']}")
            # print(f'Download URL: {latest_file['download_url']}')
        else:
            print("No files found in the directory.")
    else:
        print(f"Failed to fetch directory contents. Status code: {response.status_code}")
    latest_file = pd.read_json(latest_file['download_url'])
    return latest_file

def ContinentCountryMapping(file):
    continentCountryMapping = {}
    for index, row in file.iterrows():
        continent = row['continent']
        country_name = row['country_name']

        # Check if continent is not in the dictionary
        if continent not in continentCountryMapping:
            continentCountryMapping[continent] = [country_name]
        # If the continent exists but country is not already in the list for that continent
        elif country_name not in continentCountryMapping[continent]:
            continentCountryMapping[continent].append(country_name)
        else:
            continue   
    return continentCountryMapping


def main():
    # st.sidebar.image(".\Streamlit\DevOps.png")
    st.title("DevOps YouTube Trends")
    st.header("Channel Insights")
    st.subheader("Top 10 channels")
    file = FetchLatestFile()
    # Unique return nd.array array has not remove like list it has delete or boolean indexing we have used boolean indexing
    file = file.sort_values(by = 'continent', ascending = True)
    continents = file['continent'].unique()
    # continents = continents[continents != 'Unknown']
    file = file.sort_values(by = 'country_name', ascending = True)
    countries = file['country_name'].unique()
    # countries = countries[countries != 'Unknown']
    # contentType = file['videoContentType'].unique()
    continents = st.sidebar.multiselect("Continent",continents)
    Countries = st.sidebar.multiselect("Countries",countries)
    continentCountryMapping = ContinentCountryMapping(file)

    # visualByFilter = {}
    # for i in countries:
    #     visualByFilter[i] = {   
    #                             'top10channels': {}, 'top10videos': {},
    #                             'VideoPublishedYearLast10Years': {}, 'VideoDurationClassification': {},
    #                             'videoContentTypePie' : {}, 'channelCountryBarGraph': {},
    #                             'channelContinentPie':{}, 'ITHubPie': {}
    #                         }

    # print(visualByFilter)
    top10videos = file[['channelName','videoId','videoEngagementScoreRank']].head(10)
    file = file.drop_duplicates(subset='channelName')
    file  = file.sort_values(by = ['channelViewCount', 'channelSubscriberCount','channelGrowthScoreRank'],ascending = [False,False,True])
    top10channels = file[['channelName','channelGrowthScoreRank','videoTitle']].head(10)
    # https://www.youtube.com/watch?v=<video_id>
    # https://www.youtube.com/watch?v=3c-iBn73dDE
    return True

if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    import requests
    import pandas as pd
    import json
    import streamlit as st
    import pandas as pd
    main()
