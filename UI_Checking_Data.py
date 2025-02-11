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
        self.uic.Browse.clicked.connect(self.link_to_folder)
        self.uic.Next_image.clicked.connect(self.next_image)
        self.uic.Back_image.clicked.connect(self.back_image)
        self.uic.Delete_image.clicked.connect(self.delete_image)

        # khai báo các biến 
        self.alpha = 1
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
        # self.overlape_image()


    def update_list_image_and_label(self):
        # Chỉ cần lấy một file ảnh từ thư mục RGB, IR, hoặc labels
        options = QFileDialog.Options()
        rgb_image_path = QFileDialog.getOpenFileName(self, "Select RGB Image", "", "Image Files (*.jpg *.png);;All Files (*)", options=options)[0]
        
        if not rgb_image_path:
            print("No image selected!")
            return

        # Lấy thông tin thư mục con (train, test, etc.) và tên file từ đường dẫn ảnh RGB
        subfolder_name = rgb_image_path.split(os.sep)[-2]  # Ví dụ: 'train'
        rgb_filename = os.path.basename(rgb_image_path)  # Ví dụ: '11_10_normal.jpg'

        # Tạo đường dẫn đến các file IR và label tương ứng
        ir_image_path = rgb_image_path.replace("RGBimages", "IRimages")
        label_image_path = rgb_image_path.replace("RGBimages", "labels").replace(".jpg", ".txt")
        
        # In ra các đường dẫn để kiểm tra
        print("IR Image Path:", ir_image_path)
        print("Label Image Path:", label_image_path)
        
        # Thêm vào danh sách các file
        self.ir_image_list = [ir_image_path]
        self.rgb_image_list = [rgb_image_path]
        self.label_list = [label_image_path]


    def display_image_to_label(self):
        # Duyệt qua tất cả ảnh IR và RGB và file label
        for ir_image_path, rgb_image_path, label_path in zip(self.ir_image_list, self.rgb_image_list, self.label_list):
            # Hiển thị ảnh IR và RGB
            self.uic.IR_image.setPixmap(QPixmap(ir_image_path))  # Hiển thị ảnh IR
            self.uic.RGB_image.setPixmap(QPixmap(rgb_image_path))  # Hiển thị ảnh RGB

            # Hiển thị tên file
            ir_image_name = os.path.basename(ir_image_path)
            self.uic.Name_file.setText(f"Image: {ir_image_name}")

            # Chồng ảnh và vẽ bounding box từ file label
            # self.overlape_image(ir_image_path, rgb_image_path, label_path)

    def link_to_folder(self):
        # Tìm thư mục lớn
        options = QFileDialog.Options()
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder", options=options)
        self.uic.folder_path.setText(folder_path)

        # Khởi tạo các thư mục con
        self.ir_data_dir = os.path.join(folder_path, 'IRimages')
        self.rgb_data_dir = os.path.join(folder_path, 'RGBimages')
        self.label_data_dir = os.path.join(folder_path, 'labels')

        # Kiểm tra nếu thư mục con có tồn tại
        if not (os.path.exists(self.ir_data_dir) and os.path.exists(self.rgb_data_dir) and os.path.exists(self.label_data_dir)):
            print("Missing one of the required directories (IRimages, RGBimages, labels).")
            return

        # Cập nhật danh sách ảnh và nhãn
        self.update_list_image_and_label()

        # Hiển thị ảnh đầu tiên
        # self.display_image_to_label()



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
        if self.current_index == (len(self.ir_image_list) -1):
            self.current_index = 0
        self.update_list_image()
        self.display_image_to_label()
        # self.overlape_image()



    def overlape_image(self, ir_image_path, rgb_image_path, label_path):
            # Mở ảnh IR và RGB
        ir_image_pil = Image.open(ir_image_path)
        rgb_image_pil = Image.open(rgb_image_path)

        # Đọc file label và vẽ bounding box lên ảnh
        with open(label_path, 'r') as label_file:
            lines = label_file.readlines()

        # Chuyển ảnh RGB thành mảng numpy
        rgb_image_array = np.array(rgb_image_pil)
        height, width, channels = rgb_image_array.shape

        # Vẽ bounding box từ file label
        for line in lines:
            class_id, x_center, y_center, box_width, box_height = map(float, line.strip().split())
            x_center = int(x_center * width)
            y_center = int(y_center * height)
            box_width = int(box_width * width)
            box_height = int(box_height * height)

            x_min = x_center - box_width // 2
            y_min = y_center - box_height // 2
            x_max = x_center + box_width // 2
            y_max = y_center + box_height // 2

            # Vẽ bounding box (màu xanh lá)
            rgb_image_array = cv2.rectangle(rgb_image_array, (x_min, y_min), (x_max, y_max), (0, 255, 0), 1)

        # Chuyển đổi lại thành ảnh để hiển thị
        rgb_image = cv2.cvtColor(rgb_image_array, cv2.COLOR_BGR2RGB)
        height, width, channels = rgb_image.shape
        bytes_per_line = channels * width
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, width, height, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(width * 2, height * 2, Qt.KeepAspectRatio)
        self.uic.Overlape_image.setPixmap(QPixmap.fromImage(p))

        
if __name__ == "__main__":
    # run app
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())