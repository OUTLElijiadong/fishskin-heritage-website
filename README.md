# 鱼皮非遗文化网站

展示鱼皮制作技艺（非物质文化遗产）的单页网站，介绍鱼皮工艺的历史、作品、传承人与相关动态。

[![CI](https://github.com/OUTLElijiadong/fishskin-heritage-website/actions/workflows/ci.yml/badge.svg)](https://github.com/OUTLElijiadong/fishskin-heritage-website/actions/workflows/ci.yml)
[![部署 Pages](https://github.com/OUTLElijiadong/fishskin-heritage-website/actions/workflows/pages.yml/badge.svg)](https://github.com/OUTLElijiadong/fishskin-heritage-website/actions/workflows/pages.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)

- **在线预览**：<https://outlelijiadong.github.io/fishskin-heritage-website/>
- **技术形态**：纯静态单页，**无构建步骤**

## 快速开始

直接用浏览器打开 `index.html` 即可。若需要本地起服务（推荐，避免 `file://` 协议下的资源加载差异）：

```bash
python3 -m http.server 8000
# 浏览器访问 http://localhost:8000
```

改完想自查一遍再提交：

```bash
python3 scripts/check_assets.py index.html   # 本地资源 + 站内锚点自检
npx html-validate index.html                 # HTML 规范检查
```

## 页面结构

| 区块 | 锚点 | 说明 |
|---|---|---|
| 首页横幅 | `#home` | 鱼皮非遗文化主题，背景图为 `封面.jpg` |
| 工艺介绍 | `#about` | 鱼皮工艺的历史与特点 |
| 作品展示 | `#gallery` | 鱼皮工艺品图集 |
| 传承人风采 | `#inheritors` | 传承人介绍 |
| 新闻动态 | `#news` | 相关活动信息 |
| 联系我们 | `#contact` | 联系方式与留言板 |

## 技术栈

- HTML5 + Tailwind CSS（CDN 引入，**非生产构建**，仅适合展示型站点）
- Font Awesome 6.4.0 图标（CDN）
- Google Fonts：Noto Serif SC

> CDN 方案的优点是零构建、零依赖；代价是首屏受第三方网络影响，且 Tailwind 的 JIT 在客户端执行。
> 若将来要上生产流量，建议改为本地构建产物替换 CDN。

## 目录结构

```
├── index.html              # 网站主页面（单页）
├── 封面.jpg                # 首页横幅背景图（CSS url() 引用）
├── scripts/
│   └── check_assets.py     # 资源与锚点自检脚本（CI 调用）
├── docs/
│   └── ISSUE_MANAGEMENT.md # 标签 / 里程碑 / 看板使用说明
├── .github/
│   ├── CODEOWNERS          # 评审负责人
│   ├── ISSUE_TEMPLATE/     # issue 表单
│   ├── PULL_REQUEST_TEMPLATE.md
│   ├── dependabot.yml      # 依赖与 action 版本自动更新
│   └── workflows/
│       ├── ci.yml          # 结构 / 资源 / 文档校验
│       ├── pages.yml       # 部署 GitHub Pages
│       ├── release.yml     # release-please 自动发版
│       └── pr-title.yml    # Conventional Commits 校验
├── .release-please-config.json
├── .release-please-manifest.json
├── .htmlvalidate.json      # HTML 检查规则
└── .gitmessage             # 本地提交信息模板
```

## 自动化

| 触发 | 工作流 | 作用 |
|---|---|---|
| PR / push main | `ci.yml` | 资源与锚点自检、HTML 规范检查、Markdown 死链检查 |
| push main | `pages.yml` | 自动部署到 GitHub Pages |
| push main | `release.yml` | 扫描 Conventional Commits，维护 Release PR、打 tag、发版 |
| PR 创建/编辑 | `pr-title.yml` | 校验 PR 标题是否符合 Conventional Commits |
| 每周一 03:00 | Dependabot | 更新 workflow 引用的 action 版本 |

发版规则：`fix:` → patch，`feat:` → minor，`!`/`BREAKING CHANGE` → major，`docs`/`chore`/`ci` 不触发发版。

## 参与贡献

分支命名、提交信息、评审流程请见 **[CONTRIBUTING.md](./CONTRIBUTING.md)**。
标签体系、里程碑与看板用法请见 **[docs/ISSUE_MANAGEMENT.md](./docs/ISSUE_MANAGEMENT.md)**。
安全问题请先阅读 **[SECURITY.md](./SECURITY.md)**。

## 内容声明

- 作品区、传承人、新闻配图当前为占位图（`picsum.photos`），可在 `index.html` 中替换为真实素材。
- 页面中的人物、新闻、联系方式均为演示占位内容，**非真实信息**。
- 网站为响应式设计，适配桌面与移动端。

## 许可证

[MIT License](./LICENSE) © 李嘉栋 (OUTLElijiadong)
