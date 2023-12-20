def set_copied_data_to_list(selector: int = None, data: str = None):
    def is_grade_korean() -> list:
        grade_data = []
        grade_dict = {'상': 0,
                      '중': 1,
                      '하': 2}
        if ("최상" in data):
            for item in data:
                try:
                    if item == '최상':
                        grade_data.append(0)
                    else:
                        grade_data.append(grade_dict[item] + 1)
                except (KeyError, ValueError):
                    grade_data.append(0)

        elif ("상" in data) or ("중" in data) or ("하" in data):
            try:
                for item in data:
                    grade_data.append(grade_dict[item])
            except (KeyError, ValueError):
                grade_data.append(0)

        else:
            try:
                for item in data:
                    grade_data.append(int(item))
            except (KeyError, ValueError):
                grade_data.append(0)

        return grade_data

    data = [str(i) for i in data.splitlines()]

    if selector == 1 or selector == 2:
        return data

    elif selector == 3:
        stacked_evaluation_datas = list()
        for row in list(data):
            evaluation_data = [str(i) for i in row.split("\t")]
            stacked_evaluation_datas.append(evaluation_data)

        stacked_evaluation_datas.sort(key=lambda x: (int(x[1].split(" ")[0]), x[0]))
        print(stacked_evaluation_datas)

        return stacked_evaluation_datas

    elif selector == 4:
        return is_grade_korean()[:]

