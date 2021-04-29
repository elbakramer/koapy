from koapy import KiwoomOpenApiPlusEntrypoint

with KiwoomOpenApiPlusEntrypoint() as context:
    context.EnsureConnected()

    account_nos = context.GetAccountList()
    print("전체 계좌 목록: %s" % account_nos)

    account_no = account_nos[0]
    print("사용할 계좌번호: %s" % account_no)
    print()

    series = context.GetDepositInfo(account_no)
    print("예수금상세현황요청 : 예수금상세현황")
    print(series.to_markdown())
    print()

    df = context.GetAccountRateOfReturnAsDataFrame(account_no)
    print("계좌수익률요청 : 계좌수익률")  # TR 이름에서 그대로 따왔긴 한데, 정작 수익률은 그 어디에도 없음..
    print(df.to_markdown())
    print()

    summary, foreach = context.GetAccountEvaluationStatusAsSeriesAndDataFrame(
        account_no
    )
    print("계좌평가현황요청 : 계좌평가현황")
    print(summary.to_markdown())
    print("계좌평가현황요청 : 종목별계좌평가현황")
    print(foreach.to_markdown())
    print()

    # 위와 아래의 차이는 수수료/세금 영향을 고려하냐 안하냐의 차이인듯, 위는 고려하지 않고 아래는 모두 고려하는것으로 보임

    summary, foreach = context.GetAccountEvaluationBalanceAsSeriesAndDataFrame(
        account_no
    )
    print("계좌평가잔고내역요청 : 계좌평가결과")
    print(summary.to_markdown(disable_numparse=True))
    print("계좌평가잔고내역요청 : 계좌평가잔고개별합산")
    print(foreach.to_markdown())
    print()
