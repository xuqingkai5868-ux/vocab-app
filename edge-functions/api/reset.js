// ===== POST /api/reset =====
// 重置某用户进度（currentDay → 1, states → {}）
// user 只能重置自己；admin 可重置任意（body 传 userId）
// 请求体（可选）：{ userId: "gao" }

export async function onRequestPost({ request }) {
  const userId = request.headers.get('x-user-id');
  const role = request.headers.get('x-user-role');

  let body = {};
  try {
    body = await request.json();
  } catch {
    // 允许空 body
  }

  const target = (body && body.userId) || userId;

  if (role !== 'admin' && target !== userId) {
    return json({ error: 'forbidden', message: '只能重置自己的进度' }, 403);
  }

  const empty = {
    currentDay: 1,
    states: {},
    lastUpdated: Date.now()
  };

  await my_kv.put(`state:${target}`, JSON.stringify(empty));

  return json({ ok: true, userId: target, state: empty });
}

function json(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json' }
  });
}
