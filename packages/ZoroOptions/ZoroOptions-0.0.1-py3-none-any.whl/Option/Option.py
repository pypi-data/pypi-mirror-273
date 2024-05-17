from ZoroOptions import BinomialModel


class Option(BinomialModel):
    __optionTypeList = ["Call", "Put"]
    __optionStyleList = ["European", "American"]

    def __init__(self, S0, K, sigma=0.0, r=0.0, T=1, N=100, optionType: str = "Call", optionStyle: str = \
            "European"):
        super().__init__()
        self.S0 = S0
        self.K = K
        self.sigma = sigma
        self.r = r
        self.T = T
        self.N = N

        self.__optionType = optionType
        self.__optionStyle = optionStyle

        if self.__optionType not in self.__optionTypeList:
            raise Exception("Provide the correct option type from list:\n\t\t\t" + \
                            '\n\t\t\t'.join(str(x) for x in self.__optionTypeList))
        if self.__optionStyle not in self.__optionStyleList:
            raise Exception("Provide the correct option type from list:\n\t\t\t" + \
                            '\n\t\t\t'.join(str(x) for x in self.__optionStyleList))

    def payoff(self) -> int:
        if self.__optionType == "Call":
            return max(self.S0 - self.K, 0)
        elif self.__optionType == "Put":
            return max(self.K - self.S0, 0)
        else:
            return -1

    def moneyness(self) -> str:
        if self.__optionType == "Call":
            if self.S0 > self.K:
                return "ITM"
            elif self.S0 < self.K:
                return "OTM"
            else:
                return "ATM"
        else:
            if self.S0 > self.K:
                return "OTM"
            elif self.S0 < self.K:
                return "ITM"
            else:
                return "ATM"

    def BinomialMethodOption(self, method="Standard"):
        return self._BinomialTreeMethod(self.S0, self.K, self.sigma, self.r, self.T, self.N, self.__optionType,
                                        method=method)
