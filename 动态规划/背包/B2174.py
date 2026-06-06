# 完全背包 求最优解
import sys

# 01 背包：每个物品只能选一次，容量倒序遍历
# 完全背包：每个物品可以无限选，容量正序遍历

def main():
    data = list(map(int, sys.stdin.readline().split()))
    n = data[0]
    V = data[1]
    bag = []
    for _ in range(n):
        bag.append(list(map(int, sys.stdin.readline().split())))
    
    # dp[i] 表示容量不超过 i 时能获得的最大价值
    dp = [0] * (V+1) 
    for w,val in bag:
        for capacity in range(w,V+1):
            dp[capacity] = max(dp[capacity],dp[capacity-w]+val)
    
    sys.stdout.write(str(dp[V]))

if __name__ == '__main__':
    main()