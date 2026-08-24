# 矩阵快速幂
import sys

MOD = 10**9 + 7
# 1e9 + 7      # 1000000007.0，浮点数
# 10**9 + 7    # 1000000007，整数

def multiply(A,B,n):
    C = [[0]*n for _ in range(n)]

    for i in range(n):
        row_a = A[i]
        row_c = C[i]

        for k in range(n):
            value = row_a[k]
            if value == 0:
                continue

            row_b = B[k]

            for j in range(n):
                row_c[j] += value * row_b[j] #A[i][k] * B[k][j]

        # 当前行统一取模
        for j in range(n):
            row_c[j] %= MOD

    return C

def matrix_power(A,exp,n):
    '''
        矩阵快速幂计算 A^exp
    '''
    res = [[0]*n for _ in range(n)]

    # 单位矩阵
    for i in range(n):
        res[i][i] = 1

    base = A
    while exp > 0:
        # exponent 当前最低位为 1 时，需要乘以 base
        if exp & 1:
            res = multiply(res,base,n)

        # exponent 当前最低位为 0 时，需要平方 base
        base = multiply(base,base,n)
        # exponent 右移一位
        exp >>= 1

    return res

def main():
    input = sys.stdin.buffer.readline
    n,k = map(int,input().split())

    matrix = []
    for _ in range(n):
        row = list(map(int,input().split()))
        matrix.append([value % MOD for value in row])

    ans = matrix_power(matrix,k,n)

    out = []
    for row in ans:
        out.append(' '.join(map(str,row)))
    sys.stdout.buffer.write('\n'.join(out).encode())

if __name__ == '__main__':
    main()


# ============================================================
# 矩阵快速幂：数学理论、算法思路与实现细节
# ============================================================
#
# 一、矩阵是什么
#
# 矩阵是按照行和列排列的一组数。
#
# 例如：
#
#     A = [1 2 3]
#         [4 5 6]
#
# 这是一个 2 行 3 列的矩阵，记作 2 * 3 矩阵。
#
# 本题给定的是 n * n 的方阵，
# 因为只有方阵才能和自身相乘：
#
#     A * A
#     A^2
#     A^3
#
#
# 二、矩阵乘法
#
# 设 A 是 m * n 矩阵，
# B 是 n * p 矩阵，
# 那么 A * B 可以相乘，
# 结果 C 是 m * p 矩阵。
#
# C[i][j] 的计算公式是：
#
#     C[i][j] = A[i][0] * B[0][j]
#             + A[i][1] * B[1][j]
#             + ...
#             + A[i][n-1] * B[n-1][j]
#
# 也就是：
#
#     C[i][j] = sum(A[i][k] * B[k][j])
#
# 代码中的三层循环：
#
#     for i in range(n):
#         for k in range(n):
#             for j in range(n):
#                 C[i][j] += A[i][k] * B[k][j]
#
# 正是在实现：
#
#     C[i][j] += A[i][k] * B[k][j]
#
# 其中：
#
#     i：结果矩阵的行；
#     j：结果矩阵的列；
#     k：A 的列和 B 的行之间的匹配位置。
#
#
# 三、矩阵乘法的结合律
#
# 矩阵乘法一般不满足交换律：
#
#     A * B 不一定等于 B * A
#
# 但是矩阵乘法满足结合律：
#
#     (A * B) * C = A * (B * C)
#
# 这保证了矩阵幂有明确意义：
#
#     A^4 = A * A * A * A
#
# 可以按照不同的结合顺序计算。
#
# 矩阵快速幂正是利用了这个结合律。
#
#
# 四、单位矩阵
#
# 对 n * n 矩阵，单位矩阵 I 的主对角线元素为 1，
# 其他位置为 0。
#
# 例如三阶单位矩阵：
#
#     I = [1 0 0]
#         [0 1 0]
#         [0 0 1]
#
# 单位矩阵相当于普通乘法中的数字 1：
#
#     A * I = I * A = A
#
# 因此定义：
#
#     A^0 = I
#
# 代码中：
#
#     res = [[0] * n for _ in range(n)]
#
#     for i in range(n):
#         res[i][i] = 1
#
# 就是在构造单位矩阵。
#
#
# 五、普通快速幂
#
# 普通的幂运算可以利用：
#
#     a^0 = 1
#
# 如果 exp 是偶数：
#
#     a^exp = (a^(exp/2))^2
#
# 如果 exp 是奇数：
#
#     a^exp = a^(exp//2) * a^(exp//2) * a
#
# 例如：
#
#     a^13 = a^8 * a^4 * a
#
# 因为：
#
#     13 = 8 + 4 + 1
#
# 通过不断把指数除以 2，
# 原本需要 O(exp) 次乘法的问题，
# 可以降低到 O(log exp) 次。
#
#
# 六、矩阵快速幂
#
# 矩阵快速幂和普通快速幂完全相同，
# 只需要把“数字乘法”替换成“矩阵乘法”。
#
# 初始时：
#
#     result = I
#     base = A
#
# 当指数 exp 的二进制最低位为 1 时，
# 把当前的 base 乘到 result 中：
#
#     result = result * base
#
# 然后把 base 平方：
#
#     base = base * base
#
# 再把指数除以 2：
#
#     exp = exp // 2
#
# 对应代码：
#
#     while exp > 0:
#         if exp & 1:
#             res = multiply(res, base, n)
#
#         base = multiply(base, base, n)
#         exp >>= 1
#
#
# 七、`exp & 1` 的含义
#
# 整数在二进制下，最低位为：
#
#     0 -> 偶数
#     1 -> 奇数
#
# `exp & 1` 是按位与运算，
# 它只保留 exp 的最低二进制位。
#
# 例如：
#
#     13 = 1101₂
#     13 & 1 = 1
#
# 所以 13 是奇数。
#
#     12 = 1100₂
#     12 & 1 = 0
#
# 所以 12 是偶数。
#
# 在 Python 中：
#
#     if exp & 1:
#
# 当 exp 为奇数时条件成立。
#
#
# 八、`exp >>= 1` 的含义
#
# 右移一位相当于整数除以 2：
#
#     exp >>= 1
#
# 等价于：
#
#     exp = exp >> 1
#     exp = exp // 2
#
# 例如：
#
#     13 = 1101₂
#     13 >> 1 = 0110₂ = 6
#
# 快速幂就是不断查看最低位，
# 然后把指数右移一位。
#
#
# 九、为什么每一轮都要平方 base
#
# base 表示当前需要考虑的幂：
#
#     第一轮：base = A
#     第二轮：base = A^2
#     第三轮：base = A^4
#     第四轮：base = A^8
#
# 所以每一轮都执行：
#
#     base = base * base
#
# 例如求 A^13：
#
#     13 的二进制是 1101
#
# 各轮对应关系：
#
#     1 -> A
#     0 -> A^2
#     1 -> A^4
#     1 -> A^8
#
# 因此：
#
#     A^13 = A^8 * A^4 * A
#
#
# 十、为什么要对每个元素取模
#
# 题目要求输出：
#
#     A^k mod 1000000007
#
# 模运算满足：
#
#     (x + y) mod p
#     = ((x mod p) + (y mod p)) mod p
#
#     (x * y) mod p
#     = ((x mod p) * (y mod p)) mod p
#
# 因此可以在矩阵乘法过程中及时取模，
# 不必等到所有乘法完成后再取模。
#
# 代码中先计算一整行的乘积和，
# 然后统一执行：
#
#     row_c[j] %= MOD
#
# 这样既保证答案正确，
# 又可以控制数字规模。
#
#
# 十一、为什么 `MOD = 10**9 + 7`
#
# 题目中的模数是：
#
#     10^9 + 7 = 1000000007
#
# 在 Python 中：
#
#     10**9 + 7
#
# 是整数。
#
# 但：
#
#     1e9 + 7
#
# 中的 `1e9` 是浮点数，
# 所以整个结果会变成：
#
#     1000000007.0
#
# 如果使用浮点模数，矩阵元素也可能变成浮点数，
# 输出就会出现：
#
#     1.0 2.0
#
# 而题目要求输出整数。
#
# 所以本题必须使用：
#
#     MOD = 10**9 + 7
#
# 或：
#
#     MOD = 1000000007
#
#
# 十二、`multiply` 函数的实现细节
#
# 代码：
#
#     C = [[0] * n for _ in range(n)]
#
# 先创建一个 n * n 的全零矩阵，
# 用来保存 A * B 的结果。
#
# 对固定的 i 和 k：
#
#     value = A[i][k]
#
# 如果 value 为 0：
#
#     if value == 0:
#         continue
#
# 那么 A[i][k] * B[k][j] 对所有 j 都是 0，
# 可以直接跳过，减少计算。
#
# `row_a`、`row_b`、`row_c` 是行引用：
#
#     row_a = A[i]
#     row_b = B[k]
#     row_c = C[i]
#
# 这样可以减少重复的二维下标访问，
# 对 Python 的运行速度更有利。
#
#
# 十三、k = 0 时为什么输出单位矩阵
#
# 题目允许：
#
#     k = 0
#
# 根据幂的定义：
#
#     A^0 = I
#
# 所以程序初始化：
#
#     res = I
#
# 如果 `exp == 0`，
# `while exp > 0` 一次都不会执行，
# 直接返回单位矩阵。
#
#
# 十四、算法流程
#
#     1. 读入 n 和 k；
#     2. 读入矩阵 A，并将元素对 MOD 取模；
#     3. 创建 n 阶单位矩阵 result；
#     4. 令 base = A；
#     5. 查看 k 的最低二进制位；
#     6. 如果最低位为 1，则 result *= base；
#     7. 令 base *= base；
#     8. k 右移一位；
#     9. 重复直到 k 变成 0；
#    10. 输出 result。
#
#
# 十五、复杂度
#
# 两个 n 阶矩阵相乘需要三层循环，
# 时间复杂度为：
#
#     O(n^3)
#
# 快速幂需要处理 k 的每个二进制位，
# 需要 O(log k) 轮。
#
# 因此总时间复杂度为：
#
#     O(n^3 log k)
#
# 程序同时保存若干个 n * n 矩阵，
# 空间复杂度为：
#
#     O(n^2)
