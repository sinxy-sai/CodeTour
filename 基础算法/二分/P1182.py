import sys
# 二分答案 贪心 最小可行值

def main():
    input = sys.stdin.buffer.readline
    n,m = map(int,input().split())
    data = list(map(int,input().split()))

    left = max(data)
    right = sum(data)

    def check(limit):
        segments = 1
        current_sum = 0

        for x in data:
            if current_sum + x <= limit:
                current_sum += x
            else:
                current_sum = x
                segments += 1

        if segments <= m:
            return True
        else:
            return False

    while left <= right:
        mid = (left + right) // 2
        if check(mid):
            right = mid - 1 # 当 mid 是可行答案时，尝试更小的 mid
        else:
            left = mid + 1

    print(left)
if __name__ == '__main__':
    main()


# ============================================================
# 二分答案 + 贪心：算法理论、思路与实现细节
# ============================================================
#
# 一、题目要求
#
# 将一个正整数数列分成 m 段，每一段必须连续，
# 使所有段的和中的最大值尽可能小。
#
# 例如：
#
#     4 2 4 5 1
#
# 分成 3 段时，可以分为：
#
#     [4 2] [4] [5 1]
#
# 各段的和为 6、4、6，
# 最大段和为 6。
#
# 本题要求的就是所有分法中“最大段和”的最小值。
#
#
# 二、把最优化问题转化为判定问题
#
# 直接求最优分法比较困难，
# 可以先猜一个答案 limit：
#
#     假设每一段的和都不能超过 limit，
#     判断能否把数列分成不超过 m 段。
#
# 这就是 check(limit) 要完成的工作。
#
# 如果可以在不超过 m 段的情况下完成分段，
# 说明 limit 是可行的。
#
# 如果最少也需要超过 m 段，
# 说明 limit 太小，不可行。
#
#
# 三、为什么 check 函数使用贪心
#
# 代码从左到右处理每个数字：
#
#     if current_sum + x <= limit:
#         current_sum += x
#     else:
#         current_sum = x
#         segments += 1
#
# 当前数字能够放入当前段时，就继续放入；
# 如果放入后超过 limit，就必须从当前数字开始新的一段。
#
# 这种做法会让每一段尽可能多地放入数字，
# 从而使使用的段数尽可能少。
#
# 为什么段数最少很重要？
#
# 如果在限制 limit 下，贪心算法都需要超过 m 段，
# 那么任何其他分法都不可能使用不超过 m 段。
#
# 因为其他分法如果提前切段，只会让前面的段更短，
# 不会比“尽量延后切段”的方法使用更少的段数。
#
#
# 四、check(limit) 的正确性直觉
#
# 对于每个数字 x：
#
#     1. 如果 current_sum + x <= limit，
#        放入当前段不会违反限制；
#
#     2. 如果 current_sum + x > limit，
#        当前段已经不能再放 x，
#        只能在 x 前面切一刀。
#
# 由于数组元素不能拆分，且每段必须连续，
# 这次切分是被 limit 强制出来的。
#
# 因此贪心算法得到的是在 limit 限制下的最少段数。
#
# 最后：
#
#     segments <= m
#
# 表示 limit 可行。
#
# 题目要求“恰好分成 m 段”，
# 但判断时使用“不超过 m 段”仍然正确。
#
# 原因是数组中的元素都是非负数：
# 如果某种分法只用了少于 m 段，
# 可以继续在某些段内部切开，
# 不会增大任何一段的和。
# 因此一定可以调整为恰好 m 段。
#
#
# 五、答案范围
#
# 每一段至少包含一个元素，
# 所以最大段和不可能小于数列中的最大元素：
#
#     left = max(data)
#
# 如果限制等于整个数列的总和，
# 可以不切分，只有一段：
#
#     right = sum(data)
#
# 因为 m <= n，且允许继续切分，
# 所以答案一定在：
#
#     [max(data), sum(data)]
#
# 之间。
#
#
# 六、为什么具有单调性
#
# 假设限制 limit 可行，
# 说明可以把数列分成不超过 m 段，
# 且每段和都不超过 limit。
#
# 如果把限制增大为 limit + 1，
# 原来的分法仍然满足要求，
# 因此 limit + 1 也一定可行。
#
# 所以可行性呈现为：
#
#     较小限制：不可行
#     较大限制：可行
#
# 形式如下：
#
#     False False False True True True
#                          ^
#                    第一个可行值
#
# 本题要找的是“第一个可行值”。
#
#
# 七、当前程序使用的二分模板
#
# 程序使用：
#
#     left = max(data)
#     right = sum(data)
#
#     while left <= right:
#         mid = (left + right) // 2
#
#         if check(mid):
#             right = mid - 1
#         else:
#             left = mid + 1
#
# 这是“闭区间 + 记录边界”的写法。
#
# 当 check(mid) 为 True：
#
#     mid 可行，但还可能存在更小的可行答案，
#     所以向左搜索：
#
#         right = mid - 1
#
# 当 check(mid) 为 False：
#
#     mid 太小，必须增大限制，
#     所以向右搜索：
#
#         left = mid + 1
#
# 循环结束时，left 就是第一个可行值。
#
#
# 八、三种常见二分模板
#
# 二分没有唯一固定写法。
# 下面三种模板都可以正确实现二分，
# 但区间含义、循环条件和边界更新方式必须互相匹配。
#
#
# ------------------------------------------------------------
# 模板一：while left <= right
# ------------------------------------------------------------
#
# 这是闭区间模板，搜索区间表示为：
#
#     [left, right]
#
# 只要 left <= right，区间中就仍然有候选答案。
#
# 求最小可行值的写法：
#
#     left = lower_bound
#     right = upper_bound
#
#     while left <= right:
#         mid = (left + right) // 2
#
#         if check(mid):
#             right = mid - 1
#         else:
#             left = mid + 1
#
#     answer = left
#
# 适用于 P1182：
#
#     check(limit) 为 True：
#         limit 可行，尝试更小；
#     check(limit) 为 False：
#         limit 不可行，必须更大。
#
# 求最大可行值时：
#
#     answer = lower_bound - 1
#
#     while left <= right:
#         mid = (left + right) // 2
#
#         if check(mid):
#             answer = mid
#             left = mid + 1
#         else:
#             right = mid - 1
#
#     输出 answer
#
# 这种写法需要显式保存 answer，
# 或者根据循环结束时的 left/right 判断答案。
#
#
# ------------------------------------------------------------
# 模板二：while right - left > 1
# ------------------------------------------------------------
#
# 这种写法通常使用两个哨兵：
#
#     left：一定可行或一定满足某种条件；
#     right：一定不可行或一定不满足某种条件。
#
# 搜索区间不是普通的 [left, right]，
# 而是不断把两个边界缩小到相邻位置。
#
# P1182 求最小可行值时，可以写成：
#
#     left = max(data) - 1  # 一定不可行
#     right = sum(data)     # 一定可行
#
#     while right - left > 1:
#         mid = (left + right) // 2
#
#         if check(mid):
#             right = mid
#         else:
#             left = mid
#
#     answer = right
#
# 因为本题寻找第一个可行值，
# 所以左边放不可行值，右边放可行值。
#
# 如果求最大可行值，则反过来：
#
#     left = 0              # 一定可行的虚拟边界
#     right = max_value + 1 # 一定不可行
#
#     while right - left > 1:
#         mid = (left + right) // 2
#
#         if check(mid):
#             left = mid
#         else:
#             right = mid
#
#     answer = left
#
# 这种模板中，不能写成 while left < right，
# 因为当两个边界相邻时，
# 普通下取中点可能等于 left，
# 导致边界不再变化。
#
#
# ------------------------------------------------------------
# 模板三：while left < right
# ------------------------------------------------------------
#
# 这种模板常用左闭右开区间：
#
#     [left, right)
#
# 右端点 right 不属于当前搜索区间。
#
# 求第一个满足条件的位置：
#
#     left = 0
#     right = n
#
#     while left < right:
#         mid = (left + right) // 2
#
#         if check(mid):
#             right = mid
#         else:
#             left = mid + 1
#
#     answer = left
#
# 这里当 mid 满足条件时保留 mid：
#
#     right = mid
#
# 因为 mid 可能就是第一个满足条件的位置。
#
# 当 mid 不满足条件时排除 mid：
#
#     left = mid + 1
#
# P2249 中的 `bisect_left` 就是这种思想：
#
#     寻找第一个 data[i] >= target 的位置。
#
# 对 P1182，也可以使用“第一个可行值”的形式：
#
#     left = max(data)
#     right = sum(data) + 1
#
#     while left < right:
#         mid = (left + right) // 2
#
#         if check(mid):
#             right = mid
#         else:
#             left = mid + 1
#
#     answer = left
#
# 这里 right 是右开边界，
# 它可以等于 sum(data) + 1。
#
#
# 九、三种模板的区别总结
#
# +--------------------------+----------------------+----------------------+
# | 循环条件                 | 区间或边界含义       | 常见用途             |
# +--------------------------+----------------------+----------------------+
# | while left <= right      | 闭区间 [left, right] | 普通二分、记录答案   |
# | while right - left > 1   | 两个哨兵逐渐相邻     | 可行/不可行边界二分  |
# | while left < right       | 左闭右开 [left,right)| lower_bound、找首个值|
# +--------------------------+----------------------+----------------------+
#
# 对于“最小可行值”：
#
#     可行时通常向左：
#         right = mid
#         或 right = mid - 1
#
# 对于“最大可行值”：
#
#     可行时通常向右：
#         left = mid
#         或 left = mid + 1
#
# 但具体是否加减 1，
# 取决于当前使用的是闭区间还是哨兵边界。
#
#
# 十、为什么不同模板不能混用
#
# 例如：
#
#     while right - left > 1:
#         mid = (left + right) // 2
#         if check(mid):
#             left = mid
#
# 这是“最大可行值”的更新方式。
#
# 如果在求最小可行值时仍然写成：
#
#     left = mid
#
# 就会把可行的 mid 放到左边，
# 最后得到的可能是最后一个不可行值，
# 而不是第一个可行值。
#
# 因此写二分前应先明确：
#
#     1. 要找第一个可行值，还是最后一个可行值；
#     2. 使用闭区间、左闭右开区间，还是哨兵边界；
#     3. mid 是否仍然可能是答案；
#     4. 更新边界时是否需要加一或减一。
#
#
# 十一、算法流程
#
#     1. 读入数列和需要的段数 m；
#     2. 设定最大段和的最小可能值 max(data)；
#     3. 设定最大段和的最大可能值 sum(data)；
#     4. 猜测一个最大段和 limit；
#     5. 使用贪心计算 limit 下的最少分段数；
#     6. 如果段数不超过 m，说明 limit 可行；
#     7. 二分寻找最小的可行 limit；
#     8. 输出该 limit。
#
#
# 十二、正确性直觉
#
# 对固定的 limit，贪心算法每次都尽可能延长当前段，
# 因而得到满足段和限制时的最少段数。
#
# 如果贪心得到的段数超过 m，
# 那么任何分法都无法在 limit 下完成要求。
#
# 如果贪心得到的段数不超过 m，
# 则 limit 可行；由于元素非负，
# 可以继续切分为恰好 m 段。
#
# 同时，limit 越大越容易满足分段要求，
# 所以 check(limit) 具有单调性。
#
# 二分最终找到第一个可行的 limit，
# 这就是所有分段方案中最大段和的最小值。
#
#
# 十三、复杂度分析
#
# 设数列元素总和为 S。
#
# 二分的答案范围最多为 S，
# 所以二分次数为：
#
#     O(log S)
#
# 每次 check 都遍历整个数列，
# 时间复杂度为 O(n)。
#
# 总时间复杂度为：
#
#     O(n log S)
#
# 保存数列需要：
#
#     O(n)
#
# 二分过程使用常数个变量，
# 所以额外空间复杂度为：
#
#     O(1)
