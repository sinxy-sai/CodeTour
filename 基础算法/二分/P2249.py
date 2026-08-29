import sys

def bisect_left(data,target):
    left,right = 0,len(data)
    while left < right:
        mid = (left+right)//2
        if data[mid] < target:
            # mid 不可能是答案
            left = mid+1
        else:
            # mid 可能是第一个 >= target 的位置
            right = mid
    return left

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
# 二分查找：算法思路、理论与实现细节
# ============================================================
#
# 一、题目条件
#
# 数列满足单调不减：
#
#     data[0] <= data[1] <= ... <= data[n-1]
#
# 这意味着：
#
#     如果某个位置的值小于 target，
#     那么它左边的值也一定小于 target；
#
#     如果某个位置的值大于等于 target，
#     那么它右边的值也一定大于等于 target。
#
# 正因为存在这种单调性，
# 才能使用二分查找。
#
#
# 二、题目真正需要寻找的是什么
#
# 题目要求 target 第一次出现的位置。
#
# 这可以转化为：
#
#     寻找第一个满足 data[index] >= target 的位置。
#
# 找到这个位置后：
#
#     如果 data[index] == target，
#         它就是 target 第一次出现的位置；
#
#     如果 data[index] > target，
#         说明 target 不存在。
#
# 代码中的：
#
#     index = bisect_left(data, target)
#
# 查找的就是第一个大于等于 target 的位置。
#
#
# 三、`bisect_left` 的含义
#
# `bisect_left(data, target)` 可以理解为：
#
#     如果要把 target 插入 data，
#     为了保持数组有序，
#     应该插入的最左位置。
#
# 例如：
#
#     data = [1, 3, 3, 3, 5]
#     target = 3
#
# 返回下标 1：
#
#     [1, 3, 3, 3, 5]
#         ^
#         第一个 3
#
# 如果：
#
#     target = 4
#
# 返回下标 4，
# 因为 4 应该插入 3 和 5 之间。
#
#
# 四、为什么使用左闭右开区间
#
# 函数初始化：
#
#     left = 0
#     right = len(data)
#
# 当前搜索区间表示为：
#
#     [left, right)
#
# 也就是包含 left，
# 但不包含 right。
#
# 例如数组长度为 5：
#
#     初始区间是 [0, 5)
#
# 实际包含下标：
#
#     0、1、2、3、4
#
# 这种写法有两个好处：
#
#     1. right 可以等于 len(data)；
#     2. target 比所有元素都大时，
#        可以自然返回 len(data)。
#
#
# 五、二分循环的判断
#
# 代码：
#
#     mid = (left + right) // 2
#
# 如果：
#
#     data[mid] < target
#
# 那么 mid 以及 mid 左边的所有元素都小于 target。
#
# 因此 mid 不可能是第一个大于等于 target 的位置，
# 可以舍弃左半部分：
#
#     left = mid + 1
#
# 如果：
#
#     data[mid] >= target
#
# 那么 mid 可能就是答案，
# 但它左边还可能存在更早的位置。
#
# 所以不能令 left = mid + 1，
# 而是保留 mid 及其左侧：
#
#     right = mid
#
#
# 六、循环不变量
#
# 二分过程中始终维护：
#
#     left 左边的所有位置都满足 data[i] < target；
#
#     right 以及 right 右边的位置，
#     不一定全部是答案区域，
#     但答案不会在 right 右边。
#
# 更直观地说：
#
#     答案始终位于 [left, right) 中。
#
# 当 data[mid] < target 时：
#
#     mid 不可能是答案，
#     所以答案只能在 [mid + 1, right)。
#
# 当 data[mid] >= target 时：
#
#     mid 可能是答案，
#     所以答案仍在 [left, mid) 或正好是 mid，
#     合并写成 [left, mid) 的下一轮边界。
#
#
# 七、为什么循环结束后返回 left
#
# 循环条件是：
#
#     while left < right:
#
# 当循环结束时：
#
#     left == right
#
# 此时搜索区间为空，
# `left` 就是数组中的分界位置：
#
#     下标小于 left 的元素都 < target；
#     下标大于等于 left 的元素都 >= target。
#
# 因此：
#
#     left = 第一个 data[i] >= target 的位置
#
# 所以函数最后返回：
#
#     return left
#
#
# 八、具体例子：查找第一次出现的 3
#
#     data = [1, 3, 3, 3, 5]
#     target = 3
#
# 初始：
#
#     left = 0, right = 5
#
# 第一次：
#
#     mid = 2
#     data[2] = 3 >= 3
#     right = 2
#
# 第二次：
#
#     left = 0, right = 2
#     mid = 1
#     data[1] = 3 >= 3
#     right = 1
#
# 第三次：
#
#     left = 0, right = 1
#     mid = 0
#     data[0] = 1 < 3
#     left = 1
#
# 此时：
#
#     left = 1, right = 1
#
# 返回 1。
#
# 下标 1 对应题目中的第 2 个位置，
# 所以输出：
#
#     index + 1 = 2
#
#
# 九、具体例子：查找不存在的 4
#
#     data = [1, 3, 3, 3, 5]
#     target = 4
#
# 二分结束后：
#
#     left = 4
#
# 因为：
#
#     data[0]、data[1]、data[2]、data[3] < 4
#     data[4] = 5 >= 4
#
# 但：
#
#     data[4] != 4
#
# 所以 target 不存在，输出 -1。
#
#
# 十、为什么要判断 `index < n`
#
# 如果 target 大于数组中的所有元素，
# `bisect_left` 会返回：
#
#     index = n
#
# 例如：
#
#     data = [1, 3, 5]
#     target = 10
#
# 返回：
#
#     index = 3
#
# 但数组最大下标是 2，
# 直接访问 data[3] 会越界。
#
# 所以代码先判断：
#
#     if index < n and data[index] == target:
#
# Python 的 `and` 具有短路特性：
# 如果 index < n 不成立，
# 就不会继续访问 data[index]。
#
#
# 十一、为什么输出 `index + 1`
#
# Python 下标从 0 开始：
#
#     data[0] 是第 1 个数；
#     data[1] 是第 2 个数。
#
# 题目中的编号从 1 开始，
# 因此：
#
#     题目编号 = Python 下标 + 1
#
# 代码：
#
#     out.append(index + 1)
#
# 正是在完成这个转换。
#
#
# 十二、为什么重复数字不会影响二分
#
# 数列是单调不减，而不是严格递增，
# 所以可能出现：
#
#     [1, 2, 2, 2, 5]
#
# 普通“找到一个 target”可能返回中间的 2，
# 但本题要求第一次出现。
#
# `bisect_left` 在遇到：
#
#     data[mid] >= target
#
# 时继续向左收缩：
#
#     right = mid
#
# 因此最终一定定位到最左边的符合位置。
#
#
# 十三、算法流程
#
#     1. 读入单调不减数组；
#     2. 对每个查询值 target 执行二分；
#     3. 找到第一个 data[index] >= target 的位置；
#     4. 判断该位置是否真的等于 target；
#     5. 若相等，输出 index + 1；
#     6. 否则输出 -1。
#
#
# 十四、复杂度分析
#
# 每次二分都会把搜索区间缩小约一半，
# 因此单次查询的时间复杂度为：
#
#     O(log n)
#
# m 次查询的总时间复杂度为：
#
#     O(m log n)
#
# 保存数组需要：
#
#     O(n)
#
# 保存输出结果需要：
#
#     O(m)
#
# 总空间复杂度为：
#
#     O(n + m)
