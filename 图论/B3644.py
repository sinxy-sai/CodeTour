# 拓扑排序
import sys
from collections import deque

def main():
    input = sys.stdin.buffer.readline
    n = int(input())

    graph = [[] for _ in range(n+1)]
    indegree = [0]*(n+1)
    
    for i in range(1,n+1):
        for x in map(int,input().split()):
            if x == 0:
                break
            graph[i].append(x)
            indegree[x] += 1

    queue = deque()
    for i in range(1,n+1):
        if indegree[i] == 0:
            queue.append(i)

    ans = []
    while queue:
        node = queue.popleft()
        ans.append(node)

        for nxt in graph[node]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)

    sys.stdout.buffer.write(' '.join(map(str,ans)).encode())


if __name__ == '__main__':
    main()


# 思路说明：
#
# 一、这题本质上是有向图
#
# 把每个人看成一个顶点。
# 如果 i 是 x 的前辈，就建立一条有向边：
#
#     i -> x
#
# 输入第 i 行中的每个编号 x，
# 都表示 x 是 i 的后辈。
#
# 例如：
#
#     2 4 5 1 0
#
# 表示建立三条边：
#
#     2 -> 4
#     2 -> 5
#     2 -> 1
#
# 题目要求前辈必须比后辈先输出，
# 也就是对于每条边 i -> x，
# i 必须排在 x 前面。
#
# 这正是有向图的拓扑排序问题。
#
#
# 二、为什么可以使用拓扑排序
#
# 家族的前辈关系不应该出现环。
#
# 如果出现：
#
#     A -> B
#     B -> C
#     C -> A
#
# 就表示 A 是 B 的前辈，B 是 C 的前辈，
# 但 C 又是 A 的前辈，关系发生矛盾。
#
# 所以本题的关系图可以看作一个有向无环图，
# 也就是 DAG。
#
# DAG 一定存在拓扑序。
# 拓扑序就是一个顶点序列，
# 使得每条有向边 u -> v 都满足：
#
#     u 出现在 v 之前
#
#
# 三、邻接表存图
#
# 程序使用：
#
#     graph = [[] for _ in range(n + 1)]
#
# graph[i] 保存从 i 出发的所有边的终点。
#
# 读到 i 的后代 x 时：
#
#     graph[i].append(x)
#
# 就是添加有向边 i -> x。
#
# 因为每个人的后代数量可能不同，
# 邻接表比邻接矩阵更适合。
#
# 邻接矩阵需要 O(n^2) 空间，
# 而邻接表只需要保存实际存在的边，
# 空间是 O(n + E)。
#
# 这里 E 表示家族关系边的数量。
#
#
# 四、入度是什么
#
# 一个顶点的入度，是指向它的边的数量。
#
# 在本题中：
#
#     indegree[x]
#
# 表示 x 有多少个已知前辈。
#
# 读到边 i -> x 时：
#
#     indegree[x] += 1
#
# 入度为 0 的人没有前辈，
# 可以最先输出。
#
#
# 五、Kahn 拓扑排序算法
#
# 本程序使用的是 Kahn 算法。
#
# 基本流程：
#
#     1. 把所有入度为 0 的点加入队列
#     2. 从队列取出一个点并输出
#     3. 删除这个点发出的所有边
#     4. 如果某个后继入度变成 0，就加入队列
#     5. 重复以上过程
#
# 对应代码：
#
#     queue = deque()
#     for i in range(1, n + 1):
#         if indegree[i] == 0:
#             queue.append(i)
#
# 先把所有没有前辈的人放进队列。
#
# 处理当前节点：
#
#     node = queue.popleft()
#     ans.append(node)
#
# 输出 node，表示它已经排在所有后辈之前。
#
# 删除 node 发出的边：
#
#     for nxt in graph[node]:
#         indegree[nxt] -= 1
#
# node 已经被处理，
# 所以它不再是 nxt 的“未处理前辈”。
#
# 如果 nxt 的入度变成 0：
#
#     if indegree[nxt] == 0:
#         queue.append(nxt)
#
# 说明 nxt 的所有前辈都已经输出，
# 它现在也可以加入拓扑序。
#
#
# 六、为什么入度变成 0 就能输出
#
# 一个点只有在所有前驱都被处理后，
# 才能保证它前面的要求全部满足。
#
# indegree[x] 记录的就是还没有处理的前驱数量。
#
# 当：
#
#     indegree[x] == 0
#
# 就说明 x 已经没有未处理的前辈，
# 因此可以安全地输出。
#
#
# 七、输入中的 0
#
# 每行最后的 0 表示：
#
#     当前人的后代信息输入结束
#
# 所以代码：
#
#     for x in map(int, input().split()):
#         if x == 0:
#             break
#
# 遇到 0 就停止处理这一行。
# 0 不是一个真正的顶点，也不会加入图。
#
#
# 八、为什么输出顺序可以不唯一
#
# 如果队列里同时有多个入度为 0 的点，
# 它们之间没有前后依赖关系。
#
# 例如：
#
#     1 和 2 都没有前辈
#
# 那么：
#
#     1 2 ...
#
# 和：
#
#     2 1 ...
#
# 都可能是合法答案。
#
# 题目允许输出任意一种拓扑序，
# 所以使用普通队列即可。
#
#
# 九、复杂度分析
#
# 建图时，每条边处理一次：
#
#     O(n + E)
#
# Kahn 算法中：
#
#     每个点入队、出队一次
#     每条边被处理一次
#
# 所以拓扑排序也是：
#
#     O(n + E)
#
# 总时间复杂度：
#
#     O(n + E)
#
# 空间复杂度：
#
#     graph 邻接表需要 O(n + E)
#     indegree 需要 O(n)
#     queue 和 ans 需要 O(n)
#
# 所以总空间复杂度是：
#
#     O(n + E)
#
#
# 十、图论归类
#
# 这道题可以归类为：
#
#     有向图
#     有向无环图 DAG
#     邻接表
#     入度
#     Kahn 拓扑排序
#
# 它表面上是整理家族关系，
# 本质上是在有向图中寻找满足先后约束的顶点序列。
