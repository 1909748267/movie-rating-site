# 电影评分网站设计文档

**创建日期：** 2026-04-18  
**项目类型：** 中等复杂度  
**测试覆盖率目标：** 后端≥91%，前端≥85%

---

## 一、项目概述

### 1.1 项目目标
从零开发一个电影评分网站，用户可以浏览最近上映的电影、进行评分和评论。

### 1.2 核心功能
- 主页：展示最近上映电影列表
- 用户注册：邮箱、用户名、密码、确认密码（最简单实现）
- 用户登录：邮箱、密码（最简单实现）
- 个人信息管理：修改密码（最简单实现）
- 评分：用户对电影打分（1-5星）
- 评论：用户发表评论
- 关于页面：网站介绍 + 统计信息
- 数据爬取：豆瓣网（主要）+ 猫眼电影（兜底）

### 1.3 技术栈
- **前端：** React 18 + Vite 5 + React Router 6 + Axios
- **后端：** Python 3.x + FastAPI + SQLAlchemy 2.0 + bcrypt + Pydantic 2.0
- **数据库：** SQLite 3
- **爬虫：** requests + BeautifulSoup4
- **测试：** pytest + Vitest + React Testing Library

---

## 二、整体架构设计

### 2.1 架构模式
经典三层架构（前后端分离）

### 2.2 项目结构

```
movie-rating-website/
├── frontend/                 # 前端项目
│   ├── src/
│   │   ├── components/      # React组件
│   │   ├── pages/           # 页面组件
│   │   ├── services/        # API服务
│   │   ├── utils/           # 工具函数
│   │   └── App.jsx          # 主应用
│   ├── package.json
│   └── vite.config.js
├── backend/                  # 后端项目
│   ├── app/
│   │   ├── api/             # API路由
│   │   ├── models/          # 数据模型
│   │   ├── schemas/         # Pydantic模型
│   │   ├── services/        # 业务逻辑
│   │   ├── crawlers/        # 爬虫模块
│   │   └── main.py          # FastAPI入口
│   ├── tests/               # 测试文件
│   ├── requirements.txt
│   └── database.db          # SQLite数据库
└── docs/                     # 文档
    └── superpowers/
        └── specs/           # 设计文档
```

### 2.3 技术栈详细说明

**前端：**
- React 18：UI框架
- Vite 5：构建工具
- React Router 6：路由管理
- Axios：HTTP客户端
- CSS Modules：样式管理

**后端：**
- FastAPI 0.104+：Web框架
- SQLAlchemy 2.0：ORM
- bcrypt：密码加密
- Pydantic 2.0：数据验证
- requests + BeautifulSoup4：爬虫

**数据库：**
- SQLite 3：轻量级数据库

---

## 三、数据库设计

### 3.1 数据表结构

#### 3.1.1 users（用户表）
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

#### 3.1.2 movies（电影表）
```sql
CREATE TABLE movies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    poster_url TEXT,
    director TEXT,
    actors TEXT,
    genre TEXT,
    release_date TEXT,
    duration INTEGER,
    synopsis TEXT,
    source TEXT,  -- 数据来源：douban/maoyan
    source_id TEXT,  -- 来源网站的电影ID
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_movies_source ON movies(source, source_id);
```

#### 3.1.3 ratings（评分表）
```sql
CREATE TABLE ratings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    movie_id INTEGER NOT NULL,
    score INTEGER NOT NULL,  -- 1-5分
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (movie_id) REFERENCES movies(id),
    UNIQUE(user_id, movie_id)  -- 每个用户对每部电影只能评分一次
);

CREATE INDEX idx_ratings_movie ON ratings(movie_id);
```

#### 3.1.4 comments（评论表）
```sql
CREATE TABLE comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    movie_id INTEGER NOT NULL,
    content TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (movie_id) REFERENCES movies(id)
);

CREATE INDEX idx_comments_movie ON comments(movie_id);
CREATE INDEX idx_comments_user ON comments(user_id);
```

---

## 四、API接口设计

### 4.1 基础信息
- **API基础路径：** `/api/v1`
- **认证方式：** JWT Token（存储在localStorage）

### 4.2 统一响应格式

**成功响应：**
```json
{
  "code": "SUCCESS",
  "message": "操作成功",
  "data": { ... }
}
```

**错误响应：**
```json
{
  "code": "ERROR_CODE",
  "message": "中文错误提示"
}
```

### 4.3 接口列表

#### 4.3.1 用户认证接口

**POST /api/v1/auth/register**
- 功能：用户注册
- 请求体：
  ```json
  {
    "email": "user@example.com",
    "username": "username",
    "password": "password123",
    "confirm_password": "password123"
  }
  ```
- 响应：
  ```json
  {
    "code": "SUCCESS",
    "message": "注册成功",
    "data": { "user_id": 1 }
  }
  ```

**POST /api/v1/auth/login**
- 功能：用户登录
- 请求体：
  ```json
  {
    "email": "user@example.com",
    "password": "password123"
  }
  ```
- 响应：
  ```json
  {
    "code": "SUCCESS",
    "message": "登录成功",
    "data": {
      "token": "jwt_token_here",
      "user": {
        "id": 1,
        "email": "user@example.com",
        "username": "username"
      }
    }
  }
  ```

**POST /api/v1/auth/logout**
- 功能：用户登出
- 响应：
  ```json
  {
    "code": "SUCCESS",
    "message": "登出成功"
  }
  ```

#### 4.3.2 用户管理接口

**GET /api/v1/users/me**
- 功能：获取当前用户信息
- 需要认证：是
- 响应：
  ```json
  {
    "code": "SUCCESS",
    "data": {
      "id": 1,
      "email": "user@example.com",
      "username": "username",
      "created_at": "2026-04-18T10:00:00"
    }
  }
  ```

**PUT /api/v1/users/me/password**
- 功能：修改密码
- 需要认证：是
- 请求体：
  ```json
  {
    "old_password": "old_password123",
    "new_password": "new_password456",
    "confirm_password": "new_password456"
  }
  ```
- 响应：
  ```json
  {
    "code": "SUCCESS",
    "message": "密码修改成功"
  }
  ```

#### 4.3.3 电影接口

**GET /api/v1/movies**
- 功能：获取电影列表
- 查询参数：`page`（默认1），`page_size`（默认20）
- 响应：
  ```json
  {
    "code": "SUCCESS",
    "data": {
      "movies": [
        {
          "id": 1,
          "title": "电影标题",
          "poster_url": "https://...",
          "director": "导演",
          "avg_score": 4.5,
          "rating_count": 100
        }
      ],
      "total": 100,
      "page": 1,
      "page_size": 20
    }
  }
  ```

**GET /api/v1/movies/{movie_id}**
- 功能：获取电影详情
- 响应：
  ```json
  {
    "code": "SUCCESS",
    "data": {
      "id": 1,
      "title": "电影标题",
      "poster_url": "https://...",
      "director": "导演",
      "actors": "演员1, 演员2",
      "genre": "类型",
      "release_date": "2026-04-18",
      "duration": 120,
      "synopsis": "剧情简介",
      "avg_score": 4.5,
      "rating_count": 100
    }
  }
  ```

**GET /api/v1/movies/{movie_id}/ratings**
- 功能：获取电影评分统计
- 响应：
  ```json
  {
    "code": "SUCCESS",
    "data": {
      "avg_score": 4.5,
      "count": 100
    }
  }
  ```

**GET /api/v1/movies/{movie_id}/comments**
- 功能：获取电影评论列表
- 查询参数：`page`（默认1），`page_size`（默认20）
- 响应：
  ```json
  {
    "code": "SUCCESS",
    "data": {
      "comments": [
        {
          "id": 1,
          "user_id": 1,
          "username": "username",
          "content": "评论内容",
          "created_at": "2026-04-18T10:00:00"
        }
      ],
      "total": 50,
      "page": 1,
      "page_size": 20
    }
  }
  ```

#### 4.3.4 评分接口

**POST /api/v1/movies/{movie_id}/ratings**
- 功能：提交评分
- 需要认证：是
- 请求体：
  ```json
  {
    "score": 5
  }
  ```
- 响应：
  ```json
  {
    "code": "SUCCESS",
    "message": "评分成功"
  }
  ```

**PUT /api/v1/movies/{movie_id}/ratings**
- 功能：更新评分
- 需要认证：是
- 请求体：
  ```json
  {
    "score": 4
  }
  ```
- 响应：
  ```json
  {
    "code": "SUCCESS",
    "message": "评分更新成功"
  }
  ```

**GET /api/v1/movies/{movie_id}/ratings/me**
- 功能：获取当前用户的评分
- 需要认证：是
- 响应：
  ```json
  {
    "code": "SUCCESS",
    "data": {
      "score": 5
    }
  }
  ```

#### 4.3.5 评论接口

**POST /api/v1/movies/{movie_id}/comments**
- 功能：发表评论
- 需要认证：是
- 请求体：
  ```json
  {
    "content": "这是一条评论"
  }
  ```
- 响应：
  ```json
  {
    "code": "SUCCESS",
    "message": "评论成功"
  }
  ```

**PUT /api/v1/comments/{comment_id}**
- 功能：更新评论
- 需要认证：是
- 请求体：
  ```json
  {
    "content": "这是更新后的评论"
  }
  ```
- 响应：
  ```json
  {
    "code": "SUCCESS",
    "message": "评论更新成功"
  }
  ```

**DELETE /api/v1/comments/{comment_id}**
- 功能：删除评论
- 需要认证：是
- 响应：
  ```json
  {
    "code": "SUCCESS",
    "message": "评论删除成功"
  }
  ```

#### 4.3.6 统计接口

**GET /api/v1/stats**
- 功能：获取网站统计信息
- 响应：
  ```json
  {
    "code": "SUCCESS",
    "data": {
      "movie_count": 100,
      "user_count": 50,
      "comment_count": 200
    }
  }
  ```

---

## 五、前端页面设计

### 5.1 页面路由

```
/                    # 主页 - 最近上映电影列表
/login               # 登录页面
/register            # 注册页面
/profile             # 个人信息页面（修改密码）
/movie/:id           # 电影详情页（包含评分和评论）
/about               # 关于页面
```

### 5.2 页面组件结构

#### 5.2.1 主页
- **导航栏组件：** Logo、登录/注册按钮、用户信息
- **电影列表组件：** 展示电影卡片（海报、标题、导演、评分）
- **分页组件：** 支持翻页

#### 5.2.2 登录页面
- **登录表单组件：** 邮箱、密码输入框
- **表单验证：** 前端基础验证
- **错误提示组件：** 显示后端返回的错误信息

#### 5.2.3 注册页面
- **注册表单组件：** 邮箱、用户名、密码、确认密码
- **表单验证：** 前端基础验证
- **错误提示组件**

#### 5.2.4 个人信息页面
- **密码修改表单：** 旧密码、新密码、确认密码
- **用户信息展示：** 邮箱、用户名、注册时间

#### 5.2.5 电影详情页
- **电影信息组件：** 海报、标题、导演、演员、简介等
- **评分组件：** 星级评分（1-5星）
- **评论列表组件：** 显示所有评论
- **评论表单组件：** 发表评论

#### 5.2.6 关于页面
- **网站介绍文本**
- **统计信息展示：** 电影总数、用户总数、评论总数

### 5.3 通用组件
- **Header：** 顶部导航栏
- **Footer：** 底部信息
- **Loading：** 加载状态
- **ErrorBoundary：** 错误边界
- **PrivateRoute：** 私有路由（需要登录才能访问）
- **Toast：** 消息提示组件

---

## 六、数据爬取设计

### 6.1 爬虫模块架构

```
backend/app/crawlers/
├── base_crawler.py      # 爬虫基类
├── douban_crawler.py    # 豆瓣爬虫
├── maoyan_crawler.py    # 猫眼爬虫
└── crawler_manager.py   # 爬虫管理器
```

### 6.2 爬取策略

#### 6.2.1 豆瓣爬虫（主要数据源）
- **目标URL：** `https://movie.douban.com/cinema/nowplaying/`
- **爬取内容：** 电影标题、海报、导演、演员、类型、上映日期、时长、简介
- **反爬策略：**
  - 设置User-Agent模拟浏览器
  - 添加随机延迟（1-3秒）
  - 使用Session保持连接
- **数据解析：** BeautifulSoup解析HTML

#### 6.2.2 猫眼爬虫（兜底数据源）
- **目标URL：** `https://maoyan.com/films`
- **爬取内容：** 与豆瓣相同字段
- **反爬策略：** 同豆瓣
- **数据解析：** BeautifulSoup解析HTML

#### 6.2.3 爬虫管理器
- **优先级策略：** 豆瓣 > 猫眼
- **失败重试：** 最多重试3次
- **数据去重：** 根据source和source_id判断是否已存在
- **更新策略：** 每日定时更新电影数据

### 6.3 爬取流程

```
1. 启动爬虫管理器
2. 尝试豆瓣爬虫
   - 成功：保存数据到数据库
   - 失败：记录日志，尝试猫眼爬虫
3. 猫眼爬虫
   - 成功：保存数据到数据库
   - 失败：记录错误日志
4. 数据清洗和去重
5. 更新数据库
```

### 6.4 数据字段映射

```python
{
    "title": "电影标题",
    "poster_url": "海报图片URL",
    "director": "导演",
    "actors": "演员列表",
    "genre": "类型",
    "release_date": "上映日期",
    "duration": "时长（分钟）",
    "synopsis": "剧情简介",
    "source": "douban/maoyan",
    "source_id": "来源网站的电影ID"
}
```

### 6.5 错误处理

- **网络超时：** 记录日志，返回空列表
- **解析失败：** 记录日志，跳过该电影
- **数据不完整：** 保存已有字段，缺失字段设为None

---

## 七、错误处理设计

### 7.1 后端错误处理

#### 7.1.1 错误代码定义

```python
SUCCESS = "SUCCESS"
ERROR_INVALID_INPUT = "INVALID_INPUT"
ERROR_UNAUTHORIZED = "UNAUTHORIZED"
ERROR_FORBIDDEN = "FORBIDDEN"
ERROR_NOT_FOUND = "NOT_FOUND"
ERROR_DUPLICATE_EMAIL = "DUPLICATE_EMAIL"
ERROR_DUPLICATE_USERNAME = "DUPLICATE_USERNAME"
ERROR_WRONG_PASSWORD = "WRONG_PASSWORD"
ERROR_PASSWORD_MISMATCH = "PASSWORD_MISMATCH"
ERROR_ALREADY_RATED = "ALREADY_RATED"
ERROR_INTERNAL = "INTERNAL_ERROR"
```

#### 7.1.2 错误处理中间件

```python
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={
            "code": "INTERNAL_ERROR",
            "message": "服务器内部错误"
        }
    )
```

#### 7.1.3 验证错误处理

```python
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={
            "code": "INVALID_INPUT",
            "message": "输入数据格式错误"
        }
    )
```

### 7.2 前端错误处理

#### 7.2.1 Axios拦截器

```javascript
axios.interceptors.response.use(
  response => response.data,
  error => {
    const message = error.response?.data?.message || "网络错误";
    showError(message);
    return Promise.reject(error);
  }
);
```

#### 7.2.2 错误提示组件
- 使用Toast或Alert组件显示错误信息
- 自动消失（3秒后）
- 支持多个错误堆叠显示

#### 7.2.3 表单验证错误
- **实时验证：** 输入时即时反馈
- **提交验证：** 提交前统一验证
- **错误信息显示：** 显示在对应字段下方

#### 7.2.4 认证错误处理
- **401错误：** 自动跳转到登录页
- **Token过期：** 清除本地存储，跳转登录页
- **权限不足：** 显示403错误页面

---

## 八、测试策略设计

### 8.1 测试覆盖率目标
- **后端：** ≥91%（中等任务）
- **前端：** ≥85%（简单任务）

### 8.2 后端测试（pytest）

#### 8.2.1 单元测试

```
tests/
├── test_models.py          # 数据模型测试
├── test_schemas.py         # Pydantic模型测试
├── test_services/          # 业务逻辑测试
│   ├── test_auth_service.py
│   ├── test_movie_service.py
│   ├── test_rating_service.py
│   └── test_comment_service.py
└── test_crawlers/          # 爬虫测试
    ├── test_douban_crawler.py
    └── test_maoyan_crawler.py
```

#### 8.2.2 集成测试

```
tests/
├── test_api/               # API端点测试
│   ├── test_auth_api.py
│   ├── test_user_api.py
│   ├── test_movie_api.py
│   ├── test_rating_api.py
│   └── test_comment_api.py
└── test_db.py              # 数据库测试
```

#### 8.2.3 测试策略
- 使用pytest作为测试框架
- 使用pytest-cov测量覆盖率
- 使用测试数据库（内存SQLite）
- Mock外部依赖（爬虫请求）
- TDD流程：RED-GREEN-REFACTOR

### 8.3 前端测试（Vitest + React Testing Library）

#### 8.3.1 组件测试

```
frontend/src/
├── components/__tests__/
│   ├── Header.test.jsx
│   ├── MovieCard.test.jsx
│   └── Rating.test.jsx
└── pages/__tests__/
    ├── Home.test.jsx
    ├── Login.test.jsx
    └── MovieDetail.test.jsx
```

#### 8.3.2 集成测试

```
frontend/src/
└── __tests__/
    ├── auth.test.jsx       # 认证流程测试
    └── rating.test.jsx     # 评分流程测试
```

#### 8.3.3 测试策略
- 使用Vitest作为测试运行器
- 使用React Testing Library测试组件
- 使用MSW（Mock Service Worker）模拟API
- 测试用户交互和状态变化
- 测试错误处理和边界情况

### 8.4 TDD执行流程

#### 8.4.1 RED阶段
1. 编写失败的测试用例
2. 运行测试，确认失败

#### 8.4.2 GREEN阶段
1. 编写最小代码使测试通过
2. 运行测试，确认通过

#### 8.4.3 REFACTOR阶段
1. 重构代码，优化结构
2. 运行测试，确保仍然通过

### 8.5 测试覆盖率检查

```bash
# 后端
pytest --cov=app --cov-report=html --cov-fail-under=91

# 前端
npm run test -- --coverage --coverage.thresholds.global.lines=85
```

---

## 九、依赖管理

### 9.1 前端依赖（package.json）

```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.20.0",
    "axios": "^1.6.0"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.2.0",
    "vite": "^5.0.0",
    "vitest": "^1.0.0",
    "@testing-library/react": "^14.1.0",
    "@testing-library/jest-dom": "^6.1.0",
    "msw": "^2.0.0"
  }
}
```

### 9.2 后端依赖（requirements.txt）

```
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
pydantic==2.5.0
pydantic-settings==2.1.0
bcrypt==4.1.1
python-jose[cryptography]==3.3.0
requests==2.31.0
beautifulsoup4==4.12.2
lxml==4.9.3
pytest==7.4.3
pytest-cov==4.1.0
pytest-asyncio==0.21.1
httpx==0.25.2
```

### 9.3 依赖安装命令

```bash
# 前端（使用淘宝镜像）
npm config set registry https://registry.npmmirror.com
npm install

# 后端（使用清华源）
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

---

## 十、安全设计

### 10.1 密码安全
- 使用bcrypt进行密码哈希
- 密码强度要求：至少6位
- 密码确认：注册和修改密码时需要确认

### 10.2 认证安全
- 使用JWT进行身份认证
- Token存储在localStorage
- Token过期时间：7天
- 敏感操作需要验证Token

### 10.3 数据安全
- SQL注入防护：使用SQLAlchemy ORM
- XSS防护：React自动转义
- CSRF防护：JWT Token认证

### 10.4 API安全
- 需要认证的接口验证Token
- 用户只能修改自己的评论
- 用户只能更新自己的评分

---

## 十一、部署设计

### 11.1 开发环境
- 前端：`npm run dev`（端口5173）
- 后端：`uvicorn app.main:app --reload`（端口8000）
- 数据库：SQLite文件（database.db）

### 11.2 生产环境
- 前端：构建静态文件，使用Nginx托管
- 后端：使用Gunicorn + Uvicorn
- 数据库：SQLite文件（需要定期备份）

### 11.3 环境变量
```
# 后端
DATABASE_URL=sqlite:///./database.db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_DAYS=7
```

---

## 十二、开发计划

### 12.1 开发阶段划分

**阶段一：项目初始化**
- 创建项目结构
- 配置开发环境
- 设置依赖管理

**阶段二：数据库设计与实现**
- 创建数据库模型
- 实现数据库迁移
- 编写数据库测试

**阶段三：后端核心功能**
- 实现用户认证
- 实现电影管理
- 实现评分和评论
- 编写API测试

**阶段四：数据爬取**
- 实现豆瓣爬虫
- 实现猫眼爬虫
- 实现爬虫管理器
- 编写爬虫测试

**阶段五：前端开发**
- 创建页面组件
- 实现路由配置
- 集成API调用
- 编写组件测试

**阶段六：集成测试与优化**
- 前后端集成测试
- 性能优化
- 错误处理完善
- 测试覆盖率达标

**阶段七：部署与交付**
- 生产环境配置
- 部署验证
- 文档完善
- 最终交付

---

## 十三、验收标准

### 13.1 功能验收
- 用户可以注册、登录、修改密码
- 主页显示最近上映电影列表
- 用户可以对电影评分和评论
- 关于页面显示统计信息
- 数据爬取功能正常工作

### 13.2 质量验收
- 后端测试覆盖率≥91%
- 前端测试覆盖率≥85%
- 所有测试通过
- 代码符合规范

### 13.3 性能验收
- 页面加载时间<3秒
- API响应时间<500ms
- 支持至少100个并发用户

### 13.4 安全验收
- 密码使用bcrypt加密
- API接口有认证保护
- 无SQL注入、XSS等安全漏洞

---

## 十四、风险与应对

### 14.1 技术风险
- **风险：** 爬虫被反爬机制阻止
- **应对：** 多数据源兜底，降低请求频率

### 14.2 时间风险
- **风险：** 测试覆盖率难以达标
- **应对：** 优先编写核心功能测试，逐步完善

### 14.3 兼容性风险
- **风险：** 不同浏览器兼容性问题
- **应对：** 使用标准Web技术，测试主流浏览器

---

## 十五、总结

本设计文档详细描述了电影评分网站的架构设计、数据库设计、API设计、前端设计、爬虫设计、错误处理、测试策略等各个方面。项目采用经典三层架构，前后端分离，使用React + FastAPI + SQLite技术栈，遵循TDD开发流程，确保代码质量和测试覆盖率。

项目将按照七个阶段逐步实施，每个阶段都有明确的目标和验收标准。通过严格的质量控制和风险管理，确保项目按时高质量交付。
