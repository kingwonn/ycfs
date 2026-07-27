#!/usr/bin/env python3
"""ablation — 力消融实验框架(M2 最致命验证的骨架)。

回答产品的头号技术风险:力/触觉数据是否提升 contact-rich 策略?能否跨本体迁移?

方法:同一批 (观察, 动作) 数据,训两个策略——
  · vis:  只用视觉+位姿特征
  · vis+force: 额外加力/触觉特征
比较成功率。若 vis+force 显著高于 vis,力有用;否则力是噪声。
跨本体:在本体 A 的数据上训,在本体 B 上测,看力优势是否还在。

诚实边界(写在代码里):
  · 本文件用【合成 contact-rich 任务】先跑通框架逻辑,证明它能区分"力有用/无用"两种世界。
    真实结论必须换成公开真机数据集(见 m2/README,等数据可得性调查确认)。
  · 这里用轻量分类器(sklearn)代替真 VLA——它验证的是"力通道是否携带任务相关信息",
    不是"VLA 能否利用它"。前者是后者的必要不充分条件:力若连轻模型都提升不了,
    重模型多半也不行(便宜的证伪);力若提升了,仍需真 VLA 复核(不充分)。

用法:
  python3 m2/ablation.py                 合成数据自证框架
  python3 m2/ablation.py --world null     力无用的世界(对照:force 不应提升)
"""
import sys

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score

RNG = np.random.default_rng(11)


def make_task(n=1200, world="contact", embodiment=0):
    """合成 contact-rich 任务。

    world="contact": 成功与否真正依赖接触力(力携带信息)——force 应提升
    world="null":    成功只依赖视觉,力是纯噪声——force 不应提升(对照)
    embodiment:      不同本体:动作/视觉分布平移 + 力的标定尺度不同(模拟跨本体 gap)
    """
    shift = embodiment * 0.6
    vis = RNG.normal(shift, 1.0, size=(n, 6))          # 视觉+位姿特征
    pose = RNG.normal(shift, 1.0, size=(n, 3))
    # 力特征:本体不同→标定尺度不同(force gap 的来源)
    scale = 1.0 + 0.5 * embodiment
    latent_contact = RNG.normal(0, 1.0, size=n)        # 真实接触强度(隐变量)
    force = np.stack([latent_contact * scale + RNG.normal(0, 0.2, size=n),
                      latent_contact * 0.7 * scale + RNG.normal(0, 0.2, size=n),
                      RNG.normal(0, 1.0, size=n)], axis=1)
    # 成功标签
    vis_signal = vis[:, 0] - 0.5 * vis[:, 1]
    if world == "contact":
        logit = 0.8 * vis_signal + 1.3 * latent_contact    # 力真正决定成败
    else:
        logit = 1.5 * vis_signal + 0.0 * latent_contact    # 力无关
    prob = 1 / (1 + np.exp(-logit))
    success = (RNG.random(n) < prob).astype(int)
    return {"vis": np.hstack([vis, pose]), "force": force, "y": success}


def evaluate(feat, y, k=5):
    clf = RandomForestClassifier(n_estimators=120, max_depth=8, random_state=0)
    return cross_val_score(clf, feat, y, cv=k, scoring="accuracy")


def run_within(world):
    d = make_task(world=world, embodiment=0)
    vis_only = evaluate(d["vis"], d["y"])
    vis_force = evaluate(np.hstack([d["vis"], d["force"]]), d["y"])
    return vis_only, vis_force


def run_cross(world):
    """本体 0 训 → 本体 1 测,看力优势是否跨本体保留。"""
    tr = make_task(world=world, embodiment=0)
    te = make_task(world=world, embodiment=1)

    def fit_test(cols_tr, cols_te):
        clf = RandomForestClassifier(n_estimators=120, max_depth=8, random_state=0)
        clf.fit(cols_tr, tr["y"])
        return clf.score(cols_te, te["y"])
    vis_only = fit_test(tr["vis"], te["vis"])
    vis_force = fit_test(np.hstack([tr["vis"], tr["force"]]),
                         np.hstack([te["vis"], te["force"]]))
    return vis_only, vis_force


def main():
    world = "null" if "--world" in sys.argv and "null" in sys.argv else "contact"
    print("=" * 62)
    print(f"力消融实验(合成骨架)  世界={world}"
          + ("(力携带信息)" if world == "contact" else "(力=噪声,对照)"))
    print("=" * 62)

    vo, vf = run_within(world)
    d_in = vf.mean() - vo.mean()
    print(f"[同本体] 仅视觉        成功率 {vo.mean():.3f} ± {vo.std():.3f}")
    print(f"[同本体] 视觉+力       成功率 {vf.mean():.3f} ± {vf.std():.3f}")
    print(f"         力的增益 Δ = {d_in:+.3f}")

    cvo, cvf = run_cross(world)
    d_cross = cvf - cvo
    print(f"[跨本体] 仅视觉(A训B测)成功率 {cvo:.3f}")
    print(f"[跨本体] 视觉+力(A训B测)成功率 {cvf:.3f}")
    print(f"         力的跨本体增益 Δ = {d_cross:+.3f}")
    print("-" * 62)
    if world == "contact":
        print(f"预期:力应提升(Δ>0)。同本体 {'✓' if d_in > 0.02 else '✗'}  "
              f"跨本体 {'✓保留' if d_cross > 0.0 else '✗被gap吃掉'}")
    else:
        print(f"预期:力不应提升(Δ≈0)。同本体 {'✓' if abs(d_in) < 0.03 else '✗误报'}")
    print("=" * 62)
    print("注:这是合成骨架,证明框架能区分'力有用/无用'。真结论需接公开真机数据(见 m2/README)。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
