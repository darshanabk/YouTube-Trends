
import os
from dotenv import load_dotenv
import requests
import pandas as pd
import numpy as np
import json
import streamlit as st
import altair as alt
import plotly.express as px
import base64

@st.cache_data
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

            # print(f"Latest file: {latest_file['name']}")
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

def get_base64_image(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
        

def textMetricsMain(file, Filter_DataFrame):
    averageVideoLikeFliteredData = Filter_DataFrame['videoLikeCount'].mean()
    averageVideoLikeTotalData = file['videoLikeCount'].mean()# 100%
    percentageVideoLike = ((averageVideoLikeFliteredData/averageVideoLikeTotalData)-1) * 100 if averageVideoLikeTotalData else 0
    percentageVideoLike = round(percentageVideoLike, 0)

    file = file.drop_duplicates(subset='channelId')
    Filter_DataFrame = Filter_DataFrame.drop_duplicates(subset='channelId')

    averageChannelViewliteredData = Filter_DataFrame['channelViewCount'].mean()
    averageChannelViewTotalData = file['channelViewCount'].mean() # 100%
    percentageChannelView = ((averageChannelViewliteredData/averageChannelViewTotalData)-1) * 100 if averageChannelViewTotalData else 0
    percentageChannelView =  round(percentageChannelView, 0)

    averageChannelSubscriberFliteredData = Filter_DataFrame['channelSubscriberCount'].mean()
    averageChannelSubscriberTotalData = file['channelSubscriberCount'].mean() # 100%
    percentageChannelSubscriber = ((averageChannelSubscriberFliteredData/averageChannelSubscriberTotalData)-1) * 100 if averageChannelSubscriberTotalData else 0
    percentageChannelSubscriber = round(percentageChannelSubscriber, 0)

    First_Frame, Second_Frame, Third_Frame = st.columns(3)

    with First_Frame:
        st.markdown(f'<h4>Average Video Likes: {averageVideoLikeFliteredData:.0f}</h4>', unsafe_allow_html=True)
        if percentageVideoLike < 0:
            st.markdown(f'<h4><span style="color:red;">▼ {percentageVideoLike:.0f}% lower than the overall average.</span></h4>', unsafe_allow_html=True)
        elif percentageVideoLike > 0:
            st.markdown(f'<h4><span style="color:green;">▲ {percentageVideoLike:.0f}% higher than the overall average.</span></h4>', unsafe_allow_html=True)
        else:
            st.markdown(f'<h4><span style="color:#4682B4;">⬤ Average percentage: 100%.</span></h4>', unsafe_allow_html=True)

    with Second_Frame:
        st.markdown(f'<h4>Average Channel Views: {averageChannelViewliteredData:.0f}</h4>', unsafe_allow_html=True)
        if percentageChannelView < 0:
            st.markdown(f'<h4><span style="color:red;">▼ {percentageChannelView:.0f}% lower than the overall average.</span></h4>', unsafe_allow_html=True)
        elif percentageChannelView > 0:
            st.markdown(f'<h4><span style="color:green;">▲ {percentageChannelView:.0f}% higher than the overall average.</span></h4>', unsafe_allow_html=True)
        else:
            st.markdown(f'<h4><span style="color:#4682B4;">⬤ Average percentage: 100%.</span></h4>', unsafe_allow_html=True)

    with Third_Frame:
        st.markdown(f'<h4>Average Channel Subscribers: {averageChannelSubscriberFliteredData:.0f}</h4>', unsafe_allow_html=True)
        if percentageChannelSubscriber < 0:
            st.markdown(f'<h4><span style="color:red;">▼ {percentageChannelSubscriber:.0f}% lower than the overall average.</span></h4>', unsafe_allow_html=True)
        elif percentageChannelSubscriber > 0:
            st.markdown(f'<h4><span style="color:green;">▲ {percentageChannelSubscriber:.0f}% higher than the overall average.</span></h4>', unsafe_allow_html=True)
        else:
            st.markdown(f'<h4><span style="color:#4682B4;">⬤ Average percentage: 100%.</span></h4>', unsafe_allow_html=True)


def top10channels(Filter_DataFrame):
    Filter_DataFrame = Filter_DataFrame.drop_duplicates(subset='channelName')
    Filter_DataFrame  = Filter_DataFrame.sort_values(by = ['channelViewCount', 'channelSubscriberCount','channelGrowthScoreRank'],ascending = [False,False,True])
    top10channels = Filter_DataFrame[['channelName']].head(10)
    top10channels.reset_index(drop = True, inplace = True)
    top10channels['Rank'] = top10channels.index + 1
    top10channels_sorted = top10channels.sort_values(by = 'Rank', ascending=True)
    print(top10channels_sorted)
    chart = alt.Chart(top10channels_sorted).mark_bar().encode(
    x='Rank',  # x-axis is channel name
    y='channelName',        # y-axis is the index (which starts from 1)
    tooltip=['channelName', 'Rank']  # Tooltip to show channel name and index
    ).properties(
    title="Top 10 Channels")

    st.altair_chart(chart, use_container_width=True)
    # https://www.youtube.com/watch?v=<video_id>
    # https://www.youtube.com/watch?v=3c-iBn73dDE   


        
def streamlitMain(file,FilterContinents,FilterCountries,FilterCategory):
    # st.image("./Streamlit/DevOps.png")
    # st.title("DevOps YouTube Trends")
    # st.markdown("##")

    image_path = "./Streamlit/DevOps.png"
    base64_image = get_base64_image(image_path)
    # Display title and image in one line using HTML + CSS
    st.markdown(
        f"""
        <div style="display: flex; align-items: center;">
            <img src="data:image/png;base64,{base64_image}" width="40" height = "40" style="border-radius: 50%;"margin-right: 10px;">
            <h1 style="margin: 0; font-size: 58px;">DevOps YouTube Trends</h1>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.header("Channel Insights")
    # st.subheader("Top 10 channels")
    if "All" in FilterContinents:
        FilterContinents = file["continent"].unique().tolist()  # Get all values
    if "All" in FilterCountries:
        FilterCountries = file["country_name"].unique().tolist()  # Get all values
    if FilterCategory == "All":
        FilterCategory = file["videoContentType"].unique().tolist()  # Get all values
    else:
        FilterCategory = [FilterCategory]  # Convert to list for `.query()`

    # Filter_DataFrame  = file.query("(continent == @FilterContinents | country_name == @FilterCountries) & videoContentType == @FilterCategory")
    Filter_DataFrame = file.query(
        "(continent in @FilterContinents | country_name in @FilterCountries) & videoContentType in @FilterCategory"
    )

    if Filter_DataFrame.empty:
        st.warning("No data available based on the current filter.")
        st.stop()

    textMetricsMain(file, Filter_DataFrame)
    st.divider()
    top10channels(Filter_DataFrame)
    # st.dataframe(Filter_DataFrame)
    
def streamlitSideBar(file):
    st.sidebar.header("Filter")
    file = file.sort_values(by = 'continent', ascending = True)
    continents = file['continent'].unique()
    continents= np.append(continents, 'All')
    file = file.sort_values(by = 'country_name', ascending = True)
    countries = file['country_name'].unique()
    countries = np.append(countries, 'All')
    file = file.sort_values(by = 'videoContentType', ascending = True)
    category = file['videoContentType'].unique()
    category = np.append(category, 'All')
    FilterContinents = st.sidebar.multiselect("Select Continents", options = continents, default = 'All')
    FilterCountries = st.sidebar.multiselect("Select Countries", options = countries, default = 'All')
    FilterCategory = st.sidebar.radio("Select Category", options  = category, index=len(category) - 1)
    
    return FilterContinents, FilterCountries, FilterCategory 

def main():
    file =FetchLatestFile()
    FilterContinents, FilterCountries, FilterCategory  = streamlitSideBar(file)
    streamlitMain(file,FilterContinents,FilterCountries,FilterCategory)
    continentCountryMapping = ContinentCountryMapping(file)
    
    return True


if __name__ == "__main__":
    main()
