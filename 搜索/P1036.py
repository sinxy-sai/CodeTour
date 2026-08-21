# 基础回溯
# DFS 枚举组合
# 递归参数设计
# 避免重复方案
# 搜索结束条件
# 记忆化搜索
# 动态规划
import sys
from functools import cache

def isPrime(num):
    if (num <= 1):
        return False

    if (num == 2):
        return True
    
    if (num % 2 == 0):
        return False
    
    for i in range(3,int(num**0.5)+1,2):
        if (num % i == 0):
            return False
    return True

def main():
    input = sys.stdin.readline
    n,k = map(int,input().strip().split())
    data = list(map(int,input().strip().split()))

    @cache
    def dfs(index,remain_count,current_sum):
        if remain_count == 0:
            return int(isPrime(current_sum))

        if index < 0 or remain_count < 0:
            return 0

        if index + 1 < remain_count:
            return 0

        not_choose = dfs(index-1,remain_count,current_sum )

        choose = dfs(index-1,remain_count-1,current_sum+data[index])

        return not_choose + choose

    ans = dfs(n-1,k,0)

    sys.stdout.write(str(ans))

if __name__ == '__main__':
    main()


# ==================== 理论、算法思路与细节 ====================
#
# 一、题目本质
#
# 从 n 个数中选择 k 个数，
# 判断它们的和是否为素数，
# 统计和为素数的组合数量。
#
# 这里的“选择 k 个数”指选择下标不同的数字。
# 选择顺序不重要：
#
#     3 + 7 + 19
#
# 和：
#
#     19 + 7 + 3
#
# 属于同一种组合。
#
#
# 二、为什么使用 DFS
#
# 每个数字都有两种选择：
#
#     选择当前数字
#     不选择当前数字
#
# 因此可以使用 DFS 枚举所有选择方案。
#
# 代码中的递归函数是：
#
#     dfs(index, remain_count, current_sum)
#
# 它表示：
#
#     只考虑下标 0 到 index 的数字，
#     还需要选择 remain_count 个数字，
#     当前已经选择的数字和为 current_sum，
#     返回最终能够得到多少个合法方案。
#
#
# 三、三个递归参数
#
# 1. index
#
# index 是当前正在考虑的最大下标。
#
# 如果：
#
#     index = 3
#
# 那么当前可以使用：
#
#     data[0], data[1], data[2], data[3]
#
# 一共有：
#
#     index + 1
#
# 个数字。
#
#
# 2. remain_count
#
# 表示还需要选择多少个数字。
#
# 初始时：
#
#     remain_count = k
#
# 每选择一个数字：
#
#     remain_count -= 1
#
#
# 3. current_sum
#
# 表示当前已经选择的数字和。
#
# 不选择当前数字时，和不变；
# 选择当前数字时：
#
#     current_sum + data[index]
#
#
# 四、递归终止条件
#
# 代码：
#
#     if remain_count == 0:
#         return int(isPrime(current_sum))
#
# 表示已经选择够 k 个数字。
#
# 此时不再继续枚举，
# 直接判断 current_sum 是否为素数。
#
#     是素数：返回 1
#     不是素数：返回 0
#
# 这里返回 1 或 0，
# 是因为 dfs 返回的是“方案数量”。
#
#
# 五、为什么要先判断 remain_count == 0
#
# 当前代码的判断顺序是：
#
#     if remain_count == 0:
#         ...
#
#     if index < 0 or remain_count < 0:
#         return 0
#
# 这个顺序不能随意交换。
#
# 如果：
#
#     index = -1
#     remain_count = 0
#
# 说明所有数字都处理完了，
# 并且刚好选够了 k 个数字。
#
# 这时应该判断 current_sum 是否为素数，
# 而不是直接返回 0。
#
#
# 六、剩余数字不够时剪枝
#
# 代码：
#
#     if index < 0 or remain_count < 0:
#         return 0
#
# 如果 index < 0，
# 表示已经没有数字可以选择。
#
# 如果 remain_count < 0，
# 表示选择数量已经超过 k，
# 这个状态不可能是合法方案。
#
# 代码还判断：
#
#     if index + 1 < remain_count:
#         return 0
#
# 从下标 0 到 index 一共有：
#
#     index + 1
#
# 个数字。
#
# 如果：
#
#     index + 1 < remain_count
#
# 说明剩余数字数量少于还需要选择的数量，
# 不可能选够，直接返回 0。
#
# 例如：
#
#     index = 1
#     remain_count = 3
#
# 当前只有 data[0] 和 data[1] 两个数字，
# 但还需要选择 3 个，
# 所以这个状态不可能成功。
#
#
# 七、不选当前数字
#
# 代码：
#
#     not_choose = dfs(
#         index - 1,
#         remain_count,
#         current_sum
#     )
#
# 表示：
#
#     不选择 data[index]，
#     接下来只考虑 data[0] 到 data[index - 1]。
#
# 因为当前数字已经决定“不选”，
# 所以 index 要减 1。
#
# 还需要选择的数量不变，
# 当前和也不变。
#
#
# 八、选择当前数字
#
# 代码：
#
#     choose = dfs(
#         index - 1,
#         remain_count - 1,
#         current_sum + data[index]
#     )
#
# 表示：
#
#     选择 data[index]，
#     接下来只考虑 data[0] 到 data[index - 1]。
#
# 选择了一个数字后：
#
#     remain_count 减 1
#     current_sum 加上 data[index]
#
# 选择当前数字后仍然要把 index 减 1，
# 因为当前数字已经处理完，
# 不允许再次选择同一个下标。
#
#
# 九、状态转移方程
#
# 设：
#
#     F(index, sum, remain)
#
# 表示当前状态的合法方案数。
#
# 那么：
#
#     F(index, sum, remain)
#
# 等于两种情况之和：
#
#     不选 data[index]
#     选择 data[index]
#
# 转移方程为：
#
#     F(index, sum, remain)
#       =
#     F(index - 1, sum, remain)
#       +
#     F(index - 1,
#       sum + data[index],
#       remain - 1)
#
# 这就是典型的 0/1 选择递推。
#
#
# 十、为什么需要 @cache
#
# 代码：
#
#     @cache
#     def dfs(...):
#
# 说明使用记忆化搜索。
#
# 不同的选择路径可能到达完全相同的状态：
#
#     (index, remain_count, current_sum)
#
# 从相同状态继续搜索，
# 后面的答案一定相同，
# 所以只需要计算一次。
#
# 第一次计算某个状态时，
# Python 会把结果缓存起来。
#
# 以后再次遇到相同参数：
#
#     dfs(index, remain_count, current_sum)
#
# 就直接返回之前的结果，
# 不再重复递归。
#
# 注意：
#
#     cache 减少的是重复计算，
#     不是把不同组合错误地合并。
#
# 如果相同状态由两条不同路径到达，
# 两个父状态仍然会分别使用这个状态的结果，
# 因此方案数量不会少算。
#
#
# 十一、为什么这也是动态规划
#
# 这段程序表面上使用的是递归，
# 但它同时具有动态规划的两个特征：
#
#     1. 存在重复子问题
#     2. 一个状态的答案可以由更小状态转移得到
#
# 因此它属于：
#
#     记忆化搜索
#
# 也可以看作：
#
#     自顶向下的动态规划
#
#
# 十二、素数判断
#
# isPrime(num) 使用试除法。
#
# 如果一个数不是素数，
# 一定存在一个不超过 sqrt(num) 的因数。
#
# 因此只需要检查：
#
#     2, 3, 4, ..., sqrt(num)
#
# 本程序进一步先处理：
#
#     num <= 1
#     num == 2
#     num 是偶数
#
# 然后只枚举奇数除数：
#
#     range(3, int(num ** 0.5) + 1, 2)
#
#
# 十三、一个简单的递归过程
#
# 假设：
#
#     data = [3, 7, 12, 19]
#     k = 3
#
# 初始状态：
#
#     dfs(3, 0, 3)
#
# 当前考虑 data[3] = 19。
#
# 分成两种情况：
#
#     不选 19：
#         dfs(2, 0, 3)
#
#     选择 19：
#         dfs(2, 19, 2)
#
# 对每个状态继续进行“选 / 不选”，
# 直到 remain_count == 0。
#
# 最终会枚举：
#
#     3 + 7 + 12 = 22
#     3 + 7 + 19 = 29
#     3 + 12 + 19 = 34
#     7 + 12 + 19 = 38
#
# 只有 29 是素数，
# 所以答案为 1。
#
#
# 十四、为什么不会重复枚举组合
#
# 每次处理完 data[index] 后，
# 下一层只访问 index - 1。
#
# 因此每个数字只会被决定一次：
#
#     选它
#     或不选它
#
# 不会出现：
#
#     先选下标 1，再选下标 0
#     先选下标 0，再选下标 1
#
# 这种顺序重复的问题。
#
# 每条“选 / 不选”路径唯一对应一个下标集合，
# 所以不会重复计算同一种组合。
#
#
# 十五、搜索、递归和回溯的体现
#
# 递归：
#
#     dfs 函数调用自身。
#
# 搜索：
#
#     枚举当前数字选或不选的所有可能。
#
# 回溯：
#
#     选择一种情况递归深入；
#     返回后尝试另一种情况。
#
# 这里没有显式使用 append 和 pop，
# 因为当前选择结果直接通过参数传递：
#
#     current_sum + data[index]
#     remain_count - 1
#
# 每个递归调用都有自己独立的参数，
# 所以不需要手动撤销 current_sum。
#
#
# 十六、复杂度分析
#
# 如果不使用 cache，
# 最多需要枚举所有选择方案，
# 复杂度接近：
#
#     O(2^n)
#
# 如果只看最终选择 k 个的组合，
# 主要数量约为：
#
#     C(n, k)
#
# 使用 cache 后，
# 每个不同的 `(index, remain_count, current_sum)` 状态只计算一次。
#
# 因此复杂度取决于实际可达状态数量：
#
#     O(状态数量 * 素数判断复杂度)
#
# 素数判断最坏约为：
#
#     O(sqrt(current_sum))
#
# cache 会占用与状态数量相关的空间。
#
# 这也是本程序相比普通组合回溯更快，
# 但可能使用更多内存的原因。


# ==================== 记忆化搜索与动态规划 ====================
#
# 一、@cache 是什么
#
#     @cache
#     def dfs(...):
#
# 是 Python 提供的缓存工具。
#
# 它会根据函数的参数保存返回值：
#
#     (index, remain_count, current_sum)
#                 ↓
#                答案
#
# 如果以后再次调用完全相同的函数：
#
#     dfs(index, remain_count, current_sum)
#
# Python 会直接返回之前保存的答案，
# 不会重新执行函数内部的递归。
#
# 所以：
#
#     @cache 是实现缓存的一种工具，
#     不是记忆化搜索这个概念本身。
#
#
# 二、什么是记忆化搜索
#
# 记忆化搜索可以理解为：
#
#     DFS 递归 + 缓存已经计算过的状态
#
# 如果不使用 @cache，
# 这段程序就是普通的 DFS：
#
#     不断进行“选择当前数字 / 不选择当前数字”
#     可能重复计算相同的子问题。
#
# 加上 @cache 后：
#
#     第一次遇到一个状态时计算；
#     后面再次遇到这个状态时直接读取答案。
#
# 因此当前程序是：
#
#     记忆化搜索。
#
#
# 三、为什么它同时也是动态规划
#
# 动态规划通常需要以下几个要素：
#
#     1. 可以定义状态
#     2. 状态之间存在转移关系
#     3. 存在重复子问题
#
# 本题的状态是：
#
#     dfs(index, remain_count, current_sum)
#
# 表示：
#
#     只考虑下标 0 到 index 的数字，
#     还需要选择 remain_count 个数字，
#     当前和为 current_sum 时，
#     能得到的合法方案数。
#
# 状态转移是：
#
#     不选择 data[index]：
#
#         dfs(
#             index - 1,
#             remain_count,
#             current_sum
#         )
#
#     选择 data[index]：
#
#         dfs(
#             index - 1,
#             remain_count - 1,
#             current_sum + data[index]
#         )
#
# 因此这个递归函数本身就是状态转移过程。
#
# @cache 保存了每个状态的答案，
# 所以本程序也属于动态规划。
#
#
# 四、三种概念之间的关系
#
# 普通 DFS：
#
#     只递归搜索，不保存状态答案。
#
# 记忆化搜索：
#
#     DFS 递归 + 缓存状态答案。
#
# 动态规划：
#
#     通过定义状态和状态转移，
#     高效解决存在重复子问题的问题。
#
# 记忆化搜索是动态规划的一种实现方式。
#
# 可以表示成：
#
#     动态规划
#     ├── 自顶向下：记忆化搜索
#     └── 自底向上：循环填表
#
#
# 五、本程序为什么叫“自顶向下”
#
# 程序从最初的大问题开始：
#
#     dfs(n - 1, k, 0)
#
# 再递归拆成更小的问题：
#
#     dfs(n - 2, ...)
#     dfs(n - 3, ...)
#     ...
#
# 这是从目标状态向基础状态递归，
# 所以叫：
#
#     自顶向下的动态规划。
#
#
# 六、自底向上的动态规划
#
# 如果不用递归，
# 而是从最小状态开始，
# 用循环逐步计算更大的状态，
# 就是自底向上的动态规划。
#
# 例如很多 01 背包程序使用：
#
#     for i in range(n):
#         for capacity in range(...):
#             dp[capacity] = ...
#
# 它们不会从 dfs 开始，
# 而是直接按照状态顺序填表。
#
#
# 七、@cache 不是动态规划的必要条件
#
# 不使用 @cache，
# 也可以手动建立缓存字典：
#
#     memo = {}
#
#     state = (index, remain_count, current_sum)
#
#     if state in memo:
#         return memo[state]
#
#     ...
#
#     memo[state] = result
#
# 这和 @cache 的思想相同。
#
# 因此：
#
#     @cache 只是 Python 中更方便的写法；
#     记忆化搜索的本质是保存状态答案。
#
#
# 八、为什么缓存不会导致少算方案
#
# 假设两个不同的选择路径到达相同状态：
#
#     dfs(index, remain_count, current_sum)
#
# 从这个状态往后能够得到 5 种合法方案。
#
# 第一次到达时计算并缓存：
#
#     这个状态的答案是 5。
#
# 第二次到达时直接返回 5。
#
# 两个父状态仍然会分别把这个 5 加入自己的结果，
# 因此：
#
#     cache 减少的是重复计算，
#     不是把不同的组合合并成一个组合。
#
#
# 九、本题最终归类
#
# 从搜索角度看：
#
#     本题是 DFS 的“选择 / 不选择”搜索。
#
# 从优化角度看：
#
#     本题使用了记忆化搜索。
#
# 从动态规划角度看：
#
#     本题是自顶向下的动态规划。
#
# 所以三种说法都正确：
#
#     DFS
#     记忆化搜索
#     动态规划
