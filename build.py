"""Build the complete static blog. Python 3, standard library only."""
from pathlib import Path
from html import escape as esc
import json, re
from datetime import datetime
from email.utils import format_datetime

ROOT = Path(__file__).resolve().parent
S = json.loads((ROOT / 'site.json').read_text(encoding='utf-8'))
DESC = esc(S['description'])
URL = S['url'].rstrip('/')

def inline(text):
    text = esc(text)
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'`(.+?)`', r'<code>\1</code>', text)
    return text

def markdown(text):
    out, para, in_list = [], [], False
    def flush():
        if para:
            out.append('<p>' + inline(' '.join(para)) + '</p>'); para.clear()
    for line in text.splitlines() + ['']:
        if not line.strip():
            flush()
            if in_list: out.append('</ul>'); in_list = False
        elif line.startswith('#'):
            flush(); m = re.match(r'^(#{1,6})\s+(.+)$', line)
            if m: out.append(f'<h{len(m[1])}>{inline(m[2])}</h{len(m[1])}>')
            else: para.append(line)
        elif re.fullmatch(r'!\[.*?\]\(.+?\)', line):
            flush(); m = re.fullmatch(r'!\[(.*?)\]\((.+?)\)', line)
            out.append(f'<figure><img src="{esc(m[2], quote=True)}" alt="{esc(m[1], quote=True)}" loading="lazy"><figcaption>{esc(m[1])}</figcaption></figure>')
        elif line.startswith('- '):
            flush()
            if not in_list: out.append('<ul>'); in_list = True
            out.append('<li>' + inline(line[2:]) + '</li>')
        else: para.append(line)
    return '\n'.join(out)

def page(title, content, active='', depth=0, description=None):
    prefix = '../' * depth
    links = [('首页', 'index.html', 'home'), ('文章', 'writing.html', 'writing'), ('项目', 'projects.html', 'projects'), ('关于', 'about.html', 'about')]
    nav = ''.join(f'<a href="{prefix}{path}"'+(' aria-current="page"' if key == active else '')+f'>{label}</a>' for label, path, key in links)
    return f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} · {esc(S['name'])}</title><meta name="description" content="{esc(description or S['description'], quote=True)}">
<meta name="theme-color" content="#f6f5f1"><meta property="og:title" content="{esc(title, quote=True)}"><meta property="og:description" content="{esc(description or S['description'], quote=True)}"><meta property="og:type" content="website">
<link rel="icon" href="{prefix}assets/favicon.svg" type="image/svg+xml"><link rel="alternate" type="application/rss+xml" title="{esc(S['title'])}" href="{prefix}feed.xml"><link rel="stylesheet" href="{prefix}assets/style.css"><script src="{prefix}assets/app.js" defer></script></head>
<body><a class="skip" href="#main">跳到正文</a><header class="site-header wrap"><a class="brand" href="{prefix}index.html" aria-label="张斌诚的个人博客首页"><span class="monogram">BC.</span><span>张斌诚<span class="brand-sub">BINCHENG ZHANG</span></span></a><nav aria-label="主导航">{nav}</nav><a class="github" href="https://github.com/{esc(S['github'])}" target="_blank" rel="noopener noreferrer">GitHub ↗</a></header>
<main id="main" class="wrap">{content}</main><footer class="wrap footer"><div><strong>张斌诚</strong><p>{DESC}</p></div><div class="footer-links"><a href="{prefix}feed.xml">RSS 订阅 ↗</a><a href="https://github.com/{esc(S['github'])}" target="_blank" rel="noopener noreferrer">GitHub ↗</a><span>© 2026 · 持续学习，认真记录</span></div></footer></body></html>'''

def post_rows(posts):
    return ''.join(f'''<a class="post-row" href="posts/{p['slug']}.html" data-search="{esc(p['title']+' '+p['category']+' '+p['summary'], quote=True)}"><span class="post-date">{p['date'].replace('-', '.')}<span>{esc(p['category'])}</span></span><div><h3>{esc(p['title'])}</h3><p>{esc(p['summary'])}</p></div><span class="row-arrow" aria-hidden="true">↗</span></a>''' for p in posts)

def save(path, text):
    dest = ROOT / path; dest.parent.mkdir(exist_ok=True, parents=True); dest.write_text(text, encoding='utf-8')

home = f'''<section class="hero"><div><p class="eyebrow">HELLO, WORLD / 你好，世界</p><h1>我是张斌诚。<br>在探索中，<br><span>把想法变成实物。</span></h1><p class="hero-desc">{DESC}</p><p class="hero-intro">西安电子科技大学 · 光电信息科学与工程教改班<br>记录嵌入式开发、智能无人系统与光电科研中的学习和实践。</p><a class="button" href="writing.html">开始阅读 <span>↗</span></a><a class="text-link" href="about.html">认识我 →</a></div><aside class="hero-aside"><div class="feature-photo"><img src="assets/hovercraft.png" alt="我负责的气垫悬浮车项目实物" width="1706" height="1279"><span class="photo-label">PROJECT 01 / 气垫悬浮车</span></div><p class="photo-note">从控制程序到实物调试<br><span>在搭建中运用知识，在调试中理解原理。</span></p></aside></section>
<section class="academic-strip" aria-label="学业表现"><div><strong>国家奖学金</strong><span>曾获荣誉</span></div><div><strong>1<span> / 10</span></strong><span>2025—2026学年成绩与综测排名</span></div><div><strong>93<span> 分</span></strong><span>答辩时推免课程均分</span></div><div><strong>634<span> 分</span></strong><span>大学英语六级</span></div></section>
<section class="section"><div class="section-head"><div><p class="eyebrow">WRITING / 学习与思考</p><h2>最近的记录</h2></div><a class="text-link" href="writing.html">全部文章 ↗</a></div>{post_rows(S['posts'])}</section>
<section class="section"><div class="section-head"><div><p class="eyebrow">SELECTED PROJECTS / 实践</p><h2>在动手中寻找答案</h2></div><a class="text-link" href="projects.html">查看项目 ↗</a></div><div class="project-grid"><a class="project" href="posts/hovercraft-project.html"><img src="assets/hovercraft.png" alt="气垫悬浮车" loading="lazy"><div class="project-meta"><span>省级大创 · 已结项</span><span>01</span></div><h3>气垫悬浮车 ↗</h3><p>项目负责人 / 软件设计 / 无刷电调驱动</p></a><a class="project" href="projects.html#air-ground"><img src="assets/drone.jpg" alt="空地协同系统中的无人机实物" loading="lazy"><div class="project-meta"><span>2026 年模电竞赛 · 三等奖</span><span>02</span></div><h3>空地协同系统 ↗</h3><p>救援物资抛投与行驶小车上的起降任务</p></a></div></section>
<section class="closing"><p class="eyebrow">BEYOND THE LAB / 学习之外</p><h2>认真探索，也认真生活。</h2><p>喜欢乒乓球和匹克球，也参与班级事务与志愿服务。<br>在团队协作和服务他人的过程中，一点点成为更好的自己。</p><a class="text-link" href="about.html">更多关于我 →</a></section>'''
save('index.html', page('首页', home, 'home'))

writing = f'''<section class="page-heading"><p class="eyebrow">WRITING / 文章</p><h1>记录，理解，再出发。</h1><p>竞赛复盘、项目实践，以及在学习中逐渐想明白的事。</p></section><div class="search-line"><label for="search">搜索文章</label><input id="search" type="search" placeholder="输入标题、分类或关键词" autocomplete="off"><span id="result-count" aria-live="polite">{len(S['posts'])} 篇文章</span></div><section class="post-list" aria-label="文章列表">{post_rows(S['posts'])}<p id="empty" hidden>没有找到相关文章，试试其他关键词。</p></section>'''
save('writing.html', page('文章', writing, 'writing'))

awards = [('2025', '全国大学生电子设计竞赛', '陕西赛区一等奖'), ('2025', '全国大学生数学竞赛', '省级二等奖'), ('2026', '全国大学生英语竞赛', '省级三等奖'), ('2026', '陕西省大学生模拟及模数混合电路应用设计竞赛', '三等奖'), ('2026', '校数学建模竞赛', '二等奖')]
about = '''<section class="page-heading"><p class="eyebrow">ABOUT / 关于我</p><h1>你好，我是张斌诚。</h1><p>西安电子科技大学光电工程学院<br>2024 级光电信息科学与工程专业 · 教改班</p></section><div class="about-layout"><aside class="about-index"><span>01 / 学业与荣誉</span><span>02 / 技能与兴趣</span><span>03 / 科研与实践</span><span>04 / 学习之外</span></aside><div class="prose"><h2>学业与荣誉</h2><p>我始终把学习作为基础，也喜欢用实际任务检验自己的理解。2025—2026 学年，我的学习成绩与综合测评均位列教改班第一；答辩时推免课程均分为 93 分，大学英语六级 634 分。曾获国家奖学金、“军训优秀学员”称号。</p><ul>'''+''.join(f'<li>{year} 年{esc(name)}：<strong>{esc(prize)}</strong></li>' for year, name, prize in awards)+'''</ul><h2>技能与兴趣</h2><p>围绕智能无人系统，逐步学习单片机开发、电机控制与视觉识别。接触的工具与技术包括 STM32、TI MSPM0、C++、Python、Verilog、ROS、OpenCV 和 Linux。希望在持续实践中，成长为软硬件兼通的工程师。</p><h2 id="research">科研与实践</h2><p>主持气垫悬浮车省级大创项目并完成结项，另有自动行驶小车项目获 2026 年省级大创立项。</p><p>在微波光子创新俱乐部，参与文爱军老师指导的微波光子雷达回波模拟相关工作，以及韩彪老师指导的激光通信 PPS/TOD 授时相关研究。竞赛经验帮助我更快上手任务，科研实践则让我更加重视原理与结果的可靠性。</p><h2>学习之外</h2><p>我热爱乒乓球和匹克球，参加 2025 年、2026 年“西军电杯”匹克球比赛，与队友两次为光电工程学院赢得团体赛亚军。</p><p>我也参与班级事务、帮助学业困难同学，并在“西小电”志愿服务中陪伴教职工子女，担任他们的“小老师”。牛津剑桥访学期间，我担任小组队长，与跨校同学合作完成医学图像分类模型，并参访树莓派公司。</p><blockquote>在实践中求真，在坚持中成长。</blockquote></div></div>'''
save('about.html', page('关于我', about, 'about'))

projects = '''<section class="page-heading"><p class="eyebrow">PROJECTS / 项目</p><h1>让知识在实物中落地。</h1><p>从模块开发到系统联调，在具体任务中积累工程实践经验。</p></section><article class="project-detail"><img src="assets/hovercraft.png" alt="气垫悬浮车项目实物"><div><p class="eyebrow">01 / 省级大创 · 已结项</p><h2>基于高速轴流风机的气垫悬浮车</h2><p>担任项目负责人，承担软件设计与无刷电调驱动工作，与团队完成系统搭建和调试。</p><a class="text-link" href="posts/hovercraft-project.html">阅读项目记录 ↗</a></div></article><article class="project-detail" id="air-ground"><img src="assets/drone.jpg" alt="空地协同无人机"><div><p class="eyebrow">02 / 2026 年模电竞赛</p><h2>空地协同系统</h2><p>与队友合作完成救援物资抛投和无人机在行驶小车上起降任务，获得陕西省大学生模拟及模数混合电路应用设计竞赛三等奖。</p><a class="text-link" href="posts/starting-with-an-led.html">阅读竞赛经历 ↗</a></div></article><article class="research-detail"><p class="eyebrow">03 / 省级大创 · 已立项</p><h2>基于 MSPM0 系列单片机的自动行驶小车</h2><p>担任项目负责人，开展软硬件设计与调试。项目于 2026 年获省级大创立项。</p></article><article class="research-detail"><p class="eyebrow">04 / 科研实践</p><h2>微波光子雷达与激光通信授时</h2><p>参与微波光子雷达回波模拟及激光通信 PPS/TOD 授时相关工作，在链路搭建和实验验证中积累经验。</p><a class="text-link" href="posts/competition-and-research.html">阅读科研随笔 ↗</a></article>'''
save('projects.html', page('项目实践', projects, 'projects'))

for i,p in enumerate(S['posts']):
    text = (ROOT / p['file']).read_text(encoding='utf-8')
    following = S['posts'][(i+1) % len(S['posts'])]
    body = f'''<div class="article-top"><a href="../writing.html">← 返回文章</a><span>{esc(p['category'])} / {p['date'].replace('-', '.')}</span></div><article class="article"><header><h1>{esc(p['title'])}</h1><p class="article-summary">{esc(p['summary'])}</p><span class="byline">张斌诚 · 约 {max(1, round(len(text)/350))} 分钟阅读</span></header><div class="prose">{markdown(text)}</div></article><a class="next-post" href="{following['slug']}.html"><span>继续阅读</span><strong>{esc(following['title'])} ↗</strong></a>'''
    save('posts/'+p['slug']+'.html', page(p['title'], body, 'writing', 1, p['summary']))

save('404.html', page('页面未找到', '<section class="page-heading"><p class="eyebrow">404</p><h1>这页暂时没有记录。</h1><p>可以回到首页，继续阅读其他文章。</p><a class="button" href="'+URL+'/index.html">返回首页 ↗</a></section>'))
save('.nojekyll', '')
save('robots.txt', 'User-agent: *\nAllow: /\nSitemap: '+URL+'/sitemap.xml\n')
paths=['index.html','about.html','writing.html','projects.html']+['posts/'+p['slug']+'.html' for p in S['posts']]
save('sitemap.xml','<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+URL+'/'+p+'</loc></url>' for p in paths)+'</urlset>')
items=''.join(f'<item><title>{esc(p["title"])}</title><link>{URL}/posts/{p["slug"]}.html</link><guid>{URL}/posts/{p["slug"]}.html</guid><description>{esc(p["summary"])}</description><pubDate>{format_datetime(datetime.fromisoformat(p["date"]+"T12:00:00+08:00"))}</pubDate></item>' for p in S['posts'])
save('feed.xml',f'<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>{esc(S["title"])}</title><link>{URL}</link><description>{DESC}</description><language>zh-CN</language>{items}</channel></rss>')
print(f'Built {len(paths)} pages and RSS for {S["github"]}.')
