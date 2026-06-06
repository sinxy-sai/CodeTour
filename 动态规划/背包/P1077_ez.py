# 多重背包 + 恰好装满 + 求方案数
import sys

MOD = 10**6 + 7

def main():
    data = list(map(int, sys.stdin.readline().split()))
    n = data[0]
    m = data[1]
    bag = list(map(int, sys.stdin.readline().split()))
    
    # dp[i][j] 表示前 i 种花刚好摆 j 盆的方案数
    dp = [[0] * (m+1) for _ in range(n+1)]
    dp[0][0] = 1 # 不选任何花，摆 0 盆的方案数为 1
    for i in range(1,n+1):
        for j in range(m+1):
            for c in range(bag[i-1]+1):
                if c > j:
                    break
                dp[i][j] = (dp[i][j] + dp[i-1][j-c]) % MOD

    
    sys.stdout.write(str(dp[n][m]))


if __name__ == '__main__':
    main()