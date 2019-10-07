# -*- coding: utf-8 -*-
"""
Created on Tue Sep 24 09:19:21 2019

@author: 邵振轩
"""

import requests
import html
import pprint
import time
import os
import re



header={"user-agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"}



#新建网络错误
class NetworkError(RuntimeError):
    def __init__(self,error_code):
        self.error_code=error_code



#解析url传递的参数
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



#获取歌曲信息的网址
get_song_url="https://wwwapi.kugou.com/yy/index.php"
#歌曲类
class song:
    def __init__(self,Hash,AlbumID):#Hash:一串跟ID相关的字符串 AlbumID:专辑ID
        #url传递的参数
        get_song_data={'r': 'play/getdata', 
                       'hash': Hash, 
                       'album_id': AlbumID, 
                       'platid': '4', 
                       '_': str(int(time.time())), 
                       "dfid": "3LfNPU1d3gyV0JwCNc4KepO3", 
                       "mid": "1b841ca1d9fd98d740d09d85625dbcb8"}
        
        #发送get请求，返回json文件
        self.response=requests.get(get_song_url,params=get_song_data,headers=header)
        self.data=self.response.json()
        
        """
        返回的json文件（例子）
        {'data': {'album_id': '1602728',
                  'album_name': 'Taylor Gang Timeline (Mixtape)',
                  'audio_id': '11299767',
                  'audio_name': 'Wiz Khalifa、Charlie Puth - See You Again',
                  'author_id': '83823',
                  'author_name': 'Wiz Khalifa、Charlie Puth',
                  'authors': [{'author_id': '83823',
                               'author_name': 'Wiz Khalifa',
                               'avatar': 'http://singerimg.kugou.com/uploadpic/softhead/400/20161109/20161109160316706340.jpg',
                               'is_publish': '1',
                               'sizable_avatar': 'http://singerimg.kugou.com/uploadpic/softhead/{size}/20161109/20161109160316706340.jpg'},
                              {'author_id': '87865',
                               'author_name': 'Charlie Puth',
                               'avatar': 'http://singerimg.kugou.com/uploadpic/softhead/400/20190916/20190916160549234.jpg',
                               'is_publish': '1',
                               'sizable_avatar': 'http://singerimg.kugou.com/uploadpic/softhead/{size}/20190916/20190916160549234.jpg'}],
                  'bitrate': 127,
                  'filesize': 3675849,
                  'hash': '7775FBCCF9E20887AB01CBB41E87162D',
                  'have_album': 1,
                  'have_mv': 1,
                  'img': 'http://imge.kugou.com/stdmusic/20160909/20160909042711813162.jpg',
                  'lyrics': '\ufeff[id:$00000000]\r\n'
                            '[ar:Wiz Khalifa]\r\n'
                            '[ti:See You Again]\r\n'
                            '[by:]\r\n'
                            '[hash:7775fbccf9e20887ab01cbb41e87162d]\r\n'
                            '[al:]\r\n'
                            '[sign:]\r\n'
                            '[qq:]\r\n'
                            '[total:0]\r\n'
                            '[offset:-74]\r\n'
                            '[00:00.04]Wiz Khalifa、Charlie Puth - See You Again\r\n'
                            '[00:00.20]Written by：Justin Franks/Charlie Puth/Cameron '
                            'Thomaz/Sage The Gemini\r\n'
                            "[00:10.74]Charlie Puth：It's been a long day without you "
                            'my friend\r\n'
                            "[00:17.70]And I'll tell you all about it when I see you "
                            'again\r\n'
                            "[00:23.50]We've come a long way from where we began\r\n"
                            "[00:29.38]Oh I'll tell you all about it when I see you "
                            'again\r\n'
                            '[00:35.40]When I see you again\r\n'
                            '[00:40.22]Wiz Khalifa：Damn who knew all the planes we '
                            'flew\r\n'
                            "[00:43.20]Good things we've been through\r\n"
                            "[00:44.91]That I'll be standing right here\r\n"
                            '[00:46.63]Talking to you about another path\r\n'
                            '[00:49.05]I know we loved to hit the road and laugh\r\n'
                            "[00:51.32]But something told me that it wouldn't last\r\n"
                            '[00:53.69]Had to switch up look at things different see '
                            'the bigger picture\r\n'
                            '[00:57.40]Those were the days hard work forever pays\r\n'
                            '[01:00.59]Now I see you when a better place\r\n'
                            '[01:05.32]Wiz Khalifa：How could we not talk about family '
                            "when family's all that we got\r\n"
                            '[01:08.96]Everything I went through you were standing '
                            'there by my side\r\n'
                            '[01:11.86]And now you gonna be with me for the last '
                            'ride\r\n'
                            "[01:14.06]Charlie Puth：It's been a long day without you "
                            'my friend\r\n'
                            "[01:20.63]And I'll tell you all about it when I see you "
                            'again\r\n'
                            "[01:26.50]We've come a long way from where we began\r\n"
                            "[01:32.45]Oh I'll tell you all about it when I see you "
                            'again\r\n'
                            '[01:38.47]When I see you again\r\n'
                            '[01:56.53]Wiz Khalifa：First you both go out your way\r\n'
                            "[01:58.05]And the vibe is feeling strong and what's\r\n"
                            '[01:59.96]Small turn to a friendship a friendship\r\n'
                            '[02:01.84]Turn into a bond and that bond will never\r\n'
                            '[02:03.69]Be broke and the love will never get lost\r\n'
                            '[02:08.53]And when brotherhood come first then the '
                            'line\r\n'
                            '[02:10.61]Will never be crossed established it on our '
                            'own\r\n'
                            '[02:13.03]When that line had to be drawn and that line is '
                            'what\r\n'
                            "[02:15.63]We reach so remember me when I'm gone\r\n"
                            '[02:20.26]Wiz Khalifa：How could we not talk about family '
                            "when family's all that we got\r\n"
                            '[02:23.90]Everything I went through you were standing '
                            'there by my side\r\n'
                            '[02:26.85]And now you gonna be with me for the last '
                            'ride\r\n'
                            '[02:29.38]Charlie Puth：Let the light guide your way hold '
                            'every memory\r\n'
                            '[02:38.34]As you go and every road you take will always '
                            'lead you home\r\n'
                            '[02:49.49]Hoo\r\n'
                            "[02:52.95]Charlie Puth：It's been a long day without you "
                            'my friend\r\n'
                            "[02:59.62]And I'll tell you all about it when I see you "
                            'again\r\n'
                            "[03:05.52]We've come a long way from where we began\r\n"
                            "[03:11.43]Oh I'll tell you all about it when I see you "
                            'again\r\n'
                            '[03:17.28]When I see you again\r\n'
                            '[03:22.96]Again\r\n'
                            '[03:29.35]When I see you again see you again\r\n'
                            '[03:41.32]When I see you again\r\n',
                  'play_url': 'https://webfs.yun.kugou.com/201910071633/44d8f198885bb63a3dcd7760c0ac49cf/G013/M03/10/19/rYYBAFUHoGSAfjDTADgWycPN4R0327.mp3',
                  'privilege': 8,
                  'privilege2': '1000',
                  'song_name': 'See You Again',
                  'timelength': 229000,
                  'video_id': '174105'},
         'err_code': 0,
         'status': 1}
        """
        
        #检查错误码
        if self.data["err_code"]!=0:
            raise NetworkError(self.data["err_code"])
        
        #歌曲名称
        self.name=self.data["data"]["audio_name"]
    
    def download(self,file_dir="",file_name=""):#下载歌曲函数
        #自动填写文件路径
        if file_name=="":
            file=os.path.join(file_dir,"%s.%s"%(self.data["data"]["audio_name"],self.data["data"]["play_url"].split(".")[-1]))
        else:
            file=os.path.join(file_dir,file_name)
        
        #检查歌曲是否无下载路径（歌曲有可能是付费歌曲）
        if self.data["data"]["play_url"]!="":
            f=open(file,"wb")
            f.write(requests.get(self.data["data"]["play_url"],headers=header).content)
            f.close()
        else:
            raise NetworkError("Error:The play_url is empty.")
    
    def download_img(self,file_dir="",file_name=""):#下载歌曲图片
        #自动填写路径
        if file_name=="":
            file=os.path.join(file_dir,"%s.%s"%(self.data["data"]["audio_name"],self.data["data"]["img"].split(".")[-1]))
        else:
            file=os.path.join(file_dir,file_name)
        
        #检查歌曲图片是否无下载路径（歌曲演唱者未提交照片）
        if self.data["data"]["img"]!="":
            f=open(file,"wb")
            f.write(requests.get(self.data["data"]["img"],headers=header).content)
            f.close()
        else:
            raise NetworkError("Error:The img_url is empty.")



#获取搜索信息的网址
search_url="https://songsearch.kugou.com/song_search_v2"
#搜索类
class search:
    def __init__(self,word):#word:搜素的关键字、词
        #url传递的参数
        search_data={'keyword': word, 
                     'page': '1', 
                     'pagesize': '30', 
                     'userid': '-1', 
                     'clientver': '', 
                     'platform': 'WebFilter', 
                     'tag': 'em', 
                     'filter': '2', 
                     'iscorrection': '1', 
                     'privilege_filter': '0', 
                     '_': int(time.time())}
        
        #发送get请求，返回json文件
        self.response=requests.get(search_url,params=search_data,headers=header)
        self.data=self.response.json()
        
        """
        返回的json文件（例子）
        {'data': {'aggregation': [{'count': 0, 'key': 'DJ'},
                                  {'count': 0, 'key': '现场'},
                                  {'count': 0, 'key': '广场舞'},
                                  {'count': 0, 'key': '伴奏'},
                                  {'count': 0, 'key': '铃声'}],
                  'allowerr': 0,
                  'chinesecount': 0,
                  'correctionforce': 0,
                  'correctionsubject': '',
                  'correctiontip': '',
                  'correctiontype': 0,
                  'istag': 0,
                  'istagresult': 0,
                  'lists': [{'A320Privilege': 10,
                             'ASQPrivilege': 10,
                             'Accompany': 1,
                             'AlbumID': '1602728',
                             'AlbumName': 'Taylor Gang Timeline (Mixtape)',
                             'AlbumPrivilege': 8,
                             'AudioCdn': 100,
                             'Audioid': 11299767,
                             'Auxiliary': '',
                             'Bitrate': 128,
                             'Duration': 229,
                             'ExtName': 'mp3',
                             'FailProcess': 4,
                             'FileHash': '7775FBCCF9E20887AB01CBB41E87162D',
                             'FileName': 'Wiz Khalifa、Charlie Puth - <em>See You '
                                         'Again</em>',
                             'FileSize': 3675849,
                             'FoldType': 0,
                             'Grp': [{'A320Privilege': 10,
                                      'ASQPrivilege': 10,
                                      'Accompany': 1,
                                      'AlbumID': '2566745',
                                      'AlbumName': 'Furious 7 (Original Motion Picture '
                                                   'Soundtrack) (速度与激情7 电影原声带)',
                                      'AlbumPrivilege': 8,
                                      'AudioCdn': 100,
                                      'Audioid': 11299767,
                                      'Auxiliary': '',
                                      'Bitrate': 128,
                                      'Duration': 229,
                                      'ExtName': 'mp3',
                                      'FailProcess': 4,
                                      'FileHash': '7775FBCCF9E20887AB01CBB41E87162D',
                                      'FileName': 'Wiz Khalifa、Charlie Puth - <em>See '
                                                  'You Again</em>',
                                      'FileSize': 3675849,
                                      'HQBitrate': 320,
                                      'HQDuration': 229,
                                      'HQExtName': 'mp3',
                                      'HQFailProcess': 4,
                                      'HQFileHash': '20D3EAA8E4CE277BC4A30F3D53971AE1',
                                      'HQFileSize': 9185805,
                                      'HQPayType': 3,
                                      'HQPkgPrice': 1,
                                      'HQPrice': 200,
                                      'HQPrivilege': 10,
                                      'HasAlbum': 1,
                                      'HiFiQuality': 2,
                                      'ID': '63999842',
                                      'IsOriginal': 0,
                                      'M4aSize': 941044,
                                      'MixSongID': '63999842',
                                      'MvHash': '74FA5AA22270012890C200D515F724AE',
                                      'MvTrac': 3,
                                      'MvType': 2,
                                      'OldCpy': 1,
                                      'OriOtherName': '',
                                      'OriSongName': '<em>See You Again</em>',
                                      'OtherName': '',
                                      'OwnerCount': 26,
                                      'PayType': 3,
                                      'PkgPrice': 1,
                                      'Price': 200,
                                      'Privilege': 8,
                                      'Publish': 1,
                                      'PublishAge': 255,
                                      'QualityLevel': 3,
                                      'ResBitrate': 0,
                                      'ResDuration': 0,
                                      'ResFileHash': '',
                                      'ResFileSize': 0,
                                      'SQBitrate': 801,
                                      'SQDuration': 230,
                                      'SQExtName': 'flac',
                                      'SQFailProcess': 4,
                                      'SQFileHash': 'DC0AEB619143C7A91066E08C49258CB7',
                                      'SQFileSize': 22986169,
                                      'SQPayType': 3,
                                      'SQPkgPrice': 1,
                                      'SQPrice': 200,
                                      'SQPrivilege': 10,
                                      'Scid': 11299767,
                                      'SingerId': [83823, 87865],
                                      'SingerName': 'Wiz Khalifa、Charlie Puth',
                                      'SongLabel': '',
                                      'SongName': '<em>See You Again</em>',
                                      'Source': '',
                                      'SourceID': 0,
                                      'SuperBitrate': 0,
                                      'SuperDuration': 0,
                                      'SuperExtName': '',
                                      'SuperFileHash': '',
                                      'SuperFileSize': 0,
                                      'TopicRemark': '',
                                      'TopicUrl': '',
                                      'Type': 'audio',
                                      'mvTotal': 0,
                                      'trans_param': {'cid': 5916761,
                                                      'display': 0,
                                                      'display_rate': 0,
                                                      'musicpack_advance': 0,
                                                      'pay_block_tpl': 1}},
                                     {'A320Privilege': 10,
                                      'ASQPrivilege': 10,
                                      'Accompany': 1,
                                      'AlbumID': '1990739',
                                      'AlbumName': "Now That's What I Call Music! 91",
                                      'AlbumPrivilege': 8,
                                      'AudioCdn': 100,
                                      'Audioid': 11299767,
                                      'Auxiliary': '',
                                      'Bitrate': 128,
                                      'Duration': 229,
                                      'ExtName': 'mp3',
                                      'FailProcess': 4,
                                      'FileHash': '7775FBCCF9E20887AB01CBB41E87162D',
                                      'FileName': 'Wiz Khalifa、Charlie Puth - <em>See '
                                                  'You Again</em>',
                                      'FileSize': 3675849,
                                      'HQBitrate': 320,
                                      'HQDuration': 229,
                                      'HQExtName': 'mp3',
                                      'HQFailProcess': 4,
                                      'HQFileHash': '20D3EAA8E4CE277BC4A30F3D53971AE1',
                                      'HQFileSize': 9185805,
                                      'HQPayType': 3,
                                      'HQPkgPrice': 1,
                                      'HQPrice': 200,
                                      'HQPrivilege': 10,
                                      'HasAlbum': 1,
                                      'HiFiQuality': 2,
                                      'ID': '54900330',
                                      'IsOriginal': 0,
                                      'M4aSize': 941044,
                                      'MixSongID': '54900330',
                                      'MvHash': '74FA5AA22270012890C200D515F724AE',
                                      'MvTrac': 3,
                                      'MvType': 2,
                                      'OldCpy': 1,
                                      'OriOtherName': '',
                                      'OriSongName': '<em>See You Again</em>',
                                      'OtherName': '',
                                      'OwnerCount': 6,
                                      'PayType': 3,
                                      'PkgPrice': 1,
                                      'Price': 200,
                                      'Privilege': 8,
                                      'Publish': 1,
                                      'PublishAge': 255,
                                      'QualityLevel': 3,
                                      'ResBitrate': 0,
                                      'ResDuration': 0,
                                      'ResFileHash': '',
                                      'ResFileSize': 0,
                                      'SQBitrate': 801,
                                      'SQDuration': 230,
                                      'SQExtName': 'flac',
                                      'SQFailProcess': 4,
                                      'SQFileHash': 'DC0AEB619143C7A91066E08C49258CB7',
                                      'SQFileSize': 22986169,
                                      'SQPayType': 3,
                                      'SQPkgPrice': 1,
                                      'SQPrice': 200,
                                      'SQPrivilege': 10,
                                      'Scid': 11299767,
                                      'SingerId': [83823, 87865],
                                      'SingerName': 'Wiz Khalifa、Charlie Puth',
                                      'SongLabel': '',
                                      'SongName': '<em>See You Again</em>',
                                      'Source': '',
                                      'SourceID': 0,
                                      'SuperBitrate': 0,
                                      'SuperDuration': 0,
                                      'SuperExtName': '',
                                      'SuperFileHash': '',
                                      'SuperFileSize': 0,
                                      'TopicRemark': '',
                                      'TopicUrl': '',
                                      'Type': 'audio',
                                      'mvTotal': 0,
                                      'trans_param': {'cid': 31178160,
                                                      'display': 0,
                                                      'display_rate': 0,
                                                      'musicpack_advance': 0,
                                                      'pay_block_tpl': 1}},
                                     {'A320Privilege': 10,
                                      'ASQPrivilege': 10,
                                      'Accompany': 1,
                                      'AlbumID': '8334930',
                                      'AlbumName': "NOW That's What I Call Music, Vol. "
                                                   '56',
                                      'AlbumPrivilege': 8,
                                      'AudioCdn': 100,
                                      'Audioid': 11299767,
                                      'Auxiliary': '',
                                      'Bitrate': 128,
                                      'Duration': 229,
                                      'ExtName': 'mp3',
                                      'FailProcess': 4,
                                      'FileHash': '7775FBCCF9E20887AB01CBB41E87162D',
                                      'FileName': 'Wiz Khalifa、Charlie Puth - <em>See '
                                                  'You Again</em>',
                                      'FileSize': 3675849,
                                      'HQBitrate': 320,
                                      'HQDuration': 229,
                                      'HQExtName': 'mp3',
                                      'HQFailProcess': 4,
                                      'HQFileHash': '20D3EAA8E4CE277BC4A30F3D53971AE1',
                                      'HQFileSize': 9185805,
                                      'HQPayType': 3,
                                      'HQPkgPrice': 1,
                                      'HQPrice': 200,
                                      'HQPrivilege': 10,
                                      'HasAlbum': 1,
                                      'HiFiQuality': 2,
                                      'ID': '106132814',
                                      'IsOriginal': 0,
                                      'M4aSize': 941044,
                                      'MixSongID': '106132814',
                                      'MvHash': '74FA5AA22270012890C200D515F724AE',
                                      'MvTrac': 3,
                                      'MvType': 2,
                                      'OldCpy': 1,
                                      'OriOtherName': '',
                                      'OriSongName': '<em>See You Again</em>',
                                      'OtherName': '',
                                      'OwnerCount': 3,
                                      'PayType': 3,
                                      'PkgPrice': 1,
                                      'Price': 200,
                                      'Privilege': 8,
                                      'Publish': 1,
                                      'PublishAge': 255,
                                      'QualityLevel': 3,
                                      'ResBitrate': 0,
                                      'ResDuration': 0,
                                      'ResFileHash': '',
                                      'ResFileSize': 0,
                                      'SQBitrate': 801,
                                      'SQDuration': 230,
                                      'SQExtName': 'flac',
                                      'SQFailProcess': 4,
                                      'SQFileHash': 'DC0AEB619143C7A91066E08C49258CB7',
                                      'SQFileSize': 22986169,
                                      'SQPayType': 3,
                                      'SQPkgPrice': 1,
                                      'SQPrice': 200,
                                      'SQPrivilege': 10,
                                      'Scid': 11299767,
                                      'SingerId': [83823, 87865],
                                      'SingerName': 'Wiz Khalifa、Charlie Puth',
                                      'SongLabel': '',
                                      'SongName': '<em>See You Again</em>',
                                      'Source': '',
                                      'SourceID': 0,
                                      'SuperBitrate': 0,
                                      'SuperDuration': 0,
                                      'SuperExtName': '',
                                      'SuperFileHash': '',
                                      'SuperFileSize': 0,
                                      'TopicRemark': '',
                                      'TopicUrl': '',
                                      'Type': 'audio',
                                      'mvTotal': 0,
                                      'trans_param': {'cid': 32144589,
                                                      'display': 0,
                                                      'display_rate': 0,
                                                      'musicpack_advance': 0,
                                                      'pay_block_tpl': 1}},
                                     {'A320Privilege': 10,
                                      'ASQPrivilege': 10,
                                      'Accompany': 1,
                                      'AlbumID': '1008786',
                                      'AlbumName': '2016 GRAMMY Nominees',
                                      'AlbumPrivilege': 8,
                                      'AudioCdn': 100,
                                      'Audioid': 11299767,
                                      'Auxiliary': '',
                                      'Bitrate': 128,
                                      'Duration': 229,
                                      'ExtName': 'mp3',
                                      'FailProcess': 4,
                                      'FileHash': '7775FBCCF9E20887AB01CBB41E87162D',
                                      'FileName': 'Wiz Khalifa、Charlie Puth - <em>See '
                                                  'You Again</em>',
                                      'FileSize': 3675849,
                                      'HQBitrate': 320,
                                      'HQDuration': 229,
                                      'HQExtName': 'mp3',
                                      'HQFailProcess': 4,
                                      'HQFileHash': '20D3EAA8E4CE277BC4A30F3D53971AE1',
                                      'HQFileSize': 9185805,
                                      'HQPayType': 3,
                                      'HQPkgPrice': 1,
                                      'HQPrice': 200,
                                      'HQPrivilege': 10,
                                      'HasAlbum': 1,
                                      'HiFiQuality': 2,
                                      'ID': '64498518',
                                      'IsOriginal': 0,
                                      'M4aSize': 941044,
                                      'MixSongID': '64498518',
                                      'MvHash': '74FA5AA22270012890C200D515F724AE',
                                      'MvTrac': 3,
                                      'MvType': 2,
                                      'OldCpy': 0,
                                      'OriOtherName': '',
                                      'OriSongName': '<em>See You Again</em>',
                                      'OtherName': '',
                                      'OwnerCount': 4,
                                      'PayType': 3,
                                      'PkgPrice': 1,
                                      'Price': 200,
                                      'Privilege': 8,
                                      'Publish': 1,
                                      'PublishAge': 255,
                                      'QualityLevel': 3,
                                      'ResBitrate': 0,
                                      'ResDuration': 0,
                                      'ResFileHash': '',
                                      'ResFileSize': 0,
                                      'SQBitrate': 801,
                                      'SQDuration': 230,
                                      'SQExtName': 'flac',
                                      'SQFailProcess': 4,
                                      'SQFileHash': 'DC0AEB619143C7A91066E08C49258CB7',
                                      'SQFileSize': 22986169,
                                      'SQPayType': 3,
                                      'SQPkgPrice': 1,
                                      'SQPrice': 200,
                                      'SQPrivilege': 10,
                                      'Scid': 11299767,
                                      'SingerId': [83823, 87865],
                                      'SingerName': 'Wiz Khalifa、Charlie Puth',
                                      'SongLabel': '',
                                      'SongName': '<em>See You Again</em>',
                                      'Source': '',
                                      'SourceID': 0,
                                      'SuperBitrate': 0,
                                      'SuperDuration': 0,
                                      'SuperExtName': '',
                                      'SuperFileHash': '',
                                      'SuperFileSize': 0,
                                      'TopicRemark': '',
                                      'TopicUrl': '',
                                      'Type': 'audio',
                                      'mvTotal': 0,
                                      'trans_param': {'cid': 7346792,
                                                      'display': 0,
                                                      'display_rate': 0,
                                                      'musicpack_advance': 0,
                                                      'pay_block_tpl': 1}},
                                     {'A320Privilege': 10,
                                      'ASQPrivilege': 10,
                                      'Accompany': 1,
                                      'AlbumID': '550853',
                                      'AlbumName': 'Nine Track Mind (Special Edition)',
                                      'AlbumPrivilege': 8,
                                      'AudioCdn': 100,
                                      'Audioid': 11299767,
                                      'Auxiliary': '',
                                      'Bitrate': 128,
                                      'Duration': 229,
                                      'ExtName': 'mp3',
                                      'FailProcess': 4,
                                      'FileHash': '7775FBCCF9E20887AB01CBB41E87162D',
                                      'FileName': 'Wiz Khalifa、Charlie Puth - <em>See '
                                                  'You Again</em>',
                                      'FileSize': 3675849,
                                      'HQBitrate': 320,
                                      'HQDuration': 229,
                                      'HQExtName': 'mp3',
                                      'HQFailProcess': 4,
                                      'HQFileHash': '20D3EAA8E4CE277BC4A30F3D53971AE1',
                                      'HQFileSize': 9185805,
                                      'HQPayType': 3,
                                      'HQPkgPrice': 1,
                                      'HQPrice': 200,
                                      'HQPrivilege': 10,
                                      'HasAlbum': 1,
                                      'HiFiQuality': 2,
                                      'ID': '64422181',
                                      'IsOriginal': 0,
                                      'M4aSize': 941044,
                                      'MixSongID': '64422181',
                                      'MvHash': '74FA5AA22270012890C200D515F724AE',
                                      'MvTrac': 3,
                                      'MvType': 2,
                                      'OldCpy': 1,
                                      'OriOtherName': '',
                                      'OriSongName': '<em>See You Again</em>',
                                      'OtherName': '',
                                      'OwnerCount': 3,
                                      'PayType': 3,
                                      'PkgPrice': 1,
                                      'Price': 200,
                                      'Privilege': 8,
                                      'Publish': 1,
                                      'PublishAge': 255,
                                      'QualityLevel': 3,
                                      'ResBitrate': 0,
                                      'ResDuration': 0,
                                      'ResFileHash': '',
                                      'ResFileSize': 0,
                                      'SQBitrate': 801,
                                      'SQDuration': 230,
                                      'SQExtName': 'flac',
                                      'SQFailProcess': 4,
                                      'SQFileHash': 'DC0AEB619143C7A91066E08C49258CB7',
                                      'SQFileSize': 22986169,
                                      'SQPayType': 3,
                                      'SQPkgPrice': 1,
                                      'SQPrice': 200,
                                      'SQPrivilege': 10,
                                      'Scid': 11299767,
                                      'SingerId': [83823, 87865],
                                      'SingerName': 'Wiz Khalifa、Charlie Puth',
                                      'SongLabel': '',
                                      'SongName': '<em>See You Again</em>',
                                      'Source': '',
                                      'SourceID': 0,
                                      'SuperBitrate': 0,
                                      'SuperDuration': 0,
                                      'SuperExtName': '',
                                      'SuperFileHash': '',
                                      'SuperFileSize': 0,
                                      'TopicRemark': '',
                                      'TopicUrl': '',
                                      'Type': 'audio',
                                      'mvTotal': 0,
                                      'trans_param': {'cid': 6814968,
                                                      'display': 0,
                                                      'display_rate': 0,
                                                      'musicpack_advance': 0,
                                                      'pay_block_tpl': 1}},
                                     {'A320Privilege': 10,
                                      'ASQPrivilege': 10,
                                      'Accompany': 1,
                                      'AlbumID': '2443390',
                                      'AlbumName': 'Nine Track Mind',
                                      'AlbumPrivilege': 8,
                                      'AudioCdn': 100,
                                      'Audioid': 11299767,
                                      'Auxiliary': '',
                                      'Bitrate': 128,
                                      'Duration': 229,
                                      'ExtName': 'mp3',
                                      'FailProcess': 4,
                                      'FileHash': '7775FBCCF9E20887AB01CBB41E87162D',
                                      'FileName': 'Wiz Khalifa、Charlie Puth - <em>See '
                                                  'You Again</em>',
                                      'FileSize': 3675849,
                                      'HQBitrate': 320,
                                      'HQDuration': 229,
                                      'HQExtName': 'mp3',
                                      'HQFailProcess': 4,
                                      'HQFileHash': '20D3EAA8E4CE277BC4A30F3D53971AE1',
                                      'HQFileSize': 9185805,
                                      'HQPayType': 3,
                                      'HQPkgPrice': 1,
                                      'HQPrice': 200,
                                      'HQPrivilege': 10,
                                      'HasAlbum': 1,
                                      'HiFiQuality': 2,
                                      'ID': '62599220',
                                      'IsOriginal': 0,
                                      'M4aSize': 941044,
                                      'MixSongID': '62599220',
                                      'MvHash': '74FA5AA22270012890C200D515F724AE',
                                      'MvTrac': 3,
                                      'MvType': 2,
                                      'OldCpy': 0,
                                      'OriOtherName': '',
                                      'OriSongName': '<em>See You Again</em>',
                                      'OtherName': '',
                                      'OwnerCount': 3,
                                      'PayType': 3,
                                      'PkgPrice': 1,
                                      'Price': 200,
                                      'Privilege': 8,
                                      'Publish': 1,
                                      'PublishAge': 255,
                                      'QualityLevel': 3,
                                      'ResBitrate': 0,
                                      'ResDuration': 0,
                                      'ResFileHash': '',
                                      'ResFileSize': 0,
                                      'SQBitrate': 801,
                                      'SQDuration': 230,
                                      'SQExtName': 'flac',
                                      'SQFailProcess': 4,
                                      'SQFileHash': 'DC0AEB619143C7A91066E08C49258CB7',
                                      'SQFileSize': 22986169,
                                      'SQPayType': 3,
                                      'SQPkgPrice': 1,
                                      'SQPrice': 200,
                                      'SQPrivilege': 10,
                                      'Scid': 11299767,
                                      'SingerId': [83823, 87865],
                                      'SingerName': 'Wiz Khalifa、Charlie Puth',
                                      'SongLabel': '',
                                      'SongName': '<em>See You Again</em>',
                                      'Source': '',
                                      'SourceID': 0,
                                      'SuperBitrate': 0,
                                      'SuperDuration': 0,
                                      'SuperExtName': '',
                                      'SuperFileHash': '',
                                      'SuperFileSize': 0,
                                      'TopicRemark': '',
                                      'TopicUrl': '',
                                      'Type': 'audio',
                                      'mvTotal': 0,
                                      'trans_param': {'cid': 5066362,
                                                      'display': 0,
                                                      'display_rate': 0,
                                                      'musicpack_advance': 0,
                                                      'pay_block_tpl': 1}},
                                     {'A320Privilege': 10,
                                      'ASQPrivilege': 10,
                                      'Accompany': 1,
                                      'AlbumID': '7536462',
                                      'AlbumName': 'Feel My Collect Song',
                                      'AlbumPrivilege': 8,
                                      'AudioCdn': 100,
                                      'Audioid': 11299767,
                                      'Auxiliary': '',
                                      'Bitrate': 128,
                                      'Duration': 229,
                                      'ExtName': 'mp3',
                                      'FailProcess': 4,
                                      'FileHash': '7775FBCCF9E20887AB01CBB41E87162D',
                                      'FileName': 'Wiz Khalifa、Charlie Puth - <em>See '
                                                  'You Again</em>',
                                      'FileSize': 3675849,
                                      'HQBitrate': 320,
                                      'HQDuration': 229,
                                      'HQExtName': 'mp3',
                                      'HQFailProcess': 4,
                                      'HQFileHash': '20D3EAA8E4CE277BC4A30F3D53971AE1',
                                      'HQFileSize': 9185805,
                                      'HQPayType': 3,
                                      'HQPkgPrice': 1,
                                      'HQPrice': 200,
                                      'HQPrivilege': 10,
                                      'HasAlbum': 1,
                                      'HiFiQuality': 2,
                                      'ID': '101801375',
                                      'IsOriginal': 0,
                                      'M4aSize': 941044,
                                      'MixSongID': '101801375',
                                      'MvHash': '74FA5AA22270012890C200D515F724AE',
                                      'MvTrac': 3,
                                      'MvType': 2,
                                      'OldCpy': 1,
                                      'OriOtherName': '',
                                      'OriSongName': '<em>See You Again</em>',
                                      'OtherName': '',
                                      'OwnerCount': 6,
                                      'PayType': 3,
                                      'PkgPrice': 1,
                                      'Price': 200,
                                      'Privilege': 8,
                                      'Publish': 1,
                                      'PublishAge': 255,
                                      'QualityLevel': 3,
                                      'ResBitrate': 0,
                                      'ResDuration': 0,
                                      'ResFileHash': '',
                                      'ResFileSize': 0,
                                      'SQBitrate': 801,
                                      'SQDuration': 230,
                                      'SQExtName': 'flac',
                                      'SQFailProcess': 4,
                                      'SQFileHash': 'DC0AEB619143C7A91066E08C49258CB7',
                                      'SQFileSize': 22986169,
                                      'SQPayType': 3,
                                      'SQPkgPrice': 1,
                                      'SQPrice': 200,
                                      'SQPrivilege': 10,
                                      'Scid': 11299767,
                                      'SingerId': [83823, 87865],
                                      'SingerName': 'Wiz Khalifa、Charlie Puth',
                                      'SongLabel': '',
                                      'SongName': '<em>See You Again</em>',
                                      'Source': '',
                                      'SourceID': 0,
                                      'SuperBitrate': 0,
                                      'SuperDuration': 0,
                                      'SuperExtName': '',
                                      'SuperFileHash': '',
                                      'SuperFileSize': 0,
                                      'TopicRemark': '',
                                      'TopicUrl': '',
                                      'Type': 'audio',
                                      'mvTotal': 0,
                                      'trans_param': {'cid': 29359576,
                                                      'display': 0,
                                                      'display_rate': 0,
                                                      'musicpack_advance': 0,
                                                      'pay_block_tpl': 1}}],
                             'HQBitrate': 320,
                             'HQDuration': 229,
                             'HQExtName': 'mp3',
                             'HQFailProcess': 4,
                             'HQFileHash': '20D3EAA8E4CE277BC4A30F3D53971AE1',
                             'HQFileSize': 9185805,
                             'HQPayType': 3,
                             'HQPkgPrice': 1,
                             'HQPrice': 200,
                             'HQPrivilege': 10,
                             'HasAlbum': 1,
                             'HiFiQuality': 2,
                             'ID': '38335643',
                             'IsOriginal': 1,
                             'M4aSize': 941044,
                             'MixSongID': '38335643',
                             'MvHash': '74FA5AA22270012890C200D515F724AE',
                             'MvTrac': 3,
                             'MvType': 2,
                             'OldCpy': 1,
                             'OriOtherName': '',
                             'OriSongName': '<em>See You Again</em>',
                             'OtherName': '',
                             'OwnerCount': 28564,
                             'PayType': 3,
                             'PkgPrice': 1,
                             'Price': 200,
                             'Privilege': 8,
                             'Publish': 1,
                             'PublishAge': 255,
                             'QualityLevel': 3,
                             'ResBitrate': 0,
                             'ResDuration': 0,
                             'ResFileHash': '',
                             'ResFileSize': 0,
                             'SQBitrate': 801,
                             'SQDuration': 230,
                             'SQExtName': 'flac',
                             'SQFailProcess': 4,
                             'SQFileHash': 'DC0AEB619143C7A91066E08C49258CB7',
                             'SQFileSize': 22986169,
                             'SQPayType': 3,
                             'SQPkgPrice': 1,
                             'SQPrice': 200,
                             'SQPrivilege': 10,
                             'Scid': 11299767,
                             'SingerId': [83823, 87865],
                             'SingerName': 'Wiz Khalifa、Charlie Puth',
                             'SongLabel': '',
                             'SongName': '<em>See You Again</em>',
                             'Source': '',
                             'SourceID': 0,
                             'SuperBitrate': 0,
                             'SuperDuration': 0,
                             'SuperExtName': '',
                             'SuperFileHash': '',
                             'SuperFileSize': 0,
                             'TopicRemark': '',
                             'TopicUrl': '',
                             'Type': 'audio',
                             'mvTotal': 0,
                             'trans_param': {'cid': 31179108,
                                             'display': 0,
                                             'display_rate': 0,
                                             'musicpack_advance': 0,
                                             'pay_block_tpl': 1}},
                            {'A320Privilege': 0,
                             'ASQPrivilege': 0,
                             'Accompany': 1,
                             'AlbumID': '14597377',
                             'AlbumName': 'See You Again (Piano Demo)',
                             'AlbumPrivilege': 0,
                             'AudioCdn': 100,
                             'Audioid': 12080153,
                             'Auxiliary': '',
                             'Bitrate': 128,
                             'Duration': 228,
                             'ExtName': 'mp3',
                             'FailProcess': 0,
                             'FileHash': '6BE63F669B2CAB186B0281E5E51BDBC4',
                             'FileName': 'Charlie Puth - <em>See You Again</em>',
                             'FileSize': 3649384,
                             'FoldType': 0,
                             'Grp': {},
                             'HQBitrate': 320,
                             'HQDuration': 228,
                             'HQExtName': 'mp3',
                             'HQFailProcess': 0,
                             'HQFileHash': '1C83BD8BAB66CB43F2FCE35F580ABA20',
                             'HQFileSize': 9129401,
                             'HQPayType': 0,
                             'HQPkgPrice': 0,
                             'HQPrice': 0,
                             'HQPrivilege': 0,
                             'HasAlbum': 1,
                             'HiFiQuality': 1,
                             'ID': '104358639',
                             'IsOriginal': 1,
                             'M4aSize': 931579,
                             'MixSongID': '104358639',
                             'MvHash': '07861ECAFD1B6DB2946A02F5D95EC58E',
                             'MvTrac': 3,
                             'MvType': 2,
                             'OldCpy': 1,
                             'OriOtherName': '',
                             'OriSongName': '<em>See You Again</em>',
                             'OtherName': '',
                             'OwnerCount': 3199,
                             'PayType': 0,
                             'PkgPrice': 0,
                             'Price': 0,
                             'Privilege': 0,
                             'Publish': 1,
                             'PublishAge': 255,
                             'QualityLevel': 2,
                             'ResBitrate': 0,
                             'ResDuration': 0,
                             'ResFileHash': '',
                             'ResFileSize': 0,
                             'SQBitrate': 0,
                             'SQDuration': 0,
                             'SQExtName': '',
                             'SQFailProcess': 0,
                             'SQFileHash': '',
                             'SQFileSize': 0,
                             'SQPayType': 0,
                             'SQPkgPrice': 0,
                             'SQPrice': 0,
                             'SQPrivilege': 0,
                             'Scid': 12080153,
                             'SingerId': [87865],
                             'SingerName': 'Charlie Puth',
                             'SongLabel': '',
                             'SongName': '<em>See You Again</em>',
                             'Source': '',
                             'SourceID': 0,
                             'SuperBitrate': 0,
                             'SuperDuration': 0,
                             'SuperExtName': '',
                             'SuperFileHash': '',
                             'SuperFileSize': 0,
                             'TopicRemark': '',
                             'TopicUrl': '',
                             'Type': 'audio',
                             'mvTotal': 0,
                             'trans_param': {'cid': -1,
                                             'display': 0,
                                             'display_rate': 0,
                                             'musicpack_advance': 0,
                                             'pay_block_tpl': 1}},
                            '作者的话：由于空间问题，这里只显示前2个歌曲信息，实际共有三十首'],
                  'page': 1,
                  'pagesize': 30,
                  'searchfull': 1,
                  'subjecttype': 0,
                  'tab': '全部',
                  'total': 353},
         'error_code': 0,
         'error_msg': '',
         'status': 1}
        """
        
        #检查错误码
        if self.data["error_code"]!=0:
            raise NetworkError(self.data["error_code"])
        
        #song对象列表
        self.songs=[]
        for i in self.data["data"]["lists"]:
            self.songs.append(song(i["FileHash"],i["AlbumID"]))



#获取专辑信息的网址
album_url="https://www.kugou.com/album/"
#专辑类
class album:
    def __init__(self,album_id):#专辑ID
        #发送get请求，返回html文件
        self.response=requests.get(album_url+str(album_id)+".html")
        
        #song对象列表
        self.songs=[]
        #html中会有 字母数字|数字 的字符串，“|”前是Hash，后是AlbumID
        """
        例如：
        <a title="Wiz Khalifa、Charlie Puth - See You Again" hidefocus="true" href="javascript:;" data="7775FBCCF9E20887AB01CBB41E87162D|229000">
            ...
        </a>
        """
        self.data_list=re.findall('[A-Z0-9]+\|[0-9]+',self.response.text)
        for i in self.data_list:
            self.songs.append(song(i.split("|")[0],i.split("|")[1]))
        
        #锁定歌曲详细简介
        f1=self.response.text.find("<p class=\"more_intro\">")+22
        f2=self.response.text.find("</p>",f1-1)
        #简介中可能会有html转义符，用这个函数进行转义
        self.intro=html.unescape(self.response.text[f1:f2].replace("<span></span>",""))
        
        #锁定歌曲信息
        f1=self.response.text.find("<p class=\"detail\">")+18
        f2=self.response.text.find("</p>",f1-1)
        """
        self.response.text[f1:f2]=='''
            <span>专辑名：</span>Taylor Gang Timeline (Mixtape)<br>
            <span>歌手：</span>Wiz Khalifa<br>
            <span>唱片公司：</span>华纳唱片<br>
            <span>发行时间：</span>2015-01-01
        '''
        """
        self.detail={}
        for i in html.unescape(self.response.text[f1:f2]).split("<br />"):#<br>会变成<br />，不知道为什么
            f_1=i.find("<span>")+6
            f_2=i.find("</span>",f_1-1)
            #后方可能出现\t，显示为8个空格，这里必须要写8个空格
            self.detail[i[f_1:f_2-1]] = i[f_2+7:].replace("\r\n        ","")



class singer:
    def __init__(self,album_id):
        pass



if __name__=="__main__":
    
    s=search("see you again")
    so=s.songs[0]
    
    #a=album(1602728)
    #print(len(a.songs))
    #a.songs[int(input("选择："))].download()

