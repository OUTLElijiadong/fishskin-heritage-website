# 议题管理规范

本文件定义标签体系、里程碑与项目看板的使用方式。目标是：**任何一个 issue 在任何时刻都能立刻回答
「它是什么、多紧急、归谁、排在哪一轮」**。

## 一、标签体系

标签分四个维度，每个 issue **每个维度最多打一个**，避免标签爆炸。
维度用前缀区分，在 GitHub 标签页里按前缀排序后会自然分组。

### 1. 类型 `type:*` —— 它是什么（必填，互斥）

| 标签 | 颜色 | 含义 |
|---|---|---|
| `type: bug` | `#d73a4a` 红 | 功能不符预期 |
| `type: enhancement` | `#a2eeef` 青 | 新功能或改进 |
| `type: documentation` | `#0075ca` 蓝 | 仅文档 |
| `type: question` | `#d876e3` 紫 | 提问，可能转为讨论 |
| `type: chore` | `#ededed` 灰 | 依赖、CI、杂项 |
| `type: dependencies` | `#0366d6` 深蓝 | 依赖更新（Dependabot 自动打） |

### 2. 优先级 `P0 / P1 / P2` —— 多紧急（必填，互斥）

| 标签 | 颜色 | 判定标准 |
|---|---|---|
| `P0` | `#b60205` 深红 | 线上页面不可用、白屏、内容严重错误 |
| `P1` | `#fbca04` 黄 | 下个迭代必须解决 |
| `P2` | `#0e8a16` 绿 | 有空再做，不影响发布 |

### 3. 状态 `status:*` —— 卡在哪（可选）

| 标签 | 颜色 | 含义 |
|---|---|---|
| `status: needs-triage` | `#ededed` 灰 | 新提的，还没分类（issue 模板自动打） |
| `status: blocked` | `#5319e7` 紫 | 被外部因素阻塞，需在评论里写明等什么 |
| `status: needs-info` | `#fbca04` 黄 | 等信息，超过 14 天无回应可关闭 |
| `status: duplicate` | `#cfd3d7` 浅灰 | 重复，指向原 issue 后关闭 |
| `status: wontfix` | `#ffffff` 白 | 明确不做，需写明理由 |

### 4. 范围 `area:*` —— 归哪块（可选）

| 标签 | 颜色 | 含义 |
|---|---|---|
| `area: content` | `#c2e0c6` 浅绿 | 文案、图文素材 |
| `area: layout` | `#bfd4f2` 浅蓝 | 布局与响应式 |
| `area: a11y` | `#7057ff` 紫 | 无障碍 / 可访问性 |
| `area: ci` | `#fef2c0` 浅黄 | 工作流与自动化 |
| `area: deploy` | `#d4c5f9` 淡紫 | Pages 部署 |
| `area: dependencies` | `#0366d6` 深蓝 | 依赖与 action 版本 |

### 5. 补充标签

| 标签 | 颜色 | 含义 |
|---|---|---|
| `good first issue` | `#7057ff` 紫 | 适合外部贡献者上手 |
| `help wanted` | `#008672` 绿 | 欢迎协助 |

### 一键创建

```bash
gh label create "type: bug"          --color d73a4a --description "功能不符预期" --force
gh label create "type: enhancement"  --color a2eeef --description "新功能或改进" --force
gh label create "type: documentation" --color 0075ca --description "仅文档变更" --force
gh label create "type: question"     --color d876e3 --description "提问" --force
gh label create "type: chore"        --color ededed --description "依赖、CI、杂项" --force
gh label create "type: dependencies" --color 0366d6 --description "依赖更新" --force
gh label create "P0"                 --color b60205 --description "线上不可用，立即处理" --force
gh label create "P1"                 --color fbca04 --description "下个迭代必须解决" --force
gh label create "P2"                 --color 0e8a16 --description "有空再做" --force
gh label create "status: needs-triage" --color ededed --description "尚未分类" --force
gh label create "status: blocked"    --color 5319e7 --description "被外部因素阻塞" --force
gh label create "status: needs-info" --color fbca04 --description "等待补充信息" --force
gh label create "status: duplicate"  --color cfd3d7 --description "重复议题" --force
gh label create "status: wontfix"    --color ffffff --description "明确不做" --force
gh label create "area: content"      --color c2e0c6 --description "文案与素材" --force
gh label create "area: layout"       --color bfd4f2 --description "布局与响应式" --force
gh label create "area: a11y"         --color 7057ff --description "无障碍" --force
gh label create "area: ci"           --color fef2c0 --description "工作流与自动化" --force
gh label create "area: deploy"       --color d4c5f9 --description "Pages 部署" --force
gh label create "area: dependencies" --color 0366d6 --description "依赖与 action 版本" --force
gh label create "good first issue"   --color 7057ff --description "适合新手上手" --force
gh label create "help wanted"        --color 008672 --description "欢迎协助" --force
```

`--force` 表示已存在则更新，重复执行无副作用。

## 二、里程碑（Milestone）

里程碑回答「**排在哪一轮**」。建议按**目标**而非按时间命名，因为时间会变，目标不会。

命名格式：`v<版本> — <一句话目标>`

示例：

| 里程碑 | 目标 | 建议周期 |
|---|---|---|
| `v0.2.0 — 素材真实化` | 用真实鱼皮工艺素材替换全部 picsum 占位图 | 2 周 |
| `v0.3.0 — 移动端体验优化` | 修复小屏下导航与图集布局问题 | 2 周 |
| `v1.0.0 — 正式发布` | 内容定稿、性能达标、去除 CDN 依赖 | 1 个月 |

使用规则：

- 每个里程碑必须有**明确的完成定义**（Done Criteria），写进 description
- 一个 issue **只归属一个**里程碑；不确定的先不挂，等 triage 会再定
- 里程碑关闭时，残留 issue 必须**显式转出**到下一个里程碑，不允许遗留
- 里程碑与 release-please 的版本号不强制绑定，但建议对齐：里程碑名里的版本号即目标版本

创建：

```bash
gh api repos/OUTLElijiadong/fishskin-heritage-website/milestones \
  -f title="v0.2.0 — 素材真实化" \
  -f description="用真实鱼皮工艺素材替换全部 picsum 占位图。完成定义：index.html 中不再出现 picsum.photos 引用。" \
  -f due_on="2026-10-06T00:00:00Z"
```

## 三、项目看板（Projects）

看板回答「**现在在做什么**」。建议建一个 Project（Board 视图），列如下：

| 列 | 进入条件 | 退出条件 |
|---|---|---|
| 📥 **Inbox** | 新 issue 自动进入 | 完成 triage：补齐 type + 优先级标签 |
| 🔍 **Triage** | 已有 type 标签但尚未评估 | 已挂里程碑并指定负责人 |
| 📋 **Backlog** | 已排期，本轮不做 | 被拉入当前里程碑 |
| 🏗 **In Progress** | 有人认领并开始 | PR 已开出 |
| 👀 **In Review** | PR 已开，等待评审 | PR 已合并 |
| ✅ **Done** | PR 合并 | 自动归档（设置自动流转） |

配置建议：

1. **自动化规则**：开内置 workflow
   - Issue opened → 加到 `Inbox`
   - Issue closed → 移到 `Done`
   - PR merged → 关联的 issue 移到 `Done`
   - PR opened → 关联 issue 移到 `In Review`
2. **自定义字段**：加一个 `Priority` 单选项（P0/P1/P2），与标签保持一致，便于看板排序
3. **视图**：至少两个
   - *Board* —— 日常推进
   - *Table + 按 Milestone 分组* —— 每周检视进度
4. **Issue 与 PR 关联**：PR 描述里写 `Closes #12`，合并后 issue 自动关闭并流转

## 四、每周例行动作（单人维护时的最小版）

1. 清空 `Inbox`：每条新 issue 补齐 `type:*` + 优先级标签
2. 检查 `status: blocked` / `status: needs-info`：超过 14 天无进展就关闭并说明
3. 扫一眼当前里程碑的完成度，把不做的 issue 转出
4. 合并 release-please 的 Release PR（有新内容时）
