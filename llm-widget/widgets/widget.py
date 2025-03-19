from Orange.widgets.widget import OWWidget, Input, Output
from Orange.widgets import gui
import Orange.data
from PyQt5.QtWidgets import QTextEdit  # QtWidgets에서 QTextEdit 사용
from .llm import LLM  # llm.py에서 LLM 클래스를 가져옴


class LLMTransformerWidget(OWWidget):
    name = "LLM Transformer"
    description = "GPT API를 통해 입력 데이터를 변환하는 Orange3 위젯"
    icon = "icons/example.svg"
    priority = 10

    class Inputs:
        text_data = Input("입력 데이터", Orange.data.Table)

    class Outputs:
        transformed_data = Output("GPT 응답 데이터", list)

    def __init__(self):
        super().__init__()

        # API 키 입력 필드
        self.api_key = ""
        self.api_key_input = gui.lineEdit(
            self.controlArea, self, "api_key", label="API Key:"
        )

        # 프롬프트 입력 필드
        self.prompt = "입력 데이터를 변환해주세요."
        self.prompt_input = gui.lineEdit(
            self.controlArea, self, "prompt", label="Prompt:"
        )

        # 변환 실행 버튼
        self.transform_button = gui.button(
            self.controlArea, self, "변환 실행", callback=self.process
        )
        self.transform_button.setDisabled(True)  # 초기에는 비활성화

        # 🛠 결과 출력 필드 (QTextEdit 사용)
        self.result_text = ""
        self.result_display = QTextEdit()
        self.result_display.setReadOnly(True)  # 읽기 전용 설정
        self.mainArea.layout().addWidget(self.result_display)  # Orange3의 레이아웃에 추가

        self.text_data = None

    @Inputs.text_data
    def set_data(self, data):
        """Orange Table 데이터를 list[str]로 변환하여 저장 (Meta에서 `comment_text` 추출)"""
        print(f"📌 `set_data()` 실행됨 - 데이터 타입: {type(data)}")

        if data is None or len(data) == 0:
            print("❌ `set_data()`가 빈 데이터([])를 받았습니다. 기본 테스트 데이터를 넣습니다.")
            data = ["This is a test input sentence."]  # 기본 테스트 데이터
        else:
            if isinstance(data, Orange.data.Table):
                print(f"✅ Orange Table 확인됨 - 데이터 개수: {len(data)}")
                print(f"✅ Orange Table 컬럼 정보: {data.domain}")

                if "comment_text" in data.domain.metas:
                    meta_index = data.domain.index(
                        data.domain.metas["comment_text"]
                    )  # Meta 컬럼 인덱스
                    data = [str(row.metas[meta_index]) for row in data]

        self.text_data = data
        print(f"📌 최종 변환된 입력 데이터: {self.text_data[:5]} ...")  # 데이터 내용 확인
        self.transform_button.setDisabled(False)

    def process(self):
        """변환 실행 버튼을 눌렀을 때만 GPT API 호출"""
        if not self.text_data or not self.api_key.strip():
            self.result_text = "❌ API Key 또는 입력 데이터가 없습니다."
            self.result_display.setPlainText(self.result_text)
            return

        try:
            # GPT API 호출
            llm = LLM(self.api_key)
            results = llm.get_response(self.prompt, self.text_data)

            # 변환된 결과를 출력으로 보냄
            self.Outputs.transformed_data.send(results)
            self.result_text = "\n".join(results)

            # 🛠 결과 출력 UI 업데이트
            self.result_display.setPlainText(self.result_text)

        except Exception as e:
            self.result_text = f"❌ Error: {str(e)}"
            self.Outputs.transformed_data.send([])
            self.result_display.setPlainText(self.result_text)
