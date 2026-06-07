# 多维线性DP
import sys

def main():
    N,M = map(int, sys.stdin.readline().split())
    boards = list(map(int, sys.stdin.readline().split()))
    cards = list(map(int, sys.stdin.readline().split()))

    c1 = cards.count(1)
    c2 = cards.count(2)
    c3 = cards.count(3)
    c4 = cards.count(4)

    # dp[i][j][k][l] 表示用了 i 张 1，j 张 2，k 张 3，l 张 4 能获得的最大分数
    dp = [[[[0]*(c4+1) for _ in range(c3+1)] for _ in range(c2+1)] for _ in range(c1+1)]
    # 初始化：在起点，没有用任何卡片，获得的分数就是起点的分数
    dp[0][0][0][0] = boards[0]

    for i in range(c1+1):
        for j in range(c2+1):
            for k in range(c3+1):
                for l in range(c4+1):
                    if  i == 0 and j == 0 and k == 0 and l == 0:
                        continue

                    # 使用这些卡片走的步数
                    pos = i*1+j*2+k*3+l*4
                    # 每次在使用这4张卡片之一的时候，都要考虑上一步状态的最大分数，取其中的最大值作为状态转换起点
                    best = 0
                    # 上次最后用的是1步卡
                    if i > 0:
                        best = max(best,dp[i-1][j][k][l])
                    # 上次最后用的是2步卡
                    if j > 0:
                        best = max(best,dp[i][j-1][k][l])
                    # 上次最后用的是3步卡
                    if k > 0:
                        best = max(best,dp[i][j][k-1][l])
                    # 上次最后用的是4步卡
                    if l > 0:
                        best = max(best,dp[i][j][k][l-1])

                    dp[i][j][k][l] = best + boards[pos]
    
    sys.stdout.write(str(dp[c1][c2][c3][c4]))

if __name__ == '__main__':
    main()