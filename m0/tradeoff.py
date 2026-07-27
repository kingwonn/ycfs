#!/usr/bin/env python3
"""tradeoff — 技术路线选型决策矩阵引擎(产品矩阵的计算内核)。

用户要求:每个模态穷举技术路线 → 逐条第一性分析 → 多维对比 → 场景适配 → 产品矩阵。
散文对比会骗人(形容词不可比)。本引擎强制:每条路线在每维度上填**数值分**,
按场景加权求和,输出可排序、可复算、可审计的选型。

数据源:practice/routes/*.json —— 每个模态一个文件,由技术调查填充。
产品目标不同(旗舰/铺量/灵巧手专用),权重不同 → 同一批路线得出不同选型。

设计纪律:
  · 缺数据的维度记 null 并计入 coverage,不拿 0 或满分蒙混(诚实优先于好看的排名)。
  · 权重集中在 PROFILES,可审计;改权重不改数据,防止"调权重凑出想要的赢家"。
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ROUTES_DIR = ROOT / "practice" / "routes"

# 七个评估维度(1-5 分,5 最好)。方向已归一:高分=对本产品越有利。
DIMENSIONS = ["accuracy", "multimodal", "portability", "cost", "manufacturability",
              "sim2real_scarcity", "maturity"]

# 场景/产品档位的权重(和不必为 1,内部归一)。
PROFILES = {
    # 旗舰:计量级力觉数据,精度与稀缺性优先
    "flagship": {"accuracy": 5, "multimodal": 4, "portability": 3, "cost": 2,
                 "manufacturability": 4, "sim2real_scarcity": 5, "maturity": 3},
    # 铺量:低成本可众包,成本与轻便与量产优先
    "volume":   {"accuracy": 2, "multimodal": 2, "portability": 5, "cost": 5,
                 "manufacturability": 5, "sim2real_scarcity": 3, "maturity": 4},
    # 灵巧手专用:多模态与稀缺性优先,成本不敏感
    "dexterous":{"accuracy": 5, "multimodal": 5, "portability": 2, "cost": 1,
                 "manufacturability": 3, "sim2real_scarcity": 5, "maturity": 2},
}


def load_routes(modality):
    f = ROUTES_DIR / f"{modality}.json"
    if not f.exists():
        return None
    return json.loads(f.read_text(encoding="utf-8"))


def score_route(route, weights):
    """加权得分 + 覆盖率。缺项(null)不计入分子分母,单独报 coverage。"""
    num = den = 0.0
    missing = []
    for d in DIMENSIONS:
        v = route["scores"].get(d)
        w = weights[d]
        if v is None:
            missing.append(d)
            continue
        num += v * w
        den += 5 * w                      # 满分基准
    score = round(num / den, 3) if den else None
    coverage = round(1 - len(missing) / len(DIMENSIONS), 2)
    return score, coverage, missing


def rank(modality, profile):
    data = load_routes(modality)
    if data is None:
        return None
    weights = PROFILES[profile]
    rows = []
    for r in data["routes"]:
        s, cov, missing = score_route(r, weights)
        rows.append({"name": r["name"], "score": s, "coverage": cov,
                     "missing": missing, "principle": r.get("principle", "")})
    # 排序:先按覆盖率达标(≥0.7)分组,再按分数;低覆盖率的不许排在前面冒充赢家
    rows.sort(key=lambda x: (x["coverage"] >= 0.7, x["score"] or 0), reverse=True)
    return {"modality": data["modality"], "profile": profile, "rows": rows}


def render(result):
    if result is None:
        return
    print(f"\n{'='*70}\n模态: {result['modality']}   档位: {result['profile']}\n{'='*70}")
    print(f"{'路线':<28}{'得分':>7}{'覆盖':>7}  缺失维度")
    print("-" * 70)
    for r in result["rows"]:
        s = f"{r['score']:.3f}" if r["score"] is not None else "  —  "
        flag = "" if r["coverage"] >= 0.7 else "  ⚠低覆盖"
        miss = ",".join(r["missing"]) if r["missing"] else "-"
        print(f"{r['name'][:27]:<28}{s:>7}{r['coverage']:>7.0%}  {miss}{flag}")


def main():
    mods = [p.stem for p in ROUTES_DIR.glob("*.json")] if ROUTES_DIR.exists() else []
    if not mods:
        print(f"未发现路线数据。技术调查回来后写入 {ROUTES_DIR}/<modality>.json")
        print("schema: {\"modality\":\"触觉\",\"routes\":[{\"name\":..,\"principle\":..,")
        print("         \"scores\":{\"accuracy\":1-5|null, ...7维}, \"source\":\"链接\"}]}")
        return 0
    profiles = sys.argv[1:] or list(PROFILES)
    for m in sorted(mods):
        for p in profiles:
            render(rank(m, p))
    return 0


if __name__ == "__main__":
    sys.exit(main())
