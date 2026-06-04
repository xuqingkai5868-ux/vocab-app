// ===== GET /api/me =====
// 返回当前登录用户的资料
// 响应：{ user: { id, name, role, grade? } }

export async function onRequestGet({ request }) {
  const userId = request.headers.get('x-user-id');
  const role = request.headers.get('x-user-role');

  const userRaw = await my_kv.get(`user:${userId}`);
  if (!userRaw) {
    return json({ error: 'user_not_found' }, 404);
  }

  const u = JSON.parse(userRaw);
  return json({
    user: {
      id: userId,
      name: u.name,
      role: u.role,
      grade: u.grade || null
    }
  });
}

function json(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json' }
  });
}
