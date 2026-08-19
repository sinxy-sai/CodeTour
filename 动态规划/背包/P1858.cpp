// 前 K 优解背包 + 恰好装满背包 + 01 背包
#include <bits/stdc++.h>
using namespace std;

int main()
{
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int K, V, N;
    cin >> K >> V >> N;

    vector<pair<int, long long>> items(N);

    for (int i = 0; i < N; i++)
    {
        int w;
        long long value;

        cin >> w >> value;
        items[i] = {w, value};
    }

    const long long NEG = -(1LL << 60);

    // dp[capacity * K + rank]
    // 表示恰好装满 capacity 时，第 rank 优的价值
    vector<long long> dp(
        1LL * (V + 1) * K,
        NEG);

    // 恰好装满容量 0 的最优方案价值为 0
    dp[0] = 0;

    vector<long long> temp(K, NEG);

    for (auto [w, value] : items)
    {
        // 01 背包，容量必须倒序
        for (int capacity = V; capacity >= w; capacity--)
        {
            long long base = 1LL * capacity * K;
            long long prev = 1LL * (capacity - w) * K;

            // capacity - w 无法恰好装满，不能转移
            if (dp[prev] == NEG)
            {
                continue;
            }

            // 当前物品即使接到最优方案上，
            // 也进不了当前容量的前 K 名，可以直接跳过
            if (dp[base + K - 1] != NEG &&
                dp[prev] + value <= dp[base + K - 1])
            {
                continue;
            }

            int p1 = 0;
            int p2 = 0;

            for (int rank = 0; rank < K; rank++)
            {
                long long value1 = NEG;
                long long value2 = NEG;

                // 不选当前物品
                if (p1 < K)
                {
                    value1 = dp[base + p1];
                }

                // 选当前物品
                if (p2 < K && dp[prev + p2] != NEG)
                {
                    value2 = dp[prev + p2] + value;
                }

                if (value1 > value2)
                {
                    temp[rank] = value1;
                    p1++;
                }
                else
                {
                    temp[rank] = value2;
                    p2++;
                }
            }

            // 更新当前容量的前 K 优解
            for (int rank = 0; rank < K; rank++)
            {
                dp[base + rank] = temp[rank];
            }
        }
    }

    long long answer = 0;
    long long start = 1LL * V * K;

    for (int rank = 0; rank < K; rank++)
    {
        answer += dp[start + rank];
    }

    cout << answer << '\n';

    return 0;
}