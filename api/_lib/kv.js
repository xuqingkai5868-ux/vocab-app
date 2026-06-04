// 统一封装 Vercel KV 调用
// 所有数据走 Upstash Redis（Vercel KV 后端）
// key 命名空间：user:xxx / pin:xxx / state:xxx / session:xxx

import { kv } from '@vercel/kv';

export const K = {
  user: (id) => `user:${id}`,
  pin: (id) => `pin:${id}`,
  state: (id) => `state:${id}`,
  session: (token) => `session:${token}`
};

export async function kvGet(key) {
  return await kv.get(key);
}

export async function kvSet(key, value) {
  // 传对象会被 JSON 序列化；传字符串原样存
  return await kv.set(key, value);
}

export async function kvDel(key) {
  return await kv.del(key);
}

export async function kvGetJSON(key) {
  const raw = await kv.get(key);
  if (raw == null) return null;
  if (typeof raw === 'string') {
    try { return JSON.parse(raw); } catch { return null; }
  }
  return raw;
}

export async function kvSetJSON(key, value) {
  return await kv.set(key, JSON.stringify(value));
}

export async function kvKeysByPrefix(prefix) {
  // 列出所有匹配前缀的 key。Upstash 用 SCAN，避免 KEYS * 阻塞
  const keys = [];
  let cursor = '0';
  do {
    const [next, batch] = await kv.scan(cursor, { match: `${prefix}*`, count: 200 });
    cursor = next;
    for (const k of batch) keys.push(k);
  } while (cursor !== '0');
  return keys;
}
