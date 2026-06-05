// ===== GET /api/kvtest =====
// 真打 my_kv：put → get → delete
// 用于验证 KV 命名空间是否真的注入到 Edge Function 作用域

export async function onRequestGet() {
  if (typeof my_kv === 'undefined') {
    return new Response(JSON.stringify({
      ok: false,
      error: 'my_kv_undefined',
      message: 'my_kv 全局变量在 Edge Function 作用域未注入',
      hint: '去 EdgeOne 控制台 → 命名空间管理 → 确认变量名是 "my_kv"（不是命名空间名）'
    }), {
      status: 500,
      headers: { 'Content-Type': 'application/json; charset=utf-8' }
    });
  }

  try {
    const testKey = 'test:kvtest:' + Date.now();
    await my_kv.put(testKey, 'hello-world');
    const got = await my_kv.get(testKey);
    await my_kv.delete(testKey);
    return new Response(JSON.stringify({
      ok: true,
      put_then_get: got,
      my_kv_type: typeof my_kv
    }), {
      headers: { 'Content-Type': 'application/json; charset=utf-8' }
    });
  } catch (e) {
    return new Response(JSON.stringify({
      ok: false,
      error: 'kv_call_threw',
      message: String(e && e.message || e),
      stack: String(e && e.stack || '')
    }), {
      status: 500,
      headers: { 'Content-Type': 'application/json; charset=utf-8' }
    });
  }
}
