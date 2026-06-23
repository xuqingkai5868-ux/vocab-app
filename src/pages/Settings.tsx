import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Card } from '../components/Card';
import { useAuth } from '../contexts/AuthContext';
import { useApp } from '../contexts/AppContext';
import { getTotalDays } from '../services/utils/petVocabLoader';

export function Settings() {
  const navigate = useNavigate();
  const { user, logout } = useAuth();
  const { wordsPerDay, setWordsPerDay } = useApp();
  const totalDays = getTotalDays(wordsPerDay);

  const handleReset = () => {
    if (!confirm(`确定重置 ${user?.name || '用户'} 的所有学习进度吗？`)) return;
    localStorage.removeItem('vocab_user');
    localStorage.removeItem('di_states');
    alert('已重置');
    logout();
  };

  return (
    <div className="space-y-4">
      <h1 className="text-lg font-bold text-gray-800">设置</h1>

      <Card>
        <h2 className="font-semibold text-gray-700 mb-3">每日学习量</h2>
        <div className="flex items-center gap-4">
          <input
            type="range" min={5} max={50} step={5}
            value={wordsPerDay}
            onChange={e => setWordsPerDay(parseInt(e.target.value))}
            className="flex-1 accent-primary-500"
          />
          <span className="text-lg font-bold text-primary-500 min-w-[3rem] text-center">{wordsPerDay}</span>
        </div>
        <div className="flex justify-between text-xs text-gray-400 mt-1">
          <span>每天 5 词</span>
          <span>每天 50 词</span>
        </div>
        <div className="mt-2 text-sm text-gray-500">
          共 {totalDays} 天完成 · 当前 Day {useApp().state.currentDay}
        </div>
      </Card>

      <Card>
        <h2 className="font-semibold text-gray-700 mb-3">学习信息</h2>
        <div className="space-y-2 text-sm">
          <div className="flex justify-between"><span className="text-gray-500">学员</span><span>{user?.name || '-'}</span></div>
          <div className="flex justify-between"><span className="text-gray-500">词库</span><span>PET {getTotalDays(wordsPerDay) * wordsPerDay} 词</span></div>
        </div>
      </Card>

      <Card>
        <h2 className="font-semibold text-gray-700 mb-3">操作</h2>
        <button onClick={handleReset} className="w-full py-2.5 bg-red-500 text-white rounded-lg text-sm">重置学习进度</button>
        <button onClick={() => { logout(); navigate('/'); }} className="w-full py-2.5 mt-2 border border-gray-200 text-gray-600 rounded-lg text-sm">退出登录</button>
      </Card>
    </div>
  );
}
