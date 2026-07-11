"""provenance.verify — L1 出口零编造:引用解析核验(D1)。

铁律:核验的不是「有没有引用」,而是「引用是否解析得到该值」——
LLM 会 RAG 出错值再编一个像真的页码;「检查有引用」放行,「解析被引页并确认
数值字面出现」才拦得住(correctness ≠ faithfulness)。

中英等强:归一化用 Unicode NFKC(全角→半角)+ 去千分位 + 去空白 + 小写,
匹配层对语言无感——拦截率的语言对称性由 property 测试证明。

硬阻断语义:无出处 / 页码不解析 / 值未见于被引页 → HardBlock,绝不放行
一个「看起来对」的值。
"""
import re
import unicodedata
from dataclasses import dataclass


@dataclass
class Claim:
    value: str        # 对外声称的值(含单位可选),如 "50 kHz" / "512" / "310 V"
    doc: str          # 文档标识
    page: int | None  # 1-based 页码
    label: str = ""   # 该值的名称(报错用)


@dataclass
class Verdict:
    ok: bool
    reason: str = ""


def normalize(text: str) -> str:
    """NFKC(全角数字/字母/标点→半角)+ 去千分位逗号 + 去全部空白 + 小写。"""
    t = unicodedata.normalize("NFKC", text)
    t = re.sub(r"(?<=\d),(?=\d{3})", "", t)   # 1,000 → 1000
    t = re.sub(r"\s+", "", t)                  # 单位间距/换行/CJK 无空格差异
    return t.lower()


def verify_claim(claim: Claim, get_page_text) -> Verdict:
    """get_page_text(page:int) -> str|None。返回 Verdict;不 ok 即硬阻断。"""
    if not claim.doc or not claim.doc.strip():
        return Verdict(False, f"[{claim.label}] 无出处(doc 为空)——硬阻断")
    if claim.page is None:
        return Verdict(False, f"[{claim.label}] 无页码——硬阻断")
    page_text = get_page_text(claim.page)
    if page_text is None:
        return Verdict(False, f"[{claim.label}] 页码 {claim.page} 不解析(文档无此页)——硬阻断")
    if not claim.value or not claim.value.strip():
        return Verdict(False, f"[{claim.label}] 声称值为空——硬阻断")
    if normalize(claim.value) not in normalize(page_text):
        return Verdict(False,
                       f"[{claim.label}] 值『{claim.value}』未见于 {claim.doc} 第 {claim.page} 页——硬阻断(疑似编造)")
    return Verdict(True)


def verify_batch(claims, get_page_text):
    """返回 (通过数, 阻断列表[(claim, reason)])。任何阻断都必须被调用方处理,不许静默。"""
    blocked = []
    ok = 0
    for c in claims:
        v = verify_claim(c, get_page_text)
        if v.ok:
            ok += 1
        else:
            blocked.append((c, v.reason))
    return ok, blocked


class PdfSource:
    """生产后端:pdfplumber 确定性抽取(本地解析,NDA 文档不出域)。"""

    def __init__(self, path):
        import pdfplumber
        self._pdf = pdfplumber.open(path)

    def get_page_text(self, page: int):
        if page < 1 or page > len(self._pdf.pages):
            return None
        return self._pdf.pages[page - 1].extract_text() or ""

    def close(self):
        self._pdf.close()
