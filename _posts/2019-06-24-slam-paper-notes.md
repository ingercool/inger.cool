---
title: "论文粗读|Past, Present, and Future of SLAM"
layout: post
date: 2019-06-24
tag: 
- Paper Reading Notes
category: blog
author: ingerchao
description: The notes of mac using
---

## Past, Present, and Future of SLAM: Towards the Robust-Perception Age

本篇论文从当下的SLAM领域的研究现状入手，回顾了相关的工作，检阅了大量相关领域的 paper，包括mapping 长期以来的健壮性和可移植性；mapping 的度量和语义表示、理论性能，并探索了一些SLAM技术应用的其他新领域；以批判性的眼光看待已经发表的文章，描绘了新的挑战和仍然值得研究的问题。

同时也包括作者对两个热议问题的看法：机器人真的需要SLAM吗？通过学者们的努力，SLAM问题解决了吗？

### Introduction

SLAM的应用环境主要有两种，一种是辅助其他的任务，比如为人们提供直观的路径导航，另一种是用于降低在估算机器人状态时的误差。

循环闭合（loop closure）：机器人通过查找已知区域重置定位错误的情况。因此，SLAM在不同的场景中扮演不同的角色，先前的 MAP 大多都不可用，需要重新构建。

> SLAM aims at building a globally consistent representation
> of the environment, leveraging both ego-motion measurements
> and loop closures.
>
> However, more recent odometry algorithms are based on visual and inertial information, and have very small drift.

![vio-vs-slvm](/assets/images/paper/vio-vs-slam.png)

当构建从起点 A 到终点 B 的地图时，左图为基于 odometry 里程计算的 Map，可以看出是一条长长的路径，而 SLAM 通过 loop closures，走到 C 点时会发现 C 到 B 有直达的短路径。

可以从以下几个方面评估 SLAM 的成熟度问题：robot, environment, performance requirements. 例如，将 2D 室内环境与配有车轮编码器和激光扫描仪的机器人结合进行映射，具有足够的精度和鲁棒性（Kuka导航解决方案）； 缓慢移动的基于视觉的 SLAM 机器人（火星探测机器人、家用机器人）；还有视觉惯性测距（vision-inertial odometry）也是一个比较成熟的领域。

robor/enviornment/performance 三方面依然需要大量的基础研究，当下的 SLAM 算法在机器人快速移动或复杂环境下很容易就会失败，同样，SLAM 算法也不能满足严格的性能要求。

![slam-age](/assets/images/paper/slam-age.png)

在过去三十年间，SLAM 领域取得了很大进展， 前 20 年成为 *classical age*，引入了 SLAM 的主要概率公式，包括基于扩展 Kalman 过滤器、Rao-Blackwellized粒子滤波器和最大似然估计的方法，阐明了与强大数据关联的基本挑战。接下来的一段时间是2004-2015，称之为 *algorithmic-analysis age*，引入了 SLAM 的基础要素，包括 observability, convergence, consistency. 这段时间主要研究问题是 SLAM 的效率和理解问题。

这篇论文认为当下进入了第三个阶段，*robust-perception age*。本阶段有以下几个关键特征：

- robust performance：在广泛的环境中长时间以较低的故障率运行；该系统包括故障安全机制，并具有根据情况选择系统参数的自调整功能
- high-level understanding ：对环境的高级理解；
- resource awareness：对可用的传感和计算资源进行定制，并提高根据可利用资源调整计算负载的方法；
- Task-driven perception：要求 SLAM 系统能够以任务为驱动，自主选择相关的感知信息，过滤掉不相关的传感器数据；生成自适应的地图表示，其复杂性可能因任务而异。

以下的章节可以自行选择自己感兴趣的阅读（我选择先不读）。

###Anatomy of  a Modern  SLAM System

### Long-Term Autonomy  I: Robustness

### Long-Term Autonomy II: Scalability

### Representation I: Metric Map Models

### Representation II: Semantic Map Models

### New Theoretical Tools for SLAM

### Active SLAM

### New Frontiers: Sensors and Learning

### Conclusion

SLAM 在很多领域都有着非常重要的应用，包括与 SLAM 息息相关的 VIO领域，在实际生活中也已经落地了许多应用，从自动驾驶到移动设备，SLAM系统在 GPS 访问不到的领域或精度不够的区域提供定位和解决方案。

我们可以根据不同的任务确定更合适的的 SLAM 系统。选择最合适的SLAM系统的一种更一般的方法是将SLAM作为一种机制来计算一个足够的统计数据，该统计数据总结了机器人过去的所有观察结果，从这个意义上说，在这种压缩表示中要保留与任务密切相关的信息。

要实现真正强大的感知、导航和长期使用的机器人，SLAM 目前还尚未得到解决，需要更多学者的努力和研究。

可以使用新型传感器、新工具（例如凸面松弛和对偶理论或深度学习）以及主动感知等技术来解决 SLAM 问题。SLAM仍然是大多数机器人应用程序不可或缺的支柱，尽管在过去几十年中取得了惊人的进展，但现有的SLAM系统远不能提供与人类轻松创建和使用的环境模型相比具有洞察力、可操作性和紧凑性的环境模型。

-----------

[Past, Present, and Future of Simultaneous Localization And Mapping: Towards the Robust-Perception Age](https://arxiv.org/abs/1606.05830) (2016)