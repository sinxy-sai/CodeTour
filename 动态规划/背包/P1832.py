# 完全背包 + 恰好装满 + 方案数 + 素数
import sys

def get_primes(n):
    '''
    获取小于等于 n 的所有素数(质数)
    基于埃氏筛法
    '''
    is_prime = [True]*(n+1)
    if n >=0 :
        is_prime[0] = False
    if n >= 1:
        is_prime[1] = False

    for i in range(2,int(n**0.5)+1):
        # 如果 i 是素数，那么 i 的倍数都不是素数
        if is_prime[i]:
            # 从 i*i 开始，因为 i*i 之前的倍数(i*1,i*2,...,i*i-1)已经标记为合数了
            for j in range(i*i,n+1,i):
                is_prime[j] = False

    primes = []
    for i in range(2,n+1):
        if is_prime[i]:
            primes.append(i)

    return primes

def main():
    # 这里的输入输出在洛谷有坑
    # data = list(map(int, sys.stdin.readline().split()))
    n = int(sys.stdin.readline())
    bag = get_primes(n)
    
    # dp[i] 表示容量刚好为 i 时的方案数
    dp = [0] * (n+1)
    # 初始化：容量为 0 时，方案数为 1
    dp[0] = 1 
    for w in bag:
        for capacity in range(w,n+1):
            # dp[capacity]表示不选当前这个物品时，凑出capacity的方案数
            # dp[capacity-w]表示选当前这个物品时，凑出capacity-w的方案数
            dp[capacity] = dp[capacity] + dp[capacity-w]

    
    sys.stdout.write(str(dp[n]))


if __name__ == '__main__':
    main()
