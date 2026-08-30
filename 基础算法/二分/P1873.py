import sys
# 二分答案模板 最大可行值

def main():
    input = sys.stdin.buffer.readline
    n,m = map(int,input().split())
    data = list(map(int,input().split()))

    left = 0
    right = max(data)+1 #左闭右开[left,right)

    def check(h):
        wood = 0
        for height in data:
            if height > h:
                wood += height - h
                if wood >= m:
                    return True
        return False

    while right - left > 1:
        mid = (left + right) // 2
        if check(mid):
            left = mid #mid可行，尝试更大的高度
        else:
            right = mid #mid不可行，尝试更小的高度

    sys.stdout.buffer.write(str(left).encode())

if __name__ == '__main__':
    main()


# ============================================================
# 二分答案：算法理论、思路与实现细节
# ============================================================
#
# 一、题目要求
#
# 选择一个尽可能高的锯片高度 H，使得所有树被锯下的木材总长度至少为 m。
#
# 如果一棵树的高度为 height，那么它贡献的木材长度为：
#
#     max(0, height - H)
#
# 因此，固定锯片高度 H 后，木材总长度为：
#
#     wood(H) = sum(max(0, height - H))
#
#
# 二、为什么这是二分答案
#
# 本题不是在一个有序数组中查找元素，
# 而是在所有可能的答案 H 中寻找最优值。
#
# 这种“答案范围很大，但可以快速判断某个答案是否可行”的问题，
# 可以使用二分答案。
#
# 对于一个候选高度 H，可以定义判断函数：
#
#     check(H) = wood(H) >= m
#
# 如果 check(H) 为 True，说明锯片高度 H 可以获得至少 m 米木材，
# 因此 H 是可行答案。
#
# 如果 check(H) 为 False，说明高度 H 太高，得到的木材不够，
# 因此 H 不可行。
#
#
# 三、可行性函数为什么具有单调性
#
# 当锯片高度从 H 提高到 H + 1 时，
# 每棵树被砍下的部分只会减少或保持不变，
# 不可能增加。
#
# 所以：
#
#     H 越小，wood(H) 越大；
#     H 越大，wood(H) 越小。
#
# 可行性呈现如下形式：
#
#     高度较低：可行
#     高度较高：可行
#     某个分界点之后：不可行
#
# 本题要求的是：
#
#     最后一个可行的 H
#
# 这正是二分答案可以解决的单调问题。
#
#
# 四、check 函数的含义
#
# 代码：
#
#     def check(h):
#         wood = 0
#         for height in data:
#             if height > h:
#                 wood += height - h
#                 if wood >= m:
#                     return True
#         return False
#
# 对每棵树：
#
#     height <= h
#
# 说明树不高于锯片，不会被砍下木材，贡献为 0。
#
#     height > h
#
# 说明会被砍下 height - h 米。
#
# 当累计木材已经达到 m 时，可以立即返回 True，
# 因为后面的树不再影响“是否至少得到 m 米”的判断。
#
#
# 五、二分边界的含义
#
# 代码使用：
#
#     left = 0
#     right = max(data) + 1
#
# 并把搜索区间理解为：
#
#     left 始终是可行高度；
#     right 始终是不可行高度。
#
# 为什么 left = 0 可行？
#
# 锯片高度为 0 时，所有树都被砍掉，
# 得到的木材是所有树高之和。
# 题目保证树木总高度大于 m，
# 所以 H = 0 一定可行。
#
# 为什么 right = max(data) + 1 不可行？
#
# 这个高度比最高的树还高，
# 不会砍下任何木材，总木材为 0，
# 而 m >= 1，所以一定不可行。
#
# 这里的 right 是一个“不可行哨兵”，
# 它不是真正需要枚举的答案。
#
#
# 六、为什么可行时是 left = mid
#
# 代码：
#
#     if check(mid):
#         left = mid
#     else:
#         right = mid
#
# 如果 mid 可行，那么 mid 可能正好就是最大的可行高度，
# 不能把它排除，所以要保留 mid：
#
#     left = mid
#
# 如果 mid 不可行，那么 mid 和比它更高的高度都不可能满足要求，
# 因此保留右边界作为不可行位置：
#
#     right = mid
#
#
# 七、为什么循环条件是 right - left > 1
#
# 每轮循环后都要让区间严格缩小。
#
# 当：
#
#     right - left == 1
#
# 说明两个边界相邻，例如：
#
#     left = 15   # 可行
#     right = 16  # 不可行
#
# 此时 15 已经是最后一个可行高度，
# 答案就是 left，不需要继续循环。
#
# 如果使用：
#
#     while right > left:
#
# 当 left = 15、right = 16 时：
#
#     mid = (15 + 16) // 2 = 15
#
# 如果 mid 可行，执行 left = mid，
# left 仍然是 15，状态不会变化，可能造成死循环。
#
# 因此当前这种“可行左边界 + 不可行右边界”的写法，
# 必须使用：
#
#     while right - left > 1:
#
#
# 八、循环结束时为什么输出 left
#
# 循环结束时：
#
#     right - left <= 1
#
# 由于 left 可行、right 不可行，
# 且两者不能相等，所以一定有：
#
#     right = left + 1
#
# 因此 left 正好是最后一个可行高度，
# 也就是题目要求的最高锯片高度。
#
#
# 九、一个简单例子
#
# 树高为：
#
#     [20, 15, 10, 17]
#
# 需要木材：
#
#     m = 7
#
# 当 H = 15 时：
#
#     (20 - 15) + (17 - 15) = 5 + 2 = 7
#
# 所以 H = 15 可行。
#
# 当 H = 16 时：
#
#     (20 - 16) + (17 - 16) = 4 + 1 = 5
#
# 木材不足，H = 16 不可行。
#
# 因此答案是：
#
#     15
#
# 二分最终会得到：
#
#     left = 15   # 最大可行高度
#     right = 16  # 最小不可行高度
#
#
# 十、另一种常见二分写法
#
# 本文件采用的是：
#
#     left 可行，right 不可行
#     while right - left > 1
#     可行时 left = mid
#
# 也可以使用左闭右闭区间：
#
#     left = 0
#     right = max(data)
#     answer = 0
#
#     while left <= right:
#         mid = (left + right) // 2
#         if check(mid):
#             answer = mid
#             left = mid + 1
#         else:
#             right = mid - 1
#
# 这种写法在 check(mid) 可行时用 left = mid + 1，
# 是因为 mid 已经被保存到 answer 中，
# 下一轮要继续搜索比 mid 更大的答案。
#
# 两种写法都正确，关键是边界含义、循环条件和更新方式必须匹配。
#
#
# 十一、算法流程
#
#     1. 读入树的数量 n、所需木材 m 和每棵树的高度；
#     2. 设置可行边界 left = 0；
#     3. 设置不可行边界 right = 最高树高 + 1；
#     4. 取中间高度 mid；
#     5. 用 check(mid) 计算木材是否达到 m；
#     6. 若可行，尝试提高锯片高度；
#     7. 若不可行，降低锯片高度；
#     8. 当两个边界相邻时停止；
#     9. 输出 left。
#
#
# 十二、正确性直觉
#
# check(H) 能够正确判断高度 H 是否可行，
# 因为它逐棵计算了在 H 高度下能够砍下的木材。
#
# 木材总量随着 H 增大而不增加，
# 所以可行高度构成一个连续的前缀：
#
#     0, 1, ..., answer
#
# 不可行高度从 answer + 1 开始。
#
# 二分始终保留一个可行高度 left 和一个不可行高度 right，
# 每次排除一半不可能的答案，
# 最终得到最大的可行高度 left。
#
#
# 十三、复杂度分析
#
# 设最高树高为 h_max。
#
# 二分高度范围需要进行 O(log h_max) 次判断，
# 每次 check 都遍历 n 棵树，时间复杂度为 O(n)。
#
# 因此总时间复杂度为：
#
#     O(n log h_max)
#
# 保存树高数组需要：
#
#     O(n)
#
# 二分过程只使用常数个变量，
# 所以额外空间复杂度为：
#
#     O(1)
