### Rountine when start this code
### pyuic5 -x Data_checking.ui -o Data_checking.py
### python UI_checking_data.py
import sys
import os
import cv2
import numpy as np
from PIL import Image
# pip install pyqt5, pip install pyqt5 tools
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import  Qt
# just change the name
from Data_checking import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # the way app working
        self.uic = Ui_MainWindow()
        self.uic.setupUi(self)
        self.uic.Opacity_slide.valueChanged.connect(self.adjust_opacity)
        self.uic.Zoom_slide.valueChanged.connect(self.adjust_zoom)
        self.uic.Browse.clicked.connect(self.link_to_folder)
        self.uic.Next_image.clicked.connect(self.next_image)
        self.uic.Back_image.clicked.connect(self.back_image)
        self.uic.Delete_image.clicked.connect(self.delete_image)

        # khai báo các biến 
        self.alpha = 1
        self.zoom_value = 0
        self.current_index = 0
        self.ir_image_list = []
        self.thermal_image_list = []
        self.ir_image_path = []
        self.thermal_image_path = []
        self.label_list = []
        self.label_path = []

    def keyPressEvent(self, event):
        if event.key() == ord('A') or event.key() == ord('a'):
            self.back_image()
        elif event.key() == ord('D') or event.key() == ord('d'):
            self.next_image()
    def adjust_opacity(self,value):

        # Giảm 50% opacity của ảnh Thermal
        self.alpha = value/100
        self.overlape_image()
    
    def adjust_zoom(self,value):
        # Giảm 50% opacity của ảnh Thermal
        self.zoom_value = value/100
        self.overlape_image()


        # Chồng ảnh Thermal lên ảnh IR
    def update_list_image(self):
        self.ir_image_list = os.listdir(self.ir_data_dir)
        self.thermal_image_list = os.listdir(self.thermal_data_dir)
        
        # print(self.ir_image_list)  ## lấy tên file:  Thermal_Image_10_1000.jpg

        # # # Sắp xếp danh sách hình ảnh theo thứ tự số trong tên file
        # self.ir_image_list.sort(key=lambda x: (int(x.split("_")[2]), int(x.split("_")[3].split(".")[0])))
        # self.thermal_image_list.sort(key=lambda x: (int(x.split("_")[2]), int(x.split("_")[3].split(".")[0])))

        # print(self.thermal_image_list[0])  ## lấy tên file:  SẮP XẾP LẠI THEO TRẬT TỰ TĂNG DẦN Thermal_Image_1_0.jpg

    
    # def update_list_label(self):
    #     self.label_list = os.listdir(self.label_data_dir)
    # #     self.label_list = self.label_list [1:] # bỏ cái file classes ở phía khúc đầu đi
        
    # #     print(self.label_list[0]) 


    def link_to_folder(self):
        # find the link
        options = QFileDialog.Options() # thiết lập các tùy chọn cho hộp thoại
        options |= QFileDialog.ShowDirsOnly #chỉ hiển thị các thư mục (folder) trong hộp thoại chọn file
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder", options=options) #để hiển thị hộp thoại và cho phép người dùng chọn một folder bất kỳ
        self.uic.folder_path.setText(folder_path)

        # # Lặp qua tất cả các tệp và thư mục trong thư mục Data_image_1
        # for root, dirs, files in os.walk(folder_path):
        #     for dir_name in dirs:
        #         # Kiểm tra nếu tên của folder con bắt đầu bằng "IR", gán đường dẫn của nó cho biến A
        #         if dir_name.startswith("IR_Data_Image"):
        #             self.ir_data_dir = os.path.join(root, dir_name)
        #         # Kiểm tra nếu tên của folder con bắt đầu bằng "Thermal", gán đường dẫn của nó cho biến B
        #         elif dir_name.startswith("Thermal_Data_Image"):
        #             self.thermal_data_dir = os.path.join(root, dir_name)
        #         elif dir_name.startswith("Label_Data_Image"):
        #             self.label_data_dir = os.path.join(root, dir_name)

        # # Khởi tạo các thư mục con
        self.ir_data_dir = os.path.join(folder_path, 'RGBimages')
        self.thermal_data_dir = os.path.join(folder_path, 'IRimages')
        self.label_data_dir = os.path.join(folder_path, 'labels')

        # print (self.rgb_data_dir) 
        # D:/ALL PROJECTS/Dong_Brother_Ben_Tre/IR_Thermal_Fusion_Humae_Detection/Checking_Datasets/Gathered_Dataset\IR_Data_Image
                    
        self.update_list_image()    
        # self.update_list_label()
        # Bộ đếm chỉ số hình ảnh đang hiển thị
        self.current_index = 0

        # mở hình ảnh đầu tiên và show lên label
        self.display_image_to_label()

    def next_image(self):
        self.current_index += 1
        if self.current_index >= len(self.ir_image_list) or self.current_index >= len(self.thermal_image_list):
            self.current_index = 0
        self.display_image_to_label()
    def back_image(self):
        self.current_index -= 1
        if self.current_index < 0  or self.current_index < 0:
            self.current_index = len(self.ir_image_list) - 1
        self.display_image_to_label() 
    
    def delete_image(self):
        # print("delete IR image",os.path.join(self.ir_data_dir, self.ir_image_list[self.current_index]))
        # print("delete Thermal image",os.path.join(self.thermal_data_dir, self.thermal_image_list[self.current_index]))
        os.remove(os.path.join(self.ir_data_dir, self.ir_image_list[self.current_index]))
        os.remove(os.path.join(self.thermal_data_dir, self.thermal_image_list[self.current_index]))
        ir_image_name_file = os.path.join(self.ir_data_dir, self.ir_image_list[self.current_index])
        label_name_file = os.path.basename(ir_image_name_file).replace('IRimages', 'labels').replace('.jpg', '.txt')
        os.remove(os.path.join(self.label_data_dir, label_name_file))

        if self.current_index == (len(self.ir_image_list) -1):
            self.current_index = 0
        self.update_list_image()
        self.display_image_to_label()
        self.overlape_image()
    def display_image_to_label(self):
        # Lấy tên hình ảnh hiện tại của cả IR và Thermal
        ir_image_name_file = self.ir_image_list[self.current_index]
        # print (ir_image_name_file)
        thermal_image_name_file = self.thermal_image_list[self.current_index]

        # # Đọc hình ảnh
        ir_image_path = os.path.join(self.ir_data_dir, ir_image_name_file)
        thermal_image_path = os.path.join(self.thermal_data_dir, thermal_image_name_file)

        print ("thermal_image_path",thermal_image_path)

        # # Hiển thị tên file ảnh hiện tại
        # current_ir_type = ir_image_name_file.split("_")[0]
        # current_ir_folder = ir_image_name_file.split("_")[2]
        # current_ir_image_number = ir_image_name_file.split("_")[3].split(".")[0]

        # current_thermal_type = thermal_image_name_file.split("_")[0]
        # current_thermal_folder = thermal_image_name_file.split("_")[2]
        # current_thermal_image_number = thermal_image_name_file.split("_")[3].split(".")[0]

        if os.path.exists(thermal_image_path):
            self.uic.Thermal_image.setPixmap(QPixmap(thermal_image_path))
        else:
            print("Thermal image not found!")

        # Lấy kích thước widget
        widget_width = self.uic.Thermal_image.width()
        widget_height = self.uic.Thermal_image.height()
        print(f"IR Image: {os.path.basename(ir_image_path)}, Thermal Image: {os.path.basename(thermal_image_path)}") #IR Image: IR_Image_6_380, Thermal Image: Thermal_Image_6_380
        self.uic.Thermal_image.setPixmap(QPixmap(thermal_image_path).scaled(widget_width, widget_height, QtCore.Qt.KeepAspectRatio))
        self.uic.IR_image.setPixmap(QPixmap(ir_image_path).scaled(widget_width, widget_height, QtCore.Qt.KeepAspectRatio))
        self.uic.Name_file.setAlignment(QtCore.Qt.AlignCenter)
        self.uic.Name_file.setText(f"Image_{ir_image_name_file}")
        self.overlape_image()


    def overlape_image(self):
        # Lấy tên hình ảnh hiện tại của cả IR và Thermal
        ir_image_name_file = self.ir_image_list[self.current_index]
        thermal_image_name_file = self.thermal_image_list[self.current_index]

        # Lấy tên file label hiện tại
        label_name_file = os.path.basename(ir_image_name_file).replace('IRimages', 'labels').replace('.jpg', '.txt')

        # Đọc hình ảnh
        ir_image_path = os.path.join(self.ir_data_dir, ir_image_name_file)
        thermal_image_path = os.path.join(self.thermal_data_dir, thermal_image_name_file)

        # Đọc file label
        label_file_path = os.path.join(self.label_data_dir, label_name_file)
        print("label_file_path:", os.path.basename(label_file_path))

        ir_image_pil = Image.open(ir_image_path)
        thermal_image_pil = Image.open(thermal_image_path)

        # Điều chỉnh opacity của ảnh Thermal
        thermal_image_pil.putalpha(round(self.alpha * 255))

        # Chồng ảnh Thermal lên ảnh IR
        ir_image_pil.paste(thermal_image_pil, (0, 0), mask=thermal_image_pil)
        ir_image_array = np.array(ir_image_pil)
        ir_image = cv2.cvtColor(ir_image_array, cv2.COLOR_RGBA2BGRA)
        img_combined = ir_image
        rgb_image = cv2.cvtColor(img_combined, cv2.COLOR_BGRA2RGBA)

        height, width, channel = rgb_image.shape

        # Khởi tạo giá trị mặc định cho zoom_factor
        zoom_factor = 1.0
        crop_start_x, crop_start_y = 0, 0

        # Thực hiện zoom nếu self.zoom_value được thiết lập
        if hasattr(self, "zoom_value") and 0.0 < self.zoom_value <= 1.0:
            zoom_factor = 1 + self.zoom_value  # Tính hệ số zoom (ví dụ: 1.5 khi zoom_value = 0.5)
            new_width = int(width * zoom_factor)
            new_height = int(height * zoom_factor)

            # Resize ảnh với zoom_factor
            resized_image = cv2.resize(rgb_image, (new_width, new_height), interpolation=cv2.INTER_LINEAR)

            # Cắt ảnh về kích thước ban đầu (crop từ trung tâm)
            crop_start_x = (new_width - width) // 2
            crop_start_y = (new_height - height) // 2
            rgb_image = resized_image[crop_start_y:crop_start_y + height, crop_start_x:crop_start_x + width]

        # Vẽ bounding box sau khi điều chỉnh tọa độ
        with open(label_file_path, 'r') as label_file:
            lines = label_file.readlines()

        for line in lines:
            class_id, x_center, y_center, box_width, box_height = map(float, line.strip().split())

            # Tọa độ gốc trên ảnh ban đầu
            x_center *= width
            y_center *= height
            box_width *= width
            box_height *= height

            # Điều chỉnh tọa độ bounding box sau khi zoom
            x_center = (x_center * zoom_factor) - crop_start_x
            y_center = (y_center * zoom_factor) - crop_start_y
            box_width *= zoom_factor
            box_height *= zoom_factor

            # Tính toán tọa độ góc bounding box
            x_min = int(x_center - box_width // 2)
            y_min = int(y_center - box_height // 2)
            x_max = int(x_center + box_width // 2)
            y_max = int(y_center + box_height // 2)

            # Vẽ bounding box lên ảnh
            color = (0, 255, 0)  # Green color for bounding boxes
            thickness = 1

            rgb_image = cv2.rectangle(rgb_image, (x_min, y_min), (x_max, y_max), color, thickness)

        # Hiển thị ảnh với Qt
        rgb_image_bytes = rgb_image.tobytes()  # Chuyển đổi mảng numpy sang bytes
        bytes_per_line = channel * width
        convert_to_Qt_format = QtGui.QImage(rgb_image_bytes, width, height, bytes_per_line, QtGui.QImage.Format_RGBA8888)
        p = convert_to_Qt_format.scaled(width * 2, height * 2, Qt.KeepAspectRatio)
        self.uic.Overlape_image.setPixmap(QPixmap.fromImage(p))




        
if __name__ == "__main__":
    # run app
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())