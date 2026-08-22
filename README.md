<div align="center">

# CodeTour

<p>基于 <a href="https://www.luogu.com.cn/">洛谷</a> 的个人算法与数据结构学习记录。</p>

<p>
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/language-Python%203-3776AB?logo=python&logoColor=white" alt="Python 3"></a>
  <a href="https://isocpp.org/"><img src="https://img.shields.io/badge/language-C%2B%2B-00599C?logo=cplusplus&logoColor=white" alt="C++"></a>
  <a href="https://www.luogu.com.cn/"><img src="https://img.shields.io/badge/platform-%E6%B4%9B%E8%B0%B7-EA2027" alt="Luogu"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-green.svg" alt="MIT License"></a>
</p>

<p>系统整理算法与数据结构题目的实现、复盘和专题笔记。代码以 Python 为主，部分题目提供 C++ 对照版本。</p>

</div>

## 目录结构

```text
算法/
├─ 动态规划/
│  ├─ 背包/          # 01 背包、完全背包、多重背包、前 K 优解等
│  ├─ 区间/          # 区间 DP
│  ├─ 线性/          # 线性 DP
│  ├─ 树形/          # 树形 DP 预留专题
│  └─ 状压/          # 状态压缩 DP 预留专题
├─ 线性数据结构/
│  ├─ 栈/            # 栈、单调栈
│  └─ 队列/          # 队列、双端队列、单调队列
├─ 非线性数据结构/
│  ├─ 堆/            # 堆与优先队列
│  ├─ 并查集/        # 集合合并与连通性查询
│  ├─ 树/            # 二叉树、LCA、树遍历、哈夫曼树
│  ├─ 字典树/        # Trie
│  └─ 区间数据结构/  # 树状数组、线段树、ST 表
├─ 图论/             # 拓扑排序、最短路、最小生成树、Floyd、LCA
├─ 搜索/             # DFS、BFS、回溯、剪枝、状压搜索
├─ 字符串/           # KMP、Manacher、AC 自动机
├─ 数学/             # 数论、快速幂、筛法、矩阵、线性代数等
└─ 哈希/             # 字符串哈希、数值哈希、计数与查找
```

## 当前进度

截至 **2026 年 8 月 22 日**，仓库共有 **100 个代码文件**：

- Python：90 个
- C++：10 个
- 专题总结：7 份

| 分类 | 代码数量 | 主要覆盖内容 |
| --- | ---: | --- |
| 动态规划 | 28 | 背包、线性 DP、区间 DP |
| 非线性数据结构 | 19 | 堆、并查集、树、Trie、树状数组、线段树、ST 表 |
| 数学 | 12 | 数论、筛法、快速幂、矩阵、线性方程组 |
| 搜索 | 13 | DFS、BFS、组合、排列、数独、剪枝、状压搜索 |
| 哈希 | 10 | 字符串哈希、数值哈希、计数 |
| 线性数据结构 | 8 | 栈、单调栈、队列、双端队列、单调队列 |
| 字符串 | 5 | KMP、Manacher、AC 自动机 |
| 图论 | 5 | 拓扑排序、Floyd、Dijkstra、最小生成树 |
| **合计** | **100** |  |

> 注：同一道题的不同实现会分别保留，例如带有 `_ez` 后缀的版本；代码数量不等于不同题目的数量。

## 代表性题目

<details>
<summary>动态规划</summary>

- `P1048`：01 背包
- `P1077`：组合计数与背包
- `P1757`：混合背包
- `P1833`：混合背包与时间规划
- `P1775`、`P2858`、`P4170`：区间 DP
- `B3637`、`P1095`、`P1115`、`P1216`：线性 DP
- `P1858`：前 K 优解背包

</details>

<details>
<summary>搜索与回溯</summary>

- `B3625_1`、`B3625_2`：迷宫 BFS 与 DFS
- `P1162`、`P1443`：Flood Fill 与网格最短路
- `P1036`：组合搜索与记忆化搜索
- `P1157`、`P1706`：组合与全排列
- `P1219`：八皇后与对角线剪枝
- `P1731`：多参数搜索、可行性剪枝、最优性剪枝
- `P1784`：数独、位掩码、MRV 剪枝
- `P2392`：二叉决策 DFS 与子集划分
- `P1433`：状态压缩搜索与记忆化 DP

</details>

<details>
<summary>图论</summary>

- `B3644`：拓扑排序
- `B3647`：Floyd 全源最短路
- `P3371`：Dijkstra 单源最短路
- `P3366`：Kruskal、并查集与最小生成树
- `P3379`：倍增 LCA

</details>

<details>
<summary>非线性与区间数据结构</summary>

- `P3378`：堆与优先队列
- `P3367`：并查集
- `P1305`、`B3642`、`P4913`：二叉树建立、遍历与深度
- `B2168`：哈夫曼树与哈夫曼编码
- `P8306`：Trie 前缀统计
- `P3374`、`P3368`：树状数组
- `P3372`、`P3373`：线段树与懒标记
- `P3865`：ST 表与 RMQ

</details>

<details>
<summary>字符串</summary>

- `P3375`：KMP
- `P3805`：Manacher
- `P3808`：AC 自动机

</details>

<details>
<summary>数学与哈希</summary>

- 数学目录包含质数、因数、快速幂、逆元、筛法、矩阵运算、线性方程组等题目。
- 哈希目录包含字符串哈希、数值哈希、重复结构查找和计数类题目。

</details>

## 学习路线

当前的学习顺序大致为：

```text
线性数据结构
    ↓
树、堆、并查集、Trie
    ↓
树状数组、线段树、ST 表
    ↓
DFS、BFS、回溯与剪枝
    ↓
动态规划
    ↓
图论与字符串算法
    ↓
数学算法、哈希与更复杂的综合题
```

搜索专题中的基本范式：

```text
组合：start
排列：used
网格搜索：visited
约束搜索：候选集合 + 剪枝
状压搜索：mask
```

动态规划专题重点记录：

```text
状态定义
状态转移
初始化
遍历顺序
空间优化
复杂度分析
```

## 文件规范

- 解题代码使用 Python 3 编写，文件名以题号为主，例如 `P1048.py`、`B2173.py`。
- C++ 对照实现使用 `.cpp` 后缀。
- 同题的补充实现通过简短后缀区分，例如 `P1077_ez.py`。
- 专题知识整理统一命名为 `总结.md`。
- 代码尽量保留状态定义、转移过程、边界处理和复杂度说明。
- 代码注释以帮助理解算法为主，避免与语句含义重复的空泛注释。

## 本地运行

克隆仓库：

```bash
git clone https://github.com/sinxy-sai/CodeTour.git
cd CodeTour
```

运行 Python 题目：

```bash
python "搜索/P1784.py"
```

运行 C++ 题目：

```bash
g++ -std=c++17 -O2 "非线性数据结构/区间数据结构/P3372.cpp" -o main
./main
```

Windows PowerShell 下可以使用：

```powershell
g++ -std=c++17 -O2 "非线性数据结构/区间数据结构/P3372.cpp" -o main.exe
.\main.exe
```

程序按照洛谷题目的标准输入格式读取数据，并将答案输出到标准输出。题目要求、输入格式和样例请以洛谷对应题目页面为准。

## 代码说明

本仓库以“理解算法模型”为主要目标：

1. 先独立分析题目和数据范围。
2. 明确状态、选择、转移和终止条件。
3. 编写 Python 版本并通过样例与评测。
4. 对容易混淆的代码补充中文注释。
5. 对性能敏感的题目记录 TLE、MLE、RE 等问题。
6. 必要时使用 C++ 对照实现，理解语言性能差异。

部分题目存在多种实现，例如：

- 递归与非递归；
- 普通写法与 `_ez` 简化写法；
- Python 与 C++；
- 暴力搜索与剪枝搜索。

这些版本会根据学习过程同时保留，便于比较不同算法和实现方式。

## 使用说明

仓库内容是个人学习过程的记录，解法不一定是唯一或最优实现。建议先独立思考，再将代码作为思路参考；不同语言版本、Python 版本和评测环境可能影响运行结果。

## License

本项目基于 [MIT License](LICENSE) 开源。
