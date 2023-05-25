# -*- coding:UTF-8 -*-

import sys
import json
import re
import os
import traceback

cur_path = os.path.dirname(__file__)
DB_PATH = cur_path + "/lyrics.db"
import httpclient
import sqliteclient

http = httpclient.Http()

class LyricsRequest:

    def __init__(self):

        self.table_name = "t_lyrics"
        self.sqlite = sqliteclient.Sqlite(DB_PATH)

    def init_db(self):

        sql_string = "create table if not exists %s(song_name text,singer text,album text,lyric_txt text,lyric txt)"%self.table_name
        self.sqlite.non_query(sql_string)



    """
    main function
    """
    def main(self,song_name):
        """
        @return: [(singer,album,lyric_txt,lyric)...]
        @rtype: list
        
        @return False: not find the lyrics
        """

        result = self.read_lyric(song_name)
        if result == []:
            result = self.get_baidu_lyrics(song_name)
            if not result:
                return False
            else:
                return result
        else:
            return result

        

    def read_lyric(self,song_name):
        """
        @return: [(singer,album,lyric_txt,lyric)...]
        @rtype: list
        """
        result = self.sqlite.query("select song_name,singer,album,lyric_txt,lyric from %s where song_name like '%%%s%%'"%(self.table_name,song_name))

        return result

    def get_baidu_lyrics(self,keyword):

        
        result = []
        url = "http://music.baidu.com/search/lrc?key=%s"%(http.quote(keyword.encode("u8")))
        html = http.connect(url)
        not_has_keyword = http.get_tag_html(html,"p",{"class":"sorry"})
        
        if len(not_has_keyword) > 0:
            return 
        songs_list = http.get_tag_html(html,"li",{"class":"clearfix bb"})
#        print len(songs_list)
        for i in songs_list:
#            print http.html2txt(i)
            song = self.get_song_attrs(i)
            if song:
                result.append(song)
        return result
#        print songs_list

    def get_song_attrs(self,html):

        no_write = False
        song_name_list = http.get_tag_attrs(html,"a",{"href":"/song/\d+"})
#        print song_name_list
        if song_name_list:
            song_name = song_name_list[0]["title"]
#            print song_name
        else:
            no_write = True

        singer_list = http.get_tag_attrs(html,"span",{"class":"author_list"})
#        print singer_list
        singer_html = http.get_tag_html(html,"span",{"class":"author_list"})
#        print singer_html
        if singer_list:
            singer = singer_list[0]["title"]
#            print singer
        else:
            singer == u"未知"
        album_list = http.get_tag_attrs(html,"a",{"href":"/album/\d+"})
#        print album_list
        if album_list:
            album = album_list[0]["title"]
        else:
            album = u"未知"
#        print html
        lyric_html = http.get_tag_html(html,"p",{"id":"lyricCont-\d+"}) 
#        print lyric_html
        if not lyric_html:
#            print "no lyric"
            no_write = True
        lyric_txt = http.html2txt(lyric_html[0])
#        print lyric_txt
#        lyric = http.get_tag_attrs(html,"a",{"class":"down-lrc-btn[^>]*"}) 
        lyric_url = re.findall("down-lrc-btn { 'href':'(.*?)'",html)[0]
        lyric_url = "http://music.baidu.com/" + lyric_url
        lyric = http.connect(lyric_url)
        exists_song_list = self.sqlite.query("select * from %s where song_name='%s' and singer='%s' "%(self.table_name,song_name,singer))
        if exists_song_list:
#            print exists_song_list
#            print "exists"
            no_write = True
        sql_string = "insert into %s(song_name,singer,album,lyric_txt,lyric) values(?,?,?,?,?)"%self.table_name
        param = (song_name,singer,album,lyric_txt,lyric)
        try:
#            print "non_query"
            if not no_write:
                self.sqlite.non_query(sql_string,param)
        except:
            traceback.print_exc()
            print sql_string.encode("u8")
        return param
#        return html

if "__main__" == __name__:

    test = LyricsRequest()
    test.init_db()
#    test.add_lyric2db("test","fafjdsa")
    song_name = u"我们都是木头人"
    lyrics_list = test.main(song_name)
    if lyrics_list:
        for lyric in lyrics_list:
            print lyric[0]
            print lyric[1]
            print lyric[2]
            print lyric[3]

    print len(lyrics_list)

#    print test.get_baidu_lyrics(song_name)


