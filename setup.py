from setuptools import setup, find_packages

setup(
    # 애드온 이름
    name="Orange Widget",  
    version="0.1",
    # 애드온 설명
    description="Orange3 LLM 기반 사용자 정의 위젯입니다.",
    packages=find_packages(),
    include_package_data=True,
    # 위젯을 사용하기 위해 필요한 종속성 확인
    install_requires=["Orange3", "OpenAI", "PyQT5", "dotenv"],
    entry_points={
        # 위젯 그룹 등록
        # LLM Widgets라는 그룹에
        # llm_transformer.widgets 안에 있는 위젯이 자동으로 포함됩니다.
        "orange.widgets": [
            "Orange Widget = orangecontrib.widgets",
        ]
    },
)
