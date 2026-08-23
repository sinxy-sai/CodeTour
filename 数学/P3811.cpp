#include <bits/stdc++.h>
using namespace std;

int main()
{
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, p;
    cin >> n >> p;

    vector<int> inverse(n + 1);

    inverse[1] = 1;

    for (int i = 2; i <= n; ++i)
    {
        /*
            Python：
            inverse[i] = (p - p // i) * inverse[p % i] % p

            使用 long long，避免乘法过程中 int 溢出。
        */
        inverse[i] =
            1LL * (p - p / i) * inverse[p % i] % p;
    }

    // 集中输出，减少大量输出操作
    string output;
    output.reserve(static_cast<size_t>(n) * 10);

    for (int i = 1; i <= n; ++i)
    {
        output += to_string(inverse[i]);
        output.push_back('\n');
    }

    cout << output;

    return 0;
}