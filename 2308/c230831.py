import numpy as np
from collections import defaultdict

class MinCoins():
    @staticmethod
    def min_coins_change(coins=[1,2,3], amount=10):
        dp = [np.inf]*(amount+1)
        dp[0] = 0
        for i in range(amount+1):
            for coin in coins:
                dp[i] = min(dp[i], 1+dp[i-coin])
        return dp[-1]

    @staticmethod
    def min_coins_change2(coins=[1,2,3], amount=100):
        dp = [np.inf]*(amount+1)
        dp[0] = 0
        largest_coin_used = np.zeros(amount+1)
        for i in range(amount+1):
            for coin in coins:
                if 1+dp[i-coin] < dp[i]:
                    dp[i] = 1+dp[i-coin]
                    largest_coin_used[i] = coin
        return dp[-1], largest_coin_used

    @staticmethod
    def actual_coins(largest_coin_used):
        coins = [largest_coin_used[-1]]
        sum_coins = largest_coin_used[-1]
        amount = len(largest_coin_used)-1
        ix = int(amount)
        while sum_coins < amount:
            ix -= int(coins[-1])
            coins.append(largest_coin_used[ix])
            sum_coins += largest_coin_used[ix]
        return coins


def tst_coins():
    coins, largest_coin_used = MinCoins().min_coins_change2()
    print(coins)
    print(largest_coin_used)
    coins = MinCoins().actual_coins(largest_coin_used)
    print(coins)


class JaggedArr():
    def __init__(self, a=[[1,2,3],[1,2],[1,2,3,4]]):
        self.a = a
        self.arr = np.zeros(len(a))
    
    def combos(self, k):
        if k == len(self.a):
            print(self.arr)
            return
        for i in self.a[k]:
            self.arr[k] = i
            self.combos(k+1)


if __name__ == "__main__":
    #tst_coins()
    jg = JaggedArr()
    jg.combos(0)
