# 强连通分量 Tarjan算法
import sys
sys.setrecursionlimit(10**6)
# 在有向图中，如果一个顶点集合中的任意两个顶点 u、v 都满足：
# u 可以到达 v
# v 也可以到达 u
# 那么这个顶点集合就是一个强连通分量。
class TarjanSCC():
    def __init__(self,n):
        self.n = n
        self.graph = [[] for _ in range(n+1)]
        # dfn[u] 表示顶点 u 是第几个被 DFS 访问的
        self.dfn = [0]*(n+1)
        # low[u] 表示从 u 的 DFS 子树出发，能够回到的最早顶点
        self.low = [0]*(n+1)
        self.in_stack = [False]*(n+1)
        self.stack = []
        self.timestamp = 0
        self.components = []

    def addEdge(self,u,v):
        self.graph[u].append(v)

    def dfs(self,u):
        self.timestamp += 1
        self.dfn[u] = self.timestamp
        self.low[u] = self.timestamp

        self.stack.append(u)
        self.in_stack[u] = True

        for v in self.graph[u]:
            if self.dfn[v] == 0:
                # 未访问过 v
                self.dfs(v)
                # 如果 v 的子树能够回到某个很早的顶点，
                # 那么 u 也可以先走到 v，
                # 再沿着 v 的路径走过去。
                self.low[u] = min(self.low[u],self.low[v])

            elif self.in_stack[v]:
                # 已访问过 v，且 v 在栈中,说明存在返祖边(回到v了)
                self.low[u] = min(self.low[u],self.dfn[v])

        # u 是一个强连通分量的根节点 
        # 从顶点 u 的子树出发，无法回到编号比 u 更小的栈中顶点。
        if self.low[u] == self.dfn[u]:
            component = []
            while True:
                v = self.stack.pop()
                self.in_stack[v] = False
                component.append(v)

                # 一直从栈顶弹出，直到把当前分量的根节点 u 也弹出
                if v == u:
                    break
            component.sort() # 按顶点编号升序
            self.components.append(component)

    def find_components(self):
        for vertex in range(1,self.n+1):
            if self.dfn[vertex] == 0:
                self.dfs(vertex)

        # 按每个强连通分量的最小编号排序
        self.components.sort(
            key=lambda component: component[0] #因为前面已经执行过：component.sort()所以每个分量的第一个元素就是它的最小编号。
        )
        return self.components

def main():
    data = map(int,sys.stdin.buffer.read().split())
    it = iter(data)
    n,m = next(it),next(it)

    tarjan = TarjanSCC(n)
   
    for _ in range(m):
        u,v = next(it),next(it)
        tarjan.addEdge(u,v)

    components = tarjan.find_components()

    out = [str(len(components))]
    for component in components:
        out.append(' '.join(map(str,component)))
    sys.stdout.buffer.write('\n'.join(out).encode())
        
if __name__ == '__main__':
    main()


# ============================================================
# 强连通分量 Tarjan 算法：理论、思路与细节
# ============================================================
#
# 一、什么是强连通分量
#
# 在有向图中，如果一个顶点集合中的任意两个顶点 u、v
# 都满足：
#
#     u 可以到达 v；
#     v 也可以到达 u；
#
# 那么这个顶点集合就是一个强连通分量，
# 英文简称 SCC（Strongly Connected Component）。
#
# 例如：
#
#     1 -> 2
#     2 -> 3
#     3 -> 1
#
# 顶点 1、2、3 之间可以互相到达，
# 所以 {1, 2, 3} 是一个强连通分量。
#
# 注意：
#
#     强连通要求有方向的路径可以互相到达；
#     不是只要把边看成无向边后连通就可以。
#
#
# 二、Tarjan 算法的整体思想
#
# Tarjan 算法使用一次 DFS，
# 同时维护：
#
#     1. DFS 访问顺序；
#     2. 每个顶点能够回到的最早顶点；
#     3. 一个保存当前 DFS 活跃顶点的栈。
#
# 当某个顶点满足：
#
#     low[u] == dfn[u]
#
# 就说明 u 是一个强连通分量的根，
# 此时从栈顶不断弹出顶点，
# 直到弹出 u，
# 弹出的所有顶点正好组成一个强连通分量。
#
#
# 三、`dfn[u]` 的含义
#
# 代码：
#
#     self.timestamp += 1
#     self.dfn[u] = self.timestamp
#
# `dfn[u]` 表示顶点 u 第几次被 DFS 访问。
#
# 例如 DFS 访问顺序为：
#
#     1 -> 2 -> 3 -> 4
#
# 那么：
#
#     dfn[1] = 1
#     dfn[2] = 2
#     dfn[3] = 3
#     dfn[4] = 4
#
# `dfn` 一旦赋值就不会改变。
#
# 如果：
#
#     dfn[u] == 0
#
# 就表示顶点 u 还没有被访问。
#
#
# 四、`low[u]` 的含义
#
# `low[u]` 表示：
#
#     从 u 的 DFS 子树出发，
#     通过 DFS 树边和返祖边，
#     能够到达的最早顶点的 dfn 值。
#
# “最早”指的是 dfn 最小，
# 不是路径长度最短。
#
# 顶点刚被访问时，
# 至少可以到达自己：
#
#     self.low[u] = self.dfn[u]
#
# 如果之后发现可以到达更早的顶点，
# 就更新：
#
#     self.low[u] = min(
#         self.low[u],
#         ...
#     )
#
#
# 五、DFS 栈的作用
#
# 访问顶点 u 时：
#
#     self.stack.append(u)
#     self.in_stack[u] = True
#
# 栈中保存的是：
#
#     已经访问过，
#     但还没有确定所属强连通分量的顶点。
#
# 例如当前 DFS 路径为：
#
#     1 -> 2 -> 3 -> 4
#
# 栈可能是：
#
#     [1, 2, 3, 4]
#
# 只有仍然在栈中的顶点，
# 才可能和当前顶点属于同一个尚未确定的强连通分量。
#
#
# 六、处理未访问的子节点
#
# 代码：
#
#     if self.dfn[v] == 0:
#         self.dfs(v)
#         self.low[u] = min(
#             self.low[u],
#             self.low[v]
#         )
#
# 如果 v 还没有访问，
# 那么边 u -> v 是 DFS 树边。
#
# 先递归处理 v 的整棵子树。
#
# 如果 v 的子树能够回到某个很早的顶点，
# 那么 u 可以先走到 v，
# 再沿着 v 的路径走过去。
#
# 因此 u 也能够到达那个很早的顶点，
# 所以要用 low[v] 更新 low[u]。
#
#
# 七、处理已经访问且仍在栈中的顶点
#
# 代码：
#
#     elif self.in_stack[v]:
#         self.low[u] = min(
#             self.low[u],
#             self.dfn[v]
#         )
#
# 如果 v 已经访问过且仍在栈中，
# 说明边 u -> v 指向当前 DFS 活跃区域。
#
# 如果 v 是 u 的祖先，
# 这就是一条返祖边，
# 表示 u 可以回到更早访问的 v。
#
# 于是：
#
#     low[u] = min(low[u], dfn[v])
#
# 如果 v 已经访问过，
# 但不在栈中，
# 说明 v 所属的强连通分量已经确定，
# 不能再用它更新当前 low 值。
#
#
# 八、为什么 `low[u] == dfn[u]` 表示找到一个分量
#
# 如果：
#
#     low[u] < dfn[u]
#
# 说明 u 的子树还能够回到 u 的某个祖先，
# 所以 u 还不是强连通分量的根。
#
# 如果：
#
#     low[u] == dfn[u]
#
# 说明从 u 的子树出发，
# 无法回到比 u 更早的栈中顶点。
#
# 因此 u 是一个强连通分量的根节点。
#
# 从栈顶到 u 的这部分顶点，
# 正好构成一个完整的强连通分量。
#
#
# 九、为什么从栈顶弹出顶点
#
# 代码：
#
#     component = []
#
#     while True:
#         v = self.stack.pop()
#         self.in_stack[v] = False
#         component.append(v)
#
#         if v == u:
#             break
#
# 假设当前栈为：
#
#     [1, 2, 3, 4, 5]
#
# 如果 u = 4，
# 从栈顶弹出：
#
#     5、4
#
# 得到：
#
#     component = [5, 4]
#
# 弹出 4 后停止，
# 因为 4 是当前强连通分量的根。
#
# 不能继续弹出 3、2、1，
# 因为它们属于其他分量或仍在等待判断。
#
#
# 十、`in_stack[v] = False` 的作用
#
# 顶点 v 从栈中弹出后：
#
#     self.in_stack[v] = False
#
# 表示 v 所属的强连通分量已经确定。
#
# 以后再次遇到 v 时，
# 就不能把 v 当成当前 DFS 活跃区域中的顶点，
# 也不能用 dfn[v] 更新其他顶点的 low 值。
#
#
# 十一、为什么要对每个分量内部排序
#
# Tarjan 弹出顶点的顺序由 DFS 过程决定，
# 不一定是节点编号从小到大的顺序。
#
# 例如弹出结果可能是：
#
#     [6, 1, 5, 2]
#
# 题目要求每个强连通分量按节点编号升序输出，
# 所以执行：
#
#     component.sort()
#
# 得到：
#
#     [1, 2, 5, 6]
#
#
# 十二、为什么还要给所有分量排序
#
# 题目要求的输出顺序是：
#
#     先输出包含 1 号点的分量；
#     然后寻找还没有输出的最小编号顶点；
#     输出它所属的分量；
#     重复这个过程。
#
# 由于每个 component 已经升序排列，
# 所以：
#
#     component[0]
#
# 就是这个分量的最小顶点编号。
#
# 代码：
#
#     self.components.sort(
#         key=lambda component: component[0]
#     )
#
# 就是按照每个分量的最小编号排序。
#
# 例如：
#
#     [[3, 4], [1, 2, 5, 6]]
#
# 排序后：
#
#     [[1, 2, 5, 6], [3, 4]]
#
# 正好符合题目要求。
#
#
# 十三、重边和自环的处理
#
# 本题允许重边和自环。
#
# 重边：
#
#     1 -> 2
#     1 -> 2
#
# 直接在邻接表中保存两次即可。
#
# 自环：
#
#     3 -> 3
#
# 也直接加入：
#
#     graph[3].append(3)
#
# Tarjan 的 DFS 逻辑可以自然处理它们，
# 不需要额外去重。
#
#
# 十四、为什么 `find_components` 要遍历所有顶点
#
# 代码：
#
#     for vertex in range(1, self.n + 1):
#         if self.dfn[vertex] == 0:
#             self.dfs(vertex)
#
# 图可能不是从 1 号顶点全部可达的。
#
# 如果只从 1 号顶点 DFS，
# 只能找到 1 号顶点可达部分的强连通分量。
#
# 从每个未访问顶点重新 DFS，
# 才能找到整张图的所有强连通分量。
#
#
# 十五、算法流程
#
#     1. 建立有向图的邻接表；
#     2. 初始化 dfn、low、栈和时间戳；
#     3. 从每个未访问顶点开始 Tarjan DFS；
#     4. 访问顶点时设置 dfn 和 low；
#     5. 根据 DFS 树边或返祖边更新 low；
#     6. 当 low[u] == dfn[u] 时弹出一个完整分量；
#     7. 对每个分量内部排序；
#     8. 按分量最小节点编号排序；
#     9. 输出所有分量。
#
#
# 十六、复杂度分析
#
# Tarjan 算法中：
#
#     每个顶点只被 DFS 访问一次；
#     每条边只被扫描一次。
#
# 因此 Tarjan 本身的时间复杂度为：
#
#     O(n + m)
#
# 每个顶点最多入栈一次、出栈一次，
# 栈空间为：
#
#     O(n)
#
# 邻接表保存 n 个顶点和 m 条边，
# 所以基础空间复杂度为：
#
#     O(n + m)
#
# 由于题目要求对每个强连通分量内部排序，
# 排序部分会额外产生：
#
#     O(sum(k_i log k_i))
#
# 的复杂度，其中 k_i 是第 i 个分量的大小。
