
### python create_overlap_image.py
import sys
import os
import cv2
from PIL import Image, ImageEnhance
import numpy as np
folder_path = './Selected_data_images/Less_Smoke/Far/Multi_person/Data_Image_10'
alpha = 0.4
brightness_factor = 2.0
contrast_factor = 1.2
current_index = 0
ir_image_list = []
thermal_image_list = []
ir_image_path = []
thermal_image_path = []
# Tạo thư mục chứa các ảnh overlap
folder_number = os.path.basename(folder_path) #trích xuất đường dẫn cuối cùng, ví dụ Data_Image_6
folder_number = folder_number.split("_")[2] # Lấy số thứ tự folder 
overlap_dir = os.path.join(folder_path, 'Overlap_Data_Image_'+ str(folder_number)) #lấy folder_path + Overlap_Data_Image + số tt
os.makedirs(overlap_dir, exist_ok=True) # tạo thư mục với tên như biến overlap_path

# Tạo thư mục chứa các file label
label_dir = os.path.join(folder_path, 'Label_Data_Image_'+ str(folder_number))
os.makedirs(label_dir, exist_ok=True)

# Lặp qua tất cả các tệp và thư mục trong thư mục Data_image_{number}
for root, dirs, files in os.walk(folder_path):
    for dir_name in dirs:
        # Kiểm tra nếu tên của folder con bắt đầu bằng "IR", gán đường dẫn của nó cho biến A
        if dir_name.startswith("IR"):
            ir_data_dir = os.path.join(root, dir_name)
        # Kiểm tra nếu tên của folder con bắt đầu bằng "Thermal", gán đường dẫn của nó cho biến B
        elif dir_name.startswith("Thermal"):
            thermal_data_dir = os.path.join(root, dir_name)

ir_image_list = os.listdir(ir_data_dir)
thermal_image_list = os.listdir(thermal_data_dir)

# Sắp xếp danh sách hình ảnh theo thứ tự số trong tên file
ir_image_list.sort(key=lambda x: int(x.split("_")[3].split(".")[0]))
thermal_image_list.sort(key=lambda x: int(x.split("_")[3].split(".")[0]))

# vòng lặp với số lần tương ứng số lượng cặp ảnh
for current_index in range(len(ir_image_list)):
    # Lấy tên hình ảnh hiện tại của cả IR và Thermal
    ir_image_name_file = ir_image_list[current_index]
    thermal_image_name_file = thermal_image_list[current_index]

    # Đọc hình ảnh
    ir_image_path = os.path.join(ir_data_dir, ir_image_name_file)
    thermal_image_path = os.path.join(thermal_data_dir, thermal_image_name_file)

    # đường dẫn cho file hình ảnh combine
    file_numberID = ir_image_list[current_index].split("_")[3]
    combine_image_file_dir = os.path.join(overlap_dir, f"Overlape_Image_{folder_number}_{file_numberID}")
    # print(combine_image_file_dir)    "./Selected_data_images\Affected_Heat_Source\Data_Image_6\Overlap_Data_Image_6\Overlape_Image_6_2325.jpg"
    # # Mở hình ảnh lên 
    ir_image_pil = Image.open(ir_image_path)
    thermal_image_pil = Image.open(thermal_image_path)
    
    # Điều chỉnh giá trị để tăng độ sáng
    ir_image_pil = ImageEnhance.Brightness(ir_image_pil).enhance(brightness_factor)
    # Điều chỉnh giá trị để tăng độ tương phản
    ir_image_pil = ImageEnhance.Contrast(ir_image_pil).enhance(contrast_factor)

    #giảm opacity ảnh thermal
    thermal_image_pil.putalpha(round(alpha*255))
    ir_image_pil.paste(thermal_image_pil, (0,0), mask = thermal_image_pil)
    ir_image_array = np.array(ir_image_pil)
    img_combined = cv2.cvtColor(ir_image_array, cv2.COLOR_BGRA2RGBA)

    cv2.imshow("Combine_image_with_ovelap",img_combined)
    cv2.imwrite(combine_image_file_dir, img_combined)
    # Waits for a keystroke
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

# Destroys all the windows created
cv2.destroyAllwindows() 

