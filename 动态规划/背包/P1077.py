# 多重背包 + 恰好装满 + 求方案数
import sys

MOD = 10**6 + 7

def main():
    data = list(map(int, sys.stdin.readline().split()))
    n = data[0]
    m = data[1]
    bag = list(map(int, sys.stdin.readline().split()))
    
    # dp[i] 表示容量为 i 时的方案数
    dp = [0] * (m+1)
    # 初始化，容量为0时什么都不放，方案数为1
    dp[0] = 1 
    # 依次处理每一种物品，统计摆出不同容量的方案数。
    for c in bag:
        # 如果直接在 dp 上改，可能会把当前花重复使用
        new_dp = [0] * (m+1)
        # 在处理当前这种花时，遍历之前的花摆出的不同容量的方案
        for used in range(m+1):
            # 说明之前的花摆不出容量为used的方案
            if dp[used] == 0:
                continue

            # 当前这种花可以用cnt盆，遍历所有可能的摆法
            for cnt in range(c+1):
                # 超过了总容量m，不能继续摆
                if used + cnt > m:
                    break
                new_dp[used + cnt] = (new_dp[used + cnt] + dp[used]) % MOD

        dp = new_dp
    
    sys.stdout.write(str(dp[m]))


if __name__ == '__main__':
    main()