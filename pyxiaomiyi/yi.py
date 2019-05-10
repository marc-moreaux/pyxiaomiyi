#! /usr/bin/env python
# encoding: windows-1250
#
# Res Andy 

import os, re, sys, time, socket

class Yi:
    '''Class to access functionalities of the xiaomi yi action camera
    
    Params:
        ip (str): ip of the camera
        port (int): interface port of the camera
    '''

    def __init__(self, ip='192.168.42.1', port=7878):

        self.ip = ip
        self.port = port
        self.sock = None
        self.token = 0
        self.connect()

    def __repr__(self):
        return '{}:{}, {}'.format(self.ip, self.port, self.token)

    def connect(self):
        '''Connect to the camera to get a token
        '''
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self.ip, self.port))
            self.sock = sock
        except:
            print('Could not connect to camera at: {}:{}'.format(
                self.ip, self.port))

        self.token = 0
        self.sock.settimeout(1)

        self.send_code(257)
        while True:
            data = self.get_buffer()
            if 'rval' in data:
                break
        self.token = re.findall('"param": (.+) }', data)[0]

    def send_code(self, code, param=None):
        '''Send a code to the camera
        '''
        msg = '{{"msg_id":{},"token":{}'.format(code, self.token)
        if param != None:
            msg += ', "param": "{}"'.format(param)
        msg += '}}'
        self.sock.send(msg.encode('utf-8'))
        print('sent:', msg)

    def get_buffer(self, wait_time=2):
        '''
        Params:
            wait_time (int): wait 2 seconds for an answer max
        '''
        data = None
        start = time.time()
        while (data == None) and ((time.time() - start)  < wait_time):
            try:
                data = str(self.sock.recv(4096))
                print('recieved: ', data)
                return data
            except:
                time.sleep(0.4)
        print('nothing in buffer')
        
    def take_picture(self):
        self.send_code(769)
        for _ in range(5):
            self.get_buffer()

    def grab_video_start(self):
        self.send_code(513)
        for _ in range(3):
            self.get_buffer()

    def grab_video_stop(self):
        self.send_code(514)
        for _ in range(3):
            self.get_buffer()

    def grab_video(self, duration):
        self.grab_video_start()
        time.sleep(duration)
        self.grab_video_stop()

cam = Yi()
cam.take_picture()
cam.grab_video(3)
cam.take_picture()
print(cam)
