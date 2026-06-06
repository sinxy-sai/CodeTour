# 前K优解背包 + 恰好装满背包 + 01背包问题
import sys

# 此题在洛谷上由于Python的性能问题，需要使用C++实现才能AC

# 给你 K 个容量相同的 01 背包，
# 每个背包都必须恰好装满， (恰好装满背包问题)
# 每个背包内部每种物品最多选一次， (01背包问题)
# 不同背包之间可以选相同物品，但是两个背包的物品清单不能完全一样。 (方案要求不同)

# 目标： 让这 K 个不同方案的价值总和最大。 (01背包问题的前K优解(以往的01背包是求最优解)  )

def main():
    data = list(map(int, sys.stdin.readline().split()))
    K = data[0] 
    V = data[1] 
    N = data[2]

    bag = []
    for _ in range(N):
        bag.append(list(map(int, sys.stdin.readline().split())))
    
    # dp[i] 表示容量恰好为 i 时的前K大价值列表
    dp = [[] for _ in range(V+1)]
    dp[0] = [0] # 容量为0时，只有一种方案，就是不选任何物品，价值为0

    # 恰好装满背包求最优解的初始化与01背包求最优解不同，01背包的初始化是dp = [0] * (V+1)，而恰好装满背包的初始化是 dp[0] = 0 ，其他dp[i] = -inf

    for w,val in bag:
        # 01背包，容量倒序遍历
        for capacity in range(V,w-1,-1):
            # 合并后排序太慢了
            candidates = []

            # 不选当前物品
            for old_val in dp[capacity]:
                candidates.append(old_val)

            # 选当前物品
            for old_val in dp[capacity-w]:
                candidates.append(old_val+val)
            
            # 取前K大价值
            candidates.sort(reverse=True)
            dp[capacity] = candidates[:K]
    

    sys.stdout.write(str(sum(dp[V][:K]))) # 取前K大价值的和

if __name__ == '__main__':
    main()