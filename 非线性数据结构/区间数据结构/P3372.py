# 线段树1
import sys

class SegmentTree:
    def __init__(self,values):
        self.n = len(values)-1
        self.tree = [0]*(self.n*4)
        self.lazy = [0]*(self.n*4)

        self.build(1,1,self.n,values)

    def build(self,node,left,right,values):
        if left == right:
            self.tree[node] = values[left]
            return

        mid = (left+right)//2

        self.build(2*node,left,mid,values)
        self.build(2*node+1,mid+1,right,values)
        self.push_up(node)

    def push_up(self,node):
        self.tree[node] = self.tree[2*node] + self.tree[2*node+1]

    def apply(self,node,left,right,value):
        self.tree[node] += (right - left + 1)*value
        self.lazy[node] += value

    def push_down(self,node,left,right):
        if self.lazy[node] == 0 or left == right:
            return
        mid = (left+right)//2
        value = self.lazy[node]
        self.apply(2*node,left,mid,value)
        self.apply(2*node+1,mid+1,right,value)
        self.lazy[node] = 0
    

    def update(self,node,left,right,ql,qr,value):
        # 完全覆盖
        if ql <= left and right <= qr:
            self.apply(node,left,right,value)
            return
        
        # 部分覆盖
        self.push_down(node,left,right)
        mid = (left+right)//2

        if ql <= mid:
            self.update(2*node,left,mid,ql,qr,value)
        if qr > mid:
            self.update(2*node+1,mid+1,right,ql,qr,value)

        self.push_up(node)

    def range_sum(self,node,left,right,ql,qr):
        if ql <= left and right <= qr:
            return self.tree[node]

        self.push_down(node,left,right)
        mid = (left+right)//2
        res = 0
        if ql <= mid:
            res += self.range_sum(2*node,left,mid,ql,qr)
        if qr > mid:
            res += self.range_sum(2*node+1,mid+1,right,ql,qr)

        return res

def main():
    data = list(map(int,sys.stdin.buffer.read().split()))
    it = iter(data)
    n = next(it)
    m = next(it)

    values = [0]
    for _ in range(n):
        values.append(next(it))

    seg = SegmentTree(values)
    out = []

    for _ in range(m):
        op = next(it)

        # 区间加法
        if op == 1:
            left = next(it)
            right = next(it)
            k = next(it)
            seg.update(1,1,n,left,right,k)

        # 区间求和
        elif op == 2:
            left = next(it)
            right = next(it)
            out.append(str(seg.range_sum(1,1,n,left,right)))

    sys.stdout.write('\n'.join(out))

if __name__ == '__main__':
    main()


# 思路说明：
#
# 一、线段树是什么
#
# 线段树是一种维护区间信息的数据结构。
# 它把一个大区间不断二分成左右两个小区间，
# 每个树节点负责一个连续区间。
#
# 例如数组下标为 [1, 5]：
#
#                 [1, 5]
#                /     \
#             [1, 3]   [4, 5]
#             /   \     /   \
#          [1,2] [3]  [4]  [5]
#
# 本题每个节点维护：
#
#     tree[node]
#
# 表示当前节点所负责区间的总和。
#
#
# 二、本题为什么使用线段树
#
# 本题需要支持：
#
#     1. 区间 [left, right] 每个数加 k
#     2. 查询区间 [left, right] 的总和
#
# 如果直接修改区间里的每个元素，
# 一次区间修改最坏需要 O(n)。
#
# 如果每次查询都重新遍历区间，
# 一次查询也可能是 O(n)。
#
# 线段树配合懒标记，
# 可以让两种操作都做到 O(log n)。
#
#
# 三、如何用数组表示线段树
#
# 本程序没有定义树节点对象，
# 而是用数组保存：
#
#     tree[node]
#     lazy[node]
#
# 根节点编号是 1。
#
# 对于节点 node：
#
#     左儿子：2 * node
#     右儿子：2 * node + 1
#
# 为了保证空间足够，
# 通常开：
#
#     4 * n
#
# 个位置。
#
#
# 四、build：建树
#
# build(node, left, right, values)
# 表示建立当前节点 node，
# 它负责数组区间 [left, right]。
#
# 如果：
#
#     left == right
#
# 说明当前是叶子节点，
# 直接保存对应数组值：
#
#     tree[node] = values[left]
#
# 否则把区间分成两半：
#
#     [left, mid]
#     [mid + 1, right]
#
# 递归建立左右儿子，
# 最后用左右儿子的和计算当前节点：
#
#     tree[node] = tree[left_child] + tree[right_child]
#
#
# 五、push_up：向上维护
#
# 代码：
#
#     def push_up(self, node):
#         self.tree[node] = (
#             self.tree[2 * node]
#             + self.tree[2 * node + 1]
#         )
#
# 当前区间的和等于：
#
#     左区间的和 + 右区间的和
#
# 当某个子区间被修改后，
# 递归返回到父节点时，
# 就要调用 push_up 重新计算父节点。
#
#
# 六、lazy：懒标记
#
#     lazy[node]
#
# 表示：
#
#     当前区间整体加了多少，
#     但这个修改还没有下传给左右儿子
#
# 例如节点负责区间 [1, 5]，
# 现在整个区间都加 3。
#
# 不需要立刻递归修改所有叶子，
# 只需要：
#
#     tree[node] += 5 * 3
#     lazy[node] += 3
#
# 当前区间的总和已经正确，
# 修改暂时保存在 lazy 中。
#
# 这就是“懒”标记：
# 能暂时不往下递归，就先不递归。
#
#
# 七、apply：整体应用修改
#
# 代码：
#
#     def apply(self, node, left, right, value):
#         self.tree[node] += (
#             (right - left + 1) * value
#         )
#         self.lazy[node] += value
#
# 当前区间长度是：
#
#     right - left + 1
#
# 如果区间内每个数都加 value，
# 总和就增加：
#
#     区间长度 * value
#
# 同时给 lazy[node] 加 value，
# 表示这次整体修改还需要在以后传给子区间。
#
#
# 八、push_down：下传懒标记
#
# 如果当前节点有懒标记，
# 但接下来要访问它的子节点，
# 就必须把这个修改传下去。
#
# 代码：
#
#     self.apply(2 * node, left, mid, value)
#     self.apply(2 * node + 1, mid + 1, right, value)
#
# 左右子区间都整体加 value。
#
# 传完后清空当前节点的懒标记：
#
#     self.lazy[node] = 0
#
# 因为这个标记已经交给左右儿子了。
#
# 如果当前是叶子节点，
# 没有子节点可以下传，
# 所以直接返回。
#
#
# 九、update：区间修改
#
# update(node, left, right, ql, qr, value)
# 表示把目标区间 [ql, qr] 中的每个数加 value。
#
# 情况 1：完全覆盖
#
# 如果：
#
#     ql <= left and right <= qr
#
# 说明当前区间完全被目标区间覆盖。
#
# 直接：
#
#     self.apply(node, left, right, value)
#
# 不需要继续递归。
#
# 情况 2：部分覆盖
#
# 如果当前区间只和目标区间部分重叠：
#
#     1. 先 push_down
#     2. 递归处理有交集的左子区间
#     3. 递归处理有交集的右子区间
#     4. 最后 push_up
#
# 判断是否访问左子区间：
#
#     if ql <= mid:
#
# 判断是否访问右子区间：
#
#     if qr > mid:
#
#
# 十、range_sum：区间查询
#
# range_sum(node, left, right, ql, qr)
# 表示查询 [ql, qr] 的区间和。
#
# 情况 1：完全覆盖
#
# 如果当前区间完全位于查询区间内：
#
#     if ql <= left and right <= qr:
#         return self.tree[node]
#
# 直接返回当前节点保存的区间和。
#
# 情况 2：部分覆盖
#
# 如果只是部分重叠：
#
#     1. 先 push_down，保证子节点数据是最新的
#     2. 查询有交集的左子区间
#     3. 查询有交集的右子区间
#     4. 把结果相加
#
# 查询不需要 push_up，
# 因为查询不会改变节点数据。
#
#
# 十一、为什么需要递归返回后的 push_up
#
# 假设修改位置 3 所在的区间。
#
# 递归路径可能是：
#
#     [1, 5]
#        -> [1, 3]
#           -> [3, 3]
#
# 修改叶子 [3,3] 后，
# 递归返回到 [1,3]：
#
#     tree[1,3] = tree[1,2] + tree[3,3]
#
# 再返回到 [1,5]：
#
#     tree[1,5] = tree[1,3] + tree[4,5]
#
# 这就是线段树的“向上维护”过程。
#
#
# 十二、为什么区间操作是 O(log n)
#
# 线段树每次把区间对半分，
# 树的高度是 O(log n)。
#
# 一次区间修改或区间查询，
# 只会访问与目标区间相关的少量节点，
# 并且完全覆盖的节点可以直接处理。
#
# 配合 lazy 懒标记，
# 不需要访问区间内的每个叶子。
#
# 所以：
#
#     区间修改：O(log n)
#     区间查询：O(log n)
#
#
# 十三、复杂度分析
#
# 建树：
#
#     O(n)
#
# 每次区间加：
#
#     O(log n)
#
# 每次区间求和：
#
#     O(log n)
#
# 总时间复杂度：
#
#     O(n + m log n)
#
# 空间复杂度：
#
#     tree 和 lazy 都开 O(n)
#
# 所以空间复杂度是：
#
#     O(n)
#
#
# 十四、和树状数组的区别
#
# 树状数组更适合：
#
#     单点修改 + 区间查询
#     区间修改 + 单点查询
#
# 本题是：
#
#     区间修改 + 区间查询
#
# 虽然也可以用两个树状数组实现，
# 但线段树加懒标记是更直观、常见的模板。
