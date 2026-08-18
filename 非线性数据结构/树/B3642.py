# 二叉树的遍历
import sys

class BinaryTree:
    def __init__(self,n):
        self.left = [0] * (n + 1)
        self.right = [0] * (n + 1)
        self.root = None

    def add_node(self,node,left,right):
        if self.root is None:
            self.root = node
        self.left[node] = left
        self.right[node] = right

    def preorder(self):
        ans = []
        stack = [self.root]

        while stack:
            node = stack.pop()
            ans.append(str(node))
            if self.right[node]:
                stack.append(self.right[node])
            if self.left[node]:
                stack.append(self.left[node])

        return ans

    def inorder(self):
        ans = []
        stack = []
        node = self.root
        while stack or node:
            while node:
                stack.append(node)
                node = self.left[node]

            node = stack.pop()
            ans.append(str(node))
            node = self.right[node]

        return ans

    def postorder(self):
        ans = []
        stack = [self.root]

        while stack:
            node = stack.pop()
            ans.append(str(node))
            if self.left[node]:
                stack.append(self.left[node])
            if self.right[node]:
                stack.append(self.right[node])

        ans.reverse()
        return ans



def main():
    n = int(sys.stdin.readline())
    tree = BinaryTree(n)
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
# 节点编号是 1 到 n，根节点固定为 1。
#
# 第 i 行输入两个整数 left 和 right，
# 表示：
#
#     i 的左儿子是 left
#     i 的右儿子是 right
#
# 如果 left 或 right 是 0，
# 表示对应儿子不存在。
#
# 建好树后，要输出三种遍历：
#
#     前序遍历
#     中序遍历
#     后序遍历
#
# 这题 n 最大可以到 10^6，
# 递归 DFS 可能因为递归太深而 RE。
# 所以本程序使用“非递归栈”来模拟遍历。
#
#
# 二、如何存树
#
# 因为节点编号是 1 到 n 的整数，
# 所以可以直接用数组保存左右儿子：
#
#     self.left[node]
#     self.right[node]
#
# 例如：
#
#     left[1] = 2
#     right[1] = 7
#
# 表示：
#
#     1 的左儿子是 2
#     1 的右儿子是 7
#
# 这种写法比字典更适合本题，
# 因为节点编号连续，数组访问更快。
#
#
# 三、为什么用栈
#
# 递归 DFS 本质上就是系统帮我们维护了一个调用栈。
#
# 例如递归写：
#
#     dfs(left)
#     dfs(right)
#
# Python 会把当前函数状态压入调用栈，
# 等子树处理完再回来。
#
# 非递归写法就是：
#
#     我们自己用 list 当栈
#
# 来模拟这个过程。
#
# 这样不会受到 Python 默认递归深度限制的影响。
#
#
# 四、前序遍历：根 -> 左 -> 右
#
# 前序遍历的顺序是：
#
#     先访问当前节点
#     再访问左子树
#     最后访问右子树
#
# 使用栈时：
#
#     stack = [root]
#
# 每次弹出一个节点 node：
#
#     node = stack.pop()
#     ans.append(str(node))
#
# 因为栈是后进先出，
# 想让左儿子先被访问，
# 就要先把右儿子压栈，再把左儿子压栈：
#
#     if right[node]:
#         stack.append(right[node])
#     if left[node]:
#         stack.append(left[node])
#
# 这样左儿子在栈顶，
# 下一次会先弹出左儿子。
#
# 所以前序遍历代码对应：
#
#     根 -> 左 -> 右
#
#
# 五、中序遍历：左 -> 根 -> 右
#
# 中序遍历的顺序是：
#
#     先访问左子树
#     再访问当前节点
#     最后访问右子树
#
# 非递归中序遍历的核心是：
#
#     一路向左，把沿途节点全部压栈
#
# 代码：
#
#     while node:
#         stack.append(node)
#         node = left[node]
#
# 这表示：
#
#     当前节点先不能访问，
#     因为它的左子树还没处理。
#     所以先把它存起来，然后继续走左儿子。
#
# 当 node 变成 0，
# 说明左边走到底了。
#
# 此时弹出栈顶：
#
#     node = stack.pop()
#     ans.append(str(node))
#
# 这个节点的左子树已经处理完，
# 现在可以访问根节点。
#
# 访问完根节点后，
# 转向右子树：
#
#     node = right[node]
#
# 整个过程就是：
#
#     左 -> 根 -> 右
#
#
# 六、后序遍历：左 -> 右 -> 根
#
# 后序遍历直接非递归写会稍微麻烦。
# 本程序使用一个常见技巧：
#
#     先得到 根 -> 右 -> 左
#     再整体反转
#
# 为什么可行？
#
# 因为：
#
#     根 -> 右 -> 左
#
# 反过来就是：
#
#     左 -> 右 -> 根
#
# 正好是后序遍历。
#
# 所以代码先类似前序遍历，
# 但压栈顺序改成：
#
#     if left[node]:
#         stack.append(left[node])
#     if right[node]:
#         stack.append(right[node])
#
# 因为栈是后进先出，
# 右儿子会先被弹出，
# 所以访问顺序变成：
#
#     根 -> 右 -> 左
#
# 最后：
#
#     ans.reverse()
#
# 就得到：
#
#     左 -> 右 -> 根
#
#
# 七、为什么 ans 里存 str(node)
#
# 遍历得到的 node 是整数。
# 但是输出时需要使用：
#
#     ' '.join(ans)
#
# join 只能拼接字符串列表，
# 不能直接拼接整数列表。
#
# 所以遍历时直接：
#
#     ans.append(str(node))
#
# 最后输出会更方便。
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
#     每个节点入栈、出栈各一次，O(n)
#
# 中序遍历：
#
#     每个节点入栈、出栈各一次，O(n)
#
# 后序遍历：
#
#     每个节点入栈、出栈各一次，O(n)
#     最后 reverse 也是 O(n)
#
# 所以总时间复杂度是：
#
#     O(n)
#
# 空间复杂度：
#
#     left/right 数组保存树结构，O(n)
#     三个遍历结果 val1、val2、val3，总共 O(n)
#     栈最坏可能存 O(n) 个节点
#
# 所以整体空间复杂度是：
#
#     O(n)
#
#
# 九、递归版和非递归版的区别
#
# 递归版写法更接近遍历定义，
# 但当树很深时，Python 可能因为递归深度限制 RE。
#
# 非递归版代码稍微复杂一些，
# 但它自己用 stack 模拟 DFS，
# 不依赖 Python 的函数调用栈，
# 更适合 n 很大的题目。
