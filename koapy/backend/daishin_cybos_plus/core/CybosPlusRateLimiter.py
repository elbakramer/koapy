from koapy.utils.rate_limiting.RateLimiter import TimeWindowRateLimiter


class CybosPlusLookupRequestRateLimiter(TimeWindowRateLimiter):

    """
    시세 오브젝트 조회 제한: 15초에 최대 60건으로제한

    Q. 플러스 데이터 요청 사용 제한에 대해 알고 싶습니다.
    http://money2.daishin.com/e5/mboard/ptype_accordion/plusFAQ/DW_Basic_List.aspx?boardseq=298&m=9508&p=8835&v=8640
    """

    def __init__(self):
        super().__init__(15, 60)


class CybosPlusTradeRequestRateLimiter(TimeWindowRateLimiter):

    """
    주문관련 오브젝트 조회 제한: 15초에 최대 20건으로제한

    Q. 플러스 데이터 요청 사용 제한에 대해 알고 싶습니다.
    http://money2.daishin.com/e5/mboard/ptype_accordion/plusFAQ/DW_Basic_List.aspx?boardseq=298&m=9508&p=8835&v=8640
    """

    def __init__(self):
        super().__init__(15, 20)
