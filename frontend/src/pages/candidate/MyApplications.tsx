import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../../services/api';
import { Application } from '../../types';
import Card from '../../components/common/Card';
import Badge from '../../components/common/Badge';
import Button from '../../components/common/Button';
import { 
  Briefcase, 
  Calendar, 
  MapPin, 
  Building2, 
  AlertCircle, 
  ArrowRight, 
  Sparkles,
  CheckCircle2,
  Clock,
  XCircle
} from 'lucide-react';

export const MyApplications: React.FC = () => {
  const [applications, setApplications] = useState<Application[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchApplications();
  }, []);

  const fetchApplications = async () => {
    try {
      const res = await api.get('/candidates/my-applications');
      setApplications(res.data);
    } catch {
      setError('Failed to fetch applications.');
    } finally {
      setLoading(false);
    }
  };

  const getStatusBadge = (status: string) => {
    switch (status?.toUpperCase()) {
      case 'SHORTLISTED':
        return <Badge variant="success">Shortlisted</Badge>;
      case 'INTERVIEW':
        return <Badge variant="warning">Interview Scheduled</Badge>;
      case 'REJECTED':
        return <Badge variant="danger">Not Selected</Badge>;
      case 'SCREENING':
        return <Badge variant="primary">In Screening</Badge>;
      default:
        return <Badge variant="neutral">Under Review</Badge>;
    }
  };

  const getStatusMessage = (status: string) => {
    switch (status?.toUpperCase()) {
      case 'SHORTLISTED':
        return {
          icon: <CheckCircle2 className="w-4 h-4 text-emerald-400" />,
          text: 'Congratulations! The recruiter has shortlisted your profile for the next stage.',
          color: 'text-emerald-300'
        };
      case 'INTERVIEW':
        return {
          icon: <Calendar className="w-4 h-4 text-purple-400" />,
          text: 'Great news! You have been invited for an interview. The recruiter will reach out with details.',
          color: 'text-purple-300'
        };
      case 'REJECTED':
        return {
          icon: <XCircle className="w-4 h-4 text-rose-400" />,
          text: 'Thank you for applying. The team has decided to move forward with other candidates at this time.',
          color: 'text-slate-400'
        };
      default:
        return {
          icon: <Clock className="w-4 h-4 text-sky-400" />,
          text: 'Your application has been received and is currently being evaluated by the hiring team.',
          color: 'text-slate-400'
        };
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-white mb-1">My Applications</h1>
          <p className="text-sm text-slate-400">
            Track your applied roles, AI fit scores, and hiring status in real time.
          </p>
        </div>
        <Link to="/candidate/jobs">
          <Button variant="primary" size="sm">
            Browse Job Openings
          </Button>
        </Link>
      </div>

      {error && (
        <div className="p-4 rounded-xl bg-rose-500/10 border border-rose-500/20 text-rose-300 text-sm flex items-center gap-3">
          <AlertCircle className="w-5 h-5 flex-shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {loading ? (
        <div className="flex items-center justify-center min-h-[40vh]">
          <div className="animate-spin w-8 h-8 border-4 border-indigo-500 border-t-transparent rounded-full" />
        </div>
      ) : applications.length === 0 ? (
        <Card className="p-12 text-center">
          <Briefcase className="w-12 h-12 mx-auto text-slate-600 mb-3" />
          <h3 className="text-base font-semibold text-white">No active applications</h3>
          <p className="text-xs text-slate-400 mt-1 mb-6">
            You haven't submitted any job applications yet. Browse open roles and apply with your resume!
          </p>
          <Link to="/candidate/jobs">
            <Button variant="primary" size="md">
              Explore Job Openings
            </Button>
          </Link>
        </Card>
      ) : (
        <div className="space-y-4">
          {applications.map((app) => {
            const statusInfo = getStatusMessage(app.status);
            const score = app.match_score ? Math.round(app.match_score) : null;

            return (
              <Card
                key={app.id}
                className="p-6 space-y-4 hover:border-slate-700 transition"
              >
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                  <div className="space-y-1.5">
                    <div className="flex flex-wrap items-center gap-3">
                      <h3 className="text-lg font-bold text-white">
                        {app.job?.title || `Position #${app.job_id}`}
                      </h3>
                      {getStatusBadge(app.status)}
                    </div>

                    <div className="flex flex-wrap items-center gap-x-4 gap-y-1 text-xs text-slate-400">
                      <span className="flex items-center gap-1">
                        <Building2 className="w-3.5 h-3.5 text-slate-500" />
                        {app.job?.department || 'Engineering'}
                      </span>
                      <span className="flex items-center gap-1">
                        <MapPin className="w-3.5 h-3.5 text-slate-500" />
                        {app.job?.location || 'Remote'}
                      </span>
                      <span className="flex items-center gap-1">
                        <Calendar className="w-3.5 h-3.5 text-slate-500" />
                        Applied on {new Date(app.created_at).toLocaleDateString()}
                      </span>
                    </div>
                  </div>

                  {/* AI Match Score Pill */}
                  {score !== null && (
                    <div className="flex items-center gap-3 p-3 bg-slate-950 rounded-xl border border-slate-800 self-start sm:self-auto">
                      <Sparkles className="w-4 h-4 text-indigo-400" />
                      <div>
                        <div className="flex items-baseline gap-1.5">
                          <span className={`text-xl font-bold ${
                            score >= 80 ? 'text-emerald-400' : score >= 65 ? 'text-indigo-400' : 'text-amber-400'
                          }`}>
                            {score}%
                          </span>
                          <span className="text-[10px] text-slate-400 uppercase font-semibold">AI Match</span>
                        </div>
                        <div className="w-20 bg-slate-800 rounded-full h-1 mt-1 overflow-hidden">
                          <div
                            className={`h-full rounded-full ${
                              score >= 80 ? 'bg-emerald-400' : score >= 65 ? 'bg-indigo-400' : 'bg-amber-400'
                            }`}
                            style={{ width: `${score}%` }}
                          />
                        </div>
                      </div>
                    </div>
                  )}
                </div>

                {/* Status Explanation Banner */}
                <div className="pt-3 border-t border-slate-800/80 flex items-center justify-between gap-4">
                  <div className="flex items-center gap-2 text-xs">
                    {statusInfo.icon}
                    <span className={statusInfo.color}>{statusInfo.text}</span>
                  </div>

                  <Link to={`/candidate/match-analyzer?jobId=${app.job_id}`}>
                    <Button variant="ghost" size="sm" className="text-xs">
                      Analyze Match
                      <ArrowRight className="w-3.5 h-3.5 ml-1" />
                    </Button>
                  </Link>
                </div>
              </Card>
            );
          })}
        </div>
      )}
    </div>
  );
};
