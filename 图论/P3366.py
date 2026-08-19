# 最小生成树
# Kruskal + 并查集
import sys

class UnionFind:
    def __init__(self,n):
        self.parent = list(range(n+1))
        self.size = [1]*(n+1)

    def find(self,x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self,x,y):
        root_x = self.find(x)
        root_y = self.find(y)

        if root_x == root_y:
            return False

        if self.size[root_x] < self.size[root_y]:
            root_x,root_y = root_y,root_x

        self.parent[root_y] = root_x
        self.size[root_x] += self.size[root_y]
        return True

def main():
    input = sys.stdin.buffer.readline
    n,m = map(int,input().split())

    edges = []

    for _ in range(m):
        x,y,z = map(int,input().split())
        edges.append((z,x,y))

    edges.sort()

    uf = UnionFind(n)
    total = 0
    selected = 0

    for weight,x,y in edges:
        if uf.union(x,y):
            total += weight
            selected += 1

            if selected == n-1:
                break
    if selected == n-1:
        sys.stdout.write(str(total))
    else:
        sys.stdout.write('orz')

if __name__ == '__main__':
    main()


# 思路说明：
#
# 一、什么是生成树
#
# 对于一个无向连通图，
# 如果选出一些边，使得：
#
#     1. 所有 n 个节点都被连接
#     2. 不存在环
#
# 选出的边集合就构成一棵生成树。
#
# 一棵含有 n 个节点的树，恰好有：
#
#     n - 1 条边
#
# 如果边数少于 n - 1，
# 一定无法连接所有节点；
# 如果边数达到 n - 1 且没有环，
# 就已经是一棵树。
#
#
# 二、什么是最小生成树
#
# 图中每条边都有一个权值，
# 可以理解为修路成本、距离或连接代价。
#
# 最小生成树，简称 MST，
# 就是在所有生成树中，
# 选出边权总和最小的一棵。
#
# 本题要求：
#
#     如果图连通，输出最小生成树的总边权
#     如果图不连通，输出 orz
#
#
# 三、Kruskal 算法
#
# Kruskal 是求最小生成树的贪心算法。
#
# 它的基本步骤是：
#
#     1. 把所有边按权值从小到大排序
#     2. 依次考虑每条边
#     3. 如果加入这条边不会形成环，就选它
#     4. 如果会形成环，就跳过
#     5. 选够 n - 1 条边后结束
#
# 代码：
#
#     edges.sort()
#
# 因为边保存成：
#
#     (weight, x, y)
#
# 所以默认会优先按照 weight 排序。
#
#
# 四、为什么可以贪心地先选小边
#
# 设当前考虑的是按权值排序后最小的、
# 能连接两个不同连通块的边。
#
# 如果不选这条边，
# 而换成一条更大的边来连接这两个连通块，
# 总权值不会更优。
#
# 所以每次选择当前最小的合法边，
# 可以保证最终得到一棵最小生成树。
#
# Kruskal 的关键不是“所有小边都选”，
# 而是：
#
#     小边优先，并且不能形成环
#
#
# 五、为什么需要并查集
#
# 处理一条边 x - y 时，
# 需要判断 x 和 y 是否已经连通。
#
# 如果已经连通：
#
#     加入 x - y 会形成环
#
# 如果还不连通：
#
#     加入 x - y 可以连接两个连通块
#
# 并查集正好支持：
#
#     find(x)：找到 x 所在集合的代表
#     union(x, y)：合并两个集合
#
# 代码：
#
#     if uf.union(x, y):
#         total += weight
#
# union() 返回 True，
# 说明 x 和 y 原本不在同一个集合，
# 这条边被选入最小生成树。
#
# 如果返回 False，
# 说明两点已经连通，
# 这条边会形成环，应该跳过。
#
#
# 六、union() 如何判断成环
#
# 代码先找到两个端点的根：
#
#     root_x = self.find(x)
#     root_y = self.find(y)
#
# 如果：
#
#     root_x == root_y
#
# 说明 x 和 y 在同一个连通块中。
# 此时再加入一条 x - y 的边，
# 就会形成环：
#
#     return False
#
# 如果根不同：
#
#     self.parent[root_y] = root_x
#
# 把两个连通块合并，
# 并返回 True。
#
#
# 七、并查集中的两个优化
#
# 1. 路径压缩
#
#     self.parent[x] = self.parent[self.parent[x]]
#
# 查找根节点时，
# 让 x 直接跳向祖父节点，
# 逐渐缩短查找路径。
#
# 它不会改变集合关系，
# 只会让以后查询更快。
#
# 2. 按大小合并
#
#     if self.size[root_x] < self.size[root_y]:
#         root_x, root_y = root_y, root_x
#
# 保证把较小的集合挂到较大的集合下面。
#
# 这样可以避免并查集的树退化得太深。
#
#
# 八、什么时候得到最小生成树
#
# 每次成功合并两个不同连通块，
# 就选中一条边：
#
#     selected += 1
#     total += weight
#
# 当：
#
#     selected == n - 1
#
# 时，已经选出了 n - 1 条边。
#
# 因为这些边每次都没有形成环，
# 并且连接过程持续合并连通块，
# 所以它们构成一棵生成树。
#
# 由于边是按权值从小到大选择的，
# 这棵生成树就是最小生成树。
#
#
# 九、如何判断图不连通
#
# 如果图连通，
# Kruskal 最终一定能选出 n - 1 条边。
#
# 如果所有边处理完后：
#
#     selected < n - 1
#
# 说明有些节点仍然属于不同的连通块，
# 原图不连通，无法生成一棵包含所有节点的生成树。
#
# 所以输出：
#
#     orz
#
#
# 十、Kruskal 和最小生成树的关系
#
# 最小生成树是一个问题，
# Kruskal 是解决这个问题的一种算法。
#
# 求最小生成树常见的两种算法是：
#
#     Kruskal：排序边 + 并查集
#     Prim：从节点出发，用优先队列扩展
#
# Kruskal 更适合边集明确、需要按边权排序的情况。
#
#
# 十一、复杂度分析
#
# 边排序：
#
#     O(m log m)
#
# 并查集合并和查询：
#
#     O(m alpha(n))
#
# 其中 alpha(n) 是增长极慢的反阿克曼函数，
# 实际上可以近似看成常数。
#
# 所以总时间复杂度是：
#
#     O(m log m)
#
# 空间复杂度：
#
#     edges 保存 m 条边，O(m)
#     并查集 parent 和 size，O(n)
#
# 总空间复杂度是：
#
#     O(n + m)
