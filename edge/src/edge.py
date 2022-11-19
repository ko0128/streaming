#importing libraries
import socket
import cv2
import pickle
import struct
from flask import Flask, render_template, Response, request, json

app = Flask(__name__)

def gen_frames(client_socket):
    print('Gen_frame')
    data = b""
    payload_size = struct.calcsize("Q")
    while True:
        while len(data) < payload_size:
            packet = client_socket.recv(4*1024)
            print('RECEIVED')
            if not packet: break
            data+=packet
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q",packed_msg_size)[0]
        while len(data) < msg_size:
            data += client_socket.recv(4*1024)
        frame_data = data[:msg_size]
        data  = data[msg_size:]
        frame = pickle.loads(frame_data)
        #success, frame = camera.read()
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def gen_frames_get(clientSocket):
    print('Gen_frame_get')
    data = b""
    payload_size = struct.calcsize("Q")
    while True:
        #print(f'payload_size: {payload_size}')
        while len(data) < payload_size:
            packet = clientSocket.recv(4*1024)
            #print('RECEIVED')
            if not packet: break
            data+=packet
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        #print(f'packed_msg_size: {packed_msg_size}')
        msg_size = struct.unpack("Q",packed_msg_size)[0]
        #print(f'msg_size: {msg_size}')
        while len(data) < msg_size:
            data += clientSocket.recv(4*1024)
        frame_data = data[:msg_size]
        data  = data[msg_size:]
        frame = pickle.loads(frame_data)
        #success, frame = camera.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        canny = cv2.Canny(blurred, 30, 150)

        ret, buffer = cv2.imencode('.jpg', canny)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')



@app.route('/video', methods=['GET'])
def video():
    # data = json.loads(request.data)
    # print(data)
    # if data['status']==0:
    #     return "Useage: curl -X POST -H \"Content-Type: application/json\" -d \'{\"status\":0}\' \"[ip]:[port]/video\""
    IPADDR = request.args.get('ip')
    PORT = int(request.args.get('port'))
    clientSocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    clientSocket.connect((IPADDR,PORT))

    return Response(gen_frames_get(clientSocket),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
    #return render_template('video.html') 

#curl -X POST -H "Content-Type: application/json" -d '{"status":0}' "127.0.0.1:7777/video"

@app.route('/')
def index():
    print('In index')
    return render_template('index.html')

if __name__=='__main__':
    app.run('0.0.0.0',port=5566)
    #app.run('0.0.0.0')