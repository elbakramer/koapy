from koapy import KiwoomOpenApiContext

with KiwoomOpenApiContext() as context:
    # 로그인 처리
    context.EnsureConnected()

    # 조건검색을 사용하기 위해서는 먼저 서버에 저장된 조건들을 불러와야함 (GetConditionLoad)
    # 아래 함수는 조건을 불러온적이 없다면 불러오고 성공 이벤트까지 기다렸다 반환함
    # 이전 호출여부와 상관없이 강제로 다시 조건을 불러오려면 LoadCondition() 호출
    context.EnsureConditionLoaded()

    # 불러온 조건 리스트 확인, (조건번호, 조건이름) 쌍 리스트 반환
    conditions = context.GetConditionNameListAsList()
    print(conditions)

    # 이후 예시의 정상동작을 위해 아래에서 사용되는 조건들과 같은 이름을 가지는 조건들이 미리 저장되어 있어야함
    # - 대형 저평가 우량주
    # - 중소형 저평가주

    # 위의 조건식들은 키움에서 예시로 제공하는 추천식들을 그대로 이름을 똑같이 해서 저장한 것들임
    # 참고로 조건들을 편집하고 저장하는건 영웅문 HTS 내부에서만 가능함

    # 조건검색을 실행할 첫 조건명
    condition_name = '대형 저평가 우량주'

    # 조건을 만족하는 코드 리스트를 바로 반환 (단순 조건검색)
    codes, info = context.GetCodeListByCondition(condition_name, with_info=True)
    print(codes)
    print(info)

    # 조건검색을 다시 실행할 조건명 (같은 조건식은 1분에 1건 제한이므로 예시 실행시 제한을 회피하기 위해서 새로 설정)
    condition_name = '중소형 저평가주'

    # 실시간 조건 검색 예시, 편입된/제외된 코드 리스트 쌍을 스트림으로 반환 (실시간 조건 검색)
    for i, (inserted, deleted) in enumerate(context.GetCodeListByConditionAsStream(condition_name)):
        print()
        print('event: %d' % i)
        print('inserted: %s' % inserted)
        print('deleted: %s' % deleted)
