# 部署到 Vercel 完整指南

> 适用：暑假共学背单词系统（3 账号 PIN 鉴权 + 1447 词 + 83 天计划）
> 部署目标：拿到 `https://eustudy.vercel.app` 这种永久可访问的 URL
> 预计耗时：30 分钟（你 + 我一起做）

---

## 你需要做的事（6 步，每步 1-3 分钟）

### Step 1：注册 Vercel 账号
- 打开 https://vercel.com/signup
- **建议用 GitHub 登录**（后面部署直接绑 repo，最省事）
- 不用绑卡，free tier 完全够用

### Step 2：创建 Vercel KV 数据库
- 登录后 → 顶部导航「Storage」→ 「Create Database」→ 选 「KV」
- 名字随便起，比如 `vocab-kv`
- Region 选 **`Washington, D.C., USA (iad1)`**（对中国大陆延迟最低）
- 点 Create → 完成后会看到 KV 详情页

### Step 3：创建 Vercel 项目 + 绑 KV
- 顶部导航 「Add New...」→ 「Project」
- 如果你用 GitHub 登录 → 选 `Import Git Repository` → 把 vocab-app 推到 GitHub 后选这个 repo
- 如果你不想用 Git → 选 「Browse All Templates」→ 「Blank」
- 创建后进项目设置 → 「Storage」 tab → 「Connect Store」→ 选刚才创建的 `vocab-kv`
- **关键**：连接后 Vercel 会自动注入 3 个环境变量：
  - `KV_URL`
  - `KV_REST_API_URL`
  - `KV_REST_API_TOKEN`
  - `KV_REST_API_READ_ONLY_TOKEN`

> **如果不用 Git（手动部署）**：
> - 把整个 `vocab-app/` 目录压缩成 zip（不含 node_modules）
> - 在 Vercel 项目页 → 「Deployments」 tab → 拖拽 zip 上传
> - 第一次会让你登录，授权完自动部署

### Step 4：执行命令部署
打开 PowerShell（在 `vocab-app/` 目录下）：

```bash
npm install
npx vercel login          # 第一次会跳浏览器授权
npx vercel                # 部署到 preview 环境（自动分配一个 url）
npx vercel --prod         # 部署到 production（拿到 *.vercel.app 永久域名）
```

> 第一次执行 `npx vercel` 时会问几个问题：
> - Set up and deploy? → **Y**
> - Which scope? → 选你的账号
> - Link to existing project? → **N**（第一次）
> - What's your project's name? → 输入 `eustudy`（这决定你的 URL：eustudy.vercel.app）
> - In which directory is your code located? → 直接回车（默认 ./）
> - Want to modify these settings? → **N**

### Step 5：初始化 3 账号（一次性的）
部署完成后浏览器打开 `https://eustudy.vercel.app/api/seed` 看一眼——应该返回 401 unauthorized（正常的，seed 是 POST 不是 GET）。

然后在 PowerShell 里跑：

```bash
curl -X POST https://eustudy.vercel.app/api/seed `
  -H "Content-Type: application/json" `
  -d '{
    "users": {
      "gao":   { "name": "哥哥", "role": "user", "grade": "高一" },
      "di":    { "name": "弟弟", "role": "user", "grade": "三年级" },
      "admin": { "name": "管理员", "role": "admin" }
    },
    "pins": { "gao": "1234", "di": "5678", "admin": "9999" }
  }'
```

返回 `{"ok":true,"seeded":["gao","di","admin"],"overwritten":false}` = 成功。

### Step 6：测试 3 账号
浏览器打开 `https://eustudy.vercel.app`：
- 选「哥哥」→ PIN `1234` → 应该进首页，看到 day 1
- 右上角切「弟弟」→ PIN `5678`
- 切「管理员」→ PIN `9999` → 应该能看到所有人的进度
- 标几个词为「掌握」→ 关浏览器 → 再打开同一个账号 → 进度应保留（证明云端 KV 存住了）

---

## 常见问题

### Q：KV 里的数据能存多久？
A：永久保留（除非你手动删 KV 实例）。free tier 限额：256MB 存储 + 10 万命令/天，对 3 个孩子的进度（< 1MB）足够用到 2030 年。

### Q：怎么换 PIN？
A：浏览器开无痕窗口 → 用 admin PIN `9999` 登录 → 进设置（暂未做 UI）→ 改用 seed 重置：
```bash
curl -X POST https://eustudy.vercel.app/api/seed -H "Content-Type: application/json" -d '{ "users": {...}, "pins": {...}, "adminConfirmPin": "9999" }'
```

### Q：怎么删一个账号？
A：进 Vercel 控制台 → Storage → vocab-kv → 找到 `user:xxx` / `pin:xxx` / `state:xxx` 三个 key → Delete。

### Q：本地的 cloudflared tunnel 还要保留吗？
A：**不用了**。Vercel 是真云，关电脑也照常工作。tunnel 是个保底方案，留着不碍事（不占资源）。

### Q：以后改前端要重新部署？
A：是的。`npx vercel --prod` 一次。30 秒生效。

### Q：以后加新词要重新部署吗？
A：要。前端 `index.html` 嵌入了 SCHEDULE 数组（83 天词表），改词表就要重新构建+部署。或者改造为从 `/api/schedule` 动态拉取（这是后续优化，不在当前范围）。

---

## 当前项目结构

```
vocab-app/
├── api/                       ← Vercel Functions（6 个端点 + 3 个 lib）
│   ├── _lib/
│   │   ├── kv.js              ← @vercel/kv 封装
│   │   ├── respond.js         ← JSON 响应工具
│   │   └── verifyToken.js     ← Bearer token 验证
│   ├── login.js
│   ├── me.js
│   ├── state.js
│   ├── summary.js
│   ├── reset.js
│   └── seed.js
├── index.html                 ← 前端单页（直接放 Vercel 静态托管）
├── package.json               ← 依赖：@vercel/kv
├── vercel.json                ← Vercel 路由/构建配置
├── plan-完整计划.md           ← 83 天词表（嵌入到 index.html）
├── 部署指南-Vercel.md         ← 本文件
└── 部署指南.md                ← 旧 EdgeOne 指南（保留备查）
```

> 旧 `edge-functions/` 目录和 `local-server.js` 已废弃（保留备查，不影响 Vercel 部署）。
