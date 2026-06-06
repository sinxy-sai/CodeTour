import sys

def main():
    n = int(sys.stdin.readline())
    A = list(map(int, sys.stdin.readline().split()))

    # dp[i] 表示以A[i]结尾的最大连续子段和
    dp = [0]*n
    dp[0] = A[0]
    for i in range(1,n):
        # 两种选择：
        # 1.接在前一个子段后面 dp[i-1]+A[i]
        # 2.单独成一个子段的开头 A[i]
        dp[i] = max(dp[i-1]+A[i],A[i])

    # 最大连续字段和是所有以每个位置结尾的最大连续子段和中的最大值
    sys.stdout.write(str(max(dp)))

if __name__ == '__main__':
    main()