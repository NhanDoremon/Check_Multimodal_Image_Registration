# python augmentation.py
from PIL import Image
import os
import random
import math
import numpy as np
import cv2
def flip_image(image, flip_type):
    if flip_type == "none":
        return image
    elif flip_type == "horizontal":
        flipped_horizontal = cv2.flip(image, 1)
        return flipped_horizontal
    elif flip_type == "vertical":
        flipped_vertical = cv2.flip(image, 0)
        return flipped_vertical

def rotate_image(image, angle):
    return image.rotate(angle)
def rotate_im(image, angle):
    """Rotate the image.
    
    Rotate the image such that the rotated image is enclosed inside the tightest
    rectangle. The area not occupied by the pixels of the original image is colored
    black. 
    
    Parameters
    ----------
    
    image : numpy.ndarray
        numpy image
    
    angle : float
        angle by which the image is to be rotated
    
    Returns
    -------
    
    numpy.ndarray
        Rotated Image
    
    """
    # grab the dimensions of the image and then determine the
    # centre
    (h, w) = image.shape[:2]
    (cX, cY) = (w // 2, h // 2)

    # grab the rotation matrix (applying the negative of the
    # angle to rotate clockwise), then grab the sine and cosine
    # (i.e., the rotation components of the matrix)
    M = cv2.getRotationMatrix2D((cX, cY), angle, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])

    # compute the new bounding dimensions of the image
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))

    # adjust the rotation matrix to take into account translation
    # M[0, 2] += (nW / 2) - cX
    # M[1, 2] += (nH / 2) - cY

    # perform the actual rotation and return the image
    image = cv2.warpAffine(image, M, (w, h))

#    image = cv2.resize(image, (w,h))
    return image

def get_corners(bboxes,image_width,image_height):
    
    """Get corners of bounding boxes
    
    Parameters
    ----------
    
    bboxes: numpy.ndarray
        Numpy array containing bounding boxes of shape `N X 4` where N is the 
        number of bounding boxes and the bounding boxes are represented in the
        format `x1 y1 x2 y2`
    
    returns
    -------
    
    numpy.ndarray
        Numpy array of shape `N x 8` containing N bounding boxes each described by their 
        corner co-ordinates `x1 y1 x2 y2 x3 y3 x4 y4`      
        
    """


    # Tính toán tọa độ tương đối của bounding box trên ảnh
    x_center = bboxes[1] * image_width
    y_center = bboxes[2] * image_height
    width = bboxes[3] * image_width
    height = bboxes[4] * image_height

    # Tính tọa độ của các góc bounding box
    x1 = int(x_center - width / 2)
    y1 = int(y_center - height / 2)
    x4 = int(x_center + width / 2)
    y4 = int(y_center + height / 2)
    
    x2 = x1 + width
    y2 = y1 
    
    x3 = x1
    y3 = y1 + height

    corners = np.hstack((x1,y1,x2,y2,x3,y3,x4,y4))
    
    return corners

def rotate_box(corners,angle, w,h):
    
    """Rotate the bounding box.
    
    
    Parameters
    ----------
    
    corners : numpy.ndarray
        Numpy array of shape `N x 8` containing N bounding boxes each described by their 
        corner co-ordinates `x1 y1 x2 y2 x3 y3 x4 y4`
    
    angle : float
        angle by which the image is to be rotated
        
    cx : int
        x coordinate of the center of image (about which the box will be rotated)
        
    cy : int
        y coordinate of the center of image (about which the box will be rotated)
        
    h : int 
        height of the image
        
    w : int 
        width of the image
    
    Returns
    -------
    
    numpy.ndarray
        Numpy array of shape `N x 8` containing N rotated bounding boxes each described by their 
        corner co-ordinates `x1 y1 x2 y2 x3 y3 x4 y4`
    """
    # Kích thước ảnh
    (h, w) = (h,w)
    (cx, cy) = (w // 2, h // 2)
    corners = corners.reshape(-1,2)
    corners = np.hstack((corners, np.ones((corners.shape[0],1), dtype = type(corners[0][0]))))
    # print (corners)
    M = cv2.getRotationMatrix2D((cx, cy), angle, 1.0)
    
    
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])
    
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))
    # adjust the rotation matrix to take into account translation
    # M[0, 2] += (nW / 2) - cx
    # M[1, 2] += (nH / 2) - cy
    # Prepare the vector to be transformed
    calculated = np.dot(M,corners.T).T
    
    calculated = calculated.reshape(-1,8)
    
    return calculated

def get_enclosing_box(corners,image_height):
    """Get an enclosing box for ratated corners of a bounding box
    
    Parameters
    ----------
    
    corners : numpy.ndarray
        Numpy array of shape `N x 8` containing N bounding boxes each described by their 
        corner co-ordinates `x1 y1 x2 y2 x3 y3 x4 y4`  
    
    Returns 
    -------
    
    numpy.ndarray
        Numpy array containing enclosing bounding boxes of shape `N X 4` where N is the 
        number of bounding boxes and the bounding boxes are represented in the
        format `x1 y1 x2 y2`
        
    """
    x_ = corners[:,[0,2,4,6]]
    y_ = corners[:,[1,3,5,7]]

    xmin = np.min(x_,1).reshape(-1,1)
    ymin = np.min(y_,1).reshape(-1,1)
    xmax = np.max(x_,1).reshape(-1,1)
    ymax = np.max(y_,1).reshape(-1,1)
    # print("ymax", ymax[:,0] )
    if ymax[:,0] > image_height:
        ymax[:,0] = image_height
    final = np.hstack((xmin, ymin, xmax, ymax,corners[:,8:]))
    
    return final
def update_label(label_lines, image_width, image_height, flip_type=None, angle=None):
    updated_label_lines = []
    for line in label_lines:
        parts = line.strip().split()
        class_id = parts[0]
        x_center = float(parts[1])
        y_center = float(parts[2])
        width = float(parts[3])
        height = float(parts[4])
        new_x_center = x_center
        new_y_center = y_center
        new_width = width
        new_height = height
        
        if flip_type == "none":
            new_x_center = new_x_center
            new_y_center = new_y_center
        elif flip_type == "horizontal":
            new_x_center = 1 - new_x_center
        elif flip_type == "vertical":
            new_y_center = 1 - new_y_center

        if angle is not None:
            angle = int(angle)
            bbox_yolo = [parts[0],new_x_center,new_y_center,new_width,new_height]
            corner = get_corners(bbox_yolo,image_width,image_height)
            rotate_bbox = rotate_box(corner,angle, image_width,image_height)
            enclose_bbox = get_enclosing_box(rotate_bbox,image_height)
            x_min = float(enclose_bbox[:,0])
            y_min = float(enclose_bbox[:,1])
            x_max = float(enclose_bbox[:,2])
            y_max = float(enclose_bbox[:,3])
            new_x_center = ((x_min + x_max) / 2)/image_width
            new_y_center = ((y_min + y_max) / 2)/image_height
            new_width = (x_max - x_min)/image_width
            new_height = (y_max - y_min)/image_height
            pass

        updated_label_line = f"{class_id} {new_x_center} {new_y_center} {new_width} {new_height}"
        updated_label_lines.append(updated_label_line)

    return updated_label_lines

input_folder = "./MyDatasets/Valid"
final_dataset = "./Final_Datasets"
output_folder = "./Final_Datasets/Augmented_Valid"

if not os.path.exists(final_dataset):
    os.makedirs(final_dataset)
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

output_IR= os.path.join(output_folder, 'IR_Data_Image_Augmented')
output_Thermal = os.path.join(output_folder, 'Thermal_Data_Image_Augmented')
output_Labels = os.path.join(output_folder, 'Label_Data_Image_Augmented')

if not os.path.exists(output_IR):
    os.makedirs(output_IR)
if not os.path.exists(output_Thermal):
    os.makedirs(output_Thermal)
if not os.path.exists(output_Labels):
    os.makedirs(output_Labels)



flip_types = ["none","horizontal", "vertical"]
angles = [-10,-20,0,10,20]
augment_factor = 3  # Số lần tăng gấp 3 lượng dữ liệu

# Duyệt qua tất cả các tệp trong thư mục input_folder
for ir_file in os.listdir(os.path.join(input_folder, 'IR_Data_Image')):
    if ir_file.endswith('.jpg'):
        ir_path = os.path.join(input_folder, 'IR_Data_Image', ir_file)
        thermal_path = os.path.join(input_folder, 'Thermal_Data_Image', ir_file.replace('IR', 'Thermal'))
        label_path = os.path.join(input_folder, 'Label_Data_Image', ir_file.replace('IR_Image', 'Label_Image').replace('.jpg', '.txt'))
        # print ("label_path:",label_path)

        image_name = os.path.splitext(ir_file)[0] #Ex: IR_Image_13_1410
        image_name = image_name.split("_") #Ex: ['IR', 'Image', '13', '1410']
        # Lấy phần tên tệp từ vị trí thứ 2 trở đi
        image_name = '_'.join(image_name[1:])  #Ex: Image_13_1410
        print(image_name)
        with open(label_path, "r") as label_file:
            label_lines = label_file.readlines()

        for _ in range(augment_factor):
            flip_type = random.choice(flip_types)
            angle_deg = random.choice(angles)

            IR_image = cv2.imread(ir_path)
            Thermal_image = cv2.imread(thermal_path)
            # Kích thước ảnh
            image_height, image_width, _ = IR_image.shape
            augmented_IR_image = IR_image
            augmented_Thermal_image = Thermal_image

            if flip_type:
                augmented_IR_image = flip_image(augmented_IR_image, flip_type)
                augmented_Thermal_image = flip_image(augmented_Thermal_image, flip_type)

            if angle_deg:
                augmented_IR_image = rotate_im(augmented_IR_image, angle_deg)
                augmented_Thermal_image = rotate_im(augmented_Thermal_image, angle_deg)

            augmented_IR_image_path = os.path.join(output_folder,"IR_Data_Image_Augmented",f"IR_{image_name}_Augmented_{flip_type}_{angle_deg}.jpg")
            augmented_Thermal_image_path = os.path.join(output_folder,"Thermal_Data_Image_Augmented",f"ThermaL_{image_name}_Augmented_{flip_type}_{angle_deg}.jpg")            
            # save image 
            cv2.imwrite(augmented_IR_image_path,augmented_IR_image)
            cv2.imwrite(augmented_Thermal_image_path,augmented_Thermal_image)
            
            # print ("augmented_IR_image_path:",augmented_IR_image_path) #Ex: ./Augmented_Train\IR_Data_Image_Augmented\IR_Image_10_365_Augmented_horizontal_180.jpg
            # print ("augmented_Thermal_image_path:",augmented_Thermal_image_path) #Ex: ./Augmented_Train\Thermal_Data_Image_Augmented\ThermaL_Image_10_365_Augmented_horizontal_180.jpg
            updated_labels = update_label(label_lines, image_width, image_height, flip_type=flip_type, angle=angle_deg)
            updated_label_path = os.path.join(output_folder,"Label_Data_Image_Augmented", f"Label_{image_name}_augmented_{flip_type}_{angle_deg}.txt")

            # print ("updated_label_path", updated_label_path) #Ex: ./Augmented_Train\Image_10_365_augmented_vertical_30.txt
            
            with open(updated_label_path, "w") as updated_label_file:
                for line in updated_labels:
                    updated_label_file.write(line + "\n")
