import cv2
import mediapipe as mp
import numpy as np
import pandas as pd
import time
import imageio
import tkinter as tk
from tkinter import filedialog

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh

webcam = False
all_pointe = False
# For webcam input:
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
if webcam:
  cap = cv2.VideoCapture(0)
else:
    # Open the file explorer dialog
    file_path = filedialog.askopenfilename()

    # Check if a file was selected
    if file_path:
        print("Selected file:", file_path)
    else:
        print("No file selected.")
    cap = cv2.VideoCapture(file_path)

# Define the codec and create VideoWriter object
with imageio.get_writer('output.mp4', fps=60) as writer:

    llx, lly, llz = [], [], []
    ulx, uly, ulz = [], [], []
    lelx, lely, lelz = [], [], []
    rlx, rly, rlz = [], [], []
    jcx, jcy, jcz = [], [], []
    jlx, jly, jlz = [], [], []
    jrx, jry, jrz = [], [], []
    jlcx, jlcy, jlcz = [], [], []
    jrcx, jrcy, jrcz = [], [], []
    jlclx, jlcly, jlclz = [], [], []
    jrcrx, jrcry, jrcrz = [], [], []
    jlux, jluy, jluz = [], [], []
    jrux, jruy, jruz = [], [], []
    bex, bey, bez = [], [], []
    rrex, rrey, rrez = [], [], []
    lrex,lrey,lrez = [], [], []
    pTime = 0
    with mp_face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as face_mesh:
      while cap.isOpened():
        success, image = cap.read()
        if not success and webcam:
          print("Ignoring empty camera frame.")
          # If loading a video, use 'break' instead of 'continue'.
          continue
        elif not success and not webcam:
          dict = {'LLx': llx, 'LLy': lly, 'LLz': llz,
                  'ULx': ulx, 'ULy': uly, 'ULz': ulz,
                  'LeLx': lelx, 'LeLy': lely, 'LeLz': lelz,
                  'RLx': rlx, 'RLy': rly, 'RLz': rlz,
                  'JCx': jcx, 'JCy': jcy, 'JCz': jcz,
                  'JLx': jlx, 'JLy': jly, 'JLz': jlz,
                  'JRx': jrx, 'JRy': jry, 'JRz': jrz,
                  'JLCx': jlcx, 'JLCy': jlcy, 'JLCz': jlcz,
                  'JRCx': jrcx, 'JRCy': jrcy, 'JRCz': jrcz,
                  'JLCLx': jlclx, 'JLCLy': jlcly, 'JLCLz': jlclz,
                  'JRCRx': jrcrx, 'JRCRy': jrcry, 'JRCRz': jrcrz,
                  'JLUx': jlux, 'JLUy': jluy, 'JLUz': jluz,
                  'JRUx': jrux, 'JRUy': jruy, 'JRUz': jruz,
                  'BEx': bex, 'BEy': bey, 'BEz': bez,
                  'RREx': rrex, 'RREy':rrey, 'RREz': rrez,
                  'LREx': lrex, 'LREy':lrey, 'LREz': lrez,
                  }
          df = pd.DataFrame(dict)
          # Open file dialog for save location selection
          save_path = filedialog.asksaveasfilename()

          # Check if a file path was selected
          if save_path:
              print("Selected file path:", save_path)
          else:
              print("No file path selected.")
          df.to_csv(save_path)
          break

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(image, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN,
                    3, (0, 255, 0), 3)
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(image)

        ih, iw, ic = image.shape
        face_3d = []
        face_2d = []

        # Draw the face mesh annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.multi_face_landmarks:
          for face_landmarks in results.multi_face_landmarks:
            for id, lm in enumerate(face_landmarks.landmark):
                ih, iw, ic = image.shape
                x, y, z = int(lm.x * iw), int(lm.y * ih), float(lm.z * ic)
                if all_pointe:
                  cv2.putText(image, str(id), (x, y), cv2.FONT_HERSHEY_PLAIN, 0.7, (0, 255, 0), 1)
                elif id == 17: # Lower lip
                  llx.append(x)
                  lly.append(y)
                  llz.append(z)
                elif id == 0: # Upper lip
                  ulx.append(x)
                  uly.append(y)
                  ulz.append(z)
                elif id == 287: # Left lip
                  lelx.append(x)
                  lely.append(y)
                  lelz.append(z)
                elif id == 57: # Right lip
                  rlx.append(x)
                  rly.append(y)
                  rlz.append(z)
                elif id == 152: # Jaw center
                  jcx.append(x)
                  jcy.append(y)
                  jcz.append(z)
                elif id == 378: # Jaw left
                  jlx.append(x)
                  jly.append(y)
                  jlz.append(z)
                elif id == 149: # Jaw right
                  jrx.append(x)
                  jry.append(y)
                  jrz.append(z)
                elif id == 377: # Jaw left center
                  jlcx.append(x)
                  jlcy.append(y)
                  jlcz.append(z)
                elif id == 262: # Jaw left upper
                  jlux.append(x)
                  jluy.append(y)
                  jluz.append(z)
                elif id == 148: # Jaw right center
                  jrcx.append(x)
                  jrcy.append(y)
                  jrcz.append(z)
                elif id == 32: # Jaw right upper
                  jrux.append(x)
                  jruy.append(y)
                  jruz.append(z)
                elif id == 400: # Jaw left center left
                  jlclx.append(x)
                  jlcly.append(y)
                  jlclz.append(z)
                elif id == 176: # Jaw right center right
                  jrcrx.append(x)
                  jrcry.append(y)
                  jrcrz.append(z)
                elif id == 6: # Between eyes
                  bex.append(x)
                  bey.append(y)
                  bez.append(z)
                elif id == 226: # right of right eye
                  rrex.append(x)
                  rrey.append(y)
                  rrez.append(z)
                elif id == 244: # left of right eye
                  lrex.append(x)
                  lrey.append(y)
                  lrez.append(z)
                if id in [0, 1, 17, 57, 287, 4, 152, 378, 149, 6, 226, 244, 464, 446, 262,32,148,377,400,176]:
                  cv2.putText(image, ".", (x, y), cv2.FONT_HERSHEY_PLAIN,0.7, (0, 255, 0), 3)
                  face_2d.append([x,y])
                  face_3d.append([x,y,lm.z])
                if id == 1:
                  nose_2d = (x, y)
                  nose_3d = (x,y,lm.z*3000)

            face_2d = np.array(face_2d, dtype=np.float64)
            face_3d = np.array(face_3d, dtype=np.float64)

            # The camera matrix
            focal_length = iw
            cam_matrix = np.array([[focal_length,0,ih/2],
                                   [0,focal_length,iw/2],
                                   [0,0,1]])

            # The distortion parameters
            dist_matrix = np.zeros((4,1), dtype=np.float64)

            # solve PnP
            success, rot_vec, trans_vec = cv2.solvePnP(face_3d, face_2d, cam_matrix, dist_matrix)

            # Get rotational matrix
            rmat, jac = cv2.Rodrigues(rot_vec)

            # Get angles
            angles, mtxR, mtxQ, Qx, Qy, Qz = cv2.RQDecomp3x3(rmat)

            # Get the rotation degrees
            x = angles[0] * 360
            y = angles[1] * 360
            z = angles[2] * 360

            # See where user's head is tilting
            if y < -10:
              text = "Looking Left"
            elif y > 10:
              text = "Looking Right"
            elif x < -10:
              text = "Looking Down"
            elif x > 10:
              text = "Looking Up"
            else:
              text = "Looking Forward"

            # Dispay the nose direction
            nose_3d_projection, jacobian = cv2.projectPoints(nose_3d, rot_vec, trans_vec, cam_matrix, dist_matrix)

            p1 = (int(nose_2d[0]), int(nose_2d[1]))
            p2 = (int(nose_2d[0] + y * 10), int(nose_2d[1] - x * 10))

            cv2.line(image, p1, p2, (255,0,0), 3)

            # add text on the image
            cv2.putText(image, text, (250,50), cv2.FONT_HERSHEY_PLAIN, 2, (0,255,0), 2)



            """mp_drawing.draw_landmarks(
                image=image,
                landmark_list=face_landmarks,
                connections=mp_face_mesh.FACEMESH_TESSELATION,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp_drawing_styles
                .get_default_face_mesh_tesselation_style())
            mp_drawing.draw_landmarks(
                image=image,
                landmark_list=face_landmarks,
                connections=mp_face_mesh.FACEMESH_CONTOURS,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp_drawing_styles
                .get_default_face_mesh_contours_style())
            mp_drawing.draw_landmarks(
                image=image,
                landmark_list=face_landmarks,
                connections=mp_face_mesh.FACEMESH_IRISES,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp_drawing_styles
                .get_default_face_mesh_iris_connections_style())"""
        # Flip the image horizontally for a selfie-view display.
        cv2.imshow('MediaPipe Face Mesh', image)# cv2.flip(image, 1))
        #writer.append_data(image)
        if cv2.waitKey(5) & 0xFF == 27:
          break
    if webcam:
      cap.release()