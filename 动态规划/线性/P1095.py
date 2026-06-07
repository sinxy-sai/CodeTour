# 线性DP 多决策阶段DP + 贪心预处理
import sys

def main():
    M,S,T = map(int,sys.stdin.readline().split())
    # 每秒有三种决策
    # 1. 跑步：距离 +17
    # 2. 闪烁：如果魔法值 >=10，距离 +60，魔法值 -10
    # 3. 休息：距离不变，魔法值 +4
    # 直接把“距离 + 魔法值”一起做 DP 会麻烦。这个题有一个常用简化：
    # 先算出“只用闪烁和休息”时，每一秒最多能走多远。
    # 然后再和“跑步”比较。
    # 这个题最妙的地方就是：闪烁体系负责提供“高收益跳跃”，跑步体系负责在不能有效闪烁的时候补距离。
    # 因此不用做二维 DP。

    # flash_dist[i] 表示第 i 秒最多能走多远，只用闪烁和休息决策
    flash_dist = [0]*(T+1)
    mana = M
    for i in range(1,T+1):
        if mana >= 10:
            # 魔法够，就闪烁
            flash_dist[i] = flash_dist[i-1]+60
            mana -= 10
        else:
            # 魔法不够，就休息
            flash_dist[i] = flash_dist[i-1]
            mana += 4
    
    # best 表示第 i 秒最多能走多远，综合考虑三种决策
    best = 0
    for i in range(1,T+1):
        best = max(best+17,flash_dist[i])
        if best >= S:
            sys.stdout.write('Yes\n'+str(i))
            return 

    sys.stdout.write('No\n'+str(best))
    

if __name__ == '__main__':
    main()