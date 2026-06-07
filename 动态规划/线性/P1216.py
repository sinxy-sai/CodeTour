# 二维线性DP 网格路径最优
import sys

def main():
    n = int(sys.stdin.readline())
    A = []
    for _ in range(n):
        A.append(list(map(int, sys.stdin.readline().split())))

    # A[r][c] 现在表示从三角形顶部到 第 r 行第 c 列 的最大路径和 变成了DP数组
    # 第 i 行 只依赖 第 i-1 行，所以原地更新安全，如果一个 DP 的状态依赖当前行已经更新过的值，就不能随便原地更新
    for r in range(1,n):
        for c in range(r+1):
            if c == 0:
                # 每一行最左边，只能从上一行最左边下来
                A[r][c] += A[r-1][c]
            elif c == r:
                # 每一行最右边，只能从上一行最右边下来
                A[r][c] += A[r-1][c-1]
            else:
                # 其他位置，可以从上一行的左边或右边下来
                A[r][c] += max(A[r-1][c],A[r-1][c-1])
    sys.stdout.write(str(max(A[n-1])))

if __name__ == '__main__':
    main()