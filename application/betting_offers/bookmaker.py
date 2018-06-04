class Handicapper:
    def __init__(self, ret_percent):
        self.ret_percent = ret_percent

    def handicap(self, prob1, probx, prob2):
        odds = []
        # if prob1 < self.ret_percent and probx < self.ret_percent and prob2 < self.ret_percent:
        odds.append(round(self.ret_percent/prob1, 2))
        odds.append(round(self.ret_percent/probx, 2))
        odds.append(round(self.ret_percent/prob2, 2))

        return odds
        # else:
        #     prob_list = helper(prob1, probx, prob2)
        #     return odds_helper(prob_list)

    def helper(self, prob1, probx, prob2):
        l = []
        l.append(("1", prob1))
        l.append(("x", probx))
        l.append(("2", prob2))
        l.sort(key=lambda tup: tup[1], reverse=True)
        return l

    def odds_helper(self, prob_list):
        p = prob_list[0][0]
        odds1 = 1
        oddsx = 1
        odds2 = 1
        if p == "1":
            odds1 = 1.01

        elif p == "x":
            oddsx = 1.01

        elif p == "2":
            odds2 = 1.01
