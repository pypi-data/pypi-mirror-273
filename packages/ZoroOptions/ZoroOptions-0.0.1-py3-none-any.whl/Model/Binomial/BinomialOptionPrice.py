import numpy as np


class BinomialModel:
    def __init__(self, method="Standard"):
        __method = method

    def _MethodVariables(self, sigma, r, T, N, method="Standard"):
        dt = T / N
        if method == "Standard":
            u = np.exp(sigma * np.sqrt(dt))
            d = 1.0 / u
            pu = (np.exp(r * dt) - d) / (u - d)
            pd = 1.0 - pu
        elif method == "CRR79":
            u = np.exp((r - 0.5 * sigma ** 2) * dt + sigma * np.sqrt(dt))
            d = np.exp((r - 0.5 * sigma ** 2) * dt - sigma * np.sqrt(dt))
            pu = 1 / 2
            pd = 1 / 2
        elif method == "JR83":
            u = np.exp(sigma * np.sqrt(dt))
            d = np.exp(-1 * sigma * np.sqrt(dt))
            pu = 0.5 + (r - 0.5 * sigma ** 2) * (np.sqrt(dt) / (2 * sigma))
            pd = 1 - pu
        elif method == "TRG92":
            u = np.exp(np.sqrt((sigma ** 2) * dt + (r * dt - 0.5 * sigma ** 2 * np.sqrt(dt)) ** 2))
            d = np.exp(-np.sqrt((sigma ** 2) * dt + (r * dt - 0.5 * sigma ** 2 * np.sqrt(dt)) ** 2))
            pu = 0.5 + 0.5 * (r - 0.5 * sigma ** 2) * (
                    dt / np.sqrt((sigma ** 2) * dt + (r * dt - 0.5 * sigma ** 2 * np.sqrt(dt)) ** 2))
            pd = 1 - pu
        else:
            raise Exception("Choose method from 'Standard', 'CRR79', 'JR83', 'TRG92' ")

        return u, d, pu, pd

    def _BinomialTreeMethod(self, S0, K, sigma, r, T, N, optionType="Call", optionStyle="European", method="Standard"):
        dt = T / N
        u, d, pu, pd = self._MethodVariables(sigma, r, T, N, method)
        # Construct the binomial tree : option price.
        # S underlying assest value
        optionPriceTree = np.zeros((N + 1, N + 1))
        assetPriceTree = np.zeros((N + 1, N + 1))

        for i in range(0, N + 1):
            assetPriceTree[N, i] = S0 * (u ** i) * (d ** (N - i))
            if optionType == "Call":
                optionPriceTree[N, i] = max(assetPriceTree[N, i] - K, 0)
            elif optionType == "Put":
                optionPriceTree[N, i] = max(K - assetPriceTree[N, i], 0)
            else:
                raise Exception("Choose from 'Call' or 'Put'")

        for j in range(N - 1, -1, -1):
            for i in range(0, j + 1):
                optionPriceTree[j, i] = np.exp(-r * dt) * (
                        pu * optionPriceTree[j + 1, i + 1] + (1 - pu) * optionPriceTree[j + 1, i])
                assetPriceTree[j, i] = S0 * (u ** i) * (d ** (N - i))
                if optionStyle == "American":
                    if optionType == "Call":
                        optionPriceTree[j, i] = np.maximum(optionPriceTree[j, i], assetPriceTree[j, i] - K)
                        # Decision between the European option price and the payoff from early-exercise
                    else:
                        optionPriceTree[j, i] = np.maximum(optionPriceTree[j, i], K - assetPriceTree[j, i])
        # print(tree)
        return optionPriceTree[0, 0]

