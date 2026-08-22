#include <bits/stdc++.h>
using namespace std;

int main()
{
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, q;
    cin >> n >> q;

    vector<bool> isComposite(n + 1, false);
    vector<int> primes;

    for (int i = 2; i <= n; ++i)
    {
        // i 没有被标记，说明 i 是质数
        if (!isComposite[i])
        {
            primes.push_back(i);
        }

        // 用质数筛选 i 的倍数
        for (int p : primes)
        {
            long long value = 1LL * i * p;

            if (value > n)
            {
                break;
            }

            isComposite[value] = true;

            // 保证每个合数只被最小质因数筛选一次
            if (i % p == 0)
            {
                break;
            }
        }
    }

    while (q--)
    {
        int k;
        cin >> k;

        // 第 k 小的素数在下标 k - 1 的位置
        cout << primes[k - 1] << '\n';
    }

    return 0;
}