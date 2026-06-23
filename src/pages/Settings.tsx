import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Card } from '../components/Card';
import { useAuth } from '../contexts/AuthContext';

export function Settings() {
  const navigate = useNavigate();
  const { user, logout } = useAuth();

  const handleReset = () => {
    if (!confirm('确定重置弟弟的所有学习进度吗？此操作不可撤销。')) return;
    localStorage.removeItem('di_states');
    localStorage.removeItem('vocab_user');
    alert('已重置');
    logout();
  };

  return (
    <div className="space-y-4">
      <h1 className="text-lg font-bold text-gray-800">设置</h1>

      <Card>
        <h2 className="font-semibold text-gray-700 mb-3">学习信息</h2>
        <div className="space-y-2 text-sm">
          <div className="flex justify-between"><span className="text-gray-500">学员</span><span>{user?.name || '弟弟'}</span></div>
          <div className="flex justify-between"><span className="text-gray-500">目标</span><span>剑桥 PET 考试</span></div>
          <div className="flex justify-between"><span className="text-gray-500">版本</span><span>PET v1.0</span></div>
        </div>
      </Card>

      <Card>
        <h2 className="font-semibold text-gray-700 mb-3">操作</h2>
        <button
          onClick={handleReset}
          className="w-full py-2.5 bg-red-500 text-white rounded-lg text-sm"
        >
          重置学习进度
        </button>
        <button
          onClick={() => { logout(); navigate('/'); }}
          className="w-full py-2.5 mt-2 border border-gray-200 text-gray-600 rounded-lg text-sm"
        >
          退出登录
        </button>
      </Card>
    </div>
  );
}
