# 二叉树的深度
import sys

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

    def get_depth(self):
        ans = 0
        stack = [(self.root,1)]

        while stack:
            node,depth = stack.pop()
            ans = max(ans,depth)
            if self.left[node]:
                stack.append((self.left[node],depth+1))
            if self.right[node]:
                stack.append((self.right[node],depth+1))

        return ans

def main():
    input = sys.stdin.buffer.readline
    n = int(input())

    Tree = BinaryTree(n)

    for i in range(1,n+1):
        left,right = map(int,input().split())
        Tree.add_node(i,left,right)

    ans = Tree.get_depth()
    sys.stdout.write(str(ans))

if __name__ == '__main__':
    main()


# 思路说明：
#
# 一、题目要做什么
#
# 给出一棵二叉树。
# 每个节点 i 有两个儿子：
#
#     left[i]   左儿子
#     right[i]  右儿子
#
# 如果某个儿子编号是 0，
# 表示这个儿子不存在。
#
# 题目要求输出二叉树的最大深度。
# 二叉树的深度指：
#
#     从根节点到最深叶子节点，一共经过了多少层
#
# 根节点的深度是 1。
# 根的儿子深度是 2。
# 再往下一层深度是 3。
#
#
# 二、如何存树
#
# 因为节点编号是 1 到 n，
# 所以本程序用两个数组保存树：
#
#     self.left[node]
#     self.right[node]
#
# 例如输入第 1 行：
#
#     2 7
#
# 表示：
#
#     1 的左儿子是 2
#     1 的右儿子是 7
#
# 就存成：
#
#     left[1] = 2
#     right[1] = 7
#
# 节点编号连续时，用数组比字典更合适，
# 因为数组下标访问更快。
#
#
# 三、为什么用非递归栈
#
# 这题 n 最大可以到 10^6。
# 如果树退化成一条链：
#
#     1 -> 2 -> 3 -> 4 -> ...
#
# 递归 DFS 的深度可能达到 10^6，
# Python 容易因为递归深度或调用栈问题 RE。
#
# 所以这个版本不用递归，
# 而是自己维护一个 stack 来模拟 DFS。
#
#
# 四、栈里保存什么
#
# 栈里保存的是：
#
#     (节点编号, 当前节点深度)
#
# 代码：
#
#     stack = [(self.root, 1)]
#
# 表示从根节点开始，
# 根节点深度是 1。
#
# 每次弹出一个节点：
#
#     node, depth = stack.pop()
#
# 然后用当前深度更新答案：
#
#     ans = max(ans, depth)
#
# 如果它有左儿子，
# 左儿子的深度就是 depth + 1：
#
#     stack.append((self.left[node], depth + 1))
#
# 如果它有右儿子，
# 右儿子的深度也是 depth + 1：
#
#     stack.append((self.right[node], depth + 1))
#
# 这样遍历完整棵树后，
# ans 就是出现过的最大深度。
#
#
# 五、为什么不用判断叶子节点
#
# 叶子节点的左右儿子都是 0。
# 当弹出叶子节点时，
# 代码会先更新：
#
#     ans = max(ans, depth)
#
# 然后发现没有左儿子、没有右儿子，
# 不再向栈里加入新节点。
#
# 所以不需要单独写：
#
#     如果是叶子节点就更新答案
#
# 每个节点都更新一次 ans 即可。
#
#
# 六、root 怎么来
#
# 题目说明根节点编号是 1。
#
# 本程序在 add_node() 中：
#
#     if self.root is None:
#         self.root = node
#
# 因为输入按 1 到 n 的顺序给出，
# 第一次加入的 node 就是 1，
# 所以 self.root 会被设为 1。
#
# 也可以直接在 __init__ 里写：
#
#     self.root = 1
#
#
# 七、复杂度分析
#
# 建树时，每个节点读入一次：
#
#     O(n)
#
# 求深度时，每个节点最多入栈一次、出栈一次：
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
#     stack 最坏情况下可能保存 O(n) 个节点
#
# 所以整体空间复杂度是：
#
#     O(n)
#
#
# 八、和递归版的关系
#
# 递归版的思想是：
#
#     depth(node) = max(depth(left[node]), depth(right[node])) + 1
#
# 非递归版本质上也是 DFS，
# 只是把“函数递归调用栈”换成了自己手写的 stack。
#
# 对 n 很大的题目，
# 非递归版通常更稳。
