// ===== GET /api/ping =====
// 同 echo，但只返回最基本的 ping/pong，看最简路径

export async function onRequestGet() {
  return new Response(JSON.stringify({ ok: true, msg: 'pong', ts: Date.now() }), {
    headers: { 'Content-Type': 'application/json; charset=utf-8' }
  });
}
