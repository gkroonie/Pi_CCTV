#############################
#FACIAL RECOGINITION PROGRAM#
#############################

#Python Packages
import face_recognition #performs the faicial recognition
import cv2 #OpenCV to read video from the webcam
import numpy as np #To perform mathematical wizardry
from datetime import datetime #Associating dates and times with recognitions
import subprocess as sp #To run the FFmpeg command from within Python
import sys, errno


# Face recognition on live video from your webcam. It includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

# Defining the input device for FFmpeg
Camera = '/dev/video0'

# Defining output UDP address
#UDP_out = '"udp://239.192.1.100:5000?pkt_size=1316"'

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)


# Obtaining dimensions of the video frame
#ret, frame = video_capture.read()
#height, width, ch = frame.shape

# Defining vairiable to enter into FFmpeg string
#dimension = '{}x{}'.format(width, height)
    #Commenting out as this part isn't needed -># f_format = 'bgr24' # bgr24 is just what OpenCV uses
#fps = str(video_capture.get(cv2.CAP_PROP_FPS))


# Structuring the FFmpeg string
command = ['ffmpeg',
           '-y',
           '-f', 'rawvideo',
           '-s', '640x480',
           '-pix_fmt', 'bgr24',
           '-r', '30',
           '-i', '-',
           '-an',
           '-vcodec', 'h264',
           '-b:v', '2000k',
           '\"udp://239.192.1.100:5000?pkt_size=1316\"' ]
           

# Subprocess to open pipe to command line
proc = sp.Popen(command, stdin=sp.PIPE, stderr=sp.PIPE)


# Load a sample picture for each person and learn how to recognize it.
george_image = face_recognition.load_image_file("george.jpg")
george_face_encoding = face_recognition.face_encodings(george_image)[0]

mike_image = face_recognition.load_image_file("mike.jpg")
mike_face_encoding = face_recognition.face_encodings(mike_image)[0]

marion_image = face_recognition.load_image_file("Marion.jpg")
marion_face_encoding = face_recognition.face_encodings(marion_image)[0]

# Create arrays of known face encodings and their names
known_face_encodings = [
    george_face_encoding,
    mike_face_encoding,
    marion_face_encoding
]

known_face_names = [
    "George",
    "Mike",
    "Marion"
]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            DateTime = datetime.now()
            now = DateTime.replace(microsecond=0)
            face_names.append(name)
            print(face_names, now)
    process_this_frame = not process_this_frame


    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)
    # FlippedFrame = cv2.flip(frame, 1)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    # Writing the OpenCV video frame to the FFmpeg pipe process (previously defined)
    for proc in process_list:
            if __name__ == '__main__':
                proc.start()
    
    try:
        proc.stdin.write(frame.tostring())
    except IOError as e:
        if e.errno == errno.EPIPE:
            print('WTF is going on')

# Cleanly exit all processes
video_capture.release()
cv2.destroyAllWindows()
proc.stdin.close()
proc.stderr.close()
proc.wait()

