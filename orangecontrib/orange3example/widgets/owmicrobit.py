from Orange.widgets.widget import OWWidget, Input, Output
from Orange.widgets import get_distribution
import Orange.data

from PyQt5.QtWidgets import QTextEdit, QPushButton, QComboBox, QLabel, QHBoxLayout, QWidget
from orangecontrib.orange3example.utils import microbit


class OWMicrobit(OWWidget):
    name = "Microbit Communicator"
    description = "통신 포트를 통해 마이크로비트와 데이터를 주고받는 위젯"
    icon = "../icons/machine-learning-03-svgrepo-com.svg"
    priority = 20

    class Inputs:
        text_data = Input("입력 텍스트", Orange.data.Table)

    class Outputs:
        received_data = Output("수신 데이터", Orange.data.Table)

    def __init__(self):
        super().__init__()

        self.text_data = None
        self.received_text = ""

        # 포트 선택 UI
        port_layout = QHBoxLayout()
        port_widget = QWidget()
        port_widget.setLayout(port_layout)

        self.port_combo = QComboBox()
        self.port_combo.setEditable(True)
        port_layout.addWidget(self.port_combo)

        self.refresh_button = QPushButton("🔄")
        self.refresh_button.clicked.connect(self.refresh_ports)
        port_layout.addWidget(self.refresh_button)

        self.connect_button = QPushButton("연결")
        self.connect_button.clicked.connect(self.connect_to_microbit)
        port_layout.addWidget(self.connect_button)

        self.status_label = QLabel("연결되지 않음")
        port_layout.addWidget(self.status_label)

        self.controlArea.layout().addWidget(port_widget)

        # 전송 텍스트 입력
        self.send_box = QTextEdit()
        self.send_box.setPlaceholderText("마이크로비트로 보낼 텍스트를 입력하세요")
        self.controlArea.layout().addWidget(self.send_box)

        self.send_button = QPushButton("전송")
        self.send_button.clicked.connect(self.send_to_microbit)
        self.controlArea.layout().addWidget(self.send_button)

        # 수신 텍스트 표시
        self.receive_box = QTextEdit()
        self.receive_box.setReadOnly(True)
        self.mainArea.layout().addWidget(self.receive_box)

        # 로그 출력창
        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)
        self.controlArea.layout().addWidget(self.log_box)

        # 초기 포트 목록 로드
        self.refresh_ports()

    def log(self, text):
        self.log_box.append(text)

    def refresh_ports(self):
        self.port_combo.clear()
        self.log("🔄 포트 새로고침 중...")
        if microbit:
            try:
                ports = microbit.list_ports()
                if ports:
                    self.port_combo.addItems(ports)
                    self.log(f"사용 가능한 포트: {', '.join(ports)}")
                else:
                    self.log("사용 가능한 포트가 없습니다.")
            except Exception as e:
                self.log(f"포트 검색 실패: {str(e)}")
        else:
            self.log("microbit 모듈이 로드되지 않았습니다.")

    def connect_to_microbit(self):
        if not microbit:
            self.status_label.setText("microbit 모듈 없음")
            self.log("microbit 모듈이 없습니다.")
            return

        port = self.port_combo.currentText()
        try:
            microbit.connect(port)
            self.status_label.setText(f"연결됨 ({port})")
            self.log(f"{port} 포트에 연결되었습니다.")
        except Exception as e:
            self.status_label.setText(f"연결 실패")
            self.log(f"연결 실패: {str(e)}")

    @Inputs.text_data
    def set_text_data(self, data):
        if isinstance(data, Orange.data.Table):
            self.text_data = data
            try:
                text = str(data[0][0])
                self.log(f"입력 데이터를 수신했습니다: {text}")
                self.send_text_to_microbit(text)  # 자동 전송
            except Exception as e:
                self.log(f"입력 텍스트 추출 실패: {e}")

    def send_text_to_microbit(self, text: str):
        if not text:
            self.receive_box.setPlainText("전송할 텍스트가 없습니다.")
            self.log("전송할 텍스트가 없습니다.")
            return

        if not microbit:
            self.receive_box.setPlainText("[Error] microbit 모듈이 없습니다.")
            self.log("microbit 모듈이 없습니다.")
            return

        if not microbit.is_connected():
            self.receive_box.setPlainText("먼저 포트를 연결하세요.")
            self.log("포트가 연결되지 않았습니다.")
            return

        try:
            response = microbit.send_and_receive(text)
            self.receive_box.setPlainText(response)

            domain = Orange.data.Domain([], metas=[Orange.data.StringVariable("Received")])
            out_table = Orange.data.Table(domain, [[response]])
            self.Outputs.received_data.send(out_table)

            self.log(f"보냄: {text}")
            self.log(f"수신: {response}")
        except Exception as e:
            self.receive_box.setPlainText(f"[Error] {str(e)}")
            self.log(f"전송 중 오류 발생: {str(e)}")

    def send_to_microbit(self):
        text = self.send_box.toPlainText().strip()
        self.send_text_to_microbit(text)
