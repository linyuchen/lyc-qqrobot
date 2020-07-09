#coding=UTF8
import lyrics_request
lyrics_request = lyrics_request.LyricsRequest()

class Lyrics:

    def __init__(self):
        self.lyrics_list = []

    def get_lyrics(self,song_name):

        lyrics_list = lyrics_request.main(song_name)
#        print lyrics
        if lyrics_list:
            self.lyrics_list = lyrics_list
            index = 1
            result = ""
            for lyric in lyrics_list:
                result += u"%d：歌名:%s，歌手:%s，专辑名:%s\n"%(index,lyric[0],lyric[1],lyric[2])
                index += 1

            return result
        else:
            return u"没有找到 %s 相关歌词"%song_name 

    def get_lyric(self,index,lrc_type=3):
        """
        @param index:the index of self.lyrics_list
        @param lrc_type:3 txt, 4 lrc
        """

        if self.lyrics_list == []:
            return u"请先搜索歌词!"
        if not index.isdigit():
            return u"命令有误"
        index = int(index)
        if index > len(self.lyrics_list):
            return u"命令有误"

        return self.lyrics_list[index - 1][lrc_type]

