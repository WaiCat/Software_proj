import json

# 주어진 문자열
policy_info = {'정책이름': '금정구 청년창조발전소(꿈터플러스) 입주 스타트업 모집', '신청기간': '2023-11-24 ~ 2023-12-26', '진행일정': '신청서 작성 및 접수(11/24~12/26)→ 서면심사(12/27)→ 심사결과 통보(개별 통보)→ 입주계약 체결(12/28~12/29)→ 입주(1/1~)', '지원대상': '기타', '담당기관': '청년창조발전소 꿈터플러스', '문의': '051-710-4920~3', '홈페이지': 'http://www.xn--cw0bn74d.kr/board/bbs/board.php?bo_table=notice≀_id=153'}


# 작은 따옴표를 큰 따옴표로 변경하는 코드
policy_info_str = str(policy_info).replace("'", '"')



# 문자열을 딕셔너리로 변환
program_info = json.loads(policy_info_str)

# 딕셔너리 출력
print(program_info)
