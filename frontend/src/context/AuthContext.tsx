import React, { createContext, useContext, useState, useEffect } from 'react';
import api from '../services/api';
import { UserRole } from '../types';

interface AuthState {
  token: string | null;
  role: UserRole | null;
  userId: number | null;
  email: string | null;
  isAuthenticated: boolean;
  loading: boolean;
  login: (email: string, password: string) => Promise<any>;
  register: (email: string, password: string, role: UserRole, full_name?: string) => Promise<any>;
  logout: () => void;
}

const AuthContext = createContext<AuthState | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [token, setToken] = useState<string | null>(localStorage.getItem('token'));
  const [role, setRole] = useState<UserRole | null>(localStorage.getItem('role') as UserRole | null);
  const [userId, setUserId] = useState<number | null>(
    localStorage.getItem('userId') ? Number(localStorage.getItem('userId')) : null
  );
  const [email, setEmail] = useState<string | null>(localStorage.getItem('email'));
  const [loading, setLoading] = useState(false);

  const login = async (loginEmail: string, loginPassword: string) => {
    setLoading(true);
    try {
      const res = await api.post('/auth/login', {
        email: loginEmail,
        password: loginPassword,
      });
      const data = res.data;
      const newToken = data.access_token;
      const newRole = data.user?.role || (data.role as UserRole) || 'CANDIDATE';
      const newUserId = data.user?.id || data.user_id || 1;
      const newEmail = data.user?.email || loginEmail;

      localStorage.setItem('token', newToken);
      localStorage.setItem('role', newRole);
      localStorage.setItem('userId', String(newUserId));
      localStorage.setItem('email', newEmail);
      localStorage.setItem('user', JSON.stringify({ role: newRole, email: newEmail, id: newUserId }));

      setToken(newToken);
      setRole(newRole);
      setUserId(newUserId);
      setEmail(newEmail);
      return data;
    } finally {
      setLoading(false);
    }
  };

  const register = async (
    regEmail: string,
    regPassword: string,
    regRole: UserRole,
    fullName?: string
  ) => {
    setLoading(true);
    try {
      const res = await api.post('/auth/register', {
        email: regEmail,
        password: regPassword,
        role: regRole,
        full_name: fullName,
      });
      const data = res.data;
      // Auto-login upon registration
      return await login(regEmail, regPassword);
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('role');
    localStorage.removeItem('userId');
    localStorage.removeItem('email');
    localStorage.removeItem('user');
    setToken(null);
    setRole(null);
    setUserId(null);
    setEmail(null);
  };

  return (
    <AuthContext.Provider
      value={{
        token,
        role,
        userId,
        email,
        isAuthenticated: !!token,
        loading,
        login,
        register,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export default AuthContext;
