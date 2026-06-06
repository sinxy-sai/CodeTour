# 完全背包 + 恰好装满 + 方案数
import sys

def main():
    # 这里的输入输出在洛谷有坑
    # data = list(map(int, sys.stdin.readline().split()))
    data = list(map(int, sys.stdin.buffer.read().split()))
    V = data[0]
    N = data[1]
    # bag = list(map(int, sys.stdin.readline().split()))
    bag = data[2:]
    
    # dp[i] 表示容量刚好为 i 时的方案数
    dp = [0] * (N+1)
    # 初始化：容量为 0 时，方案数为 1
    dp[0] = 1 
    for w in bag:
        for capacity in range(w,N+1):
            # dp[capacity]表示不选当前这个物品时，凑出capacity的方案数
            # dp[capacity-w]表示选当前这个物品时，凑出capacity-w的方案数
            dp[capacity] = dp[capacity] + dp[capacity-w]

    
    sys.stdout.write(str(dp[N]))


if __name__ == '__main__':
    main()
