# 网格 Flood Fill
# 连通块
# 从边界开始搜索
# 外部区域与内部区域
# DFS/BFS 染色
import sys
from collections import deque

def main():
    input = sys.stdin.readline
    n = int(input())

    grid = [list(map(int,input().strip().split())) for _ in range(n)]
    visited = [[False]*n for _ in range(n)]
    queue = deque()

    # 把边界上的 0 加入队列
    for i in range(n):
        for j in range(n):
            if i == 0 or i == n-1 or j == 0 or j == n-1:
                if grid[i][j] == 0 and not visited[i][j]:
                    visited[i][j] = True
                    queue.append((i,j))

    directions = [(0,1),(0,-1),(1,0),(-1,0)]

    # 从边界向外部区域扩散
    while queue:
        x,y = queue.popleft()
        for dx,dy in directions:
            nx = x + dx
            ny = y + dy
            if not (0<=nx<n and 0<=ny<n):
                continue
            if grid[nx][ny] != 0:
                continue
            if visited[nx][ny]:
                continue
            visited[nx][ny] = True
            queue.append((nx,ny))

    # # 没有被边界 BFS 访问到的 0 在闭合圈内部 要被染色
    for i in range(n):
        for j in range(n):
            if grid[i][j] == 0 and not visited[i][j]:
                grid[i][j] = 2

    for row in grid:
        sys.stdout.write(' '.join(map(str,row))+'\n')


if __name__ == '__main__':
    main()


# ==================== 理论、算法思路与细节 ====================
#
# 一、题目本质
#
# 这道题不是直接从闭合圈内部寻找 0，
# 因为题目没有直接告诉我们内部区域的起点。
#
# 题目给出的判断标准是：
#
#     如果一个 0 能够只经过其他 0 到达方阵边界，
#     那么它属于闭合圈外部；
#     否则它属于闭合圈内部。
#
# 因此可以反过来处理：
#
#     从边界上的 0 出发，
#     找到所有能够到达边界的 0。
#
# 最后没有被找到的 0，
# 就一定在闭合圈内部。
#
#
# 二、什么是 Flood Fill
#
# Flood Fill 叫做“洪水填充”或“泛洪填充”。
#
# 它的思想是：
#
#     从一个起点出发，
#     向上下左右扩散，
#     把所有满足条件的相邻位置找出来。
#
# 常见应用包括：
#
#     统计网格连通块
#     判断两个位置是否连通
#     迷宫搜索
#     图片区域填充
#     染色
#
# 本题使用 BFS 实现 Flood Fill。
#
#
# 三、为什么从边界上的 0 开始
#
# 题目规定：
#
#     能通过 0 走到方阵边界的区域属于外部；
#     无法到达边界的区域属于内部。
#
# 所以所有外部区域都能从某个边界 0 出发被搜索到。
#
# 算法步骤是：
#
#     1. 找出所有边界上的 0
#     2. 将它们加入 BFS 队列
#     3. 只经过其他 0 向四周扩散
#     4. 标记所有能够到达的 0
#     5. 遍历整个方阵
#     6. 将未被访问的 0 修改为 2
#
#
# 四、为什么边界上的所有 0 都要作为起点
#
# 方阵边界上可能有多个互相不连通的 0 区域。
#
# 如果只选择一个边界 0，
# 可能漏掉另一个外部区域。
#
# 因此代码遍历整个方阵：
#
#     for i in range(n):
#         for j in range(n):
#
# 只要发现一个边界 0，
# 就加入队列。
#
# 这相当于同时从所有外部入口开始搜索。
#
#
# 五、为什么只能经过 0
#
# 闭合圈由数字 1 构成，
# 数字 1 相当于障碍物。
#
# BFS 扩散时：
#
#     if grid[nx][ny] != 0:
#         continue
#
# 这表示：
#
#     只能进入值为 0 的位置；
#     不能穿过值为 1 的闭合圈。
#
# 因此 BFS 不会从外部穿过闭合圈进入内部。
#
#
# 六、visited 数组的含义
#
#     visited[i][j]
#
# 表示位置 `(i, j)` 是否已经被边界 BFS 搜索到。
#
# 如果：
#
#     visited[i][j] == True
#
# 说明这个 0 可以从边界到达，
# 它属于闭合圈外部。
#
# 如果最后：
#
#     grid[i][j] == 0
#     visited[i][j] == False
#
# 说明这个 0 没有办法从边界到达，
# 它属于闭合圈内部，需要改成 2。
#
#
# 七、为什么入队时立即标记
#
# 代码：
#
#     visited[i][j] = True
#     queue.append((i, j))
#
# 一个位置第一次加入队列时就标记，
# 可以保证它不会被重复加入。
#
# 如果等到出队时才标记，
# 多个相邻位置可能同时把它加入队列，
# 造成重复搜索。
#
#
# 八、四个方向的含义
#
#     directions = [
#         (0, 1),
#         (0, -1),
#         (1, 0),
#         (-1, 0)
#     ]
#
# 它们分别表示：
#
#     向右、向左、向下、向上
#
# 当前位置 `(x, y)` 的相邻位置是：
#
#     nx = x + dx
#     ny = y + dy
#
# 只有同时满足以下条件时，
# 才能继续扩散：
#
#     1. 没有越界
#     2. grid[nx][ny] == 0
#     3. 还没有访问过
#
#
# 九、为什么最后再把 0 改成 2
#
# 不能在 BFS 搜索过程中直接把外部 0 改成其他数字，
# 因为还需要保留原数组信息来判断能否继续扩散。
#
# 本程序使用 visited 数组单独记录搜索结果。
#
# BFS 完成后：
#
#     能从边界到达的 0：保留为 0
#     不能从边界到达的 0：修改为 2
#
# 对应代码：
#
#     if grid[i][j] == 0 and not visited[i][j]:
#         grid[i][j] = 2
#
#
# 十、正确性说明
#
# BFS 从所有边界 0 出发，
# 并且只沿着 0 移动。
#
# 因此被 visited 标记的 0，
# 一定存在一条只经过 0 的路径连接到边界，
# 它们属于外部区域。
#
# 反过来，所有没有被 visited 标记的 0，
# 都无法通过 0 到达边界。
#
# 根据题目定义，
# 它们正好是闭合圈内部的 0。
#
# 因此把这些位置改成 2 是正确的。
#
#
# 十一、为什么使用 BFS，而不是必须使用 BFS
#
# 本题使用 BFS，但 DFS 也可以完成相同任务。
#
# 因为本题只关心：
#
#     一个 0 是否与边界连通。
#
# 并不要求最短距离。
#
# 所以以下两种方式都可以：
#
#     从边界 0 开始 BFS
#     从边界 0 开始 DFS
#
# BFS 的优点是使用队列，
# 不会受到 Python 递归深度的影响。
#
#
# 十二、Flood Fill 通用模板
#
#     queue = deque([start])
#     visited[start] = True
#
#     while queue:
#         state = queue.popleft()
#
#         for next_state in 相邻位置:
#             if next_state 越界:
#                 continue
#             if next_state 不满足搜索条件:
#                 continue
#             if next_state 已访问:
#                 continue
#
#             visited[next_state] = True
#             queue.append(next_state)
#
# 本题的特殊之处是：
#
#     起点不是一个固定位置，
#     而是所有边界上的 0。
#
#
# 十三、复杂度分析
#
# 方阵共有 n * n 个位置。
#
# 每个位置最多入队一次，
# 每次最多检查四个方向。
#
# 时间复杂度：
#
#     O(n^2)
#
# visited 数组、队列和输入矩阵都需要 O(n^2) 空间，
# 因此空间复杂度：
#
#     O(n^2)
