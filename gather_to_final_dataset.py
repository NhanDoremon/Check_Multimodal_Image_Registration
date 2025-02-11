###python gather_to_final_dataset.py

import os
import shutil



# Đường dẫn tới thư mục gốc (Datasets)
orginal_dir = '.'
root_dir = './Selected_data_images'

# tạo các đường dẫn 
Gathered_Dataset_dir = os.path.join(orginal_dir, 'Gathered_Dataset')
Ir_data_dir = os.path.join(Gathered_Dataset_dir, 'IR_Data_Image')
Thermal_data_dir = os.path.join(Gathered_Dataset_dir, 'Thermal_Data_Image')
Label_dir = os.path.join(Gathered_Dataset_dir, 'Label_Data_Image')

# tạo các thư mục cần thiết
if not os.path.exists(Gathered_Dataset_dir):
    os.makedirs(Gathered_Dataset_dir)
if not os.path.exists(Ir_data_dir):
    os.makedirs(Ir_data_dir)
if not os.path.exists(Thermal_data_dir):
    os.makedirs(Thermal_data_dir)
if not os.path.exists(Label_dir):
    os.makedirs(Label_dir)

for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file.startswith("IR_Image_"):
            root_file_path = os.path.join(root, file)
            des_file_path = Ir_data_dir
            shutil.copy(root_file_path, des_file_path)
        elif file.startswith("Thermal_Image_"):
            root_file_path = os.path.join(root, file)
            des_file_path = Thermal_data_dir
            shutil.copy(root_file_path, des_file_path)
        elif file.startswith("Label_Image_") and file.lower().endswith(".txt"):
            root_file_path = os.path.join(root, file)
            des_file_path = Label_dir
            shutil.copy(root_file_path, des_file_path)
