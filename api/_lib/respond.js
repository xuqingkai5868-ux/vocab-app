// 统一 JSON 响应 + Bearer token 解析
// Vercel Node.js Functions 共用工具

export function json(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json; charset=utf-8' }
  });
}

export function getBearerToken(req) {
  const auth = req.headers.get('authorization') || req.headers.get('Authorization') || '';
  return auth.replace(/^Bearer\s+/i, '').trim();
}
