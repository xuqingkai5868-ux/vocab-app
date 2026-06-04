// ===== GET /api/summary =====
// 返回所有用户进度概览，按角色过滤敏感度：
//   admin → 看所有人的 full state（含 currentDay）
//   user  → 看自己 full + 看别人百分比（mastered/fuzzy 计数 → 客户端算百分比）
//
// 响应：{ [userId]: { name, role, mastered, fuzzy, currentDay? } }

export async function onRequestGet({ request }) {
  const userId = request.headers.get('x-user-id');
  const role = request.headers.get('x-user-role');

  // 列出所有 user:* 记录
  const userList = await my_kv.list({ prefix: 'user:' });

  const result = {};
  for (const k of userList.keys) {
    const id = k.name.replace('user:', '');
    const u = JSON.parse(await my_kv.get(k.name));

    const stateRaw = await my_kv.get(`state:${id}`);
    const state = stateRaw ? JSON.parse(stateRaw) : { currentDay: 1, states: {} };

    const mastered = Object.values(state.states || {}).filter(s => s === 'mastered').length;
    const fuzzy = Object.values(state.states || {}).filter(s => s === 'fuzzy').length;

    const isSelf = id === userId;
    const isAdmin = role === 'admin';

    result[id] = {
      name: u.name,
      role: u.role,
      mastered,
      fuzzy,
      // currentDay 仅 admin 或 自己可见
      currentDay: (isAdmin || isSelf) ? (state.currentDay || 1) : null
    };
  }

  return json(result);
}

function json(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json' }
  });
}
