from openai import OpenAI


class LLM:
    """GPT API를 호출하는 클래스"""

    def __init__(self, api_key):
        self.openai_client = OpenAI(api_key=api_key)

    def get_response(self, prompt, data_list):
        """GPT의 응답을 받아서 그대로 반환"""
        results = []

        for data in data_list:
            try:
                response = self.openai_client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": prompt},
                        {"role": "user", "content": str(data)},
                    ],
                    temperature=0,
                )
                results.append(response.choices[0].message.content.strip())

            except Exception as e:
                results.append(f"Error: {str(e)}")  # 오류 발생 시 메시지 추가

        return results
