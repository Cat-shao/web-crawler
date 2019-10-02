# -*- coding: utf-8 -*-
"""
Created on Tue Sep 24 09:19:21 2019

@author: 邵振轩
"""

import requests
from bs4 import BeautifulSoup
import pprint
import time
import os
import re


header={"user-agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"}


class NetworkError(RuntimeError):
    def __init__(self,error_code):
        self.error_code=error_code


def split(url,to_list=False,to_dict=False,to_str=False):
    if to_list:
        data=[]
        for i in url.split("?")[1].split("&"):
            data.append(i.split("="))
        return data
    elif to_dict:
        data={}
        for i in url.split("?")[1].split("&"):
            data[i.split("=")[0]]=i.split("=")[1]
        return data
    elif to_str:
        data=""
        for i in url.split("?")[1].split("&"):
            data+=i.split("=")[0] + " = " + i.split("=")[1] +"\n"
        return data
    else:
        return url.split("?")[0]


get_song_url="https://wwwapi.kugou.com/yy/index.php"
class song:
    def __init__(self,Hash,AlbumID):
        get_song_data={'r': 'play/getdata', 'hash': Hash, 'album_id': AlbumID, 'platid': '4', '_': str(int(time.time())), "dfid": "3LfNPU1d3gyV0JwCNc4KepO3", "mid": "1b841ca1d9fd98d740d09d85625dbcb8"}
        self.response=requests.get(get_song_url,params=get_song_data,headers=header)
        self.data=self.response.json()
        if self.data["err_code"]!=0:
            raise NetworkError(self.data["err_code"])
    
    def download(self,file_dir="",file_name=""):
        if file_name=="":
            file=os.path.join(file_dir,"%s.%s"%(self.data["data"]["audio_name"],self.data["data"]["play_url"].split(".")[-1]))
        else:
            file=os.path.join(file_dir,file_name)
        
        f=open(file,"wb")
        f.write(requests.get(self.data["data"]["play_url"],headers=header).content)
        f.close()
    
    def download_img(self,file_dir="",file_name=""):
        if file_name=="":
            file=os.path.join(file_dir,"%s.%s"%(self.data["data"]["audio_name"],self.data["data"]["img"].split(".")[-1]))
        else:
            file=os.path.join(file_dir,file_name)
        
        f=open(file,"wb")
        f.write(requests.get(self.data["data"]["img"],headers=header).content)
        f.close()


search_url="https://songsearch.kugou.com/song_search_v2"
class search:
    def __init__(self,word):
        search_data={'keyword': word, 'page': '1', 'pagesize': '30', 'userid': '-1', 'clientver': '', 'platform': 'WebFilter', 'tag': 'em', 'filter': '2', 'iscorrection': '1', 'privilege_filter': '0', '_': int(time.time())}
        self.response=requests.get(search_url,params=search_data,headers=header)
        self.data=self.response.json()
        if self.data["error_code"]!=0:
            raise NetworkError(self.data["error_code"])
    
    def select(self,num):
        return song(self.data["data"]["lists"][num]["FileHash"],self.data["data"]["lists"][num]["AlbumID"])


album_url="https://www.kugou.com/album/"
class album:
    def __init__(self,album_id):
        self.response=requests.get(album_url+str(album_id)+".html")
        self.songs=[]
        self.data_list=re.findall('[A-Z0-9]+\|[0-9]+',self.response.text)
        for i in self.data_list:
            self.songs.append(song(i.split("|")[0],i.split("|")[1]))
        self.soup = BeautifulSoup(self.response.text,"lxml")
        self.soup.find()
        self.intro=re.findall(r'<div class="intro"><p><span>简介：</span>.+</p></div>',self.response.text)
        """<p><span>简介：</span>CD (1990/12/12)
ディスク枚数: 1
レーベル: ソニーレコード
収録時間: 44 分
ASIN: B00005G3EV
EAN： 4988009159621</p>"
singer_url="""
class singer:
    def __init__(self,album_id):
        pass
if __name__=="__main__":
    """"
    s=search("夕焼けの歌")
    s.select(0).download()
    """
    a=album(1852745)

