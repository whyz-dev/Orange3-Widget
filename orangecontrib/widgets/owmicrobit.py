from Orange.widgets.widget import OWWidget, Input, Output
from Orange.widgets import gui
from PyQt5.QtWidgets import QTextEdit, QPushButton, QComboBox, QLabel, QHBoxLayout, QWidget
import Orange.data

try:
    from orangecontrib.llm_transformer.utils import microbit
except ImportError:
    microbit = None


class OWMicrobit(OWWidget):
    name = "Microbit Communicator"
    description = "통신 포트를 통해 마이크로비트와 데이터를 주고받는 위젯"
    icon = "icons/category.svg"
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
        self.refresh_ports()
        port_layout.addWidget(self.port_combo)

        self.refresh_button = QPushButton("🔄")
        self.refresh_button.clicked.connect(self.refresh_ports)
        port_layout.addWidget(self.refresh_button)

        self.connect_button = QPushButton("연결")
        self.connect_button.clicked.connect(self.connect_to_microbit)
        port_layout.addWidget(self.connect_button)

        self.status_label = QLabel("❌ 연결되지 않음")
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

    def refresh_ports(self):
        self.port_combo.clear()
        if microbit:
            ports = microbit.list_ports()
            self.port_combo.addItems(ports)

    def connect_to_microbit(self):
        if not microbit:
            self.status_label.setText("❌ microbit 모듈 없음")
            return

        port = self.port_combo.currentText()
        try:
            microbit.connect(port)
            self.status_label.setText(f"✅ 연결됨 ({port})")
        except Exception as e:
            self.status_label.setText(f"❌ 연결 실패: {e}")

    @Inputs.text_data
    def set_text_data(self, data):
        if isinstance(data, Orange.data.Table):
            self.text_data = data

    def send_to_microbit(self):
        text = self.send_box.toPlainText().strip()
        if not text:
            self.receive_box.setPlainText("전송할 텍스트가 없습니다.")
            return

        if microbit:
            try:
                if not microbit.is_connected():
                    self.receive_box.setPlainText("❌ 먼저 포트를 연결하세요.")
                    return
                response = microbit.send_and_receive(text)
                self.receive_box.setPlainText(response)

                domain = Orange.data.Domain([], metas=[Orange.data.StringVariable("Received")])
                out_table = Orange.data.Table(domain, [[response]])
                self.Outputs.received_data.send(out_table)
            except Exception as e:
                self.receive_box.setPlainText(f"[Error] {str(e)}")
        else:
            self.receive_box.setPlainText("[Error] microbit 모듈이 없습니다.")