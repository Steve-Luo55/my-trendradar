"""Publish the news report and a credential-free copy of the official editor."""

from copy import deepcopy
from html import escape
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


NAV = '''<nav class="site-nav" aria-label="网站导航">
<a href="./">热点报告</a><a href="./editor/">配置编辑器</a><a href="./sources.html">信源与更新说明</a>
</nav>'''
STYLE = '''<style>
.site-nav{max-width:1200px;margin:0 auto 16px;display:flex;flex-wrap:wrap;gap:8px;font:14px/1.5 system-ui,sans-serif}
.site-nav a{padding:9px 14px;border:1px solid #e2e8f0;border-radius:8px;color:#334155;background:#fff;text-decoration:none}
.site-nav a:hover,.site-nav a:focus-visible{color:#4f46e5;border-color:#818cf8;outline:2px solid transparent}
@media screen and (min-width:900px){.container{max-width:1200px}}
@media screen and (max-width:480px){.site-nav{gap:6px}.site-nav a{padding:8px 10px;font-size:12px}}
</style>'''


def prepare_pages(output=None):
    output = Path(output) if output else ROOT / "pages_dist"
    report = ROOT / "output/index.html"
    if not report.is_file() or "</html>" not in report.read_text():
        raise RuntimeError("A complete, newly generated HTML report is required")
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)
    html = report.read_text().replace("</head>", STYLE + "</head>", 1)
    html = html.replace("<body>", "<body>" + NAV, 1)
    (output / "index.html").write_text(with_canonical(html, SITE_URL))
    (output / ".nojekyll").touch()

    editor = output / "editor"
    (editor / "assets").mkdir(parents=True)
    (editor / "index.html").write_text(with_canonical((ROOT / "docs/index.html").read_text(), SITE_URL + "editor/"))
    for name in ("style.css", "script.js", "i18n.js"):
        shutil.copyfile(ROOT / "docs/assets" / name, editor / "assets" / name)
    (editor / "version_configs").write_text((ROOT / "version_configs").read_text())

    config = yaml.safe_load((ROOT / "config/config.yaml").read_text())
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
    page += NAV + '''<main><h1>信源与更新说明</h1>
<p>当前启用 11 个平台热榜和 1 个 RSS 源。下表是采集配置；每轮实际成功情况以热点报告和运行日志为准。</p>
<div class="table-wrap"><table><thead><tr><th>来源</th><th>类型</th><th>获取渠道</th><th>配置状态</th></tr></thead><tbody>'''
    page += "".join(rows) + '''</tbody></table></div>
<h2>收集到什么</h2><p>热榜通过 NewsNow 获取标题、排名及原始链接，部分返回数据可能来自上游缓存；没有抓取各平台文章全文。
Hacker News 通过 hnrss.org 提供的订阅获取。雅虎财经默认 RSS 地址因返回 404 已关闭，阮一峰博客保持关闭。</p>
<h2>筛选与保存</h2><p>网页和邮件展示关键词命中的条目，RSS 同时启用 1 天的新鲜度过滤。
当前没有开启 AI 筛选、翻译或分析，关键词命中不代表内容经过事实核验。
每轮使用临时数据库，当前站点没有跨次运行的历史记录或可靠的增量去重。</p>
<h2>什么时候更新</h2><p>GitHub Actions 计划每小时第 37 分钟抓取一次，报告显示北京时间，实际启动可能延迟。
本副本已移除上游 7 天停用和签到清日志流程，无需每周签到。GitHub 自身的调度与长期无活动停用规则仍适用。</p>
<h2>配置怎么生效</h2><p>配置编辑器用于编辑和导出文件，草稿仅保存在当前浏览器。将导出的配置提交到本仓库后，后台任务才会使用新设置。
公开编辑器中的配置副本已去除凭据；邮件授权码、收件地址和 API 密钥应保存在 GitHub Secrets。</p>
<p><a href="https://github.com/Steve-Luo55/my-trendradar/actions">查看实际运行记录</a> ·
基于 <a href="https://github.com/sansan0/TrendRadar">TrendRadar</a>，遵循 GPL-3.0 许可证。</p></main></body></html>'''
    (output / "sources.html").write_text(with_canonical(page, SITE_URL + "sources.html"))
    return output


if __name__ == "__main__":
    print(prepare_pages())
