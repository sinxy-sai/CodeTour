# 线性DP 子序列最优（没要求连续）
import sys

def main():
    n = int(sys.stdin.readline())
    A = list(map(int, sys.stdin.readline().split()))

    # dp[i] 表示以A[i]结尾的最长上升子序列的长度
    dp = [1]*n

    for i in range(1,n):
        # 遍历在i之前的所有位置j，作为可以考虑的前一个位置
        for j in range(i):
            # 如果 A[j] 比 A[i] 小，A[i] 就可以接在 A[j] 后面
            if A[j] < A[i]:
                # 选择接在 A[j] 后面，或者单独成一个子序列的开头
                dp[i] = max(dp[i],dp[j]+1)

    # 最大上升子序列的长度是所有以每个位置结尾的最长上升子序列长度中的最大值
    sys.stdout.write(str(max(dp)))

if __name__ == '__main__':
    main()