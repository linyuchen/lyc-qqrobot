#coding:UTF8
"""
tcp
"""
import socket
import urllib

class Packet:

    SIZE = 8

    def __init__(self):


        self.header = "%%0%dd"%(Packet.SIZE)
#        self.bufferSize = 1024

    def __create_sock(self):

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return sock

    def create_client_sock(self, addr, port):

        sock = self.__create_sock()
        sock.connect((addr, port))
        return sock

    def create_server_sock(self, addr, port):
        
        sock = self.__create_sock()
        sock.bind((addr, port))
        sock.listen(0)
        return sock

    def pack(self, data):
        """
        :data: unicode data
        :return: urlquote data 
        """

#        data = urllib.quote(data)
        data = data.encode("u8")
        length = len(data)        
        header = self.header % length
#        print header
        assert len(header) <= Packet.SIZE, "data too long"
#        print header
        data = header + data
        return data

    def unpack(self, data):
        """
        :data: packed data
        :return: unpack data
        """

#        data = urllib.unquote(data)
        data = data.decode("u8")
#        print data
        return data


    def send(self, sock, data):

        data = self.pack(data)
        
        #sock = self.create_sock()
#        print data
        sock.sendall(data)
        #data = self.read(sock)
        #sock.close()
        #return data

    def read(self, sock):

        header = sock.recv(Packet.SIZE)
        #header = sock.recv(100)
        #print u"头部", header
        length = int(header)

#        print length
        resData = ""
#        while 1:
#        data = sock.recv(length)
#        resData += data
        read_length = 0
        while 1:
            data = sock.recv(length)
            read_length += len(data)
#            print read_length
            resData += data
            if read_length == length:
                break
#            print len(data)
#        print resData
        data = self.unpack(resData)
        return data






