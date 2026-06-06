# 二维费用01背包 + 求最大值
import sys

def main():
    data = list(map(int, sys.stdin.readline().split()))
    H = data[0]
    T = data[1]
    n = int(sys.stdin.readline())
    bag = []
    for _ in range(n):
        bag.append(list(map(int, sys.stdin.readline().split())))
    
    # dp[i][j] 表示容量不超过 i,质量不超过 j 时能获得的最大价值
    dp = [[0] * (T+1) for _ in range(H+1)]
    for h,t,val in bag:
        for capacity in range(H,h-1,-1):
            for weight in range(T,t-1,-1):
                dp[capacity][weight] = max(dp[capacity][weight],dp[capacity-h][weight-t]+val)

    
    sys.stdout.write(str(dp[H][T]))


if __name__ == '__main__':
    main()