import sys
import math
# DFS 剪枝 枚举 
# 多参数搜索 + 约束搜索+ 可行性剪枝 + 最优性剪枝
def main():
    n,m =list(map(int,sys.stdin.buffer.read().split()))

    # min_vol[k]：
    # 剩余 k 层时，至少需要的体积
    #
    # 因为半径和高度都必须严格递减，且都是正整数
    # 最小情况是：
    #
    # Pi*R^2*H
    # 半径：k, k-1, ..., 1
    # 高度：k, k-1, ..., 1
    #
    # 最小体积为：
    # k^3 + (k-1)^3 + ... + 1^3
    min_vol = [0]*(m+1)
    for i in range(1,m+1):
        min_vol[i] = min_vol[i-1] + i**3

    min_side = [0]*(m+1)
    # min_side[k]：
    # 剩余 k 层时，至少需要的表面积
    #
    # 因为半径和高度都必须严格递减，且都是正整数
    # 最小情况是：
    #
    # 2*Pi*R*H
    # 半径：k, k-1, ..., 1
    # 高度：k, k-1, ..., 1
    #
    # 最小表面积为：
    # 2(k^2 + (k-1)^2 + ... + 1^2)
    for i in range(1,m+1):
        min_side[i] = min_side[i-1] + 2*i*i

    best = float('inf')

    def dfs(remaining_layers,used_volume,surface,max_radius,max_height):
        '''
        remaining_layers：还需要设计多少层；
        used_volume：已经使用的体积；
        surface：当前已经产生的表面积；
        max_radius：当前半径必须小于它；
        max_height：当前高度必须小于它。
        '''
        nonlocal best

        # 1.终止条件(剩余层数为0,且体积为n)
        if remaining_layers == 0:
            if used_volume == n:
                best = min(best,surface)
            return

        # 2.剪枝

        # 可行性剪枝

        # 当前使用的体积+剩余层数的最小体积大于n要剪枝
        if used_volume + min_vol[remaining_layers] > n:
            return

        # 最优性剪枝

        # 之前产生的表面积+剩余层数的最小表面积大于best要剪枝
        lower_bound = surface + min_side[remaining_layers]
        if remaining_layers == m:
            lower_bound += remaining_layers**2
        if lower_bound >= best:
            return

        # 3.计算当前状态
        remaining_vol = n - used_volume

        # 最优性剪枝

        # 之前产生的表面积+剩余体积（包含当前层）至少有的侧面积大于best要剪枝（S = 2*V/R）
        if surface + 2 * remaining_vol // max_radius >= best:
            return

        # 可用体积：剩余体积-当前层的最小体积
        available_vol = remaining_vol - min_vol[remaining_layers-1]

        # 注：每层的半径和高度最小都是剩余层数
        # 下一层最大半径：当前半径-1，可用体积//剩余层数的整数部分
        max_r = min(max_radius - 1,math.isqrt(available_vol//remaining_layers))

        # 4.枚举半径和高度
        # 从大到小枚举，因为半径和高度必须严格递减（约束搜索）
        for radius in range(max_r,remaining_layers-1,-1):
            radius_square = radius**2
            max_h = min(max_height - 1,available_vol//radius_square)

            if max_h < remaining_layers:
                continue

            for height in range(max_h,remaining_layers-1,-1):
                current_volume = radius_square*height
                added_surface = 2*radius*height

                if remaining_layers == m:
                    added_surface += radius_square

                # 最优性剪枝
                # 之前产生的表面积+加上这一层新增的面积+剩余体积（已经不含当前层的体积）至少有的侧面积大于best要剪枝（S = 2*V/R）
                rest_volume = remaining_vol - current_volume
                if surface + added_surface + 2 * rest_volume // max_radius >= best:
                    continue

                # 5.递归
                dfs(remaining_layers-1,used_volume+current_volume,surface+added_surface,radius,height)

    dfs(m,0,0,math.isqrt(n)+1,n+1)

    if best == float('inf'):
        sys.stdout.write('0')
    else:
        sys.stdout.write(str(best))

if __name__ == '__main__':
    main()


# ============================================================
# P1731 生日蛋糕：理论、算法思路与细节
# ============================================================
#
# 一、题目本质
#
# 需要设计 M 层圆柱形蛋糕，使得：
#
#     R1 > R2 > ... > RM
#     H1 > H2 > ... > HM
#
# 并且所有圆柱体的体积之和为 N。
#
# 题目要求使蛋糕外表面积最小。
# 由于题目中的实际体积和面积都带有 pi，
# 程序统一把 pi 约掉，只计算 N 和 S。
#
#
# 二、表面积公式
#
# 第 i 层圆柱的侧面积除以 pi 后为：
#
#     2 * Ri * Hi
#
# 蛋糕所有层的顶部暴露面积合起来，
# 会因为上下层相互覆盖而合并成最底层的面积：
#
#     R1^2
#
# 题目不计算最底层的下底面。
#
# 所以目标函数为：
#
#     S = R1^2 + 2 * R1 * H1
#                 + 2 * R2 * H2
#                 + ...
#                 + 2 * RM * HM
#
# 代码中的 surface 保存的就是当前已经产生的 S。
#
# 当正在选择最底层时：
#
#     if remaining_layers == m:
#         added_surface += radius_square
#
# 这里额外加上的 radius_square 就是最底层的 R1^2。
#
#
# 三、为什么使用 DFS
#
# 每一层都需要选择两个正整数：
#
#     半径 radius
#     高度 height
#
# 并且下一层必须满足：
#
#     下一层半径 < 当前层半径
#     下一层高度 < 当前层高度
#
# 因此可以用 DFS 一层一层地尝试所有合法的半径和高度。
#
# 但是直接枚举会产生大量方案，所以必须配合剪枝。
#
#
# 四、dfs 参数含义
#
#     dfs(
#         remaining_layers,
#         used_volume,
#         surface,
#         max_radius,
#         max_height
#     )
#
# 参数含义：
#
# remaining_layers：
#     还需要设计多少层。
#
# used_volume：
#     已经设计的层所占用的体积。
#
# surface：
#     已经设计的层产生的 S。
#
# max_radius：
#     当前层半径必须小于它。
#
# max_height：
#     当前层高度必须小于它。
#
# 例如：
#
#     dfs(2, 40, 50, 6, 8)
#
# 表示：
#
#     还需要设计 2 层；
#     已经使用体积 40；
#     当前面积为 50；
#     当前层半径小于 6；
#     当前层高度小于 8。
#
#
# 五、为什么从下往上搜索
#
# 当前程序从最底层开始设计。
#
# 假设当前层半径为 radius，
# 那么下一层只能选择：
#
#     radius - 1 或更小的半径。
#
# 因此递归时传入：
#
#     dfs(..., radius, height)
#
# 下一层就会受到：
#
#     当前半径 < radius
#     当前高度 < height
#
# 的限制。
#
# 对应代码：
#
#     max_radius - 1
#     max_height - 1
#
# 这正好保证：
#
#     R1 > R2 > ... > RM
#     H1 > H2 > ... > HM
#
#
# 六、最小体积数组 min_vol
#
# 如果还剩 k 层，那么为了满足半径和高度严格递减，
# 当前层的最小半径和高度至少是 k。
#
# 最小情况为：
#
#     半径：k, k - 1, ..., 1
#     高度：k, k - 1, ..., 1
#
# 所以最小体积为：
#
#     k^2 * k
#     + (k - 1)^2 * (k - 1)
#     + ...
#     + 1^2 * 1
#
# 也就是：
#
#     k^3 + (k - 1)^3 + ... + 1^3
#
# 代码预处理：
#
#     min_vol[i] = min_vol[i - 1] + i ** 3
#
#
# 七、可行性剪枝
#
# 代码：
#
#     if used_volume + min_vol[remaining_layers] > n:
#         return
#
# 含义是：
#
#     当前已经使用 used_volume；
#     剩余层即使采用最小尺寸，
#     总体积仍然超过目标体积 n。
#
# 例如：
#
#     n = 100
#     used_volume = 95
#     remaining_layers = 2
#     min_vol[2] = 1^3 + 2^3 = 9
#
# 那么：
#
#     95 + 9 > 100
#
# 即使后面的层全部取最小尺寸，也无法得到体积 100，
# 当前分支一定无解，可以直接返回。
#
# 这就是本题最核心的可行性剪枝。
#
#
# 八、为什么当前层的半径和高度至少为 remaining_layers
#
# 如果还剩 3 层，最小的严格递减序列只能是：
#
#     3, 2, 1
#
# 所以当前正在选择的最底层半径和高度都至少为 3。
#
# 因此循环下界是：
#
#     remaining_layers
#
# 代码：
#
#     for radius in range(
#         max_r,
#         remaining_layers - 1,
#         -1
#     )
#
# 和：
#
#     for height in range(
#         max_h,
#         remaining_layers - 1,
#         -1
#     )
#
#
# 九、min_side 与最小表面积剪枝
#
# 每层的侧面积除以 pi 后为：
#
#     2 * R * H
#
# 剩余 k 层时，理论上的最小侧面积为：
#
#     2 * (k^2 + (k - 1)^2 + ... + 1^2)
#
# 所以：
#
#     min_side[i] = min_side[i - 1] + 2 * i * i
#
# 代码：
#
#     lower_bound = surface + min_side[remaining_layers]
#
# 表示：
#
#     当前已经产生的面积
#     + 剩余层理论上的最小侧面积
#
# 如果这个下界已经不小于 best：
#
#     if lower_bound >= best:
#         return
#
# 那么后面不可能产生更优答案。
#
# 这是最优性剪枝，而不是可行性剪枝。
#
# 注意：
#
# min_side 只计算侧面积。
# 最底层的 R1^2 需要单独加上：
#
#     if remaining_layers == m:
#         lower_bound += remaining_layers ** 2
#
#
# 十、体积与侧面积的估价剪枝
#
# 这是本题能够通过大数据的关键剪枝。
#
# 对于一层圆柱：
#
#     V = R^2 * H
#     S = 2 * R * H
#
# 因此：
#
#     S = 2 * V / R
#
# 当前层以及上面的层半径都不超过 max_radius，
# 所以剩余体积至少需要约：
#
#     2 * remaining_vol / max_radius
#
# 的侧面积。
#
# 代码：
#
#     if surface + 2 * remaining_vol // max_radius >= best:
#         return
#
# 如果这个估计值已经不可能优于 best，
# 就不用继续搜索当前分支。
#
# 这里使用整数除法会让估计值略小一些，
# 但不会错误剪掉可能的最优解，只是剪枝力度稍弱。
#
#
# 十一、选择当前层后再次估价
#
# 当前层选择 radius 和 height 后：
#
#     current_volume = radius^2 * height
#
# 剩余体积为：
#
#     rest_volume = remaining_vol - current_volume
#
# 代码再次估计剩余层至少需要的侧面积：
#
#     surface
#     + added_surface
#     + 2 * rest_volume // max_radius
#
# 如果仍然不可能优于 best，就跳过当前高度：
#
#     if (
#         surface
#         + added_surface
#         + 2 * rest_volume // max_radius
#         >= best
#     ):
#         continue
#
# 这比只在递归函数开头判断更细，
# 因为它可以直接排除当前半径下的某些高度。
#
# 如果把估价中的 max_radius 改成当前 radius，
# 由于上面层的半径实际上还要小于当前 radius，
# 得到的下界会更大，剪枝会更强。
# 但当前程序使用 max_radius 仍然是安全的，只是估计较宽松。
#
#
# 十二、为什么从大到小枚举
#
# 代码从大到小枚举半径和高度：
#
#     for radius in range(max_r, remaining_layers - 1, -1):
#     for height in range(max_h, remaining_layers - 1, -1):
#
# 这样做可以较早构造出一个完整方案，
# 尽快得到一个较小的 best。
#
# best 越小，后续的最优性剪枝越有效。
#
# 这是一种常见的搜索策略：
#
#     先找到一个较好的可行解，
#     再用它作为上界剪掉更多分支。
#
#
# 十三、完整搜索流程
#
# 1. 预处理 min_vol 和 min_side。
#
# 2. 从最底层开始枚举半径和高度。
#
# 3. 检查半径和高度是否满足严格递减。
#
# 4. 检查剩余体积是否还有可行方案。
#
# 5. 检查面积下界是否已经不可能更优。
#
# 6. 选择当前层，递归设计上一层。
#
# 7. 所有层设计完成且体积恰好为 n 时，更新 best。
#
#
# 十四、复杂度
#
# 这道题的 DFS 最坏情况下仍然是指数级，
# 很难用简单的多项式复杂度表示。
#
# 但实际搜索规模会被以下剪枝大幅压缩：
#
#     1. 半径严格递减；
#     2. 高度严格递减；
#     3. 剩余最小体积剪枝；
#     4. 剩余最小表面积剪枝；
#     5. 体积-侧面积估价剪枝；
#     6. 从大到小搜索尽早得到较优答案。
#
# 递归深度最多为 M，因此递归栈空间为：
#
#     O(M)
#
# min_vol 和 min_side 数组空间为：
#
#     O(M)
#
# 总辅助空间复杂度为：
#
#     O(M)
#
# 本题真正的难点不在 DFS 本身，
# 而在于构造足够强、同时不会误剪的剪枝下界。
