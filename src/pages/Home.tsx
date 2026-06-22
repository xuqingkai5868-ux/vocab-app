import React, { useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { useApp } from '../contexts/AppContext';
import { Card } from '../components/Card';
import { ProgressBar } from '../components/ProgressBar';
import { Loading } from '../components/Loading';
import { getTotalDays } from '../services/utils/vocabLoader';

function wordId(theme: string, word: string) {
  return `${theme}|${word}`;
}

export function Home() {
  const { user } = useAuth();
  const { state, streak, todayNewWords, vocabIndex, loadAll, updateUserState, doCheckIn } = useApp();
  const navigate = useNavigate();

  useEffect(() => {
    loadAll();
  }, []);

  const toggleState = useCallback((w: { theme: string; word: string }) => {
    const id = wordId(w.theme, w.word);
    const current = state.states[id];
    let next: 'mastered' | 'fuzzy';
    if (!current) next = 'fuzzy';
    else if (current === 'fuzzy') next = 'mastered';
    else next = 'fuzzy';

    const newStates = { ...state.states, [id]: next };
    updateUserState({ ...state, states: newStates });
  }, [state, updateUserState]);

  if (!vocabIndex) return <Loading text="加载词库中..." />;

  const totalDays = getTotalDays(vocabIndex);
  const newWordsTarget = 8;
  const reviewWordsTarget = 15;

  const masteredToday = todayNewWords.filter(w => state.states[wordId(w.theme, w.word)] === 'mastered').length;
  const fuzzyToday = todayNewWords.filter(w => state.states[wordId(w.theme, w.word)] === 'fuzzy').length;

  const handleCheckIn = async () => {
    const ok = await doCheckIn({
      newWordsCompleted: masteredToday,
      reviewWordsCompleted: 0,
      studyDurationMinutes: 15,
    });
    if (!ok) {
      alert('学习任务未完成，还不能打卡');
    }
  };

  const todayStr = new Date().toLocaleDateString('zh-CN', {
    year: 'numeric', month: 'long', day: 'numeric', weekday: 'long',
  });

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-xl font-bold text-gray-800">
            {user?.name || '用户'}，早上好！
          </h1>
          <p className="text-sm text-gray-500 mt-0.5">{todayStr}</p>
        </div>
        <div className="text-right">
          <div className="text-xs text-gray-400">学习进度</div>
          <div className="text-lg font-bold text-primary-500">
            第 {state.currentDay}/{totalDays} 天
          </div>
        </div>
      </div>

      <Card>
        <h2 className="font-semibold text-gray-700 mb-3">今日学习计划</h2>
        <ProgressBar
          value={masteredToday}
          max={newWordsTarget}
          label={`新词 (${todayNewWords.length})`}
          color="bg-primary-500"
        />
        <ProgressBar
          value={0}
          max={reviewWordsTarget}
          label="复习"
          color="bg-success-500"
          className="mt-3"
        />
      </Card>

      {todayNewWords.length > 0 && (
        <Card>
          <h2 className="font-semibold text-gray-700 mb-3">
            今日新词
            <span className="text-xs text-gray-400 ml-2">点击切换状态 ○ → ⭐ → ✓</span>
          </h2>
          <div className="space-y-2">
            {todayNewWords.map((w, i) => {
              const id = wordId(w.theme, w.word);
              const s = state.states[id];
              return (
                <div
                  key={id}
                  onClick={() => toggleState(w)}
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
                      <span className="text-sm text-gray-500 ml-2">{w.cn}</span>
                    </div>
                  </div>
                  <span className={`text-lg ${s ? '' : 'opacity-40'}`}>
                    {s === 'mastered' ? '✓' : s === 'fuzzy' ? '⭐' : '○'}
                  </span>
                </div>
              );
            })}
          </div>
          <button
            onClick={() => navigate('/conversation')}
            className="mt-4 w-full py-2.5 bg-primary-500 text-white rounded-xl font-medium hover:bg-primary-600 transition-colors"
          >
            进入 AI 对话练习 🤖
          </button>
        </Card>
      )}

      <div className="grid grid-cols-3 gap-3">
        <Card onClick={() => navigate('/conversation')} className="text-center py-4">
          <div className="text-2xl mb-1">💬</div>
          <div className="text-sm text-gray-600">AI 对话</div>
        </Card>
        <Card onClick={() => navigate('/review')} className="text-center py-4">
          <div className="text-2xl mb-1">📝</div>
          <div className="text-sm text-gray-600">复习（{fuzzyToday}）</div>
        </Card>
        <Card onClick={() => navigate('/vocabulary')} className="text-center py-4">
          <div className="text-2xl mb-1">📖</div>
          <div className="text-sm text-gray-600">生词本</div>
        </Card>
      </div>

      <Card>
        <div className="flex items-center justify-between">
          <div>
            <div className="text-sm text-gray-500">连续打卡</div>
            <div className="text-2xl font-bold text-primary-500">{streak} 天</div>
          </div>
          <button
            onClick={handleCheckIn}
            className="px-6 py-2.5 bg-success-500 text-white rounded-xl font-medium hover:bg-success-600 transition-colors"
          >
            今日打卡
          </button>
        </div>
      </Card>
    </div>
  );
}
