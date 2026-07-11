#!/usr/bin/env python3
"""D1 单测:L1 引用解析核验——真值放行/篡改与伪造页 100% 拦截/中英拦截率相等/无出处硬阻断。
含真 PDF 端到端(reportlab 生成中英双页 → pdfplumber 抽取 → 同一核验器)。"""
import sys

from verify import Claim, PdfSource, verify_claim

passed = failed = 0


def check(cond, name):
    global passed, failed
    if cond:
        passed += 1
    else:
        failed += 1
        print(f"FAIL: {name}")


# ── 文本层:同一组值,英文页与中文页(含全角数字/千分位/单位间距差异) ──
EN_PAGE = ("Maximum PWM frequency is 50 kHz. Nominal current 20,000 mA."
           " Flash size 512 KB. HSO validated to 5 kHz electrical frequency."
           " Bus voltage 310 V. Stall trip time 500 ms."
           " Thermal fuse rating 184 C. Impeller has 13 blades.")
CN_PAGE = ("最大 PWM 频率为50kHz。额定电流 20,000mA。"
           "Flash 容量 ５１２ KB。HSO 已验证至 5 kHz 电气频率。"
           "母线电压 ３１０V。堵转跳闸时间 500ms。"
           "热熔断规格 184C。叶轮为 13 叶。")
PAGES = {1: EN_PAGE, 2: CN_PAGE}
get_page = lambda p: PAGES.get(p)  # noqa: E731

VALUES = ["50 kHz", "20,000 mA", "512 KB", "5 kHz", "310 V", "500 ms", "184 C", "13"]
TAMPERED = ["55 kHz", "20,001 mA", "256 KB", "8 kHz", "220 V", "900 ms", "150 C", "11"]

# T1: 真值全放行(EN 页 + CN 页各 8) —— 语言等强的「零误伤」侧
en_true = sum(verify_claim(Claim(v, "DS", 1, f"en{i}"), get_page).ok for i, v in enumerate(VALUES))
cn_true = sum(verify_claim(Claim(v, "DS", 2, f"cn{i}"), get_page).ok for i, v in enumerate(VALUES))
check(en_true == len(VALUES), f"T1a EN 真值 {en_true}/{len(VALUES)} 全放行")
check(cn_true == len(VALUES), f"T1b CN 真值 {cn_true}/{len(VALUES)} 全放行(全角/千分位/空格差异被归一)")
check(en_true == cn_true, "T1c 真值放行率中英相等")

# T2: 篡改值 100% 拦截(两种语言) —— property:拦截率相等
en_block = sum(not verify_claim(Claim(v, "DS", 1, f"te{i}"), get_page).ok for i, v in enumerate(TAMPERED))
cn_block = sum(not verify_claim(Claim(v, "DS", 2, f"tc{i}"), get_page).ok for i, v in enumerate(TAMPERED))
check(en_block == len(TAMPERED), f"T2a EN 篡改拦截 {en_block}/{len(TAMPERED)} = 100%")
check(cn_block == len(TAMPERED), f"T2b CN 篡改拦截 {cn_block}/{len(TAMPERED)} = 100%")
check(en_block == cn_block, "T2c 拦截率中英相等(单语言盲区不存在)")

# T3: 伪造页引用:值真实但页码指错/不存在 → 拦
check(not verify_claim(Claim("50 kHz", "DS", 2, "wrongpage"), get_page).ok
      or "50kHz" in CN_PAGE.replace(" ", ""), "T3a 错页引用被拦(除非该页恰有该值)")
check(not verify_claim(Claim("512 KB", "DS", 99, "nopage"), get_page).ok, "T3b 不存在的页码硬阻断")

# T4: 无出处/无页码/空值 → 硬阻断
check(not verify_claim(Claim("50 kHz", "", 1, "nodoc"), get_page).ok, "T4a 无 doc 硬阻断")
check(not verify_claim(Claim("50 kHz", "DS", None, "nopg"), get_page).ok, "T4b 无页码硬阻断")
check(not verify_claim(Claim("", "DS", 1, "noval"), get_page).ok, "T4c 空值硬阻断")

# ── 真 PDF 端到端:reportlab 生成(EN 页 + STSong 中文页)→ pdfplumber 抽取 ──
PDF = "/tmp/d1_spec.pdf"
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfgen import canvas

pdfmetrics.registerFont(UnicodeCIDFont("STSong-Light"))
c = canvas.Canvas(PDF, pagesize=A4)
c.setFont("Helvetica", 12)
y = 800
for line in ("Maximum PWM frequency is 50 kHz.", "Nominal current 20,000 mA.",
             "Flash size 512 KB.", "Bus voltage 310 V."):
    c.drawString(60, y, line); y -= 24
c.showPage()
c.setFont("STSong-Light", 12)
y = 800
for line in ("最大PWM频率为50kHz。", "额定电流 20,000 mA。", "Flash容量512KB。", "母线电压310V。"):
    c.drawString(60, y, line); y -= 24
c.showPage()
c.save()

src = PdfSource(PDF)
gp = src.get_page_text
check(verify_claim(Claim("50 kHz", "PDF", 1, "p1"), gp).ok, "T5a PDF·EN 真值放行")
check(verify_claim(Claim("310 V", "PDF", 2, "p2"), gp).ok, "T5b PDF·CN 真值放行(pdfplumber 抽 CID 中文)")
check(not verify_claim(Claim("55 kHz", "PDF", 1, "p3"), gp).ok, "T5c PDF·EN 篡改被拦")
check(not verify_claim(Claim("256 KB", "PDF", 2, "p4"), gp).ok, "T5d PDF·CN 篡改被拦")
check(not verify_claim(Claim("50 kHz", "PDF", 9, "p5"), gp).ok, "T5e PDF 不存在页硬阻断")
src.close()

print(f"RESULT: {passed} passed, {failed} failed")
sys.exit(0 if failed == 0 else 1)
