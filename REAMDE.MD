# Detailed Architecture Explanation

## Overview

The system is divided into three main parts, each with a specific objective:

1. Video Synchronization Jobs
2. Auto-Upload Job
3. Search and Events Endpoints

## 1. Video Synchronization Jobs

### Objective:
Periodically pull public and private videos from various sources, index, and save them to create a holistic view of the video data.

### Components:
- **Video Handlers**: Modules to handle video fetching from different sources (e.g., Google Drive, YouTube, Zoom, Gong).
- **Airflow DAGs**: Workflows in Apache Airflow to manage the periodic execution of video synchronization tasks.
- **Data Storage**: A centralized repository (e.g., a database) to store metadata and indexed information about the videos.

### Process:
1. **Fetch User URLs**: Retrieve URLs of videos to be synchronized from a user-specific source (e.g., a database or an API).
2. **Process URLs**: Use the appropriate handler to process each URL and retrieve video data.
3. **Index Data**: Create an index of the video data for efficient search and retrieval.
4. **Save to Database**: Store the indexed video data in a database.

### Importance of Holistic View:
- **Foundation for Auto-Upload Jobs**: Provides a complete and up-to-date repository of all video data, enabling automated rules to upload videos accurately based on predefined criteria.
- **Video Search**: Allows users to search across the entire video data set, providing comprehensive search results from multiple sources.
- **User Inquiries and Updates**: Supports endpoints to notify users of new updates and allows them to query the entire dataset for specific information.

## 2. Auto-Upload Job

### Objective:
Periodically pull auto-upload rules and use the holistic view of the video data to upload videos according to preset rules.

### Components:
- **Auto-Upload Rule Fetcher**: A component to fetch the auto-upload rules from a predefined source.
- **Airflow DAGs**: Workflows to schedule and execute the auto-upload tasks based on the rules.
- **Uploader**: A component that handles the actual uploading of videos according to the fetched rules.

### Process:
1. **Fetch Auto-Upload Rules**: Retrieve the rules for auto-uploading videos.
2. **Match Rules with Data**: Use the holistic view of the video data to determine which videos need to be uploaded according to the rules.
3. **Upload Videos**: Upload the matched videos to the specified destinations.

### Dependency on Holistic View:
The holistic view created in Part 1 ensures that the auto-upload job has access to the latest and most complete video data, enabling accurate and efficient video uploads based on user-defined rules.

## 3. Search and Events Endpoints

### Objective:
Provide endpoints to query the entire video data for new updates and perform searches.

### Components:
- **Search API**: An endpoint to search through the indexed video data.
- **Events API**: An endpoint to provide updates and notifications about new or changed video data.

### Process:
1. **Search Endpoint (`/search`)**: Allows users to search for videos based on various criteria (e.g., keywords, date range).
2. **Events Endpoint (`/events`)**: Provides notifications or updates about new video uploads, changes, or other relevant events.

### Dependency on Holistic View:
The holistic view of video data is essential for providing accurate and comprehensive search results and event notifications. It ensures that users have access to a unified dataset, making the search and event functionalities reliable and effective.

## Overall System Architecture

### Airflow DAGs for Scheduling:

#### Video Sync DAG:
- **Task 1**: Fetch User URLs
- **Task 2**: Process URLs
- **Task 3**: Index Data
- **Task 4**: Save to Database

#### Auto-Upload DAG:
- **Task 1**: Fetch Auto-Upload Rules
- **Task 2**: Match Rules with Data
- **Task 3**: Upload Videos

### Components Interaction:
- **Video Handlers**: Communicate with video sources to fetch video data.
- **Database**: Central repository for storing indexed video data.
- **Search and Events API**: Interface for querying and interacting with the video data.
