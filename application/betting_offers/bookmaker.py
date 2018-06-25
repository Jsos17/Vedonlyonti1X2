class Handicapper:
    def __init__(self, ret_percent):
        self.ret_percent = ret_percent

    def handicap(self, prob1, probx, prob2):
        odds = []
        odds.append(round(self.ret_percent/prob1, 2))
        odds.append(round(self.ret_percent/probx, 2))
        odds.append(round(self.ret_percent/prob2, 2))

        return odds
