#include <bits/stdc++.h>
using namespace std;

int manacher(const string& s) {
    int n = static_cast<int>(s.size());
    int ans = 1;

    // d1[i]：
    // 以 i 为中心的最长奇数回文半径
    vector<int> d1(n, 0);

    int left = 0;
    int right = -1;

    // 处理奇数长度回文
    for (int i = 0; i < n; i++) {
        int radius;

        if (i > right) {
            radius = 1;
        } else {
            // i 关于当前回文中心的镜像位置
            int mirror = left + right - i;

            // 继承镜像位置的半径，
            // 但不能超过当前已知回文的右边界
            radius = min(d1[mirror], right - i + 1);
        }

        // 向两边扩展
        while (
            i - radius >= 0 &&
            i + radius < n &&
            s[i - radius] == s[i + radius]
        ) {
            radius++;
        }

        d1[i] = radius;

        // 奇数回文长度
        int length = 2 * radius - 1;
        ans = max(ans, length);

        // 更新右端点最靠右的回文区间
        if (i + radius - 1 > right) {
            left = i - radius + 1;
            right = i + radius - 1;
        }
    }

    // 释放 d1，降低内存峰值
    vector<int>().swap(d1);

    // d2[i]：
    // 以 i-1 和 i 之间的空隙为中心的偶数回文半径
    vector<int> d2(n, 0);

    left = 0;
    right = -1;

    // 处理偶数长度回文
    for (int i = 0; i < n; i++) {
        int radius;

        if (i > right) {
            radius = 0;
        } else {
            // 偶数回文的镜像位置
            int mirror = left + right - i + 1;

            radius = min(d2[mirror], right - i + 1);
        }

        // 向两边扩展
        while (
            i - radius - 1 >= 0 &&
            i + radius < n &&
            s[i - radius - 1] == s[i + radius]
        ) {
            radius++;
        }

        d2[i] = radius;

        // 偶数回文长度
        int length = 2 * radius;
        ans = max(ans, length);

        // 当前偶数回文区间为：
        // [i - radius, i + radius - 1]
        if (i + radius - 1 > right) {
            left = i - radius;
            right = i + radius - 1;
        }
    }

    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string s;
    cin >> s;

    cout << manacher(s) << '\n';

    return 0;
}