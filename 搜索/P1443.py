# BFS 能求无权图最短路
# BFS 最短路
# 队列
# 层数/距离数组
# 八个方向移动
import sys
from collections import deque

def main():
    input = sys.stdin.readline
    n,m,x,y = map(int,input().split())
    directions = [[2,1],[1,2],[2,-1],[1,-2],[-2,1],[-1,2],[-2,-1],[-1,-2]]

    res = [[-1]*(m+1) for _ in range(n+1)]
    res[x][y] = 0
    queue = deque([(x,y)])

    while queue:
        x,y = queue.popleft()
        for dx,dy in directions:
            nx = x + dx
            ny = y + dy
            if not (1<=nx<=n and 1<=ny<=m):
                continue
            if res[nx][ny] != -1:
                continue
            res[nx][ny] = res[x][y] + 1
            queue.append((nx,ny))

    out = []
    for i in range(1,n+1):
        out.append(' '.join(map(str,res[i][1:m+1])))
    sys.stdout.write('\n'.join(map(str,out)))

if __name__ == '__main__':
    main()


# ==================== 算法思路与细节 ====================
#
# 一、题目本质
#
# 棋盘上的每个位置都可以看成图中的一个节点。
#
# 如果马可以从位置 A 一步跳到位置 B，
# 就表示图中存在一条边：
#
#     A -> B
#
# 每次跳马的代价都是 1，
# 因此这是一张无权图。
#
# 题目要求求出起点到所有位置的最少步数，
# 所以使用 BFS。
#
#
# 二、为什么使用 BFS
#
# BFS 会按照距离起点的层数进行搜索：
#
#     第 0 层：起点
#     第 1 层：一步可以到达的位置
#     第 2 层：两步可以到达的位置
#     第 3 层：三步可以到达的位置
#
# 因为所有边的权值都相同，都是 1，
# 所以某个位置第一次被 BFS 访问时，
# 得到的就是从起点到它的最短步数。
#
#
# 三、马的八种移动
#
# 马在棋盘上可以进行以下八种跳跃：
#
#     ( 2,  1)
#     ( 1,  2)
#     ( 2, -1)
#     ( 1, -2)
#     (-2,  1)
#     (-1,  2)
#     (-2, -1)
#     (-1, -2)
#
# 如果当前位置是 (x, y)，
# 通过偏移量 (dx, dy) 后的新位置是：
#
#     nx = x + dx
#     ny = y + dy
#
#
# 四、res 数组的含义
#
#     res[i][j]
#
# 表示：
#
#     从起点到棋盘位置 (i, j) 的最少步数。
#
# 初始化为 -1：
#
#     res = [[-1] * (m + 1) for _ in range(n + 1)]
#
# `-1` 有两个含义：
#
#     1. 这个位置还没有被访问过；
#     2. 最终表示这个位置无法到达。
#
# 起点距离自己为 0：
#
#     res[x][y] = 0
#
#
# 五、为什么可以用 res 判断访问状态
#
# 代码：
#
#     if res[nx][ny] != -1:
#         continue
#
# 如果 res[nx][ny] 不等于 -1，
# 说明这个位置已经被访问过。
#
# 由于 BFS 第一次访问某个位置时，
# 得到的就是最短距离，
# 后面再次到达这个位置时不需要更新。
#
# 因此不需要额外建立 visited 数组，
# 直接使用 res 数组即可。
#
#
# 六、队列中的状态
#
# 队列保存待处理的棋盘位置：
#
#     queue = deque([(x, y)])
#
# 每次取出队首：
#
#     x, y = queue.popleft()
#
# 表示处理当前位置，
# 并枚举马从当前位置可以跳到的八个位置。
#
# 新位置确定距离后入队：
#
#     res[nx][ny] = res[x][y] + 1
#     queue.append((nx, ny))
#
# 这里的状态转移是：
#
#     新位置距离 = 当前距离 + 1
#
#
# 七、为什么新位置要在入队时标记
#
# 代码先执行：
#
#     res[nx][ny] = res[x][y] + 1
#
# 再执行：
#
#     queue.append((nx, ny))
#
# 这表示一个位置一旦入队，
# 就立即标记为已经访问。
#
# 如果等到出队时才标记，
# 可能有多个位置同时把它加入队列，
# 从而造成重复入队。
#
# 入队时标记可以保证：
#
#     每个棋盘位置最多入队一次。
#
#
# 八、为什么需要判断边界
#
# 棋盘的有效行号是：
#
#     1 <= nx <= n
#
# 有效列号是：
#
#     1 <= ny <= m
#
# 因此代码判断：
#
#     if not (1 <= nx <= n and 1 <= ny <= m):
#         continue
#
# 如果新位置越界，
# 就不能加入队列。
#
# 程序使用了 n + 1 行、m + 1 列的数组，
# 这样可以直接使用题目中的 1-based 坐标，
# 不需要把起点减一。
#
#
# 九、为什么最后仍为 -1 的位置不可达
#
# BFS 会从起点出发，
# 访问所有通过合法跳跃可以到达的位置。
#
# 如果某个位置最后仍然是 -1，
# 说明 BFS 从起点出发始终没有到达它。
#
# 因此它不可达，按照题目要求输出 -1。
#
#
# 十、算法正确性
#
# BFS 按照距离起点从小到大的顺序处理位置。
#
# 假设当前位置 (x, y) 的最短距离为 d，
# 那么马从它跳到的每个合法位置距离就是 d + 1。
#
# BFS 在访问这些位置时，
# 不可能存在更短的路径还没有被处理，
# 因为更短距离的节点一定会先出队。
#
# 所以：
#
#     res[nx][ny] = res[x][y] + 1
#
# 得到的就是新位置的最短距离。
#
#
# 十一、复杂度分析
#
# 棋盘一共有 n * m 个位置。
#
# 每个位置最多入队一次，
# 每次最多检查 8 种跳法。
#
# 因此时间复杂度为：
#
#     O(8 * n * m) = O(n * m)
#
# `res` 数组需要保存所有位置的距离，
# 队列最多也可能保存 O(n * m) 个位置，
# 所以空间复杂度为：
#
#     O(n * m)
#
#
# 十二、BFS 最短路通用模板
#
#     distance = [[-1] * width for _ in range(height)]
#     distance[start_x][start_y] = 0
#
#     queue = deque([(start_x, start_y)])
#
#     while queue:
#         x, y = queue.popleft()
#
#         for dx, dy in directions:
#             nx = x + dx
#             ny = y + dy
#
#             if 越界:
#                 continue
#
#             if 不能到达:
#                 continue
#
#             if distance[nx][ny] != -1:
#                 continue
#
#             distance[nx][ny] = distance[x][y] + 1
#             queue.append((nx, ny))
#
# 这道题只需要把 directions 换成马的八种移动方式。
