import sys
# 二分答案 贪心 最大可行值

def main():
    input = sys.stdin.buffer.readline
    L,N,M = map(int,input().split())

    data = []
    for _ in range(N):
        data.append(int(input()))

    position = [0] + data + [L]

    def check(dist):
        remove_cnt = 0
        last_save = 0
        for i in range(1,N+2):
            if position[i] - position[last_save] < dist:
                remove_cnt +=1
            else:
                last_save = i

        if remove_cnt <= M:
            return True
        else:
            return False

    left = 0
    right = L
    # ans = 0

    while left <= right:
        mid = (left + right) // 2
        if check(mid):
            # ans = mid
            left = mid + 1
        else:
            right = mid - 1
    

    sys.stdout.buffer.write(str(right).encode())
if __name__ == '__main__':
    main()


# ============================================================
# 二分答案 + 贪心：算法理论、思路与实现细节
# ============================================================
#
# 一、题目要求
#
# 河道起点位于 0，终点位于 L，
# 中间有 N 块岩石。
#
# 选手只能在相邻的保留岩石之间跳跃。
# 组委会最多移走 M 块中间岩石，
# 目标是让所有跳跃距离中的最小值尽可能大。
#
# 设某种移石方案下的所有跳跃距离为：
#
#     d1, d2, ..., dt
#
# 那么这套方案的难度是：
#
#     min(d1, d2, ..., dt)
#
# 题目要求最大化这个最小值。
#
#
# 二、二分答案的转化
#
# 不直接求最大的最短跳跃距离，
# 而是先假设一个候选答案 dist：
#
#     假设所有相邻保留岩石之间的距离都至少为 dist，
#     判断最多移走 M 块岩石能否做到。
#
# 这就是 check(dist) 的含义。
#
# 如果 check(dist) 为 True，
# 说明最短跳跃距离至少可以达到 dist。
#
# 如果 check(dist) 为 False，
# 说明 dist 太大，无法在移走 M 块岩石以内完成。
#
#
# 三、为什么具有单调性
#
# 如果最短跳跃距离至少为 dist 的方案存在，
# 那么要求最短跳跃距离至少为 dist - 1 时，
# 原来的方案仍然满足要求。
#
# 因此：
#
#     dist 越小，越容易满足；
#     dist 越大，越难满足。
#
# 可行性呈现为：
#
#     True True True True False False
#                         ^
#                   最大可行距离
#
# 题目要求最后一个 True，
# 所以使用“最大可行值”的二分模板。
#
#
# 四、位置数组和两个端点
#
# 代码：
#
#     position = [0] + data + [L]
#
# 将起点 0 和终点 L 也加入数组。
#
# 这样所有相邻位置之间的差值就表示一次跳跃距离：
#
#     position[i] - position[last_save]
#
# 其中：
#
#     last_save
#
# 表示上一个保留下来的岩石下标。
#
# 起点和终点不能被移走，
# 但它们必须参与跳跃距离的判断。
#
#
# 五、check(dist) 中的贪心策略
#
# 代码从左到右扫描所有岩石：
#
#     if position[i] - position[last_save] < dist:
#         remove_cnt += 1
#     else:
#         last_save = i
#
# 当前岩石与上一个保留位置的距离小于 dist 时，
# 两者不能同时保留。
#
# 此时移走当前岩石，并让上一个保留位置保持不变：
#
#     remove_cnt += 1
#
# 如果距离至少为 dist，
# 就保留当前岩石：
#
#     last_save = i
#
# 这是一种“尽量保留左边位置”的贪心方法。
#
#
# 六、为什么贪心能让移除数量最少
#
# 假设当前保留位置是 last_save，
# 当前岩石位置是 position[i]。
#
# 如果：
#
#     position[i] - position[last_save] < dist
#
# 那么这两个位置不能同时保留。
#
# 对于当前岩石来说：
#
#     保留 last_save
#
# 可以让后面的岩石拥有更大的可用距离；
#
#     保留 position[i]
#
# 则可能使后续岩石距离它更近。
#
# 因此遇到距离不足时，删除当前岩石不会减少后续能够保留的岩石数量，
# 并且为后面留下更大的空间。
#
# 逐个位置采用这个策略，
# 最终得到在 dist 限制下所需移除的最少岩石数。
#
# 所以：
#
#     remove_cnt <= M
#
# 当且仅当候选距离 dist 可行。
#
#
# 七、关于终点的处理
#
# 代码把终点 L 也放入 position 中统一处理。
#
# 终点本身不能被移走，
# 当扫描到终点且最后一段距离不足 dist 时，
# 代码仍然把 remove_cnt 加一。
#
# 这个加一可以理解为：
#
#     为了让终点前的最后一跳达到 dist，
#     至少还需要删除一个之前保留的中间岩石。
#
# 代码统计的是“还需要一次删除操作”，
# 并不是真的删除终点。
#
# 这种统一写法可以避免单独处理终点，
# 计数结果仍然等价于实际需要移走的中间岩石数量。
#
#
# 八、二分边界
#
# 代码使用：
#
#     left = 0
#     right = L
#
# 距离 0 一定可行，
# 因为任何相邻位置之间的距离都不小于 0。
#
# 距离 L 也可能可行：
#
#     如果只有起点和终点，
#     一次跳跃距离正好为 L。
#
# 因此不能把 right 当作“一定不可行”的哨兵，
# 当前程序使用的是闭区间二分。
#
#
# 九、当前程序使用的闭区间模板
#
# 代码：
#
#     while left <= right:
#         mid = (left + right) // 2
#
#         if check(mid):
#             left = mid + 1
#         else:
#             right = mid - 1
#
# 这是寻找“最大可行值”的模板。
#
# 如果 mid 可行：
#
#     mid 有可能是答案，
#     但还要尝试更大的距离：
#
#         left = mid + 1
#
# 如果 mid 不可行：
#
#     mid 以及更大的距离都不可能可行，
#     所以：
#
#         right = mid - 1
#
#
# 十、为什么当前程序最后可以输出 right
#
# 在当前模板中：
#
#     可行时 left = mid + 1；
#     不可行时 right = mid - 1。
#
# 循环结束时一定有：
#
#     left = right + 1
#
# 因为题目中 dist = 0 一定可行，
# 所以至少存在一个可行答案。
#
# 最后的 right 就是：
#
#     最大的可行距离。
#
# 因此可以直接输出：
#
#     print(right)
#
# 也可以写成使用 answer 的形式：
#
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
#     print(answer)
#
# 两种写法都正确。
#
# 需要注意，不能看到 while left <= right
# 就无条件输出 right。
#
# 只有当更新规则是：
#
#     可行 -> left = mid + 1
#     不可行 -> right = mid - 1
#
# 并且目标是最大可行值时，
# 循环结束后的 right 才是最后一个可行值。
#
# 如果目标是最小可行值，
# 通常应输出 left，或者使用 answer 保存可行的 mid。
#
#
# 十一、三种二分模板对本题的写法
#
# 1. 闭区间模板：
#
#     left = 0
#     right = L
#
#     while left <= right:
#         mid = (left + right) // 2
#         if check(mid):
#             left = mid + 1
#         else:
#             right = mid - 1
#
#     answer = right
#
# 2. 哨兵边界模板：
#
#     left = 0              # 一定可行
#     right = L + 1         # 一定不可行
#
#     while right - left > 1:
#         mid = (left + right) // 2
#         if check(mid):
#             left = mid
#         else:
#             right = mid
#
#     answer = left
#
# 3. 左闭右开模板：
#
#     left = 0
#     right = L + 1
#
#     while left < right:
#         mid = (left + right + 1) // 2
#         if check(mid):
#             left = mid
#         else:
#             right = mid - 1
#
#     answer = left
#
# 三种写法都能求最大可行距离，
# 但不能混合它们的循环条件和边界更新方式。
#
#
# 十二、样例分析
#
#     L = 25
#     岩石位置：2, 11, 14, 17, 21
#     M = 2
#
# 尝试 dist = 4：
#
#     0 -> 2       距离 2，不足 4，移走 2
#     0 -> 11      距离 11，保留 11
#     11 -> 14     距离 3，不足 4，移走 14
#     11 -> 17     距离 6，保留 17
#     17 -> 21     距离 4，保留 21
#     21 -> 25     距离 4，保留终点
#
# 共移走 2 块岩石，dist = 4 可行。
#
# 尝试 dist = 5 时，至少需要移走 3 块岩石，
# 超过 M = 2，因此 dist = 5 不可行。
#
# 所以答案为 4。
#
#
# 十三、算法流程
#
#     1. 把起点 0、所有中间岩石和终点 L 放入 position；
#     2. 猜测一个最短跳跃距离 dist；
#     3. 从左到右贪心统计需要移走的岩石数；
#     4. 如果移除数量不超过 M，dist 可行；
#     5. 如果 dist 可行，尝试更大的 dist；
#     6. 如果 dist 不可行，尝试更小的 dist；
#     7. 输出最大可行距离。
#
#
# 十四、正确性直觉
#
# 对固定的 dist，贪心会在距离不足时删除当前岩石，
# 保留更靠左的位置，从而给后续岩石留下最大的间隔。
# 因此它计算出的 remove_cnt 是达到 dist 所需的最少删除数。
#
# 当 remove_cnt <= M 时，说明可以在预算内完成移石；
# 当 remove_cnt > M 时，说明 dist 不可行。
#
# 又因为 dist 越大越难满足，
# 可行性具有单调性。
#
# 二分找到的最后一个可行 dist，
# 就是移走至多 M 块岩石后，最短跳跃距离的最大值。
#
#
# 十五、复杂度分析
#
# 每次 check 需要扫描 N + 1 个相邻位置，
# 时间复杂度为：
#
#     O(N)
#
# 距离范围为 [0, L]，
# 二分次数为：
#
#     O(log L)
#
# 总时间复杂度为：
#
#     O(N log L)
#
# position 数组保存起点、终点和所有中间岩石，
# 空间复杂度为：
#
#     O(N)
