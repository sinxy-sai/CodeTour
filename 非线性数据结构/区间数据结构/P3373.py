# 线段树2
import sys

class SegmentTree:
    def __init__(self,values,mod):
        self.n = len(values)-1
        self.mod = mod
        self.tree = [0]*(self.n*4)
        self.lazy_add = [0]*(self.n*4)
        self.lazy_mul = [1]*(self.n*4)

        self.build(1,1,self.n,values)

    def build(self,node,left,right,values):
        if left == right:
            self.tree[node] = values[left] % self.mod
            return

        mid = (left+right)//2

        self.build(2*node,left,mid,values)
        self.build(2*node+1,mid+1,right,values)
        self.push_up(node)

    def push_up(self,node):
        self.tree[node] = (self.tree[2*node] + self.tree[2*node+1]) % self.mod

    def apply(self,node,left,right,mul,add):
        length = (right - left + 1)
        self.tree[node] = (self.tree[node]*mul + length*add) % self.mod
        self.lazy_mul[node] = (self.lazy_mul[node]*mul) % self.mod
        self.lazy_add[node] = (self.lazy_add[node]*mul + add) % self.mod

    def push_down(self,node,left,right):
        if self.lazy_mul[node] == 1 and self.lazy_add[node] == 0:
            return
        mid = (left+right)//2
        mul = self.lazy_mul[node]
        add = self.lazy_add[node]
        self.apply(2*node,left,mid,mul,add)
        self.apply(2*node+1,mid+1,right,mul,add)
        self.lazy_mul[node] = 1
        self.lazy_add[node] = 0
    

    def update(self,node,left,right,ql,qr,mul,add):
        # 完全覆盖
        if ql <= left and right <= qr:
            self.apply(node,left,right,mul,add)
            return
        
        # 部分覆盖
        self.push_down(node,left,right)
        mid = (left+right)//2

        if ql <= mid:
            self.update(2*node,left,mid,ql,qr,mul,add)
        if qr > mid:
            self.update(2*node+1,mid+1,right,ql,qr,mul,add)

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

        return res % self.mod

def main():
    data = list(map(int,sys.stdin.buffer.read().split()))
    it = iter(data)
    n = next(it)
    m = next(it)
    mod = next(it)

    values = [0]
    for _ in range(n):
        values.append(next(it))

    seg = SegmentTree(values,mod)
    out = []

    for _ in range(m):
        op = next(it)

        # 区间乘法
        if op == 1:
            left = next(it)
            right = next(it)
            k = next(it)
            seg.update(1,1,n,left,right,k%mod,0)

        # 区间加法
        elif op == 2:
            left = next(it)
            right = next(it)
            k = next(it)
            seg.update(1,1,n,left,right,1,k%mod)

        # 区间求和
        elif op == 3:
            left = next(it)
            right = next(it)
            out.append(str(seg.range_sum(1,1,n,left,right)))

    sys.stdout.write('\n'.join(out))

if __name__ == '__main__':
    main()


# 思路说明：
#
# 一、题目要维护什么
#
# 本题需要维护一个数列，并支持三种操作：
#
#     1. 区间乘法：区间 [l, r] 中每个数乘 k
#     2. 区间加法：区间 [l, r] 中每个数加 k
#     3. 区间求和：查询 [l, r] 的总和
#
# 这是“区间修改 + 区间查询”问题，
# 使用线段树和懒标记解决。
#
# 由于题目要求所有结果对 mod 取模，
# 每次更新和查询都要及时取模。
#
#
# 二、线段树节点保存什么
#
#     tree[node]
#
# 表示当前节点负责区间的元素和。
#
# 例如当前节点负责 [l, r]，
# 那么：
#
#     tree[node] = a[l] + ... + a[r]
#
# 线段树通过二分区间，
# 把一个大区间拆成左右两个子区间。
#
#
# 三、为什么需要两个懒标记
#
# 区间修改有两种：
#
#     乘法
#     加法
#
# 因此每个节点需要保存两个待下传的标记：
#
#     lazy_mul[node]
#     lazy_add[node]
#
# 它们共同表示一个变换：
#
#     x -> x * lazy_mul[node] + lazy_add[node]
#
# 初始时没有任何修改，
# 所以这个变换应该是：
#
#     x -> x * 1 + 0
#
# 因此初始化为：
#
#     lazy_mul = 1
#     lazy_add = 0
#
# 这里乘法标记必须是 1，
# 不能初始化成 0。
#
#
# 四、apply：把一次变换应用到当前区间
#
# 当前区间长度是：
#
#     length = right - left + 1
#
# 如果对区间中每个数执行：
#
#     x -> x * mul + add
#
# 那么区间和会变成：
#
#     old_sum * mul + length * add
#
# 所以代码：
#
#     self.tree[node] = (
#         self.tree[node] * mul
#         + length * add
#     ) % mod
#
# 例如区间有 4 个数，
# 每个数都加 3，
# 区间总和就增加：
#
#     4 * 3 = 12
#
#
# 五、区间乘法和加法如何表示
#
# 区间乘 k：
#
#     x -> x * k
#
# 所以调用：
#
#     update(..., mul=k, add=0)
#
# 区间加 k：
#
#     x -> x + k
#
# 可以写成：
#
#     x -> x * 1 + k
#
# 所以调用：
#
#     update(..., mul=1, add=k)
#
#
# 六、懒标记为什么要复合
#
# 假设节点原来已经有一个旧变换：
#
#     old: x -> x * old_mul + old_add
#
# 现在又来一个新变换：
#
#     new: x -> x * mul + add
#
# 新操作是在旧操作之后执行，
# 所以总变换是：
#
#     (x * old_mul + old_add) * mul + add
#
# 展开：
#
#     x * old_mul * mul
#     + old_add * mul
#     + add
#
# 因此合并后的懒标记是：
#
#     lazy_mul = old_mul * mul
#     lazy_add = old_add * mul + add
#
# 对应代码：
#
#     self.lazy_mul[node] = (
#         self.lazy_mul[node] * mul
#     ) % self.mod
#
#     self.lazy_add[node] = (
#         self.lazy_add[node] * mul + add
#     ) % self.mod
#
# 不能简单写成：
#
#     lazy_add += add
#
# 因为新的乘法会同时放大之前积累的加法。
#
# 例如先加 3，再乘 2：
#
#     (x + 3) * 2 = 2x + 6
#
# 所以最终的加法标记应该是 6，而不是 3。
#
#
# 七、push_down：下传懒标记
#
# 如果当前节点有未下传的：
#
#     lazy_mul[node]
#     lazy_add[node]
#
# 说明当前区间的总和已经更新，
# 但左右子区间还没有真正记录这些修改。
#
# 当后续操作需要访问子节点时，
# 就调用 push_down：
#
#     self.apply(left_child, ..., mul, add)
#     self.apply(right_child, ..., mul, add)
#
# 把同一个变换传给左右儿子。
#
# 下传完成后，当前节点恢复成无标记状态：
#
#     lazy_mul[node] = 1
#     lazy_add[node] = 0
#
# 这是因为：
#
#     x -> x * 1 + 0
#
# 表示没有待下传的操作。
#
#
# 八、build：建立初始线段树
#
# 如果当前区间只有一个位置：
#
#     left == right
#
# 直接保存原数组的值。
#
# 如果区间不止一个位置，
# 就递归建立左右子区间，
# 然后：
#
#     tree[node] =
#         tree[left_child] + tree[right_child]
#
# 最后对 mod 取模。
#
#
# 九、update：区间修改
#
# 如果当前节点区间完全被目标区间覆盖：
#
#     ql <= left and right <= qr
#
# 直接调用：
#
#     apply(node, left, right, mul, add)
#
# 不需要继续递归，
# 这就是懒标记的作用。
#
# 如果只是部分覆盖：
#
#     1. 先 push_down
#     2. 递归处理有交集的左子区间
#     3. 递归处理有交集的右子区间
#     4. 最后 push_up 更新当前区间和
#
#
# 十、range_sum：区间查询
#
# 如果当前节点区间完全位于查询区间内，
# 直接返回：
#
#     tree[node]
#
# 如果只是部分覆盖，
# 先 push_down，
# 确保子区间拿到父节点的所有修改。
#
# 然后递归查询左右子区间，
# 将结果相加并对 mod 取模。
#
#
# 十一、操作顺序为什么重要
#
# 乘法和加法不满足交换律。
#
# 先加 3 再乘 2：
#
#     (x + 3) * 2 = 2x + 6
#
# 先乘 2 再加 3：
#
#     x * 2 + 3 = 2x + 3
#
# 两者结果不同。
#
# 所以懒标记合并时，
# 必须按照“旧操作先执行，新操作后执行”的顺序进行函数复合。
#
#
# 十二、复杂度分析
#
# 建树：
#
#     O(n)
#
# 每次区间乘法：
#
#     O(log n)
#
# 每次区间加法：
#
#     O(log n)
#
# 每次区间求和：
#
#     O(log n)
#
# 总时间复杂度：
#
#     O(n + q log n)
#
# tree、lazy_mul、lazy_add 都是 O(n) 数组，
# 所以空间复杂度：
#
#     O(n)
#
#
# 十三、和 P3372 的区别
#
# P3372 只有区间加法，
# 每个节点只需要一个 lazy_add。
#
# P3373 同时有区间乘法和区间加法，
# 所以需要：
#
#     lazy_mul
#     lazy_add
#
# 并且两个标记不能独立处理，
# 必须按照仿射变换：
#
#     x -> x * mul + add
#
# 进行合并。
