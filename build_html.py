"""一次性构建脚本: 把 schedule.min.json 嵌入到 index.html 模板中"""
import json

# 读取 schedule 数据
with open('schedule.min.json', 'r', encoding='utf-8') as f:
    schedule_data = f.read()

# HTML 模板 (CSS + JS 内联)
html = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<meta name="theme-color" content="#4f46e5">
<title>暑假共学背单词</title>
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Microsoft YaHei", sans-serif;
  background: #f5f5f7;
  color: #1f2937;
  line-height: 1.5;
  -webkit-font-smoothing: antialiased;
}
button { font: inherit; cursor: pointer; border: none; background: none; }
button:active { transform: scale(0.97); }
.app-header {
  position: sticky; top: 0; z-index: 10;
  background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
  color: white;
  padding: 14px 16px 12px;
  box-shadow: 0 2px 8px rgba(79,70,229,0.15);
}
.app-header h1 { font-size: 18px; font-weight: 600; margin-bottom: 10px; }
.user-switch { display: flex; gap: 8px; }
.user-btn {
  flex: 1; padding: 8px 10px;
  background: rgba(255,255,255,0.15);
  color: white;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.2s;
}
.user-btn.active { background: white; color: #4f46e5; font-weight: 600; }
.app-main { padding: 12px; padding-bottom: 80px; }
.day-nav {
  display: flex; align-items: center; justify-content: space-between;
  background: white; padding: 12px;
  border-radius: 12px; margin-bottom: 12px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}
.nav-btn {
  padding: 8px 14px; background: #eef2ff; color: #4f46e5;
  border-radius: 8px; font-size: 14px; font-weight: 500;
  min-width: 72px;
}
.nav-btn:disabled { opacity: 0.4; cursor: not-allowed; }
.day-info { text-align: center; flex: 1; }
.day-title { font-size: 16px; font-weight: 600; color: #1f2937; }
.day-type {
  font-size: 12px; margin-top: 2px; padding: 2px 8px;
  display: inline-block; border-radius: 10px;
}
.day-type.new { background: #dbeafe; color: #1e40af; }
.day-type.review { background: #fef3c7; color: #92400e; }
.day-type.rest { background: #f3f4f6; color: #6b7280; }
.progress-section {
  background: white; padding: 12px 16px;
  border-radius: 12px; margin-bottom: 12px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}
.progress-text {
  display: flex; justify-content: space-between;
  font-size: 14px; margin-bottom: 8px;
}
.progress-text strong { color: #4f46e5; font-size: 16px; }
.progress-bar {
  height: 8px; background: #e5e7eb;
  border-radius: 4px; overflow: hidden;
}
.progress-fill {
  height: 100%; background: linear-gradient(90deg, #10b981, #4f46e5);
  border-radius: 4px; transition: width 0.4s ease;
}
.theme-header {
  background: white; padding: 10px 16px;
  border-radius: 12px; margin-bottom: 8px;
  font-size: 14px; color: #6b7280;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}
.theme-header strong { color: #1f2937; }
.word-list { display: flex; flex-direction: column; gap: 6px; }
.word-card {
  display: flex; align-items: center; gap: 10px;
  background: white; padding: 10px 12px;
  border-radius: 10px;
  box-shadow: 0 1px 2px rgba(0,0,0,0.04);
  transition: all 0.2s;
}
.word-card.mastered { background: #f0fdf4; }
.word-card.fuzzy { background: #fffbeb; }
.word-idx {
  width: 28px; height: 28px;
  background: #eef2ff; color: #4f46e5;
  border-radius: 50%; font-size: 12px; font-weight: 600;
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
}
.word-card.mastered .word-idx { background: #d1fae5; color: #065f46; }
.word-card.fuzzy .word-idx { background: #fef3c7; color: #92400e; }
.word-info { flex: 1; min-width: 0; }
.word-en {
  font-size: 16px; font-weight: 600; color: #1f2937;
  margin-bottom: 2px;
}
.word-en .word-cn-inline {
  font-size: 13px; color: #6b7280; font-weight: 400; margin-left: 6px;
}
.word-phrase {
  font-size: 12px; color: #9ca3af;
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.state-btn {
  width: 36px; height: 36px;
  font-size: 20px;
  border-radius: 8px;
  background: #f3f4f6; color: #9ca3af;
  flex-shrink: 0;
  transition: all 0.15s;
}
.state-btn.mastered { background: #10b981; color: white; }
.state-btn.fuzzy { background: #f59e0b; color: white; }
.review-section, .rest-section, .fuzzy-section {
  background: white; padding: 16px;
  border-radius: 12px; margin-bottom: 8px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}
.review-section h3, .fuzzy-section h3, .rest-section h3 {
  font-size: 15px; font-weight: 600; margin-bottom: 10px;
  color: #4f46e5;
}
.fuzzy-section h3 { color: #f59e0b; }
.theme-group { margin-bottom: 14px; }
.theme-group:last-child { margin-bottom: 0; }
.theme-group-title {
  font-size: 13px; color: #6b7280; margin-bottom: 6px;
  font-weight: 500;
}
.theme-group .word-card { padding: 8px 10px; }
.action-btn {
  display: block; width: 100%;
  padding: 12px; margin-top: 8px;
  background: linear-gradient(135deg, #4f46e5, #7c3aed);
  color: white; border-radius: 10px;
  font-size: 15px; font-weight: 600;
  box-shadow: 0 2px 6px rgba(79,70,229,0.25);
}
.action-btn:disabled { opacity: 0.5; cursor: not-allowed; }
.empty-state {
  text-align: center; padding: 30px 20px;
  color: #9ca3af; font-size: 14px;
}
.rest-content {
  text-align: center; padding: 20px 0;
  color: #6b7280;
}
.rest-content .emoji { font-size: 48px; margin-bottom: 12px; }
.rest-content h2 {
  font-size: 20px; color: #1f2937; margin-bottom: 8px;
  font-weight: 600;
}
.rest-content p { font-size: 14px; margin-bottom: 4px; }
.rest-tips {
  margin-top: 16px; padding: 14px;
  background: #f9fafb; border-radius: 10px;
  font-size: 13px; text-align: left;
  color: #6b7280;
}
.app-footer {
  position: fixed; bottom: 0; left: 0; right: 0;
  display: flex; gap: 6px;
  background: white;
  padding: 10px 12px;
  border-top: 1px solid #e5e7eb;
  box-shadow: 0 -2px 8px rgba(0,0,0,0.05);
}
.footer-btn {
  flex: 1; padding: 10px 8px;
  background: #f3f4f6; color: #4b5563;
  border-radius: 8px; font-size: 13px; font-weight: 500;
}
.modal {
  position: fixed; inset: 0;
  background: rgba(0,0,0,0.5);
  display: flex; align-items: center; justify-content: center;
  z-index: 100; padding: 20px;
}
.modal.hidden { display: none; }
.modal-content {
  background: white; border-radius: 16px;
  padding: 24px; max-width: 400px; width: 100%;
  text-align: center;
}
.modal-content h2 {
  font-size: 18px; color: #1f2937; margin-bottom: 16px;
}
.dictation-prompt {
  font-size: 14px; color: #6b7280; margin-bottom: 16px;
  min-height: 20px;
}
.dictation-prompt.speaking { color: #4f46e5; font-weight: 600; }
#dictation-input {
  width: 100%; padding: 12px;
  font-size: 18px; border: 2px solid #e5e7eb;
  border-radius: 10px; text-align: center;
  margin-bottom: 12px;
}
#dictation-input:focus { outline: none; border-color: #4f46e5; }
.dictation-feedback {
  min-height: 24px; margin-bottom: 16px;
  font-size: 14px; font-weight: 600;
}
.dictation-feedback.correct { color: #10b981; }
.dictation-feedback.wrong { color: #ef4444; }
.dictation-controls {
  display: flex; gap: 8px; margin-bottom: 12px;
}
.dictation-controls button {
  flex: 1; padding: 10px;
  border-radius: 8px; font-size: 14px; font-weight: 500;
}
#dictation-replay { background: #eef2ff; color: #4f46e5; }
#dictation-skip { background: #fef3c7; color: #92400e; }
#dictation-close { background: #f3f4f6; color: #6b7280; }
.dictation-progress {
  font-size: 13px; color: #9ca3af;
}
.dictation-result {
  text-align: center; padding: 10px 0;
}
.dictation-result-score {
  font-size: 48px; font-weight: 700; color: #4f46e5;
  margin-bottom: 8px;
}
.toast {
  position: fixed; top: 70px; left: 50%;
  transform: translateX(-50%);
  background: rgba(0,0,0,0.85); color: white;
  padding: 10px 20px; border-radius: 20px;
  font-size: 14px; z-index: 200;
  animation: fadeInOut 2s forwards;
}
@keyframes fadeInOut {
  0% { opacity: 0; transform: translate(-50%, -10px); }
  20%, 80% { opacity: 1; transform: translate(-50%, 0); }
  100% { opacity: 0; transform: translate(-50%, -10px); }
}
@media (min-width: 640px) {
  .app-main { max-width: 600px; margin: 0 auto; }
  .word-en { font-size: 18px; }
}
</style>
</head>
<body>
<div id="app">
  <header class="app-header">
    <h1>📚 暑假共学背单词</h1>
    <div class="user-switch">
      <button class="user-btn active" data-user="gao">👧 姐姐（高一）</button>
      <button class="user-btn" data-user="primary">👦 弟弟（三年级）</button>
    </div>
  </header>

  <main class="app-main">
    <nav class="day-nav">
      <button id="prev-day" class="nav-btn">‹ 上一天</button>
      <div class="day-info">
        <div class="day-title">Day <span id="current-day">1</span> / 83</div>
        <div class="day-type new" id="day-type">新词日</div>
      </div>
      <button id="next-day" class="nav-btn">下一天 ›</button>
    </nav>

    <div class="progress-section">
      <div class="progress-text">
        <span>已掌握 <strong id="mastered-count">0</strong> / 1460</span>
        <span id="progress-percent">0%</span>
      </div>
      <div class="progress-bar">
        <div class="progress-fill" id="progress-fill" style="width:0%"></div>
      </div>
    </div>

    <div class="theme-header" id="theme-header"></div>
    <div id="content-area"></div>
  </main>

  <footer class="app-footer">
    <button id="export-btn" class="footer-btn">💾 导出</button>
    <button id="import-btn" class="footer-btn">📥 导入</button>
    <button id="dictation-btn" class="footer-btn">🔊 听写</button>
    <button id="reset-btn" class="footer-btn">🔄 重置</button>
  </footer>

  <div id="dictation-modal" class="modal hidden">
    <div class="modal-content">
      <h2>听写测试</h2>
      <div class="dictation-prompt" id="dictation-prompt">点击"开始"听写</div>
      <input type="text" id="dictation-input" placeholder="输入听到的单词" autocomplete="off" autocapitalize="off" autocorrect="off">
      <div class="dictation-feedback" id="dictation-feedback"></div>
      <div class="dictation-controls">
        <button id="dictation-start">开始</button>
        <button id="dictation-replay" class="hidden">🔊 再听</button>
        <button id="dictation-skip">跳过</button>
        <button id="dictation-close">关闭</button>
      </div>
      <div class="dictation-progress" id="dictation-progress">0 / 10</div>
    </div>
  </div>

  <input type="file" id="import-file" accept=".json" style="display:none">
</div>

<script>
const SCHEDULE = __DATA__;

// ===== State =====
const STORAGE_KEY = 'vocab-app-v1';
let state = {
  activeUser: 'gao',
  users: {
    gao: { name: '姐姐（高一）', currentDay: 1, states: {} },
    primary: { name: '弟弟（三年级）', currentDay: 1, states: {} }
  }
};

function loadState() {
  try {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved) {
      const parsed = JSON.parse(saved);
      // 兼容旧版
      if (parsed.users) {
        state = Object.assign(state, parsed);
        if (!state.users.gao) state.users.gao = { name: '姐姐（高一）', currentDay: 1, states: {} };
        if (!state.users.primary) state.users.primary = { name: '弟弟（三年级）', currentDay: 1, states: {} };
      }
    }
  } catch (e) {
    console.warn('Failed to load state', e);
  }
}

function saveState() {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
  } catch (e) {
    console.error('Failed to save state', e);
  }
}

function wordId(w) { return w.theme + '|' + w.word; }

function getUserState() { return state.users[state.activeUser]; }

// ===== Stats =====
function getStats() {
  const u = getUserState();
  let mastered = 0, fuzzy = 0, learned = 0;
  for (const day of SCHEDULE) {
    if (day.type !== '新词') continue;
    for (const w of day.words) {
      const s = u.states[wordId(w)];
      if (s === 'mastered') { mastered++; learned++; }
      else if (s === 'fuzzy') { fuzzy++; learned++; }
    }
  }
  return { mastered, fuzzy, learned, total: 1460 };
}

// ===== Render =====
function render() {
  const u = getUserState();
  const day = SCHEDULE[u.currentDay - 1];

  // Update user switch
  document.querySelectorAll('.user-btn').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.user === state.activeUser);
  });

  // Update day nav
  document.getElementById('current-day').textContent = u.currentDay;
  document.getElementById('prev-day').disabled = u.currentDay <= 1;
  document.getElementById('next-day').disabled = u.currentDay >= SCHEDULE.length;

  const dayTypeEl = document.getElementById('day-type');
  dayTypeEl.className = 'day-type ' + (day.type === '新词' ? 'new' : day.type === '复习' ? 'review' : 'rest');
  dayTypeEl.textContent = day.type === '新词' ? '新词日' : day.type === '复习' ? '复习日' : '休息日';

  // Progress
  const stats = getStats();
  document.getElementById('mastered-count').textContent = stats.mastered;
  document.getElementById('progress-percent').textContent = (stats.mastered / stats.total * 100).toFixed(1) + '%';
  document.getElementById('progress-fill').style.width = (stats.mastered / stats.total * 100) + '%';

  // Theme header
  const themeHeader = document.getElementById('theme-header');
  if (day.type === '新词') {
    // 计算主题范围
    const themeRanges = {};
    day.words.forEach(w => {
      if (!themeRanges[w.theme]) themeRanges[w.theme] = [w.themeIdx, w.themeIdx];
      else themeRanges[w.theme][1] = w.themeIdx;
    });
    const desc = Object.entries(themeRanges)
      .map(([t, [s, e]]) => `<strong>${t}</strong>（${s}${s !== e ? '-' + e : ''}）`)
      .join(' + ');
    themeHeader.innerHTML = '📖 ' + desc;
  } else if (day.type === '复习') {
    themeHeader.innerHTML = '🔁 复习 ' + (day.themes || []).map(t => `<strong>${t}</strong>`).join(' · ');
  } else {
    themeHeader.innerHTML = '😌 休息日';
  }

  // Content
  const content = document.getElementById('content-area');
  content.innerHTML = '';
  if (day.type === '新词') {
    renderNewDay(content, day);
  } else if (day.type === '复习') {
    renderReviewDay(content, day);
  } else {
    renderRestDay(content, day);
  }
}

function renderNewDay(container, day) {
  const u = getUserState();
  const list = document.createElement('div');
  list.className = 'word-list';

  day.words.forEach((w, i) => {
    const id = wordId(w);
    const s = u.states[id] || 'new';
    const card = document.createElement('div');
    card.className = 'word-card ' + s;
    card.innerHTML = `
      <div class="word-idx">${i + 1}</div>
      <div class="word-info">
        <div class="word-en">${w.word}<span class="word-cn-inline">${w.cn}</span></div>
        ${w.phrase ? `<div class="word-phrase">${w.phrase}</div>` : '<div class="word-phrase">&nbsp;</div>'}
      </div>
      <button class="state-btn ${s}" data-word-id="${id}" data-idx="${i}">
        ${s === 'mastered' ? '✓' : s === 'fuzzy' ? '⭐' : '○'}
      </button>
    `;
    list.appendChild(card);
  });
  container.appendChild(list);

  // 主题标注（每行）
  // 已通过 word-card 隐含，可考虑加 theme 标签
}

function renderReviewDay(container, day) {
  const u = getUserState();

  // 5 主题循环
  const themes = day.themes || [];
  themes.forEach(theme => {
    const section = document.createElement('div');
    section.className = 'review-section';
    const themeWords = day.words.filter(w => w.theme === theme);
    let html = `<h3>📚 ${theme}</h3><div class="word-list">`;
    themeWords.forEach((w, i) => {
      const id = wordId(w);
      const s = u.states[id] || 'new';
      html += `
        <div class="word-card ${s}">
          <div class="word-idx">${i + 1}</div>
          <div class="word-info">
            <div class="word-en">${w.word}<span class="word-cn-inline">${w.cn}</span></div>
            ${w.phrase ? `<div class="word-phrase">${w.phrase}</div>` : '<div class="word-phrase">&nbsp;</div>'}
          </div>
          <button class="state-btn ${s}" data-word-id="${id}" data-idx="r${i}">${s === 'mastered' ? '✓' : s === 'fuzzy' ? '⭐' : '○'}</button>
        </div>
      `;
    });
    html += '</div>';
    section.innerHTML = html;
    container.appendChild(section);
  });

  // 模糊回炉
  const fuzzyWords = collectFuzzyWords(day);
  if (fuzzyWords.length > 0) {
    const fuzzySection = document.createElement('div');
    fuzzySection.className = 'fuzzy-section';
    let html = '<h3>⭐ 模糊回炉</h3><div class="word-list">';
    fuzzyWords.forEach((w, i) => {
      const id = wordId(w);
      html += `
        <div class="word-card fuzzy">
          <div class="word-idx">${i + 1}</div>
          <div class="word-info">
            <div class="word-en">${w.word}<span class="word-cn-inline">${w.cn}</span></div>
            ${w.phrase ? `<div class="word-phrase">${w.phrase}</div>` : '<div class="word-phrase">&nbsp;</div>'}
          </div>
          <button class="state-btn fuzzy" data-word-id="${id}">⭐</button>
        </div>
      `;
    });
    html += '</div></div>';
    fuzzySection.innerHTML = html;
    container.appendChild(fuzzySection);
  }

  // 听写按钮
  const dictBtn = document.createElement('button');
  dictBtn.className = 'action-btn';
  dictBtn.textContent = '🎧 听写测试 (5 词)';
  dictBtn.onclick = () => startDictation(day);
  container.appendChild(dictBtn);
}

function collectFuzzyWords(day) {
  const u = getUserState();
  const result = [];
  // 收集本周期的所有新词日的 ⭐ 词
  const dayIdx = day.day - 1;
  const cycleStart = Math.floor(dayIdx / 7) * 7;
  for (let i = cycleStart; i < cycleStart + 5 && i < SCHEDULE.length; i++) {
    if (SCHEDULE[i].type !== '新词') continue;
    SCHEDULE[i].words.forEach(w => {
      if (u.states[wordId(w)] === 'fuzzy') {
        result.push(w);
      }
    });
  }
  return result;
}

function renderRestDay(container, day) {
  const rest = document.createElement('div');
  rest.className = 'rest-section rest-content';
  const tips = [
    '🎵 听英文儿歌 / 看英文动画（不背词，纯磨耳朵）',
    '📖 翻一翻这周背过的单词本',
    '🚶 出门走走，眼睛和脑子都休息',
    '✏️ 玩一玩单词游戏（Quizlet / 多邻国）'
  ];
  const tip = tips[Math.floor(Math.random() * tips.length)];
  rest.innerHTML = `
    <div class="emoji">😌</div>
    <h2>休息日</h2>
    <p>今天不用背新词，<br>给大脑放个假。</p>
    <div class="rest-tips">
      <strong>今天推荐：</strong><br>${tip}
    </div>
  `;
  container.appendChild(rest);
}

// ===== State Cycle =====
function cycleState(id, btn) {
  const u = getUserState();
  const cur = u.states[id] || 'new';
  const next = cur === 'new' ? 'mastered' : cur === 'mastered' ? 'fuzzy' : 'new';
  if (next === 'new') {
    delete u.states[id];
  } else {
    u.states[id] = next;
  }
  saveState();
  render();
}

function clearState(id, btn) {
  // 复习日 ⭐ 按钮 → 直接清成 mastered (回炉成功)
  const u = getUserState();
  if (u.states[id] === 'fuzzy') {
    u.states[id] = 'mastered';
  } else if (u.states[id] === 'mastered') {
    delete u.states[id];
  } else {
    u.states[id] = 'mastered';
  }
  saveState();
  render();
}

// ===== Dictation =====
let dictationState = null;

function startDictation(day) {
  const u = getUserState();
  // 选 5 个本周期新词日里没掌握（或模糊）的词
  const candidates = [];
  const dayIdx = day.day - 1;
  const cycleStart = Math.floor(dayIdx / 7) * 7;
  for (let i = cycleStart; i < cycleStart + 5 && i < SCHEDULE.length; i++) {
    if (SCHEDULE[i].type !== '新词') continue;
    SCHEDULE[i].words.forEach(w => {
      const s = u.states[wordId(w)];
      if (s !== 'mastered') candidates.push(w);
    });
  }
  if (candidates.length === 0) {
    showToast('本周期没有可听写的词 🎉');
    return;
  }
  // 随机取最多 5 个
  shuffle(candidates);
  const picks = candidates.slice(0, Math.min(5, candidates.length));
  dictationState = { picks, idx: 0, correct: 0, total: picks.length, input: '' };
  document.getElementById('dictation-modal').classList.remove('hidden');
  document.getElementById('dictation-start').classList.remove('hidden');
  document.getElementById('dictation-replay').classList.add('hidden');
  document.getElementById('dictation-prompt').textContent = '点击"开始"听写';
  document.getElementById('dictation-prompt').classList.remove('speaking');
  document.getElementById('dictation-input').value = '';
  document.getElementById('dictation-feedback').textContent = '';
  document.getElementById('dictation-feedback').className = 'dictation-feedback';
  document.getElementById('dictation-progress').textContent = `0 / ${dictationState.total}`;
}

function speakWord(word) {
  if (!('speechSynthesis' in window)) {
    showToast('浏览器不支持语音');
    return;
  }
  window.speechSynthesis.cancel();
  const u = new SpeechSynthesisUtterance(word);
  u.lang = 'en-US';
  u.rate = 0.85;
  u.pitch = 1;
  window.speechSynthesis.speak(u);
  const prompt = document.getElementById('dictation-prompt');
  prompt.textContent = '🔊 播放中...';
  prompt.classList.add('speaking');
}

function nextDictation() {
  if (!dictationState) return;
  if (dictationState.idx >= dictationState.total) {
    // 完成
    const score = Math.round(dictationState.correct / dictationState.total * 100);
    const prompt = document.getElementById('dictation-prompt');
    const fb = document.getElementById('dictation-feedback');
    prompt.textContent = '测试完成';
    prompt.classList.remove('speaking');
    fb.innerHTML = `<div class="dictation-result"><div class="dictation-result-score">${score}%</div><div>${dictationState.correct} / ${dictationState.total} 正确</div></div>`;
    fb.className = 'dictation-feedback correct';
    document.getElementById('dictation-start').classList.remove('hidden');
    document.getElementById('dictation-start').textContent = '再来一次';
    document.getElementById('dictation-replay').classList.add('hidden');
    dictationState = null;
    return;
  }
  const w = dictationState.picks[dictationState.idx];
  speakWord(w.word);
  document.getElementById('dictation-input').value = '';
  document.getElementById('dictation-input').disabled = false;
  document.getElementById('dictation-input').focus();
  document.getElementById('dictation-feedback').textContent = '';
  document.getElementById('dictation-feedback').className = 'dictation-feedback';
  document.getElementById('dictation-progress').textContent = `${dictationState.idx + 1} / ${dictationState.total}`;
  document.getElementById('dictation-start').classList.add('hidden');
  document.getElementById('dictation-replay').classList.remove('hidden');
}

function checkDictation() {
  if (!dictationState) return;
  const w = dictationState.picks[dictationState.idx];
  const input = document.getElementById('dictation-input').value.trim().toLowerCase();
  const correct = w.word.toLowerCase();
  const fb = document.getElementById('dictation-feedback');
  if (input === correct) {
    fb.textContent = '✓ 正确！';
    fb.className = 'dictation-feedback correct';
    dictationState.correct++;
    // 标记为 mastered
    getUserState().states[wordId(w)] = 'mastered';
    saveState();
    setTimeout(() => {
      dictationState.idx++;
      nextDictation();
    }, 800);
  } else if (input === '') {
    // 空
  } else {
    fb.innerHTML = `✗ 正确拼写: <strong>${w.word}</strong> (${w.cn})`;
    fb.className = 'dictation-feedback wrong';
    setTimeout(() => {
      dictationState.idx++;
      nextDictation();
    }, 1800);
  }
}

function shuffle(arr) {
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
}

function showToast(msg) {
  const t = document.createElement('div');
  t.className = 'toast';
  t.textContent = msg;
  document.body.appendChild(t);
  setTimeout(() => t.remove(), 2000);
}

// ===== Event Handlers =====
document.addEventListener('click', e => {
  const btn = e.target.closest('.state-btn');
  if (btn) {
    const id = btn.dataset.wordId;
    if (!id) return;
    // 复习日的 ⭐ 按钮语义不同: 模糊 → 掌握
    if (btn.classList.contains('fuzzy') && btn.textContent === '⭐') {
      // 看上下文: 在 word-card.fuzzy 里 → 复习回炉成功
      const card = btn.closest('.word-card');
      if (card && card.classList.contains('fuzzy') && card.parentElement.parentElement.classList.contains('fuzzy-section')) {
        // 模糊回炉区
        clearState(id, btn);
        return;
      }
    }
    cycleState(id, btn);
    return;
  }

  if (e.target.closest('#prev-day')) {
    if (getUserState().currentDay > 1) {
      getUserState().currentDay--;
      saveState();
      render();
    }
  }
  if (e.target.closest('#next-day')) {
    if (getUserState().currentDay < SCHEDULE.length) {
      getUserState().currentDay++;
      saveState();
      render();
    }
  }

  // User switch
  const userBtn = e.target.closest('.user-btn');
  if (userBtn) {
    state.activeUser = userBtn.dataset.user;
    saveState();
    render();
    showToast('已切换到 ' + getUserState().name);
  }

  // Footer
  if (e.target.closest('#export-btn')) exportData();
  if (e.target.closest('#import-btn')) document.getElementById('import-file').click();
  if (e.target.closest('#dictation-btn')) {
    const u = getUserState();
    const day = SCHEDULE[u.currentDay - 1];
    if (day.type === '新词') {
      // 新词日也允许听写
      startDictation(day);
    } else {
      startDictation(day);
    }
  }
  if (e.target.closest('#reset-btn')) {
    if (confirm('确定要重置 ' + getUserState().name + ' 的所有进度吗？此操作不可撤销。')) {
      getUserState().states = {};
      getUserState().currentDay = 1;
      saveState();
      render();
      showToast('已重置');
    }
  }

  // Dictation
  if (e.target.closest('#dictation-start')) {
    if (!dictationState || dictationState.idx >= dictationState.total) {
      // 重新开始
      const u = getUserState();
      const day = SCHEDULE[u.currentDay - 1];
      startDictation(day);
    }
    nextDictation();
  }
  if (e.target.closest('#dictation-replay')) {
    if (dictationState && dictationState.idx < dictationState.total) {
      speakWord(dictationState.picks[dictationState.idx].word);
    }
  }
  if (e.target.closest('#dictation-skip')) {
    if (dictationState) {
      dictationState.idx++;
      nextDictation();
    }
  }
  if (e.target.closest('#dictation-close')) {
    dictationState = null;
    document.getElementById('dictation-modal').classList.add('hidden');
    render();
  }
});

// 听写输入框回车提交
document.getElementById('dictation-input').addEventListener('keydown', e => {
  if (e.key === 'Enter') {
    if (dictationState && dictationState.idx < dictationState.total) {
      checkDictation();
    } else {
      nextDictation();
    }
  }
});

// 导入文件
document.getElementById('import-file').addEventListener('change', e => {
  const file = e.target.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = ev => {
    try {
      const data = JSON.parse(ev.target.result);
      if (data.users && confirm('导入将覆盖当前所有用户进度，确定吗？')) {
        state = data;
        if (!state.users.gao) state.users.gao = { name: '姐姐（高一）', currentDay: 1, states: {} };
        if (!state.users.primary) state.users.primary = { name: '弟弟（三年级）', currentDay: 1, states: {} };
        saveState();
        render();
        showToast('导入成功 ✓');
      }
    } catch (err) {
      showToast('文件格式错误');
    }
  };
  reader.readAsText(file);
  e.target.value = '';
});

// 导出
function exportData() {
  const data = JSON.stringify(state, null, 2);
  const blob = new Blob([data], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  const date = new Date().toISOString().slice(0, 10);
  a.href = url;
  a.download = `vocab-backup-${date}.json`;
  a.click();
  URL.revokeObjectURL(url);
  showToast('已下载备份');
}

// ===== Init =====
loadState();
render();
</script>
</body>
</html>
'''

# 嵌入数据
final = html.replace('__DATA__', schedule_data)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(final)

import os
print(f'index.html: {os.path.getsize("index.html")} bytes')
print('Done.')
