import React, { useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { useApp } from '../contexts/AppContext';
import { Card } from '../components/Card';
import { ProgressBar } from '../components/ProgressBar';
import { Loading } from '../components/Loading';
import { getTotalDays } from '../services/utils/petVocabLoader';

export function Home() {
  const { user } = useAuth();
  const { state, streak, todayNewWords, todayPhrases, todayStage, loadAll, updateUserState, doCheckIn } = useApp();
  const navigate = useNavigate();
  const totalDays = getTotalDays();

  useEffect(() => {
    loadAll();
  }, []);

  const toggleState = useCallback((word: string) => {
    const current = state.states[word];
    let next: 'mastered' | 'fuzzy';
    if (!current) next = 'fuzzy';
    else if (current === 'fuzzy') next = 'mastered';
    else next = 'fuzzy';

    updateUserState({ ...state, states: { ...state.states, [word]: next } });
  }, [state, updateUserState]);

  if (!state) return <Loading text="加载中..." />;

  const masteredToday = todayNewWords.filter(w => state.states[w.word] === 'mastered').length;
  const fuzzyToday = todayNewWords.filter(w => state.states[w.word] === 'fuzzy').length;

  const handleCheckIn = async () => {
    const ok = await doCheckIn({ newWordsCompleted: masteredToday, reviewWordsCompleted: 0, studyDurationMinutes: 15 });
    if (!ok) alert('任务未完成，还不能打卡');
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-xl font-bold text-gray-800">
            {user?.name || '弟弟'}，加油！🐯
          </h1>
          <p className="text-sm text-gray-500 mt-0.5">
            PET 备考 · 第 {state.currentDay}/{totalDays} 天
          </p>
        </div>
        <div className="text-right">
          <div className="text-2xl font-bold text-primary-500">
            阶段 {todayStage}
          </div>
          <div className="text-xs text-gray-400">语法阶段</div>
        </div>
      </div>

      <Card>
        <h2 className="font-semibold text-gray-700 mb-3">今日任务</h2>
        <ProgressBar value={masteredToday} max={todayNewWords.length} label={`新词 (${todayNewWords.length})`} color="bg-primary-500" />
        {todayPhrases.length > 0 && (
          <div className="mt-2 text-sm text-gray-500">
            短语 {todayPhrases.length} 条
          </div>
        )}
      </Card>

      {todayNewWords.length > 0 && (
        <Card>
          <h2 className="font-semibold text-gray-700 mb-3">
            今日新词
            <span className="text-xs text-gray-400 ml-2">点击切换 ○ → △ → ✓</span>
          </h2>
          <div className="space-y-2">
            {todayNewWords.map((w, i) => {
              const s = state.states[w.word];
              return (
                <div
                  key={w.word}
                  onClick={() => toggleState(w.word)}
                  className={`flex items-center justify-between px-4 py-3 rounded-xl cursor-pointer transition-colors ${
                    s === 'mastered' ? 'bg-green-50 border border-green-200' :
                    s === 'fuzzy' ? 'bg-yellow-50 border border-yellow-200' :
                    'bg-white border border-gray-100'
                  }`}
                >
                  <div className="flex items-center gap-3">
                    <span className="text-xs font-mono text-gray-400 w-5">{i + 1}</span>
                    <div>
                      <span className="font-medium text-gray-800">{w.word}</span>
                      <span className="text-sm text-gray-500 ml-2">_{w.pos}_</span>
                      <span className="text-sm text-gray-500 ml-1">{w.meaning}</span>
                    </div>
                  </div>
                  <span className={`text-lg ${s ? '' : 'opacity-40'}`}>
                    {s === 'mastered' ? '✓' : s === 'fuzzy' ? '△' : '○'}
                  </span>
                </div>
              );
            })}
          </div>
        </Card>
      )}

      {todayPhrases.length > 0 && (
        <Card>
          <h2 className="font-semibold text-gray-700 mb-3">关联短语</h2>
          <div className="space-y-2">
            {todayPhrases.map((p, i) => (
              <div key={i} className="flex items-center px-4 py-2 rounded-xl bg-gray-50">
                <span className={`mr-2 ${p.source === 'book' ? 'text-amber-600' : 'text-blue-600'}`}>
                  {p.source === 'book' ? '📗' : '📘'}
                </span>
                <div>
                  <span className="text-sm font-medium text-gray-800">{p.phrase}</span>
                  <span className="text-xs text-gray-500 ml-2">{p.meaning}</span>
                  {p.associated_word && (
                    <span className="text-xs text-gray-400 ml-1">（→ {p.associated_word}）</span>
                  )}
                </div>
              </div>
            ))}
          </div>
        </Card>
      )}

      <div className="grid grid-cols-3 gap-3">
        <Card onClick={() => navigate('/review')} className="text-center py-4">
          <div className="text-2xl mb-1">🔄</div>
          <div className="text-sm text-gray-600">复习 {fuzzyToday > 0 ? `(${fuzzyToday})` : ''}</div>
        </Card>
        <Card onClick={() => navigate('/vocabulary')} className="text-center py-4">
          <div className="text-2xl mb-1">📖</div>
          <div className="text-sm text-gray-600">词库</div>
        </Card>
        <Card onClick={() => navigate('/settings')} className="text-center py-4">
          <div className="text-2xl mb-1">⚙️</div>
          <div className="text-sm text-gray-600">设置</div>
        </Card>
      </div>

      <Card>
        <div className="flex items-center justify-between">
          <div>
            <div className="text-sm text-gray-500">连续打卡</div>
            <div className="text-2xl font-bold text-primary-500">
              {streak > 0 ? `${streak} 天 ${streak >= 7 ? '🔥' : streak >= 3 ? '💪' : '🌱'}` : '0 天'}
            </div>
          </div>
          <div className="flex gap-2">
            <button onClick={() => navigate('/study')} className="flex-1 py-2.5 bg-primary-500 text-white rounded-xl font-medium">
              开始学习 📚
            </button>
            <button onClick={handleCheckIn} className="px-4 py-2.5 bg-success-500 text-white rounded-xl font-medium">
              打卡 ✓
            </button>
          </div>
        </div>
      </Card>
    </div>
  );
}
