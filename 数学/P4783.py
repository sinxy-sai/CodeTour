# 矩阵求逆 费马小定理 高斯-约旦消元
import sys

MOD = 10**9 + 7

def matrix_inverse(matrix,n):
    # 构造增广矩阵 [A | I] -> [I | A^(-1)]
    for i in range(n):
        matrix[i].extend([1 if i == j else 0 for j in range(n)])

    for col in range(n):
        # 找到第col列非零元素的行
        pivot_row = -1

        for row in range(col,n):
            if matrix[row][col] != 0:
                pivot_row = row
                break

        # 找不到主元，说明矩阵不可逆
        if pivot_row == -1:
            return None

        # 交换主元行
        matrix[col],matrix[pivot_row] = matrix[pivot_row],matrix[col]

        # 求主元的模逆元
        pivot = matrix[col][col]
        inverse_pivot = pow(pivot,MOD-2,MOD)

        # 将主元化为1
        matrix[col][col:] = [value * inverse_pivot % MOD for value in matrix[col][col:]]

        pivot_row_data = matrix[col][col:]

        # 消去其他行当前列的元素
        for row in range(n):
            if row == col:
                continue

            factor = matrix[row][col]

            if factor == 0:
                continue

            matrix[row][col:] = [(x - factor*y)%MOD for x,y in zip(matrix[row][col:],pivot_row_data)]

    # 右半部分是逆矩阵
    return [matrix[i][n:] for i in range(n)]


def main():
    input = sys.stdin.buffer.readline
    n = int(input())

    matrix = []
    for _ in range(n):
        row = list(map(int,input().split()))
        matrix.append([value % MOD  for value in row])

    ans = matrix_inverse(matrix,n)
    if ans is None:
        sys.stdout.write('No Solution')
    else:
        out = []
        for row in ans:
            out.append(' '.join(map(str,row)))
        sys.stdout.write('\n'.join(out))

if __name__ == '__main__':
    main()


# ============================================================
# 矩阵求逆：数学理论、算法思路与实现细节
# ============================================================
#
# 一、什么是逆矩阵
#
# 对于 n 阶方阵 A，如果存在一个 n 阶方阵 B，使得：
#
#     A * B = B * A = I
#
# 那么 B 就叫做 A 的逆矩阵，记作：
#
#     B = A^(-1)
#
# 其中 I 是单位矩阵。
#
# 例如二阶单位矩阵是：
#
#     I = [1 0]
#         [0 1]
#
# 单位矩阵相当于普通乘法中的 1：
#
#     A * I = I * A = A
#
#
# 二、矩阵什么时候可逆
#
# 一个方阵 A 可逆，当且仅当：
#
#     det(A) != 0
#
# 在本题的模 MOD 意义下，应理解为：
#
#     det(A) 不等于 0 (mod MOD)
#
# 如果矩阵的行列式模 MOD 后等于 0，
# 那么矩阵不可逆，应输出：
#
#     No Solution
#
# 代码没有直接计算行列式，
# 而是通过高斯-约旦消元寻找每一列的主元。
#
# 如果某一列找不到非零主元，
# 就说明矩阵的秩小于 n，
# 矩阵不可逆。
#
#
# 三、增广矩阵的构造
#
# 求逆矩阵的经典方法是构造：
#
#     [ A | I ]
#
# 左边是原矩阵 A，
# 右边是同阶单位矩阵 I。
#
# 例如：
#
#     A = [1 2]
#         [3 4]
#
# 构造增广矩阵：
#
#     [1 2 | 1 0]
#     [3 4 | 0 1]
#
# 接下来对整行进行高斯-约旦消元，
# 目标是把左半部分 A 化为单位矩阵：
#
#     [ A | I ]  ->  [ I | A^(-1) ]
#
#
# 四、为什么右半部分会变成逆矩阵
#
# 每一次初等行变换，都等价于在左边乘以一个初等矩阵。
#
# 如果所有行变换合起来对应的矩阵是 E，
# 那么：
#
#     E * [A | I]
#     = [E * A | E * I]
#     = [E * A | E]
#
# 消元完成后，左半部分变成单位矩阵：
#
#     E * A = I
#
# 根据逆矩阵定义：
#
#     E = A^(-1)
#
# 因此右半部分就是：
#
#     E = A^(-1)
#
# 所以：
#
#     [A | I] -> [I | A^(-1)]
#
# 这就是增广矩阵求逆法的数学依据。
#
#
# 五、高斯-约旦消元
#
# 普通高斯消元通常只把主元下面的元素消成 0，
# 得到上三角矩阵，然后再回代。
#
# 高斯-约旦消元会把主元所在列的其他元素全部消成 0，
# 最终直接得到单位矩阵。
#
# 目标形式是：
#
#     [1 0 0 | b11 b12 b13]
#     [0 1 0 | b21 b22 b23]
#     [0 0 1 | b31 b32 b33]
#
# 右半部分：
#
#     [b11 b12 b13]
#     [b21 b22 b23]
#     [b31 b32 b33]
#
# 就是 A^(-1)。
#
#
# 六、主元的选择
#
# 处理第 col 列时，
# 程序会在第 col 行到第 n-1 行中寻找非零元素：
#
#     for row in range(col, n):
#         if matrix[row][col] != 0:
#             pivot_row = row
#             break
#
# 如果当前行主元为 0，
# 但下面存在非零元素，
# 就把对应的行交换上来。
#
# 例如：
#
#     [0 2 | 1 0]
#     [3 4 | 0 1]
#
# 第一列不能使用 0 作为主元，
# 所以交换两行：
#
#     [3 4 | 0 1]
#     [0 2 | 1 0]
#
# 如果整列都是 0，
# 就找不到主元，矩阵不可逆。
#
#
# 七、模意义下的除法
#
# 在普通实数运算中，
# 把主元 a 化为 1 可以整行除以 a。
#
# 但模运算中不能直接进行普通除法。
# 需要使用 a 的乘法逆元：
#
#     a * a^(-1) ≡ 1 (mod MOD)
#
# 模意义下：
#
#     除以 a
#     等价于乘以 a^(-1)
#
# 因此当前主元行为：
#
#     [a, x1, x2, ..., y1, y2, ...]
#
# 时，整行乘以 a^(-1)，主元就变成：
#
#     a * a^(-1) ≡ 1 (mod MOD)
#
#
# 八、费马小定理与模逆元
#
# 本题的模数：
#
#     MOD = 10^9 + 7
#
# 是质数。
#
# 对于不被 MOD 整除的 a，费马小定理给出：
#
#     a^(MOD-1) ≡ 1 (mod MOD)
#
# 把它写成：
#
#     a * a^(MOD-2) ≡ 1 (mod MOD)
#
# 因此：
#
#     a^(-1) ≡ a^(MOD-2) (mod MOD)
#
# 所以代码使用：
#
#     inverse_pivot = pow(pivot, MOD - 2, MOD)
#
# 计算主元的模逆元。
#
# 例如模 7 下，a = 3：
#
#     3^(7-2) = 3^5 = 243
#     243 mod 7 = 5
#
# 验证：
#
#     3 * 5 = 15 ≡ 1 (mod 7)
#
# 所以 5 是 3 在模 7 下的逆元。
#
#
# 九、将主元化为 1
#
# 代码：
#
#     pivot = matrix[col][col]
#     inverse_pivot = pow(pivot, MOD - 2, MOD)
#
#     matrix[col][col:] = [
#         value * inverse_pivot % MOD
#         for value in matrix[col][col:]
#     ]
#
# `matrix[col][col:]` 表示当前行从主元开始到行末的部分。
#
# 例如：
#
#     当前行：[0, 0, 3, 6, 1, 4]
#     col = 2
#
# 那么：
#
#     matrix[col][col:] = [3, 6, 1, 4]
#
# 前面的 0 已经在之前的列中处理完成，
# 所以只需要更新后面的部分。
#
# 不能只把主元位置改成 1，
# 因为整行除以主元时，
# 这一行的所有元素都必须同步变化。
#
#
# 十、消去其他行
#
# 主元行化为：
#
#     [ ..., 1, ..., | ...]
#
# 如果其他行当前列的元素为 factor，
# 就执行：
#
#     Rrow <- Rrow - factor * Rcol
#
# 当前列会变成：
#
#     factor - factor * 1 = 0
#
# 代码：
#
#     factor = matrix[row][col]
#
#     matrix[row][col:] = [
#         (x - factor * y) % MOD
#         for x, y in zip(
#             matrix[row][col:],
#             pivot_row_data
#         )
#     ]
#
# 其中：
#
#     x：目标行对应位置的元素；
#     y：主元行对应位置的元素。
#
# `zip` 将两行相同位置的元素配对，
# 逐个完成：
#
#     x - factor * y
#
#
# 十一、为什么要对每一步取模
#
# 模运算满足：
#
#     (a + b) mod P
#     = ((a mod P) + (b mod P)) mod P
#
#     (a * b) mod P
#     = ((a mod P) * (b mod P)) mod P
#
# 因此每次加法、乘法后及时取模，
# 不会影响最后的答案。
#
# 代码中的：
#
#     (x - factor * y) % MOD
#
# 可以控制元素大小，
# 同时保证所有运算都在模 MOD 意义下进行。
#
#
# 十二、算法流程
#
#     1. 读入矩阵 A；
#     2. 构造增广矩阵 [A | I]；
#     3. 依次处理第 0 到第 n-1 列；
#     4. 寻找当前列的非零主元；
#     5. 找不到主元则输出 No Solution；
#     6. 交换主元行；
#     7. 求主元的模逆元；
#     8. 将主元所在行化为主元为 1；
#     9. 消去其他行当前列的元素；
#    10. 得到 [I | A^(-1)]；
#    11. 输出右半部分。
#
#
# 十三、与 P3389 线性方程组的联系
#
# P3389 也是高斯-约旦消元，
# 但两道题的增广矩阵不同。
#
# 求解线性方程组：
#
#     [A | B] -> [I | X]
#
# 右侧得到未知数解 X。
#
# 求矩阵逆：
#
#     [A | I] -> [I | A^(-1)]
#
# 右侧得到矩阵 A 的逆。
#
# 本质上都是：
#
#     通过初等行变换把左侧矩阵化为单位矩阵。
#
#
# 十四、复杂度
#
# 一共有 n 列需要处理。
# 每列需要消去最多 n 行，
# 每行最多更新 2n 个元素。
#
# 因此高斯-约旦消元的主要时间复杂度为：
#
#     O(n^3)
#
# 每个主元求一次快速幂逆元，
# 额外复杂度为：
#
#     O(n log MOD)
#
# 总复杂度可写为：
#
#     O(n^3 + n log MOD)
#
# 由于 n <= 400，
# 主导部分是 O(n^3)。
#
# 增广矩阵保存了 O(n^2) 个元素，
# 所以空间复杂度为：
#
#     O(n^2)
