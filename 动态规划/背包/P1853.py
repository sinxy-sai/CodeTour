# 完全背包 + 滚动更新背包容量 + 求最大值
import sys

def main():
    s,n,d = map(int, sys.stdin.readline().split())
    bag = []
    for _ in range(d):
        w,val = map(int, sys.stdin.readline().split())
        bag.append([w//1000,val])

    money = s

    for _ in range(n):
        V = money // 1000 # 表示最多能投资的 1000 单位数量。
        # dp[i] 表示容量不超过 i * 1000 时能获得的最大价值
        dp = [0] * (V+1) 
        for w,val in bag:
            for capacity in range(w,V+1):
                dp[capacity] = max(dp[capacity],dp[capacity-w]+val)
        money += dp[V]
    
    sys.stdout.write(str(money))

if __name__ == '__main__':
    main()