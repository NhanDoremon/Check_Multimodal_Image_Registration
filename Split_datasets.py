# python Split_datasets.py
import os
import shutil
import random

# Đường dẫn tới thư mục gốc (Datasets)
data_dir = './Gathered_Dataset'

# Tạo thư mục mới (MyDatasets)
new_data_dir = 'MyDatasets'
if not os.path.exists(new_data_dir):
    os.makedirs(new_data_dir, exist_ok=True)

# Tạo thư mục train, valid và test trong thư mục MyDatasets
train_dir = os.path.join(new_data_dir, 'Train')
train_IR_image_dir = os.path.join(new_data_dir, 'Train', 'IR_Data_Image' )
train_themal_image_dir = os.path.join(new_data_dir, 'Train', 'Thermal_Data_Image' )
train_labels = os.path.join(new_data_dir, 'Train', 'Label_Data_Image' )

valid_dir = os.path.join(new_data_dir, 'Valid')
valid_IR_image_dir = os.path.join(new_data_dir, 'Valid', 'IR_Data_Image' )
valid_themal_image_dir = os.path.join(new_data_dir, 'Valid', 'Thermal_Data_Image' )
valid_labels_dir = os.path.join(new_data_dir, 'Valid', 'Label_Data_Image' )

test_dir = os.path.join(new_data_dir, 'Test')
test_IR_image_dir = os.path.join(new_data_dir, 'Test', 'IR_Data_Image' )
test_themal_image_dir = os.path.join(new_data_dir, 'Test', 'Thermal_Data_Image' )
test_labels_dir = os.path.join(new_data_dir, 'Test', 'Label_Data_Image' )



os.makedirs(train_dir, exist_ok=True)
os.makedirs(train_IR_image_dir, exist_ok=True)
os.makedirs(train_themal_image_dir, exist_ok=True)
os.makedirs(train_labels, exist_ok=True)

os.makedirs(valid_dir, exist_ok=True)
os.makedirs(valid_IR_image_dir, exist_ok=True)
os.makedirs(valid_themal_image_dir, exist_ok=True)
os.makedirs(valid_labels_dir, exist_ok=True)


os.makedirs(test_dir, exist_ok=True)
os.makedirs(test_IR_image_dir, exist_ok=True)
os.makedirs(test_themal_image_dir, exist_ok=True)
os.makedirs(test_labels_dir, exist_ok=True)



# Danh sách tên các thư mục (IR_Data_Image và Thermal_Data_Image và Labels)
subfolders = [f.name for f in os.scandir(data_dir) if f.is_dir()]
if "Overlap_Data_Image_10" in subfolders:
    subfolders.remove("Overlap_Data_Image_10")
# print (subfolders) #Ex: ['IR_Data_Image_10', 'Label_Data_Image_10', 'Thermal_Data_Image_10']
# Lấy danh sách tất cả các file trong thư mục con IR_Data_Image
files = os.listdir(os.path.join(data_dir, subfolders[0]))
random.shuffle(files)

# Tính toán số lượng file trong mỗi thư mục train, valid và test
num_files = len(files)
num_train = int(num_files * 0.6)
num_valid = int(num_files * 0.2)

# Phân chia các file vào các thư mục train, valid và test
for i, file in enumerate(files):
    number_folder = os.path.basename(file).split("_")[2].split(".")[0]
    image_number = file.split("_")[3].split(".")[0] # Lấy số thứ tự hình ảnh
    ir_path = os.path.join(data_dir, subfolders[0], file)
    thermal_image = f"Thermal_Image_{number_folder}_{image_number}.jpg"
    label_image = f"Label_Image_{number_folder}_{image_number}.txt"
    # print(image_number)
    # print(number_folder)
    # print(file)
    # print (os.path.join(train_dir, thermal_image))

    thermal_path = os.path.join(data_dir, subfolders[2], thermal_image)
    label_path = os.path.join(data_dir, subfolders[1], label_image)
    
    # print ("label_path",label_path)
    # print ("train_labels",train_labels)
    if i < num_train:
        # dst_train = os.path.join(train_dir, thermal_image)
        shutil.copy(ir_path, train_IR_image_dir)
        shutil.copy(thermal_path, train_themal_image_dir)
        shutil.copy(label_path, train_labels)
    elif i < num_train + num_valid:
        # dst_valid = os.path.join(valid_dir, thermal_image)
        shutil.copy(ir_path, valid_dir)
        shutil.copy(thermal_path, valid_themal_image_dir)
        shutil.copy(label_path, valid_labels_dir)
    else:
        # dst_test = os.path.join(test_dir, thermal_image)
        shutil.copy(ir_path, test_IR_image_dir)
        shutil.copy(thermal_path, test_themal_image_dir)
        shutil.copy(label_path, test_labels_dir)


    # if i < num_train:
    #     dst_train = os.path.join(train_dir, thermal_image)
    #     dst_valid = os.path.join(valid_dir, thermal_image)
    #     dst_test = os.path.join(test_dir, thermal_image)
    # elif i < num_train + num_valid:
    #     dst_train = os.path.join(train_dir, thermal_image)
    #     dst_valid = os.path.join(valid_dir, thermal_image)
    #     dst_test = os.path.join(test_dir, thermal_image)
    # else:
    #     dst_train = os.path.join(train_dir, thermal_image)
    #     dst_valid = os.path.join(valid_dir, thermal_image)
    #     dst_test = os.path.join(test_dir, thermal_image)

    # # Copy tập hình ảnh từ image_path vừa tải lên qua dst_train/valid/test
    # shutil.copy(image_path, dst_train)
    # shutil.copy(image_path, dst_valid)
    # shutil.copy(image_path, dst_test)

    # # Copy tập tin Thermal_Data_Image
    # thermal_path = os.path.join(data_dir, subdirs[1], thermal_image)
    # # print("thermal_path",thermal_path)
    # shutil.copy(thermal_path, dst_train)
    # shutil.copy(thermal_path, dst_valid)
    # shutil.copy(thermal_path, dst_test)

    # # Copy tập tin Label_Data_Image
    # label_path = os.path.join(data_dir, subdirs[2], label_image)
    # # print("label_path",label_path)
    # shutil.copy(label_path, dst_train)
    # shutil.copy(label_path, dst_valid)
    # shutil.copy(label_path, dst_test)

