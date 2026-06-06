#  分组背包 求最优解
import sys

def main():
    data = list(map(int, sys.stdin.readline().split()))
    m = data[0]
    n = data[1]
    group = {}
    for _ in range(n):
        w,val,group_id = map(int, sys.stdin.readline().split())
        if group_id not in group:
            group[group_id] = []
        group[group_id].append([w,val])
    
    # dp[i] 表示容量不超过 i 时能获得的最大价值
    dp = [0] * (m+1) 
    # 一组组处理
    for group_id in group:
        items = group[group_id]
        # 分组背包：每组最多选一个物品
        # 倒序遍历容量，避免同一组内选多个物品。
        for capacity in range(m,-1,-1):
            # 每组最终会贡献不选或者选其中一个物品
            best = dp[capacity]
            for w,val in items:
                if capacity >= w:
                    best = max(best,dp[capacity-w]+val)
            dp[capacity] = best

    
    sys.stdout.write(str(dp[m]))


if __name__ == '__main__':
    main()