// ===== EdgeOne Pages Token Verify =====
// 验证 Authorization Bearer Token，从 my_kv 读取 session
//
// 返回：
//   成功 → { session: { token, userId, role, name, grade, issuedAt, expiresAt } }
//   失败 → { error, status, message }

import { K, kvGetJSON, kvDel } from './kv.js';

const SESSION_TTL_MS = 30 * 24 * 60 * 60 * 1000; // 30 天

export async function verifyToken(request) {
  const auth = request.headers.get('Authorization') || '';
  const m = auth.match(/^Bearer\s+(\S+)$/i);
  if (!m) {
    return { error: 'unauthorized', status: 401, message: '缺少 Bearer Token' };
  }
  const token = m[1];

  const session = await kvGetJSON(K.session(token));
  if (!session) {
    return { error: 'invalid_token', status: 401, message: 'Token 无效或已过期' };
  }

  // 检查过期（30 天）
  if (session.expiresAt && session.expiresAt < Date.now()) {
    await kvDel(K.session(token));
    return { error: 'token_expired', status: 401, message: 'Token 已过期' };
  }

  return { session };
}
