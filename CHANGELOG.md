# Changelog

本文件遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/) 格式，
版本号遵循 [语义化版本 2.0.0](https://semver.org/lang/zh-CN/)。

自本文件建立之日起，正式的版本条目由 [release-please](https://github.com/googleapis/release-please)
自动生成——它扫描 main 分支上的 Conventional Commits，在 Release PR 中累计变更、
算出下一个版本号，PR 合并后自动打 tag 并发布 GitHub Release。**请勿手改自动生成的条目。**

## 历史变更（自动化启用前）

以下条目为人工补录，记录了启用自动化之前的提交历史。

### 2026-09-13

- 初始化仓库：鱼皮非遗文化网站单页（首页横幅、工艺介绍、作品展示、传承人风采、新闻动态、联系我们六个区块）
- 新增 MIT LICENSE
- 替换联系方式中的占位信息，并在 README 中标注页面内容为演示数据
- 为图标按钮补充 `type="button"` 与 `aria-label`，为社交图标链接补充 `aria-label`（无障碍修复）
- 补齐 `.gitignore`、CI、Pages 部署、自动发版、issue/PR 模板等仓库规范化配置
