# 线性DP 线性递推计数 + 前缀和优化
import sys

def main():
    N,K= map(int, sys.stdin.readline().split())

    # dp[i] 表示到第i个位置的方案数
    dp = [0]*(N+1)
    dp[0] = 1

    # 暴力递推，超时
    # for i in range(1,N+1):
    #     for j in range(1,min(i,K)+1):
    #         dp[i] += dp[i-j]
        
    # sys.stdout.write(str(dp[N] % (100003)))


    # 需要用前缀和优化，空间换时间，因为dp[i] 只依赖 dp[i-1] 到 dp[i-K]的和
    prefix = [0]*(N+1)
    prefix[0] = 1
    # dp[i] = prefix[i-1] - prefix[i-K-1]

    for i in range(1,N+1):
        if i <= K:
            dp[i] = prefix[i-1]
        else:
            dp[i] = prefix[i-1] - prefix[i-K-1]
        
        dp[i] %= (100003)
        prefix[i] = dp[i] + prefix[i-1]
        
    sys.stdout.write(str(dp[N]))

if __name__ == '__main__':
    main()