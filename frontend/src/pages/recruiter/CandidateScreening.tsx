import React, { useState, useEffect } from 'react';
import { useSearchParams, useNavigate, Link } from 'react-router-dom';
import api from '../../services/api';
import { Job, RankedCandidate } from '../../types';
import Card from '../../components/common/Card';
import Button from '../../components/common/Button';
import Badge from '../../components/common/Badge';
import Modal from '../../components/common/Modal';
import { 
  Sparkles, 
  Search, 
  CheckCircle2, 
  XCircle, 
  ArrowRight, 
  Eye, 
  UserCheck, 
  GitCompare, 
  MapPin, 
  Briefcase, 
  Clock, 
  AlertCircle,
  FileText,
  HelpCircle,
  Users,
  Mail,
  Phone,
  Calendar,
  Send,
  Plus,
  Copy,
  Check,
  Award,
  Filter,
  Cpu
} from 'lucide-react';

export const CandidateScreening: React.FC = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const navigate = useNavigate();

  const [jobs, setJobs] = useState<Job[]>([]);
  const [selectedJobId, setSelectedJobId] = useState<number | string>(
    searchParams.get('jobId') || ''
  );
  const [statusFilter, setStatusFilter] = useState<string>('ALL');
  const [searchQuery, setSearchQuery] = useState<string>('');

  const [candidates, setCandidates] = useState<RankedCandidate[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);

  // Comparison selections
  const [selectedCandidateIds, setSelectedCandidateIds] = useState<string[]>([]);

  // Modals
  const [activeModalCandidate, setActiveModalCandidate] = useState<RankedCandidate | null>(null);
  const [activeResumeCandidate, setActiveResumeCandidate] = useState<RankedCandidate | null>(null);
  const [activeQuestionsCandidate, setActiveQuestionsCandidate] = useState<RankedCandidate | null>(null);
  const [questionsLoading, setQuestionsLoading] = useState(false);
  const [questionsData, setQuestionsData] = useState<any | null>(null);
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    fetchJobs();
  }, []);

  useEffect(() => {
    if (jobs.length > 0 && !selectedJobId) {
      const initialId = searchParams.get('jobId') || jobs[0].id;
      setSelectedJobId(initialId);
    }
  }, [jobs]);

  useEffect(() => {
    if (selectedJobId) {
      handleRunScreening();
    }
  }, [selectedJobId]);

  const fetchJobs = async () => {
    try {
      const res = await api.get('/jobs/');
      setJobs(res.data);
    } catch {
      // ignore
    }
  };

  const handleRunScreening = async () => {
    if (!selectedJobId) {
      return;
    }
    setLoading(true);
    setError(null);
    setSelectedCandidateIds([]);

    try {
      const res = await api.post('/screening/rank', {
        job_id: Number(selectedJobId),
        top_k: 50
      });
      setCandidates(res.data.candidates || []);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to fetch applicants.');
    } finally {
      setLoading(false);
    }
  };

  const toggleSelectCandidate = (candidateId: string) => {
    if (selectedCandidateIds.includes(candidateId)) {
      setSelectedCandidateIds(selectedCandidateIds.filter((id) => id !== candidateId));
    } else {
      if (selectedCandidateIds.length >= 3) {
        alert('You can compare a maximum of 3 candidates simultaneously.');
        return;
      }
      setSelectedCandidateIds([...selectedCandidateIds, candidateId]);
    }
  };

  const handleLaunchComparison = () => {
    if (selectedCandidateIds.length < 2) {
      alert('Please select at least 2 candidates to compare.');
      return;
    }
    const candidateParams = selectedCandidateIds.join(',');
    navigate(`/recruiter/compare?jobId=${selectedJobId}&candidates=${candidateParams}`);
  };

  const handleUpdateStatus = async (candidateId: string, status: string) => {
    try {
      await api.post('/screening/update-status', {
        job_id: Number(selectedJobId),
        candidate_id: candidateId,
        status: status
      });
      setCandidates((prev) =>
        prev.map((c) => (c.candidate_id === candidateId ? { ...c, status: status as any } : c))
      );
      setMessage({ type: 'success', text: `Candidate status updated to ${status}!` });
      setTimeout(() => setMessage(null), 3500);
    } catch {
      alert('Failed to update status.');
    }
  };

  const handleAutoShortlist = async () => {
    if (!selectedJobId) return;
    try {
      const res = await api.post('/screening/auto-shortlist', {
        job_id: Number(selectedJobId),
        threshold: 75.0
      });
      setMessage({ type: 'success', text: res.data.message || 'Auto-shortlist complete!' });
      setTimeout(() => setMessage(null), 4000);
      handleRunScreening();
    } catch {
      alert('Failed to auto-shortlist.');
    }
  };

  const handleSeedApplicants = async () => {
    if (!selectedJobId) return;
    try {
      await api.post(`/jobs/${selectedJobId}/seed-demo-applicants`);
      setMessage({ type: 'success', text: '4 realistic applicants added to this position!' });
      setTimeout(() => setMessage(null), 4000);
      handleRunScreening();
    } catch {
      alert('Failed to add demo applicants.');
    }
  };

  const handleOpenQuestions = async (cand: RankedCandidate) => {
    setActiveQuestionsCandidate(cand);
    setQuestionsLoading(true);
    setQuestionsData(null);
    setCopied(false);
    try {
      const res = await api.post('/screening/interview-questions', {
        job_id: Number(selectedJobId),
        candidate_id: cand.candidate_id
      });
      setQuestionsData(res.data.questions);
    } catch {
      setQuestionsData({
        technical_questions: [
          'Can you explain how you designed and optimized your backend or ML pipeline?',
          'What architectural trade-offs do you consider for high-traffic real-time workloads?'
        ],
        behavioral_questions: [
          'Describe a challenging production incident you resolved under tight deadlines.',
          'How do you handle disagreement with peers regarding system architecture decisions?'
        ],
        project_questions: [
          'Walk us through the key system components of the most recent project listed on your resume.'
        ]
      });
    } finally {
      setQuestionsLoading(false);
    }
  };

  const handleCopyQuestions = () => {
    if (!questionsData) return;
    const lines: string[] = [];
    if (questionsData.technical_questions?.length) {
      lines.push('--- TECHNICAL QUESTIONS ---');
      questionsData.technical_questions.forEach((q: string, i: number) => lines.push(`${i + 1}. ${q}`));
    }
    if (questionsData.behavioral_questions?.length) {
      lines.push('\n--- BEHAVIORAL QUESTIONS ---');
      questionsData.behavioral_questions.forEach((q: string, i: number) => lines.push(`${i + 1}. ${q}`));
    }
    if (questionsData.project_questions?.length) {
      lines.push('\n--- PROJECT QUESTIONS ---');
      questionsData.project_questions.forEach((q: string, i: number) => lines.push(`${i + 1}. ${q}`));
    }
    navigator.clipboard.writeText(lines.join('\n'));
    setCopied(true);
    setTimeout(() => setCopied(false), 2500);
  };

  // Filter candidates by status and search query
  const filteredCandidates = candidates.filter((cand) => {
    if (statusFilter !== 'ALL' && cand.status?.toUpperCase() !== statusFilter.toUpperCase()) {
      return false;
    }
    if (searchQuery.trim()) {
      const q = searchQuery.toLowerCase();
      const matchName = cand.name?.toLowerCase().includes(q);
      const matchSkills = cand.matched_skills?.some((s) => s.toLowerCase().includes(q));
      const matchTitle = cand.current_title?.toLowerCase().includes(q);
      const matchLoc = cand.location?.toLowerCase().includes(q);
      if (!matchName && !matchSkills && !matchTitle && !matchLoc) {
        return false;
      }
    }
    return true;
  });

  const shortlistedCount = candidates.filter((c) => c.status === 'SHORTLISTED').length;
  const interviewCount = candidates.filter((c) => c.status === 'INTERVIEW').length;
  const reviewCount = candidates.filter((c) => !c.status || c.status === 'APPLIED').length;
  const rejectedCount = candidates.filter((c) => c.status === 'REJECTED').length;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-white mb-1">Applicant Review & AI Shortlisting</h1>
          <p className="text-sm text-slate-400">
            Review candidates who applied to your open jobs, ranked by multi-signal AI matching.
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-2.5">
          {selectedCandidateIds.length >= 2 && (
            <Button variant="secondary" size="sm" onClick={handleLaunchComparison}>
              <GitCompare className="w-3.5 h-3.5 mr-1.5" />
              Compare Selected ({selectedCandidateIds.length})
            </Button>
          )}
          <Button 
            variant="secondary" 
            size="sm" 
            onClick={handleSeedApplicants}
            disabled={!selectedJobId}
            title="Adds 4 sample applicants with realistic profiles to test AI ranking and shortlisting"
          >
            <Plus className="w-3.5 h-3.5 mr-1.5 text-indigo-400" />
            + Add 4 Demo Applicants
          </Button>
          <Button 
            variant="primary" 
            size="sm" 
            onClick={handleAutoShortlist} 
            disabled={candidates.length === 0}
          >
            <Sparkles className="w-3.5 h-3.5 mr-1.5 text-amber-300" />
            Auto-Shortlist Top Matches (≥75%)
          </Button>
        </div>
      </div>

      {/* Message & Error alerts */}
      {message && (
        <div className={`p-4 rounded-xl border text-sm flex items-center gap-3 ${
          message.type === 'success' 
            ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-300' 
            : 'bg-rose-500/10 border-rose-500/30 text-rose-300'
        }`}>
          <CheckCircle2 className="w-5 h-5 flex-shrink-0" />
          <span>{message.text}</span>
        </div>
      )}

      {error && (
        <div className="p-4 rounded-xl bg-rose-500/10 border border-rose-500/20 text-rose-300 text-sm flex items-center gap-3">
          <AlertCircle className="w-5 h-5 flex-shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* Job Selection & Filters Card */}
      <Card className="p-5 space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {/* Job Selector */}
          <div className="md:col-span-2">
            <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">
              Select Job Opening
            </label>
            <select
              value={selectedJobId}
              onChange={(e) => {
                setSelectedJobId(e.target.value);
                setSearchParams({ jobId: e.target.value });
              }}
              className="w-full px-3.5 py-2.5 bg-slate-950 border border-slate-700 rounded-xl text-white text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
            >
              <option value="">-- Choose Job Opening --</option>
              {jobs.map((j) => (
                <option key={j.id} value={j.id}>
                  {j.title} ({j.department} • {j.location}) — {j.applicant_count || 0} applied
                </option>
              ))}
            </select>
          </div>

          {/* Search Applicant */}
          <div>
            <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">
              Search Applicants
            </label>
            <div className="relative">
              <Search className="w-4 h-4 absolute left-3.5 top-3 text-slate-500" />
              <input
                type="text"
                placeholder="Name, skill, or title..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-9 pr-3.5 py-2.5 bg-slate-950 border border-slate-700 rounded-xl text-white text-sm placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
            </div>
          </div>
        </div>

        {/* Quick Stats & Status Tabs */}
        <div className="pt-3 border-t border-slate-800 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          {/* Status Tabs */}
          <div className="flex flex-wrap items-center gap-2">
            <button
              onClick={() => setStatusFilter('ALL')}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition ${
                statusFilter === 'ALL'
                  ? 'bg-indigo-600 text-white'
                  : 'bg-slate-800/80 text-slate-400 hover:text-white'
              }`}
            >
              All Applicants ({candidates.length})
            </button>
            <button
              onClick={() => setStatusFilter('SHORTLISTED')}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition flex items-center gap-1.5 ${
                statusFilter === 'SHORTLISTED'
                  ? 'bg-emerald-600 text-white'
                  : 'bg-slate-800/80 text-emerald-400 hover:text-white'
              }`}
            >
              <span className="w-2 h-2 rounded-full bg-emerald-400" />
              Shortlisted ({shortlistedCount})
            </button>
            <button
              onClick={() => setStatusFilter('INTERVIEW')}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition flex items-center gap-1.5 ${
                statusFilter === 'INTERVIEW'
                  ? 'bg-purple-600 text-white'
                  : 'bg-slate-800/80 text-purple-400 hover:text-white'
              }`}
            >
              <span className="w-2 h-2 rounded-full bg-purple-400" />
              Interview ({interviewCount})
            </button>
            <button
              onClick={() => setStatusFilter('APPLIED')}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition flex items-center gap-1.5 ${
                statusFilter === 'APPLIED'
                  ? 'bg-sky-600 text-white'
                  : 'bg-slate-800/80 text-sky-400 hover:text-white'
              }`}
            >
              <span className="w-2 h-2 rounded-full bg-sky-400" />
              Under Review ({reviewCount})
            </button>
            <button
              onClick={() => setStatusFilter('REJECTED')}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition flex items-center gap-1.5 ${
                statusFilter === 'REJECTED'
                  ? 'bg-rose-600 text-white'
                  : 'bg-slate-800/80 text-rose-400 hover:text-white'
              }`}
            >
              <span className="w-2 h-2 rounded-full bg-rose-400" />
              Rejected ({rejectedCount})
            </button>
          </div>

          <div className="text-xs text-slate-400 flex items-center gap-2">
            <span>Showing <strong className="text-white">{filteredCandidates.length}</strong> candidates</span>
          </div>
        </div>
      </Card>

      {/* Loading state */}
      {loading && (
        <div className="flex flex-col items-center justify-center min-h-[30vh] space-y-3">
          <div className="animate-spin w-8 h-8 border-4 border-indigo-500 border-t-transparent rounded-full" />
          <span className="text-xs text-slate-400">Evaluating multi-signal AI candidate matching...</span>
        </div>
      )}

      {/* Empty State */}
      {!loading && candidates.length === 0 && (
        <Card className="p-12 text-center">
          <Users className="w-12 h-12 mx-auto text-slate-600 mb-3" />
          <h3 className="text-base font-semibold text-white">No applicants found for this position</h3>
          <p className="text-xs text-slate-400 mt-1 mb-5 max-w-md mx-auto">
            Candidates who submit their application and resume for this job will be ranked here automatically.
            You can also add 4 demo applicants to test the AI ranking right now.
          </p>
          <div className="flex items-center justify-center gap-3">
            <Button variant="primary" size="md" onClick={handleSeedApplicants}>
              <Plus className="w-4 h-4 mr-2" />
              Add 4 Demo Applicants
            </Button>
            <Link to="/recruiter/jobs">
              <Button variant="ghost" size="md">
                View All Jobs
              </Button>
            </Link>
          </div>
        </Card>
      )}

      {/* Candidate List / Cards */}
      {!loading && filteredCandidates.length > 0 && (
        <div className="space-y-3">
          {filteredCandidates.map((cand) => {
            const isSelected = selectedCandidateIds.includes(cand.candidate_id);
            const score = Math.round(cand.final_score);
            const status = cand.status?.toUpperCase() || 'APPLIED';

            return (
              <Card 
                key={cand.candidate_id} 
                className={`p-5 transition border ${
                  isSelected 
                    ? 'border-indigo-500 bg-indigo-950/20' 
                    : 'border-slate-800 hover:border-slate-700 bg-slate-900/60'
                }`}
              >
                <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
                  {/* Left: Rank, Checkbox & Candidate Info */}
                  <div className="flex items-start gap-3.5">
                    <div className="flex flex-col items-center gap-2 pt-1">
                      <input
                        type="checkbox"
                        checked={isSelected}
                        onChange={() => toggleSelectCandidate(cand.candidate_id)}
                        className="w-4 h-4 rounded border-slate-700 text-indigo-600 focus:ring-indigo-500 bg-slate-950 cursor-pointer"
                        title="Select to compare"
                      />
                      <span
                        className={`inline-flex items-center justify-center w-7 h-7 rounded-full font-bold text-xs ${
                          cand.rank === 1
                            ? 'bg-amber-500/20 text-amber-300 border border-amber-500/30'
                            : cand.rank === 2
                            ? 'bg-slate-300/20 text-slate-200 border border-slate-400/30'
                            : cand.rank === 3
                            ? 'bg-amber-700/20 text-amber-500 border border-amber-700/30'
                            : 'bg-slate-800 text-slate-400'
                        }`}
                      >
                        #{cand.rank}
                      </span>
                    </div>

                    <div className="space-y-1">
                      <div className="flex flex-wrap items-center gap-2.5">
                        <h3 className="text-base font-bold text-white">{cand.name}</h3>
                        
                        {/* Status Badge */}
                        {status === 'SHORTLISTED' && (
                          <Badge variant="success">Shortlisted</Badge>
                        )}
                        {status === 'INTERVIEW' && (
                          <Badge variant="warning">Interview</Badge>
                        )}
                        {status === 'REJECTED' && (
                          <Badge variant="danger">Rejected</Badge>
                        )}
                        {status === 'APPLIED' && (
                          <Badge variant="neutral">Under Review</Badge>
                        )}
                      </div>

                      <div className="text-xs text-slate-400 flex flex-wrap items-center gap-x-3 gap-y-1">
                        <span>{cand.current_title || 'Software Engineer'}</span>
                        {cand.current_company && (
                          <>
                            <span>•</span>
                            <span>{cand.current_company}</span>
                          </>
                        )}
                        <span>•</span>
                        <span className="flex items-center gap-1">
                          <Briefcase className="w-3 h-3" />
                          {cand.years_of_experience} yrs exp
                        </span>
                        <span>•</span>
                        <span className="flex items-center gap-1">
                          <MapPin className="w-3 h-3" />
                          {cand.location || 'Remote'}
                        </span>
                      </div>

                      {/* Contact Info (if available) */}
                      {(cand.email || cand.phone) && (
                        <div className="flex flex-wrap items-center gap-3 text-[11px] text-slate-500 pt-0.5">
                          {cand.email && (
                            <span className="flex items-center gap-1">
                              <Mail className="w-3 h-3 text-slate-400" />
                              {cand.email}
                            </span>
                          )}
                          {cand.phone && (
                            <span className="flex items-center gap-1">
                              <Phone className="w-3 h-3 text-slate-400" />
                              {cand.phone}
                            </span>
                          )}
                        </div>
                      )}

                      {/* Matched Skills */}
                      <div className="flex flex-wrap gap-1.5 pt-2">
                        {cand.matched_skills && cand.matched_skills.slice(0, 5).map((s, idx) => (
                          <span
                            key={idx}
                            className="px-2 py-0.5 rounded text-[11px] font-medium bg-indigo-500/10 text-indigo-300 border border-indigo-500/20"
                          >
                            {s}
                          </span>
                        ))}
                        {cand.matched_skills && cand.matched_skills.length > 5 && (
                          <span className="text-[10px] text-slate-500 self-center">
                            +{cand.matched_skills.length - 5} more
                          </span>
                        )}
                      </div>
                    </div>
                  </div>

                  {/* Middle: AI Match Fit Score */}
                  <div className="flex lg:flex-col items-center justify-between lg:justify-center p-3 lg:p-4 bg-slate-950/80 rounded-xl border border-slate-800 lg:min-w-[170px]">
                    <div className="flex items-baseline gap-1.5">
                      <span
                        className={`text-2xl font-black ${
                          score >= 80
                            ? 'text-emerald-400'
                            : score >= 65
                            ? 'text-indigo-400'
                            : 'text-amber-400'
                        }`}
                      >
                        {score}%
                      </span>
                      <span className="text-[11px] text-slate-400 font-semibold">AI Match</span>
                    </div>

                    <div className="w-28 bg-slate-800 rounded-full h-1.5 mt-1 overflow-hidden">
                      <div
                        className={`h-full rounded-full ${
                          score >= 80
                            ? 'bg-emerald-400'
                            : score >= 65
                            ? 'bg-indigo-400'
                            : 'bg-amber-400'
                        }`}
                        style={{ width: `${score}%` }}
                      />
                    </div>

                    <div className="flex items-center gap-3 text-[10px] text-slate-400 mt-2 font-mono">
                      <span>Sem: {Math.round(cand.semantic_score)}%</span>
                      <span>•</span>
                      <span>Keyw: {Math.round(cand.keyword_score)}%</span>
                    </div>
                  </div>

                  {/* Right: Actions */}
                  <div className="flex flex-wrap lg:flex-col items-center lg:items-end gap-2 pt-2 lg:pt-0">
                    <div className="flex items-center gap-1.5">
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => setActiveResumeCandidate(cand)}
                        title="View applicant resume text and background details"
                      >
                        <FileText className="w-3.5 h-3.5 mr-1" />
                        Resume
                      </Button>
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => setActiveModalCandidate(cand)}
                        title="Inspect grounded AI matching evidence and rationale"
                      >
                        <Eye className="w-3.5 h-3.5 mr-1" />
                        Evidence
                      </Button>
                      <Button
                        variant="secondary"
                        size="sm"
                        onClick={() => handleOpenQuestions(cand)}
                        title="Generate tailored AI interview questions for this applicant"
                      >
                        <Sparkles className="w-3.5 h-3.5 mr-1 text-amber-300" />
                        AI Questions
                      </Button>
                    </div>

                    <div className="flex items-center gap-1.5 mt-1">
                      {status !== 'SHORTLISTED' && (
                        <Button
                          variant="primary"
                          size="sm"
                          onClick={() => handleUpdateStatus(cand.candidate_id, 'SHORTLISTED')}
                          className="bg-emerald-600 hover:bg-emerald-500 text-white"
                        >
                          <UserCheck className="w-3.5 h-3.5 mr-1" />
                          Shortlist
                        </Button>
                      )}
                      {status !== 'INTERVIEW' && (
                        <Button
                          variant="secondary"
                          size="sm"
                          onClick={() => handleUpdateStatus(cand.candidate_id, 'INTERVIEW')}
                          className="text-purple-300 border-purple-800/60 hover:bg-purple-950/30"
                        >
                          <Calendar className="w-3.5 h-3.5 mr-1" />
                          Interview
                        </Button>
                      )}
                      {status !== 'REJECTED' && (
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => handleUpdateStatus(cand.candidate_id, 'REJECTED')}
                          className="text-slate-400 hover:text-rose-400"
                        >
                          <XCircle className="w-3.5 h-3.5 mr-1" />
                          Reject
                        </Button>
                      )}
                    </div>
                  </div>
                </div>
              </Card>
            );
          })}
        </div>
      )}

      {/* MODAL 1: AI Generated Interview Questions */}
      {activeQuestionsCandidate && (
        <Modal
          isOpen={Boolean(activeQuestionsCandidate)}
          onClose={() => setActiveQuestionsCandidate(null)}
          title={`AI Interview Questions — ${activeQuestionsCandidate.name}`}
          size="lg"
        >
          <div className="space-y-5 text-slate-300 text-xs">
            <div className="flex items-center justify-between p-3.5 bg-slate-950 rounded-xl border border-slate-800">
              <div>
                <span className="text-white font-semibold text-sm">{activeQuestionsCandidate.name}</span>
                <span className="text-slate-400 block text-[11px]">
                  {activeQuestionsCandidate.current_title || 'Software Engineer'} • AI Match: {Math.round(activeQuestionsCandidate.final_score)}%
                </span>
              </div>
              <Button variant="secondary" size="sm" onClick={handleCopyQuestions} disabled={questionsLoading}>
                {copied ? (
                  <>
                    <Check className="w-3.5 h-3.5 mr-1 text-emerald-400" />
                    Copied!
                  </>
                ) : (
                  <>
                    <Copy className="w-3.5 h-3.5 mr-1" />
                    Copy Questions
                  </>
                )}
              </Button>
            </div>

            {questionsLoading ? (
              <div className="flex flex-col items-center justify-center py-10 space-y-3">
                <div className="animate-spin w-7 h-7 border-3 border-indigo-500 border-t-transparent rounded-full" />
                <span className="text-xs text-slate-400">Synthesizing tailored interview questions using Gemini AI...</span>
              </div>
            ) : questionsData ? (
              <div className="space-y-4 max-h-[60vh] overflow-y-auto pr-1">
                {/* Technical Questions */}
                {questionsData.technical_questions?.length > 0 && (
                  <div className="p-4 rounded-xl bg-slate-950/80 border border-slate-800 space-y-2.5">
                    <h4 className="text-xs font-bold text-indigo-300 uppercase tracking-wider flex items-center gap-1.5">
                      <Cpu className="w-3.5 h-3.5" />
                      Technical & Architecture Deep Dive
                    </h4>
                    <ol className="list-decimal list-inside space-y-2 text-slate-200 leading-relaxed">
                      {questionsData.technical_questions.map((q: string, idx: number) => (
                        <li key={idx} className="pl-1">
                          <span>{q}</span>
                        </li>
                      ))}
                    </ol>
                  </div>
                )}

                {/* Behavioral Questions */}
                {questionsData.behavioral_questions?.length > 0 && (
                  <div className="p-4 rounded-xl bg-slate-950/80 border border-slate-800 space-y-2.5">
                    <h4 className="text-xs font-bold text-emerald-300 uppercase tracking-wider flex items-center gap-1.5">
                      <Users className="w-3.5 h-3.5" />
                      Behavioral & Teamwork Alignment
                    </h4>
                    <ol className="list-decimal list-inside space-y-2 text-slate-200 leading-relaxed">
                      {questionsData.behavioral_questions.map((q: string, idx: number) => (
                        <li key={idx} className="pl-1">
                          <span>{q}</span>
                        </li>
                      ))}
                    </ol>
                  </div>
                )}

                {/* Project Questions */}
                {questionsData.project_questions?.length > 0 && (
                  <div className="p-4 rounded-xl bg-slate-950/80 border border-slate-800 space-y-2.5">
                    <h4 className="text-xs font-bold text-amber-300 uppercase tracking-wider flex items-center gap-1.5">
                      <Award className="w-3.5 h-3.5" />
                      Resume Project & Impact Probing
                    </h4>
                    <ol className="list-decimal list-inside space-y-2 text-slate-200 leading-relaxed">
                      {questionsData.project_questions.map((q: string, idx: number) => (
                        <li key={idx} className="pl-1">
                          <span>{q}</span>
                        </li>
                      ))}
                    </ol>
                  </div>
                )}
              </div>
            ) : null}
          </div>
        </Modal>
      )}

      {/* MODAL 2: View Resume & Profile */}
      {activeResumeCandidate && (
        <Modal
          isOpen={Boolean(activeResumeCandidate)}
          onClose={() => setActiveResumeCandidate(null)}
          title={`Candidate Resume — ${activeResumeCandidate.name}`}
          size="lg"
        >
          <div className="space-y-4 text-slate-300 text-xs">
            <div className="p-4 bg-slate-950 rounded-xl border border-slate-800 grid grid-cols-1 sm:grid-cols-3 gap-3">
              <div>
                <span className="text-[10px] text-slate-500 uppercase tracking-wider block">Full Name</span>
                <span className="text-sm font-bold text-white">{activeResumeCandidate.name}</span>
              </div>
              <div>
                <span className="text-[10px] text-slate-500 uppercase tracking-wider block">Contact</span>
                <span className="text-xs text-slate-300">{activeResumeCandidate.email || 'Not provided'}</span>
                {activeResumeCandidate.phone && (
                  <span className="block text-slate-400">{activeResumeCandidate.phone}</span>
                )}
              </div>
              <div>
                <span className="text-[10px] text-slate-500 uppercase tracking-wider block">Experience</span>
                <span className="text-xs text-white font-semibold">
                  {activeResumeCandidate.years_of_experience} years • {activeResumeCandidate.location || 'Remote'}
                </span>
              </div>
            </div>

            {/* Matched Skills */}
            {activeResumeCandidate.matched_skills && activeResumeCandidate.matched_skills.length > 0 && (
              <div>
                <span className="text-[11px] font-semibold text-slate-400 block mb-1.5">Technical Skills</span>
                <div className="flex flex-wrap gap-1.5">
                  {activeResumeCandidate.matched_skills.map((s, idx) => (
                    <span
                      key={idx}
                      className="px-2.5 py-1 rounded-md text-xs font-medium bg-slate-800 text-indigo-300 border border-slate-700"
                    >
                      {s}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* Resume Text */}
            <div>
              <span className="text-[11px] font-semibold text-slate-400 block mb-1.5">Submitted Resume Content</span>
              <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 max-h-[40vh] overflow-y-auto whitespace-pre-wrap font-mono text-[11px] text-slate-300 leading-relaxed">
                {activeResumeCandidate.raw_resume_text || 
                  `${activeResumeCandidate.name} is an experienced professional with ${activeResumeCandidate.years_of_experience} years in ${activeResumeCandidate.current_title || 'Software Engineering'}.\n\nKey Skills: ${activeResumeCandidate.matched_skills?.join(', ') || 'N/A'}\n\nCandidate submitted this application through the portal.`}
              </div>
            </div>

            {/* Modal actions */}
            <div className="flex items-center justify-end gap-2 pt-2 border-t border-slate-800">
              <Button
                variant="primary"
                size="sm"
                onClick={() => {
                  handleUpdateStatus(activeResumeCandidate.candidate_id, 'SHORTLISTED');
                  setActiveResumeCandidate(null);
                }}
              >
                <UserCheck className="w-3.5 h-3.5 mr-1" />
                Shortlist Candidate
              </Button>
            </div>
          </div>
        </Modal>
      )}

      {/* MODAL 3: Grounded Match Evidence */}
      {activeModalCandidate && (
        <Modal
          isOpen={Boolean(activeModalCandidate)}
          onClose={() => setActiveModalCandidate(null)}
          title={`Explainable Match Evidence — ${activeModalCandidate.name}`}
          size="lg"
        >
          <div className="space-y-6 text-slate-300 text-xs">
            {/* Top Stat Row */}
            <div className="grid grid-cols-3 gap-3 p-4 bg-slate-950 rounded-xl border border-slate-800">
              <div>
                <span className="text-slate-400 block uppercase tracking-wider text-[10px]">Rank Position</span>
                <span className="text-xl font-bold text-white">#{activeModalCandidate.rank}</span>
              </div>
              <div>
                <span className="text-slate-400 block uppercase tracking-wider text-[10px]">Overall Match</span>
                <span className="text-xl font-bold text-indigo-400">
                  {Math.round(activeModalCandidate.final_score)}%
                </span>
              </div>
              <div>
                <span className="text-slate-400 block uppercase tracking-wider text-[10px]">Experience Fit</span>
                <span className="text-xl font-bold text-emerald-400">
                  {activeModalCandidate.years_of_experience} yrs
                </span>
              </div>
            </div>

            {/* Why candidate ranked here */}
            <div>
              <h4 className="text-sm font-semibold text-white mb-2 flex items-center gap-1.5">
                <Sparkles className="w-4 h-4 text-indigo-400" />
                Ranking Rationale & Grounded Evidence
              </h4>
              <div className="p-3.5 rounded-xl bg-slate-950/80 border border-slate-800 leading-relaxed text-slate-300">
                {activeModalCandidate.explanation?.why_ranked ||
                  `Candidate demonstrates strong semantic alignment (${Math.round(
                    activeModalCandidate.semantic_score
                  )}%) and overlaps across core technical requirements.`}
              </div>
            </div>

            {/* Strengths and Gaps Split */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div className="p-3.5 rounded-xl bg-emerald-950/20 border border-emerald-800/40 space-y-2">
                <h5 className="font-semibold text-emerald-300 flex items-center gap-1.5">
                  <CheckCircle2 className="w-4 h-4" />
                  Key Strengths
                </h5>
                <ul className="space-y-1 text-slate-300">
                  {activeModalCandidate.explanation?.strengths &&
                  activeModalCandidate.explanation.strengths.length > 0 ? (
                    activeModalCandidate.explanation.strengths.map((st: string, idx: number) => (
                      <li key={idx} className="flex items-start gap-1.5">
                        <span className="text-emerald-400 font-bold">•</span>
                        <span>{st}</span>
                      </li>
                    ))
                  ) : (
                    <li>Strong technical alignment across target stack.</li>
                  )}
                </ul>
              </div>

              <div className="p-3.5 rounded-xl bg-rose-950/20 border border-rose-800/40 space-y-2">
                <h5 className="font-semibold text-rose-300 flex items-center gap-1.5">
                  <XCircle className="w-4 h-4" />
                  Skill Gaps & Deliberation
                </h5>
                <ul className="space-y-1 text-slate-300">
                  {activeModalCandidate.explanation?.skill_gaps &&
                  activeModalCandidate.explanation.skill_gaps.length > 0 ? (
                    activeModalCandidate.explanation.skill_gaps.map((gap: string, idx: number) => (
                      <li key={idx} className="flex items-start gap-1.5">
                        <span className="text-rose-400 font-bold">•</span>
                        <span>{gap}</span>
                      </li>
                    ))
                  ) : (
                    <li>No critical skill gaps identified.</li>
                  )}
                </ul>
              </div>
            </div>

            {/* Signal Weights Table */}
            <div>
              <h5 className="font-semibold text-white mb-2">Normalized Multi-Signal Decomposition</h5>
              <div className="grid grid-cols-4 gap-2 text-center text-[11px]">
                <div className="p-2 bg-slate-950 rounded-lg border border-slate-800">
                  <span className="text-slate-400 block">Dense Vector</span>
                  <strong className="text-white font-mono">{Math.round(activeModalCandidate.semantic_score)}%</strong>
                </div>
                <div className="p-2 bg-slate-950 rounded-lg border border-slate-800">
                  <span className="text-slate-400 block">Sparse BM25</span>
                  <strong className="text-white font-mono">{Math.round(activeModalCandidate.keyword_score)}%</strong>
                </div>
                <div className="p-2 bg-slate-950 rounded-lg border border-slate-800">
                  <span className="text-slate-400 block">Skill Match</span>
                  <strong className="text-white font-mono">{Math.round(activeModalCandidate.skill_score)}%</strong>
                </div>
                <div className="p-2 bg-slate-950 rounded-lg border border-slate-800">
                  <span className="text-slate-400 block">Experience Fit</span>
                  <strong className="text-white font-mono">{Math.round(activeModalCandidate.experience_score)}%</strong>
                </div>
              </div>
            </div>
          </div>
        </Modal>
      )}
    </div>
  );
};
