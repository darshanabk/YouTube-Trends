import os
from dotenv import load_dotenv
import requests
import pandas as pd
import numpy as np
import streamlit as st
import altair as alt
import plotly.colors as pc
import plotly.express as px
import plotly.graph_objects as go
import base64
import streamlit.components.v1 as components


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
    
def TextMetricMain(file, Filter_DataFrame):
    averageVideoLikeFliteredData = Filter_DataFrame['videoLikeCount'].mean()
    averageVideoLikeTotalData = file['videoLikeCount'].mean()# 100%
    percentageVideoLike = ((averageVideoLikeFliteredData/averageVideoLikeTotalData)-1) * 100 if averageVideoLikeTotalData else 0

    averageVideoViewFliteredData = Filter_DataFrame['videoViewCount'].mean()
    averageVideoViewTotalData = file['videoViewCount'].mean()# 100%
    percentageVideoView = ((averageVideoViewFliteredData/averageVideoViewTotalData)-1) * 100 if averageVideoViewTotalData else 0

    file = file.drop_duplicates(subset='channelId')
    Filter_DataFrame = Filter_DataFrame.drop_duplicates(subset='channelId')

    averageChannelViewliteredData = Filter_DataFrame['channelViewCount'].mean()
    averageChannelViewTotalData = file['channelViewCount'].mean() # 100%
    percentageChannelView = ((averageChannelViewliteredData/averageChannelViewTotalData)-1) * 100 if averageChannelViewTotalData else 0

    averageChannelSubscriberFliteredData = Filter_DataFrame['channelSubscriberCount'].mean()
    averageChannelSubscriberTotalData = file['channelSubscriberCount'].mean() # 100%
    percentageChannelSubscriber = ((averageChannelSubscriberFliteredData/averageChannelSubscriberTotalData)-1) * 100 if averageChannelSubscriberTotalData else 0
    
    First_column, Second_column, Third_column = st.columns([1,2,1])
    Sub_column1, Sub_column2 = Second_column.columns(2)

    with First_column:
        delta_value = averageVideoLikeFliteredData - averageVideoLikeTotalData
        # delta_text = f"{delta_value:.0f} ({percentageVideoLike:.0f}%)"
        delta_text = f"{delta_value:.0f}"
        st.markdown("<h5>❤  Average Likes</h5>", unsafe_allow_html=True)
        # Display metric
        st.metric(
            label="Video",
            value=f"{averageVideoLikeFliteredData:.0f}",
            delta=delta_text,
            delta_color = "normal"
        )

    with Sub_column1:
        delta_value = averageVideoViewFliteredData - averageVideoViewTotalData
        # delta_text = f"{delta_value:.0f} ({percentageChannelView:.0f}%)"
        delta_text = f"{delta_value:.0f}"
        st.markdown("<h5>👀 Average Views</h5>", unsafe_allow_html=True)
        # Display metric
        st.metric(
            label="Video",
            value=f"{averageVideoViewFliteredData:.0f}",
            delta=delta_text,
            delta_color = "normal"
        )

    with Sub_column2:
        delta_value = averageChannelViewliteredData - averageChannelViewTotalData
        # delta_text = f"{delta_value:.0f} ({percentageChannelView:.0f}%)"
        delta_text = f"{delta_value:.0f}"
        st.markdown("<h5>👀 Average Views</h5>", unsafe_allow_html=True)
        # Display metric
        st.metric(
            label="Channel",
            value=f"{averageChannelViewliteredData:.0f}",
            delta=delta_text,
            delta_color = "normal"
        )

    with Third_column:
        delta_value = averageChannelSubscriberFliteredData - averageChannelSubscriberTotalData
        # delta_text = f"{delta_value:.0f} ({percentageChannelSubscriber:.0f}%)"
        delta_text = f"{delta_value:.0f}"
        # st.markdown(f"<h5p>{person_icon}Average Channel Subscribers</h5>", unsafe_allow_html=True)
        st.write(f"<h5>{person_icon} Average Subscribers</h5>", unsafe_allow_html=True)
        # Display metric
        st.metric(
            label="Channel",
            value=f"{averageChannelSubscriberFliteredData:.0f}",
            delta=delta_text,
            delta_color = "normal"
        )

    

    def percentageDifference(percentage):
        if percentage < 0:
            st.markdown(f'<p><span style="color:red;">▼ {percentage:.0f}% </span>lower than the overall average</p>', unsafe_allow_html=True)
        elif percentage > 0:
            st.markdown(f'<p><span style="color:green;">▲ {percentage:.0f}% </span>higher than the overall average</p>', unsafe_allow_html=True)
        else:
            st.markdown(f'<p><span style="color:#4682B4;">⬤ 100% </span>overall average</p>', unsafe_allow_html=True)

    with First_column:
        percentageDifference(percentageVideoLike)

    with Sub_column1:
        percentageDifference(percentageVideoView)

    with Sub_column2:
        percentageDifference(percentageChannelView)

    with Third_column:
        percentageDifference(percentageChannelSubscriber)

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
                            #    title="Top 10 Channels by Subscribers",
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
                                    yaxis=dict(categoryorder="total ascending"),
                                    autosize=True,
                                    width=None,  # Allows automatic width adjustment
                                    height = None
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
                            #    title="Top 10 videos by Likes",
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
                                    yaxis=dict(categoryorder="total ascending"),
                                    autosize=True,
                                    width=None,  # Allows automatic width adjustment
                                    height = None
                                    )
    return fig_top10videos, Filter_DataFrame


# 🚀 Engagement Score(Average as middle value speedometer), 📈 Growth Score(Average as middle value speedometer), 🎬 Total Videos Uploaded(count), 
def averageScoreGaugeChart(file,Filter_DataFrame,column,title):
        averageScore = file[column].mean()
        averageScore = averageScore.round(0)
        min_score = file[column].min()
        max_score = file[column].max()
        filtered_averageScore = Filter_DataFrame[column].mean()
        filtered_averageScore = filtered_averageScore.round(0)
        if filtered_averageScore < averageScore:
            range_score = [min_score, averageScore+1]
            color_score = "red"
        else:
            range_score = [averageScore, max_score+1]
            color_score = "green"
        fig_score = go.Figure(go.Indicator(
        mode = 'gauge+number+delta',
        delta = {"reference": averageScore, "relative": False, "valueformat": ".0f"},
        value = filtered_averageScore,
        number={"valueformat": ".0f"}, 
        title = {'text': title, "font": {"size": 18, "weight": "bold"}},
        gauge={
        "axis": {"range": range_score},
        "bar": {"color": "black"},
        "steps": [
            {"range": range_score, "color":color_score}]
        
        }
        ))
        fig_score.update_layout(
            margin=dict(l=0, r=0, t=0, b=0),
            autosize=True,
            width=None,  # Allows automatic width adjustment
            height=None
        )
        return averageScore, fig_score

def ScoreGaugeChartMain(file, Filter_DataFrame):

    average_engagement_score, fig_engagement_score = averageScoreGaugeChart(file,Filter_DataFrame,'videoEngagementScore', "Average Engagement Score")
    average_growth_score, fig_growth_score = averageScoreGaugeChart(file,Filter_DataFrame,'channelGrowthScore',"Average Growth Score")

    First_Frame, Second_Frame = st.columns([1,1])

    with First_Frame:
        st.markdown('<h5>Overall Average Video Engagement  Score</h5>',
        unsafe_allow_html=True)
        st.markdown(f'<div style = "font-size: 36px;">🎯{average_engagement_score:.0f}</div>',unsafe_allow_html=True)
        # st.metric(label = "", value = average_engagement_score)
        First_Frame.plotly_chart(fig_engagement_score,use_container_width=True)

    
    with Second_Frame:
        st.markdown('<h5>Overall Average Channel Growth Score</h5>',
        unsafe_allow_html=True)
        st.markdown(f'<div style = "font-size: 36px;">🎯{average_growth_score:.0f}</div>',unsafe_allow_html=True)
        # st.metric(label = "Overall Average Video Engagement  Score", value = average_growth_score)
        Second_Frame.plotly_chart(fig_growth_score,use_container_width=True)


    return True

# ⏳Average Upload Frequency (`channelVideoCount / channelAgeInYears`),🎯 Like-to-View Ratio, 💬 Comment-to-View Ratio,

def FrequencyRatioMain(file, Filter_DataFrame):
    def averageFrequency(dataframe):
        dataframe = dataframe.groupby(by='channelId', as_index=False).agg({ 
        'channelName': 'first',
        'channelAgeInYears': 'mean',
        'channelVideoCount': 'mean',
        })
        averageChannelVideoCount = dataframe['channelVideoCount'].mean()
        averageChannelAgeInYears = dataframe['channelAgeInYears'].mean()
        averageUploadFreq = (averageChannelVideoCount / averageChannelAgeInYears) if averageChannelAgeInYears else 0
        return  averageUploadFreq
    
    averageUploadFreq = averageFrequency(Filter_DataFrame)
    averageOverallUploadFreq =averageFrequency(file)

    def averageRatio(file,Filter_DataFrame,column):
        averageFileRatio = file[column].mean()
        averageFilterRatio = Filter_DataFrame[column].mean()
        percentageDifference = ((averageFilterRatio / averageFileRatio)-1)*100 if averageFileRatio else 0
        return  averageFileRatio,averageFilterRatio ,percentageDifference

    first_column, second_column = st.columns([1, 2])
    with first_column:
        st.markdown("<h5>Video Performance Overview</h5>", unsafe_allow_html=True)
        with st.container():
            # ⏳Average Upload Frequency (`channelVideoCount / channelAgeInYears`)
            delta_value = averageUploadFreq - averageOverallUploadFreq
            percentage_change = (delta_value / averageOverallUploadFreq) * 100 if averageOverallUploadFreq else 0
            delta_text = f"{delta_value:.0f} (Percentage Change: {percentage_change:.0f}%)"
            st.markdown('<h6>Average Upload Frequency</h6>',unsafe_allow_html=True)
            # Display metric
            st.metric(
                label=f"{averageUploadFreq:.0f} videos posted per year",
                value=f"⏳{averageUploadFreq:.0f}",
                delta=delta_text,
                delta_color = "normal"
            )
            st.write("")
        with st.container():
            #🎯 Like-to-View Ratio
            averageFileRatio,averageFilterRatio, percentage_change  = averageRatio(file,Filter_DataFrame,"videoLikeToViewRatio")
            delta_value = averageFilterRatio - averageFileRatio
            delta_text = f"{delta_value:.4f} (Percentage Change: {percentage_change:.0f}%)"
            st.markdown('<h6>Average Like to View Ratio</h6>',unsafe_allow_html=True)
            # Display metric
            st.metric(
                label=f"Out of every 100 views, {averageFilterRatio:.4f}% received a like",
                value=f"🎯{averageFilterRatio:.4f}",
                delta=delta_text,
                delta_color = "normal"
            )
            st.write("")
        with st.container():
            # 💬 Comment-to-View Ratio
            averageFileRatio,averageFilterRatio, percentage_change  = averageRatio(file,Filter_DataFrame,"videoCommentToViewRatio")
            delta_value = averageFilterRatio - averageFileRatio
            delta_text = f"{delta_value:.4f} (Percentage Change: {percentage_change:.0f}%)"
            st.markdown('<h6>Average Comment to View Ratio</h6>',unsafe_allow_html=True)
            # Display metric
            st.metric(
                label=f"Out of every 100 views, {averageFilterRatio:.4f}% received a comment",
                value=f"💬{averageFilterRatio:.4f}",
                delta=delta_text,
                delta_color = "normal"
            )

    with second_column:
        ScoreGaugeChartMain(file, Filter_DataFrame)

    return True
# 🎯 Is in IT Hub Country?(yes/No),videoDurationClassification (Categorical column)
# channelGrowthScore and videoEngagementScore continent distribution, channelGrowthScore and videoEngagementScore country distribution
def ITHubVideoClassification(Filter_DataFrame):
    col1, col2 = st.columns([1,1]) 
    with col1:
        df_it_hub = Filter_DataFrame.groupby(['it_hub_country', 'country_name'], as_index=False).size()
        df_it_hub = df_it_hub.sort_values(by="size", ascending=False)
        blue_shades = ["#00008B", "#0000CD", "#4169E1", "#4682B4", "#1E90FF"]  # Dark Blue → Medium Blue
        orange_shades = ["#8B4513", "#D2691E", "#FF8C00", "#FFA500", "#FFD700"]  # Dark Orange → Gold
        green_shades = ["#006400", "#228B22", "#2E8B57", "#32CD32", "#00FF00"]  # Dark Green → Light Green

        yes_countries = df_it_hub[df_it_hub['it_hub_country'] == "Yes"]['country_name'].unique()
        no_countries = df_it_hub[df_it_hub['it_hub_country'] == "No"]['country_name'].unique()
        unknown_countries = df_it_hub[~df_it_hub['it_hub_country'].isin(["Yes", "No"])]["country_name"].unique()

        color_map = {}
        for i, country in enumerate(yes_countries):
            color_map[country] = orange_shades[i % len(orange_shades)]  

        for i, country in enumerate(no_countries):
            color_map[country] = blue_shades[i % len(blue_shades)]  

        for i, country in enumerate(unknown_countries):
            color_map[country] = green_shades[i % len(green_shades)]  

        fig_IT = px.bar(df_it_hub, 
                        x='it_hub_country', 
                        y='size', 
                        color='country_name', 
                        title="IT Hub Country Distribution",
                        labels={'it_hub_country': 'IT Hub', 'size': 'Count'},
                        barmode='stack', 
                        color_discrete_map=color_map,
                        category_orders={"it_hub_country": ["Yes", "No", "Unknown"]})  

        st.plotly_chart(fig_IT)

    with col2:
        fig_duration = px.pie(Filter_DataFrame, names='videoDurationClassification', 
                              title="Video Duration Classification",
                              color='videoDurationClassification')
        st.plotly_chart(fig_duration)
    

    return True

def GeoScore(Filter_DataFrame):
     
    selected_metric_label = st.selectbox("Select a metric:", ["Channel Growth", "Video Engagement"])
    metric_mapping = {
                            "Channel Growth": "channelGrowthScore",
                            "Video Engagement": "videoEngagementScore"
                        }
    selected_metric =  metric_mapping.get(selected_metric_label)
    col1, col2 = st.columns(2)  
    with col1:
        df_continent = Filter_DataFrame.groupby('continent', as_index=False).agg({
            'channelGrowthScore': 'mean',
            'videoEngagementScore': 'mean'
        })
        df_continent = df_continent.sort_values(by=selected_metric,ascending = False)
        # fig_continent = px.bar(df_continent, x='continent', y=selected_metric,
        #                        title=f"{selected_metric_label} by Continent")
        fig_continent = px.pie(
                                df_continent, 
                                names="continent",  # Categories for the pie chart
                                values=selected_metric,  # Values to determine the size of slices
                                title=f"{selected_metric_label} by Continent",
                                color="continent",  # Color by continent
                                hole=0.3  # Optional: Set this for a donut chart effect
                            )
        st.plotly_chart(fig_continent)

    with col2:
        df_country = Filter_DataFrame.groupby('country_name', as_index=False).agg({
            'channelGrowthScore': 'mean',
            'videoEngagementScore': 'mean'
        }).nlargest(10, selected_metric)  # Display Top 10 Countries
        df_country = df_country.sort_values(by=selected_metric,ascending = False)
        fig_country = px.bar(df_country, x='country_name', y=selected_metric,
                             title=f"{selected_metric_label} by Country (Top 10)")
        st.plotly_chart(fig_country)

    return True

def streamlitMain(file,FilterContinents,FilterCountries,FilterCategory,FilterYears,FilterChannelNames,FilterLicensedContent):
    # st.image("./Streamlit/DevOps.png")
    # st.title("DevOps YouTube Trends")
    # st.markdown("##")

    image_path = "./Streamlit/DevOps2.png"
    base64_image = get_base64_image(image_path)
    # Display title and image in one line using HTML + CSS
    st.markdown(
        f"""
        <div style="display: flex; align-items: center;">
            <div class="animated-box"><img src="data:image/png;base64,{base64_image}" width="35" height = "35" style="border-radius: 50%;"margin-right: 10px;"></div>
            <h1 style="margin: 0; font-size: 40px"> &nbsp; DevOps YouTube Trends</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

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
    st.divider()
    TextMetricMain(file, Filter_DataFrame)
    st.divider()
    FrequencyRatioMain(file, Filter_DataFrame)
    st.divider()
    ITHubVideoClassification(Filter_DataFrame)
    st.divider()
    GeoScore(Filter_DataFrame)
    st.divider()
    fig_top10channels = top10channels(Filter_DataFrame)
    fig_top10videos, videoFilterDataFrame= top10videos(Filter_DataFrame)

    Left_Frame, Right_Frame = st.columns([1,1])
    with Left_Frame:
        st.markdown(f"<h5>Top 10 Channels by{person_icon}Subscribers</h5>", unsafe_allow_html=True)
    with Right_Frame:
        st.markdown("<h5>Top 10 videos by ❤ Likes</h5>", unsafe_allow_html=True)

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
def get_width():
    components.html(
        """
        <script>
            var body = window.parent.document.querySelector(".main");
            var screenWidth = window.innerWidth;
            var streamlitWidth = body.clientWidth;
            var availableWidth = Math.min(screenWidth, streamlitWidth);
            window.parent.document.body.setAttribute("data-width", availableWidth);
        </script>
        """,
        height=0
    )

def main():
    
    file =FetchLatestFile()
    FilterContinents, FilterCountries, FilterCategory, FilterYears, FilterChannelNames, FilterLicensedContent  = streamlitSideBar(file)
    streamlitMain(file,FilterContinents,FilterCountries,FilterCategory, FilterYears, FilterChannelNames,FilterLicensedContent)
    continentCountryMapping = ContinentCountryMapping(file)
    return True


if __name__ == "__main__":
    st.set_page_config(layout="wide")
    # get_width()
    st.markdown( 
        """
        <style>
            @keyframes popUp {
                0% { transform: scale(0.5); opacity: 0; }
                50% { transform: scale(1.1); opacity: 1; }
                100% { transform: scale(1); }
            }
            .animated-box {
                width: 40px;
                height: 45px;
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
    person_icon = f"""
                <svg width="30" height="25" viewBox="0 0 25 25" fill="none" xmlns="http://www.w3.org/2000/svg" style="vertical-align: middle;">
                    <!-- Head (Small Circle) -->
                    <circle cx="12" cy="9" r="3" stroke="#FFFFFF" stroke-width="1" fill="#000000" />
                    <!-- Body (Big Half Circle) -->
                    <path d="M5,20 A7,7 0 0,1 19,20" stroke="#FFFFFF" stroke-width="1" fill="#000000"/>
                </svg>
                """
    
    main()
