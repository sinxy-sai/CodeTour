# 哈希表
import sys

def main():
    n = int(sys.stdin.readline())

    mp = {} # 相当于哈希表
    ans = 0
    mod = 1 << 64 # 等价于 2^64

    for i in range(1,n+1):
        x,y = map(int,sys.stdin.readline().split())
        old = mp.get(x,0)
        ans = (ans + i * old) % mod
        mp[x] = y

    sys.stdout.write(str(ans))

if __name__ == '__main__':
    main()


# 思路说明：
#
# 题目要求维护一个映射 f(x)。
# 初始时所有 x 对应的值都是 0。
# 每次操作给出 x 和 y，需要先查询当前 f(x) 的旧值，再把 f(x) 更新成 y。
#
# 也就是说，每次操作的顺序是：
#
#     old = f(x)
#     ans += i * old
#     f(x) = y
#
# 为什么想到哈希表：
# 这题的核心需求是维护“键 -> 值”的映射关系。
# x 是键，f(x) 是值。
# 每次都要根据 x 快速查询旧值，再更新成新值。
# 哈希表可以平均 O(1) 完成查询和修改，所以适合这道题。
#
# Python 里的写法：
#
#     mp = {}
#
# 这里的 mp 是一个字典，可以看成哈希表。
# mp[x] 表示当前记录的 f(x)。
#
# 查询旧值时使用：
#
#     old = mp.get(x, 0)
#
# 如果 x 之前出现过，得到它之前保存的值；
# 如果 x 没出现过，说明 f(x) 仍然是初始值 0。
# get(x, 0) 的意思就是：查找键 x，如果不存在就返回 0。
#
# 更新时使用：
#
#     mp[x] = y
#
# 表示把 f(x) 改成 y。
#
# 为什么要对 2^64 取模：
# 题目要求最后输出 sum(i * ans_i) 对 2^64 取模的结果。
# Python 整数不会自动溢出，所以需要手动写：
#
#     mod = 1 << 64
#     ans = ans % mod
#
# 在 C++ 中如果使用 unsigned long long，溢出会自然等价于对 2^64 取模。
#
# 关于变量名 _：
# Python 里 _ 通常表示“这个变量我不会使用”。
# 例如只想循环 n 次，但不关心当前是第几次，可以写：
#
#     for _ in range(n):
#
# 但这道题需要用操作编号 i 参与计算：
#
#     ans += i * old
#
# 所以不适合写成 _，更清楚的写法是：
#
#     for i in range(1, n + 1):
#
# 注意：
# 这个 Python 版本适合理解题意和哈希表映射思想。
# 由于 n 最大是 5 * 10^6，读入量和操作次数都很大，Python 不一定能通过最大数据。
# 这题更适合用 C++ 实现快速读入和更高性能的哈希表。
