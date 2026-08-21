# 状压DP/状态压缩搜索
# 位运算
# 状态压缩
# 记忆化搜索
# 状压 DP
# 访问集合
import sys
import math
from functools import cache

def main():
    input = sys.stdin.buffer.readline
    n = int(input())

    points = [(0.0,0.0)]

    for _ in range(n):
        points.append(tuple(map(float,input().split())))

    # dist[i][j] 表示 points[i] 和 points[j] 之间的距离
    dist = [[0.0]*(n+1) for _ in range(n+1)]
    # 预计算dist数组
    for i in range(n+1):
        x1,y1 = points[i]
        for j in range(n+1):
            x2,y2 = points[j]
            dist[i][j] = math.sqrt((x1-x2)**2+(y1-y2)**2)

    @cache
    def dfs(mask,last):
        '''
        args:
            mask: 已经吃掉的奶酪集合
            last: 最后吃掉的奶酪编号
        return:
        从起点出发，吃掉mask中所有奶酪，最后停在last处奶酪的最短距离
        '''

        # 只有一个奶酪被吃
        if mask == (1 << (last-1)):
            return dist[0][last]

        # 去掉last，得到上一步之前按已经吃掉的奶酪集合
        previous_mask = mask ^ (1 << (last - 1))

        best = float('inf')

        for previous in range(1,n+1):
            bit = 1 << (previous - 1)

            # 如果previous_mask中没有previous，跳过
            if not (previous_mask & bit):
                continue

            candidate = dfs(previous_mask,previous) + dist[previous][last]

            best = min(best,candidate)

        return best

    full_mask = (1 << n) - 1

    ans = min(dfs(full_mask,last) for last in range(1,n+1))

    sys.stdout.write(f"{ans:.2f}")
    
if __name__ == '__main__':
    main()


# ============================================================
# P1433 吃奶酪：理论、算法思路与细节
# ============================================================
#
# 一、题目考查的知识点
#
# 1. DFS 搜索：尝试下一块还没有吃过的奶酪。
# 2. 状态压缩：用一个整数的二进制位表示奶酪是否已经吃过。
# 3. 记忆化搜索：缓存已经计算过的状态，避免重复计算。
# 4. 动态规划：当前状态由更小的子状态转移而来。
# 5. 欧几里得距离：计算平面上两个点之间的距离。
#
#
# 二、题目为什么不能直接枚举排列
#
# 老鼠要把 n 块奶酪全部吃掉，每块奶酪只能吃一次。
# 如果直接枚举吃奶酪的顺序，就是枚举 n 个元素的全排列，共有：
#
#     n!
#
# 种顺序。
#
# 当 n = 15 时，15! 很大，直接枚举每一种完整顺序会比较慢。
# 但是，不同的路线可能会到达同一个“已吃集合”和“当前位置”。
# 只要这两个条件相同，后续能够走出的最短距离就相同。
# 因此可以把这些重复情况合并成一个状态。
#
#
# 三、状态压缩
#
# 一共有 n 块奶酪，用一个整数 mask 表示哪些奶酪已经吃过。
#
# 约定：
#
#     第 0 位表示 1 号奶酪
#     第 1 位表示 2 号奶酪
#     第 2 位表示 3 号奶酪
#     ...
#
# 某一位是 1，表示对应奶酪已经吃过；
# 某一位是 0，表示对应奶酪还没有吃。
#
# 例如 n = 4：
#
#     mask = 0101
#
# 表示：
#
#     1 号奶酪已经吃过
#     2 号奶酪没有吃
#     3 号奶酪已经吃过
#     4 号奶酪没有吃
#
# 原本可以用集合 {1, 3} 表示，现在用整数 5 的二进制形式 0101
# 表示，这种把集合压缩成整数的方式就叫“状态压缩”。
#
#
# 四、完整状态为什么是 dfs(mask, last)
#
# 代码中的状态是：
#
#     dfs(mask, last)
#
# 含义是：
#
#     已经吃掉 mask 表示的所有奶酪，
#     当前最后停在 last 号奶酪，
#     返回从起点出发到达这里的最短距离。
#
# 只记录 mask 不够，因为下一步的距离取决于老鼠当前所在的位置。
#
# 例如已经吃过 1、2、3 号奶酪：
#
#     1 -> 2 -> 3
#
# 和：
#
#     2 -> 1 -> 3
#
# 虽然吃奶酪的集合相同，但只有记录最后停在 3 号奶酪，才能知道下一步
# 是从 3 号奶酪出发。
#
#
# 五、二进制位运算
#
# 第 i 块奶酪对应的二进制位是：
#
#     bit = 1 << (i - 1)
#
# 例如：
#
#     i = 3
#     bit = 1 << 2 = 0100
#
# 1. 判断第 i 块奶酪是否已经吃过：
#
#     mask & bit
#
# 如果结果为 0，表示这一位是 0，奶酪没有吃过；
# 如果结果不为 0，表示这一位是 1，奶酪已经吃过。
#
# 2. 加入一块奶酪：
#
#     mask | bit
#
# 3. 删除一块奶酪：
#
#     mask ^ bit
#
# 当前状态中 last 一定已经被吃掉，所以 last 对应的位一定是 1，
# 因此可以用异或把它变回 0：
#
#     previous_mask = mask ^ (1 << (last - 1))
#
#
# 六、递归终止条件
#
# 如果：
#
#     mask == (1 << (last - 1))
#
# 说明 mask 中只有 last 这一块奶酪。
#
# 此时路线没有经过其他奶酪，只能是：
#
#     起点 -> last
#
# 所以直接返回：
#
#     dist[0][last]
#
# 其中 0 号点表示起点 (0, 0)。
#
#
# 七、状态转移
#
# 当前要求计算：
#
#     dfs(mask, last)
#
# 因为最后吃的是 last，所以在吃 last 之前，老鼠一定在某一块
# previous 奶酪处。
#
# 先去掉 last：
#
#     previous_mask = mask ^ (1 << (last - 1))
#
# 然后枚举 previous_mask 中的每一块奶酪作为上一步：
#
#     dfs(previous_mask, previous) + dist[previous][last]
#
# 其中：
#
#     dfs(previous_mask, previous)
#
# 表示已经吃掉 previous_mask 中的奶酪，并且最后停在 previous；
#
#     dist[previous][last]
#
# 表示从 previous 走到 last。
#
# 所以状态转移方程是：
#
#     dfs(mask, last)
#     =
#     min(
#         dfs(previous_mask, previous)
#         + dist[previous][last]
#     )
#
# 代码中的：
#
#     if not (previous_mask & bit):
#         continue
#
# 表示如果 previous 不在 previous_mask 中，就不能作为上一步，直接跳过。
#
#
# 八、为什么最后还要枚举最后一块奶酪
#
#     full_mask = (1 << n) - 1
#
# 当 n = 4 时：
#
#     1 << n = 10000
#     (1 << n) - 1 = 01111
#
# 这表示 1 到 n 号奶酪全部已经吃掉。
#
# 但是最后吃的是哪一块奶酪不确定，所以要计算：
#
#     dfs(full_mask, 1)
#     dfs(full_mask, 2)
#     ...
#     dfs(full_mask, n)
#
# 最终答案是这些状态中的最小值。
#
#
# 九、@cache 与动态规划
#
# @cache 会按照函数参数缓存返回值。
#
# 例如 dfs(0111, 3) 第一次计算后，结果会被保存。
# 之后再次遇到 dfs(0111, 3) 时，直接返回保存的结果，不再递归计算。
#
# 这种写法叫“记忆化搜索”：
#
#     形式上：从目标状态递归到更小状态；
#     实质上：每个状态只计算一次；
#     本质上：自顶向下的动态规划。
#
# 所以这道题既可以说是记忆化搜索，也可以说是状态压缩 DP。
#
#
# 十、距离预处理
#
# 两个点 (x1, y1)、(x2, y2) 的欧几里得距离是：
#
#     sqrt((x1 - x2)^2 + (y1 - y2)^2)
#
# 程序先计算所有点对之间的距离：
#
#     dist[i][j]
#
# 其中：
#
#     0 号点是起点 (0, 0)
#     1 到 n 号点是奶酪
#
# 这样状态转移时可以直接查表，不需要重复计算平方根。
#
#
# 十一、复杂度
#
# mask 一共有 2^n 种，last 有 n 种，因此状态数量最多是：
#
#     O(n * 2^n)
#
# 每个状态最多枚举 n 个 previous，所以时间复杂度是：
#
#     O(n^2 * 2^n)
#
# 距离预处理需要：
#
#     O(n^2)
#
# 记忆化搜索的空间复杂度：
#
#     O(n * 2^n)
#
# 距离数组的空间复杂度：
#
#     O(n^2)
#
# 总空间复杂度：
#
#     O(n * 2^n + n^2)
#
# n <= 15 时，这种算法可以接受。
