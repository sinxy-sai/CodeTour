# DFS + 回溯 + 约束判断 + 最少候选数剪枝
import sys

FULL = (1 << 9) - 1 #111111111

def main():
    data = []
    for _ in range(9):
        data.append(list(map(int,sys.stdin.buffer.readline().split())))


    # row_mask[i] 表示第 i 行已经使用的数字（位掩码）
    # col_mask[i] 表示第 i 列已经使用的数字（位掩码）
    # box_mask[i] 表示第 i 个 九宫格已经使用的数字（位掩码）
    row_mask = [0]*9
    col_mask = [0]*9
    box_mask = [0]*9

    blanks = []

    for r in range(9):
        for c in range(9):
            value = data[r][c]
            if value == 0:
                blanks.append((r,c))
                continue

            # 如果某一位是 1，说明这个数字已经被使用。
            bit = 1 << (value - 1) # 比如 value == 5,bit = 000010000
            box = (r // 3) * 3 + c // 3
            row_mask[r] |= bit
            col_mask[c] |= bit
            box_mask[box] |= bit

    def dfs(index):
        # 递归结束条件：所有空白位置都被填充
        if index == len(blanks):
            return True

        best_index = index
        best_candidates = 0
        best_count = 10

        # 枚举候选数字
        for i in range(index,len(blanks)):
            r,c = blanks[i]
            box = (r // 3) * 3 + c // 3

            used = row_mask[r] | col_mask[c] | box_mask[box]
            candidates = FULL ^ used #异或
            # bit_count() 表示二进制中 1 的个数 例如001000.bit_count() == 1
            candidates_count = candidates.bit_count()

            # 约束判断：当前位置没有候选数字
            if candidates_count == 0:
                return False

            # 最少候选数剪枝
            if candidates_count < best_count:
                best_index = i
                best_candidates = candidates
                best_count = candidates_count

                if best_count == 1:
                    break

        blanks[index],blanks[best_index] = blanks[best_index],blanks[index]

        r,c = blanks[index]
        box = (r // 3) * 3 + c // 3
        candidates = best_candidates

        # 枚举候选数字
        while candidates:
            # 取最低位的 1
            bit = candidates & -candidates
            # 从候选数字中移除最低位的 1
            candidates -= bit
            # bit_length() 表示最高位的 1 位于第几位之后 例如001000.bit_length() == 4
            digit = bit.bit_length()
            data[r][c] = digit
            row_mask[r] |= bit
            col_mask[c] |= bit
            box_mask[box] |= bit
            if dfs(index + 1):
                return True
            # 回溯
            data[r][c] = 0
            row_mask[r] ^= bit
            col_mask[c] ^= bit
            box_mask[box] ^= bit

        blanks[index],blanks[best_index] = blanks[best_index],blanks[index]
        return False

    dfs(0)

    out = []
    for row in data:
        out.append(' '.join(map(str,row)))
    sys.stdout.write('\n'.join(out))

if __name__ == '__main__':
    main()