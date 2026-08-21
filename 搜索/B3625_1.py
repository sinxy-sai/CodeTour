# DFS 版：理解递归搜索
# BFS 版：理解队列搜索
# 二维网格
# 上下左右移动
# 边界判断
# 访问标记
# DFS/BFS 判断可达性
import sys
from collections import deque

def main():
    input = sys.stdin.readline
    n, m = map(int, input().split())
    data = [input().strip() for _ in range(n)]
    visited = [[False]*m for _ in range(n)]

    directions = [(0,1),(0,-1),(1,0),(-1,0)]

    # 1. 初始化状态和起点入队
    visited[0][0] = True
    queue = deque([(0,0)])

    while queue:
        # 2. 出队
        x,y = queue.popleft()

        # 3. 处理当前状态
        if x == n - 1 and y == m - 1:
            sys.stdout.write('Yes')
            return

        # 4. 枚举下一步选择
        for dx,dy in directions:
            nx = x + dx
            ny = y + dy

            # 5. 做选择(处理冲突)
            if not (0<=nx<n and 0<=ny<m):
                continue
            if data[nx][ny] == '#':
                continue
            if visited[nx][ny]:
                continue

            # 6. 标记下一步状态
            visited[nx][ny] = True

            # 7. 入队
            queue.append((nx,ny))

    sys.stdout.write('No')

if __name__ == '__main__':
    main()


# ==================== BFS 理论、算法思路与细节 ====================
#
# 一、BFS 是什么
#
# BFS 是 Breadth-First Search 的缩写，
# 中文是“广度优先搜索”。
#
# BFS 的核心思想是：
#
#     先搜索距离起点较近的状态，
#     再搜索距离起点较远的状态。
#
# 如果把起点看成第 0 层，
# 那么：
#
#     第 0 层：起点本身
#     第 1 层：一步可以到达的位置
#     第 2 层：两步可以到达的位置
#     第 3 层：三步可以到达的位置
#
# BFS 会按照这个层次顺序进行搜索。
#
#
# 二、为什么 BFS 使用队列
#
# 队列具有“先进先出”的特点：
#
#     先进入队列的状态先被处理。
#
# 起点先入队，
# 起点的所有相邻位置随后入队，
# 再处理这些相邻位置的下一层位置。
#
# 因此队列天然保证了：
#
#     先处理距离起点近的位置，
#     后处理距离起点远的位置。
#
# 本程序使用：
#
#     queue = deque([(0, 0)])
#
# `deque` 的 `popleft()` 可以高效地删除队首元素。
#
# 不建议使用普通 list 的 `pop(0)`，
# 因为删除第一个元素后，
# 后面的所有元素都需要向前移动，
# 时间复杂度较高。
#
#
# 三、本题中一个状态是什么
#
# 本题是迷宫问题，
# 一个位置就是一个状态：
#
#     (x, y)
#
# 其中：
#
#     x 表示行号
#     y 表示列号
#
# 当前状态的下一步选择有四种：
#
#     向上    (-1, 0)
#     向下    (1, 0)
#     向左    (0, -1)
#     向右    (0, 1)
#
# 代码中的：
#
#     directions = [
#         (0, 1),
#         (0, -1),
#         (1, 0),
#         (-1, 0)
#     ]
#
# 就表示这四种移动方式。
#
#
# 四、BFS 的基本流程
#
# 本题 BFS 的流程是：
#
#     1. 起点入队
#     2. 标记起点已经访问
#     3. 取出队首位置
#     4. 判断是否到达终点
#     5. 枚举当前位置的四个方向
#     6. 筛选合法且未访问的位置
#     7. 标记新位置并入队
#     8. 队列为空时仍未到达终点，则无路可走
#
#
# 五、为什么起点要先标记再入队
#
# 代码：
#
#     visited[0][0] = True
#     queue = deque([(0, 0)])
#
# 表示：
#
#     起点已经被发现，
#     并且等待被处理。
#
# `visited` 表示某个位置是否已经进入过搜索范围。
#
# 如果不标记访问状态，
# 迷宫中的环可能导致重复加入：
#
#     A -> B -> A -> B -> ...
#
# 最终可能无限搜索。
#
#
# 六、为什么新位置要在入队时标记
#
# 代码：
#
#     visited[nx][ny] = True
#     queue.append((nx, ny))
#
# 必须在入队时标记，
# 而不是出队时标记。
#
# 假设两个位置都能走到 C：
#
#     A -> C
#     B -> C
#
# 如果 C 出队时才标记，
# 那么 A 处理时可能把 C 入队一次，
# B 处理时又把 C 入队一次。
#
# 如果 C 第一次入队时就标记，
# 第二次遇到 C 时就会直接跳过。
#
# 因此每个位置最多进入队列一次。
#
#
# 七、如何判断下一位置是否合法
#
# 当前状态是：
#
#     (x, y)
#
# 通过方向 `(dx, dy)` 得到：
#
#     nx = x + dx
#     ny = y + dy
#
# 这个位置必须满足三个条件：
#
#     1. 不越界
#     2. 不是墙
#     3. 没有访问过
#
# 对应代码：
#
#     if not (0 <= nx < n and 0 <= ny < m):
#         continue
#
#     if data[nx][ny] == '#':
#         continue
#
#     if visited[nx][ny]:
#         continue
#
# 只要有一个条件不满足，
# 就跳过这个方向。
#
#
# 八、为什么找到终点可以立即返回
#
# 代码：
#
#     if x == n - 1 and y == m - 1:
#         sys.stdout.write('Yes')
#         return
#
# 因为本题只要求判断：
#
#     是否存在一条路径。
#
# 一旦 BFS 取出终点，
# 就已经证明终点可达，
# 不需要继续搜索其他位置。
#
# 如果队列最后为空仍然没有取出终点，
# 说明所有可达位置都已经搜索完成，
# 终点不可达。
#
#
# 九、BFS 为什么可以求无权最短路
#
# 本题每走一步的代价都相同，都是 1。
#
# BFS 的搜索顺序是：
#
#     先访问距离 0 的位置
#     再访问距离 1 的位置
#     再访问距离 2 的位置
#     ...
#
# 所以某个位置第一次被 BFS 访问时，
# 使用的就是最少步数。
#
# 本题只要求 Yes/No，
# 没有保存距离数组。
#
# 如果要求最短步数，可以定义：
#
#     distance = [[-1] * m for _ in range(n)]
#
# 起点：
#
#     distance[0][0] = 0
#
# 新位置：
#
#     distance[nx][ny] = distance[x][y] + 1
#
#
# 十、BFS 与 DFS 的区别
#
# BFS：
#
#     使用队列
#     一层一层搜索
#     适合无权图最短路
#
# DFS：
#
#     使用递归栈或手写栈
#     一条路深入到底
#     适合遍历、枚举和回溯
#
# 本题只判断是否可达，
# BFS 和 DFS 都可以。
#
# 如果题目改成：
#
#     求最少走几步
#
# 通常应优先使用 BFS。
#
#
# 十一、BFS 的正确性思路
#
# BFS 会从起点出发，
# 把所有可以一步到达的位置加入队列。
#
# 处理完这些位置后，
# 再把所有可以两步到达的位置加入队列。
#
# 因此：
#
#     队列中的位置按照距离起点从小到大被处理。
#
# 如果终点能够到达，
# 它最终一定会被加入并处理。
#
# 如果队列为空仍没有找到终点，
# 说明所有从起点可达的位置都已经搜索过，
# 终点一定不可达。
#
#
# 十二、BFS 的通用模板：判断是否可达
#
#     def bfs(start):
#         queue = deque([start])
#         visited[start] = True
#
#         while queue:
#             state = queue.popleft()
#
#             if state 满足目标:
#                 return True
#
#             for next_state in 所有下一状态:
#                 if next_state 不合法:
#                     continue
#
#                 if next_state 已访问:
#                     continue
#
#                 visited[next_state] = True
#                 queue.append(next_state)
#
#         return False
#
#
# 十三、BFS 的通用模板：求最短距离
#
#     def bfs(start):
#         distance[start] = 0
#         queue = deque([start])
#
#         while queue:
#             state = queue.popleft()
#
#             for next_state in 所有下一状态:
#                 if next_state 不合法:
#                     continue
#
#                 if distance[next_state] != -1:
#                     continue
#
#                 distance[next_state] = \
#                     distance[state] + 1
#                 queue.append(next_state)
#
#         return distance
#
#
# 十四、BFS 与图的关系
#
# 迷宫其实也是一张图：
#
#     每个空地是一个顶点；
#     相邻空地之间有一条边。
#
# 例如当前空地可以向右走，
# 就表示图中存在一条边：
#
#     当前点 -> 右边的点
#
# 因此本题也可以理解为：
#
#     在一张无权图中，
#     判断起点能否到达终点。
#
#
# 十五、复杂度
#
# 迷宫一共有 n * m 个位置。
#
# 每个位置最多入队一次，
# 每次最多检查四个方向。
#
# 所以时间复杂度为：
#
#     O(n * m)
#
# visited 数组需要：
#
#     O(n * m)
#
# 队列最多保存 O(n * m) 个位置，
# 因此空间复杂度为：
#
#     O(n * m)
