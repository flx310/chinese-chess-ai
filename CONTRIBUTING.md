# 开发指南

## 自动同步到GitHub

本项目已配置GitHub MCP自动上传功能。

### 本地开发后上传

在本地修改文件后，执行以下命令：

```bash
cd c:\Users\Administrator\Documents\trae_projects\flyfit\chess-game

# 查看修改
git status

# 添加所有修改
git add .

# 提交
git commit -m "描述你的修改"

# 推送到GitHub
git push
```

### 使用GitHub MCP上传

如果你有GitHub MCP访问权限，可以直接通过API更新文件：

1. 修改本地文件
2. 使用MCP的 `create_or_update_file` 功能
3. 指定文件路径和内容
4. 自动提交到仓库

### 文件结构

```
chinese-chess-ai/
├── .github/
│   └── workflows/
│       └── auto-sync.yml    # 自动同步工作流
├── index.html               # 前端主页面
├── server.py                # Flask后端
├── Elephantfish.py          # AI引擎
├── start.bat                # 启动脚本
├── README.md                # 项目说明
└── CONTRIBUTING.md          # 本文件
```

### 注意事项

- 每次修改后及时提交
- 写清楚提交信息
- 定期拉取最新代码：`git pull`
