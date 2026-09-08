import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import api from '../../services/api';
import { Job, Application } from '../../types';
import Card from '../../components/common/Card';
import Button from '../../components/common/Button';
import Badge from '../../components/common/Badge';
import Modal from '../../components/common/Modal';
import { 
  Sparkles, 
  HelpCircle, 
  User, 
  ChevronRight, 
  Clock, 
  CheckCircle2, 
  AlertCircle,
  Copy,
  Briefcase
} from 'lucide-react';

const STAGES = ['APPLIED', 'SCREENING', 'SHORTLISTED', 'INTERVIEW', 'OFFERED', 'REJECTED'];

export const InterviewPipeline: React.FC = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const [jobs, setJobs] = useState<Job[]>([]);
  const [selectedJobId, setSelectedJobId] = useState<number | string>(
    searchParams.get('jobId') || ''
  );
  const [applications, setApplications] = useState<Application[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Interview Questions Generator Modal
  const [activeCandidate, setActiveCandidate] = useState<any | null>(null);
  const [questions, setQuestions] = useState<any | null>(null);
  const [questionsLoading, setQuestionsLoading] = useState(false);
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    fetchInitial();
  }, []);

  useEffect(() => {
    if (selectedJobId) {
      fetchApplications(Number(selectedJobId));
    }
  }, [selectedJobId]);

  const fetchInitial = async () => {
    try {
      const res = await api.get('/jobs/');
      setJobs(res.data);
      if (res.data.length > 0 && !selectedJobId) {
        setSelectedJobId(res.data[0].id);
      }
    } catch (err) {
      // ignore
    } finally {
      setLoading(false);
    }
  };

  const fetchApplications = async (jobId: number) => {
    try {
      const res = await api.get(`/screening/pipeline?job_id=${jobId}`);
      setApplications(res.data);
    } catch (err) {
      // fallback
    }
  };

  const handleAdvanceStatus = async (appId: number, nextStatus: string) => {
    try {
      await api.patch(`/screening/applications/${appId}`, { status: nextStatus });
      setApplications((prev) =>
        prev.map((app) => (app.id === appId ? { ...app, status: nextStatus } : app))
      );
    } catch (err: any) {
      alert('Failed to update status.');
    }
  };

  const handleGenerateQuestions = async (candidate: any) => {
    setActiveCandidate(candidate);
    setQuestions(null);
    setQuestionsLoading(true);
    setCopied(false);

    try {
      const res = await api.post('/screening/interview-questions', {
        job_id: Number(selectedJobId),
        candidate_id: candidate.candidate_id || candidate.id.toString()
      });
      setQuestions(res.data.questions || res.data);
    } catch (err: any) {
      alert('Failed to generate interview questions.');
    } finally {
      setQuestionsLoading(false);
    }
  };

  const handleCopyQuestions = () => {
    if (!questions) return;
    const text = typeof questions === 'string' ? questions : JSON.stringify(questions, null, 2);
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-white mb-1">Recruitment Stage Pipeline</h1>
          <p className="text-sm text-slate-400">
            Progress candidates through hiring milestones and generate tailored AI interview questions.
          </p>
        </div>

        <div className="w-full sm:w-72">
          <select
            value={selectedJobId}
            onChange={(e) => {
              setSelectedJobId(e.target.value);
              setSearchParams({ jobId: e.target.value });
            }}
            className="w-full px-3.5 py-2 bg-slate-900 border border-slate-700 rounded-xl text-white text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
          >
            {jobs.map((j) => (
              <option key={j.id} value={j.id}>
                {j.title}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Kanban Board Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-4 overflow-x-auto pb-4">
        {['APPLIED', 'SCREENING', 'SHORTLISTED', 'INTERVIEW', 'OFFERED'].map((stage) => {
          const stageApps = applications.filter(
            (a) => (a.status || 'APPLIED').toUpperCase() === stage
          );
          return (
            <div key={stage} className="bg-slate-900/60 rounded-xl border border-slate-800 flex flex-col min-h-[500px]">
              {/* Stage Header */}
              <div className="p-3.5 border-b border-slate-800 flex items-center justify-between bg-slate-900/90 rounded-t-xl">
                <span className="text-xs font-bold text-white uppercase tracking-wider">
                  {stage}
                </span>
                <span className="px-2 py-0.5 rounded-full bg-slate-800 text-slate-300 text-[10px] font-mono">
                  {stageApps.length}
                </span>
              </div>

              {/* Stage Cards */}
              <div className="p-3 space-y-3 flex-1 overflow-y-auto">
                {stageApps.length === 0 ? (
                  <div className="text-center py-10 text-xs text-slate-500">
                    No candidates
                  </div>
                ) : (
                  stageApps.map((app) => (
                    <Card key={app.id} className="p-3.5 space-y-3 hover:border-slate-600 transition">
                      <div>
                        <h4 className="text-sm font-semibold text-white truncate">
                          {app.candidate?.full_name || `Candidate #${app.candidate_id}`}
                        </h4>
                        <p className="text-[11px] text-slate-400 mt-0.5">
                          {app.candidate?.current_title || 'Software Engineer'}
                        </p>
                      </div>

                      <div className="flex items-center justify-between pt-2 border-t border-slate-800 text-[11px]">
                        <button
                          onClick={() => handleGenerateQuestions(app.candidate || app)}
                          className="inline-flex items-center text-indigo-400 hover:text-indigo-300 font-medium"
                        >
                          <Sparkles className="w-3 h-3 mr-1" />
                          AI Questions
                        </button>

                        <button
                          onClick={() => {
                            const nextStage =
                              stage === 'APPLIED' ? 'SCREENING' :
                              stage === 'SCREENING' ? 'SHORTLISTED' :
                              stage === 'SHORTLISTED' ? 'INTERVIEW' : 'OFFERED';
                            handleAdvanceStatus(app.id, nextStage);
                          }}
                          className="inline-flex items-center text-slate-400 hover:text-emerald-400"
                          title="Advance stage"
                        >
                          <ChevronRight className="w-4 h-4" />
                        </button>
                      </div>
                    </Card>
                  ))
                )}
              </div>
            </div>
          );
        })}
      </div>

      {/* AI Interview Questions Modal */}
      {activeCandidate && (
        <Modal
          isOpen={Boolean(activeCandidate)}
          onClose={() => setActiveCandidate(null)}
          title={`AI Tailored Interview Questions — ${activeCandidate.full_name || 'Candidate'}`}
          size="lg"
        >
          <div className="space-y-5 text-xs text-slate-300">
            <p className="text-slate-400 leading-relaxed">
              These questions are dynamically generated by analyzing the candidate's exact technical profile, career trajectory, and detected skill gaps relative to the job mandate.
            </p>

            {questionsLoading ? (
              <div className="flex flex-col items-center justify-center py-12 space-y-3">
                <div className="animate-spin w-8 h-8 border-4 border-indigo-500 border-t-transparent rounded-full" />
                <span className="text-slate-400">Synthesizing tailored interview questions...</span>
              </div>
            ) : questions ? (
              <div className="space-y-4">
                <div className="flex justify-end">
                  <Button variant="secondary" size="sm" onClick={handleCopyQuestions}>
                    <Copy className="w-3.5 h-3.5 mr-1" />
                    {copied ? 'Copied!' : 'Copy to Clipboard'}
                  </Button>
                </div>

                <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-4 font-mono leading-relaxed">
                  {Array.isArray(questions) ? (
                    questions.map((q: any, idx: number) => (
                      <div key={idx} className="space-y-1">
                        <strong className="text-indigo-300">Q{idx + 1}: {q.question || q}</strong>
                        {q.rationale && (
                          <p className="text-slate-400 text-[11px] font-sans">
                            <em>Rationale:</em> {q.rationale}
                          </p>
                        )}
                      </div>
                    ))
                  ) : (
                    <pre className="whitespace-pre-wrap font-sans text-xs text-slate-200">
                      {typeof questions === 'string' ? questions : JSON.stringify(questions, null, 2)}
                    </pre>
                  )}
                </div>
              </div>
            ) : (
              <p className="text-rose-400">No questions generated.</p>
            )}
          </div>
        </Modal>
      )}
    </div>
  );
};
