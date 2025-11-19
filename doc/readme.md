# 一、登陆页面

login.html

## 1、HTML结构

```html
<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>登录 - 标注系统</title>
  ...
</head>
<body>
  ...
</body>
</html>
```

- `<!doctype html>`：声明 HTML5 文档类型。

- `<html lang="zh-CN">`：网页语言为中文。

- `<meta charset="utf-8">`：指定页面使用 UTF-8 编码。

- `<meta name="viewport" ...>`：让页面在移动设备上自适应缩放。

- `<title>`：网页标题显示在浏览器标签。

## 2、CSS 样式

```css
body {
  margin: 0;
  font-family: "Helvetica Neue", Arial, sans-serif;
  background: #f6f8fb;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}
```

- 去掉默认 margin，设置全局字体。

- `display: flex; justify-content: center; align-items: center; height: 100vh;`  
  让登录框居中显示在屏幕中央，无论屏幕大小。

```css
.card {
  background: #fff;
  padding: 32px;
  border-radius: 12px;
  box-shadow: 0 6px 24px rgba(0,0,0,0.08);
  width: 100%;
  max-width: 400px;
}
```

- `.card` 是登录表单的容器，白色背景，圆角，阴影，最大宽度 400px。

- `padding: 32px` 给内部元素留出空间。

```css
label { display: block; margin-bottom: 4px; font-size: 14px; color: #374151; }
input[type="text"], input[type="password"] {
  width: 100%; padding: 10px; margin-bottom: 16px;
  border-radius: 8px; border: 1px solid #e6e9ef; font-size: 14px;
}
button {
  width: 100%; padding: 12px;
  border: none; border-radius: 8px;
  background: #2563eb; color: #fff;
  font-weight: 600; font-size: 16px;
  cursor: pointer;
}
.error { color: #ef4444; font-size: 13px; margin-bottom: 12px; display: none; }

```

- `label` 标签独占一行并带小间距。

- 输入框 `input` 宽度 100%，圆角，边框浅灰，字体舒适。

- 按钮 `button` 蓝色，白字，圆角。

- `.error` 用于显示错误信息，默认隐藏 `display: none`。

## 3、HTML 表单主体

```html
<div class="card">
  <h1>登录标注系统</h1>
  <div id="err" class="error"></div>
  <form id="loginForm">
    <label for="username">用户名</label>
    <input type="text" id="username" name="username" placeholder="请输入用户名" required>
    <label for="password">密码</label>
    <input type="password" id="password" name="password" placeholder="请输入密码" required>
    <button type="submit">登录</button>
  </form>
  <p style="margin-top:12px; font-size:12px; color:#6b7280;">示例账号：<strong>admin</strong> / <strong>pass</strong></p>
</div>

```

- `.card` 容器里有标题 `<h1>`。

- `<div id="err" class="error"></div>`：用于显示登录错误提示。

- `<form id="loginForm">`：表单，包含用户名和密码输入框。

- `required`：浏览器自带验证，不能为空。

- `<button type="submit">`：点击提交表单。

- `<p>`：提示示例账号信息。

具体说明：

①容器卡片

```
<div class="card">
```

- 作为整个登录组件的容器

- 通过 CSS 类 `card` 来设置样式（圆角、阴影、背景色等）

②系统标题

```
<h1>登录标注系统</h1>
```

- 显示系统名称

- `<h1>` 标签表示最重要的标题

③错误信息区域

```
<div id="err" class="error"></div>
```

- `id="err"` - 用于 JavaScript 操作

- `class="error"` - 用于 CSS 样式（通常为红色文字）

- 初始为空，登录失败时显示错误信息

④登录表单

```
<form id="loginForm">
```

- `id="loginForm"` - 用于 JavaScript 表单提交处理

- 包含所有输入字段和提交按钮

⑤用户名输入

```
<label for="username">用户名</label>
<input type="text" id="username" name="username" placeholder="请输入用户名" required>
```

- `<label>` 关联输入框，提高可访问性

- `type="text"` - 文本输入框

- `name="username"` - 表单字段名称，用于后端接收数据

- `placeholder` - 输入框提示文字

- `required` - 必填字段验证

⑥密码输入

```
<label for="password">密码</label>
<input type="password" id="password" name="password" placeholder="请输入密码" required>
```

- `type="password"` - 密码输入框（显示为圆点）

- 其他属性与用户名输入类似

⑦登录按钮

```
<button type="submit">登录</button>
```

- `type="submit"` - 表单提交按钮

- 点击后触发表单的提交事件

⑧示例账号提示

```
<p style="margin-top:12px; font-size:12px; color:#6b7280;">
    示例账号：<strong>admin</strong> / <strong>pass</strong>
</p>
```

- 内联样式设置外观

- 提供测试用的账号密码

- `<strong>` 标签突出显示账号信息

## 4、js逻辑

```javascript
// 获取表单和错误显示元素
const form = document.getElementById('loginForm');
const errDiv = document.getElementById('err');

// 添加表单提交事件监听
form.addEventListener('submit', async (e) => {
  e.preventDefault();  // 阻止表单默认提交行为
  errDiv.style.display = 'none';  // 隐藏之前的错误信息

  // 准备提交数据
  const payload = {
    username: form.username.value.trim(),  // 去除用户名前后空格
    password: form.password.value          // 密码保持原样
  };

  try {
    // 发送登录请求到服务器
    const res = await fetch('/login', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify(payload)  // 将对象转为JSON字符串
    });
    
    // 解析服务器返回的JSON数据
    const j = await res.json();

    // 检查HTTP状态码是否成功
    if (!res.ok) {
      errDiv.innerText = j.message || '登录失败';
      errDiv.style.display = 'block';
      return;  // 登录失败，停止执行
    }

    // 登录成功，保存认证信息到本地存储
    localStorage.setItem('auth_token', j.token);
    localStorage.setItem('auth_user', JSON.stringify(j.user || {}));

    // 跳转到首页
    window.location.href = '/';
    
  } catch (err) {
    // 处理网络错误或其他异常
    errDiv.innerText = '网络错误: ' + (err.message || err);
    errDiv.style.display = 'block';
  }
});
```

# 二、 Flask 应用

## 1、初始化应用

app/\__init__.py

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

# 1. 初始化扩展（但不绑定应用）
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    # 2. 创建Flask应用实例
    app = Flask(__name__, template_folder='templates')
    
    # 3. 配置应用
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'dev_secret'
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///demo.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 4. 初始化扩展并绑定到应用
    db.init_app(app)
    migrate.init_app(app, db)

    # 5. 注册蓝图
    from app.auth import auth_bp
    app.register_blueprint(auth_bp)

    # 6. 定义路由
    @app.route('/')
    def index():
        return "<h2>登录成功！这里是首页（上传页面占位）</h2>"

    return app
```

### 1、导入和扩展初始化

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy  # 数据库ORM
from flask_migrate import Migrate        # 数据库迁移工具
import os                                # 操作系统接口，用于读取环境变量

# 在函数外创建扩展实例（不绑定特定应用）
db = SQLAlchemy()
migrate = Migrate()
```

- **扩展分离**: 扩展实例在函数外创建，支持多个应用实例

- **延迟绑定**: 扩展在 `create_app()` 中才绑定到具体应用

### 2、应用工厂函数

```py
def create_app():
```

- **工厂模式**: 创建和配置Flask应用的函数

- **优势**:
  
  - 支持创建多个应用实例（测试、开发、生产）
  
  - 延迟配置，更灵活
  
  - 便于单元测试

### 3、应用配置

```py
app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'dev_secret'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///demo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
```

- **SECRET_KEY**:
  
  - 用途：会话加密、CSRF保护、Flash消息等
  
  - 优先级：环境变量 > 默认值 'dev_secret'

- **SQLALCHEMY_DATABASE_URI**:
  
  - 格式：`数据库类型://用户名:密码@主机:端口/数据库名`
  
  - 默认：SQLite 数据库文件 `demo.db`

- **SQLALCHEMY_TRACK_MODIFICATIONS**:
  
  - 设为 False 避免性能警告
  
  - 不需要对象修改跟踪时可关闭

### 4、扩展初始化

```js
db.init_app(app)
migrate.init_app(app, db)
```

- **db.init_app(app)**: 将数据库实例绑定到Flask应用

- **migrate.init_app(app, db)**: 初始化数据库迁移工具

### 5、蓝图注册

```py
from app.auth import auth_bp
app.register_blueprint(auth_bp)
```

- **模块化设计**: 将认证相关路由放在单独的蓝图

- **文件结构**
  
  app/
    __init__.py    # 这个文件
    auth.py        # 包含 auth_bp 蓝图

### 6、路由定义

```py
@app.route('/')
def index():
    return "<h2>登录成功！这里是首页（上传页面占位）</h2>"
```

- **占位页面**: 登录成功后的跳转目标

- **实际应用**: 这里应该是一个完整的上传页面

## 2、数据库处理

```py
from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash

class User(db.Model):
    # 1. 表字段定义
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password_hash = db.Column(db.String(200))
    role = db.Column(db.String(20), default='annotator')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 2. 密码管理方法
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password_hash, password)
```

### 1、导入依赖

```py
from app import db              # 数据库实例
from datetime import datetime   # 时间处理
from werkzeug.security import generate_password_hash  # 密码加密
```

### 2、 数据表字段定义

**id - 主键**

```
id = db.Column(db.Integer, primary_key=True)
```

- 类型：整数

- 作用：唯一标识每个用户

- 自动递增

**username - 用户名**

```py
username = db.Column(db.String(50), unique=True)
```

- 类型：字符串，最大长度50

- `unique=True`：用户名必须唯一，不能重复

- 用途：用户登录标识

**password_hash - 密码哈希**

```
password_hash = db.Column(db.String(200))
```

- 类型：字符串，长度200（存储加密后的密码）

- **安全设计**：不存储明文密码

- 长度200：适应不同的哈希算法输出

**role - 用户角色**

```
role = db.Column(db.String(20), default='annotator')
```

- 类型：字符串，最大长度20

- `default='annotator'`：默认角色为标注员

- 可能的角色：`admin`, `annotator`, `reviewer` 等

**created_at - 创建时间**

```
created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

- 类型：日期时间

- `default=datetime.utcnow`：自动设置创建时间为当前UTC时间

- 注意：`utcnow` 后面没有 `()`，SQLAlchemy 会在插入时自动调用

### 3、 密码管理方法

**设置密码**

```py
def set_password(self, password):
    self.password_hash = generate_password_hash(password)
```

- 使用 Werkzeug 的密码哈希功能

- 自动处理盐值(salt)和加密迭代次数

- 每次调用都会生成不同的哈希值（即使密码相同）

**验证密码**

```py
def check_password(self, password):
    from werkzeug.security import check_password_hash
    return check_password_hash(self.password_hash, password)
```

- 比较输入的密码与存储的哈希值

- 动态导入：避免循环导入问题

- 返回布尔值：`True`（密码正确）或 `False`（密码错误）

## 3、Flask认证

```py
from flask import Blueprint, request, jsonify
from app.models import User
from app import db
import jwt
from flask import current_app
from datetime import datetime, timedelta

# 1. 创建认证蓝图
auth_bp = Blueprint('auth', __name__)

# 2. Token 生成函数
def create_token(user):
    payload = {
        'user_id': user.id,
        'username': user.username,
        'role': user.role,
        'exp': datetime.utcnow() + timedelta(hours=2)
    }
    token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
    return token

# 3. 登录路由
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message':'用户名和密码必填'}), 400

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({'message':'用户名或密码错误'}), 401

    token = create_token(user)
    return jsonify({'token': token, 'user': {'id': user.id, 'username': user.username, 'role': user.role}})
```


