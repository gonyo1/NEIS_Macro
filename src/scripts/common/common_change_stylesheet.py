"""
이 파일은 PyQt 위젯의 스타일시트를 동적으로 변경하는 함수입니다.

- 창 크기 변화에 따라 폰트 크기 등 스타일 속성을 수정할 수 있습니다.
- kwargs로 속성 값을 지정하며, 대시는 언더바(_)로 작성합니다.
- 삭제하려면 kwargs 값에 "del"을 설정합니다.

사용 방법:
1. `parent`: 스타일시트를 적용할 부모 객체
2. `obj`: 대상 위젯 객체 또는 이름
3. `kwargs`: 변경할 스타일 속성 (`font=14px` 등)

예제:
```python
change_stylesheet(parent=self.MainStacks, obj=self.mb_show_eng_adj, font="16px")
change_stylesheet(parent=self.MainStacks, obj=self.mb_show_eng_adj, font="del")
"""


def change_stylesheet(parent, obj, *args, **kwargs):
    """
    특정 위젯의 스타일시트를 동적으로 변경하는 함수.

    - parent: 스타일시트를 설정할 부모 객체.
    - obj: 스타일을 변경할 대상 위젯 (QWidget 객체 또는 객체 이름).
    - args: 추가 선택자로 사용될 인자 (예: "indicator", "placeholder").
    - kwargs: 변경할 스타일 속성과 값 (예: font="14px"). 삭제하려면 값으로 "del" 지정.
    """

    def get_object_name(searched_obj_name: str = ""):
        """대상 위젯의 이름과 추가 선택자를 결합하여 반환"""
        try:
            searched_obj_name = obj.objectName()
        except AttributeError:
            searched_obj_name = obj

        # 추가 옵션이 있다면 추가
        for arg in args:
            searched_obj_name += "::" + arg if arg in ["indicator", "placeholder", "item"] else ":" + arg
        return searched_obj_name

    def find_stylesheet_section(_parent, _obj):
        """스타일시트에서 대상 객체의 시작과 끝 위치를 찾습니다."""
        if _obj[0] == "Q":
            # Object 형식일 때
            start = _parent.find(f"{_obj}\n")
        else:
            # Name 형식일 때
            start = _parent.find(f"#{_obj}")
        if start == -1:
            return None, None  # 대상 객체가 스타일시트에 없는 경우

        end = start + _parent[start:].find("}")

        return start, end

    def modify_stylesheet():
        # 빈 문자열 생성
        _stylesheet = ""

        # kwargs 에 따라 스타일시트 변경
        for key, value in kwargs.items():
            # 대시로 형식 교체
            key = key.replace("_", "-")
            new_start = crop_stylesheet.find(str(key) + ":")
            new_end = new_start + crop_stylesheet[new_start:].find(";") + 1

            # 새로운 스타일시트 작성
            new_css = "".join([key, ": ", value, ";"])

            # 해당하는 스타일시트를 찾았을 경우
            if new_start != 0:
                # print(f"  [Info] {obj_name}'s css has changed from:{crop_stylesheet[new_start:new_end]} -> to:{new_css})")
                if value != "del":
                    _stylesheet = "".join([parent_stylesheet[:start],
                                           crop_stylesheet[:new_start],
                                           new_css,
                                           crop_stylesheet[new_end:],
                                           parent_stylesheet[end:]])
                elif value == "del":
                    _stylesheet = "".join([parent_stylesheet[:start],
                                           crop_stylesheet[:new_start],
                                           crop_stylesheet[new_end:],
                                           parent_stylesheet[end:]])

            # 해당하는 스타일시트를 찾지 못했을 경우
            else:
                # print(f"  [Info] {obj_name}'s css has changed from:{crop_stylesheet[new_start:new_end]} -> to:{new_css})")
                _stylesheet = "".join([parent_stylesheet[:start],
                                       crop_stylesheet,
                                       new_css,
                                       crop_stylesheet[new_end:],
                                       parent_stylesheet[end:]])

            _stylesheet = _stylesheet.replace("\n\n", "\n")

        return _stylesheet


    # 변경할 오브젝트 이름 얻기
    obj_name = get_object_name()

    # 변경할 스타일시트 얻기
    parent_stylesheet = parent.styleSheet()

    # 변경할 위치 찾기
    start, end = find_stylesheet_section(_parent=parent_stylesheet,
                                         _obj=obj_name)
    crop_stylesheet = parent_stylesheet[start:end]

    # 변경된 스타일시트
    stylesheet = modify_stylesheet()

    # 변경된 스타일시트 적용
    parent.setStyleSheet(stylesheet)
