# 01 背包 + 恰好装满 + 求方案数
import sys

def main():
    data = list(map(int, sys.stdin.readline().split()))
    N = data[0]
    M = data[1]
    bag = list(map(int, sys.stdin.readline().split()))
    
    # dp[i] 表示容量刚好为 i 时的方案数
    dp = [0] * (M+1)
    # 初始化：容量为 0 时，方案数为 1
    dp[0] = 1 
    for w in bag:
        for capacity in range(M,w-1,-1):
            # dp[capacity]表示不选当前这个物品时，凑出capacity的方案数
            # dp[capacity-w]表示选当前这个物品时，凑出capacity-w的方案数
            dp[capacity] = dp[capacity] + dp[capacity-w]

    
    sys.stdout.write(str(dp[M]))


if __name__ == '__main__':
    main()