# 01背包:装箱
import sys

def main():
    V = int(sys.stdin.readline())
    n = int(sys.stdin.readline())
    bag = []
    for _ in range(n):
        bag.append(int(sys.stdin.readline()))
    
    # dp[i] 表示容量不超过 i 时能获得的最大体积
    dp = [0] * (V+1) 
    for w in bag:
        for capacity in range(V,w-1,-1):
            dp[capacity] = max(dp[capacity],dp[capacity-w]+w)

    
    sys.stdout.write(str(V-dp[V]))


if __name__ == '__main__':
    main()