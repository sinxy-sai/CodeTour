# 二维费用01背包 + 求最大值
import sys

def main():
    data = list(map(int, sys.stdin.readline().split()))
    n = data[0]
    M = data[1]
    T = data[2]
    bag = []
    for _ in range(n):
        bag.append(list(map(int, sys.stdin.readline().split())))
    
    # dp[i][j] 表示容量不超过 i,质量不超过 j 时能获得的最多物品数
    dp = [[0] * (T+1) for _ in range(M+1)]
    for h,t in bag:
        for capacity in range(M,h-1,-1):
            for weight in range(T,t-1,-1):
                dp[capacity][weight] = max(dp[capacity][weight],dp[capacity-h][weight-t]+1)

    
    sys.stdout.write(str(dp[M][T]))


if __name__ == '__main__':
    main()