from setuptools import setup, find_packages

setup(
    name="llm-widget",  # 플러그인 이름
    version="0.1",
    description="Orange3 LLM 기반 사용자 정의 위젯",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["Orange3", "OpenAI", "PyQT5"],
    entry_points={
        # 위젯 그룹 등록
        "orange.widgets": "LLMWidgets = widgets"
    },
)
