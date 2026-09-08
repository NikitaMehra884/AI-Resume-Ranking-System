import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { LogOut, Briefcase, User, Sparkles, LayoutDashboard } from 'lucide-react';

export const Navbar: React.FC = () => {
  const { isAuthenticated, role, email, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <header className="sticky top-0 z-40 w-full border-b border-slate-800 bg-slate-900/80 backdrop-blur-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        <Link to="/" className="flex items-center gap-2">
          <div className="h-9 w-9 rounded-xl bg-gradient-to-tr from-indigo-500 to-indigo-700 flex items-center justify-center text-white shadow-lg shadow-indigo-500/20">
            <Sparkles className="h-5 w-5" />
          </div>
          <span className="font-bold text-xl tracking-tight text-white">
            HireSense <span className="text-indigo-400 font-extrabold text-sm uppercase px-1.5 py-0.5 rounded bg-indigo-500/10 border border-indigo-500/20 ml-1">AI</span>
          </span>
        </Link>

        <nav className="flex items-center gap-4">
          {isAuthenticated ? (
            <>
              {role === 'RECRUITER' ? (
                <>
                  <Link to="/recruiter" className="text-xs sm:text-sm font-medium text-slate-300 hover:text-white transition flex items-center gap-1.5">
                    <LayoutDashboard className="h-4 w-4" /> Dashboard
                  </Link>
                  <Link to="/recruiter/screening" className="text-xs sm:text-sm font-medium text-indigo-400 hover:text-indigo-300 transition flex items-center gap-1.5">
                    <Sparkles className="h-4 w-4" /> Screening
                  </Link>
                  <Link to="/recruiter/manage-jobs" className="text-xs sm:text-sm font-medium text-slate-300 hover:text-white transition flex items-center gap-1.5">
                    <Briefcase className="h-4 w-4" /> Jobs
                  </Link>
                  <Link to="/recruiter/pipeline" className="text-xs sm:text-sm font-medium text-slate-300 hover:text-white transition">
                    Pipeline
                  </Link>
                  <Link to="/recruiter/analytics" className="text-xs sm:text-sm font-medium text-slate-300 hover:text-white transition">
                    Analytics
                  </Link>
                </>
              ) : (
                <>
                  <Link to="/candidate" className="text-xs sm:text-sm font-medium text-slate-300 hover:text-white transition flex items-center gap-1.5">
                    <LayoutDashboard className="h-4 w-4" /> Dashboard
                  </Link>
                  <Link to="/candidate/jobs" className="text-xs sm:text-sm font-medium text-slate-300 hover:text-white transition flex items-center gap-1.5">
                    <Briefcase className="h-4 w-4" /> Jobs
                  </Link>
                  <Link to="/candidate/match-analyzer" className="text-xs sm:text-sm font-medium text-indigo-400 hover:text-indigo-300 transition flex items-center gap-1.5">
                    <Sparkles className="h-4 w-4" /> Fit Analyzer
                  </Link>
                  <Link to="/candidate/my-applications" className="text-xs sm:text-sm font-medium text-slate-300 hover:text-white transition">
                    Applications
                  </Link>
                  <Link to="/candidate/profile" className="text-xs sm:text-sm font-medium text-slate-300 hover:text-white transition flex items-center gap-1.5">
                    <User className="h-4 w-4" /> Profile
                  </Link>
                </>
              )}

              <div className="h-4 w-px bg-slate-800" />

              <div className="flex items-center gap-3">
                <span className="text-xs font-semibold px-2.5 py-1 rounded-full bg-slate-800 text-slate-300 border border-slate-700">
                  {role}
                </span>
                <button
                  onClick={handleLogout}
                  className="p-1.5 rounded-lg text-slate-400 hover:text-red-400 hover:bg-slate-800 transition"
                  title="Logout"
                >
                  <LogOut className="h-4 w-4" />
                </button>
              </div>
            </>
          ) : (
            <div className="flex items-center gap-3">
              <Link to="/login" className="text-sm font-medium text-slate-300 hover:text-white transition px-3 py-1.5">
                Sign In
              </Link>
              <Link
                to="/register"
                className="text-sm font-semibold text-white bg-indigo-600 hover:bg-indigo-500 transition px-4 py-2 rounded-lg shadow-sm"
              >
                Get Started
              </Link>
            </div>
          )}
        </nav>
      </div>
    </header>
  );
};
