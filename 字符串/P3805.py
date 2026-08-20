# Manacher算法
import sys
from array import array

# 在线性时间内求最长回文子串
def manacher(s):
    n = len(s)
    ans = 1

    # d1[i] 表示以 i 为中心的最长奇数回文半径
    # "aba" i = 1,d1[1] = 2
    # 回文长度是 d1[i] * 2 - 1
    d1 = array('I',[0])*n
    # 维护当前已知的当前右端点最靠右的回文区间（不代表是最长回文区间）
    left = 0
    right = -1
    for i in range(n):
        if i > right:
            radius = 1
        else:
            # 计算镜像位置
            mirror = left + right - i
            # 可以继承镜像位置的回文半径，但不能超过当前已知回文的右边界。
            radius = min(d1[mirror],right-i+1)

        while(i - radius >= 0 and i + radius < n and s[i - radius] == s[i + radius]):
            radius += 1
        d1[i] = radius
        length = 2 * radius - 1

        if length > ans:
            ans = length

        if i + radius - 1 > right:
            left = i - radius + 1
            right = i + radius - 1

    del d1

    # d2[i] 表示以 i-1 和 i 为中心的最长偶数回文半径
    # "abba" i = 1,d2[2] = 2
    # 回文长度是 d2[2] * 2
    d2 = array('I',[0])*n
    left = 0
    right = -1
    for i in range(n):
        if i > right :
            radius = 0
        else:
            mirror = left + right - i + 1
            radius = min(d2[mirror],right - i + 1)

        while(i - radius - 1 >= 0 and i + radius < n and s[i - radius - 1] == s[i + radius]):
            radius += 1

        d2[i] = radius

        length = 2 * radius
        if length > ans:
            ans = length

        if i + radius - 1 > right:
            left = i - radius
            right = i + radius - 1

    return ans

def main():
    s = sys.stdin.buffer.readline().strip()
    sys.stdout.write(str(manacher(s)))

if __name__ == '__main__':
    main()


# ==================== 算法思路与细节 ====================
#
# 一、回文串
#
# 回文串是正着读和反着读都一样的字符串。
#
# 例如：
#
#     aba
#     abba
#     abacaba
#
# 如果枚举每个位置作为中心，再向左右扩展，
# 最坏情况下会重复比较很多字符，时间复杂度为 O(n^2)。
#
# Manacher 算法利用回文串的对称性，
# 把求最长回文子串的复杂度降到 O(n)。
#
#
# 二、Manacher 维护的区间
#
# left 和 right 表示：
#
#     当前已经找到的、右端点最靠右的回文区间
#
# 注意：
#
#     [left, right] 不一定是最长回文区间，
#     但它的 right 是目前所有已知回文中最靠右的。
#
# 之所以维护它，是因为区间 [left, right] 是回文，
# 所以区间内部的字符和回文半径具有对称关系。
#
#
# 三、奇数长度回文：d1
#
# d1[i] 表示：
#
#     以 i 为中心的最长奇数长度回文半径，
#     并且半径包含中心字符。
#
# 例如字符串：
#
#     a b a
#     0 1 2
#
# 以位置 1 为中心：
#
#     d1[1] = 2
#
# 因为回文包含：
#
#     左边的 a、中心的 b、右边的 a
#
# 奇数回文的区间是：
#
#     [i - d1[i] + 1, i + d1[i] - 1]
#
# 奇数回文的长度是：
#
#     2 * d1[i] - 1
#
# 例如 d1[i] = 3 时：
#
#     回文区间是 [i - 2, i + 2]
#     回文长度是 5
#
#
# 四、奇数回文的镜像位置
#
# 如果当前已知回文区间是 [left, right]，
# 那么位置 i 关于该回文中心的镜像位置是：
#
#     mirror = left + right - i
#
# 例如：
#
#     left = 0, right = 6, i = 5
#
# 则：
#
#     mirror = 0 + 6 - 5 = 1
#
# 在字符串 abacaba 中：
#
#     位置 1 和位置 5 关于位置 3 对称
#
# 如果当前位置 i 在 [left, right] 内，
# 就可以参考 d1[mirror] 初始化半径。
#
# 但是不能无条件使用完整的 d1[mirror]，
# 因为镜像回文可能超过当前已知区间的右边界。
#
# 所以初始化为：
#
#     radius = min(
#         d1[mirror],
#         right - i + 1
#     )
#
# right - i + 1 表示：
#
#     从中心 i 出发，在当前已知区间内，
#     最多还能覆盖到多少层。
#
# 超出 right 的部分还没有验证，
# 需要继续使用 while 进行比较。
#
#
# 五、奇数回文的扩展
#
# 当前已经知道半径为 radius，
# 那么下一对需要比较的字符是：
#
#     左边：i - radius
#     右边：i + radius
#
# 因此代码为：
#
#     while (
#         i - radius >= 0
#         and i + radius < n
#         and s[i - radius] == s[i + radius]
#     ):
#         radius += 1
#
# 例如：
#
#     i = 3, radius = 2
#
# 当前已经确认区间 [2, 4] 是回文，
# 下一次比较位置：
#
#     i - radius = 1
#     i + radius = 5
#
# 也就是比较位置 1 和位置 5。
#
# 如果相等，就把半径扩大为 3。
#
# 当前奇数回文区间的右端点是：
#
#     i + radius - 1
#
# 如果它比原来的 right 更靠右，
# 就更新：
#
#     left = i - radius + 1
#     right = i + radius - 1
#
#
# 六、偶数长度回文：d2
#
# 偶数回文的中心不在某个字符上，
# 而是在两个字符之间。
#
# 例如：
#
#     a b b a
#     0 1 2 3
#
# 中心在位置 1 和位置 2 之间。
#
# d2[i] 表示：
#
#     以 i - 1 和 i 之间的空隙为中心，
#     能够匹配的字符对数。
#
# 对于上面的 abba：
#
#     中心用 i = 2 表示
#     d2[2] = 2
#
# 因为匹配了：
#
#     s[1] == s[2]
#     s[0] == s[3]
#
# 偶数回文的区间是：
#
#     [i - d2[i], i + d2[i] - 1]
#
# 偶数回文的长度是：
#
#     2 * d2[i]
#
#
# 七、偶数回文为什么比较 i - radius - 1 和 i + radius
#
# 假设中心在 i - 1 和 i 之间。
#
# 当 radius = 0 时，
# 第一对要比较的是中心两侧：
#
#     i - 1 和 i
#
# 代入公式：
#
#     i - radius - 1 = i - 0 - 1 = i - 1
#     i + radius = i + 0 = i
#
# 如果这一对相等，radius 变为 1。
#
# 当 radius = 1 时，
# 下一对要比较的是：
#
#     i - 2 和 i + 1
#
# 代入公式：
#
#     i - radius - 1 = i - 1 - 1 = i - 2
#     i + radius = i + 1
#
# 因此偶数回文的扩展代码为：
#
#     while (
#         i - radius - 1 >= 0
#         and i + radius < n
#         and s[i - radius - 1] == s[i + radius]
#     ):
#         radius += 1
#
# 两个边界条件分别保证：
#
#     i - radius - 1 >= 0
#         左侧下标不越界
#
#     i + radius < n
#         右侧下标不越界
#
#
# 八、偶数回文的镜像公式
#
# 奇数回文的中心是一个字符，
# 所以镜像公式是：
#
#     mirror = left + right - i
#
# 偶数回文的中心是一个空隙，
# d2[i] 表示的是 i - 1 和 i 之间的空隙。
#
# 这个中心的位置可以看成：
#
#     i - 0.5
#
# 当前回文区间 [left, right] 的中心是：
#
#     (left + right) / 2
#
# 根据对称关系，可以得到偶数回文的镜像下标：
#
#     mirror = left + right - i + 1
#
# 因此代码为：
#
#     mirror = left + right - i + 1
#     radius = min(
#         d2[mirror],
#         right - i + 1
#     )
#
# 公式比奇数回文多一个 1，
# 根本原因是偶数回文的中心位于两个字符之间。
#
#
# 九、为什么要分成 d1 和 d2 两次计算
#
# 奇数回文和偶数回文的中心不同：
#
#     奇数回文：中心是某个字符
#     偶数回文：中心是两个字符之间的空隙
#
# 为了避免插入特殊字符，
# 程序分别计算：
#
#     d1：所有奇数长度回文
#     d2：所有偶数长度回文
#
# 每次计算得到一种回文的最长长度，
# 并用 ans 保存两种情况中的最大值。
#
#
# 十、为什么时间复杂度是 O(n)
#
# 如果每个中心都从头扩展，复杂度可能是 O(n^2)。
#
# Manacher 会利用 [left, right] 内的镜像信息，
# 让当前位置从一个已经确定的半径开始扩展。
#
# while 中真正成功的扩展，
# 会推动当前回文的 right 向右移动。
#
# right 最多从 0 移动到 n - 1，
# 所以所有成功扩展的总次数是 O(n)。
#
# 每个位置最多再产生一次失败比较，
# 因此总时间复杂度为：
#
#     O(n)
#
# d1 和 d2 都需要 O(n) 空间。
# 本程序计算完 d1 后使用 del d1 释放内存，
# 再计算 d2，从而降低内存峰值。
#
# array('I') 用来保存非负回文半径，
# 比 Python 的 list[int] 更节省内存。
