# 多重背包 求最优解
import sys

def main():
    data = list(map(int, sys.stdin.readline().split()))
    n = data[0]
    V = data[1]
    bag = []
    for _ in range(n):
        w,val,c = map(int, sys.stdin.readline().split())

        # 使用二进制拆分c件物品（优化了背包内数量，例如c=8，可以拆分成1,2,4,1，而不是拆成1,1,1,1,1,1,1,1）
        k = 1
        while k <= c:
            bag.append([w*k,val*k])
            c -= k
            k *= 2
        
        if c > 0:
            bag.append([w*c,val*c])
    
    # dp[i] 表示容量不超过 i 时能获得的最大价值
    dp = [0]*(V+1) 

    # 拆分后，每组物品只能选一次，所以变成了 01 背包问题
    for w,val in bag:
        for capacity in range(V,w-1,-1):
            dp[capacity] = max(dp[capacity],dp[capacity-w]+val)

    sys.stdout.write(str(dp[V]))

if __name__ == '__main__':
    main()