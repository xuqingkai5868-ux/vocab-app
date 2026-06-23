import React, { createContext, useContext, useState, useCallback, useEffect, ReactNode } from 'react';
import { useAuth } from './AuthContext';
import { getState, updateState, UserState } from '../api/state';
import { createCheckIn, getCheckIns } from '../api/checkin';
import type { CheckInRecord } from '../types/study';
import { getStats, DashboardStats } from '../api/stats';
import { getTotalDays, getDayWords, getDayPhrases, petSchedule, PETWord, PETPhrase } from '../services/utils/petVocabLoader';
import { canCheckIn } from '../services/checkIn/checkInService';
import { calculateStreak } from '../services/checkIn/streakCalculator';
import { getToday, getCurrentYear, getCurrentMonth } from '../services/utils/dateUtils';

interface AppContextType {
  state: UserState;
  checkIns: Record<string, CheckInRecord>;
  streak: number;
  todayNewWords: PETWord[];
  todayPhrases: PETPhrase[];
  todayStage: number;
  loadAll: () => Promise<void>;
  updateUserState: (newState: UserState) => Promise<void>;
  doCheckIn: (params: { newWordsCompleted: number; reviewWordsCompleted: number; studyDurationMinutes: number }) => Promise<boolean>;
}

const defaultState: UserState = { currentDay: 1, states: {} };

const AppContext = createContext<AppContextType | null>(null);

export function AppProvider({ children }: { children: ReactNode }) {
  const { user } = useAuth();
  const [userState, setUserState] = useState<UserState>(defaultState);
  const [checkIns, setCheckIns] = useState<Record<string, CheckInRecord>>({});
  const [streak, setStreak] = useState(0);
  const [todayNewWords, setTodayNewWords] = useState<PETWord[]>([]);
  const [todayPhrases, setTodayPhrases] = useState<PETPhrase[]>([]);
  const [todayStage, setTodayStage] = useState(1);

  const loadAll = useCallback(async () => {
    if (!user) return;

    try {
      const [stateResp, checkinResp] = await Promise.all([
        getState(user.id),
        getCheckIns(`${getCurrentYear()}-${String(getCurrentMonth()).padStart(2, '0')}`),
      ]);

      setUserState(stateResp.state);

      const day = stateResp.state.currentDay;
      const dayData = petSchedule.schedule.find(d => d.day === day);
      if (dayData) {
        setTodayNewWords(dayData.words);
        setTodayPhrases(dayData.phrases);
        setTodayStage(dayData.grammar_stage);
      }

      setCheckIns(checkinResp.records);
      const records = Object.values(checkinResp.records);
      setStreak(calculateStreak(records));
    } catch (e) {
      console.error('Failed to load data:', e);
    }
  }, [user]);

  const refreshCheckIns = useCallback(async () => {
    if (!user) return;
    try {
      const monthStr = `${getCurrentYear()}-${String(getCurrentMonth()).padStart(2, '0')}`;
      const resp = await getCheckIns(monthStr);
      setCheckIns(resp.records);
      const records = Object.values(resp.records);
      setStreak(calculateStreak(records));
    } catch (e) {
      console.error('Failed to load checkins:', e);
    }
  }, [user]);

  const updateUserState = useCallback(async (newState: UserState) => {
    if (!user) return;
    try {
      await updateState(user.id, newState);
      setUserState(newState);
      const dayData = petSchedule.schedule.find(d => d.day === newState.currentDay);
      if (dayData) {
        setTodayNewWords(dayData.words);
        setTodayPhrases(dayData.phrases);
      }
    } catch (e) {
      console.error('Failed to update state:', e);
      throw e;
    }
  }, [user]);

  const doCheckIn = useCallback(async (params: { newWordsCompleted: number; reviewWordsCompleted: number; studyDurationMinutes: number }) => {
    if (!user) return false;
    const checkable = canCheckIn({ ...params, newWordsTarget: 30, reviewWordsTarget: 15 });
    if (!checkable) return false;

    try {
      const today = getToday();
      await createCheckIn({
        date: today, isCompleted: true,
        studyDuration: params.studyDurationMinutes,
        newWordsCount: params.newWordsCompleted,
        reviewWordsCount: params.reviewWordsCompleted,
        conversationRounds: 0,
      });
      await refreshCheckIns();
      return true;
    } catch (e) {
      console.error('Failed to check in:', e);
      return false;
    }
  }, [user, refreshCheckIns]);

  const totalDays = getTotalDays();

  return (
    <AppContext.Provider value={{
      state: userState,
      checkIns, streak,
      todayNewWords, todayPhrases, todayStage,
      loadAll, updateUserState, doCheckIn,
    }}>
      {children}
    </AppContext.Provider>
  );
}

export function useApp(): AppContextType {
  const ctx = useContext(AppContext);
  if (!ctx) throw new Error('useApp must be used within AppProvider');
  return ctx;
}
