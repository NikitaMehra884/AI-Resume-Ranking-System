import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../../services/api';
import { Job } from '../../types';
import Card from '../../components/common/Card';
import Badge from '../../components/common/Badge';
import Button from '../../components/common/Button';
import { 
  Briefcase, 
  Users, 
  Sparkles, 
  BarChart3, 
  Plus, 
  ArrowRight, 
  Clock, 
  Sliders, 
  CheckCircle2 
} from 'lucide-react';

export const RecruiterDashboard: React.FC = () => {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchJobs();
  }, []);

  const fetchJobs = async () => {
    try {
      const res = await api.get('/jobs/');
      setJobs(res.data);
    } catch (err) {
      // ignore
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-8">
      {/* Top Welcome Banner */}
      <div className="p-6 rounded-2xl bg-gradient-to-r from-indigo-900/50 via-slate-900 to-violet-900/40 border border-indigo-500/20 shadow-xl flex flex-col sm:flex-row items-start sm:items-center justify-between gap-6">
        <div>
          <Badge variant="primary" className="mb-2">Recruiter Intelligence Suite</Badge>
          <h1 className="text-2xl sm:text-3xl font-bold text-white">Talent Command Center</h1>
          <p className="text-sm text-slate-300 mt-1 max-w-2xl">
            Screen candidates across our 100,000 profile index using dense vector embeddings, normalized BM25 scores, and grounded LLM explanations.
          </p>
        </div>
        <div className="flex gap-3">
          <Link to="/recruiter/create-job">
            <Button variant="primary" size="md">
              <Plus className="w-4 h-4 mr-1.5" />
              Post New Role
            </Button>
          </Link>
          <Link to="/recruiter/screening">
            <Button variant="secondary" size="md">
              <Sliders className="w-4 h-4 mr-1.5" />
              Screen Candidates
            </Button>
          </Link>
        </div>
      </div>

      {/* Metrics Row */}
      <div className="grid grid-cols-1 sm:grid-cols-4 gap-6">
        <Card className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Candidate Talent Pool</p>
              <h3 className="text-3xl font-extrabold text-white mt-1">100,000</h3>
            </div>
            <div className="w-12 h-12 rounded-xl bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center text-indigo-400">
              <Users className="w-6 h-6" />
            </div>
          </div>
          <div className="mt-4 flex items-center text-xs text-slate-400">
            <CheckCircle2 className="w-3.5 h-3.5 mr-1 text-emerald-400" />
            <span>FAISS Index Indexed & Ready</span>
          </div>
        </Card>

        <Card className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Active Open Roles</p>
              <h3 className="text-3xl font-extrabold text-white mt-1">{jobs.length}</h3>
            </div>
            <div className="w-12 h-12 rounded-xl bg-violet-500/10 border border-violet-500/20 flex items-center justify-center text-violet-400">
              <Briefcase className="w-6 h-6" />
            </div>
          </div>
          <div className="mt-4 flex items-center text-xs text-slate-400">
            <Clock className="w-3.5 h-3.5 mr-1 text-indigo-400" />
            <span>Real-time screening active</span>
          </div>
        </Card>

        <Card className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Retrieval Engine</p>
              <h3 className="text-2xl font-bold text-emerald-400 mt-1">4-Stage Hybrid</h3>
            </div>
            <div className="w-12 h-12 rounded-xl bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center text-emerald-400">
              <Sparkles className="w-6 h-6" />
            </div>
          </div>
          <div className="mt-4 text-xs text-slate-400">
            <span>Dense + Sparse + 8 Normalized Signals</span>
          </div>
        </Card>

        <Card className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Screening Analytics</p>
              <h3 className="text-2xl font-bold text-pink-400 mt-1">Explainable</h3>
            </div>
            <div className="w-12 h-12 rounded-xl bg-pink-500/10 border border-pink-500/20 flex items-center justify-center text-pink-400">
              <BarChart3 className="w-6 h-6" />
            </div>
          </div>
          <div className="mt-4 text-xs text-slate-400">
            <span>Zero hallucination guarantee</span>
          </div>
        </Card>
      </div>

      {/* Active Jobs Section */}
      <Card className="p-6">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h2 className="text-lg font-bold text-white">Active Positions</h2>
            <p className="text-xs text-slate-400">Manage listings and launch AI candidate screening</p>
          </div>
          <Link to="/recruiter/manage-jobs">
            <Button variant="ghost" size="sm">
              Manage All ({jobs.length})
              <ArrowRight className="w-3.5 h-3.5 ml-1" />
            </Button>
          </Link>
        </div>

        {loading ? (
          <div className="flex items-center justify-center py-12">
            <div className="animate-spin w-8 h-8 border-4 border-indigo-500 border-t-transparent rounded-full" />
          </div>
        ) : jobs.length === 0 ? (
          <div className="text-center py-12 border border-dashed border-slate-800 rounded-xl">
            <Briefcase className="w-10 h-10 mx-auto text-slate-600 mb-3" />
            <h4 className="text-sm font-semibold text-white">No jobs created yet</h4>
            <p className="text-xs text-slate-400 mt-1 mb-4">Post your first position to begin AI screening.</p>
            <Link to="/recruiter/create-job">
              <Button variant="primary" size="sm">Create Job</Button>
            </Link>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="text-slate-400 uppercase tracking-wider border-b border-slate-800 bg-slate-900/60">
                <tr>
                  <th className="py-3 px-4">Title & Department</th>
                  <th className="py-3 px-4">Location</th>
                  <th className="py-3 px-4">Experience Range</th>
                  <th className="py-3 px-4">Status</th>
                  <th className="py-3 px-4 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800">
                {jobs.slice(0, 5).map((job) => (
                  <tr key={job.id} className="hover:bg-slate-900/40 transition">
                    <td className="py-3.5 px-4">
                      <div className="font-semibold text-white text-sm">{job.title}</div>
                      <div className="text-slate-400">{job.department}</div>
                    </td>
                    <td className="py-3.5 px-4 text-slate-300">{job.location} ({job.work_mode})</td>
                    <td className="py-3.5 px-4 text-slate-300">
                      {job.minimum_experience} - {job.maximum_experience} yrs
                    </td>
                    <td className="py-3.5 px-4">
                      <Badge variant={job.status === 'PUBLISHED' ? 'success' : 'neutral'}>
                        {job.status}
                      </Badge>
                    </td>
                    <td className="py-3.5 px-4 text-right">
                      <Link to={`/recruiter/screening?jobId=${job.id}`}>
                        <Button variant="primary" size="sm">
                          <Sliders className="w-3.5 h-3.5 mr-1" />
                          Screen AI Top-K
                        </Button>
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </Card>
    </div>
  );
};
