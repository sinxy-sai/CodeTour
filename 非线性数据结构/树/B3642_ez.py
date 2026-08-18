# 二叉树的遍历
import sys

sys.setrecursionlimit(2_000_000)

class BinaryTree:
    def __init__(self):
        self.root = None
        self.children = {}

    def add_node(self,node,left,right):
        if self.root is None:
            self.root = node
        self.children[node] = (left,right)

    def preorder(self):
        ans = []
        def dfs(node):
            if node == 0:
                return

            left,right = self.children[node]
            ans.append(str(node))
            dfs(left)
            dfs(right)
        dfs(self.root)
        return ans

    def inorder(self):
        ans = []
        def dfs(node):
            if node == 0:
                return
            left,right = self.children[node]
            dfs(left)
            ans.append(str(node))
            dfs(right)
        dfs(self.root)
        return ans

    def postorder(self):
        ans = []
        def dfs(node):
            if node == 0:
                return
            left,right = self.children[node]
            dfs(left)
            dfs(right)
            ans.append(str(node))
        dfs(self.root)
        return ans



def main():
    n = int(sys.stdin.readline())
    tree = BinaryTree()
    for i in range(1,n + 1):
        left,right = map(int,sys.stdin.readline().split())
        tree.add_node(i,left,right)

    val1 = tree.preorder()
    val2 = tree.inorder()
    val3 = tree.postorder()
    out = ' '.join(val1) +'\n' + ' '.join(val2) +'\n' + ' '.join(val3)
    sys.stdout.write(out)


if __name__ == '__main__':
    main()


# 思路说明：
#
# 一、题目要做什么
#
# 给出一棵二叉树。
# 对于每个节点 i，输入它的左儿子 left 和右儿子 right。
#
# 如果某个儿子是 0，
# 表示这个方向没有子节点。
#
# 题目保证根节点编号是 1。
# 建好树之后，要输出三种遍历：
#
#     前序遍历
#     中序遍历
#     后序遍历
#
#
# 二、二叉树的三种遍历
#
# 二叉树每个节点最多有两个儿子：
#
#     左儿子
#     右儿子
#
# 三种遍历的区别在于“什么时候访问根节点”。
#
# 1. 前序遍历
#
#     根 -> 左 -> 右
#
# 对应代码：
#
#     ans.append(str(node))
#     dfs(left)
#     dfs(right)
#
# 先访问当前节点，
# 再遍历左子树，
# 最后遍历右子树。
#
#
# 2. 中序遍历
#
#     左 -> 根 -> 右
#
# 对应代码：
#
#     dfs(left)
#     ans.append(str(node))
#     dfs(right)
#
# 先遍历左子树，
# 再访问当前节点，
# 最后遍历右子树。
#
#
# 3. 后序遍历
#
#     左 -> 右 -> 根
#
# 对应代码：
#
#     dfs(left)
#     dfs(right)
#     ans.append(str(node))
#
# 先遍历左子树，
# 再遍历右子树，
# 最后访问当前节点。
#
#
# 三、如何存树
#
# 本程序使用字典存每个节点的左右儿子：
#
#     self.children[node] = (left, right)
#
# 例如输入：
#
#     2 7
#
# 表示当前节点的左儿子是 2，右儿子是 7。
#
# 如果当前节点编号是 1，
# 就存成：
#
#     children[1] = (2, 7)
#
# 遍历时想知道 node 的左右儿子，
# 直接：
#
#     left, right = self.children[node]
#
#
# 四、根节点怎么确定
#
# 本题根节点固定是 1。
#
# 本程序在 add_node() 里写：
#
#     if self.root is None:
#         self.root = node
#
# 因为输入按 1 到 n 的顺序给出，
# 第一次加入的 node 就是 1，
# 所以 root 会被设为 1。
#
# 这里也可以直接在 __init__ 里写：
#
#     self.root = 1
#
# 但现在这种写法也能正确工作。
#
#
# 五、递归终止条件
#
# 题目用 0 表示空节点。
# 所以每个 dfs 开头都有：
#
#     if node == 0:
#         return
#
# 表示走到空节点时停止，
# 不加入答案，也不继续递归。
#
#
# 六、为什么 ans 里存 str(node)
#
# 遍历时 node 是整数。
# 但是最后输出需要：
#
#     ' '.join(val1)
#
# join 只能拼接字符串列表，
# 不能直接拼接整数列表。
#
# 所以遍历时写：
#
#     ans.append(str(node))
#
# 这样最后可以直接 join 输出。
#
#
# 七、为什么需要 setrecursionlimit
#
# Python 默认递归深度大约只有一千多层。
#
# 本题 n 最大可以到 10^6。
# 二叉树在最坏情况下可能退化成一条链：
#
#     1 -> 2 -> 3 -> 4 -> ...
#
# 这样 DFS 递归深度可能达到 10^6。
#
# 如果不提高递归限制，
# 可能会报：
#
#     RecursionError: maximum recursion depth exceeded
#
# 所以程序开头写：
#
#     sys.setrecursionlimit(2_000_000)
#
# 意思是把 Python 允许的最大递归深度提高到 2,000,000。
#
# 这能避免因为默认递归限制太小而 RE。
#
# 但要注意：
# setrecursionlimit 只是放宽 Python 的递归层数限制，
# 不代表递归一定安全。
# 递归层数太深时，每一层函数调用都要占用调用栈内存。
# 如果系统栈撑不住，仍然可能 RE。
#
# 所以这个版本更适合作为 ez 理解版。
# 本题能 AC 说明当前评测环境可以承受这个递归深度，
# 但更稳的正式模板是非递归栈写法。
#
#
# 八、复杂度分析
#
# 建树：
#
#     每个节点读入一次，O(n)
#
# 前序遍历：
#
#     每个节点访问一次，O(n)
#
# 中序遍历：
#
#     每个节点访问一次，O(n)
#
# 后序遍历：
#
#     每个节点访问一次，O(n)
#
# 所以总时间复杂度是：
#
#     O(n)
#
# 空间复杂度：
#
#     children 保存 n 个节点的左右儿子，O(n)
#     三个遍历结果 val1、val2、val3，总共 O(n)
#     递归调用栈最坏 O(n)
#
# 所以整体空间复杂度是：
#
#     O(n)
#
#
# 九、递归版和非递归版的区别
#
# 递归版优点：
#
#     写法直观，和遍历定义完全一致。
#
# 递归版缺点：
#
#     树很深时依赖 setrecursionlimit，
#     可能因为调用栈太深导致 RE。
#
# 非递归版优点：
#
#     用手写栈模拟 DFS，
#     不依赖 Python 函数递归，
#     对大数据更稳。
#
# 非递归版缺点：
#
#     代码比递归版难理解一些。
