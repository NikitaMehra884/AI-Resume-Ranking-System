import React, { useState, useEffect } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import api from '../../services/api';
import Card from '../../components/common/Card';
import Button from '../../components/common/Button';
import Badge from '../../components/common/Badge';
import { 
  GitCompare, 
  ArrowLeft, 
  CheckCircle2, 
  XCircle, 
  Sparkles, 
  Briefcase, 
  MapPin, 
  AlertCircle 
} from 'lucide-react';

export const CandidateComparison: React.FC = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();

  const jobId = searchParams.get('jobId');
  const candidatesParam = searchParams.get('candidates');

  const [comparisonData, setComparisonData] = useState<any | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!jobId || !candidatesParam) {
      setError('Please select candidates to compare.');
      setLoading(false);
      return;
    }

    const fetchComparison = async () => {
      try {
        const candidateIds = candidatesParam.split(',').filter(Boolean);
        const res = await api.post('/screening/compare', {
          job_id: Number(jobId),
          candidate_ids: candidateIds
        });
        setComparisonData(res.data);
      } catch (err: any) {
        setError(err.response?.data?.detail || 'Failed to compare candidates.');
      } finally {
        setLoading(false);
      }
    };

    fetchComparison();
  }, [jobId, candidatesParam]);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[50vh]">
        <div className="animate-spin w-8 h-8 border-4 border-indigo-500 border-t-transparent rounded-full" />
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto space-y-8">
      <div className="flex items-center justify-between">
        <div>
          <button
            onClick={() => navigate(-1)}
            className="inline-flex items-center text-xs text-slate-400 hover:text-white mb-2 transition"
          >
            <ArrowLeft className="w-3.5 h-3.5 mr-1" />
            Back to Screening Table
          </button>
          <h1 className="text-2xl font-bold text-white">Side-by-Side Candidate Comparison</h1>
          <p className="text-sm text-slate-400">
            Compare shortlisted talent across technical skill overlap, seniority, and AI synthesized hiring trade-offs.
          </p>
        </div>
      </div>

      {error && (
        <div className="p-4 rounded-xl bg-rose-500/10 border border-rose-500/20 text-rose-300 text-sm flex items-center gap-3">
          <AlertCircle className="w-5 h-5 flex-shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {comparisonData && (
        <>
          {/* AI Synthesis Card */}
          <Card className="p-6 border-indigo-500/40 bg-gradient-to-r from-indigo-950/30 to-slate-900 space-y-4">
            <div className="flex items-center gap-2 text-indigo-400 font-semibold text-sm">
              <Sparkles className="w-4 h-4" />
              <span>Grounded AI Comparative Evaluation</span>
            </div>
            <p className="text-xs text-slate-300 leading-relaxed">
              {comparisonData.ai_comparison_summary ||
                'Both candidates demonstrate solid foundational credentials, with differentiation in specialized architecture and framework depth.'}
            </p>
            {comparisonData.recommendation && (
              <div className="pt-3 border-t border-slate-800 flex items-start gap-2 text-xs">
                <strong className="text-white flex-shrink-0">Recommendation:</strong>
                <span className="text-indigo-300">{comparisonData.recommendation}</span>
              </div>
            )}
          </Card>

          {/* Side-by-Side Candidate Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {(comparisonData.candidates || []).map((cand: any, idx: number) => {
              const score = Math.round(cand.final_score || 0);
              return (
                <Card key={idx} className="p-6 flex flex-col justify-between space-y-6">
                  <div>
                    {/* Header */}
                    <div className="border-b border-slate-800 pb-4">
                      <div className="flex items-center justify-between mb-2">
                        <Badge variant="primary">Candidate #{idx + 1}</Badge>
                        <span className="text-2xl font-black text-indigo-400">{score}%</span>
                      </div>
                      <h3 className="text-lg font-bold text-white">{cand.name}</h3>
                      <p className="text-xs text-slate-400 mt-0.5">{cand.current_title}</p>
                      <p className="text-xs text-slate-500">{cand.current_company}</p>
                    </div>

                    {/* Stats */}
                    <div className="py-4 border-b border-slate-800 grid grid-cols-2 gap-3 text-xs">
                      <div>
                        <span className="text-slate-400 block text-[10px] uppercase">Experience</span>
                        <strong className="text-white">{cand.years_of_experience} yrs</strong>
                      </div>
                      <div>
                        <span className="text-slate-400 block text-[10px] uppercase">Location</span>
                        <strong className="text-white truncate block">{cand.location}</strong>
                      </div>
                      <div>
                        <span className="text-slate-400 block text-[10px] uppercase">Dense Vector</span>
                        <strong className="text-indigo-300 font-mono">
                          {Math.round(cand.semantic_score || 0)}%
                        </strong>
                      </div>
                      <div>
                        <span className="text-slate-400 block text-[10px] uppercase">Lexical BM25</span>
                        <strong className="text-indigo-300 font-mono">
                          {Math.round(cand.keyword_score || 0)}%
                        </strong>
                      </div>
                    </div>

                    {/* Skills Overlap */}
                    <div className="pt-4 space-y-3">
                      <div>
                        <span className="text-[11px] font-semibold text-emerald-400 uppercase tracking-wider block mb-1.5 flex items-center gap-1">
                          <CheckCircle2 className="w-3.5 h-3.5" />
                          Matched Skills ({cand.matched_skills?.length || 0})
                        </span>
                        <div className="flex flex-wrap gap-1">
                          {cand.matched_skills && cand.matched_skills.map((s: string, sIdx: number) => (
                            <span
                              key={sIdx}
                              className="px-2 py-0.5 rounded text-[10px] bg-emerald-500/10 text-emerald-300 border border-emerald-500/20"
                            >
                              {s}
                            </span>
                          ))}
                        </div>
                      </div>

                      <div>
                        <span className="text-[11px] font-semibold text-rose-400 uppercase tracking-wider block mb-1.5 flex items-center gap-1">
                          <XCircle className="w-3.5 h-3.5" />
                          Skill Gaps ({cand.missing_skills?.length || 0})
                        </span>
                        <div className="flex flex-wrap gap-1">
                          {cand.missing_skills && cand.missing_skills.length > 0 ? (
                            cand.missing_skills.map((s: string, sIdx: number) => (
                              <span
                                key={sIdx}
                                className="px-2 py-0.5 rounded text-[10px] bg-rose-500/10 text-rose-300 border border-rose-500/20"
                              >
                                {s}
                              </span>
                            ))
                          ) : (
                            <span className="text-xs text-slate-500">None detected</span>
                          )}
                        </div>
                      </div>
                    </div>
                  </div>

                  <div className="pt-4 border-t border-slate-800">
                    <Button
                      variant="primary"
                      size="sm"
                      className="w-full"
                      onClick={() => navigate(`/recruiter/pipeline?jobId=${jobId}`)}
                    >
                      Advance Candidate
                    </Button>
                  </div>
                </Card>
              );
            })}
          </div>
        </>
      )}
    </div>
  );
};
