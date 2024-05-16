import pandas as pd 
from googleapiclient.discovery import build
import re
from lib.helpers import write_jsonl, read_json
import time
from datetime import datetime,timedelta
from lib.nlp_helpers import remove_extra_spaces
import os

#########################################################################################
# HELPERS
#########################################################################################

def YT_duration_to_milliseconds(duration):
    # Regular expression to match ISO 8601 duration format
    duration_pattern = re.compile(r'P(?:(\d+)D)?T(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?')
    
    # Match the duration string against the pattern
    match = duration_pattern.match(duration)
    if not match:
        return None

    # Extracting days, hours, minutes, and seconds
    days = int(match.group(1)) if match.group(1) else 0
    hours = int(match.group(2)) if match.group(2) else 0
    minutes = int(match.group(3)) if match.group(3) else 0
    seconds = int(match.group(4)) if match.group(4) else 0

    # Calculate total duration in milliseconds
    total_milliseconds = ((days * 24 + hours) * 60 + minutes) * 60 + seconds
    total_milliseconds *= 1000

    return total_milliseconds

def create_queries_per_period(query, publishedAfter, publishedBefore, col_publishedAfter = "publishedAfter", col_publishedBefore = "publishedBefore", date_format = '%Y-%m-%dT%H:%M:%SZ', rolling_days = 7 ):
    datetime_publishedAfter = datetime.strptime(publishedAfter, date_format)
    datetime_publishedBefore = datetime.strptime(publishedBefore, date_format)
    
    queries = []

    end = datetime_publishedBefore 

    while end > datetime_publishedAfter:
        
        start = end - timedelta(days=rolling_days)
        # print(end_date, start_date)
        if start < datetime_publishedAfter :
            start = datetime_publishedAfter

        query_copy = query.copy()
        start_str = start.strftime(date_format)
        end_str = end.strftime(date_format)
        query_copy[col_publishedAfter] = start_str
        query_copy[col_publishedBefore] = end_str
        
        queries.append(query_copy)
        end = start
    
    return queries

#########################################################################################
# API queries functions
#########################################################################################

def YT_client(api_key, api_service_name="youtube", api_version="v3"):
    """
    Instantiate a new client using an API KEY
    """
    client = build(api_service_name, api_version, developerKey=api_key)
    return client

def check_keys(lst_api_keys):
    status_ok = False
    for key_idx, apifile_path in enumerate(lst_api_keys):
        api_filename = os.path.splitext(os.path.basename(apifile_path))[0]
        api_key_data = read_json(apifile_path)
        current_quota =  api_key_data.get("current_quota")
        allowed = api_key_data.get("allowed")
        print(api_key_data.get("key"), current_quota, status_ok)
        if current_quota < allowed:
            status_ok = True
            break
        else:
            status_ok = False
    return api_filename, api_key_data, status_ok


def search_videos(client, query_dict, next_token) :
    """
    Query to search for videos using a string query and a dict of parameters
    """
    try:
        if next_token is None:
            search_response = client.search().list(
                    q=query_dict['q'],
                    part=query_dict['part'],
                    publishedBefore = query_dict["publishedBefore"],
                    publishedAfter = query_dict["publishedAfter"], 
                    regionCode = query_dict["regionCode"],
                    relevanceLanguage = query_dict["relevanceLanguage"],
                    videoDuration = query_dict["videoDuration"],
                    videoPaidProductPlacement = query_dict["videoPaidProductPlacement"],
                    order = query_dict["order"],
                    maxResults = query_dict["maxResults"]
                ).execute()
            time.sleep(0.1)
            results = search_response.get("items")
            next_token = search_response.get("nextPageToken")
            total_results = search_response.get("pageInfo").get("totalResults")

        else:
            search_response = client.search().list(
                    q=query_dict['q'],
                    part=query_dict['part'],
                    publishedBefore = query_dict["publishedBefore"],
                    publishedAfter = query_dict["publishedAfter"], 
                    regionCode = query_dict["regionCode"],
                    relevanceLanguage = query_dict["relevanceLanguage"],
                    videoDuration = query_dict["videoDuration"],
                    videoPaidProductPlacement = query_dict["videoPaidProductPlacement"],
                    order = query_dict["order"],
                    maxResults = query_dict["maxResults"],
                    pageToken=next_token
                ).execute()
            time.sleep(0.1)
            results = search_response.get("items")
            next_token = search_response.get("nextPageToken")
            total_results = search_response.get("pageInfo").get("totalResults")
    except Exception as e:
        pass
        print(e)
        results = []
        next_token = None
        total_results = 0
    return results, next_token, total_results

def process_search_videos(client, query_dict, limit, query_id, json_path, next_token = None):
    """
    process to iterate over pages of video search results and store JSON response in case of quota limit
    """
    counter=0
    results =[]
    total_results = 0 
    try:
        concatenated_string = query_dict['publishedAfter'] + "_" + query_dict['publishedBefore']
        timerange_id = "".join(c if c.isalnum() or c in ['-', '_'] else '_' for c in concatenated_string)
        filename = str(query_id)+'_'+str(timerange_id)+'_'+str(counter)
        filepath = os.path.join(json_path, filename +'.jsonl' )
        if not os.path.exists(filepath): 
            results, next_token, total_results = search_videos(client, query_dict, next_token)
            write_jsonl(results, json_path, str(query_id)+'_'+str(timerange_id)+'_'+str(counter))
            counter+=1
            while next_token is not None:
                if limit != 0:
                    if counter >= limit:
                        break
                filename = str(query_id)+'_'+str(timerange_id)+'_'+str(counter)
                filepath = os.path.join(json_path, filename +'.jsonl' )
                if not os.path.exists(filepath): 
                    new_results, next_token, _ = search_videos(client, query_dict, next_token)
                    results += new_results
                    write_jsonl(new_results, json_path,  str(query_id)+'_'+str(timerange_id)+'_'+str(counter))
                    counter+=1
                else:
                    print("file exists : ", filepath)
        else:
            print("file exists : ", filepath)
            
    except Exception as e:
        pass
        print(e)
    return results, total_results, next_token, counter

def get_video_details(client, lst):
    """
    Query to get video details
    """
    
    try:
        request = client.videos().list(
            part="id,snippet,contentDetails,statistics,status",
            id=",".join(lst),
            maxResults = 50
        )
        response = request.execute()
        results = response.get("items", [])
        time.sleep(0.1)
    except Exception as e:
        pass
        print(e)
        results=[]
    return results
    
#########################################################################################
# Parsing functions
#########################################################################################

def parse_video_details(lst_items):
    all_records =[]
    for item in lst_items:
        video_id = item.get("id", None)
        snippet = item.get("snippet", {})
        publishedAt = snippet.get("publishedAt", '1970-01-01T00:00:00Z')
        channelId = snippet.get("channelId", "")
        title = snippet.get("title", "")
        title = remove_extra_spaces(title)
        description = snippet.get("description", "")
        description = remove_extra_spaces(description)
        thumbnails = snippet.get("thumbnails", {})
        largest_thumbnail = max(thumbnails, key=lambda x: (thumbnails[x].get('width', 0) or 1) * (thumbnails[x].get('height', 0) or 1))
        largest_thumbnail_url = thumbnails[largest_thumbnail].get("url", "")
        largest_thumbnail_width = thumbnails[largest_thumbnail].get("width", 0)
        largest_thumbnail_height = thumbnails[largest_thumbnail].get("height", 0)
        channelTitle = snippet.get("channelTitle", "")
        tags = snippet.get("tags", [])
        categoryId = snippet.get("categoryId", None)
        liveBroadcastContent = snippet.get("liveBroadcastContent", None)
        defaultLanguage = snippet.get("defaultLanguage", None)
        defaultAudioLanguage = snippet.get("defaultAudioLanguage", None)
        contentDetails = item.get("contentDetails", {})
        duration = contentDetails.get("duration", "")
        if duration is not None:
            duration_ms = YT_duration_to_milliseconds(duration)
        else : 
            duration_ms = 0
        dimension = contentDetails.get("dimension", None)
        definition = contentDetails.get("definition", None)
        caption = contentDetails.get("caption", None)
        licensedContent = contentDetails.get("licensedContent", None)
        contentRating = contentDetails.get("contentRating", {})
        projection = contentDetails.get("projection", {})
        status = item.get("status",{})
        uploadStatus = status.get("uploadStatus", None)
        privacyStatus = status.get("privacyStatus", None)
        license = status.get("license", None)
        embeddable = status.get("embeddable", False)
        madeForKids = status.get("madeForKids", False)
        statistics = item.get("statistics", {})
        viewCount = statistics.get("viewCount", 0)
        likeCount = statistics.get("likeCount", 0)
        favoriteCount = statistics.get("favoriteCount", 0)
        commentCount = statistics.get("commentCount", 0)
        
        record = (video_id, publishedAt, channelId, channelTitle, title, description, viewCount, likeCount, favoriteCount, commentCount, 
                  largest_thumbnail_url, largest_thumbnail_width, largest_thumbnail_height, tags, categoryId, liveBroadcastContent, defaultLanguage, 
                  defaultAudioLanguage, duration_ms, dimension, definition, caption, licensedContent, contentRating, projection, uploadStatus, privacyStatus, license, embeddable, madeForKids)
        all_records.append(record)
    df = pd.DataFrame.from_records(all_records, columns = ["video_id", "publishedAt", "channelId", "channelTitle", "title", "description", "viewCount", "likeCount", "favoriteCount", "commentCount", 
                  "largest_thumbnail_url", "largest_thumbnail_width", "largest_thumbnail_height", "tags", "categoryId", "liveBroadcastContent", "defaultLanguage", 
                  "defaultAudioLanguage", "duration_ms", "dimension", "definition", "caption", "licensedContent", "contentRating", "projection", "uploadStatus", "privacyStatus", 
                  "license", "embeddable", "madeForKids"])
    return df

def parse_search_results(jsonl_data):
    all_records =[]
    for json in jsonl_data:
        video_id = json.get("id", {}).get("videoId", "")
        snippet = json.get("snippet", {})
        publishedAt = snippet.get("publishedAt", '1970-01-01T00:00:00Z')
        channelId = snippet.get("channelId", "")
        title = snippet.get("title", "")
        title = remove_extra_spaces(title)
        description = snippet.get("description", "")
        description = remove_extra_spaces(description)
        channelTitle = snippet.get("channelTitle", "")
        liveBroadcastContent = snippet.get("liveBroadcastContent", "")
        publishTime = snippet.get("publishTime", '1970-01-01T00:00:00Z')
        thumbnails = snippet.get("thumbnails", {})
        largest_thumbnail = max(thumbnails, key=lambda x: (thumbnails[x].get('width', 0) or 1) * (thumbnails[x].get('height', 0) or 1))
        largest_thumbnail_url = thumbnails[largest_thumbnail].get("url", "")
        largest_thumbnail_width = thumbnails[largest_thumbnail].get("width", 0)
        largest_thumbnail_height = thumbnails[largest_thumbnail].get("height", 0)

        current_record=(video_id, publishedAt, channelId, title, description, channelTitle, liveBroadcastContent, publishTime, largest_thumbnail_url, largest_thumbnail_width, largest_thumbnail_height)
        all_records.append(current_record)
    df = pd.DataFrame.from_records(all_records, columns = ["video_id", "publishedAt", "channelId", "title", "description", "channelTitle", "liveBroadcastContent", "publishTime", "largest_thumbnail_url", "largest_thumbnail_width", "largest_thumbnail_height"])
    return df

