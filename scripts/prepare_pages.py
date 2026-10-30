"""Publish the news report and a credential-free copy of the official editor."""

from copy import deepcopy
from html import escape
from html import unescape
from pathlib import Path
import re
import shutil

import yaml

ROOT = Path(__file__).resolve().parents[1]
SITE_URL = "https://steve-luo55.github.io/my-trendradar/"


def with_canonical(html, url):
    html = re.sub(r'<link\b[^>]*\brel=["\']canonical["\'][^>]*>', "", html, flags=re.I)
    return html.replace("</head>", f'<link rel="canonical" href="{url}"></head>', 1)


def public_config(config):
    """Project runtime settings without notification, AI, or storage credentials."""
    result = deepcopy(config)
    channels = result.get("notification", {}).get("channels", {})
    for settings in channels.values():
        for key in settings:
            if key != "msg_type":
                settings[key] = ""
    if "ai" in result:
        result["ai"]["api_key"] = ""
    remote = result.get("storage", {}).get("remote", {})
    for key in remote:
        if key != "retention_days":
            remote[key] = ""
    return result


def navigation(base="./"):
    return f'''<nav class="site-nav" aria-label="网站导航">
<a href="{base}">首页</a><a href="{base}report/">热点报告</a><a href="{base}editor/">配置编辑器</a><a href="{base}sources.html">信源与更新说明</a>
</nav>'''
STYLE = '''<style>
.site-nav{max-width:1200px;margin:0 auto 16px;display:flex;flex-wrap:wrap;gap:8px;font:14px/1.5 system-ui,sans-serif}
.site-nav a{padding:9px 14px;border:1px solid #e2e8f0;border-radius:8px;color:#334155;background:#fff;text-decoration:none}
.site-nav a:hover,.site-nav a:focus-visible{color:#4f46e5;border-color:#818cf8;outline:2px solid transparent}
@media screen and (max-width:480px){.site-nav{gap:6px}.site-nav a{padding:8px 10px;font-size:12px}}
</style>'''


def home_page(report_html, config):
    metadata = dict(re.findall(r'<span class="info-label">([^<]+)</span>\s*<span class="info-value">([^<]*)</span>', report_html))
    generated = escape(unescape(metadata.get("生成时间", "见热点报告")))
    platforms = len(config.get("platforms", {}).get("sources", []))
    feeds = sum(feed.get("enabled", True) for feed in config.get("rss", {}).get("feeds", []))
    html = '''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>我的 TrendRadar · 阅读与设置</title>
<meta name="description" content="从一个入口阅读热点报告、调整关键词和订阅源，查看趋势覆盖与更新安排。">
<style>
*{box-sizing:border-box}body{margin:0;background:#f5f7f8;color:#17262b;font:15px/1.7 -apple-system,BlinkMacSystemFont,'Segoe UI','PingFang SC','Microsoft YaHei',sans-serif}
a{color:inherit}header,main,footer{max-width:1120px;margin:auto;padding:0 28px}header{display:flex;align-items:center;justify-content:space-between;gap:16px;padding-top:28px;padding-bottom:28px;border-bottom:1px solid #dce4e7}
.brand{text-decoration:none;font-size:20px;font-weight:750;letter-spacing:-.5px}.brand span{color:#137a71}header>span{font-size:12px;color:#63777e}
.hero{padding:58px 0 34px}.eyebrow{font-size:12px;font-weight:700;color:#137a71;letter-spacing:1px}h1{font-size:clamp(30px,4vw,44px);line-height:1.3;letter-spacing:-1px;margin:12px 0 18px}.intro{max-width:640px;color:#53666e;font-size:16px}
.status{display:flex;flex-wrap:wrap;gap:12px 24px;margin-top:28px;font-size:13px;color:#53666e}.status strong{color:#17262b;font-weight:650}
.cards{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px;padding:8px 0 36px}.card{display:flex;flex-direction:column;text-decoration:none;min-width:0;min-height:250px;padding:27px;background:#fff;border:1px solid #dce4e7;border-radius:14px;transition:transform .15s,border-color .15s,box-shadow .15s}.card:hover{transform:translateY(-3px);border-color:#7fb6af;box-shadow:0 10px 28px #123c3510}.card:focus-visible{outline:3px solid #137a71;outline-offset:4px}.card-number{font:12px ui-monospace,monospace;color:#74878d}.card h2{font-size:22px;line-height:1.4;margin:26px 0 10px}.card p{font-size:14px;color:#60737b;margin:0 0 20px}.card-action{margin-top:auto;color:#137a71;font-weight:650;font-size:14px}
.primary{background:#153f3b;border-color:#153f3b;color:#fff}.primary .card-number,.primary p{color:#c2d9d5}.primary .card-action{color:#b5ebe1}.note{padding:22px 26px;border:1px solid #dce4e7;border-radius:12px;background:#edf2f3;color:#53666e;font-size:13px}.note strong{color:#304950}footer{padding-top:28px;padding-bottom:28px;color:#74878d;font-size:12px}footer a{color:#52696f}
@media(max-width:760px){header,main,footer{padding-left:18px;padding-right:18px}.hero{padding-top:32px}.cards{grid-template-columns:1fr;gap:14px}.card{min-height:195px;padding:23px}.card h2{margin-top:18px}.note{padding:18px}header{padding-top:20px;padding-bottom:20px}header>span{max-width:130px;text-align:right}}
</style></head><body>
<header><a class="brand" href="./">Trend<span>Radar</span></a><span>我的热点与趋势工作台</span></header>
<main><section class="hero"><div class="eyebrow">READ · CONFIGURE · UNDERSTAND</div>
<h1>从这里开始，找到你关心的变化。</h1><p class="intro">先阅读最新热点，再按需要调整关注词和订阅源。阅读页面与配置工具分开，每个入口只做一件事。</p>
<div class="status">'''
    html += f'<span>报告生成 <strong>{generated}</strong>（北京时间）</span><span>已配置 <strong>{platforms} 个热榜 · {feeds} 个 RSS</strong></span><span>邮件计划 <strong>08:30 / 20:30</strong></span>'
    html += '''</div></section><section class="cards" aria-label="选择页面">
<a class="card primary" href="report/"><span class="card-number">01 / READER</span><h2>阅读热点报告</h2><p>查看关键词热点，以及 Google Trends 美国、GitHub Trending 和科技订阅。保留官方报告的搜索、主题与导出功能。</p><span class="card-action">进入阅读页 →</span></a>
<a class="card" href="editor/"><span class="card-number">02 / SETTINGS</span><h2>可视化配置</h2><p>调整订阅源、关键词和展示方式。默认显示可视化设置，原始配置文件需要时再打开。</p><span class="card-action">打开配置工具 →</span></a>
<a class="card" href="sources.html"><span class="card-number">03 / COVERAGE</span><h2>了解信源与更新</h2><p>查看接入了什么、尚未覆盖什么，以及采集、邮件和数据保存的实际边界。</p><span class="card-action">查看覆盖说明 →</span></a>
</section><section class="note"><strong>使用提示</strong>　邮件计划为北京时间早晚各一次，网页另有定时采集；GitHub 的实际触发可能延迟。配置工具中的修改需导出并提交到仓库后生效，邮件凭据仍由 GitHub Secrets 管理。</section></main>
<footer>个人部署 · 基于 <a href="https://github.com/sansan0/TrendRadar">TrendRadar</a> · GPL-3.0 · <a href="https://github.com/Steve-Luo55/my-trendradar/actions">实际运行记录</a></footer>
<script>if(/^#tab-\\d+$/.test(location.hash)){location.replace('report/'+location.hash);}</script>
</body></html>'''
    return with_canonical(html, SITE_URL)


def prepare_pages(output=None):
    output = Path(output) if output else ROOT / "pages_dist"
    report = ROOT / "output/index.html"
    if not report.is_file() or "</html>" not in report.read_text():
        raise RuntimeError("A complete, newly generated HTML report is required")
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)
    config = yaml.safe_load((ROOT / "config/config.yaml").read_text())
    html = report.read_text().replace("</head>", STYLE + "</head>", 1)
    html = html.replace("<body>", "<body>" + navigation("../"), 1)
    (output / "report").mkdir()
    (output / "report/index.html").write_text(with_canonical(html, SITE_URL + "report/"))
    (output / "index.html").write_text(home_page(report.read_text(), config))
    (output / ".nojekyll").touch()

    editor = output / "editor"
    (editor / "assets").mkdir(parents=True)
    (editor / "index.html").write_text(with_canonical((ROOT / "docs/index.html").read_text(), SITE_URL + "editor/"))
    for name in ("style.css", "script.js", "i18n.js"):
        shutil.copyfile(ROOT / "docs/assets" / name, editor / "assets" / name)
    (editor / "version_configs").write_text((ROOT / "version_configs").read_text())

    (editor / "config").mkdir()
    (editor / "config/config.yaml").write_text(yaml.safe_dump(public_config(config), allow_unicode=True, sort_keys=False))
    for name in ("frequency_words.txt", "timeline.yaml"):
        shutil.copyfile(ROOT / "config" / name, editor / "config" / name)

    rows = []
    for source in config["platforms"]["sources"]:
        rows.append(f'<tr><td>{escape(source["name"])}</td><td>热榜</td><td>NewsNow 聚合 API</td><td>启用</td></tr>')
    for feed in config["rss"]["feeds"]:
        status = "启用" if feed.get("enabled", True) else "关闭"
        rows.append(f'<tr><td>{escape(feed["name"])}</td><td>RSS</td><td>{escape(feed["url"])}</td><td>{status}</td></tr>')
    page = '''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>信源与更新说明 · 我的 TrendRadar</title>'''
    page += STYLE + '''<style>body{margin:0;padding:24px;background:#f8fafc;color:#1e293b;font:16px/1.8 system-ui,sans-serif}
main{max-width:1000px;margin:auto;background:white;padding:32px;border:1px solid #e2e8f0;border-radius:12px}
h1{font-size:28px}h2{font-size:20px;margin-top:32px}.table-wrap{overflow-x:auto}table{width:100%;border-collapse:collapse;font-size:14px}
th,td{padding:10px 12px;border-bottom:1px solid #e2e8f0;text-align:left;overflow-wrap:anywhere}
@media(max-width:480px){body{padding:12px}main{padding:18px}h1{font-size:23px}}</style></head><body>'''
    platform_count = len(config["platforms"]["sources"])
    feed_count = sum(feed.get("enabled", True) for feed in config["rss"]["feeds"])
    page += navigation() + f'''<main><h1>信源与更新说明</h1>
<p>当前启用 {platform_count} 个平台热榜和 {feed_count} 个 RSS 源。下表是采集配置；每轮实际成功情况以热点报告和运行日志为准。</p>
<div class="table-wrap"><table><thead><tr><th>来源</th><th>类型</th><th>获取渠道</th><th>配置状态</th></tr></thead><tbody>'''
    page += "".join(rows) + '''</tbody></table></div>
<h2>收集到什么</h2><p>热榜通过 NewsNow 获取标题、排名及原始链接，部分返回数据可能来自上游缓存；没有抓取各平台文章全文。
Google Trends 美国使用 Google 官方 Trending Now RSS，它是美国地区的近期热搜，不是全球总榜，也不包含完整的关键词历史曲线。
热搜词链接打开该词的 Google Trends 查询页；本站没有抓取或保存该查询页的历史数据。
Hacker News 通过 hnrss.org 订阅获取，Ars Technica 使用媒体自有 RSS。雅虎财经默认 RSS 地址因返回 404 已关闭，阮一峰博客保持关闭。</p>
<h2>筛选与保存</h2><p>关键词区域展示匹配到的条目，RSS 同时启用 1 天的新鲜度过滤。
Google Trends、GitHub Trending、Hacker News 和 Ars Technica 另外完整展示各源最多 20 条，不受关键词过滤；部分条目可能同时出现在关键词区域。
当前没有开启 AI 筛选、翻译或分析，关键词命中不代表内容经过事实核验。
每轮使用临时数据库，当前站点没有跨次运行的历史记录或可靠的增量去重。</p>
<h2>什么时候更新与发邮件</h2><p>网页计划每小时第 37 分钟抓取更新。邮件另设每天北京时间 08:30、20:30 两次，普通网页更新不发邮件。
两种任务都使用本次抓取的当前榜单，并非全天历史汇总。GitHub 的实际启动可能延迟或漏触发，不能保证准点送达，实际执行请查看运行记录。
本副本已移除上游 7 天停用和签到清日志流程，无需每周签到。GitHub 自身的调度与长期无活动停用规则仍适用。</p>
<h2>仍未覆盖的内容</h2><p>没有接入 Google Trends Explore 历史曲线、完整全球跨地区趋势，也没有覆盖 Reddit、X、YouTube、Product Hunt 等全部榜单。
现有清单只代表明确列出的来源，不代表所有重要趋势都已收齐。</p>
<h2>配置怎么生效</h2><p>配置编辑器用于编辑和导出文件，草稿仅保存在当前浏览器。将导出的配置提交到本仓库后，后台任务才会使用新设置。
早晚邮件时间由 GitHub 工作流控制；编辑器内的“调度模板”目前未启用，调整它不会自动修改这两个邮件时刻。
公开编辑器中的配置副本已去除凭据；邮件授权码、收件地址和 API 密钥应保存在 GitHub Secrets。</p>
<p><a href="https://github.com/Steve-Luo55/my-trendradar/actions">查看实际运行记录</a> ·
基于 <a href="https://github.com/sansan0/TrendRadar">TrendRadar</a>，遵循 GPL-3.0 许可证。</p></main></body></html>'''
    (output / "sources.html").write_text(with_canonical(page, SITE_URL + "sources.html"))
    return output


if __name__ == "__main__":
    print(prepare_pages())
