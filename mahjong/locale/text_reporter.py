from mahjong.locale.locale_cn import cost_dict_cn, err_dict_cn, fu_dict_cn, yaku_dict_cn
from mahjong.locale.locale_default import cost_dict_default, err_dict_default, fu_dict_default, yaku_dict_default
from mahjong.locale.locale_en import cost_dict_en, err_dict_en, fu_dict_en, yaku_dict_en
from mahjong.locale.locale_jp import cost_dict_jp, err_dict_jp, fu_dict_jp, yaku_dict_jp


class TextReporter:
    def __init__(self, locale="Chinese"):
        self.locale = locale

        self.yaku_dict = None
        self.fu_dict = None
        self.cost_dict = None
        self.err_dict = None

        self.bind_dict_to_locale()

    def bind_dict_to_locale(self):
        if self.locale == "Chinese":
            self.yaku_dict = yaku_dict_cn
            self.fu_dict = fu_dict_cn
            self.cost_dict = cost_dict_cn
            self.err_dict = err_dict_cn
        elif self.locale == "English":
            self.yaku_dict = yaku_dict_en
            self.fu_dict = fu_dict_en
            self.cost_dict = cost_dict_en
            self.err_dict = err_dict_en
        elif self.locale == "Japanese":
            self.yaku_dict = yaku_dict_jp
            self.fu_dict = fu_dict_jp
            self.cost_dict = cost_dict_jp
            self.err_dict = err_dict_jp
        else:
            print("Unsupported Locale, use Default instead")
            self.yaku_dict = yaku_dict_default
            self.fu_dict = fu_dict_default
            self.cost_dict = cost_dict_default
            self.err_dict = err_dict_default

    def report(self, hand_response):
        str_fu_details = ""
        str_err = ""
        str_yaku_details = ""
        str_cost_details = ""

        str_yaku_details += self.cost_dict["yaku_details"]
        str_yaku_details += "\n"

        if hand_response.error:
            str_err = "{0}: {1}\n".format(self.err_dict["Error"], self.err_dict[hand_response.error])
        else:
            pass

        if hand_response.yaku:
            for yaku in hand_response.yaku:
                name = yaku.name

                if hand_response.is_open_hand:
                    han = yaku.han_open
                else:
                    han = yaku.han_closed

                str_detail = "{0}: {1}{2}\n".format(self.yaku_dict[name], han, self.cost_dict["han"])

                str_yaku_details += str_detail

            str_detail = "{0}: {1}{2}\n".format(self.cost_dict["total"], hand_response.han, self.cost_dict["han"])

            str_yaku_details += str_detail
        else:
            str_yaku_details += self.cost_dict["unavailable"]
            str_yaku_details += "\n"

        str_fu_details += self.cost_dict["fu_details"]
        str_fu_details += "\n"

        if hand_response.fu_details:
            for detail in hand_response.fu_details:
                str_detail = "{0}: {1}{2}\n".format(self.fu_dict[detail["reason"]], detail["fu"], self.cost_dict["fu"])

                str_fu_details += str_detail
        else:
            str_fu_details += self.cost_dict["unavailable"]
            str_fu_details += "\n"

        str_detail = "{0}: {1}{2}\n".format(self.cost_dict["total"], hand_response.fu, self.cost_dict["fu"])

        str_fu_details += str_detail

        str_cost_details += self.cost_dict["cost_details"]
        str_cost_details += "\n"

        if hand_response.cost:
            if hand_response.cost["additional"] == 0:  # trigger ron
                str_detail = "{0}: {1}({2}+{3}){4}\n".format(
                    self.cost_dict["trigger_pays"],
                    hand_response.cost["main"] + hand_response.cost["main_bonus"],
                    hand_response.cost["main"],
                    hand_response.cost["main_bonus"],
                    self.cost_dict["point"],
                )

                str_cost_details += str_detail

            elif hand_response.cost["main"] == hand_response.cost["additional"]:  # dealer tsumo
                str_detail = "{0}: {1}({2}+{3}){4}\n".format(
                    self.cost_dict["player_pays"],
                    hand_response.cost["main"] + hand_response.cost["main_bonus"],
                    hand_response.cost["main"],
                    hand_response.cost["main_bonus"],
                    self.cost_dict["point"],
                )

                str_cost_details += str_detail

            else:  # player tsumo
                str_detail = "{0}: {1}({2}+{3}){4}\n{5}: {6}({7}+{8}){4}\n".format(
                    self.cost_dict["dealer_pays"],
                    hand_response.cost["main"] + hand_response.cost["main_bonus"],
                    hand_response.cost["main"],
                    hand_response.cost["main_bonus"],
                    self.cost_dict["point"],
                    self.cost_dict["player_pays"],
                    hand_response.cost["additional"] + hand_response.cost["additional_bonus"],
                    hand_response.cost["additional"],
                    hand_response.cost["additional_bonus"],
                )

                str_cost_details += str_detail

            str_detail = "{0}: {1}{2}\n{3}: {4}{2}\n".format(
                self.cost_dict["kyoutaku_bonus"],
                hand_response.cost["kyoutaku_bonus"],
                self.cost_dict["point"],
                self.cost_dict["total"],
                hand_response.cost["total"],
            )

            str_cost_details += str_detail

        else:
            str_cost_details += self.cost_dict["unavailable"]
            str_cost_details += "\n"

        ret = {"cost": str_cost_details, "error": str_err, "fu_details": str_fu_details, "yaku": str_yaku_details}

        return ret
