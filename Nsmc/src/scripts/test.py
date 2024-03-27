import os
import pandas as pd
import numpy as np
from pprint import pprint

def 평가시기구분():
    start = 0
    end = 0

    print(df.columns)

    for row, value in enumerate(df["평가시기"]):
        if value is not np.nan:
            if row > 0:
                end = row - 1
                rows.append((start, end))
                start = row
        elif (row + 1) == len(df["평가시기"]):
            rows.append((start, row))


def 성취기준처리(series):
    성취기준 = [x for x in series.to_list() if x is not np.nan]
    성취기준 = "".join(성취기준)
    성취기준 = 성취기준.replace("  ", " ")
    성취기준 = 성취기준.replace("] ", "]")
    성취기준 = 성취기준.replace("]", "] ")
    성취기준 = 성취기준.replace(". ", ".")
    성취기준 = [x.strip() + "." for x in 성취기준.split(".") if len(x) > 5]

    return 성취기준


def 영역명처리(성취기준_리스트):
    영역 = {
        "국": {
            "01": "듣기·말하기",
            "02": "읽기",
            "03": "쓰기",
            "04": "문법",
            "05": "문학",
            "06": "매체"
        },
        "수": {
            "01": "수와 연산",
            "02": "도형",
            "03": "측정",
            "04": "규칙성",
            "05": "자료와 가능성"
        },
        "사": {
            "01": "우리가 살아가는 곳",
            "02": "우리가 살아가는 모습",
            "03": "우리 지역의 어제와 오늘",
            "04": "다양한 삶의 모습과 변화"
        },
        "도": {
            "01": "자신과의 관계",
            "02": "타인과의 관계",
            "03": "사회·공동체와의 관계",
            "04": "자연·초월과의 관계"
        },
        "체": {
            "01": "건강",
            "02": "도전",
            "03": "경쟁",
            "04": "표현",
            "05": "안전",
        },
        "음": {
            "01": "표현",
            "02": "감상",
            "03": "생활화"
        },
        "미": {
            "01": "체험",
            "02": "표현",
            "03": "감상"
        },
        "영": {
            "01": "듣기",
            "02": "말하기",
            "03": "읽기",
            "04": "쓰기"
        },
        "바": {
            "01": "우리는 누구로 살아갈까",
            "02": "우리는 어디서 살아갈까",
            "03": "우리는 지금 어떻게 살아갈까",
            "04": "우리는 무엇을 하며 살아갈까"
        },
        "슬": {
            "01": "우리는 누구로 살아갈까",
            "02": "우리는 어디서 살아갈까",
            "03": "우리는 지금 어떻게 살아갈까",
            "04": "우리는 무엇을 하며 살아갈까"
        },
        "즐": {
            "01": "우리는 누구로 살아갈까",
            "02": "우리는 어디서 살아갈까",
            "03": "우리는 지금 어떻게 살아갈까",
            "04": "우리는 무엇을 하며 살아갈까"
        },
        "실": {
            "01": "인간 발달과 가족",
            "02": "가정생활과 안전",
            "03": "자원 관리와 자립",
            "04": "기술 시스템",
            "05": "기술 활용"
        }
    }
    영역명리스트 = list()
    for item in 성취기준_리스트:
        교과목 = item[2]
        영역코드 = item[3:5]
        영역명 = 영역[교과목][영역코드]
        영역명리스트.append(영역명)
    return 영역명리스트


def 평가요소처리(series):
    평가요소 = [x for x in series.to_list() if x is not np.nan]
    평가요소 = "\n".join(평가요소)
    평가요소 = 평가요소.replace("  ", " ")
    평가요소 = 평가요소.replace("▪ ", "·")
    평가요소 = 평가요소.replace("▪", "·")
    평가요소 = 평가요소.replace("￭ ", "·")
    평가요소 = 평가요소.replace("￭", "·")
    평가요소 = 평가요소.replace("\n\n", "\n")
    # 평가요소 = [x.strip() + "." for x in 평가요소.split("▪") if len(x) > 5]

    return 평가요소


xlsx_path = os.path.abspath("../평가.xlsx")
for subject in ["국어", "수학", "사회", "음악", "미술", "체육", "도덕", "영어", "실과"]:
    df = pd.read_excel(xlsx_path, na_values="", sheet_name=subject)

    rows = list()
    row_data = list()

    평가시기구분()
    for start, end in rows:
        end += 1
        성취기준 = 성취기준처리(df.iloc[start:end]["성취기준"])
        영역 = 영역명처리(성취기준)
        for index, item in enumerate(성취기준):
            평가요소 = 평가요소처리(df.iloc[start:end]["평가 요소"])
            row_data.append([영역[index], item, 평가요소])

    df_final = pd.DataFrame(columns=["영역명", "성취기준", "평가요소"], data=row_data)

    output_path = os.path.abspath(f"../최종정리({subject}).xlsx")
    df_final.to_excel(output_path, index=False)