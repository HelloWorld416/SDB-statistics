# StreamDriveBench release statistics — 1,935 QA

统计分支：**v2**。数据版本：**StreamDriveBench-1935-v1**。统计日期：2026-10-31。QA 与事件统计来自当前最终 release；视频总量、时长分布、三类 QA 名称和四大类／14 小类映射沿用原统计版本。

## 1. 总体规模与统计口径

| 指标 | 数值 |
| --- | --- |
| 视频总数 | 648 |
| 总选用时长（论文展示） | 100 h |
| 总选用时长（沿用素材统计，小时） | 100.00445718 |
| 总选用时长（沿用素材统计，秒） | 360016.045836 |
| QA 总数 | 1935 |
| QA 关联事件组总数（含独立负例组） | 815 |
| 原 14 个行为小类中的事件组 | 705 |
| 独立未触发负例事件组 | 110 |
| 行为小类数 | 14 |
| QA 覆盖视频数 | 504 |


整体素材仍为 **648 个视频、约 100 小时**。第 3 节的视频时长分布完整沿用原分支，未用最终 QA 覆盖的 504 个视频重新计算素材总量。时长是选用片段长度，不是完整下载视频时长或每题输入窗口之和。

“事件数量与 1,935 条 QA 对齐”表示只计这些问题实际关联的事件，以 `(dataset, episode_id, event_id)` 去重；一组可关联多条 QA，因此是 **815 个事件组**，不是 1,935 个独立事件。所有 QA 已按正式 release 标为人工审核通过；该状态不等于事件分类或三题严格关联关系均经过独立人工验收。

## 2. 三类 QA 数量

| QA 类型 | 数量 | 占全部 QA 的比例（%） |
| --- | --- | --- |
| History QA | 700 | 36.1757 |
| Prediction QA | 552 | 28.5271 |
| Event QA | 683 | 35.2972 |
| Total | 1935 | 100.0000 |


三类名称统一为 **History QA、Prediction QA、Event QA**，分别对应历史理解、短期预测和事件触发响应。

### 按数据来源统计

| 数据源 | 视频数量 | 选用时长（h） | History QA | Prediction QA | Event QA | QA 合计 | 事件组数量 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| nuScenes | 50 | 0.270361 | 25 | 10 | 15 | 50 | 28 |
| PIE | 53 | 8.421111 | 167 | 121 | 200 | 488 | 206 |
| KITTI-360 | 18 | 2.189828 | 98 | 81 | 92 | 271 | 114 |
| BDD100K | 50 | 0.560000 | 0 | 0 | 0 | 0 | 0 |
| Boreas | 125 | 11.944546 | 108 | 68 | 106 | 282 | 129 |
| OpenDV-YouTube | 352 | 76.618611 | 302 | 272 | 270 | 844 | 338 |
| Total | 648 | 100.004457 | 700 | 552 | 683 | 1935 | 815 |


## 3. 视频时长分布：每 5 分钟一个区间

区间使用**左闭右开**规则，例如 `[5, 10)` 表示 5 分钟 ≤ 时长 < 10 分钟；恰好 10 分钟的视频计入 `[10, 15)`。百分比分母为 648 个视频。各区间长度均为 5 分钟，不合并 20–25 与 25–30 分钟；当前没有达到 30 分钟的视频。

| 时长区间（min） | 下界（s，含） | 上界（s，不含） | 视频数量 | 视频占比（%） | 区间累计选用时长（h） |
| --- | --- | --- | --- | --- | --- |
| [0, 5) | 0 | 300 | 145 | 22.3765 | 2.850398 |
| [5, 10) | 300 | 600 | 220 | 33.9506 | 22.958698 |
| [10, 15) | 600 | 900 | 155 | 23.9198 | 29.824556 |
| [15, 20) | 900 | 1200 | 58 | 8.9506 | 17.314972 |
| [20, 25) | 1200 | 1500 | 70 | 10.8025 | 27.055833 |
| [25, 30) | 1500 | 1800 | 0 | 0.0000 | 0.000000 |
| Total | — | — | 648 | 100.0000 | 100.004457 |

### 各数据源的视频时长分布

| 数据源 | [0, 5) min | [5, 10) min | [10, 15) min | [15, 20) min | [20, 25) min | [25, 30) min | 合计 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| nuScenes | 50 | 0 | 0 | 0 | 0 | 0 | 50 |
| PIE | 1 | 14 | 38 | 0 | 0 | 0 | 53 |
| KITTI-360 | 0 | 18 | 0 | 0 | 0 | 0 | 18 |
| BDD100K | 50 | 0 | 0 | 0 | 0 | 0 | 50 |
| Boreas | 44 | 68 | 7 | 6 | 0 | 0 | 125 |
| OpenDV-YouTube | 0 | 120 | 110 | 52 | 70 | 0 | 352 |
| Total | 145 | 220 | 155 | 58 | 70 | 0 | 648 |

## 4. 驾驶事件类型与数量

沿用当前 release 的 `event_category`。下表百分比分母为 **815 个 QA 关联事件组**；每个事件组只计一次。原有 14 个行为小类继续保留，新增 release 标签 `Verified non-triggering event` 单列为负例补充项，不将其视为第 15 种已发生的驾驶行为。

| Event type | 中文类别 | 事件组数量 | 占全部事件组（%） | History QA | Prediction QA | Event QA | QA 合计 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Turns / road bends | 转弯／沿道路弯曲行驶 | 229 | 28.0982 | 228 | 180 | 183 | 591 |
| Traffic-signal changes | 交通信号变化 | 101 | 12.3926 | 100 | 85 | 93 | 278 |
| Starting / acceleration | 起步／加速 | 88 | 10.7975 | 88 | 44 | 85 | 217 |
| Vehicle-light changes | 车辆灯光变化 | 55 | 6.7485 | 55 | 39 | 55 | 149 |
| Passing / relative motion | 会车／超越／相对运动 | 50 | 6.1350 | 49 | 45 | 14 | 108 |
| Stopping / deceleration | 停车／减速 | 46 | 5.6442 | 46 | 42 | 38 | 126 |
| Lane changes / merges | 变道／汇入 | 41 | 5.0307 | 41 | 35 | 35 | 111 |
| Junction / landmark passage | 通过路口／道路标志物 | 35 | 4.2945 | 33 | 31 | 21 | 85 |
| Pedestrian / cyclist actions | 行人／骑行者行为 | 35 | 4.2945 | 35 | 27 | 33 | 95 |
| Crossing traffic | 横向穿行交通 | 8 | 0.9816 | 8 | 8 | 7 | 23 |
| Road-section entry / exit | 道路区段进入／驶出 | 8 | 0.9816 | 8 | 8 | 5 | 21 |
| Visibility changes | 可见性变化 | 5 | 0.6135 | 5 | 5 | 0 | 10 |
| Multiple transition types | 多种变化类型 | 2 | 0.2454 | 2 | 2 | 2 | 6 |
| Other transitions | 其他变化 | 2 | 0.2454 | 2 | 1 | 2 | 5 |
| Verified non-triggering event | 已核验未触发事件（负例补充项） | 110 | 13.4969 | 0 | 0 | 110 | 110 |
| Total | 合计 | 815 | 100.0000 | 700 | 552 | 683 | 1935 |


类别为 release 保存的描述性标记，未重新对修订后的每道题进行语义分类。尤其普通上下文关联组的三道题可能涉及不同状态变化，表中 QA 按所属事件组的类别汇总。

### 四个事件大类

小类到大类的映射与原分支一致；**Other transitions、Visibility changes、Multiple transition types 仍归入长尾事件**。四个大类涵盖 705 个有原分类标签的事件组；大类内部占比的分母为 705，另列以全部 815 组为分母的比例。110 个独立未触发负例组不强行归入某种驾驶行为，也不并入长尾事件。

| 大类 | English label | 包含的小类（事件组数） | 事件组数量 | 占四类合计（%） | 占全部事件组（%） |
| --- | --- | --- | --- | --- | --- |
| 车辆运动行为 | Vehicle maneuvers | Turns / road bends (229)；Starting / acceleration (88)；Lane changes / merges (41)；Stopping / deceleration (46) | 404 | 57.3050 | 49.5706 |
| 交通交互与参与者状态 | Road-user interactions and states | Vehicle-light changes (55)；Passing / relative motion (50)；Pedestrian / cyclist actions (35)；Crossing traffic (8) | 148 | 20.9929 | 18.1595 |
| 道路与场景变化 | Road and scene changes | Traffic-signal changes (101)；Junction / landmark passage (35)；Road-section entry / exit (8) | 144 | 20.4255 | 17.6687 |
| 长尾事件 | Long-tail events | Other transitions (2)；Visibility changes (5)；Multiple transition types (2) | 9 | 1.2766 | 1.1043 |
| 四类合计 | Total classified | 14 个小类 | 705 | 100.0000 | 86.5031 |
| 负例补充项 | Verified non-triggering event | 不属于四个行为大类 | 110 | — | 13.4969 |
| 全体合计 | Total |  | 815 | — | 100.0000 |


“车辆运动行为”包含自车及其他车辆的方向、车道和速度变化；“交通交互与参与者状态”包含相对运动、穿行、行人／骑行者动作和灯光状态；“道路与场景变化”包含交通设施状态及通行进程。不能将车辆运动行为直接等同于自车行为。

#### 大类对应的三类 QA 数量

| 大类 | History QA | Prediction QA | Event QA | QA 合计 |
| --- | --- | --- | --- | --- |
| 车辆运动行为 | 403 | 301 | 341 | 1045 |
| 交通交互与参与者状态 | 147 | 119 | 109 | 375 |
| 道路与场景变化 | 141 | 124 | 119 | 384 |
| 长尾事件 | 9 | 8 | 4 | 21 |
| 负例补充项（不属于四类） | 0 | 0 | 110 | 110 |
| 合计 | 700 | 552 | 683 | 1935 |


绘图数据：[大类统计 CSV](event_macro_counts.csv) · [分类映射 CSV](event_macro_mapping.csv) · [全部事件类别 CSV](event_type_counts.csv) · [独立负例补充 CSV](event_negative_supplement.csv)。`event_macro_counts.csv` 中 `event_percentage` 以 705 为分母，`all_event_percentage` 以 815 为分母。

### 事件组的三类 QA 组成

| 事件组组成 | 事件组数量 | 贡献 QA 数量 |
| --- | --- | --- |
| 三类齐全 | 444 | 1332 |
| 包含两类 | 232 | 464 |
| 包含一类 | 139 | 139 |
| Total | 815 | 1935 |


444 个三类齐全组中，66 组具有源标注的严格关联标记，378 组为普通上下文关联。Event QA 包含 **572 条正例、111 条未触发负例**；其中 110 条组成上述独立负例组，另 1 条仍在原分类的事件组内，因此不能将 110 解释为全部负例数。

## 5. Queries Temporal Distribution

将三类 QA 合并，每条问题计一次；时间为 `query_second - selection_start_sec`，相对于选用片段起点。Event QA 使用问题注入时刻，不使用事件触发或轮询时刻。保持原来的七个左闭右开区间，百分比分母改为 1,935。

| 片段内提问时间区间（s） | QA 数量 | 占全部 QA（%） |
| --- | --- | --- |
| [0, 30) | 154 | 7.9587 |
| [30, 90) | 261 | 13.4884 |
| [90, 180) | 317 | 16.3824 |
| [180, 300) | 449 | 23.2041 |
| [300, 600) | 515 | 26.6150 |
| [600, 1200) | 207 | 10.6977 |
| [1200, 1800) | 32 | 1.6537 |
| Total | 1935 | 100.0000 |


绘图时使用单个数据系列；横轴为 **Time since selected clip start (s)**，纵轴为 **Number of queries**。数量依次为 `154, 261, 317, 449, 515, 207, 32`。区间宽度不等，按区间类别绘制柱状图，柱高表示数量。

绘图数据：[Queries Temporal Distribution CSV](queries_temporal_distribution.csv)。

## 6. 绘图与复现说明

- 视频分布沿用 `145, 220, 155, 58, 70, 0`，分母 648。
- QA 分布为 `700, 552, 683`，分母 1,935。
- 全部事件组分布含负例补充项，分母 815；四个原大类内部分布的分母为 705。
- CSV 百分比以 0–100 表示，均不含合计行。用整数计数计算比例可避免舍入累计误差。

本分支从 GitHub 已发布统计提交 `8165f4b` 创建，原分支保留 4,013 条版本。视频素材基线与分类映射固定保存在 [video_and_taxonomy_baseline.json](scripts/video_and_taxonomy_baseline.json)，当前 release 的视频目录仅覆盖 504 个 QA 视频，不用于覆盖完整素材基线。

底层字段对应：`HGI → History QA`，`AD → Prediction QA`，`ETP → Event QA`。本次只更新统计，不修改 release。

复现命令：

```bash
python scripts/build_v2_statistics.py --release /path/to/StreamDriveBench-release/data
```

| 源文件 | SHA-256 |
| --- | --- |
| release_manifest.json | b46cd592a3f70cdef6c0a45b77a4a475d94a3ab9970ce5526ea8d0088cdca43a |
| model_inputs.json | 781ae3432a87e3866e1d3e0fd08d892fbc641291f182ed3f522c294e5dc2a2d7 |
| episodes_metadata.json | 2931b9a49d606f95ec89a041b35b4917097cf6a644b204a93b84d5c89c520ca5 |
| event_groups.json | 55cffab78fb6038aaf492badff895a2c6865108317499d2067219a089175fba6 |
| summary.json | 0e4cbee23d3e805758c3c4a4aba932ad2fbf959f6abac33e0d9986d84053ca8f |
| labels.json | bb861cc18a4cb99098b31e5266f4f69ff825a8d97117f17d4cfdbfbfc768a9bc |


校验结果：release 全部文件哈希匹配 manifest；1,935 个唯一 query_id 全部且仅归属一个事件组；815 个事件组无重复；分类、来源和提问时间分布计数均与最终 release 一致。视频时长章节与原已发布版本逐字一致。
