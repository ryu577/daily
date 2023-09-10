import numpy as np


def perm(a, ix):
    if ix == len(a):
        print(a)
    else:
        for j in range(ix+1):
            swap(a, j, ix)
            perm(a, ix+1)
            # This is the backtracking.
            swap(a, j, ix)


def swap(a, i, j):
    tmp = a[j]
    a[j] = a[i]
    a[i] = tmp


def paren(a, ix, n=3, left_cnt=0, right_cnt=0):
    if ix == n:
        print("".join(a))
    else:
        # Here, the for loop is only two.
        a.append("(")
        left_cnt += 1
        if left_cnt <= 3 and left_cnt >= right_cnt:
            paren(a, ix+1, n, left_cnt, right_cnt)
        # This is the backtracking.
        a.pop()
        left_cnt -= 1
        a.append(")")
        right_cnt += 1
        if right_cnt <= 3 and left_cnt >= right_cnt:
            paren(a, ix+1, n, left_cnt, right_cnt)
        # This is the backtracking.
        a.pop()
        right_cnt -= 1


def max_subseq_sum(a):
    dp = [-np.inf]*len(a)
    dp[0] = a[0]
    for i in range(1,len(a)):
        if dp[i-1] > 0:
            dp[i] = dp[i-1]+a[i]
        else:
            dp[i] = a[i]
    return max(dp)


if __name__ == "__main__":
    #a = [1,2,3]
    #perm(a, 0)
    paren([], 0, 6)
    a = [-2,1,-3,4,-1,2,1,-5,4]
    sum1 = max_subseq_sum(a)
    print(sum1)

