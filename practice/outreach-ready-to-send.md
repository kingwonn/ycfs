# 即用文案:复制、粘贴、发送(不用改字)

> 三条,对三类触点。每条只问一个真问题,不像群发问卷。目标是拿到一个能翻案的
> 具体事实,不是礼貌回复。发出去后把回答记进 DIGEST / reality.py(P6:不沉淀即蒸发)。

---

## 文案 A — 给 UMI / TacUMI / UMI-FT 论文作者(邮件,英文)

> 触点:arXiv 论文通讯作者邮箱。为什么先发这个:学术作者对技术问题回复率高,
> 且没有商业动机粉饰答案。

**Subject:** Quick question on force/tactile data in VLA training pipelines

Hi Prof. [Last Name],

I've been reading your work on [UMI-FT / TacUMI] — the handheld force/tactile
data collection is exactly the direction I'm thinking about.

One question I can't answer from the papers: **in the VLA training pipelines you've
seen in practice, is force/tactile actually consumed by production models today, or
is it still mostly a research-stage modality?** I'm trying to figure out whether
building for it now is timely or premature.

Any pointer would be hugely appreciated. Thank you for the great work.

Best,
[Your name]

---

## 文案 B — 给 LeRobot / HuggingFace 机器人社区(Discord / GitHub discussion,英文)

> 触点:HF Discord 机器人频道 或 LeRobot GitHub Discussions。为什么:全球训 VLA
> 的人聚集地,答"数据卡在哪"最快最真。

Hey folks — quick question for anyone training VLA / manipulation policies on
external or collected datasets:

**When you ingest a dataset someone else collected, what breaks more often — the
format/interface (won't load into your pipeline), or the data quality itself
(sync drift, pose jitter, low usable rate after IK filtering)?**

Trying to understand where the real pain is before building anything. Also curious:
do you take end-effector-pose datasets (UMI-style), or only joint-space? Thanks!

---

## 文案 C — 给国内具身同行 / 算法工程师(私信 / 社群,中文)

> 触点:量子位丁琰分享的评论区、相关技术社群、招聘 JD 里的技术联系人。
> 为什么:一线训模型的人,直接答得出;先聊技术不聊生意,回复率高。

你好,冒昧请教一个具身数据的问题——

**你们现在训/微调用的数据,输入里带力或触觉这个模态吗?是已经在生产模型里用了,
还是只在研究阶段试?** 另外一个:你们接外部采来的数据,最常卡在哪一步,是格式读不进
管线,还是数据质量(同步、漂移、可用率)不达标?

我在判断一个方向该不该做,你的一句实话比我查十篇报告都值。谢谢!

---

## 发送顺序(按"最快拿到能翻案的事实")

1. **先 B**(开源社区,门槛最低,几小时可能有回)
2. **再 A**(学术,一两天,质量最高)
3. **再 C**(国内同行,验证商业侧)

拿到任意 2 个一致回答,就够翻/保 spec §4(力/触觉)与 §3(EE-pose)的决策了——
到那一步回来找我,我按答案改 spec,一次改到位。

## 每条回来必做(否则白问)
- 一致 → DIGEST 记一行
- 翻案 → `python3 runtime/reality.py record --escaped` + 改 spec 对应节
- 新问题 → PRECEDENTS 追判例
