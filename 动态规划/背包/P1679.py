# 完全背包 + 恰好装满 + 求最小值
import sys

def main():
    m = int(sys.stdin.readline())
    bag = []
    x = 1
    while x**4 <= m:
        bag.append(x**4)
        x += 1
    
    # dp[i] 表示容量恰好为 i 时能获得的最少物品数量
    # 初始化为无穷大，表示无法恰好装满 因为是求最小值 所以是正无穷大
    dp = [float('inf')] * (m+1) 
    dp[0] = 0
    for w in bag:
        for capacity in range(w,m+1):
            dp[capacity] = min(dp[capacity],dp[capacity-w]+1)
    
    sys.stdout.write(str(dp[m]))

if __name__ == '__main__':
    main()