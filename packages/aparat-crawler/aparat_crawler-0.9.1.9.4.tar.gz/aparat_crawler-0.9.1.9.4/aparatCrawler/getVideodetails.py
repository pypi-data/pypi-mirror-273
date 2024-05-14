import requests
from datetime import datetime
timeout_seconds=10
from datetime import datetime



def getVideoDetail(videouid,proxy=None):
    url = "https://www.aparat.com/api/fa/v1/video/video/show/videohash/"+videouid
    response=None
    global video

    response=requests.get(url=url,proxies=proxy)

    if response.status_code != 200 and response.status_code != 451:
        print(f"proxy is : {proxy}")
        print(f"url is :{url}")
        raise Exception(f"Aparat api error {response.status_code}")
    if response.status_code == 451:
        print(f"Aparat api error {response.status_code}")

    data = response.json()



    video=None
    if isinstance(data["data"], list):
        included=data["data"][0]
        video={
            "platform": "aparat",
            "_":"video",
            "id":included["id"] if "id" in included else None,
            "owner_username":included["attributes"]["owner_username"] if "owner_username" in included["attributes"] else None,
            "owner_id":int(included["relationships"]["Channel"]["data"]["id"]) ,
            "title":included["attributes"]["title"] if "title" in included["attributes"] else None,
            "tags":included["attributes"]["tags"] if "tags" in included["attributes"] else None,
            "uid":included["attributes"]["uid"] if "uid" in included["attributes"] else None,

            "visit_count":int(included["attributes"]["visit_cnt_int"]),
            
            "owner_name":data["included"][0]["attributes"]["name"] ,
            
            "poster":included["attributes"]["big_poster"] if "big_poster" in included["attributes"] else None,
            "owner_avatar":data["included"][0]["attributes"]["avatar"],
            "duration":int(included["attributes"]["duration"]) if "duration" in included["attributes"] else 0,
            "posted_date":included["attributes"]["sdate_real"] if "sdate_real" in included["attributes"] else included["attributes"]["sdate_rss"],

            "posted_timestamp":int(datetime.strptime(included["attributes"]["sdate_rss"], "%Y-%m-%d %H:%M:%S").timestamp())-12600 ,#2015-05-17 12:12:51 ##-12600 to convert iran timezone to utc
            
            "sdate_rss":included["attributes"]["sdate_rss"] ,
            "sdate_rss_tp":int(datetime.strptime(included["attributes"]["sdate_rss"], "%Y-%m-%d %H:%M:%S").timestamp())-12600 ,#2015-05-17 12:12:51 ##-12600 to convert iran timezone to utc
            "comments":None,
            "frame":included["attributes"]["frame"] if "frame" in included["attributes"] else None,
            "like_count":int(included["attributes"]["like_cnt"]) if included["attributes"]["like_cnt"]!=None else None,
            "description":included["attributes"]["description"] if "description" in included["attributes"]  else None,
            "is_deleted": False,

        }




    else:
        included=data["data"]
        video={
            "platform": "aparat",
            "_":"video",
            "id":included["id"] if "id" in included else None,
            "owner_username":included["attributes"]["owner_username"] if "owner_username" in included["attributes"] else None,
            "owner_id":int(included["relationships"]["Channel"]["data"]["id"]) ,
            "title":included["attributes"]["title"] if "title" in included["attributes"] else None,
            "tags":included["attributes"]["tags"] if "tags" in included["attributes"] else None,
            "uid":included["attributes"]["uid"] if "uid" in included["attributes"] else None,
            "visit_count":int(included["attributes"]["visit_cnt_non_formatted"]),
            
            "owner_name":data["included"][0]["attributes"]["name"] ,
            
            "poster":included["attributes"]["big_poster"] if "big_poster" in included["attributes"] else None,
            "owner_avatar":data["included"][0]["attributes"]["avatar"],
            "duration":int(included["attributes"]["duration"]) if "duration" in included["attributes"] else 0,
            "posted_date":included["attributes"]["sdate_real"] ,
            "posted_timestamp":int(datetime.strptime(included["attributes"]["sdate_real"], "%Y-%m-%d %H:%M:%S").timestamp())-12600 ,#2015-05-17 12:12:51 ##-12600 to convert iran timezone to utc
            
            "sdate_rss":included["attributes"]["sdate_real"] ,
            "sdate_rss_tp":int(datetime.strptime(included["attributes"]["sdate_real"], "%Y-%m-%d %H:%M:%S").timestamp())-12600 ,#2015-05-17 12:12:51 ##-12600 to convert iran timezone to utc
            "comments":None,
            "frame":included["attributes"]["frame"] if "frame" in included["attributes"] else None,
            "like_count":int(included["attributes"]["like_cnt_non_formatted"]) if "like_cnt_non_formatted" in included["attributes"] and included["attributes"]["like_cnt_non_formatted"] != None else 0,
            "description":included["attributes"]["description"] if "description" in included["attributes"]  else None,
            "is_deleted": False,

        }

    
    
    

    

    return video



