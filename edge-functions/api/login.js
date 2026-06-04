// ===== POST /api/login =====
// 4 位 PIN 登录 → 返回 token + user 信息
// 请求体：{ userId: "gao"|"di"|"admin", pin: "1234" }
// 响应：{ token, user: { id, name, role, grade? }, expiresAt }

export async function onRequestPost({ request }) {
  let body;
  try {
    body = await request.json();
  } catch {
    return json({ error: 'bad_request', message: '请求体不是合法 JSON' }, 400);
  }

  const { userId, pin } = body || {};
  if (!userId || !pin) {
    return json({ error: 'missing_credentials', message: '请输入账号和 PIN' }, 400);
  }

  // 校验 userId 格式（防注入）
  if (!/^[a-z][a-z0-9_]{0,31}$/.test(userId)) {
    return json({ error: 'invalid_user_id' }, 400);
  }

  // 查询 PIN
  const storedPin = await my_kv.get(`pin:${userId}`);
  if (!storedPin) {
    return json({ error: 'user_not_found', message: '账号不存在' }, 404);
  }

  if (storedPin !== String(pin)) {
    return json({ error: 'wrong_pin', message: 'PIN 不正确' }, 401);
  }

  // 查询用户资料
  const userRaw = await my_kv.get(`user:${userId}`);
  if (!userRaw) {
    return json({ error: 'user_not_found', message: '账号资料缺失' }, 404);
  }

  const user = JSON.parse(userRaw);

  // 生成 token
  const token = crypto.randomUUID();
  const session = {
    userId,
    role: user.role,
    expiresAt: Date.now() + 30 * 86400000  // 30 天
  };

  await my_kv.put(`session:${token}`, JSON.stringify(session));

  return json({
    token,
    user: {
      id: userId,
      name: user.name,
      role: user.role,
      grade: user.grade || null
    },
    expiresAt: session.expiresAt
  });
}

function json(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json' }
  });
}
