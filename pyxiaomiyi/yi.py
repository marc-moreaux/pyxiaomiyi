#! /usr/bin/env python

import re
import time
import socket


DEBUG = True


def dPrint(*param):
    if DEBUG:
        print(*param)


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
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.ip, self.port))
        except:
            print('Could not connect to camera at: {}:{}'.format(
                self.ip, self.port))

        if self.sock is None:
            raise ValueError('Could not connect to camera at: {}:{}'.format(
                self.ip, self.port))

        self.token = 0
        self.sock.settimeout(1)

        self.send_code(257)
        data = self.get_buffer(expect='"rval": 0')
        self.token = re.findall('"param": (.+) }', data)[0]

    def send_code(self, code, param=None):
        '''Send a code to the camera
        '''
        msg = '{{"msg_id":{},"token":{}'.format(code, self.token)
        if param != None:
            msg += ', "param": "{}"'.format(param)
        msg += '}}'
        self.sock.send(msg.encode('utf-8'))

        dPrint('sent:', msg)

    def get_buffer(self, wait_time=2, buffer_size=4096, expect=''):
        '''
        Params:
            wait_time (int): wait 2 seconds for an answer max
            expect (str): an string expected in the buffer
        '''
        data = None
        start = time.time()
        while ((data is None)
               and ((time.time() - start) < wait_time)):
            try:
                data = str(self.sock.recv(buffer_size))[2:-1]
                if expect in data:
                    dPrint('recieved: ', data)
                    return data
                else:
                    data = None
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

    def get_configuration(self):
        '''Output the configuration of the camera
        '''
        self.send_code(3)

        data = self.get_buffer(expect='"rval": 0')
        if not data.endswith('} ] }'):
            data += self.get_buffer()

        data = eval(data)
        conf = {}
        for d in data['param']:
            k, v = list(d.items())[0]
            conf[k] = v
        return conf

    def show_configuration(self):
        conf = self.get_configuration()
        for k, v in conf.items():
            print(k, ' -- ', v)


if __name__ == '__main__':
    cam = Yi()
    cam.take_picture()
    # cam.grab_video(3)
    # cam.take_picture()
    # cam.show_configuration()
    print(cam)
