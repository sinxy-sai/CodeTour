# 最近公共祖先LCA
import sys
from collections import deque


def main():
    input = sys.stdin.buffer.readline
    n,m,root = map(int,input().split())

    # 建树
    graph = [[] for _ in range(n+1)]

    for _ in range(n-1):
        x,y = map(int,input().split())
        graph[x].append(y)
        graph[y].append(x)

    # 预处理数据结构默认值
    LOG = (n+1).bit_length()
    depth = [0]*(n+1)
    up = [[0]*LOG for _ in range(n+1)]

    # 用 BfS 预计算深度和跳表信息
    queue = deque([root])
    depth[root] = 1

    while queue:
        node = queue.popleft()
        for nxt in graph[node]:
            if nxt == up[node][0]:
                continue

            depth[nxt] = depth[node]+1
            up[nxt][0] = node

            for j in range(1,LOG):
                up[nxt][j] = up[up[nxt][j-1]][j-1]

            queue.append(nxt)

    def lca(a,b):
        # 标准:让a的深度大于等于b的深度
        if depth[a] < depth[b]:
            a,b = b,a

        # 先把a提到和b一样的深度
        diff = depth[a] - depth[b]

        for j in range(LOG):
            if diff >> j & 1:
                a = up[a][j]

        if a == b:
            return a

        # 从大步到小步一起往上跳
        for j in range(LOG-1,-1,-1):
            if up[a][j] != up[b][j]:
                a = up[a][j]
                b = up[b][j]

        return up[a][0]


    # 输出
    out = []
    for _ in range(m):
        a,b = map(int,input().split())
        out.append(str(lca(a,b)))

    sys.stdout.write("\n".join(out))

if __name__ == '__main__':
    main()


# 思路说明：
#
# 一、LCA 是什么
#
# LCA 是 Lowest Common Ancestor，
# 中文叫“最近公共祖先”。
#
# 在一棵有根树中，
# 一个节点的祖先包括它的父亲、父亲的父亲，一直到根节点。
#
# 两个节点 a 和 b 的公共祖先，
# 就是同时是 a 的祖先、也是 b 的祖先的节点。
#
# 最近公共祖先指的是：
#
#     离 a 和 b 最近的那个公共祖先
#
# 例如：
#
#         4
#       /   \
#      2     1
#           / \
#          3   5
#
# 节点 3 和 5 的公共祖先有：
#
#     1, 4
#
# 离它们最近的是 1，
# 所以：
#
#     LCA(3, 5) = 1
#
#
# 二、为什么先像建图一样建树
#
# 题目给的是无向边：
#
#     x y
#
# 只表示 x 和 y 之间有一条边，
# 没有直接告诉谁是父亲、谁是儿子。
#
# 所以一开始要按无向图建邻接表：
#
#     graph[x].append(y)
#     graph[y].append(x)
#
# 然后从题目给定的根 root 出发，
# BFS 遍历整棵树。
#
# 在 BFS 过程中确定：
#
#     每个节点的父亲
#     每个节点的深度
#
# 这一步叫“把无根树定根”。
#
#
# 三、depth 和 up 数组
#
# depth[x] 表示节点 x 的深度。
#
# 本程序中：
#
#     depth[root] = 1
#
# 根节点深度是 1。
#
# up[x][j] 表示：
#
#     节点 x 向上跳 2^j 步后到达的祖先
#
# 例如：
#
#     up[x][0]  表示 x 向上跳 1 步，也就是 x 的父亲
#     up[x][1]  表示 x 向上跳 2 步，也就是 x 的爷爷
#     up[x][2]  表示 x 向上跳 4 步
#     up[x][3]  表示 x 向上跳 8 步
#
# 这就是“倍增”的核心。
#
#
# 四、LOG 是什么
#
# 代码：
#
#     LOG = (n + 1).bit_length()
#
# bit_length() 表示一个整数的二进制长度。
#
# LCA 中需要预处理 1、2、4、8、16 ... 这些跳跃长度。
# 树最多有 n 个节点，
# 所以最大深度差不会超过 n。
#
# LOG 只要足够覆盖 n 就可以。
#
# 例如 n = 500000 时，
# LOG 大约是 19，
# 因为 2^19 已经超过 500000。
#
#
# 五、BFS 预处理做了什么
#
# 代码：
#
#     queue = deque([root])
#     depth[root] = 1
#
# 从根节点开始 BFS。
#
# 每次取出一个节点 node：
#
#     node = queue.popleft()
#
# 遍历它相邻的点：
#
#     for nxt in graph[node]:
#
# 因为 graph 是无向邻接表，
# graph[node] 里既可能有儿子，也可能有父亲。
#
# 所以要跳过父亲：
#
#     if nxt == up[node][0]:
#         continue
#
# 如果 nxt 不是 node 的父亲，
# 那么在这次从 root 出发的 BFS 中，
# nxt 就是 node 的儿子。
#
# 于是可以确定：
#
#     depth[nxt] = depth[node] + 1
#     up[nxt][0] = node
#
# 也就是：
#
#     nxt 的深度 = 父亲深度 + 1
#     nxt 的 1 级祖先 = node
#
#
# 六、倍增转移公式
#
# 代码：
#
#     up[nxt][j] = up[up[nxt][j - 1]][j - 1]
#
# 它的意思是：
#
#     nxt 向上跳 2^j 步
#     = 先向上跳 2^(j-1) 步
#     = 再向上跳 2^(j-1) 步
#
# 因为：
#
#     2^j = 2^(j-1) + 2^(j-1)
#
# 举例：
#
#     up[x][2]
#
# 表示 x 向上跳 4 步。
#
# 可以拆成：
#
#     先从 x 向上跳 2 步，到 up[x][1]
#     再从 up[x][1] 向上跳 2 步
#
# 所以：
#
#     up[x][2] = up[up[x][1]][1]
#
# 这就是倍增表能成立的原因。
#
#
# 七、lca(a, b) 查询第一步：拉到同一深度
#
# 两个点深度可能不同。
# 例如 a 比 b 更深。
#
# 先保证 a 是更深的那个：
#
#     if depth[a] < depth[b]:
#         a, b = b, a
#
# 然后计算深度差：
#
#     diff = depth[a] - depth[b]
#
# 接下来根据 diff 的二进制，
# 把 a 向上跳到和 b 同一深度。
#
# 代码：
#
#     for j in range(LOG):
#         if diff >> j & 1:
#             a = up[a][j]
#
# 例如 diff = 13。
# 13 的二进制是：
#
#     1101
#
# 也就是：
#
#     13 = 8 + 4 + 1
#
# 那么就让 a 分别向上跳：
#
#     8 步、4 步、1 步
#
# 这样总共正好跳 13 步。
#
#
# 八、如果拉平后 a == b
#
# 代码：
#
#     if a == b:
#         return a
#
# 如果把深的点往上提之后，
# 两个点变成同一个点，
# 说明这个点就是最近公共祖先。
#
# 例如查询一个节点和它的祖先时，
# 会出现这种情况。
#
# 题目也说不保证 a != b，
# 如果 a 和 b 本来相同，
# 这里也能直接返回。
#
#
# 九、lca(a, b) 查询第二步：一起往上跳
#
# 如果 a 和 b 已经同深度，
# 但它们还不是同一个点，
# 就让它们一起往上跳。
#
# 代码：
#
#     for j in range(LOG - 1, -1, -1):
#         if up[a][j] != up[b][j]:
#             a = up[a][j]
#             b = up[b][j]
#
# 为什么要从大到小跳？
#
# 因为我们想尽量快地靠近 LCA，
# 但又不能直接跳到 LCA 上面。
#
# 如果 up[a][j] != up[b][j]，
# 说明 a 和 b 向上跳 2^j 步后，
# 仍然在 LCA 的不同分支里。
# 这一步可以安全地跳。
#
# 如果 up[a][j] == up[b][j]，
# 说明跳这么大一步会到达同一个祖先，
# 可能已经跳到 LCA 或 LCA 上方了，
# 这时不能跳，要试更小的步长。
#
# 循环结束后，
# a 和 b 还不是同一个点，
# 但它们的父亲已经相同。
#
# 所以答案是：
#
#     up[a][0]
#
#
# 十、复杂度分析
#
# 建邻接表：
#
#     n - 1 条边，每条边存两次，O(n)
#
# BFS 定根：
#
#     每个节点和每条边访问常数次，O(n)
#
# 倍增预处理：
#
#     每个节点计算 LOG 个祖先，O(n log n)
#
# 每次 LCA 查询：
#
#     拉平深度最多检查 LOG 层
#     一起上跳最多检查 LOG 层
#     所以是 O(log n)
#
# m 次查询：
#
#     O(m log n)
#
# 总时间复杂度：
#
#     O((n + m) log n)
#
# 空间复杂度：
#
#     graph 保存邻接表，O(n)
#     depth 保存每个点深度，O(n)
#     up 保存每个点的倍增祖先，O(n log n)
#     out 保存查询答案，O(m)
#
# 所以整体空间复杂度是：
#
#     O(n log n + m)
#
#
# 十一、Python 提醒
#
# 这份程序是标准倍增 LCA 思路，
# 适合学习算法。
#
# 但是本题数据范围是：
#
#     N, M <= 5 * 10^5
#
# 洛谷时限较紧，
# Python 即使算法正确，也可能因为常数较大而 TLE。
#
# 如果 Python 优化后仍然卡在 2 秒附近，
# 不建议继续硬抠常数。
# 这道 LCA 模板题后续用 C++ 写一版会更稳。
