# 模板KMP 双指针 字符串匹配
import sys


def build_longest_border_lengths(pattern):

    '''
    border_lengths[i] 表示 pattern[0:i+1] 的最长 border长度，形象的说是 pattern的长度为 i + 1的前缀子串的最长 border长度,前缀子串长度最短为1,最长为n
    border 即是在pattern[0:i+1]中既是前缀又是后缀，但不是字符串本身的子串。所以 如 "abab" 的 border_lengths[2] 为 1。
    '''
    n = len(pattern)
    border_lengths = [0]*n

    match_len = 0

    for i in range(1,n):

        while match_len > 0 and pattern[i] != pattern[match_len]:
            match_len = border_lengths[match_len-1] #获得前缀长度为match_len的最长 border长度

        if pattern[i] == pattern[match_len]:    
            match_len += 1
    
        border_lengths[i] = match_len
    
    return border_lengths


def main():
    data = sys.stdin.readlines()
    s1 = data[0].strip()
    s2 = data[1].strip()
    
    border_lengths = build_longest_border_lengths(s2)

    ans = []
    match_len = 0

    for i in range(len(s1)):
        while match_len > 0 and s1[i] != s2[match_len]:
            match_len = border_lengths[match_len-1]
        
        if s1[i] == s2[match_len]:
            match_len += 1
        
        if match_len == len(s2):
            ans.append( i - len(s2) + 2) #ans的起点是1，i的起点是0

            # 允许重叠匹配，继续回退到最长 border
            match_len = border_lengths[match_len-1]

    output = []
    for pos in ans:
        output.append(str(pos))
    
    output.append(" ".join(map(str,border_lengths)))
    sys.stdout.write("\n".join(output))

if __name__ == '__main__':
    main()
