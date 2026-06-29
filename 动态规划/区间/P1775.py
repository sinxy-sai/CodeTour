# 区间DP 基础的线性区间合并标准实现

# 所有题目都遵循「枚举区间长度→左端点→分割点」的三层循环框架
import sys

def main():
    N = int(sys.stdin.readline())
    A = list(map(int, sys.stdin.readline().split()))

    # prefix[i] 表示前 i 堆元素的总和 = A[0] + A[1] + ... + A[i-1]
    prefix = [0] * (N+1)
    for i in range(1,N+1):
        prefix[i] = prefix[i-1] + A[i-1]
    
    # dp[l][r] 表示合并 第 l 堆到第 r 堆的最小成本
    # l,r是0-based
    dp = [[0] * N for _ in range(N)]

    # length 表示区间长度
    for length in range(2,N+1):
        # l 表示区间左端点
        for l in range(0,N - length + 1):
            # r 表示区间右端点
            r = l + length -1
            dp[l][r] = float('inf')
            # 枚举区间分割点(不取r)
            for k in range(l,r):
                # 合并区间[l,k]和区间[k+1,r]为一堆 = 合并[l,k]为一堆的成本 + 合并[k+1,r]为一堆的成本 + 合并[l,r]为一堆的总和
                dp[l][r] = min(dp[l][r],dp[l][k] + dp[k+1][r] + prefix[r+1] - prefix[l])

    sys.stdout.write(str(dp[0][N-1]))
if __name__ == '__main__':
    main()