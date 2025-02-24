
import os
from dotenv import load_dotenv
import requests
import pandas as pd
import numpy as np
import json
import streamlit as st
import altair as alt
import plotly.express as px
import plotly.graph_objects as go
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
    averageVideoLikeFliteredData = (Filter_DataFrame['videoLikeCount'].mean()).round(0)
    averageVideoLikeTotalData = (file['videoLikeCount'].mean()).round(0)# 100%
    percentageVideoLike = ((averageVideoLikeFliteredData/averageVideoLikeTotalData)-1) * 100 if averageVideoLikeTotalData else 0
    percentageVideoLike = round(percentageVideoLike, 0)

    file = file.drop_duplicates(subset='channelId')
    Filter_DataFrame = Filter_DataFrame.drop_duplicates(subset='channelId')

    averageChannelViewliteredData = (Filter_DataFrame['channelViewCount'].mean()).round(0)
    averageChannelViewTotalData = (file['channelViewCount'].mean()).round(0) # 100%
    percentageChannelView = ((averageChannelViewliteredData/averageChannelViewTotalData)-1) * 100 if averageChannelViewTotalData else 0
    percentageChannelView =  round(percentageChannelView, 0)

    averageChannelSubscriberFliteredData = (Filter_DataFrame['channelSubscriberCount'].mean()).round(0)
    averageChannelSubscriberTotalData = (file['channelSubscriberCount'].mean().round(0)) # 100%
    percentageChannelSubscriber = ((averageChannelSubscriberFliteredData/averageChannelSubscriberTotalData)-1) * 100 if averageChannelSubscriberTotalData else 0
    percentageChannelSubscriber = round(percentageChannelSubscriber, 0)
   
    person_icon = f"""
    <svg width="40" height="35" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="vertical-align: middle;">
        <!-- Head (Small Circle) -->
        <circle cx="12" cy="9" r="3" stroke="#FFFFFF" stroke-width="1" fill="#000000" />
        <!-- Body (Big Half Circle) -->
        <path d="M5,20 A7,7 0 0,1 19,20" stroke="#FFFFFF" stroke-width="1" fill="#000000"/>
    </svg>
    """
    First_column, Second_column, Third_column = st.columns(3)
    with First_column:
        st.markdown(f'<div style="font-size: 18px;">Overall Average Video Likes</div>', unsafe_allow_html=True)
        
    with Second_column:
        st.markdown(f'<div style="font-size: 18px;">Overall Average Channel Views</div>', unsafe_allow_html=True)

    with Third_column:
        # st.markdown(f'<h4>Average Channel Subscribers: 👤{averageChannelSubscriberFliteredData:.0f}</h4>', unsafe_allow_html=True)
        st.markdown(f'<div style="font-size: 18px;">Overall Average Channel Subscribers</div>', unsafe_allow_html=True)
    
    First_column, Second_column, Third_column = st.columns(3)
    with First_column:
        st.markdown(f'<h4>❤ <span style="color:#4682B4;">{averageVideoLikeTotalData:.0f}</span></h4>', unsafe_allow_html=True)

    with Second_column:
        st.markdown(f'<h4>👀 <span style="color:#4682B4;">{averageChannelViewTotalData:.0f}</span></h4>', unsafe_allow_html=True)

   
    with Third_column:
        st.markdown(f'<h4>{person_icon}<span style="color:#4682B4;">{averageChannelSubscriberTotalData:.0f}</span></h4>', unsafe_allow_html=True)

    First_column, Second_column, Third_column = st.columns(3)
    with First_column:
        if percentageVideoLike < 0:
            st.markdown(f'<h4><span style="color:red;">▼ {percentageVideoLike:.0f}% </span>lower than the overall average</h4>', unsafe_allow_html=True)
        elif percentageVideoLike > 0:
            st.markdown(f'<h4><span style="color:green;">▲ {percentageVideoLike:.0f}% </span>higher than the overall average</h4>', unsafe_allow_html=True)
        else:
            st.markdown(f'<h4><span style="color:#4682B4;">⬤ 100% </span>average video likes</h4>', unsafe_allow_html=True)

    with Second_column:
        if percentageChannelView < 0:
            st.markdown(f'<h4><span style="color:red;">▼ {percentageChannelView:.0f}% </span>lower than the overall average</h4>', unsafe_allow_html=True)
        elif percentageChannelView > 0:
            st.markdown(f'<h4><span style="color:green;">▲ {percentageChannelView:.0f}% </span>higher than the overall average</h4>', unsafe_allow_html=True)
        else:
            st.markdown(f'<h4><span style="color:#4682B4;">⬤ 100% </span>average channel views</h4>', unsafe_allow_html=True)
    
    with Third_column:
            if percentageChannelSubscriber < 0:
                st.markdown(f'<h4><span style="color:red;">▼ {percentageChannelSubscriber:.0f}% </span>lower than the overall average</h4>', unsafe_allow_html=True)
            elif percentageChannelSubscriber > 0:
                st.markdown(f'<h4><span style="color:green;">▲ {percentageChannelSubscriber:.0f}% </span>higher than the overall average</h4>', unsafe_allow_html=True)
            else:
                st.markdown(f'<h4><span style="color:#4682B4;">⬤ 100% </span>average channel subscribers</h4>', unsafe_allow_html=True)


    First_column, Second_column, Third_column = st.columns(3)
    with First_column:
        st.markdown(f'<div style="font-size: 18px;">Like Difference</div>', unsafe_allow_html=True)
        
    with Second_column:
        st.markdown(f'<div style="font-size: 18px;">View Difference</div>', unsafe_allow_html=True)

    with Third_column:
        # st.markdown(f'<h4>Average Channel Subscribers: 👤{averageChannelSubscriberFliteredData:.0f}</h4>', unsafe_allow_html=True)
        st.markdown(f'<div style="font-size: 18px;">Subscriber Difference</div>', unsafe_allow_html=True)
        
    First_column, Second_column, Third_column = st.columns(3)
    with First_column:
        difference =  int(averageVideoLikeFliteredData - averageVideoLikeTotalData)
        if difference == 0:
            color = "color:#4682B4;"
        elif difference > 0:
            color = "color:green;"
            difference = "+"+str(difference)
        elif difference <0:
            color = "color:red;"
        st.markdown(f'<h4>❤ <span style={color}>{difference}</span></h4>', unsafe_allow_html=True)

    with Second_column:
        difference = int(averageChannelViewliteredData - averageChannelViewTotalData)
        if difference == 0:
            color = "color:#4682B4;"
        elif difference > 0:
            color = "color:green;"
            difference = "+"+str(difference)
        elif difference <0:
            color = "color:red;"
        st.markdown(f'<h4>👀 <span style={color}>{difference}</span></h4>', unsafe_allow_html=True)

    with Third_column:
        difference = int(averageChannelSubscriberFliteredData - averageChannelSubscriberTotalData)
        if difference == 0:
            color = "color:#4682B4;"
        elif difference > 0:
            color = "color:green;"
            difference = "+"+str(difference)
        elif difference <0:
            color = "color:red;"
        st.markdown(f'<h4>{person_icon}<span style={color}>{difference}</span></h4>', unsafe_allow_html=True)

    # First_column, Second_column, Third_column = st.columns(3)
    # with First_column:
    #     st.markdown(f'<div style="font-size: 18px;">Average Video Likes</div>', unsafe_allow_html=True)
        
    # with Second_column:
    #     st.markdown(f'<div style="font-size: 18px;">Average Channel Views</div>', unsafe_allow_html=True)

    # with Third_column:
    #     # st.markdown(f'<h4>Average Channel Subscribers: 👤{averageChannelSubscriberFliteredData:.0f}</h4>', unsafe_allow_html=True)
    #     st.markdown(f'<div style="font-size: 18px;">Average Channel Subscribers</div>', unsafe_allow_html=True)
        
    # First_column, Second_column, Third_column = st.columns(3)
    # with First_column:
    #     st.markdown(f'<h4>❤ {averageVideoLikeFliteredData:.0f}</h4>', unsafe_allow_html=True)

    # with Second_column:
    #     st.markdown(f'<h4>👀 {averageChannelViewliteredData:.0f}</h4>', unsafe_allow_html=True)

    # person_icon = f"""
    # <svg width="40" height="35" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="vertical-align: middle;">
    #     <!-- Head (Small Circle) -->
    #     <circle cx="12" cy="9" r="3" stroke="#FFFFFF" stroke-width="1" fill="#000000" />
    #     <!-- Body (Big Half Circle) -->
    #     <path d="M5,20 A7,7 0 0,1 19,20" stroke="#FFFFFF" stroke-width="1" fill="#000000"/>
    # </svg>
    # """
    # with Third_column:
    #     st.markdown(f'<h4>{person_icon}{averageChannelSubscriberFliteredData:.0f}</h4>', unsafe_allow_html=True)
    
    
    

def top10channels(Filter_DataFrame):
    Filter_DataFrame['channelLink'] = "https://www.youtube.com/channel/" + Filter_DataFrame["channelId"]
    Filter_DataFrame = Filter_DataFrame.groupby(by='channelId', as_index=False).agg({
    'channelName': 'first',  # Keeping the first occurrence of channelName
    'channelSubscriberCount': 'mean',
    'channelViewCount': 'mean',
    'channelGrowthScoreRank': 'mean',
    'channelLink': 'first'
    })
    Filter_DataFrame  = Filter_DataFrame.sort_values(
        by = ['channelSubscriberCount','channelViewCount', 'channelGrowthScoreRank'],
        ascending = [False,False,True]
    )
    Filter_DataFrame = Filter_DataFrame.head(10)
    Filter_DataFrame.reset_index(inplace = True)
    fig_top10channels = px.bar(Filter_DataFrame, 
                               x = "channelSubscriberCount",
                               y = "channelName",
                               orientation = "h",
                               title="Top 10 Channels by Subscribers",
                               color_discrete_sequence=["#4682B4"]*len(Filter_DataFrame),
                               template="plotly_dark",
                               custom_data=['channelLink']
                                )
    
    fig_top10channels.update_xaxes(title=None)  # Hide X-axis title
    fig_top10channels.update_yaxes(title=None)  # Hide Y-axis title
    for i, row in Filter_DataFrame.iterrows():
        fig_top10channels.add_annotation(
            x=row["channelSubscriberCount"], 
            y=row["channelName"],
            text=f"<a href='{row['channelLink']}' target='_blank'>🔗</a>",
            showarrow=False,
            xshift=10  # Adjusts position slightly for better visibility
        )
    fig_top10channels.update_layout(plot_bgcolor="rgba(0,0,0,0)", 
                                    xaxis=dict(showgrid=False),  
                                    yaxis=dict(categoryorder="total ascending")  
                                    )
    return fig_top10channels

def top10videos(Filter_DataFrame):
    Filter_DataFrame['videoLink'] = "https://www.youtube.com/watch?v=" + Filter_DataFrame['videoId']
    Filter_DataFrame = Filter_DataFrame.groupby(by='videoId', as_index=False).agg({
    'videoTitle': 'first', 
    'channelName': 'first',
    'videoLikeCount': 'mean',
    'videoViewCount': 'mean',
    'videoEngagementScoreRank': 'mean',
    'videoLink': 'first'
    })
    Filter_DataFrame  = Filter_DataFrame.sort_values(
        by = ['videoLikeCount','videoViewCount', 'videoEngagementScoreRank'],
        ascending = [False,False,True]
    )
    Filter_DataFrame = Filter_DataFrame.head(10)
    Filter_DataFrame.reset_index(inplace = True)
    Filter_DataFrame["channelVideo"] = Filter_DataFrame["channelName"] + " - V" + (Filter_DataFrame.index + 1).astype(str)
    fig_top10videos = px.bar(Filter_DataFrame, 
                               x = "videoLikeCount",
                               y = "channelVideo",
                               orientation = "h",
                               title="Top 10 videos by Likes",
                               color_discrete_sequence=["#4682B4"]*len(Filter_DataFrame),
                               template="plotly_dark",
                               custom_data=['videoLink']
                                )
    
    fig_top10videos.update_xaxes(title=None)  # Hide X-axis title
    fig_top10videos.update_yaxes(title=None)  # Hide Y-axis title
    for i, row in Filter_DataFrame.iterrows():
        fig_top10videos.add_annotation(
            x=row["videoLikeCount"], 
            y=row["channelVideo"],
            text=f"<a href='{row['videoLink']}' target='_blank'>🔗</a>",
            showarrow=False,
            xshift=10,  # Adjusts position slightly for better visibility
            hovertext=row["videoTitle"]
        )
    # fig_top10videos.update_traces(
    #                                 hovertemplate="<b>%{y}</b><br>Likes: %{x}<br>Title:<br>%{customdata[0]}",
    #                                 customdata=Filter_DataFrame[['videoTitle']]
    #                             )
    fig_top10videos.update_layout(plot_bgcolor="rgba(0,0,0,0)", 
                                    xaxis=dict(showgrid=False),  
                                    yaxis=dict(categoryorder="total ascending")  
                                    )
    return fig_top10videos, Filter_DataFrame


# 🚀 Engagement Score(Average as middle value speedometer), 📈 Growth Score(Average as middle value speedometer), 🎬 Total Videos Uploaded(count), 

def ScoreGaugeChartMain(file, Filter_DataFrame):
    average_engagement_score = file['videoEngagementScore'].mean()
    average_engagement_score = average_engagement_score.round(0)
    min_engagement_score = file['videoEngagementScore'].min()
    max_engagement_score = file['videoEngagementScore'].max()
    filtered_average_engagement_score = Filter_DataFrame['videoEngagementScore'].mean()
    filtered_average_engagement_score = filtered_average_engagement_score.round(0)
    if filtered_average_engagement_score < average_engagement_score:
        range_engagement_score = [min_engagement_score, average_engagement_score+1]
        color_engagement_score = "red"
    else:
        range_engagement_score = [average_engagement_score, max_engagement_score+1]
        color_engagement_score = "green"

    average_growth_score = file['channelGrowthScore'].mean()
    average_growth_score = average_growth_score.round(0)
    min_growth_score = file['channelGrowthScore'].min()
    max_growth_score = file['channelGrowthScore'].max()
    filtered_average_growth_score = Filter_DataFrame['channelGrowthScore'].mean()
    filtered_average_growth_score = filtered_average_growth_score.round(0)
    if filtered_average_growth_score < average_growth_score:
        range_growth_score = [min_growth_score, average_growth_score+1]
        color_growth_score = "red"
    else:
        range_growth_score = [average_growth_score, max_growth_score+1]
        color_growth_score = "green"


    fig_engagement_score = go.Figure(go.Indicator(
        mode = 'gauge+number+delta',
        delta = {"reference": average_engagement_score, "relative": False, "valueformat": ".0f"},
        value = filtered_average_engagement_score,
        number={"valueformat": ".0f"}, 
        title = {'text': "Average Engagement Score", "font": {"size": 18}},
        gauge={
        "axis": {"range": range_engagement_score},
        "bar": {"color": "black"},
        "steps": [
            {"range": range_engagement_score, "color":color_engagement_score}]
        
    }
    ))

    fig_growth_score = go.Figure(go.Indicator(
        mode = 'gauge+number+delta',
        delta = {"reference": average_growth_score,"relative": False, "valueformat": ".0f"},
        value = filtered_average_growth_score,
        number={"valueformat": ".0f"}, 
        title = {'text': "Average Growth Score", "font": {"size": 18}},
        gauge={
        "axis": {"range": range_growth_score},
        "bar": {"color": "black"},
        "steps": [
            {"range": range_growth_score, "color": color_growth_score}
        ]
        
    }
    ))

    First_Frame, Second_Frame = st.columns(2)

    with First_Frame:
        st.markdown('<div style="font-size: 18px;">Overall Average Video Engagement  Score</div>',
         unsafe_allow_html=True)
        st.markdown(f'<div style = "font-weight: bold;font-size: 24px;">{average_engagement_score}</div>',unsafe_allow_html=True)
        # st.metric(label = "", value = average_engagement_score)
        st.plotly_chart(fig_engagement_score,use_container_width=True)

    
    with Second_Frame:
        st.markdown('<div style="font-size: 18px;">Overall Average Channel Growth Score</div>',
         unsafe_allow_html=True)
        st.markdown(f'<div style = "font-weight: bold;font-size: 24px;">{average_growth_score}</div>',unsafe_allow_html=True)
        # st.metric(label = "Overall Average Video Engagement  Score", value = average_growth_score)
        st.plotly_chart(fig_growth_score,use_container_width=True)

    return True

# ⏳Average Upload Frequency (`channelVideoCount / channelAgeInYears`),🎯 Like-to-View Ratio, 💬 Comment-to-View Ratio,
# 🎯 Is in IT Hub Country?(Pie Chart), videoDurationClassification (Pie), videoPublishedWeekDay(Pie) , videoDefinition, videoDimension

def FrequencyRatioITHubMain(file, Filter_DataFrame):
    averageChannelVideoCount = file.groupby(by='channel', as_index=False).agg({
    'videoTitle': 'first', 
    'channelName': 'first',
    'videoLikeCount': 'mean',
    'videoViewCount': 'mean',
    'videoEngagementScoreRank': 'mean',
    })
    return True

def streamlitMain(file,FilterContinents,FilterCountries,FilterCategory,FilterYears,FilterChannelNames,FilterLicensedContent):
    # st.image("./Streamlit/DevOps.png")
    # st.title("DevOps YouTube Trends")
    # st.markdown("##")

    image_path = "./Streamlit/DevOps.png"
    base64_image = get_base64_image(image_path)
    # Display title and image in one line using HTML + CSS
    st.markdown(
        f"""
        <div style="display: flex; align-items: center;">
            <div class="animated-box"><img src="data:image/png;base64,{base64_image}" width="40" height = "40" style="border-radius: 50%;"margin-right: 10px;"></div>
            <h1 style="margin: 0; font-size: 58px;" class = "custom-text">DevOps YouTube Trends</h1>
        </div>
        """,
        unsafe_allow_html=True
    )
    # st.header("Channel Insights")
    # st.subheader("Top 10 channels")
    file["videoPublishYear"] = file["videoPublishYear"].astype(str)
    file["videoLicensedContent"] = file["videoLicensedContent"].astype(str)
    if "All" in FilterContinents:
        FilterContinents = file["continent"].unique().tolist()  # Get all values
    if "All" in FilterCountries:
        FilterCountries = file["country_name"].unique().tolist()  # Get all values
    if "All" in FilterYears:
        FilterYears = file["videoPublishYear"].unique().tolist()
    if "All" in FilterChannelNames:
        FilterChannelNames = file["channelName"].unique().tolist()
    if FilterCategory == "All":
        FilterCategory = file["videoContentType"].unique().tolist()  # Get all values
    else:
        FilterCategory = [FilterCategory]  # Convert to list for `.query()`
    if FilterLicensedContent == "All":
        FilterLicensedContent = file["videoLicensedContent"].unique().tolist()
    else:
        FilterLicensedContent = [FilterLicensedContent]

    Filter_DataFrame  = file.query("(continent in @FilterContinents | country_name in @FilterCountries | channelName in @FilterChannelNames) & videoContentType in @FilterCategory & videoPublishYear in @FilterYears & videoLicensedContent in @FilterLicensedContent")
    # Filter_DataFrame = file.query("(continent in @FilterContinents & videoPublishYear in @FilterYears)| (country_name in @FilterCountries & videoPublishYear in @FilterYears) & videoContentType in @FilterCategory")

    if Filter_DataFrame.empty:
        st.warning("No data available based on the current filter.")
        st.stop()

    textMetricsMain(file, Filter_DataFrame)
    st.divider()
    ScoreGaugeChartMain(file, Filter_DataFrame)
    st.divider()
    fig_top10channels = top10channels(Filter_DataFrame)
    fig_top10videos, videoFilterDataFrame= top10videos(Filter_DataFrame)
    Left_Frame, Right_Frame = st.columns(2)
    Left_Frame.plotly_chart(fig_top10channels,use_container_width=True)
    Right_Frame.plotly_chart(fig_top10videos,use_container_width=True)
    st.divider()
   
    # st.dataframe(Filter_DataFrame)
    
def streamlitSideBar(file):
    st.sidebar.header("Filter")
    file = file.sort_values(by = 'continent', ascending = True)
    continents = file['continent'].unique()
    continents= np.append(continents, 'All')
    file = file.sort_values(by = 'country_name', ascending = True)
    countries = file['country_name'].unique()
    countries = np.append(countries, 'All')
    file = file.sort_values(by ="videoPublishYear",ascending = True)
    Years = file['videoPublishYear'].unique()
    Years = np.append(Years, 'All')
    Years = Years.astype(str)
    file = file.sort_values(by = 'videoContentType', ascending = True)
    category = file['videoContentType'].unique()
    category = np.append(category, 'All')
    file = file.sort_values(by = 'channelName', ascending = True)
    channelNames = file['channelName'].unique()
    channelNames = np.append(channelNames, 'All')
    file = file.sort_values(by = 'videoLicensedContent', ascending = True)
    licensedContent = file['videoLicensedContent'].unique()
    licensedContent = np.append(licensedContent, 'All')
    licensedContent = licensedContent.astype(str)


    FilterContinents = st.sidebar.multiselect("Select Continents", options = continents, default = 'All')
    st.sidebar.write("OR")
    FilterCountries = st.sidebar.multiselect("Select Countries", options = countries, default = 'All')
    st.sidebar.write("OR")
    FilterChannelNames = st.sidebar.multiselect("Select Channels", options = channelNames, default = 'All' )
    st.sidebar.write("AND")
    FilterYears = st.sidebar.multiselect("Select Years", options = Years, default = 'All')
    st.sidebar.write("AND")
    FilterCategory = st.sidebar.radio("Select Category", options  = category, index=len(category) - 1)
    st.sidebar.write("AND")
    FilterLicensedContent = st.sidebar.radio("Select Licensed Content", options = licensedContent, index=len(category) - 1)
    
    return FilterContinents, FilterCountries, FilterCategory, FilterYears, FilterChannelNames, FilterLicensedContent

def main():
    file =FetchLatestFile()
    FilterContinents, FilterCountries, FilterCategory, FilterYears, FilterChannelNames, FilterLicensedContent  = streamlitSideBar(file)
    streamlitMain(file,FilterContinents,FilterCountries,FilterCategory, FilterYears, FilterChannelNames,FilterLicensedContent)
    continentCountryMapping = ContinentCountryMapping(file)
    

    return True


if __name__ == "__main__":
    st.set_page_config(layout="wide")
    st.markdown( 
"""
    <style>
        @keyframes popUp {
            0% { transform: scale(0.5); opacity: 0; }
            50% { transform: scale(1.1); opacity: 1; }
            100% { transform: scale(1); }
        }
        .animated-box {
            width: 45px;
            height: 50px;
            background-color:white;
            color: white;
            font-size: 24px;
            font-weight: bold;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 20px 0px 20px 0px;
           box-shadow: 4px 4px 15px #ff4b4b;
            animation: popUp 0.5s ease-out;
            margin: 10px;
        }
        :root {
            --shadow-color: rgba(70, 130, 180, 0.6);  /* Light blue shadow for light mode */
        }

        @media (prefers-color-scheme: dark) {
            :root {
                --shadow-color: rgba(135, 206, 250, 0.8);  /* Sky blue shadow for dark mode */
            }
        }

        .custom-text {
            font-size: 48px;
            font-weight: bold;
            text-align: center;
            color: inherit;  /* Inherit text color from theme */
            text-shadow: 1px 1px 3px var(--shadow-color); /* Adaptive shadow */
        }
    </style>
    """,
        unsafe_allow_html=True
    )

    main()
