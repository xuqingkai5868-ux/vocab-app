import React, { useState, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import { Card } from '../components/Card';
import { ProgressBar } from '../components/ProgressBar';
import { Loading } from '../components/Loading';
import { useApp } from '../contexts/AppContext';

type SelfAssessment = 'forgot' | 'vague' | 'known';

export function Review() {
  const navigate = useNavigate();
  const { vocabIndex, state } = useApp();
  const [currentIndex, setCurrentIndex] = useState(0);
  const [showMeaning, setShowMeaning] = useState(false);

  // 收集当前 Day 周期内的模糊词
  const reviewWords = useMemo(() => {
    if (!vocabIndex) return [];
    const day = state.currentDay;
    const dayIdx = day - 1;
    const cycleStart = Math.floor(dayIdx / 7) * 7;
    const result: { word: string; cn: string; theme: string }[] = [];

    for (let i = cycleStart; i < cycleStart + 5 && i < vocabIndex.days.length; i++) {
      const d = vocabIndex.days[i];
      if (d.type !== '新词') continue;
      for (const w of d.words) {
        const id = `${w.theme}|${w.word}`;
        if (state.states[id] === 'fuzzy') {
          result.push({ word: w.word, cn: w.cn, theme: w.theme });
        }
      }
    }
    return result;
  }, [vocabIndex, state]);

  const currentWord = reviewWords[currentIndex];
  const total = reviewWords.length;

  const handleAssessment = (assessment: SelfAssessment) => {
    setShowMeaning(false);
    if (currentIndex < total - 1) {
      setCurrentIndex((i) => i + 1);
    } else {
      alert('复习完成！🎉');
      navigate('/home');
    }
  };

  if (!vocabIndex) return <Loading />;

  if (total === 0) {
    return (
      <div className="space-y-4">
        <h1 className="text-lg font-bold text-gray-800">复习</h1>
        <Card>
          <p className="text-gray-500 text-center py-8">
            🎉 当前周期没有模糊词，继续保持！
          </p>
          <button onClick={() => navigate('/home')} className="w-full py-2.5 bg-primary-500 text-white rounded-lg">
            返回首页
          </button>
        </Card>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center">
        <button onClick={() => navigate('/home')} className="text-primary-500 mr-3 text-sm">
          &larr; 返回
        </button>
        <h1 className="text-lg font-bold text-gray-800">
          模糊词复习
          <span className="text-sm font-normal text-gray-400 ml-2">共 {total} 个</span>
        </h1>
      </div>

      <ProgressBar value={currentIndex} max={total} label="复习进度" />

      <Card className="text-center py-8">
        <p className="text-xs text-gray-400 mb-1">{currentWord.theme}</p>
        <p className="text-xs text-gray-400 mb-4">
          第 {currentIndex + 1}/{total} 个
        </p>
        <h2 className="text-3xl font-bold text-gray-800 mb-6">{currentWord.word}</h2>

        {!showMeaning ? (
          <button
            onClick={() => setShowMeaning(true)}
            className="px-6 py-2.5 bg-primary-500 text-white rounded-lg text-sm"
          >
            查看释义
          </button>
        ) : (
          <div className="space-y-3">
            <p className="text-lg text-gray-600">{currentWord.cn}</p>
            <p className="text-xs text-gray-400">自评：这个词你记住了吗？</p>
            <div className="flex gap-2">
              <button
                onClick={() => handleAssessment('forgot')}
                className="flex-1 py-2.5 bg-red-500 text-white rounded-lg text-sm"
              >
                忘记
              </button>
              <button
                onClick={() => handleAssessment('vague')}
                className="flex-1 py-2.5 bg-yellow-500 text-white rounded-lg text-sm"
              >
                模糊
              </button>
              <button
                onClick={() => handleAssessment('known')}
                className="flex-1 py-2.5 bg-green-500 text-white rounded-lg text-sm"
              >
                认识
              </button>
            </div>
          </div>
        )}
      </Card>
    </div>
  );
}
