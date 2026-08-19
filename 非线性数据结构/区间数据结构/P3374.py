# 树状数组1
# Fenwick Tree 1
import sys

class FenwickTree:
    def __init__(self,values):
        self.n = len(values)-1
        self.tree = values[:]

        # O(n)建树
        for i in range(1,self.n+1):
            parent = i + self.lowbit(i)

            if parent <= self.n:
                self.tree[parent] += self.tree[i]

    # x的二进制表示中最低位的1对应的位数
    def lowbit(self,x):
        return x & -x

    # 单点加法
    def add(self,index,value):
        while index <= self.n:
            self.tree[index] += value
            index += self.lowbit(index)

    # 前缀和
    def prefix_sum(self,index):
        result = 0
        while index > 0:
            result += self.tree[index]
            index -= self.lowbit(index)
        return result 

    # 区间求和
    def range_sum(self,left,right):
        return self.prefix_sum(right) - self.prefix_sum(left-1)


def main():
    data = list(map(int,sys.stdin.buffer.read().split()))
    it = iter(data)
    n = next(it)
    m = next(it)

    values = [0]
    for _ in range(n):
        values.append(next(it))

    bit = FenwickTree(values)
    out = []
    for _ in range(m):
        op = next(it)
        x = next(it)
        y = next(it)

        if op == 1:
            bit.add(x,y)
        elif op == 2:
            out.append(bit.range_sum(x,y))

    sys.stdout.write('\n'.join(map(str,out)))

if __name__ == '__main__':
    main()


# 思路说明：
#
# 一、树状数组是什么
#
# 树状数组也叫 Fenwick Tree，
# 是一种适合处理以下操作的数据结构：
#
#     1. 单点修改
#     2. 前缀和查询
#
# 本题的操作是：
#
#     将某一个数加上 value
#     查询区间 [left, right] 的和
#
# 区间和可以通过两个前缀和相减得到，
# 所以树状数组正好适合本题。
#
#
# 二、为什么不用普通前缀和
#
# 如果数组不会修改，
# 可以先计算前缀和：
#
#     prefix[i] = a[1] + ... + a[i]
#
# 查询区间和时：
#
#     sum(left, right)
#     = prefix[right] - prefix[left - 1]
#
# 查询是 O(1)。
#
# 但本题有单点修改。
# 如果 a[x] 发生变化，
# 普通前缀和中 x 以及后面的所有位置都要修改，
# 单次修改最坏是 O(n)。
#
# 树状数组把前缀信息分成多个区间块，
# 让单点修改和查询都只需要 O(log n)。
#
#
# 三、tree[i] 保存什么
#
# tree[i] 不是简单保存 a[i]，
# 而是保存一段区间的和。
#
# 这段区间的长度是：
#
#     lowbit(i) = i & -i
#
# tree[i] 保存的区间是：
#
#     [i - lowbit(i) + 1, i]
#
# 例如：
#
#     tree[1] 保存 [1, 1]
#     tree[2] 保存 [1, 2]
#     tree[3] 保存 [3, 3]
#     tree[4] 保存 [1, 4]
#     tree[5] 保存 [5, 5]
#     tree[6] 保存 [5, 6]
#     tree[8] 保存 [1, 8]
#
# 所以 tree[4] 表示：
#
#     a[1] + a[2] + a[3] + a[4]
#
# tree[6] 表示：
#
#     a[5] + a[6]
#
#
# 四、lowbit(i) 是什么
#
# 代码：
#
#     def lowbit(self, x):
#         return x & -x
#
# lowbit(i) 表示 i 的二进制中最低位的 1。
#
# 例如：
#
#     6 = 110
#     lowbit(6) = 2
#
#     8 = 1000
#     lowbit(8) = 8
#
# 它在树状数组中表示：
#
#     tree[i] 所负责的区间长度
#
#
# 五、O(n) 建树
#
# 初始时：
#
#     self.tree = values[:]
#
# 可以先把每个位置的原始值放进去。
#
# 然后执行：
#
#     for i in range(1, self.n + 1):
#         parent = i + self.lowbit(i)
#
#         if parent <= self.n:
#             self.tree[parent] += self.tree[i]
#
# 这里的 parent 不是普通二叉树意义上的父亲，
# 而是树状数组中负责更大区间的节点。
#
# 例如：
#
#     i = 3
#     lowbit(3) = 1
#     parent = 3 + 1 = 4
#
# tree[3] 负责 [3,3]，
# tree[4] 负责 [1,4]，
# 所以要把 tree[3] 的贡献加到 tree[4]。
#
# 再例如：
#
#     i = 4
#     lowbit(4) = 4
#     parent = 4 + 4 = 8
#
# tree[4] 负责 [1,4]，
# tree[8] 负责 [1,8]，
# 所以 tree[4] 是 tree[8] 的一部分。
#
# 这种建树方式每个位置只进行常数次处理，
# 因此建树复杂度是 O(n)。
#
#
# 六、单点加法
#
# 操作：
#
#     将第 index 个数加上 value
#
# 代码：
#
#     def add(self, index, value):
#         while index <= self.n:
#             self.tree[index] += value
#             index += self.lowbit(index)
#
# 修改 a[index] 后，
# 所有包含 index 的区间块都必须更新。
#
# 例如修改位置 3：
#
#     tree[3] 负责 [3,3]
#     tree[4] 负责 [1,4]
#     tree[8] 负责 [1,8]
#
# 所以更新路径是：
#
#     3 -> 4 -> 8
#
# 代码中的：
#
#     index += lowbit(index)
#
# 就是在从当前区间跳到包含它的更大区间。
#
# 每次跳跃后 index 都会变大，
# 最多跳 O(log n) 次。
#
#
# 七、前缀和查询
#
# prefix_sum(index) 查询：
#
#     a[1] + a[2] + ... + a[index]
#
# 代码：
#
#     def prefix_sum(self, index):
#         result = 0
#         while index > 0:
#             result += self.tree[index]
#             index -= self.lowbit(index)
#         return result
#
# 例如查询前缀 [1,7]：
#
#     先加 tree[7]，负责 [7,7]
#     再跳到 6，加 tree[6]，负责 [5,6]
#     再跳到 4，加 tree[4]，负责 [1,4]
#
# 于是：
#
#     [7,7] + [5,6] + [1,4]
#
# 正好覆盖 [1,7]，并且没有重复。
#
# 代码中的：
#
#     index -= lowbit(index)
#
# 就是在把当前前缀拆成若干个互不重叠的区间块。
#
#
# 八、区间求和
#
# 查询 [left, right]：
#
#     a[left] + ... + a[right]
#
# 可以使用两个前缀和：
#
#     [1, right] - [1, left - 1]
#
# 所以：
#
#     def range_sum(self, left, right):
#         return self.prefix_sum(right) - self.prefix_sum(left - 1)
#
# 例如查询 [3,7]：
#
#     sum(3,7) = prefix_sum(7) - prefix_sum(2)
#
# 因为前缀 [1,2] 被减掉后，
# 剩下的正好是 [3,7]。
#
#
# 九、为什么本题使用 1-based 下标
#
# 树状数组的跳转依赖：
#
#     index += index & -index
#     index -= index & -index
#
# 如果 index = 0：
#
#     lowbit(0) = 0
#
# 修改时会一直停在 0，导致死循环。
#
# 因此树状数组通常从下标 1 开始，
# 程序中：
#
#     values[0] = 0
#
# 第 0 个位置只是占位，
# 真正的数据从 values[1] 开始。
#
#
# 十、复杂度分析
#
# O(n) 建树：
#
#     O(n)
#
# 单点加法：
#
#     O(log n)
#
# 前缀和查询：
#
#     O(log n)
#
# 区间求和需要两次前缀和：
#
#     O(log n)
#
# 空间复杂度：
#
#     tree 数组长度为 n + 1
#     所以是 O(n)
#
#
# 十一、树状数组适合什么问题
#
# 树状数组适合：
#
#     单点修改 + 区间求和
#     单点修改 + 前缀求和
#     单点修改 + 区间计数
#     逆序对等问题
#
# 如果需要区间修改、区间查询，
# 通常需要更复杂的树状数组技巧，
# 或者使用线段树。
