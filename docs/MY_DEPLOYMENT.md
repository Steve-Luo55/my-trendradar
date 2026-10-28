# 我的 TrendRadar

- 网页：<https://steve-luo55.github.io/my-trendradar/>
- 仓库：<https://github.com/Steve-Luo55/my-trendradar>
- 运行与日志：<https://github.com/Steve-Luo55/my-trendradar/actions>
- 推送密钥：<https://github.com/Steve-Luo55/my-trendradar/settings/secrets/actions>

## 当前配置

基于官方 TrendRadar v6.11.0 模板，每小时第 33 分钟抓取一次，显示北京时间。
GitHub 定时任务可能延迟。每次成功抓取后更新 GitHub Pages，电脑关机也能运行。
关键词、11 个热榜平台和 RSS 来源采用官方默认配置，修改 `config/frequency_words.txt`
和 `config/config.yaml` 即可调整。

当前使用关键词筛选，AI 分析和 AI 翻译关闭，无需大模型 API 密钥。
网页只发布当次生成的 HTML，不公开数据库或密钥。
未配置远程存储时，每次任务使用临时数据库，网页展示当前榜单，
不提供跨次运行的历史记录或可靠的增量去重。

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
不要将 Webhook、邮箱授权码或 API 密钥提交到公开仓库。

保存密钥后，在 **Actions → Test Notifications → Run workflow** 发送一条测试消息。
日志成功并且目标渠道实际收到消息，才算接通。
此后 **Get Hot News** 每小时会向已配置渠道发送匹配到的当前榜单。

## 每周签到

保留官方 7 天活跃检测机制。每 7 天内手动运行一次
**Actions → Check In → Run workflow**。该官方工作流会清理运行记录并重置计时。
到期后如抓取已停用，先签到，再启用 **Get Hot News** 并手动运行。

## 手动更新与排错

运行 **Actions → Get Hot News → Run workflow** 可以立即更新网页。
抓取或网页发布失败时查看对应步骤日志，旧网页会保持上次成功内容。
部分信源可能临时不可用，网页会标明失败平台。
需要历史记录时按官方文档配置 S3 兼容远程存储。
