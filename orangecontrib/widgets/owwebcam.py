from Orange.widgets.widget import OWWidget
from Orange.widgets import gui
from PyQt5.QtWidgets import QLabel, QPushButton, QVBoxLayout
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QTimer
import numpy as np

try:
    from orangecontrib.utils import webcam
except ImportError:
    webcam = None

class OWWebcam(OWWidget):
    name = "Webcam Viewer"
    description = "웹캠을 실시간으로 표시하는 위젯"
    icon = "icons/category.svg"
    priority = 30

    def __init__(self):
        super().__init__()

        self.image_label = QLabel("웹캠이 시작되지 않았습니다.")
        self.controlArea.layout().addWidget(self.image_label)

        self.start_button = QPushButton("웹캠 시작")
        self.stop_button = QPushButton("중지")

        self.controlArea.layout().addWidget(self.start_button)
        self.controlArea.layout().addWidget(self.stop_button)

        self.start_button.clicked.connect(self.start_webcam)
        self.stop_button.clicked.connect(self.stop_webcam)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

    def start_webcam(self):
        if webcam:
            webcam.start_camera()
            self.timer.start(30)  # 약 30 FPS

    def stop_webcam(self):
        self.timer.stop()
        if webcam:
            webcam.stop_camera()
        self.image_label.setText("웹캠이 중지되었습니다.")

    def update_frame(self):
        if not webcam:
            return
        frame = webcam.read_frame()
        if frame is None:
            return
        frame = cvt_frame_to_qimage(frame)
        pixmap = QPixmap.fromImage(frame)
        self.image_label.setPixmap(pixmap)


def cvt_frame_to_qimage(frame):
    h, w, ch = frame.shape
    bytes_per_line = ch * w
    image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_BGR888)
    return image