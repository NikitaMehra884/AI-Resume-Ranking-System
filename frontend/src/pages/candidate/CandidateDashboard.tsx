import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../../services/api';
import { CandidateProfile, Application } from '../../types';
import Card from '../../components/common/Card';
import Badge from '../../components/common/Badge';
import Button from '../../components/common/Button';
import { 
  User, 
  FileText, 
  Briefcase, 
  Sparkles, 
  ArrowRight, 
  CheckCircle2, 
  Clock, 
  TrendingUp,
  AlertCircle
} from 'lucide-react';

export const CandidateDashboard: React.FC = () => {
  const [profile, setProfile] = useState<CandidateProfile | null>(null);
  const [applications, setApplications] = useState<Application[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [profileRes, appsRes] = await Promise.all([
          api.get('/candidates/me'),
          api.get('/candidates/my-applications')
        ]);
        setProfile(profileRes.data);
        setApplications(appsRes.data);
      } catch (err: any) {
        setError('Could not load candidate dashboard data.');
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="animate-spin w-8 h-8 border-4 border-indigo-500 border-t-transparent rounded-full" />
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {/* Welcome Banner */}
      <div className="p-6 rounded-2xl bg-gradient-to-r from-indigo-900/40 via-purple-900/30 to-slate-900 border border-indigo-500/20 shadow-xl relative overflow-hidden">
        <div className="relative z-10 max-w-2xl">
          <Badge variant="primary" className="mb-3">
            Candidate AI Hub
          </Badge>
          <h1 className="text-2xl sm:text-3xl font-bold text-white mb-2">
            Welcome back, {profile?.full_name || 'Candidate'}
          </h1>
          <p className="text-slate-300 text-sm leading-relaxed mb-6">
            Optimize your resume with our AI parser, discover roles matching your semantic profile, and analyze your fit against job descriptions with grounded explainability.
          </p>
          <div className="flex flex-wrap gap-3">
            <Link to="/candidate/upload-resume">
              <Button variant="primary" size="sm">
                <FileText className="w-4 h-4 mr-1.5" />
                Upload / Parse Resume
              </Button>
            </Link>
            <Link to="/candidate/match-analyzer">
              <Button variant="secondary" size="sm">
                <Sparkles className="w-4 h-4 mr-1.5" />
                AI Match Analyzer
              </Button>
            </Link>
            <Link to="/candidate/jobs">
              <Button variant="ghost" size="sm">
                <Briefcase className="w-4 h-4 mr-1.5" />
                Explore Jobs
              </Button>
            </Link>
          </div>
        </div>
      </div>

      {/* Metrics Row */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
        <Card className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Active Applications</p>
              <h3 className="text-3xl font-bold text-white mt-1">{applications.length}</h3>
            </div>
            <div className="w-12 h-12 rounded-xl bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center text-indigo-400">
              <Briefcase className="w-6 h-6" />
            </div>
          </div>
          <div className="mt-4 flex items-center text-xs text-slate-400">
            <Clock className="w-3.5 h-3.5 mr-1 text-indigo-400" />
            <span>Updated in real time</span>
          </div>
        </Card>

        <Card className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Extracted Skills</p>
              <h3 className="text-3xl font-bold text-white mt-1">{profile?.skills?.length || 0}</h3>
            </div>
            <div className="w-12 h-12 rounded-xl bg-violet-500/10 border border-violet-500/20 flex items-center justify-center text-violet-400">
              <TrendingUp className="w-6 h-6" />
            </div>
          </div>
          <div className="mt-4 flex items-center text-xs text-slate-400">
            <CheckCircle2 className="w-3.5 h-3.5 mr-1 text-emerald-400" />
            <span>Normalized against taxonomy</span>
          </div>
        </Card>

        <Card className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Profile Completeness</p>
              <h3 className="text-3xl font-bold text-white mt-1">
                {profile?.completeness_score ? Math.round(profile.completeness_score) : 80}%
              </h3>
            </div>
            <div className="w-12 h-12 rounded-xl bg-pink-500/10 border border-pink-500/20 flex items-center justify-center text-pink-400">
              <User className="w-6 h-6" />
            </div>
          </div>
          <div className="mt-4 w-full bg-slate-800 rounded-full h-1.5 overflow-hidden">
            <div 
              className="bg-gradient-to-r from-indigo-500 to-pink-500 h-full rounded-full transition-all"
              style={{ width: `${profile?.completeness_score || 80}%` }}
            />
          </div>
        </Card>
      </div>

      {/* Profile & Recent Applications Split */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Skills & Summary Preview */}
        <Card className="p-6 lg:col-span-1 space-y-6">
          <div>
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-base font-semibold text-white">Extracted Skills</h3>
              <Link to="/candidate/profile" className="text-xs text-indigo-400 hover:text-indigo-300">
                Edit Profile →
              </Link>
            </div>
            <div className="flex flex-wrap gap-1.5">
              {profile?.skills && profile.skills.length > 0 ? (
                profile.skills.map((s, idx) => (
                  <span
                    key={idx}
                    className="px-2.5 py-1 rounded-md text-xs font-medium bg-slate-800 text-slate-300 border border-slate-700/60"
                  >
                    {s.name}
                  </span>
                ))
              ) : (
                <p className="text-xs text-slate-500">No skills parsed yet. Upload your resume to extract skills.</p>
              )}
            </div>
          </div>

          <div className="pt-4 border-t border-slate-800">
            <h4 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Headline & Title</h4>
            <p className="text-sm text-slate-200">{profile?.current_title || 'Software Engineer'}</p>
            <p className="text-xs text-slate-400 mt-1">{profile?.current_company || 'Active in tech ecosystem'}</p>
          </div>
        </Card>

        {/* Applications Table */}
        <Card className="p-6 lg:col-span-2">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h3 className="text-base font-semibold text-white">Recent Applications</h3>
              <p className="text-xs text-slate-400">Track current status and recruiter screening</p>
            </div>
            <Link to="/candidate/my-applications">
              <Button variant="ghost" size="sm">
                View All
                <ArrowRight className="w-3.5 h-3.5 ml-1" />
              </Button>
            </Link>
          </div>

          {applications.length === 0 ? (
            <div className="text-center py-12 border border-dashed border-slate-800 rounded-xl">
              <Briefcase className="w-10 h-10 mx-auto text-slate-600 mb-3" />
              <p className="text-sm font-medium text-slate-300">No applications yet</p>
              <p className="text-xs text-slate-500 mt-1 mb-4">Browse open positions and apply with your parsed profile.</p>
              <Link to="/candidate/jobs">
                <Button variant="primary" size="sm">Browse Job Directory</Button>
              </Link>
            </div>
          ) : (
            <div className="divide-y divide-slate-800">
              {applications.slice(0, 5).map((app) => (
                <div key={app.id} className="py-3.5 flex items-center justify-between">
                  <div>
                    <h4 className="text-sm font-semibold text-white">{app.job?.title || `Job #${app.job_id}`}</h4>
                    <p className="text-xs text-slate-400">{app.job?.department} • {app.job?.location}</p>
                  </div>
                  <div className="flex items-center gap-3">
                    <Badge variant={
                      app.status === 'SHORTLISTED' ? 'success' :
                      app.status === 'REJECTED' ? 'danger' :
                      app.status === 'INTERVIEW' ? 'warning' : 'neutral'
                    }>
                      {app.status}
                    </Badge>
                  </div>
                </div>
              ))}
            </div>
          )}
        </Card>
      </div>
    </div>
  );
};
