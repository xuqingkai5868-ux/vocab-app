// ===== EdgeOne Pages Response Helper =====
// 统一 JSON 响应（CORS 头 + 中文 utf-8 + no-cache）

export function json(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: {
      'Content-Type': 'application/json; charset=utf-8',
      'Access-Control-Allow-Origin': '*',
      'Cache-Control': 'no-store'
    }
  });
}

// 从请求头提取 Bearer Token（兼容大小写）
export function getBearerToken(request) {
  const h = request.headers.get('Authorization') || '';
  const m = h.match(/^Bearer\s+(\S+)$/i);
  return m ? m[1] : null;
}
