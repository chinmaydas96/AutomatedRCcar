import threading
import socketserver
import cv2
import numpy as np
import math


class VideoStreamHandler(socketserver.StreamRequestHandler):

    def handle(self):

        stream_bytes = ' '
        
        try:
            while True:
                stream_bytes += self.rfile.read(1024)
                first = stream_bytes.find('\xff\xd8')
                last = stream_bytes.find('\xff\xd9')
                if first != -1 and last != -1:
                    jpg = stream_bytes[first:last+2]
                    stream_bytes = stream_bytes[last+2:]
                    image = cv2.imdecode(np.fromstring(jpg,dtype="uint8"),1)
                    cv2.imshow('image', image)
                    cv2.waitKey(30)

            print ("Destroying")
            cv2.destroyAllWindows()

        finally:
            print ("Connection closed on thread 1")


def server_thread(host, port):
    server = socketserver.TCPServer((host, port), VideoStreamHandler)
    server.serve_forever()

video_thread = threading.Thread(target=server_thread('192.168.1.7', 8000))
video_thread.start()
