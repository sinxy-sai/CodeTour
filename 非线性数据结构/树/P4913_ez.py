# 二叉树的深度
import sys

sys.setrecursionlimit(10**6)

class BinaryTree:
    def __init__(self,n):
        self.root = None
        self.left = [0]*(n+1)
        self.right = [0]*(n+1)


    def add_node(self,node,left,right):
        if self.root is None:
            self.root = node
        self.left[node] = left
        self.right[node] = right

    def get_depth(self,node):
        if node == 0:
            return 0

        left_depth = self.get_depth(self.left[node])
        right_depth = self.get_depth(self.right[node])
        return max(left_depth,right_depth)+1


def main():
    input = sys.stdin.buffer.readline
    n = int(input())

    Tree = BinaryTree(n)

    for i in range(1,n+1):
        left,right = map(int,input().split())
        Tree.add_node(i,left,right)

    ans = Tree.get_depth(1)
    sys.stdout.write(str(ans))

if __name__ == '__main__':
    main()


# 思路说明：
#
# 一、题目要做什么
#
# 给出一棵二叉树，
# 每个节点有左儿子和右儿子。
#
# 如果输入为 0，
# 表示对应儿子不存在。
#
# 要求输出这棵二叉树的最大深度。
#
# 深度的含义是：
#
#     从根节点到最深叶子节点，最多经过多少层
#
# 根节点算第 1 层。
# 空节点深度是 0。
# 叶子节点深度是 1。
#
#
# 二、递归求深度的核心公式
#
# 对于一个非空节点 node：
#
#     node 的深度 = 左子树深度和右子树深度的较大值 + 1
#
# 写成公式就是：
#
#     depth(node) = max(depth(left[node]), depth(right[node])) + 1
#
# 为什么要 +1？
#
# 因为除了左右子树的深度，
# 还要把当前 node 这一层算进去。
#
# 如果 node 是空节点 0：
#
#     depth(0) = 0
#
# 这就是递归终止条件。
#
#
# 三、get_depth(node) 怎么执行
#
# 代码：
#
#     def get_depth(self, node):
#         if node == 0:
#             return 0
#
#         left_depth = self.get_depth(self.left[node])
#         right_depth = self.get_depth(self.right[node])
#         return max(left_depth, right_depth) + 1
#
# 执行过程：
#
#     1. 如果 node 是 0，说明是空节点，返回 0
#     2. 递归求左子树深度
#     3. 递归求右子树深度
#     4. 取左右子树较大值，再加上当前节点这一层
#
# 例如叶子节点的左右儿子都是 0：
#
#     left_depth = 0
#     right_depth = 0
#     depth = max(0, 0) + 1 = 1
#
#
# 四、如何存树
#
# 节点编号是 1 到 n，
# 所以用两个数组保存左右儿子：
#
#     self.left[node]
#     self.right[node]
#
# 比如：
#
#     left[1] = 2
#     right[1] = 7
#
# 表示：
#
#     1 的左儿子是 2
#     1 的右儿子是 7
#
# 数组下标就是节点编号，
# 查询孩子节点很方便。
#
#
# 五、为什么设置递归深度
#
# Python 默认递归深度大约只有一千多层。
#
# 本题 n 最大是 10^6。
# 如果树退化成一条链，
# 递归深度可能接近 10^6。
#
# 所以程序开头写：
#
#     sys.setrecursionlimit(10**6)
#
# 意思是提高 Python 允许的最大递归层数，
# 否则可能出现：
#
#     RecursionError: maximum recursion depth exceeded
#
# 不过要注意：
# setrecursionlimit 只是放宽 Python 自己的递归限制，
# 递归层数太深时仍然可能因为系统调用栈不够而 RE。
#
# 因此这个文件是递归 ez 版，
# 写法清晰，适合理解；
# 若要更稳，推荐使用非递归栈版本。
#
#
# 六、复杂度分析
#
# 建树时，每个节点读入一次：
#
#     O(n)
#
# get_depth 中，每个真实节点也只会被访问一次：
#
#     O(n)
#
# 所以总时间复杂度是：
#
#     O(n)
#
# 空间复杂度：
#
#     left/right 数组保存树结构，O(n)
#     递归调用栈最坏 O(n)
#
# 所以整体空间复杂度是：
#
#     O(n)
