# 电影评分网站

一个基于 React + FastAPI + SQLite 的电影评分网站，支持用户注册登录、电影浏览、评分评论和数据爬取功能。

## 技术栈

### 后端
- **FastAPI** 0.104+ - Web框架
- **SQLAlchemy** 2.0 - ORM
- **bcrypt** - 密码加密
- **Pydantic** 2.0 - 数据验证
- **requests** + **BeautifulSoup4** - 爬虫
- **pytest** - 测试框架

### 前端
- **React** 18 - UI框架
- **Vite** 5 - 构建工具
- **React Router** 6 - 路由管理
- **Axios** - HTTP客户端
- **Vitest** - 测试框架

### 数据库
- **SQLite** 3 - 轻量级数据库

## 项目结构

```
movie-rating-website/
├── backend/                  # 后端项目
│   ├── app/
│   │   ├── api/             # API路由
│   │   ├── models/          # 数据模型
│   │   ├── schemas/         # Pydantic模型
│   │   ├── services/        # 业务逻辑
│   │   ├── crawlers/        # 爬虫模块
│   │   ├── utils/           # 工具函数
│   │   ├── config.py        # 配置文件
│   │   ├── database.py      # 数据库连接
│   │   └── main.py          # FastAPI入口
│   ├── tests/               # 测试文件
│   └── requirements.txt     # 依赖列表
├── frontend/                 # 前端项目
│   ├── src/
│   │   ├── components/      # React组件
│   │   ├── pages/           # 页面组件
│   │   ├── services/        # API服务
│   │   ├── utils/           # 工具函数
│   │   ├── App.jsx          # 主应用
│   │   └── main.jsx         # 入口文件
│   ├── package.json         # 前端依赖
│   └── vite.config.js       # Vite配置
└── docs/                     # 文档
    └── superpowers/
        ├── specs/           # 设计文档
        └── plans/           # 实现计划
```

## 快速开始

### 环境要求

- Python 3.9+
- Node.js 16+
- npm 或 yarn

### 后端安装与运行

1. 安装依赖：
```bash
cd backend
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

2. 启动服务器：
```bash
uvicorn app.main:app --reload --port 8000
```

3. 访问API文档：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 前端安装与运行

1. 安装依赖：
```bash
cd frontend
npm install --registry=https://registry.npmmirror.com
```

2. 启动开发服务器：
```bash
npm run dev
```

3. 访问前端：
- http://localhost:5173

## 功能特性

### 用户功能
- ✅ 用户注册（邮箱、用户名、密码）
- ✅ 用户登录（JWT认证）
- ✅ 个人信息管理（修改密码）

### 电影功能
- ✅ 电影列表展示
- ✅ 电影详情查看
- ✅ 电影评分统计
- ✅ 电影评论列表

### 评分功能
- ✅ 用户评分（1-5星）
- ✅ 更新评分
- ✅ 查看用户评分

### 评论功能
- ✅ 发表评论
- ✅ 更新评论
- ✅ 删除评论

### 数据爬取
- ✅ 豆瓣电影爬虫
- ✅ 猫眼电影爬虫（兜底）
- ✅ 自动切换数据源

## API端点

### 认证API
- `POST /api/v1/auth/register` - 用户注册
- `POST /api/v1/auth/login` - 用户登录
- `POST /api/v1/auth/logout` - 用户登出

### 用户API
- `GET /api/v1/users/me` - 获取当前用户信息
- `PUT /api/v1/users/me/password` - 修改密码

### 电影API
- `GET /api/v1/movies` - 获取电影列表
- `GET /api/v1/movies/{movie_id}` - 获取电影详情
- `GET /api/v1/movies/{movie_id}/ratings` - 获取电影评分统计

### 评分API
- `POST /api/v1/movies/{movie_id}/ratings` - 创建评分
- `PUT /api/v1/movies/{movie_id}/ratings` - 更新评分
- `GET /api/v1/movies/{movie_id}/ratings/me` - 获取用户评分

### 评论API
- `POST /api/v1/movies/{movie_id}/comments` - 创建评论
- `GET /api/v1/movies/{movie_id}/comments` - 获取评论列表
- `PUT /api/v1/comments/{comment_id}` - 更新评论
- `DELETE /api/v1/comments/{comment_id}` - 删除评论

### 统计API
- `GET /api/v1/stats` - 获取统计信息

### 爬虫API
- `POST /api/v1/crawler/movies` - 触发电影数据爬取

## 测试

### 后端测试
```bash
cd backend
pytest --cov=app --cov-report=html
```

### 前端测试
```bash
cd frontend
npm run test:coverage
```

## 部署

### 生产环境配置

1. 后端：
```bash
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

2. 前端：
```bash
npm run build
# 使用nginx托管dist目录
```

## 开发计划

- [ ] 添加更多电影数据源
- [ ] 实现电影搜索功能
- [ ] 添加用户头像上传
- [ ] 实现评论点赞功能
- [ ] 添加电影推荐算法
- [ ] 实现邮件验证功能
- [ ] 添加管理员后台

## 贡献指南

欢迎提交Issue和Pull Request！

## 许可证

MIT License

## 联系方式

如有问题，请提交Issue或联系项目维护者。
