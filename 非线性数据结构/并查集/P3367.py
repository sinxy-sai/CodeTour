# 并查集
import sys

class UnionFind:
    def __init__(self,n):
        self.parent = list(range(n+1))
        self.size = [1]*(n+1)

    def find(self,x):
        while self.parent[x] != x:
            # 路径压缩
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def same(self,x,y):
        return self.find(x) == self.find(y)

    def union(self,x,y):
        root_x = self.find(x)
        root_y = self.find(y)

        if root_x == root_y:
            return

        # 合并时，将树小的合并到树大的上面
        if self.size[root_x] < self.size[root_y]:
            root_x,root_y = root_y,root_x

        self.parent[root_y] = root_x
        self.size[root_x] += self.size[root_y]



def main():
    n,m = map(int,sys.stdin.buffer.readline().split())

    uf = UnionFind(n)
    out = []

    for _ in range(m):
        z,x,y = map(int,sys.stdin.buffer.readline().split())

        if z == 1:
            uf.union(x,y)

        elif z == 2:
            if uf.same(x,y):
                out.append('Y')
            else:
                out.append('N')

    sys.stdout.write('\n'.join(out))


if __name__ == '__main__':
    main()


# 思路说明：
#
# 一、并查集是什么
#
# 并查集是一种数据结构。
# 它主要用来维护若干个“不相交集合”。
#
# 它最常用来解决两类问题：
#
#     1. 合并两个元素所在的集合
#     2. 查询两个元素是否在同一个集合
#
# 所以它叫“并查集”：
#
#     并：union，合并集合
#     查：find，查询某个元素所在集合的代表
#
# 例如一开始有 5 个元素：
#
#     {1} {2} {3} {4} {5}
#
# 执行 union(1, 2) 后：
#
#     {1, 2} {3} {4} {5}
#
# 执行 union(3, 4) 后：
#
#     {1, 2} {3, 4} {5}
#
# 如果查询 same(1, 2)，答案是 True。
# 如果查询 same(1, 4)，答案是 False。
#
#
# 二、并查集的树形表示
#
# 并查集通常用“树”来表示每个集合。
# 同一个集合里的元素连成一棵树。
# 每棵树有一个根节点，根节点就是这个集合的代表元素。
#
# parent[x] 表示 x 的父节点。
#
# 如果：
#
#     parent[x] == x
#
# 说明 x 是根节点，也是这个集合的代表。
#
# 初始化时，每个元素都是一个单独的集合：
#
#     self.parent = list(range(n + 1))
#
# 也就是：
#
#     parent[1] = 1
#     parent[2] = 2
#     parent[3] = 3
#     ...
#
# 每个点一开始都指向自己。
#
#
# 三、find(x)：查询集合代表
#
# find(x) 的作用是：
#
#     找到 x 所在集合的根节点
#
# 也就是沿着 parent 一直往上走，
# 直到遇到 parent[x] == x 的节点。
#
# 朴素写法可以理解为：
#
#     while parent[x] != x:
#         x = parent[x]
#     return x
#
# 本程序中使用了路径压缩：
#
#     self.parent[x] = self.parent[self.parent[x]]
#     x = self.parent[x]
#
# 这句的意思是：
#
#     让 x 直接指向自己的爷爷节点
#
# 例如原来是：
#
#     4 -> 3 -> 2 -> 1
#     1 -> 1
#
# 调用 find(4) 时，
# 会把路径上的节点变得更接近根。
# 之后再查这些节点，速度就会更快。
#
# 路径压缩不会改变集合关系，
# 它只是把树变矮。
#
#
# 四、same(x, y)：查询是否同集合
#
# 两个元素是否在同一个集合，
# 只需要看它们的根节点是否相同：
#
#     find(x) == find(y)
#
# 如果根相同，说明它们在同一棵树里，
# 也就是同一个集合。
#
# 如果根不同，说明它们属于不同集合。
#
#
# 五、union(x, y)：合并集合
#
# 合并 x 和 y 所在集合时，
# 不能直接写 parent[y] = x。
#
# 因为 x 和 y 不一定是各自集合的根。
# 正确做法是先找到它们各自的根：
#
#     root_x = find(x)
#     root_y = find(y)
#
# 如果：
#
#     root_x == root_y
#
# 说明它们本来就在同一个集合里，
# 不需要合并。
#
# 如果根不同，
# 就把其中一棵树挂到另一棵树下面。
#
# 本程序使用“按大小合并”：
#
#     self.size[root_x]
#     self.size[root_y]
#
# 分别表示两个集合的大小。
#
# 如果 root_x 这棵树更小：
#
#     if self.size[root_x] < self.size[root_y]:
#         root_x, root_y = root_y, root_x
#
# 就交换两个根，
# 保证 root_x 是较大的集合。
#
# 然后：
#
#     self.parent[root_y] = root_x
#
# 把小集合 root_y 挂到大集合 root_x 下面。
#
# 最后更新新集合大小：
#
#     self.size[root_x] += self.size[root_y]
#
#
# 六、为什么要路径压缩和按大小合并
#
# 如果不优化，并查集可能退化成一条很长的链：
#
#     5 -> 4 -> 3 -> 2 -> 1
#
# 这样 find(5) 就要走很多步。
#
# 路径压缩：
#
#     查找根的过程中，让节点更接近根
#
# 按大小合并：
#
#     合并时，把小树挂到大树下面
#
# 这两个优化一起用，
# 可以让树非常矮。
#
# 所以并查集虽然底层是树，
# 但实际运行时每次操作都非常接近 O(1)。
#
#
# 七、本题如何对应并查集操作
#
# 题目给出 z, x, y。
#
# 如果：
#
#     z == 1
#
# 表示把 x 和 y 所在集合合并：
#
#     uf.union(x, y)
#
# 如果：
#
#     z == 2
#
# 表示查询 x 和 y 是否在同一个集合：
#
#     uf.same(x, y)
#
# 如果在同一个集合，输出：
#
#     Y
#
# 否则输出：
#
#     N
#
#
# 八、复杂度分析
#
# 设元素个数是 n，操作次数是 m。
#
# 初始化 parent 和 size：
#
#     O(n)
#
# 每次 union 或 same 都会调用 find。
# 在路径压缩 + 按大小合并后，
# 单次操作的均摊复杂度是：
#
#     O(alpha(n))
#
# alpha(n) 是反阿克曼函数，增长极慢。
# 在竞赛数据范围内，几乎可以看成常数。
#
# 所以总时间复杂度可以写作：
#
#     O((n + m) * alpha(n))
#
# 实际理解时可以近似看成：
#
#     O(n + m)
#
# 空间复杂度：
#
#     parent 长度 n + 1
#     size   长度 n + 1
#     out    最坏保存 O(m) 个查询答案
#
# 所以整体空间复杂度是：
#
#     O(n + m)
#
# 如果不把输出保存到 out，而是一边处理一边输出，
# 并查集本身的空间复杂度就是：
#
#     O(n)
