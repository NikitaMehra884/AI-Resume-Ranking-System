import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import { Navbar } from './components/common/Navbar';

// Public Pages
import { LandingPage } from './pages/LandingPage';
import { Login } from './pages/Login';
import { Register } from './pages/Register';

// Candidate Pages
import { CandidateDashboard } from './pages/candidate/CandidateDashboard';
import { CandidateProfile } from './pages/candidate/CandidateProfile';
import { ResumeUpload } from './pages/candidate/ResumeUpload';
import { JobDirectory } from './pages/candidate/JobDirectory';
import { MatchAnalyzer } from './pages/candidate/MatchAnalyzer';
import { MyApplications } from './pages/candidate/MyApplications';

// Recruiter Pages
import { RecruiterDashboard } from './pages/recruiter/RecruiterDashboard';
import { CreateJob } from './pages/recruiter/CreateJob';
import { ManageJobs } from './pages/recruiter/ManageJobs';
import { CandidateScreening } from './pages/recruiter/CandidateScreening';
import { CandidateComparison } from './pages/recruiter/CandidateComparison';
import { InterviewPipeline } from './pages/recruiter/InterviewPipeline';
import { RecruiterAnalytics } from './pages/recruiter/RecruiterAnalytics';

// Protected Route Guard
const ProtectedRoute: React.FC<{
  children: React.ReactNode;
  allowedRole?: 'CANDIDATE' | 'RECRUITER' | 'ADMIN';
}> = ({ children, allowedRole }) => {
  const { isAuthenticated, role, loading } = useAuth();

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="animate-spin w-8 h-8 border-4 border-indigo-500 border-t-transparent rounded-full" />
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  if (allowedRole && role !== allowedRole && role !== 'ADMIN') {
    return <Navigate to={role === 'RECRUITER' ? '/recruiter' : '/candidate'} replace />;
  }

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col selection:bg-indigo-500 selection:text-white">
      <Navbar />
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 flex-1 w-full">
        {children}
      </main>
      <footer className="border-t border-slate-900 py-6 text-center text-xs text-slate-600 bg-slate-950">
        © 2026 AI Recruitment Intelligence Platform • High-Throughput Talent Discovery
      </footer>
    </div>
  );
};

export const App: React.FC = () => {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          {/* Public Routes */}
          <Route path="/" element={<LandingPage />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />

          {/* Candidate Routes */}
          <Route
            path="/candidate"
            element={
              <ProtectedRoute allowedRole="CANDIDATE">
                <CandidateDashboard />
              </ProtectedRoute>
            }
          />
          <Route
            path="/candidate/profile"
            element={
              <ProtectedRoute allowedRole="CANDIDATE">
                <CandidateProfile />
              </ProtectedRoute>
            }
          />
          <Route
            path="/candidate/upload-resume"
            element={
              <ProtectedRoute allowedRole="CANDIDATE">
                <ResumeUpload />
              </ProtectedRoute>
            }
          />
          <Route
            path="/candidate/jobs"
            element={
              <ProtectedRoute allowedRole="CANDIDATE">
                <JobDirectory />
              </ProtectedRoute>
            }
          />
          <Route
            path="/candidate/match-analyzer"
            element={
              <ProtectedRoute allowedRole="CANDIDATE">
                <MatchAnalyzer />
              </ProtectedRoute>
            }
          />
          <Route
            path="/candidate/my-applications"
            element={
              <ProtectedRoute allowedRole="CANDIDATE">
                <MyApplications />
              </ProtectedRoute>
            }
          />

          {/* Recruiter Routes */}
          <Route
            path="/recruiter"
            element={
              <ProtectedRoute allowedRole="RECRUITER">
                <RecruiterDashboard />
              </ProtectedRoute>
            }
          />
          <Route
            path="/recruiter/create-job"
            element={
              <ProtectedRoute allowedRole="RECRUITER">
                <CreateJob />
              </ProtectedRoute>
            }
          />
          <Route
            path="/recruiter/manage-jobs"
            element={
              <ProtectedRoute allowedRole="RECRUITER">
                <ManageJobs />
              </ProtectedRoute>
            }
          />
          <Route
            path="/recruiter/screening"
            element={
              <ProtectedRoute allowedRole="RECRUITER">
                <CandidateScreening />
              </ProtectedRoute>
            }
          />
          <Route
            path="/recruiter/compare"
            element={
              <ProtectedRoute allowedRole="RECRUITER">
                <CandidateComparison />
              </ProtectedRoute>
            }
          />
          <Route
            path="/recruiter/pipeline"
            element={
              <ProtectedRoute allowedRole="RECRUITER">
                <InterviewPipeline />
              </ProtectedRoute>
            }
          />
          <Route
            path="/recruiter/analytics"
            element={
              <ProtectedRoute allowedRole="RECRUITER">
                <RecruiterAnalytics />
              </ProtectedRoute>
            }
          />

          {/* Fallback */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
};

export default App;
