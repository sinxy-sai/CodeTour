# 哈希表计数
import sys
from collections import Counter


def main():
    N,C = map(int,sys.stdin.readline().split())
    data = list(map(int,sys.stdin.readline().split()))

    cnt = Counter(data)

    # print(cnt)

    ans = 0
    for B in cnt:
        ans += cnt[B] * cnt[B+C]
    sys.stdout.write(str(ans))

if __name__ == '__main__':
    main()


# 思路说明：
#
# 题目要求统计满足 A - B = C 的数对数量。
# 直接枚举两个位置会是 O(N^2)，而 N 最大是 2 * 10^5，会超时。
# 因为 A - B = C 可以变形为 A = B + C，所以只要知道每个数出现了几次，
# 就可以快速判断某个 B 对应的 A = B + C 出现了多少次。
#
# 为什么想到哈希表：
# 这题的关键不是维护顺序，而是频繁查询“某个值出现了多少次”。
# 哈希表可以用接近 O(1) 的时间按值查询次数，所以适合用来做计数。
#
# 为什么用哈希表计数：
# 题目说“不同位置的数字一样的数对算不同的数对”，所以不能只看某个数字
# 是否存在，还要知道它出现了几次。
# 例如 B 出现 x 次，B + C 出现 y 次，那么这些位置可以两两配对。
#
# Counter 的作用：
# Counter 是 collections 里的计数工具，可以把列表转成“数字 -> 出现次数”的映射。
# 例如 data = [1, 1, 2, 3]，Counter(data) 得到的效果类似：
# {1: 2, 2: 1, 3: 1}
#
# Counter 的一个方便点：
# 如果访问不存在的键，普通字典可能会报 KeyError，
# 但 Counter 会返回 0。
# 所以 cnt[B + C] 即使 B + C 没有出现过，也会得到 0，不会报错。
#
# cnt[B] * cnt[B + C] 的含义：
# 枚举一个值 B 时，合法的 A 必须等于 B + C。
# 如果 B 出现 cnt[B] 次，B + C 出现 cnt[B + C] 次，
# 那么每一个 B 的位置都可以和每一个 B + C 的位置组成一个合法数对。
# 根据乘法原理，贡献就是 cnt[B] * cnt[B + C]。
#
# 这样枚举每一种 B，就能统计所有合法数对：
# 1. 不会漏掉，因为每个合法数对都有确定的 B，并且 A 一定是 B + C。
# 2. 不会重复，因为一个数对只会在枚举它自己的 B 值时被统计一次。
#
# 时间复杂度：O(N)
# 空间复杂度：O(N)
