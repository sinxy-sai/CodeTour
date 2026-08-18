# 二叉树建树
import sys

class BinaryTree:
    def __init__(self):
        self.children = {}
        self.root = None

    def add_node(self,node,left,right):
        if self.root is None:
            self.root = node

        self.children[node] = (left,right)

    def preorder(self):
        ans = []
        def dfs(node):
            if node  == '*':
                return

            left,right = self.children[node]
            ans.append(node)
            dfs(left)
            dfs(right)

        dfs(self.root)
        return ans


def main():
    n = int(sys.stdin.readline())
    tree = BinaryTree()
    for _ in range(n):
        s = sys.stdin.readline().strip()
        tree.add_node(s[0],s[1],s[2])

    out = tree.preorder()
    sys.stdout.write(''.join(out))

if __name__ == '__main__':
    main()


# 思路说明：
#
# 一、二叉树是什么
#
# 二叉树是一种树形数据结构。
# 每个节点最多有两个儿子：
#
#     左儿子
#     右儿子
#
# 如果某个儿子不存在，就称为空节点。
#
# 本题中用字符 '*' 表示空节点。
#
# 例如：
#
#     abc
#
# 表示：
#
#     节点 a 的左儿子是 b
#     节点 a 的右儿子是 c
#
# 如果输入：
#
#     d**
#
# 表示：
#
#     节点 d 没有左儿子
#     节点 d 没有右儿子
#
#
# 二、树的根节点
#
# 树里最上面的节点叫根节点。
# 从根节点出发，可以访问整棵树。
#
# 题目保证：
#
#     第一行读入的节点一定是根节点
#
# 所以在 add_node() 里：
#
#     if self.root is None:
#         self.root = node
#
# 第一次加入的节点就是根节点。
#
#
# 三、如何存二叉树
#
# 本程序使用字典保存每个节点的左右儿子：
#
#     self.children[node] = (left, right)
#
# 例如输入：
#
#     abc
#     bdi
#
# 会存成：
#
#     children['a'] = ('b', 'c')
#     children['b'] = ('d', 'i')
#
# 这样想知道某个节点的左右儿子时，
# 直接：
#
#     left, right = self.children[node]
#
# 就可以得到。
#
# 因为节点是字母，不是连续数字编号，
# 所以用字典比用数组更方便。
#
#
# 四、为什么这里不能用 split()
#
# 每一行输入是三个连续字符，
# 例如：
#
#     abc
#
# 它不是：
#
#     a b c
#
# 所以应该写：
#
#     s = sys.stdin.readline().strip()
#
# 得到字符串：
#
#     "abc"
#
# 然后用下标取：
#
#     s[0]   当前节点
#     s[1]   左儿子
#     s[2]   右儿子
#
# 如果写成：
#
#     s = sys.stdin.readline().strip().split()
#
# 对于输入 abc，
# 得到的是：
#
#     ['abc']
#
# 这个列表只有一个元素。
# 再访问 s[1]、s[2] 就会越界报错。
#
# split() 适合处理用空格分隔的输入，
# 例如：
#
#     a b c
#
# 但本题不是这种格式。
#
#
# 五、前序遍历是什么
#
# 二叉树常见遍历方式有三种：
#
#     前序遍历：根 -> 左 -> 右
#     中序遍历：左 -> 根 -> 右
#     后序遍历：左 -> 右 -> 根
#
# 本题要求输出前序遍历，
# 所以访问顺序是：
#
#     1. 先访问当前节点
#     2. 再递归遍历左子树
#     3. 最后递归遍历右子树
#
# 对应代码：
#
#     ans.append(node)
#     dfs(left)
#     dfs(right)
#
#
# 六、preorder() 的执行过程
#
# preorder() 里定义了一个 dfs(node)。
#
# 如果 node 是 '*'：
#
#     if node == '*':
#         return
#
# 说明这里是空节点，
# 不需要加入答案，也不需要继续往下递归。
#
# 如果不是空节点：
#
#     left, right = self.children[node]
#     ans.append(node)
#     dfs(left)
#     dfs(right)
#
# 先把当前节点加入答案，
# 再处理左子树，
# 再处理右子树。
#
# 最后返回 ans。
#
# main() 中：
#
#     out = tree.preorder()
#     sys.stdout.write(''.join(out))
#
# 因为 preorder() 返回的是字符列表，
# 所以用 ''.join(out) 拼成字符串输出。
#
#
# 七、样例过程
#
# 输入：
#
#     abc
#     bdi
#     cj*
#     d**
#     i**
#     j**
#
# 表示：
#
#         a
#       /   \
#      b     c
#     / \   /
#    d   i j
#
# 前序遍历是：
#
#     a
#     b
#     d
#     i
#     c
#     j
#
# 所以输出：
#
#     abdicj
#
#
# 八、复杂度分析
#
# 设节点数是 n。
#
# 建树时，每个节点读入一次，
# 时间复杂度是：
#
#     O(n)
#
# 前序遍历时，每个节点也只访问一次，
# 时间复杂度是：
#
#     O(n)
#
# 所以总时间复杂度是：
#
#     O(n)
#
# children 字典保存每个节点的左右儿子，
# ans 保存遍历结果，
# 空间复杂度是：
#
#     O(n)
#
# 本题 n <= 26，
# 数据非常小，
# 使用递归 DFS 完全没有问题。
