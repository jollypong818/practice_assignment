"""Day26 HTML의 세 문서와 다섯 질문. 파일을 다시 읽어 입력 변경을 격리합니다."""
from coursekit.io import load_json

def load_hits():
    return load_json("lecture_hits.json")

def example_hit():
    return load_hits()[0]

def load_questions():
    return load_json("questions.json")
