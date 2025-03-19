# from Orange.widgets.widget import OWWidget, Input, Output
# from Orange.widgets import gui
# import Orange.data
# import numpy as np

# class ExampleWidget(OWWidget):
#     name = "Example Widget"
#     description = "사용자 정의 Orange3 위젯"
#     priority = 10

#     class Inputs:
#         data = Input("입력 데이터", Orange.data.Table)

#     class Outputs:
#         transformed_data = Output("출력 데이터", Orange.data.Table)

#     def __init__(self):
#         super().__init__()
#         self.data = None
#         self.result = None

#         # UI 추가 (버튼 생성)
#         gui.button(self.controlArea, self, "데이터 변환", callback=self.process)

#     @Inputs.data
#     def set_data(self, data):
#         """입력 데이터를 설정하는 함수"""
#         self.data = data
#         self.process()

#     def process(self):
#         """데이터 변환 수행 (예: 모든 값 제곱)"""
#         if self.data:
#             domain = self.data.domain
#             X = self.data.X.copy()  # 데이터 복사 (원본 수정 방지)

#             # 모든 수치형 데이터를 제곱 (클래스 변수 제외)
#             X = np.square(X)

#             # 클래스 값 처리
#             if domain.class_var:
#                 Y = self.data.Y.copy()
#             else:
#                 Y = None  # 클래스 변수가 없을 경우

#             # 새로운 Orange3 데이터 생성
#             new_domain = Orange.data.Domain(domain.attributes, domain.class_var)
#             self.result = Orange.data.Table(new_domain, X, Y)

#             # 결과 출력
#             self.Outputs.transformed_data.send(self.result)
