#!/usr/bin/env python3
"""MBTI 256개 조합 페이지 자동 생성 스크립트"""
import os, json, datetime

TYPES = ["INTJ","INTP","ENTJ","ENTP","INFJ","INFP","ENFJ","ENFP",
         "ISTJ","ISFJ","ESTJ","ESFJ","ISTP","ISFP","ESTP","ESFP"]

NAMES = {
    "INTJ":"전략가","INTP":"논리술사","ENTJ":"통솔자","ENTP":"변론가",
    "INFJ":"옹호자","INFP":"중재자","ENFJ":"선도자","ENFP":"활동가",
    "ISTJ":"현실주의자","ISFJ":"수호자","ESTJ":"경영자","ESFJ":"집정관",
    "ISTP":"장인","ISFP":"모험가","ESTP":"사업가","ESFP":"연예인"
}

EMOJI = {
    "INTJ":"🧠","INTP":"🔬","ENTJ":"👑","ENTP":"💡",
    "INFJ":"🌙","INFP":"🦋","ENFJ":"☀️","ENFP":"🌈",
    "ISTJ":"📋","ISFJ":"🛡️","ESTJ":"⚖️","ESFJ":"🤝",
    "ISTP":"🔧","ISFP":"🎨","ESTP":"🏄","ESFP":"🎭"
}

GROUPS = {
    "NT": ["INTJ","INTP","ENTJ","ENTP"],
    "NF": ["INFJ","INFP","ENFJ","ENFP"],
    "SJ": ["ISTJ","ISFJ","ESTJ","ESFJ"],
    "SP": ["ISTP","ISFP","ESTP","ESFP"]
}

TRAITS = {
    "INTJ": {"strength":"전략적 사고와 장기 비전","love":"깊고 의미 있는 지적 교류를 원하며, 파트너의 독립성을 존중합니다","need":"지적 자극과 개인 공간","challenge":"감정 표현이 서툴고 완벽주의 성향"},
    "INTP": {"strength":"논리적 분석력과 창의적 문제 해결","love":"지적 호기심을 공유하는 파트너를 원하며, 자유로운 탐구를 중시합니다","need":"자율성과 지적 대화","challenge":"감정적 교류에 어려움, 일상적 책임 소홀"},
    "ENTJ": {"strength":"리더십과 결단력, 목표 달성 능력","love":"함께 성장하고 목표를 향해 나아갈 파트너를 원합니다","need":"존경과 지적 동등함","challenge":"지나친 통제, 감정보다 효율 우선"},
    "ENTP": {"strength":"창의력과 유머, 토론 능력","love":"지적으로 대등하고 모험을 즐길 파트너를 원합니다","need":"새로운 자극과 자유로운 소통","challenge":"약속 이행 부족, 논쟁을 즐기는 성향"},
    "INFJ": {"strength":"깊은 통찰력과 공감 능력","love":"영혼 깊은 곳까지 이해해주는 진정한 연결을 갈망합니다","need":"깊은 대화와 의미 있는 관계","challenge":"과도한 이상화, 갈등 회피"},
    "INFP": {"strength":"진정성과 창의적 상상력","love":"가치관을 공유하고 내면의 세계를 존중해주는 파트너를 원합니다","need":"감정적 진정성과 개인 공간","challenge":"비현실적 기대, 결정 어려움"},
    "ENFJ": {"strength":"따뜻한 리더십과 타인에 대한 헌신","love":"깊은 감정적 유대와 함께 성장하는 관계를 추구합니다","need":"감사와 인정, 깊은 교류","challenge":"과도한 헌신, 자기 희생"},
    "ENFP": {"strength":"열정과 긍정 에너지, 공감 능력","love":"자유롭고 깊은 감정적 연결을 원하며, 모험을 함께할 파트너를 찾습니다","need":"자유와 감정적 교류","challenge":"일관성 부족, 깊이보다 넓이 추구"},
    "ISTJ": {"strength":"책임감과 신뢰성, 체계적 사고","love":"안정적이고 헌신적인 관계를 중시하며, 약속을 지키는 파트너를 원합니다","need":"안정감과 명확한 기대","challenge":"변화에 대한 저항, 감정 표현 부족"},
    "ISFJ": {"strength":"헌신적 배려와 세심한 관찰력","love":"따뜻하고 안정적인 관계를 만들며, 파트너를 세심하게 챙깁니다","need":"감사와 안정감","challenge":"자기 희생, 갈등 회피"},
    "ESTJ": {"strength":"조직력과 책임감, 현실적 판단","love":"명확한 역할과 안정적인 동반자 관계를 선호합니다","need":"존경과 질서","challenge":"융통성 부족, 감정보다 규칙 우선"},
    "ESFJ": {"strength":"사교성과 배려, 조화 추구","love":"따뜻한 교류와 사회적 연결을 중시하는 관계를 만듭니다","need":"소속감과 감사","challenge":"과도한 타인 의식, 갈등 회피"},
    "ISTP": {"strength":"실용적 문제 해결과 적응력","love":"자유롭고 압박 없는 관계를 선호하며, 행동으로 사랑을 표현합니다","need":"자유와 실용적 교류","challenge":"감정 표현 어려움, 장기 계획 부족"},
    "ISFP": {"strength":"예술적 감성과 진정성","love":"조용하지만 깊은 감정적 연결을 추구하며, 현재의 순간을 소중히 합니다","need":"자유와 감정적 수용","challenge":"갈등 회피, 미래 계획 부족"},
    "ESTP": {"strength":"행동력과 현실 감각, 위기 대처","love":"활동적이고 즐거운 관계를 추구하며, 지금 이 순간을 즐깁니다","need":"자유와 모험","challenge":"장기적 헌신 어려움, 감정적 깊이 부족"},
    "ESFP": {"strength":"사교성과 긍정 에너지, 즐거움","love":"재미있고 따뜻한 관계를 만들며, 함께하는 경험을 중시합니다","need":"자유와 사회적 교류","challenge":"진지한 대화 회피, 장기 계획 부족"}
}

def same_group(a, b):
    for g in GROUPS.values():
        if a in g and b in g:
            return True
    return False

def shared_functions(a, b):
    count = 0
    for i in range(4):
        if a[i] == b[i]:
            count += 1
    return count

def get_compatibility(a, b):
    s = shared_functions(a, b)
    sg = same_group(a, b)

    # 황금 궁합 (반대 내향/외향 + 유사 기능)
    golden = [
        ("INTJ","ENFP"),("INFJ","ENTP"),("INTP","ENTJ"),("INFP","ENFJ"),
        ("ISTJ","ESFP"),("ISFJ","ESTP"),("ISTP","ESTJ"),("ISFP","ESFJ"),
        ("ENTJ","INFP"),("ENFJ","ISTP"),("ENTP","ISFJ"),("ENFP","ISTJ"),
        ("ESTJ","ISFP"),("ESFJ","INTP"),("ESTP","INFJ"),("ESFP","INTJ")
    ]
    if (a,b) in golden or (b,a) in golden:
        return {"score":95,"level":"천생연분","emoji":"💕","color":"#ec4899"}

    # 같은 유형
    if a == b:
        return {"score":75,"level":"거울 궁합","emoji":"🪞","color":"#8b5cf6"}

    # 같은 그룹
    if sg:
        return {"score":80,"level":"동류 궁합","emoji":"🤝","color":"#6366f1"}

    # E/I만 다른 경우
    if s == 3:
        return {"score":85,"level":"보완 궁합","emoji":"✨","color":"#a855f7"}

    # 2개 공유
    if s == 2:
        return {"score":70,"level":"성장 궁합","emoji":"🌱","color":"#10b981"}

    # 1개 공유
    if s == 1:
        return {"score":55,"level":"도전 궁합","emoji":"🔥","color":"#f59e0b"}

    # 0개 공유 (완전 반대)
    return {"score":45,"level":"모험 궁합","emoji":"🗺️","color":"#ef4444"}

def generate_strengths(a, b, compat):
    parts = []
    sa, sb = shared_functions(a, b), 0
    level = compat["level"]

    if level == "천생연분":
        parts.append(f"{NAMES[a]}의 {TRAITS[a]['strength']}과(와) {NAMES[b]}의 {TRAITS[b]['strength']}이(가) 완벽하게 맞물립니다.")
        parts.append("서로의 약점을 자연스럽게 보완하며, 함께 있을 때 시너지가 극대화됩니다.")
        parts.append("대화가 끊이지 않고, 서로에게서 끝없이 배울 점을 발견합니다.")
    elif level == "거울 궁합":
        parts.append(f"같은 {NAMES[a]} 유형으로, 서로를 깊이 이해하는 데 유리합니다.")
        parts.append("비슷한 가치관과 소통 방식 덕분에 오해가 적습니다.")
        parts.append("다만 같은 약점을 공유하므로 의식적인 보완이 필요합니다.")
    elif level == "동류 궁합":
        parts.append(f"같은 기질 그룹에 속해 근본적인 가치관과 세계관을 공유합니다.")
        parts.append(f"{NAMES[a]}의 {TRAITS[a]['strength']}과(와) {NAMES[b]}의 {TRAITS[b]['strength']}이(가) 서로 공명합니다.")
        parts.append("자연스러운 이해 속에서도 적당한 차이가 관계에 활력을 줍니다.")
    elif level == "보완 궁합":
        parts.append(f"에너지 방향만 다를 뿐 핵심 가치관이 유사해서, 깊은 이해를 바탕으로 서로를 보완합니다.")
        parts.append(f"{NAMES[a]}이(가) 가져오는 관점과 {NAMES[b]}이(가) 가져오는 관점이 균형을 이룹니다.")
    elif level == "성장 궁합":
        parts.append(f"적당한 공통점과 차이점이 공존해서, 서로에게서 새로운 시각을 배울 수 있습니다.")
        parts.append(f"{NAMES[a]}의 {TRAITS[a]['strength']}은(는) {NAMES[b]}에게 새로운 영감을 줍니다.")
    elif level == "도전 궁합":
        parts.append(f"상당히 다른 성향이지만, 그만큼 서로에게서 배울 것이 많습니다.")
        parts.append(f"{NAMES[a]}은(는) {TRAITS[a]['strength']}을(를), {NAMES[b]}은(는) {TRAITS[b]['strength']}을(를) 관계에 가져옵니다.")
    else:
        parts.append(f"매우 다른 두 유형이 만나 예상치 못한 성장을 경험할 수 있습니다.")
        parts.append(f"서로의 완전히 다른 강점이 오히려 팀으로서 최강의 조합을 만들 수 있습니다.")

    return parts

def generate_tips(a, b, compat):
    tips = []
    # E/I 차이
    if a[0] != b[0]:
        tips.append("외향형은 내향형 파트너에게 충분한 혼자만의 시간을 보장해주세요. 내향형은 가끔 외향형의 사교 활동에 함께 참여하는 노력을 보여주세요.")
    # S/N 차이
    if a[1] != b[1]:
        tips.append("감각형(S)은 구체적 사실로, 직관형(N)은 큰 그림으로 소통합니다. 상대방의 소통 방식에 맞춰 이야기하는 연습이 필요합니다.")
    # T/F 차이
    if a[2] != b[2]:
        tips.append("사고형(T)은 문제 해결 전에 먼저 공감을 표현해주세요. 감정형(F)은 논리적 피드백이 비판이 아닌 도움의 표현임을 이해해주세요.")
    # J/P 차이
    if a[3] != b[3]:
        tips.append("판단형(J)은 유연함을 배우고, 인식형(P)은 계획의 가치를 인정해주세요. 중요한 일은 미리 계획하되, 여유 시간은 자유롭게 두는 균형이 좋습니다.")

    if not tips:
        tips.append("같은 선호를 공유하므로 자연스러운 조화가 장점이지만, 비슷한 맹점도 공유합니다. 의식적으로 다른 관점을 탐색하는 노력이 관계를 더 풍요롭게 만듭니다.")

    tips.append(f"{NAMES[a]}은(는) {TRAITS[a]['need']}을(를) 필요로 하고, {NAMES[b]}은(는) {TRAITS[b]['need']}을(를) 필요로 합니다. 서로의 핵심 욕구를 기억하세요.")
    return tips

def generate_challenges(a, b):
    parts = []
    if a[0] != b[0]:
        parts.append("에너지 충전 방식의 차이 — 혼자 있고 싶은 때와 함께하고 싶은 때가 어긋날 수 있습니다")
    if a[1] != b[1]:
        parts.append("정보 처리 방식의 차이 — 세부 사항 vs 큰 그림으로 의견 충돌이 생길 수 있습니다")
    if a[2] != b[2]:
        parts.append("의사결정 방식의 차이 — 논리 vs 감정으로 같은 상황을 다르게 판단할 수 있습니다")
    if a[3] != b[3]:
        parts.append("생활 방식의 차이 — 계획적 vs 자유로운 스타일로 일상에서 마찰이 생길 수 있습니다")
    if not parts:
        parts.append("같은 유형이라 맹점을 공유합니다 — " + TRAITS[a]["challenge"])
    return parts

def make_page(a, b):
    c = get_compatibility(a, b)
    strengths = generate_strengths(a, b, c)
    tips = generate_tips(a, b, c)
    challenges = generate_challenges(a, b)

    na, nb = NAMES[a], NAMES[b]
    ea, eb = EMOJI[a], EMOJI[b]
    title = f"{a}({na})와 {b}({nb}) 궁합 — {c['level']} {c['emoji']}"
    desc = f"{a} {na}와 {b} {nb}의 MBTI 궁합을 분석합니다. 궁합 점수 {c['score']}%, {c['level']}. 두 유형의 강점, 약점, 연애 팁을 확인하세요."
    fname = f"mbti-{a.lower()}-{b.lower()}.html"
    url = f"https://matchtest.site/{fname}"

    strengths_html = "\n".join(f"        <li>{s}</li>" for s in strengths)
    tips_html = "\n".join(f"        <li>{t}</li>" for t in tips)
    challenges_html = "\n".join(f"        <li>{ch}</li>" for ch in challenges)

    # 관련 조합 링크 (같은 유형의 다른 조합 4개)
    related = []
    for t in TYPES:
        if t != b and t != a and len(related) < 4:
            rc = get_compatibility(a, t)
            related.append((a, t, rc))
    related_html = "\n".join(
        f'        <li><a href="mbti-{r[0].lower()}-{r[1].lower()}.html">{r[0]}와 {r[1]} ({r[2]["level"]})</a></li>'
        for r in related
    )

    score_bar_color = c["color"]

    html = f'''<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | 이름궁합 테스트</title>
    <meta name="description" content="{desc}">
    <meta name="keywords" content="{a} {b} 궁합, {a} {b}, MBTI 궁합, {na} {nb} 궁합, {a} 연애, {b} 연애, MBTI 커플">
    <link rel="canonical" href="{url}">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{desc}">
    <meta property="og:url" content="{url}">
    <meta property="og:type" content="article">
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6668425393052932" crossorigin="anonymous"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Fredoka:wght@400;600;700&family=Noto+Sans+KR:wght@400;700&family=Noto+Sans:wght@400;700&display=swap" rel="stylesheet">
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-VE4TW465YN"></script>
    <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','G-VE4TW465YN');</script>
    <style>
        *{{margin:0;padding:0;box-sizing:border-box}}
        :root{{--pink-50:#fdf2f8;--pink-100:#fce7f3;--pink-200:#fbcfe8;--pink-500:#ec4899;--pink-600:#db2777;--purple-500:#a855f7;--gray-400:#9ca3af;--gray-500:#6b7280;--gray-600:#4b5563;--gray-700:#374151}}
        body{{font-family:'Noto Sans KR','Noto Sans',sans-serif;min-height:100vh;display:flex;flex-direction:column;background:linear-gradient(160deg,#fdf2f8,#fce7f3,#fbcfe8);color:var(--gray-700);line-height:1.7}}
        a{{color:var(--pink-500);text-decoration:none}}a:hover{{text-decoration:underline}}
        .nav{{background:rgba(255,255,255,.85);backdrop-filter:blur(10px);border-bottom:1px solid var(--pink-100);padding:10px 20px;display:flex;justify-content:center;gap:16px;flex-wrap:wrap}}
        .nav a{{font-size:13px;font-weight:600;color:var(--gray-500);padding:4px 10px;border-radius:8px;transition:all .2s}}
        .nav a:hover,.nav a.active{{background:var(--pink-500);color:white;text-decoration:none}}
        main{{flex:1;display:flex;justify-content:center;padding:32px 16px}}
        .page{{background:rgba(255,255,255,.9);backdrop-filter:blur(8px);width:760px;max-width:100%;border-radius:20px;padding:36px 32px;box-shadow:0 4px 20px rgba(0,0,0,.04)}}
        h1{{font-family:'Fredoka',sans-serif;font-size:26px;color:var(--pink-600);margin-bottom:8px}}
        h2{{font-size:18px;color:var(--purple-500);margin:24px 0 8px}}
        h3{{font-size:16px;color:var(--gray-700);margin:16px 0 6px}}
        p{{font-size:14px;color:var(--gray-600);margin-bottom:14px}}
        ul{{margin:8px 0 14px 20px;font-size:14px;color:var(--gray-600)}}li{{margin-bottom:6px}}
        .breadcrumb{{font-size:12px;color:var(--gray-400);margin-bottom:16px}}
        .breadcrumb a{{color:var(--gray-500)}}
        .score-box{{text-align:center;padding:24px;margin:16px 0;background:linear-gradient(135deg,#fdf2f8,#fce7f3);border-radius:16px}}
        .score-big{{font-family:'Fredoka',sans-serif;font-size:48px;color:{score_bar_color};font-weight:700}}
        .score-label{{font-size:18px;color:var(--gray-600);margin-top:4px;font-weight:600}}
        .bar-wrap{{background:#f3f4f6;border-radius:50px;height:12px;margin:12px auto;max-width:300px;overflow:hidden}}
        .bar-fill{{height:100%;border-radius:50px;background:{score_bar_color};width:{c["score"]}%}}
        .type-row{{display:flex;gap:16px;margin:16px 0;flex-wrap:wrap}}
        .type-card{{flex:1;min-width:200px;padding:16px;background:white;border-radius:12px;box-shadow:0 2px 8px rgba(0,0,0,.04)}}
        .type-card h3{{margin-top:0;color:var(--purple-500)}}
        .cta{{display:inline-block;margin-top:20px;padding:10px 24px;background:linear-gradient(135deg,var(--pink-500),var(--purple-500));color:white;border-radius:50px;font-weight:700;font-size:14px;text-decoration:none}}
        .cta:hover{{text-decoration:none;opacity:.9}}
        .related{{background:#f9fafb;border-radius:12px;padding:16px;margin-top:20px}}
        .related h3{{color:var(--gray-700);margin-top:0}}
        footer{{background:rgba(255,255,255,.7);border-top:1px solid var(--pink-100);padding:16px;text-align:center;font-size:12px;color:var(--gray-400)}}
        footer a{{color:var(--gray-500);margin:0 8px}}
    </style>
</head>
<body>
<nav class="nav">
    <a href="index.html">홈</a>
    <a href="mbti-test.html">MBTI 테스트</a>
    <a href="mbti.html">MBTI 궁합</a>
    <a href="mbti-compatibility-guide.html">궁합 가이드</a>
    <a href="about.html">소개</a>
</nav>
<main>
<article class="page">
    <div class="breadcrumb"><a href="index.html">홈</a> &rsaquo; <a href="mbti.html">MBTI 궁합</a> &rsaquo; {a} &times; {b}</div>
    <h1>{ea} {a}({na}) &times; {eb} {b}({nb})</h1>

    <div class="score-box">
        <div class="score-big">{c["score"]}%</div>
        <div class="score-label">{c["emoji"]} {c["level"]}</div>
        <div class="bar-wrap"><div class="bar-fill"></div></div>
    </div>

    <div class="type-row">
        <div class="type-card">
            <h3>{ea} {a} — {na}</h3>
            <p>{TRAITS[a]["love"]}</p>
        </div>
        <div class="type-card">
            <h3>{eb} {b} — {nb}</h3>
            <p>{TRAITS[b]["love"]}</p>
        </div>
    </div>

    <h2>💪 이 조합의 강점</h2>
    <ul>
{strengths_html}
    </ul>

    <h2>⚡ 주의할 점</h2>
    <ul>
{challenges_html}
    </ul>

    <h2>💡 연애 팁</h2>
    <ul>
{tips_html}
    </ul>

    <h2>📊 요약</h2>
    <p>{a} {na}은(는) {TRAITS[a]["need"]}을(를) 중시하고, {b} {nb}은(는) {TRAITS[b]["need"]}을(를) 중시합니다. 이 두 유형이 서로의 핵심 욕구를 이해하고 존중할 때, {c["level"]}에서 한 단계 더 깊은 관계로 발전할 수 있습니다.</p>

    <div style="text-align:center;margin:20px 0">
        <a href="mbti.html" class="cta">MBTI 궁합 테스트 해보기</a>
        <a href="mbti-test.html" class="cta" style="margin-left:8px;background:linear-gradient(135deg,#8b5cf6,#6366f1)">내 MBTI 알아보기</a>
    </div>

    <div class="related">
        <h3>📎 {a}의 다른 궁합 보기</h3>
        <ul>
{related_html}
        </ul>
    </div>
</article>
</main>
<footer>
    <div><a href="about.html">소개</a><a href="contact.html">문의</a><a href="privacy.html">개인정보처리방침</a><a href="terms.html">이용약관</a></div>
    <div style="margin-top:8px">&copy; 2026 Love Match Test. All rights reserved.</div>
</footer>
</body>
</html>'''
    return fname, html

def generate_sitemap_entries():
    today = datetime.date.today().isoformat()
    entries = []
    for a in TYPES:
        for b in TYPES:
            fname = f"mbti-{a.lower()}-{b.lower()}.html"
            entries.append(f"""  <url>
    <loc>https://matchtest.site/{fname}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.6</priority>
  </url>""")
    return "\n".join(entries)

if __name__ == "__main__":
    outdir = os.path.dirname(os.path.abspath(__file__))
    count = 0
    for a in TYPES:
        for b in TYPES:
            fname, html = make_page(a, b)
            path = os.path.join(outdir, fname)
            with open(path, "w", encoding="utf-8") as f:
                f.write(html)
            count += 1
    print(f"Generated {count} MBTI combination pages")

    # sitemap entries 출력
    sitemap_path = os.path.join(outdir, "sitemap_mbti_entries.txt")
    with open(sitemap_path, "w", encoding="utf-8") as f:
        f.write(generate_sitemap_entries())
    print(f"Sitemap entries saved to {sitemap_path}")
