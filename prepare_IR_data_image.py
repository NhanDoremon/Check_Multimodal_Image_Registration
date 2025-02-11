# python prepare_IR_data_image.py
# Importing all necessary libraries
import cv2
import os
import cv2 
import numpy as np
from matplotlib import pyplot as plt


path_video = "./Data_videos/"
path_image = "./Data_images/" 

# frame
currentframe = 0
#selec file
type_camera = "IR"
ratio_frame = 5
file_number = 6
path_video  = path_video + type_camera + "_camera/" + type_camera + "_Data_" + str(file_number) + ".avi"
path_image  = path_image + type_camera + "_Data/"   + type_camera + "_Data_Image_" + str(file_number)+ "/" + type_camera + "_Image_"+ str(file_number)+ "_"
capture_video = cv2.VideoCapture(path_video)

### PARAMETER FOR UNDISTORTION
IR_camera_parameter = np.array([[2.718847540317855e+02, 0, 1.622103145915451e+02],[0, 2.717428547794702e+02,1.120884552560783e+02],[0, 0, 1]])
IR_Distortion_coefficient = np.array([0.078203777079096, 0.121931769290830,-0.013490151349214,0.002938087480719, -1.853156942217642]) #k1,k1,p1,p2,k3
IR_h,IR_w = 240,320
IR_newcameramtx, IR_roi = cv2.getOptimalNewCameraMatrix(IR_camera_parameter, IR_Distortion_coefficient, (IR_w,IR_h), 0, (IR_w,IR_h))


H = np.array([[ 8.35521878e-01 ,-3.33623790e-02 , 4.66509102e+01], [-2.94772799e-03 , 8.16741335e-01  ,1.42137997e+01], [-1.43029566e-04, -1.60028489e-04,  1.00000000e+00]])
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
            IR_undistortion_image = cv2.undistort(frame, IR_camera_parameter, IR_Distortion_coefficient, None, IR_newcameramtx)
            # crop the image
            x, y, w, h = IR_roi
            IR_undistortion_image = IR_undistortion_image[y:y+h, x:x+w]

            im_exp[0:239, 0:319] = IR_undistortion_image

            # writing the extracted images
            cv2.imwrite(link_save_image, im_exp)
            # increasing counter so that it will
            # show how many frames are created
        currentframe += 1
        # print(frame.shape)
    else:
        break
  
# Release all space and windows once done
capture_video.release()
cv2.destroyAllWindows()