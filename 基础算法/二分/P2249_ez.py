import sys
from bisect import bisect_left

def main():
    input = sys.stdin.buffer.readline
    n,m = map(int,input().split())
    data = list(map(int,input().split()))
    query = map(int,sys.stdin.buffer.read().split())

    out = []
    for _ in range(m):
        target = next(query)
        # bisect_left(numbers, target) 会返回：第一个大于等于 target 的位置。
        index = bisect_left(data,target)

        if index < n and data[index] == target:
            out.append(index+1)
        else:
            out.append(-1)

    sys.stdout.buffer.write(' '.join(map(str,out)).encode())


if __name__ == '__main__':
    main()


# ============================================================
# 二分查找：算法理论、思路与实现细节
# ============================================================
#
# 一、二分查找适用的条件
#
# 二分查找适用于具有单调性的有序数据。
#
# 本题中的数组满足：
#
#     a[1] <= a[2] <= ... <= a[n]
#
# 也就是单调不减。
#
# 单调不减允许数组中出现重复元素，
# 但后面的元素不能小于前面的元素。
#
# 例如：
#
#     [1, 3, 3, 3, 5, 8]
#
# 是单调不减数组。
#
#
# 二、为什么可以使用二分查找
#
# 对于目标值 target，
# 在有序数组中可以根据中间元素判断目标所在方向。
#
# 如果：
#
#     data[mid] < target
#
# 那么 mid 以及 mid 左边的元素都不可能是 target，
# 可以舍弃左半部分。
#
# 如果：
#
#     data[mid] >= target
#
# 那么 target 可能在 mid，
# 也可能在 mid 的左边，
# 所以保留左半部分。
#
# 每次判断都可以排除大约一半的候选位置，
# 这就是二分查找名称的来源。
#
#
# 三、`bisect_left` 查找什么
#
# 代码：
#
#     index = bisect_left(data, target)
#
# `bisect_left(data, target)` 返回：
#
#     第一个大于等于 target 的位置。
#
# 它也可以理解为：
#
#     如果把 target 插入有序数组，
#     为了保持有序，应该插入的最左位置。
#
# 例如：
#
#     data = [1, 3, 3, 3, 5]
#     target = 3
#
# 返回：
#
#     index = 1
#
# 因为下标 1 是第一个等于 3 的位置。
#
#
# 四、为什么 `bisect_left` 可以找到第一次出现的位置
#
# 如果 target 在数组中出现多次，
# `bisect_left` 不会返回任意一个重复元素，
# 而是会继续向左寻找。
#
# 例如：
#
#     data = [1, 3, 3, 3, 5]
#
# 查找 3：
#
#     第一个大于等于 3 的位置是下标 1
#
# 所以数组中 3 的第一次出现位置就是：
#
#     index = 1
#
# 题目编号从 1 开始，
# 因此输出：
#
#     index + 1 = 2
#
#
# 五、为什么还要判断 `data[index] == target`
#
# `bisect_left` 即使找不到 target，
# 也会返回一个合法的插入位置。
#
# 例如：
#
#     data = [1, 3, 5, 7]
#     target = 4
#
# `bisect_left` 返回：
#
#     index = 2
#
# 因为 4 应该插入到 3 和 5 之间。
#
# 但：
#
#     data[2] = 5
#
# 并不是 target。
#
# 所以必须判断：
#
#     if index < n and data[index] == target:
#
# 其中：
#
#     index < n
#
# 是为了防止 target 大于数组中的所有元素时越界。
#
# 例如：
#
#     data = [1, 3, 5]
#     target = 10
#
# 此时：
#
#     index = 3
#
# 但最大有效下标是 2，
# 因此不能直接访问 data[3]。
#
#
# 六、手写二分的区间含义
#
# 如果不使用 `bisect_left`，
# 可以维护一个左闭右闭区间：
#
#     left = 0
#     right = n - 1
#
# 每次取：
#
#     mid = (left + right) // 2
#
# 查找第一个大于等于 target 的位置时：
#
#     if data[mid] >= target:
#         right = mid - 1
#     else:
#         left = mid + 1
#
# 循环结束后，left 就是第一个大于等于 target 的位置。
#
# 这正是 `bisect_left` 完成的工作。
#
#
# 七、二分查找的循环不变量
#
# 查找过程中始终维护：
#
#     答案位置不会在 left 左边；
#     答案位置不会在 right 右边。
#
# 当：
#
#     data[mid] < target
#
# 说明 mid 不可能是答案，
# 所以：
#
#     left = mid + 1
#
# 当：
#
#     data[mid] >= target
#
# mid 可能是第一个满足条件的位置，
# 不能直接丢弃 mid，
# 所以保留左侧：
#
#     right = mid - 1
#
#
# 八、Python 下标和题目编号
#
# Python 数组下标从 0 开始：
#
#     data[0] 是第 1 个数；
#     data[1] 是第 2 个数；
#     data[2] 是第 3 个数。
#
# 题目要求输出从 1 开始的编号，
# 所以：
#
#     题目编号 = Python 下标 + 1
#
# 代码：
#
#     out.append(index + 1)
#
# 就是在完成这个转换。
#
#
# 九、输入输出细节
#
# n、m 和数组数据较多，
# 程序使用：
#
#     sys.stdin.buffer.readline
#     sys.stdin.buffer.read
#
# 进行较快的输入。
#
# 查询使用：
#
#     query = map(
#         int,
#         sys.stdin.buffer.read().split()
#     )
#
# `map` 会按需生成整数，
# 不需要额外创建一个保存所有查询整数的列表。
#
# 输出先保存到 `out`，
# 最后统一转换成字符串并输出，
# 可以减少大量输出函数调用。
#
#
# 十、算法流程
#
#     1. 读入单调不减数组 data；
#     2. 对每个查询值 target 调用 bisect_left；
#     3. 得到第一个大于等于 target 的下标 index；
#     4. 如果 index 在数组范围内且 data[index] == target，
#        输出 index + 1；
#     5. 否则输出 -1。
#
#
# 十一、复杂度分析
#
# 每次二分查找都把候选区间缩小一半，
# 因此单次查询复杂度为：
#
#     O(log n)
#
# m 次查询的复杂度为：
#
#     O(m log n)
#
# 保存数组需要：
#
#     O(n)
#
# 查询结果列表需要：
#
#     O(m)
#
# 总空间复杂度为：
#
#     O(n + m)
