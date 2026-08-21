# 经典回溯
# 逐行放置
# 做选择
# 递归
# 撤销选择
# 约束判断
# 剪枝
import sys

def main():
    n = int(sys.stdin.readline())

    # placement[row] 表示第row行放置的列
    placement = [0] * n

    # 三种冲突标记
    used_column = [False] *n
    # 左上-右下对角线 row - col + n - 1
    used_diag1 = [False] * (2*n-1)
    # 左下-右上对角线 row + col
    used_diag2 = [False] * (2*n-1) 

    solutions = []
    total_solutions = 0

    def dfs(row):
        nonlocal total_solutions

        # 1. 终止条件
        if row == n:
            total_solutions += 1
            if len(solutions) < 3:
                solutions.append(placement[:])
            return 

        # 2.枚举下一步选择
        for col in range(n):
            # 3.做选择（处理冲突）
            if used_column[col]: 
                continue
            if used_diag1[row - col + n - 1]:
                continue
            if used_diag2[row + col]:
                continue

            # 4.标记当前选择状态
            placement[row] = col + 1
            used_column[col] = True
            used_diag1[row - col + n - 1] = True
            used_diag2[row + col] = True

            # 5.递归
            dfs(row + 1)

            # 6.撤销选择
            used_column[col] = False
            used_diag1[row - col + n - 1] = False
            used_diag2[row + col] = False
            
    dfs(0)
    for solution in solutions:
        sys.stdout.write(" ".join(map(str, solution)) + "\n")

    sys.stdout.write(str(total_solutions))

if __name__ == '__main__':
    main()


# ==================== 八皇后理论、算法思路与细节 ====================
#
# 一、题目本质
#
# 在 n * n 的棋盘上放置 n 个皇后，
# 要求任意两个皇后不能处于：
#
#     同一行
#     同一列
#     同一条对角线
#
# 题目要求：
#
#     1. 找出所有合法方案
#     2. 输出字典序最小的前三个方案
#     3. 输出方案总数
#
#
# 二、为什么每一行只放一个皇后
#
# 题目要求每一行有且只有一个皇后。
#
# 因此可以按照行进行搜索：
#
#     第 0 层：给第 0 行放皇后
#     第 1 层：给第 1 行放皇后
#     第 2 层：给第 2 行放皇后
#     ...
#
# 每进入一层，就表示已经为一行放置了皇后。
#
# 这样天然保证了：
#
#     不会有两个皇后在同一行。
#
#
# 三、递归函数 dfs(row) 的含义
#
#     dfs(row)
#
# 表示：
#
#     前 row 行已经放置完成，
#     现在准备给第 row 行放置皇后。
#
# 当：
#
#     row == n
#
# 说明第 0 到第 n - 1 行都已经放置完成，
# 找到一个完整合法方案。
#
#
# 四、placement 数组
#
#     placement[row]
#
# 表示第 row 行的皇后放在哪一列。
#
# 程序输出时加 1：
#
#     placement[row] = col + 1
#
# 因为程序内部使用 0-based 下标，
# 而题目输出的列号从 1 开始。
#
# 例如：
#
#     placement = [1, 3, 5, 2, 4]
#
# 表示：
#
#     第 1 行放第 1 列
#     第 2 行放第 3 列
#     第 3 行放第 5 列
#     第 4 行放第 2 列
#     第 5 行放第 4 列
#
#
# 五、三种冲突标记
#
# 1. used_column[col]
#
# 表示第 col 列是否已经放置皇后。
#
# 如果为 True，
# 当前列不能再放皇后。
#
#
# 2. used_diag1[row - col + n - 1]
#
# 表示左上到右下方向的对角线，
# 也就是“\”方向的对角线。
#
# 同一条“\”方向对角线上的格子满足：
#
#     row - col 相同
#
# 由于 row - col 可能为负数，
# 所以加上 n - 1，保证数组下标非负。
#
#
# 3. used_diag2[row + col]
#
# 表示左下到右上方向的对角线，
# 也就是“/”方向的对角线。
#
# 同一条“/”方向对角线上的格子满足：
#
#     row + col 相同
#
#
# 六、为什么对角线数组长度是 2 * n - 1
#
# n * n 棋盘中，
# 每个方向的对角线数量都是：
#
#     2 * n - 1
#
# 因此：
#
#     used_diag1 = [False] * (2 * n - 1)
#     used_diag2 = [False] * (2 * n - 1)
#
# 对角线编号范围是：
#
#     0 到 2 * n - 2
#
#
# 七、DFS 的搜索过程
#
# 在第 row 行中，依次尝试每一列：
#
#     for col in range(n):
#
# 对每个位置检查：
#
#     当前列是否已经被占用
#     “\”方向对角线是否被占用
#     “/”方向对角线是否被占用
#
# 如果任意一种冲突存在，
# 就不能在当前位置放皇后。
#
# 如果没有冲突，就进行选择：
#
#     placement[row] = col + 1
#     used_column[col] = True
#     used_diag1[...] = True
#     used_diag2[...] = True
#
# 然后递归处理下一行：
#
#     dfs(row + 1)
#
#
# 八、回溯过程
#
# 递归返回后必须撤销刚才的选择：
#
#     used_column[col] = False
#     used_diag1[...] = False
#     used_diag2[...] = False
#
# 这表示：
#
#     当前列和两条对角线可以重新使用。
#
# 回溯的完整过程是：
#
#     选择一个位置
#     递归尝试后面的行
#     如果后面走不通，返回当前行
#     撤销当前位置
#     尝试当前行的下一列
#
# 这就是：
#
#     做选择 -> 递归 -> 撤销选择
#
#
# 九、为什么必须撤销标记
#
# 假设第 row 行曾经选择了第 col 列：
#
#     used_column[col] = True
#
# 如果递归返回后不恢复：
#
#     used_column[col] = False
#
# 那么其他搜索分支也会错误地认为第 col 列已经被占用。
#
# 这样会漏掉合法方案。
#
# 所以回溯中的每个标记都必须成对出现：
#
#     标记 True
#     递归
#     恢复 False
#
#
# 十、递归终止时如何统计答案
#
# 当：
#
#     row == n
#
# 说明已经成功放置 n 个皇后。
#
# 程序执行：
#
#     total_solutions += 1
#
# 统计方案总数。
#
# 同时：
#
#     if len(solutions) < 3:
#         solutions.append(placement[:])
#
# 保存前三个方案。
#
# 这里必须使用：
#
#     placement[:]
#
# 而不能直接保存：
#
#     solutions.append(placement)
#
# 因为 placement 是同一个可变列表，
# 后续回溯会继续修改它。
#
# 使用切片可以保存当前状态的副本。
#
#
# 十一、为什么输出方案是字典序
#
# 每一行都按照列号从小到大尝试：
#
#     for col in range(n):
#
# DFS 会优先完成列号较小的方案。
#
# 例如第一行：
#
#     先尝试第 1 列
#     再尝试第 2 列
#     再尝试第 3 列
#
# 所以得到的完整方案天然按照字典序排列。
#
# 因此只保存搜索过程中遇到的前三个完整方案，
# 就是题目要求的前三个字典序方案。
#
#
# 十二、一个合法位置的判断
#
# 当前准备在 `(row, col)` 放置皇后。
#
# 需要判断：
#
#     used_column[col]
#     used_diag1[row - col + n - 1]
#     used_diag2[row + col]
#
# 如果三者都为 False，
# 说明当前位置没有和之前的皇后冲突。
#
# 放置后：
#
#     used_column[col] = True
#     used_diag1[row - col + n - 1] = True
#     used_diag2[row + col] = True
#
#
# 十三、搜索树的含义
#
# 搜索树的每一层对应棋盘的一行。
#
# 每个分支表示这一行选择了某一列。
#
# 例如：
#
#     第 0 行选择第 2 列
#         第 1 行选择第 4 列
#             第 2 行选择第 1 列
#
# 如果某一层没有任何合法列，
# 说明当前方案无法继续，
# 直接回溯到上一层。
#
#
# 十四、剪枝体现在哪里
#
# 代码在递归之前检查：
#
#     列冲突
#     主对角线冲突
#     副对角线冲突
#
# 这就是剪枝。
#
# 如果不进行这些判断，
# 程序会枚举所有 n^n 种逐行放置方式，
# 大量方案在很早的时候就已经不合法，
# 但仍会被继续搜索。
#
# 有了冲突判断后，
# 不合法的分支会在当前行立即停止。
#
#
# 十五、递归、回溯和 DFS 的关系
#
# 递归：
#
#     dfs 函数调用自身。
#
# DFS：
#
#     优先深入处理下一行。
#
# 回溯：
#
#     当前选择导致后面无法完成时，
#     撤销选择并尝试其他列。
#
# 剪枝：
#
#     提前判断当前位置是否冲突，
#     不再搜索必定失败的分支。
#
# 本题同时体现了：
#
#     DFS + 回溯 + 剪枝
#
#
# 十六、复杂度分析
#
# 不进行剪枝时，
# 每一行有 n 种选择，
# 搜索规模接近：
#
#     O(n^n)
#
# 加入列和对角线剪枝后，
# 实际搜索规模会大幅减少。
#
# 八皇后问题通常用回溯解决，
# 其复杂度常近似表示为：
#
#     O(n!)
#
# 每个搜索状态检查列和对角线都是 O(1)，
# 所以单个状态的判断很快。
#
# 额外空间主要来自：
#
#     placement 数组
#     三个冲突标记数组
#     递归调用栈
#
# 空间复杂度为：
#
#     O(n)
