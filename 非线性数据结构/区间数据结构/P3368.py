# 树状数组2
# Fenwick Tree2 差分数组

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

    # 构造差分数组
    diff = [0]*(n+1)
    diff[1] = values[1]
    for i in range(2,n+1):
        diff[i] = values[i] - values[i-1]

    bit = FenwickTree(diff)
    out = []
    for _ in range(m):
        op = next(it)

        if op == 1:
            left = next(it)
            right = next(it)
            value = next(it)

            bit.add(left,value)

            if right + 1 <= n:
                bit.add(right+1,-value)

        elif op == 2:
            index = next(it)
            out.append(bit.prefix_sum(index))

    sys.stdout.write('\n'.join(map(str,out)))

if __name__ == '__main__':
    main()


# 思路说明：
#
# 一、这题和 P3374 的区别
#
# P3374 是：
#
#     单点修改 + 区间求和
#
# 本题是：
#
#     区间修改 + 单点查询
#
# 如果直接修改区间 [left, right] 中的每个元素，
# 一次操作最坏需要 O(n)，数据大时会超时。
#
# 本题的关键是使用差分数组，
# 把一次区间修改转化成两次单点修改。
#
#
# 二、什么是差分数组
#
# 对原数组 a 定义差分数组 diff：
#
#     diff[1] = a[1]
#     diff[i] = a[i] - a[i - 1]，i >= 2
#
# 于是原数组第 x 个数可以通过差分数组前缀和恢复：
#
#     a[x] = diff[1] + diff[2] + ... + diff[x]
#
# 也就是：
#
#     a[x] = diff 的前缀和
#
# 例如原数组：
#
#     a = [1, 5, 4, 2, 3]
#
# 差分数组是：
#
#     diff[1] = 1
#     diff[2] = 5 - 1 = 4
#     diff[3] = 4 - 5 = -1
#     diff[4] = 2 - 4 = -2
#     diff[5] = 3 - 2 = 1
#
# 所以：
#
#     diff = [1, 4, -1, -2, 1]
#
# 查询 a[3]：
#
#     1 + 4 - 1 = 4
#
# 正好恢复出原数组第 3 个数。
#
#
# 三、为什么区间加可以变成两次单点修改
#
# 假设给原数组区间 [left, right] 中的每个数加 value。
#
# 差分数组只需要修改两个位置：
#
#     diff[left] += value
#     diff[right + 1] -= value
#
# 为什么？
#
# 从 left 开始，差分前缀和会多出 value，
# 所以原数组 left 到 right 的每个数都会加 value。
#
# 在 right + 1 位置减去 value，
# 可以让之后的前缀和恢复原状，
# 所以 right + 1 之后的元素不受影响。
#
# 例如给 [2,4] 中每个数加 2：
#
# 原差分：
#
#     [1, 4, -1, -2, 1]
#
# 修改：
#
#     diff[2] += 2
#     diff[5] -= 2
#
# 新差分：
#
#     [1, 6, -1, -2, -1]
#
# 恢复原数组：
#
#     a[1] = 1
#     a[2] = 1 + 6 = 7
#     a[3] = 1 + 6 - 1 = 6
#     a[4] = 1 + 6 - 1 - 2 = 4
#     a[5] = 1 + 6 - 1 - 2 - 1 = 3
#
# 可以看到第 2 到第 4 个数都增加了 2，
# 第 5 个数恢复成原来的值。
#
#
# 四、为什么使用树状数组
#
# 差分数组上的操作变成了：
#
#     单点加法
#     前缀和查询
#
# 这正是树状数组擅长的操作。
#
# 程序中的 FenwickTree 保存的不是原数组，
# 而是差分数组 diff。
#
#     bit.add(index, value)
#
# 表示修改 diff[index]。
#
#     bit.prefix_sum(index)
#
# 表示求：
#
#     diff[1] + ... + diff[index]
#
# 这个结果就是原数组第 index 个数的当前值。
#
#
# 五、初始化差分数组
#
# 代码：
#
#     values = [0]
#     for _ in range(n):
#         values.append(next(it))
#
# values[0] 是占位位置，
# 原数组从下标 1 开始。
#
# 然后构造：
#
#     diff[1] = values[1]
#     diff[i] = values[i] - values[i - 1]
#
# 得到初始差分数组。
#
# 再把 diff 交给 FenwickTree：
#
#     bit = FenwickTree(diff)
#
# FenwickTree 内部进行 O(n) 建树，
# 之后就可以用树状数组维护差分数组。
#
#
# 六、区间修改操作
#
# 操作格式：
#
#     1 left right value
#
# 代码：
#
#     bit.add(left, value)
#
# 表示：
#
#     diff[left] += value
#
# 如果 right + 1 没有越界：
#
#     if right + 1 <= n:
#         bit.add(right + 1, -value)
#
# 表示：
#
#     diff[right + 1] -= value
#
# 这两次树状数组单点修改，
# 就完成了原数组区间 [left, right] 的整体加法。
#
# 如果 right == n，
# 那么 right + 1 超出数组范围，
# 不需要进行第二次修改。
#
#
# 七、单点查询操作
#
# 操作格式：
#
#     2 index
#
# 当前原数组第 index 个数等于差分数组前缀和：
#
#     a[index] = diff[1] + ... + diff[index]
#
# 所以代码是：
#
#     out.append(bit.prefix_sum(index))
#
# 树状数组的 prefix_sum() 会把差分数组前缀分解成多个互不重叠的区间块，
# 最终得到当前点的真实值。
#
#
# 八、树状数组中的两个跳转
#
# 单点修改时：
#
#     index += lowbit(index)
#
# 向后跳，更新所有包含当前位置的区间块。
#
# 前缀查询时：
#
#     index -= lowbit(index)
#
# 向前跳，把前缀拆成多个互不重叠的区间块。
#
# 其中：
#
#     lowbit(index) = index & -index
#
# 表示当前树状数组节点负责的区间长度。
#
#
# 九、复杂度分析
#
# 构造差分数组：
#
#     O(n)
#
# 树状数组 O(n) 建树：
#
#     O(n)
#
# 每次区间修改需要两次单点加法：
#
#     O(log n)
#
# 每次单点查询需要一次前缀和：
#
#     O(log n)
#
# 所以总时间复杂度是：
#
#     O(n + m log n)
#
# 空间复杂度：
#
#     values、diff、tree 都是 O(n)
#
# 总空间复杂度是：
#
#     O(n)
#
#
# 十、和线段树的区别
#
# 本题只要求：
#
#     区间加 + 单点查询
#
# 使用差分数组加树状数组就能解决，
# 代码和空间都比较简单。
#
# 如果题目改成：
#
#     区间加 + 区间求和
#
# 通常需要使用线段树，
# 或者使用两个树状数组的区间修改区间查询技巧。
