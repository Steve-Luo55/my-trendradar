# 我的 TrendRadar

[English](README-EN.md) · [热点报告](https://steve-luo55.github.io/my-trendradar/) · [配置编辑器](https://steve-luo55.github.io/my-trendradar/editor/) · [信源说明](https://steve-luo55.github.io/my-trendradar/sources.html) · [运行记录](https://github.com/Steve-Luo55/my-trendradar/actions)

个人热点阅读与邮件推送服务。每小时抓取配置中的平台热榜与 RSS，按关键词筛选后更新网页，并发送到已配置的邮箱。

## 当前接入

- **11 个平台热榜**：今日头条、百度热搜、华尔街见闻、澎湃新闻、bilibili 热搜、财联社热门、凤凰网、贴吧、微博、抖音、知乎。通过 NewsNow 聚合 API 获取标题、榜单名次及原文链接，并非直接抓取各站全文。
- **1 个 RSS 源**：Hacker News，使用 `https://hnrss.org/frontpage`。
- 阮一峰博客目前关闭；雅虎财经的默认 RSS 地址返回 404，已关闭。

## 如何使用

打开网页阅读本次关键词命中的热点，使用搜索、主题标签和明暗主题切换。条目链接指向原始页面。邮件推送使用 QQ SMTP，凭据保存在 GitHub Actions Secrets。

配置编辑器沿用官方的可视化界面，加载本部署去除凭据后的配置快照。编辑草稿保存在当前浏览器，导出并提交到仓库后才会改变后台任务；界面语言切换不会切换成另一套采集配置。

定时配置为每小时第 **37 分钟**运行，时间显示为北京时间；GitHub 调度可能延迟。每次实际运行时间以网页和 Actions 日志为准。

本副本已移除上游的 7 天签到停用机制，无需每周清空日志签到。GitHub 自身的调度规则仍适用，公开仓库长期没有活动时可能停用定时任务。

## 数据与功能边界

当前使用关键词筛选；AI 分类、分析和翻译均未启用。关键词命中不等于事实核验。当前榜单仅展示最近一次抓取结果，暂未配置跨次运行的历史数据库或可靠的增量去重。

## 配置与维护

- [部署和邮件设置](docs/MY_DEPLOYMENT.md)
- [信源配置](config/config.yaml)
- [关键词配置](config/frequency_words.txt)
- [手动运行抓取](https://github.com/Steve-Luo55/my-trendradar/actions/workflows/crawler.yml)
- [测试通知](https://github.com/Steve-Luo55/my-trendradar/actions/workflows/test-notification.yml)
- [上游技术文档](https://trendradar.sandev.cc/zh/docs/)

## 来源与许可证

基于 [sansan0/TrendRadar](https://github.com/sansan0/TrendRadar) v6.11.0 修改，保留上游版权说明与 [GPL-3.0 许可证](LICENSE)。平台聚合数据来自 [NewsNow](https://github.com/ourongxing/newsnow)。本仓库移除了赞助广告、邀请返利链接和推广二维码。
