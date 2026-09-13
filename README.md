# 鱼皮非遗文化网站

展示鱼皮制作技艺（非物质文化遗产）的单页网站，介绍鱼皮工艺的历史、作品、传承人与相关动态。

## 在线预览

直接用浏览器打开 `index.html` 即可，无需构建步骤。

本地起服务预览：

```bash
python3 -m http.server 8000
# 访问 http://localhost:8000
```

也可以开启 GitHub Pages：仓库 Settings → Pages → 选择 `main` 分支根目录。

## 页面内容

- 首页横幅：鱼皮非遗文化主题
- 工艺介绍：鱼皮工艺的历史与特点
- 作品展示：鱼皮工艺品图集
- 传承人风采：传承人介绍
- 新闻动态：相关活动信息
- 联系我们：联系方式与留言板

## 技术栈

- HTML5 + Tailwind CSS（CDN 引入）
- Font Awesome 图标
- Google Fonts（Noto Serif SC）

## 目录结构

```
├── index.html    # 网站主页面（单页）
├── 封面.jpg      # 首页横幅背景图
└── .gitignore
```

## 说明

- 作品区与传承人、新闻图片当前为占位图（picsum.photos），可在 `index.html` 中替换为真实素材。
- 页面中的人物、新闻、联系方式均为演示占位内容，非真实信息。
- 网站为响应式设计，适配桌面与移动端。

## 许可证

MIT License
