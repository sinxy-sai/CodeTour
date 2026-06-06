# 混合背包 求最大值
import sys

# 此题在洛谷上由于Python的性能问题，需要使用C++实现才能AC

def parse_time(time):
    hour,minute = map(int,time.split(':'))
    return hour*60+minute

def main():
    start,end,n = sys.stdin.readline().split()
    T = parse_time(end)-parse_time(start)
    n = int(n)

    # dp[i] 表示不超过 i 时的最大价值
    dp = [0]*(T+1)

    for _ in range(n):
        t,val,c = map(int,sys.stdin.readline().split())

        if c == 0:
            # 完全背包
            for capacity in range(t,T+1):
                dp[capacity] = max(dp[capacity],dp[capacity-t]+val)
        else:
            # 多重背包 (多重背包使用二进制优化成为01背包)
            k = 1
            while k <= c:
                w = k*t
                value = k*val

                for capacity in range(T,w-1,-1):
                    dp[capacity] = max(dp[capacity],dp[capacity-w]+value)

                c -= k
                k *= 2

            if c > 0:
                # 处理剩余的物品
                w = c*t
                value = c*val
                
                for capacity in range(T,w-1,-1):
                    dp[capacity] = max(dp[capacity],dp[capacity-w]+value)

    sys.stdout.write(str(dp[T]))

if __name__ == '__main__':
    main()
