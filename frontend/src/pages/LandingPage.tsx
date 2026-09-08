import React from 'react';
import { Link } from 'react-router-dom';
import { 
  Sparkles, 
  Search, 
  Sliders, 
  BarChart3, 
  ShieldCheck, 
  Cpu, 
  ArrowRight, 
  CheckCircle2, 
  Users, 
  Briefcase 
} from 'lucide-react';
import Button from '../components/common/Button';

export const LandingPage: React.FC = () => {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col selection:bg-indigo-500 selection:text-white">
      {/* Top Navigation */}
      <nav className="border-b border-slate-800/80 bg-slate-950/70 backdrop-blur-md sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-600 to-violet-500 flex items-center justify-center shadow-lg shadow-indigo-500/25">
              <Sparkles className="w-5 h-5 text-white" />
            </div>
            <div>
              <span className="text-lg font-bold bg-gradient-to-r from-white via-slate-200 to-indigo-300 bg-clip-text text-transparent">
                TalentIntelligence
              </span>
              <span className="hidden sm:inline-block ml-2 text-xs px-2 py-0.5 rounded-full bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 font-mono">
                v2.0
              </span>
            </div>
          </div>

          <div className="flex items-center space-x-3">
            <Link to="/login">
              <Button variant="ghost" size="sm">Sign In</Button>
            </Link>
            <Link to="/register">
              <Button variant="primary" size="sm">Get Started</Button>
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="relative pt-20 pb-28 overflow-hidden">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_80%_60%_at_50%_-20%,rgba(99,102,241,0.25),rgba(255,255,255,0))] pointer-events-none" />
        
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 text-center relative z-10">
          <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-300 text-xs font-semibold mb-6">
            <Cpu className="w-3.5 h-3.5" />
            Production 4-Stage Hybrid Retrieval & Multi-Signal Ranking
          </div>

          <h1 className="text-4xl sm:text-6xl lg:text-7xl font-extrabold tracking-tight text-white mb-6">
            Intelligent Hiring at Scale with{' '}
            <span className="bg-gradient-to-r from-indigo-400 via-violet-300 to-pink-400 bg-clip-text text-transparent">
              Explainable AI
            </span>
          </h1>

          <p className="text-lg sm:text-xl text-slate-400 max-w-3xl mx-auto mb-10 leading-relaxed">
            Move beyond brittle keyword filters. Discover, score, and rank 100,000+ candidates in milliseconds using 
            SentenceTransformers dense vectors, normalized BM25 lexical signals, and grounded LLM evidence.
          </p>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 max-w-md mx-auto">
            <Link to="/login" className="w-full sm:w-auto">
              <Button variant="primary" size="lg" className="w-full shadow-xl shadow-indigo-600/30">
                Sign In to Platform
                <ArrowRight className="w-4 h-4 ml-2" />
              </Button>
            </Link>
            <Link to="/register" className="w-full sm:w-auto">
              <Button variant="secondary" size="lg" className="w-full">
                Create Free Account
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Feature Highlights Grid */}
      <section className="py-20 border-t border-slate-800/80 bg-slate-900/40">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-3xl mx-auto mb-16">
            <h2 className="text-3xl font-bold text-white mb-4">
              Enterprise-Grade AI Talent Architecture
            </h2>
            <p className="text-slate-400">
              Designed from ground up with mathematical normalization, multi-signal weighting, and ethical debiasing.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="p-6 rounded-2xl bg-slate-900/90 border border-slate-800 hover:border-indigo-500/50 transition-all">
              <div className="w-12 h-12 rounded-xl bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center mb-4">
                <Search className="w-6 h-6 text-indigo-400" />
              </div>
              <h3 className="text-xl font-semibold text-white mb-2">4-Stage Hybrid Pipeline</h3>
              <p className="text-sm text-slate-400 leading-relaxed">
                Stage 1 hard eligibility filters prevent role mismatch, followed by FAISS dense vector search and BM25Okapi sparse lexical retrieval over 100,000 candidate profiles.
              </p>
            </div>

            <div className="p-6 rounded-2xl bg-slate-900/90 border border-slate-800 hover:border-indigo-500/50 transition-all">
              <div className="w-12 h-12 rounded-xl bg-violet-500/10 border border-violet-500/20 flex items-center justify-center mb-4">
                <Sliders className="w-6 h-6 text-violet-400" />
              </div>
              <h3 className="text-xl font-semibold text-white mb-2">Normalized Multi-Signal Scoring</h3>
              <p className="text-sm text-slate-400 leading-relaxed">
                Strict [0, 100] normalization across 8 distinct signals: Semantic relevance, Exact keywords, Required skills, Preferred skills, Experience seniority, Education tier, and Career trajectory.
              </p>
            </div>

            <div className="p-6 rounded-2xl bg-slate-900/90 border border-slate-800 hover:border-indigo-500/50 transition-all">
              <div className="w-12 h-12 rounded-xl bg-pink-500/10 border border-pink-500/20 flex items-center justify-center mb-4">
                <ShieldCheck className="w-6 h-6 text-pink-400" />
              </div>
              <h3 className="text-xl font-semibold text-white mb-2">Grounded & Ethical AI</h3>
              <p className="text-sm text-slate-400 leading-relaxed">
                Zero hallucination guarantee: Match explanations cite exact candidate skills and experience gaps. Strict demographic exclusion ensures fair and unbiased evaluation.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="mt-auto border-t border-slate-800 py-8 bg-slate-950 text-center text-xs text-slate-500">
        <p>© 2026 AI Recruitment Intelligence Platform • Designed for High-Throughput Enterprise Hiring</p>
      </footer>
    </div>
  );
};
