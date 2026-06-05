// ===== GET /api/echo =====
// 最小自检端点：不碰 my_kv，原样回显运行时上下文
// 用于验证 Edge Function 本身能跑通（区分是 Edge Function 加载问题还是 KV 绑定问题）

export async function onRequestGet() {
  return new Response(JSON.stringify({
    ok: true,
    ts: Date.now(),
    my_kv_type: typeof my_kv,
    globalNames: ['my_kv'],
    hint: 'typeof my_kv === "undefined" 时所有 API 必崩（因为 await kvGet 会抛）'
  }), {
    headers: { 'Content-Type': 'application/json; charset=utf-8' }
  });
}
