# 贡献指南

本仓库是纯静态单页站点，流程刻意做轻：不引入 develop 长分支，不引入 release 分支。
核心原则只有一条——**main 永远可部署**，任何变更都先经过一条短生命周期分支和一次 PR。

## 一、分支模型

采用**主干开发（Trunk-Based）**：

```
main  ──────●───────────●───────────●───────────▶  永远可部署
             \         / \         /
              feature/  fix/  docs/
```

| 分支 | 生命周期 | 说明 |
|---|---|---|
| `main` | 永久 | 唯一主干，受保护，直接对应线上 Pages |
| `feature/<短名>` | 数小时 ~ 数天 | 新功能 / 新内容 |
| `fix/<短名>` | 数小时 | 缺陷修复 |
| `docs/<短名>` | 数小时 | 仅文档变更 |
| `chore/<短名>` | 数小时 | 依赖、CI、杂项配置 |
| `refactor/<短名>` | 数天 | 重构，不改变外部行为 |

**不设 `develop`**：静态站点没有「多版本并行集成」的需求，多一条长分支只会增加同步成本和误合风险。
将来若出现「main 要冻结、另开一轮预发布」的场景，再引入 `release/<版本>` 分支也不迟。

### 命名规则

- 全小写，用连字符分隔：`feature/gallery-real-photos`
- 分支名只写**意图**，不写人名、不写日期、不写 issue 号以外的编号
- 正确：`fix/contact-phone-validation`、`docs/add-pages-badge`
- 错误：`feature/2026-09-22-改图`、`fix-嘉栋测试`、`wip`

### 分支保护规则（`main`，仓库管理员配置）

| 规则 | 值 | 理由 |
|---|---|---|
| Require a pull request before merging | ✅ | 禁止直接推送 |
| Required approvals | 1 | 至少一次评审 |
| Dismiss stale approvals | ✅ | 代码改了就重新评审 |
| Require review from Code Owners | ✅ | 配合 `.github/CODEOWNERS` |
| Require status checks to pass | `结构与资源校验`、`文档链接校验`、`Conventional Commits 标题校验` | CI 不过不许合 |
| Require branches to be up to date | ✅ | 防止基于旧代码合并 |
| Require conversation resolution | ✅ | 评审意见要闭环 |
| Block force pushes | ✅ | 禁止改写已推送历史 |
| Block branch deletion | ✅ | 防止误删主干 |
| Include administrators | ❌ | 单人仓库保留管理员 bypass，否则会锁死自己 |
| Allow merge commits | ❌ | 只留 squash 和 rebase |
| Allow squash merging | ✅ **默认** | PR 标题即提交信息，历史保持线性干净 |
| Allow rebase merging | ✅ | 备用 |

> 为什么 Include administrators 关闭：本仓库当前是单人维护。
> 一旦开启，管理员也无法直接推 main，遇到 Pages 紧急故障时会失去快速通道。
> 若将来有第二位维护者，建议改为开启，并配合 CODEOWNERS 交叉评审。

## 二、提交信息规范

统一使用 [Conventional Commits](https://www.conventionalcommits.org/zh-hans/v1.0.0/)：

```
<type>(<scope>): <subject>

[可选正文]

[可选脚注：Closes #12 / BREAKING CHANGE: ...]
```

- `type`：`feat` `fix` `docs` `style` `refactor` `perf` `test` `build` `ci` `chore` `revert`
- `scope`（可选）：`gallery` `news` `inheritors` `contact` `layout` `assets` `deps` `release`
- `subject`：祈使句，不以大写字母开头，结尾不加句号

示例：

```
feat(gallery): 替换作品区占位图为真实素材
fix(contact): 修正手机号校验正则
docs: 补充 GitHub Pages 部署说明
chore(deps): 升级 actions/checkout 到 v4
```

### 本地配置（一次即可）

```bash
git config commit.template .gitmessage     # 提交时自动带出模板
git config commit.verbose true             # 提交时显示 diff，减少写错描述
```

### 校验机制

因为本仓库用 **squash merge**，PR 标题会直接成为提交信息，所以校验放在 PR 标题上：

- `pr-title.yml` 使用 `amannn/action-semantic-pull-request` 校验标题
- 标题不合规时 CI 直接失败，无法合并

没有引入 husky + commitlint：那需要 `package.json` 和 node_modules，
对一个零依赖的静态站点来说，维护成本大于收益。本地提交信息的质量靠 `.gitmessage` 模板保证。

## 三、开发流程

```bash
# 1. 从最新的 main 切分支
git switch main && git pull
git switch -c feature/gallery-real-photos

# 2. 改代码，本地验证
python3 -m http.server 8000
python3 scripts/check_assets.py index.html
npx html-validate index.html

# 3. 提交
git add -A
git commit                      # 会弹出 .gitmessage 模板

# 4. 推送并开 PR
git push -u origin feature/gallery-real-photos
gh pr create --fill
```

PR 标题必须写成 Conventional Commits 格式，`gh pr create --fill` 会拿第一条提交信息当标题。

### 评审要点

Reviewer 至少确认：

1. 桌面端与移动端（≤390px）均无布局错乱
2. 新增/替换的本地素材真实存在，无 404
3. 站内锚点跳转正常
4. 未写入真实人物的隐私信息（本站点内容均为演示数据）
5. 涉及 `.github/`、发布配置的改动，权限是否最小化

### 合并后

- 分支由 GitHub 自动删除（PR 页面勾选 *Automatically delete head branches*，或在仓库设置里开启）
- `main` 上的 push 会自动触发 CI、Pages 部署和 release-please

## 四、发版

发版完全自动，平时不需要手动干预：

1. `feat` / `fix` 合入 main 后，release-please 机器人会开（或更新）一个标题为
   `chore(main): release 0.x.x` 的 Release PR
2. 该 PR 里能看到它算出的版本号和将写入 CHANGELOG 的内容
3. **合并这个 PR = 发布**：自动打 tag `v0.x.x` 并创建 GitHub Release

只想发个补丁但不改代码时，可以手动触发：**Actions → 自动发版 → Run workflow**。

## 五、目录约定

- 站点本体文件放**仓库根目录**（Pages 从根目录发布）
- 脚本放 `scripts/`，文档放 `docs/`，配置放 `.github/`
- 新增本地素材用**英文小写 + 连字符**命名，避免中文文件名在部分 CDN 上的编码问题

## 六、行为准则

- 技术讨论对事不对人
- 提 issue 前先搜索是否已有重复
- 发现安全问题**不要开公开 issue**，按 [SECURITY.md](./SECURITY.md) 处理
