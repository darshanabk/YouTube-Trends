def FetchLatestFile():
    # Load environment variables from .env file
    load_dotenv()

    # Access sensitive data from environment variables
    owner = os.getenv('GITHUB_OWNER')
    repo = os.getenv('GITHUB_REPO')
    directory = os.getenv('GITHUB_DIRECTORY_FEATURE')
    token = os.getenv('GITHUB_TOKEN')
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
    file = FetchLatestFile()
    # Unique return nd.array array has not remove like list it has delete or boolean indexing we have used boolean indexing
    continents = file['continent'].unique()
    # continents = continents[continents != 'Unknown']
    countries = file['country_name'].unique()
    # countries = countries[countries != 'Unknown']
    contentType = file['videoContentType'].unique()

    continentCountryMapping = ContinentCountryMapping(file)

    visualByFilter = {}
    for i in countries:
        print(i)
        visualByFilter[i] = {   
                                'top10channels': {}, 'top10videos': {},
                                'VideoPublishedYearLast10Years': {}, 'VideoDurationClassification': {},
                                'videoContentType' : {}, 'channelCountryBarGraph': {},
                                'channelContinentPie':{}, 'ITHubPie': {}
                            }

    print(visualByFilter)
    return True

if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    import requests
    import pandas as pd
    import json
    main()
