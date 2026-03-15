# 楚汉棋局 - 中国象棋人机对战

一款功能完整、规则严谨的中国象棋人机对弈应用，集成 Elephantfish.py AI 引擎。

## 功能特性

- 标准中国象棋规则（将帅照面、长将限制等）
- 四级AI难度（入门/普通/困难/大师）
- 完整音效系统（拿棋、下棋、吃子、将军、BGM）
- 悔棋功能
- 响应式布局

## 启动方式

```bash
# 安装依赖
pip install flask flask-cors

# 启动后端
python server.py

# 启动前端（新终端）
python -m http.server 8080
```

访问 http://localhost:8080

## 技术栈

- 前端：HTML5 Canvas + JavaScript
- 后端：Python Flask
- AI引擎：Elephantfish.py
