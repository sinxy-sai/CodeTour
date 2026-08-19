#include <bits/stdc++.h>
using namespace std;

int parse_time(const string &time)
{
    size_t pos = time.find(':');

    int hour = stoi(time.substr(0, pos));
    int minute = stoi(time.substr(pos + 1));

    return hour * 60 + minute;
}

int main()
{
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string start, finish;
    int n;

    cin >> start >> finish >> n;

    int T = parse_time(finish) - parse_time(start);

    vector<long long> dp(T + 1, 0);

    for (int i = 0; i < n; i++)
    {
        int t;
        long long value;
        long long count;

        cin >> t >> value >> count;

        if (count == 0)
        {
            // 完全背包
            for (int capacity = t; capacity <= T; capacity++)
            {
                dp[capacity] = max(
                    dp[capacity],
                    dp[capacity - t] + value);
            }
        }
        else
        {
            // 多重背包：二进制拆分
            long long group = 1;

            while (group <= count)
            {
                long long weight = group * t;
                long long total_value = group * value;

                if (weight <= T)
                {
                    for (int capacity = T;
                         capacity >= weight;
                         capacity--)
                    {
                        dp[capacity] = max(
                            dp[capacity],
                            dp[capacity - weight] + total_value);
                    }
                }

                count -= group;
                group *= 2;
            }

            // 处理剩余物品
            if (count > 0)
            {
                long long weight = count * t;
                long long total_value = count * value;

                if (weight <= T)
                {
                    for (int capacity = T;
                         capacity >= weight;
                         capacity--)
                    {
                        dp[capacity] = max(
                            dp[capacity],
                            dp[capacity - weight] + total_value);
                    }
                }
            }
        }
    }

    cout << dp[T] << '\n';

    return 0;
}