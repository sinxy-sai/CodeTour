# 单调队列/滑动窗口
import sys
from collections import deque

def main():
    n,k = map(int,sys.stdin.buffer.readline().split())
    data = list(map(int,sys.stdin.buffer.readline().split()))

    min_q = deque()
    max_q = deque()

    min_ans = []
    max_ans = []

    for i,x in enumerate(data):

        # 维护最小值队列，队头最小，单调递增队列
        while min_q and data[min_q[-1]] >= x:
            min_q.pop()
        min_q.append(i)

        # 维护最大值队列，队头最大，单调递减队列
        while max_q and data[max_q[-1]] <= x:
            max_q.pop()
        max_q.append(i)

        # 删掉已经滑出窗口的下标
        left = i - k + 1
        if min_q[0] < left:
            min_q.popleft()
        if max_q[0] < left:
            max_q.popleft()

         # 当窗口长度达到 k 时，记录答案
        if i >= k-1:
            min_ans.append(str(data[min_q[0]]))
            max_ans.append(str(data[max_q[0]]))

    sys.stdout.write(' '.join(min_ans) + '\n' + ' '.join(max_ans))

if __name__ == '__main__':
    main()

# 题目大意
# 给定一个长度为 n 的数组和一个长度为 k 的滑动窗口，窗口从左到右依次滑动。
# 每次窗口内共有 k 个数，要求输出每个窗口内的：

# 最小值

# 最大值

# 输出两行：

# 第一行：所有窗口的最小值

# 第二行：所有窗口的最大值

# 核心思路：单调队列
# 如果暴力求解，每个窗口都要扫描 k 个数，时间复杂度是 O(n*k)，在数据较大时会超时。

# 单调队列的核心思想是：

# 用双端队列维护“候选下标”

# 队列中下标对应的值是单调的

# 队头就是当前窗口的最值

# 对于最小值：

# 维护一个单调递增队列，队头对应的值最小

# 队列中下标对应的值从队头到队尾递增

# 对于最大值：

# 维护一个单调递减队列，队头对应的值最大

# 队列中下标对应的值从队头到队尾递减

# 算法流程
# 遍历数组中的每个元素 data[i]：

# 1. 维护最小值队列
# python
# while min_q and data[min_q[-1]] >= x:
#     min_q.pop()
# min_q.append(i)
# 如果队尾下标对应的值 >= 当前值 x

# 说明队尾元素比当前值大，而且位置更靠前

# 在后续窗口中，它不可能再成为最小值

# 所以从队尾弹出

# 最后将当前下标 i 入队

# 这样保证 min_q 中的值单调递增，队头最小。

# 2. 维护最大值队列
# python
# while max_q and data[max_q[-1]] <= x:
#     max_q.pop()
# max_q.append(i)
# 如果队尾下标对应的值 <= 当前值 x

# 说明队尾元素比当前值小，而且位置更靠前

# 在后续窗口中，它不可能再成为最大值

# 所以从队尾弹出

# 最后将当前下标 i 入队

# 这样保证 max_q 中的值单调递减，队头最大。

# 3. 删除已经滑出窗口的下标
# python
# left = i - k + 1
# if min_q[0] < left:
#     min_q.popleft()
# if max_q[0] < left:
#     max_q.popleft()
# 当前窗口的左边界是 i - k + 1

# 如果队头下标小于 left，说明它已经不在当前窗口内

# 因为队列中的下标从队头到队尾是递增的，所以只需要检查队头

# 如果队头过期，就弹出队头

# 4. 记录答案
# python
# if i >= k - 1:
#     min_ans.append(str(data[min_q[0]]))
#     max_ans.append(str(data[max_q[0]]))
# 当 i >= k - 1 时，窗口长度才达到 k

# 此时队头就是当前窗口的最值

# 最小值：data[min_q[0]]

# 最大值：data[max_q[0]]

# 关键细节
# 为什么队列存下标而不是数值？
# 因为要判断元素是否已经滑出窗口。

# 如果只存数值，无法知道这个值还在不在当前窗口内；存下标后：

# 取数值：data[q[i]]

# 判断过期：q[0] < left

# 为什么可以从队尾删除元素？
# 以最小值为例：

# 新来的元素 x 更小，且下标更靠后

# 旧元素如果比 x 大，那么在 x 存在期间，旧元素不可能成为窗口最小值

# 因此可以直接丢弃旧元素

# 同理，最大值队列中，新来的更大元素会淘汰旧的小元素。

# 相等时为什么要弹出？
# 代码中最小值队列用 >=，最大值队列用 <=。

# 相等时保留新下标，弹出旧下标

# 因为新下标更靠后，可以存活更久

# 结果不受影响，还能让队列更短

# 为什么只检查队头是否过期？
# 因为队列中的下标是单调递增的，队头一定是最早入队的下标，也最可能先滑出窗口。

# 如果队头都没有过期，那么队尾更不可能过期。

# 复杂度分析
# 时间复杂度：O(n)

# 每个元素最多入队一次、出队一次，所以整体是线性的。

# 空间复杂度：O(k)

# 队列最多同时保存 k 个下标。


# 补充说明：以本程序的 Python 写法为准
#
# 上面说的 O(k) 是“单调队列本身”的空间复杂度。
# 但是当前程序还保存了完整输入数组和完整输出数组：
#
#     data      长度 n，保存原数组
#     min_ans   长度 n - k + 1，保存所有窗口最小值
#     max_ans   长度 n - k + 1，保存所有窗口最大值
#     min_q     最多 k 个下标
#     max_q     最多 k 个下标
#
# 所以按整个程序来算，空间复杂度是：
#
#     O(n)
#
# 如果只讨论算法维护窗口最值的队列部分，
# min_q 和 max_q 的空间复杂度才是：
#
#     O(k)
#
#
# 时间复杂度：
#
# 虽然代码里有 while：
#
#     while min_q and data[min_q[-1]] >= x:
#         min_q.pop()
#
#     while max_q and data[max_q[-1]] <= x:
#         max_q.pop()
#
# 但每个下标最多进入 min_q 一次、弹出 min_q 一次；
# 也最多进入 max_q 一次、弹出 max_q 一次。
#
# 因此所有弹出操作加起来不会超过 O(n)，
# 总时间复杂度是：
#
#     O(n)
#
#
# TLE / MLE 提醒：
#
# 这题 n 最大是 10^6。
# 单调队列算法本身是正确的，复杂度也是 O(n)，
# 但是 Python 版本可能因为以下原因在洛谷上 TLE 或 MLE：
#
#     1. data 是 Python list，存 10^6 个 int 内存较大
#     2. min_ans 和 max_ans 保存了大量字符串，也很占内存
#     3. deque、list、str 转换、join 输出都有较大常数
#     4. 洛谷对 Python 的时间和内存通常没有 C++ 友好
#
# 所以这个 Python 程序适合理解单调队列思想，
# 但提交极限数据时可能 TLE / MLE。
#
# 建议：
#
#     学算法思路可以用 Python 写；
#     想稳定通过本题，建议用 C++ 实现单调队列模板。
