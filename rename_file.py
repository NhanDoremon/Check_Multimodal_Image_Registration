### python rename_file.py

import os

def rename_files_in_directory(directory_path):
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.startswith("Overlape_Image_"):
                new_file_name = file.replace("Overlape_Image_", "Label_Image_", 1)
                old_file_path = os.path.join(root, file)
                new_file_path = os.path.join(root, new_file_name)
                os.rename(old_file_path, new_file_path)
                print(f"Renamed: {old_file_path} -> {new_file_path}")

# Đường dẫn đến thư mục cha
parent_directory = "./Selected_data_images/Less_Smoke/Far/Overlap/Data_Image_15"
# "./Selected_data_images/Affected_Heat_Source/Data_Image_6"
# "./Selected_data_images/Darkness/Data_Image_5"
# "./Selected_data_images/Darkness/Data_Image_7"
# "./Selected_data_images/Dense_Smoke/Data_Image_18"
# "./Selected_data_images/Less_Smoke/Far/Multi_person/Data_Image_1" #2 , 10 , 13
# "./Selected_data_images/Less_Smoke/Far/Overlap/Data_Image_11" #12 , 14 , 15
# "./Selected_data_images/Less_Smoke/Near/Data_Image_16" 
rename_files_in_directory(parent_directory)
