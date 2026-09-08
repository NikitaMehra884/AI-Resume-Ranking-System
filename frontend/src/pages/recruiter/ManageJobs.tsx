import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../../services/api';
import { Job } from '../../types';
import Card from '../../components/common/Card';
import Button from '../../components/common/Button';
import Badge from '../../components/common/Badge';
import { Briefcase, Plus, Sliders, Trash2, MapPin, Clock, AlertCircle } from 'lucide-react';

export const ManageJobs: React.FC = () => {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchJobs();
  }, []);

  const fetchJobs = async () => {
    try {
      const res = await api.get('/jobs/');
      setJobs(res.data);
    } catch (err: any) {
      setError('Failed to fetch job listings.');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (jobId: number) => {
    if (!window.confirm('Are you sure you want to delete this job posting?')) return;
    try {
      await api.delete(`/jobs/${jobId}`);
      setJobs(jobs.filter((j) => j.id !== jobId));
    } catch (err: any) {
      alert('Failed to delete job.');
    }
  };

  const handleSeedApplicants = async (jobId: number) => {
    try {
      await api.post(`/jobs/${jobId}/seed-demo-applicants`);
      fetchJobs();
    } catch (err) {
      alert('Failed to add demo applicants.');
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-white mb-1">My Posted Jobs</h1>
          <p className="text-sm text-slate-400">
            Monitor incoming applicants, review AI matching scores, and shortlist qualified candidates.
          </p>
        </div>
        <Link to="/recruiter/create-job">
          <Button variant="primary" size="md">
            <Plus className="w-4 h-4 mr-1.5" />
            Post New Job
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
      ) : jobs.length === 0 ? (
        <Card className="p-12 text-center">
          <Briefcase className="w-12 h-12 mx-auto text-slate-600 mb-3" />
          <h3 className="text-base font-semibold text-white">No job openings created yet</h3>
          <p className="text-xs text-slate-400 mt-1 mb-6">
            Create your first job listing to receive applications from candidates.
          </p>
          <Link to="/recruiter/create-job">
            <Button variant="primary" size="md">Post Job</Button>
          </Link>
        </Card>
      ) : (
        <div className="grid grid-cols-1 gap-4">
          {jobs.map((job) => (
            <Card key={job.id} className="p-6 hover:border-indigo-500/50 transition">
              <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div className="space-y-2.5">
                  <div className="flex flex-wrap items-center gap-3">
                    <h3 className="text-lg font-bold text-white">{job.title}</h3>
                    <Badge variant={job.status === 'PUBLISHED' ? 'success' : 'neutral'}>
                      {job.status}
                    </Badge>
                    {/* Applicant Count Pill */}
                    <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold bg-indigo-500/15 text-indigo-300 border border-indigo-500/30">
                      <span className="w-2 h-2 rounded-full bg-indigo-400 animate-pulse" />
                      {job.applicant_count || 0} Applied
                    </span>
                    {job.shortlisted_count && job.shortlisted_count > 0 ? (
                      <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-semibold bg-emerald-500/15 text-emerald-300 border border-emerald-500/30">
                        {job.shortlisted_count} Shortlisted
                      </span>
                    ) : null}
                  </div>

                  <div className="flex flex-wrap items-center gap-x-4 gap-y-1 text-xs text-slate-400">
                    <span>{job.department}</span>
                    <span>•</span>
                    <span className="flex items-center gap-1">
                      <MapPin className="w-3.5 h-3.5" />
                      {job.location} ({job.work_mode})
                    </span>
                    <span>•</span>
                    <span className="flex items-center gap-1">
                      <Clock className="w-3.5 h-3.5" />
                      {job.minimum_experience} - {job.maximum_experience} yrs
                    </span>
                  </div>

                  <div className="flex flex-wrap gap-1.5 pt-1">
                    {job.skills && job.skills.map((s, idx) => (
                      <span
                        key={idx}
                        className={`text-[11px] px-2 py-0.5 rounded ${
                          s.is_required
                            ? 'bg-indigo-500/10 text-indigo-300 border border-indigo-500/20'
                            : 'bg-slate-800 text-slate-400'
                        }`}
                      >
                        {s.name}
                      </span>
                    ))}
                  </div>
                </div>

                <div className="flex flex-wrap items-center gap-3 flex-shrink-0">
                  {(!job.applicant_count || job.applicant_count === 0) && (
                    <button
                      onClick={() => handleSeedApplicants(job.id)}
                      className="text-xs px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 transition"
                      title="Add 4 realistic candidate applicants to test AI ranking and shortlisting"
                    >
                      + Add Demo Applicants
                    </button>
                  )}
                  <Link to={`/recruiter/screening?jobId=${job.id}`}>
                    <Button variant="primary" size="sm">
                      <Sliders className="w-3.5 h-3.5 mr-1.5" />
                      Review Applicants ({job.applicant_count || 0})
                    </Button>
                  </Link>
                  <button
                    onClick={() => handleDelete(job.id)}
                    className="p-2 text-slate-500 hover:text-rose-400 rounded-lg hover:bg-slate-800 transition"
                    title="Delete Job"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              </div>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
};
