# 01 背包 求最优解
import sys

def main():
    data = list(map(int, sys.stdin.readline().split()))
    T = data[0]
    M = data[1]
    bag = []
    for _ in range(M):
        bag.append(list(map(int, sys.stdin.readline().split())))
    
    # dp[i] 表示容量不超过 i 时能获得的最大价值
    dp = [0] * (T+1) 
    for w,val in bag:
        for capacity in range(T,w-1,-1):
            dp[capacity] = max(dp[capacity],dp[capacity-w]+val)

    
    sys.stdout.write(str(dp[T]))


if __name__ == '__main__':
    main()