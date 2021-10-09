class HandResponse:
    cost = None
    han = None
    fu = None
    fu_details = None
    yaku = None
    error = None
    is_open_hand = False

    def __init__(self, cost=None, han=None, fu=None, yaku=None, error=None, fu_details=None, is_open_hand=False):
        """
        :param cost: dict
        :param han: int
        :param fu: int
        :param yaku: list
        :param error: str
        :param fu_details: dict
        """
        self.cost = cost
        self.han = han
        self.fu = fu
        self.error = error
        self.is_open_hand = is_open_hand  # adding this field for yaku reporting

        if fu_details:
            self.fu_details = sorted(fu_details, key=lambda x: x["fu"], reverse=True)
        else:
            self.fu_details = None

        if yaku:
            self.yaku = sorted(yaku, key=lambda x: x.yaku_id)
        else:
            self.yaku = None

    def __str__(self):
        if self.error:
            return self.error
        else:
            return "{} han, {} fu".format(self.han, self.fu)
