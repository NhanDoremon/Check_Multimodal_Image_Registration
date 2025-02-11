# python prepare_thermal_data_image.py
# Importing all necessary libraries
import cv2
import os
import cv2 
import numpy as np
from matplotlib import pyplot as plt


path_video = "../Datasets/Data_videos/"
path_image = "../Datasets/Data_images/" 

# frame
currentframe = 0
#selec file
type_camera = "Thermal"
ratio_frame = 5
file_number = 18
path_video  = path_video + type_camera + "_camera/" + type_camera + "_Data_" + str(file_number) + ".avi"
path_image  = path_image + type_camera + "_Data/"   + type_camera + "_Data_Image_" + str(file_number)+ "/" + type_camera + "_Image_"+ str(file_number)+ "_"
capture_video = cv2.VideoCapture(path_video)

### PARAMETER FOR UNDISTORTION
T_camera_parameter = np.array([[3.198835875300515e+02, 0, 1.699457327643448e+02],[0, 3.196748530148337e+02 ,1.230209988869137e+02],[0, 0, 1]])
T_Distortion_coefficient = np.array([-0.433023739947287, 0.979431702212187,-0.001765084687888,3.163936721503637e-04, -1.780325058940053])
h_T,w_T = (240,320)
T_newcameramtx, T_roi = cv2.getOptimalNewCameraMatrix(T_camera_parameter, T_Distortion_coefficient, (w_T,h_T), 0, (w_T,h_T))

H = np.array([[ 8.35521878e-01 ,-3.30623790e-02 , 4.69509102e+01], [-2.94772799e-03 , 8.16741335e-01  ,1.42137997e+01], [-1.43029566e-04, -1.60028489e-04,  1.00000000e+00]]) #35,33,66
# Tạo một mảng 2 chiều với kích thước 334x239
black_img = np.zeros((239,334,3), dtype=np.uint8)
# Gán màu đen cho tất cả các pixel
black_img[:, :] = 0   
im_exp = black_img

while(True):
    # reading from frame
    ret,frame = capture_video.read()
    if ret:
        if currentframe%ratio_frame == 0:
            # if video is still left continue creating images
            link_save_image  = path_image + str(currentframe) + '.jpg'
            print ('Creating..' + link_save_image)

            # undistort
            T_undistortion_image = cv2.undistort(frame, T_camera_parameter, T_Distortion_coefficient, None, T_newcameramtx)
            # crop the image
            x, y, w, h = T_roi
            T_undistortion_image = T_undistortion_image[y:y+h, x:x+w]

            w_frame_max = 334  #334 is the maximum width after wrapping the image
            h_frame_max = 239   #239 is the height of Original IR image

            im_per = cv2.warpPerspective(T_undistortion_image, H, (w_frame_max,h_frame_max))
            M = np.float32([[1, 0, -12], [0, 1, +4]])  # Ma trận transform dịch trái -11 pixel, xuống +4 pixel
            shifted_img = cv2.warpAffine(im_per, M, (w_frame_max, h_frame_max))

            # writing the extracted images
            cv2.imwrite(link_save_image, shifted_img)
            # increasing counter so that it will
            # show how many frames are created
        currentframe += 1
        # print(frame.shape)
    else:
        break
  
# Release all space and windows once done
capture_video.release()
cv2.destroyAllWindows()