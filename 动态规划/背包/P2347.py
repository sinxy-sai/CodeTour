# 多重背包 + 可行性判断
import sys

def main():
    counts = list(map(int, sys.stdin.readline().split()))
    weights = [1,2,3,5,10,20]
    total_weights = 0
    for c,w in zip(counts,weights):
        total_weights += c*w
        
    
    # dp[i] 表示容量 i 是否能被凑出来
    dp = [0]*(total_weights+1) 
    dp[0] = 1

    for count,weight in zip(counts,weights):
        for _ in range(count):
            # 01背包倒序遍历，避免重复使用当前物品
            for capacity in range(total_weights,weight-1,-1):
                if dp[capacity-weight] == 1:
                    dp[capacity] = 1

    # 不包含容量为0的情况方案数
    sys.stdout.write(f"Total={sum(dp)-1}")

if __name__ == '__main__':
    main()