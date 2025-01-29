### JSON Format for Source Single Record (Raw Data Sample)

```json
[
  {
    "currentDate": "YYYY-MM-DD",          // String (Date in ISO 8601 format, e.g., "2025-01-28")
    "channelId": "string",                // String (Unique identifier for the channel, e.g., "UCdngmbVKX1Tgre699-XLlUA")
    "channelName": "string",              // String (Name of the YouTube channel, e.g., "TechWorld with Nana")
    "videoId": "string",                  // String (Unique identifier for the video, e.g., "3c-iBn73dDE")
    "videoTitle": "string",               // String (Title of the video, e.g., "Docker Tutorial for Beginners [FULL COURSE in 3 Hours]")
    "videoPublishYear": "integer",        // Integer (Year when the video was published, e.g., 2020)
    "videoPublishMonth": "integer",       // Integer (Month when the video was published, e.g., 10)
    "videoPublishDay": "integer",         // Integer (Day when the video was published, e.g., 21)
    "videoPublishTime": "HH:MM:SS",       // String (Time when the video was published in 24-hour format, e.g., "19:26:53")
    "videoPublishedOn": "ISO 8601",       // String (Full ISO 8601 timestamp, e.g., "2020-10-21T19:26:53Z")
    "videoPublishedOnInSeconds": "integer", // Integer (Timestamp in seconds, e.g., 1603308413)
    "videoUniqueId": "string",            // String (Unique identifier for the video, e.g., "3c-iBn73dDE")
    "videoViewCount": "integer",          // Integer (Total number of views, e.g., 5473802)
    "videoLikeCount": "integer",          // Integer (Total number of likes, e.g., 93038)
    "videoFavoriteCount": "integer",      // Integer (Total number of favorites, e.g., 0)
    "videoCommentCount": "integer",       // Integer (Total number of comments, e.g., 4539)
    "videoDescription": "string",         // String (Description of the video, e.g., "Full Docker Tutorial...")
    "videoTags": ["string"],              // Array of Strings (Tags associated with the video, e.g., ["docker tutorial", "docker course"])
    "videoCategoryId": "integer",         // Integer (ID representing the video category, e.g., 27)
    "videoLiveBroadcastContent": "string",// String (Type of live broadcast content, e.g., "none")
    "videoDefaultLanguage": "string",     // String (Default language of the video, e.g., "en")
    "videoDefaultAudioLanguage": "string",// String (Default audio language of the video, e.g., "en")
    "videoDuration": "ISO 8601",          // String (Video duration in ISO 8601 format, e.g., "PT2H46M15S")
    "videoDurationInSeconds": "integer",  // Integer (Duration of the video in seconds, e.g., 9975)
    "videoContentType": "string",          // String (Content type of the video, e.g., "Video")
    "videoDimension": "string",           // String (Dimension of the video, e.g., "2d")
    "videoDefinition": "string",          // String (Quality of the video, e.g., "hd")
    "videoCaption": "boolean",            // Boolean (Whether the video has captions, e.g., true)
    "videoLicensedContent": "boolean",    // Boolean (Whether the video contains licensed content, e.g., true)
    "videoProjection": "string",          // String (Projection type of the video, e.g., "rectangular")
    "channelIdUnique": "string",          // String (Unique identifier for the channel, e.g., "UCdngmbVKX1Tgre699-XLlUA")
    "channelTitleCheck": "string",        // String (Channel name for verification purposes, e.g., "TechWorld with Nana")
    "channelDescription": "string",       // String (Description of the YouTube channel, e.g., "Helping millions of engineers...")
    "channelCustomUrl": "string",         // String (Custom URL of the channel, e.g., "@techworldwithnana")
    "channelPublishYear": "integer",      // Integer (Year when the channel was created, e.g., 2019)
    "channelPublishMonth": "integer",     // Integer (Month when the channel was created, e.g., 10)
    "channelPublishDay": "integer",       // Integer (Day when the channel was created, e.g., 6)
    "channelPublishTime": "HH:MM:SS",     // String (Time when the channel was created in 24-hour format, e.g., "08:50:17")
    "channelPublishedOn": "ISO 8601",     // String (Full ISO 8601 timestamp, e.g., "2019-10-06T08:50:17Z")
    "channelPublishedOnInSeconds": "integer", // Integer (Timestamp in seconds, e.g., 1570351817)
    "channelCountry": "string",           // String (Country of the channel, e.g., "AT")
    "channelViewCount": "integer",        // Integer (Total number of views for the channel, e.g., 64177976)
    "channelSubscriberCount": "integer", // Integer (Total number of subscribers, e.g., 1200000)
    "channelVideoCount": "integer"        // Integer (Total number of videos in the channel, e.g., 126)
  }
]

```
Below is a detailed tabular column for all the fields specified in data structure. The column includes **Field Name**, **Min Length**, **Max Length**, **Value Type**, **Special Format/Notes**, and **KPI**. 

| **Field Name**                    | **Min Length** | **Max Length** | **Value Type**      | **Special Format/Notes**                                                                                     | **KPI** |
|-----------------------------------|----------------|----------------|---------------------|-------------------------------------------------------------------------------------------------------------|---------|
| `currentDate`                     | 10             | 10             | String (ISO 8601)  | Date in ISO 8601 format, e.g., `2025-01-28`. **Note:** Date when file created                                                              | No      |
| `channelId`                       | 24             | 24             | String              | Unique identifier for the channel, e.g., `UCdngmbVKX1Tgre699-XLlUA`.                                        | Yes     |
| `channelName`                     | 1              | 100            | String              | Name of the YouTube channel, e.g., `TechWorld with Nana`.                                                   | Yes     |
| `videoId`                         | 11             | 11             | String              | Unique identifier for the video, e.g., `3c-iBn73dDE`.                                                       | Yes     |
| `videoTitle`                      | 1              | 100            | String              | Title of the video, e.g., `Docker Tutorial for Beginners [FULL COURSE in 3 Hours]`.                         | Yes     |
| `videoPublishYear`                | 4              | 4              | Integer             | Year when the video was published, e.g., `2020`.                                                            | No      |
| `videoPublishMonth`               | 1              | 2              | Integer             | Month when the video was published, e.g., `10`.                                                             | No      |
| `videoPublishDay`                 | 1              | 2              | Integer             | Day when the video was published, e.g., `21`.                                                               | No      |
| `videoPublishTime`                | 8              | 8              | String (HH:MM:SS)   | Time when the video was published in 24-hour format, e.g., `19:26:53`.                                      | No      |
| `videoPublishedOn`                | 20             | 20             | String (ISO 8601)  | Full ISO 8601 timestamp, e.g., `2020-10-21T19:26:53Z`.                                                      | No      |
| `videoPublishedOnInSeconds`       | 1              | N/A            | Integer             | Timestamp in seconds, e.g., `1603308413`. **Note:** The total number of seconds from **0001-01-01 00:00:00 UTC** to **1970-01-01 00:00:00 UTC** is **62,135,596,800 seconds**. Timestamps are typically calculated from **1970-01-01 00:00:00 UTC (Unix epoch)** onwards.| No |
| `videoUniqueId`                   | 11             | 11             | String              | Alias for `videoId`.                                                                                        | Yes     |
| `videoViewCount`                  | 0              | N/A            | Integer             | Total number of views, e.g., `5473802`.                                                                     | Yes     |
| `videoLikeCount`                  | 0              | N/A            | Integer             | Total number of likes, e.g., `93038`.                                                                       | Yes     |
| `videoFavoriteCount`              | 0              | N/A            | Integer             | Total number of favorites, e.g., `0`.                                                                       | No      |
| `videoCommentCount`               | 0              | N/A            | Integer             | Total number of comments, e.g., `4539`.                                                                     | Yes     |
| `videoDescription`                | 0              | 5000           | String              | Description of the video, e.g., `Full Docker Tutorial...`.                                                  | No      |
| `videoTags`                       | 0              | N/A            | Array of Strings    | Tags associated with the video, e.g., `["docker tutorial", "docker course"]`. **Count**: Min: `0`, Max: `500`. | No      |
| `videoCategoryId`                 | 1              | 3              | Integer             | ID representing the video category, e.g., `27`.                                                             | No      |
| `videoLiveBroadcastContent`       | 4              | 20             | String              | Type of live broadcast content, e.g., `none`.                                                               | No      |
| `videoDefaultLanguage`            | 2              | 3              | String              | Default language of the video, e.g., `en`.                                                                  | No      |
| `videoDefaultAudioLanguage`       | 2              | 3              | String              | Default audio language of the video, e.g., `en`.                                                            | No      |
| `videoDuration`                   | 5              | 15             | String (ISO 8601)  | Video duration in ISO 8601 format, e.g., `PT2H46M15S`.                                                      | No      |
| `videoDurationInSeconds`          | 1              | N/A            | Integer             | Duration of the video in seconds, e.g., `9975`.                                                             | No      |
| `videoContentType`                | 5              | 6              | String              | Content type of the video, e.g., `Video`. **Note:** `Short` or `Video` or `Unknown`                         | No      |
| `videoDimension`                  | 2              | 3              | String              | Dimension of the video, e.g., `2d`.                                                                         | No      |
| `videoDefinition`                 | 2              | 2              | String              | Quality of the video, e.g., `hd`.                                                                           | No      |
| `videoCaption`                    | 4              | 5              | Boolean             | Whether the video has captions, e.g., `true`.                                                               | No      |
| `videoLicensedContent`            | 4              | 5              | Boolean             | Whether the video contains licensed content, e.g., `true`.                                                  | No      |
| `videoProjection`                 | 5              | 12             | String              | Projection type of the video, e.g., `rectangular`.                                                          | No      |
| `channelIdUnique`                 | 24             | 24             | String              | Alias for `channelId`.                                                                                      | Yes     |
| `channelTitleCheck`               | 1              | 100            | String              | Alias for `channelName`.                                                                                    | Yes     |
| `channelDescription`              | 0              | 5000           | String              | Description of the YouTube channel, e.g., `Helping millions of engineers...`.                               | No      |
| `channelCustomUrl`                | 3              | 100            | String              | Custom URL of the channel, e.g., `@techworldwithnana`.                                                      | No      |
| `channelPublishYear`              | 4              | 4              | Integer             | Year when the channel was created, e.g., `2019`.                                                            | No      |
| `channelPublishMonth`             | 1              | 2              | Integer             | Month when the channel was created, e.g., `10`.                                                             | No      |
| `channelPublishDay`               | 1              | 2              | Integer             | Day when the channel was created, e.g., `6`.                                                                | No      |
| `channelPublishTime`              | 8              | 8              | String (HH:MM:SS)   | Time when the channel was created in 24-hour format, e.g., `08:50:17`.                                      | No      |
| `channelPublishedOn`              | 20             | 20             | String (ISO 8601)  | Full ISO 8601 timestamp, e.g., `2019-10-06T08:50:17Z`.                                                      | No      |
| `channelPublishedOnInSeconds`     | 1              | N/A            | Integer             | Timestamp in seconds, e.g., `1570351817`. **Note:** The total number of seconds from **0001-01-01 00:00:00 UTC** to **1970-01-01 00:00:00 UTC** is **62,135,596,800 seconds**. Timestamps are typically calculated from **1970-01-01 00:00:00 UTC (Unix epoch)** onwards.| No |
| `channelCountry`                  | 2              | 2              | String              | Country of the channel, e.g., `AT`.                                                                         | No      |
| `channelViewCount`                | 0              | N/A            | Integer             | Total number of views for the channel, e.g., `64177976`.                                                    | Yes     |
| `channelSubscriberCount`          | 0              | N/A            | Integer             | Total number of subscribers, e.g., `1200000`.                                                               | Yes     |
| `channelVideoCount`               | 0              | N/A            | Integer             | Total number of videos in the channel, e.g., `126`.                                                         | Yes     |

