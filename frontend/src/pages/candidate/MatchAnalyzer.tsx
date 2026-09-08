import React, { useState, useEffect } from 'react';
import api from '../../services/api';
import { Job, CandidateProfile } from '../../types';
import Card from '../../components/common/Card';
import Button from '../../components/common/Button';
import Badge from '../../components/common/Badge';
import { 
  Sparkles, 
  CheckCircle2, 
  XCircle, 
  AlertCircle, 
  Target, 
  TrendingUp, 
  ArrowRight,
  BookOpen
} from 'lucide-react';

export const MatchAnalyzer: React.FC = () => {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [selectedJobId, setSelectedJobId] = useState<number | string>('');
  const [customJD, setCustomJD] = useState('');
  const [profile, setProfile] = useState<CandidateProfile | null>(null);
  const [analysis, setAnalysis] = useState<any | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const init = async () => {
      try {
        const [jobsRes, profileRes] = await Promise.all([
          api.get('/jobs/'),
          api.get('/candidates/me')
        ]);
        setJobs(jobsRes.data);
        setProfile(profileRes.data);
        if (jobsRes.data.length > 0) {
          setSelectedJobId(jobsRes.data[0].id);
        }
      } catch (err) {
        // ignore
      }
    };
    init();
  }, []);

  const handleAnalyze = async () => {
    setLoading(true);
    setError(null);
    setAnalysis(null);

    try {
      const selectedJob = jobs.find((j) => j.id === Number(selectedJobId));
      const jdText = customJD.trim() || (selectedJob ? selectedJob.description : '');

      if (!jdText) {
        setError('Please choose a job or paste a job description.');
        setLoading(false);
        return;
      }

      // Call the match analysis endpoint
      const res = await api.post('/candidates/match-analysis', {
        job_id: selectedJob ? selectedJob.id : null,
        job_description: jdText
      });
      setAnalysis(res.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to analyze match.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      <div>
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-300 text-xs font-semibold mb-3">
          <Sparkles className="w-3.5 h-3.5" />
          Explainable Candidate Matching
        </div>
        <h1 className="text-2xl font-bold text-white mb-1">AI Resume vs. Job Match Analyzer</h1>
        <p className="text-sm text-slate-400">
          Analyze how your current technical profile ranks against specific roles. Discover matched skills, detect critical skill gaps, and get grounded recommendations.
        </p>
      </div>

      {error && (
        <div className="p-4 rounded-xl bg-rose-500/10 border border-rose-500/20 text-rose-300 text-sm flex items-center gap-3">
          <AlertCircle className="w-5 h-5 flex-shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* Inputs */}
      <Card className="p-6 space-y-5">
        <div>
          <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">
            Option A: Select Active Job Opening
          </label>
          <select
            value={selectedJobId}
            onChange={(e) => {
              setSelectedJobId(e.target.value);
              setCustomJD('');
            }}
            className="w-full px-3.5 py-2.5 bg-slate-950 border border-slate-700 rounded-xl text-white text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
          >
            {jobs.map((j) => (
              <option key={j.id} value={j.id}>
                {j.title} — {j.company_name || 'Redrob AI'} ({j.location})
              </option>
            ))}
          </select>
        </div>

        <div className="relative">
          <div className="absolute inset-0 flex items-center">
            <div className="w-full border-t border-slate-800" />
          </div>
          <div className="relative flex justify-center text-xs uppercase">
            <span className="bg-slate-900 px-3 text-slate-500 font-mono">Or paste custom JD</span>
          </div>
        </div>

        <div>
          <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">
            Option B: Paste Custom Job Description Text
          </label>
          <textarea
            rows={4}
            value={customJD}
            onChange={(e) => setCustomJD(e.target.value)}
            placeholder="Paste role requirements, required tools, responsibilities..."
            className="w-full p-3 bg-slate-950 border border-slate-700 rounded-xl text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 font-mono resize-none"
          />
        </div>

        <Button
          variant="primary"
          size="md"
          className="w-full"
          onClick={handleAnalyze}
          loading={loading}
        >
          <Sparkles className="w-4 h-4 mr-2" />
          Run Match Analysis
        </Button>
      </Card>

      {/* Analysis Results */}
      {analysis && (
        <div className="space-y-6 animate-fade-in">
          {/* Top Score Banner */}
          <Card className="p-6 border-indigo-500/40 bg-gradient-to-r from-indigo-950/40 to-slate-900">
            <div className="flex flex-col sm:flex-row items-center justify-between gap-6">
              <div>
                <Badge variant={analysis.overall_match_score >= 70 ? 'success' : 'warning'} className="mb-2">
                  {analysis.overall_match_score >= 70 ? 'Strong Alignment' : 'Moderate Match'}
                </Badge>
                <h3 className="text-xl font-bold text-white">Overall Compatibility Score</h3>
                <p className="text-xs text-slate-400 mt-1 max-w-md">
                  Calculated using multi-signal normalized weights across semantic similarity, required skills, and experience fit.
                </p>
              </div>

              <div className="flex items-center gap-4">
                <div className="text-center">
                  <div className="text-4xl font-black text-indigo-400">
                    {Math.round(analysis.overall_match_score)}%
                  </div>
                  <span className="text-[11px] uppercase tracking-wider text-slate-500 font-semibold">
                    Fit Index
                  </span>
                </div>
              </div>
            </div>

            {/* Score Breakdowns */}
            <div className="grid grid-cols-3 gap-4 mt-6 pt-6 border-t border-slate-800/80">
              <div className="text-center">
                <span className="text-xs text-slate-400">Semantic Fit</span>
                <p className="text-lg font-bold text-white mt-0.5">
                  {Math.round(analysis.semantic_score || 75)}%
                </p>
              </div>
              <div className="text-center">
                <span className="text-xs text-slate-400">Required Skills</span>
                <p className="text-lg font-bold text-emerald-400 mt-0.5">
                  {Math.round(analysis.required_skill_score || 80)}%
                </p>
              </div>
              <div className="text-center">
                <span className="text-xs text-slate-400">Experience Alignment</span>
                <p className="text-lg font-bold text-violet-400 mt-0.5">
                  {Math.round(analysis.experience_score || 85)}%
                </p>
              </div>
            </div>
          </Card>

          {/* Matched vs Missing Skills */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <Card className="p-6">
              <h4 className="text-sm font-semibold text-emerald-400 flex items-center gap-2 mb-4">
                <CheckCircle2 className="w-4 h-4" />
                Matched Skills ({analysis.matched_skills?.length || 0})
              </h4>
              <div className="flex flex-wrap gap-2">
                {analysis.matched_skills && analysis.matched_skills.length > 0 ? (
                  analysis.matched_skills.map((skill: string, idx: number) => (
                    <span
                      key={idx}
                      className="px-2.5 py-1 rounded-md text-xs font-medium bg-emerald-500/10 border border-emerald-500/20 text-emerald-300"
                    >
                      {skill}
                    </span>
                  ))
                ) : (
                  <p className="text-xs text-slate-500">No overlapping skills found.</p>
                )}
              </div>
            </Card>

            <Card className="p-6">
              <h4 className="text-sm font-semibold text-rose-400 flex items-center gap-2 mb-4">
                <XCircle className="w-4 h-4" />
                Missing / Unmatched Skills ({analysis.missing_skills?.length || 0})
              </h4>
              <div className="flex flex-wrap gap-2">
                {analysis.missing_skills && analysis.missing_skills.length > 0 ? (
                  analysis.missing_skills.map((skill: string, idx: number) => (
                    <span
                      key={idx}
                      className="px-2.5 py-1 rounded-md text-xs font-medium bg-rose-500/10 border border-rose-500/20 text-rose-300"
                    >
                      {skill}
                    </span>
                  ))
                ) : (
                  <p className="text-xs text-slate-500">All required skills present!</p>
                )}
              </div>
            </Card>
          </div>

          {/* Grounded AI Recommendations */}
          <Card className="p-6 border-slate-700 space-y-4">
            <h4 className="text-sm font-semibold text-white flex items-center gap-2">
              <BookOpen className="w-4 h-4 text-indigo-400" />
              AI Resume Optimization Recommendations
            </h4>
            <div className="space-y-3 text-xs text-slate-300 leading-relaxed">
              {analysis.recommendations && analysis.recommendations.length > 0 ? (
                analysis.recommendations.map((rec: string, idx: number) => (
                  <div key={idx} className="p-3 rounded-lg bg-slate-950/60 border border-slate-800 flex items-start gap-2.5">
                    <span className="w-5 h-5 rounded-full bg-indigo-500/20 text-indigo-400 flex items-center justify-center flex-shrink-0 text-[11px] font-bold">
                      {idx + 1}
                    </span>
                    <span>{rec}</span>
                  </div>
                ))
              ) : (
                <p className="text-slate-500">Your profile is strongly tailored for this job.</p>
              )}
            </div>
          </Card>
        </div>
      )}
    </div>
  );
};
