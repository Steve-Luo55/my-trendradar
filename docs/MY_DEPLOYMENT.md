# 我的 TrendRadar

- 首页：<https://steve-luo55.github.io/my-trendradar/>
- 热点阅读：<https://steve-luo55.github.io/my-trendradar/report/>
- 官方界面的配置编辑器：<https://steve-luo55.github.io/my-trendradar/editor/>
- 信源与更新说明：<https://steve-luo55.github.io/my-trendradar/sources.html>
- 仓库：<https://github.com/Steve-Luo55/my-trendradar>
- 运行与日志：<https://github.com/Steve-Luo55/my-trendradar/actions>
- 推送密钥：<https://github.com/Steve-Luo55/my-trendradar/settings/secrets/actions>

## 当前配置

基于官方 TrendRadar v6.11.0 模板，每小时第 37 分钟抓取一次，显示北京时间。
GitHub 定时任务可能延迟。每次成功抓取后更新 GitHub Pages，电脑关机也能运行。
保留原有 11 个热榜，增加 GitHub Trending；RSS 启用 Google Trends 美国、Hacker News 和 Ars Technica。搜索与科技来源另有不经关键词过滤的展示区，每个源最多 20 条。
官方默认雅虎财经 RSS 地址返回 404，已停用；阮一峰 RSS 沿用默认停用设置。
修改 `config/frequency_words.txt` 和 `config/config.yaml` 即可调整。

当前使用关键词筛选，AI 分析和 AI 翻译关闭，无需大模型 API 密钥。
网页只发布当次生成的 HTML，不公开数据库或密钥。
当前存储后端为 `local`，每次任务使用临时数据库，网页展示当前榜单，
不提供跨次运行的历史记录或可靠的增量去重。

## 新闻报告与配置编辑器

网站首页是导航入口，`/report/` 是官方新闻报告，`/editor/` 是基于上游官方界面的配置编辑器。编辑器默认只显示可视化设置，YAML/TXT 源码按需展开。
编辑器首次访问会载入本次部署去除凭据后的配置；已有本机草稿则保留。
切换中英文只影响界面，不会换成另一套上游默认配置。
修改只保存在当前浏览器，须导出并提交到仓库的 `config/` 对应文件后，后台任务才会采用。

## 接通消息推送

在上方“推送密钥”页面点击 **New repository secret**，按使用渠道添加：

| 渠道 | Secret 名称 |
| --- | --- |
| 飞书 | `FEISHU_WEBHOOK_URL` |
| 钉钉 | `DINGTALK_WEBHOOK_URL` |
| 企业微信 | `WEWORK_WEBHOOK_URL` |
| Telegram | `TELEGRAM_BOT_TOKEN`、`TELEGRAM_CHAT_ID` |
| 邮件 | `EMAIL_FROM`、`EMAIL_PASSWORD`、`EMAIL_TO` |
| Bark | `BARK_URL` |
| ntfy | `NTFY_TOPIC`；私有服务器另配 `NTFY_SERVER_URL`、`NTFY_TOKEN` |

邮件使用邮箱提供的 SMTP 授权码；可另配 `EMAIL_SMTP_SERVER` 和 `EMAIL_SMTP_PORT`。
本部署使用 QQ 邮箱（支持 `foxmail.com` 别名），已通过 Secrets 显式设置
`EMAIL_SMTP_SERVER=smtp.qq.com`、`EMAIL_SMTP_PORT=465`，以 SSL 连接发送。
不要将 Webhook、邮箱授权码或 API 密钥提交到公开仓库。

保存密钥后，在 **Actions → Test Notifications → Run workflow** 发送一条测试消息。
日志成功并且目标渠道实际收到消息，才算接通。
邮件改为每天北京时间 **08:30、20:30** 两次；每小时第 37 分钟的网页更新不再发邮件。GitHub 的定时事件可能延迟或丢弃，时间是计划值，实际执行以 Actions 记录为准。两次邮件是抓取当时的当前榜单，并非当天历史汇总。

手动更新默认不发送邮件；需要测试完整邮件时，可在 **Run workflow** 中勾选 **send_email**。编辑器内的调度模板目前未开启，早晚两个时刻由 GitHub 工作流决定。

## 自动运行与平台限制

本副本已移除上游工作流中以 `604800` 秒判断的 7 天停用逻辑，
同时移除会删除运行日志的 Check In 工作流，不再需要每周签到。
抓取仍为每小时一次；实际执行时间和成功情况请查看 Actions 日志。

GitHub 自身仍可能在公开仓库连续 60 天无活动时停用定时工作流，
高负载时调度也可能延迟或丢弃。这些平台行为不能通过本项目保证消除。
参考：https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule

## 手动更新与排错

运行 **Actions → Get Hot News → Run workflow** 可以立即更新网页。
抓取或网页发布失败时查看对应步骤日志，旧网页会保持上次成功内容。
部分信源可能临时不可用，网页会标明失败平台。
需要历史记录时按官方文档配置 S3 兼容远程存储，并将 `storage.backend` 改为 `auto` 或 `remote`。
