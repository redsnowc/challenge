## 简述

- 希望大家讨论各种写法，指出我的错误。

- 作业外部文件也一并放在了对应的挑战目录中。

- 除多线程工资计算器无法运行在windows下外，其它挑战均无问题。

### 关于挑战21 世界温室气体排放与气温变化关联分析

该挑战绘图部分我尝试了三个版本：

- `challenge3_1.py`是不需要对实验环境做任何改动的版本，但是实际效果和示意图有所出入。
- `challenge3_2.py`这个版本是我根据个人喜好改动的版本，但需要升级实验楼测试环境下的 `matplotlib`才可通过挑战。
- `challenge3_3.py`此版本基本还原了示例图。
  -  **注意** 该版本所绘第一张图表实际上是有问题的，问题出在 x 轴坐标上，该图相隔两年和相隔三年的坐标距离是相等的，这并符合实际。

上述三个版本均可通过挑战。

三个版本效果图如下：（不同操作环境下，可能实际效果会有不同）

- `challenge3_1.py`
![1](https://github.com/redsnowc/challenge/blob/master/%E6%8C%91%E6%88%9821%20%E4%B8%96%E7%95%8C%E6%B8%A9%E5%AE%A4%E6%B0%94%E4%BD%93%E6%8E%92%E6%94%BE%E4%B8%8E%E6%B0%94%E6%B8%A9%E5%8F%98%E5%8C%96%E5%85%B3%E8%81%94%E5%88%86%E6%9E%90/challenge3_1.png)

- `challenge3_2.py`
![2](https://github.com/redsnowc/challenge/blob/master/%E6%8C%91%E6%88%9821%20%E4%B8%96%E7%95%8C%E6%B8%A9%E5%AE%A4%E6%B0%94%E4%BD%93%E6%8E%92%E6%94%BE%E4%B8%8E%E6%B0%94%E6%B8%A9%E5%8F%98%E5%8C%96%E5%85%B3%E8%81%94%E5%88%86%E6%9E%90/challenge3_2.png)

- `challenge3_3.py`
![3](https://github.com/redsnowc/challenge/blob/master/%E6%8C%91%E6%88%9821%20%E4%B8%96%E7%95%8C%E6%B8%A9%E5%AE%A4%E6%B0%94%E4%BD%93%E6%8E%92%E6%94%BE%E4%B8%8E%E6%B0%94%E6%B8%A9%E5%8F%98%E5%8C%96%E5%85%B3%E8%81%94%E5%88%86%E6%9E%90/challenge3_3.png)
