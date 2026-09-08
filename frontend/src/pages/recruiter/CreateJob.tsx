import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../../services/api';
import Card from '../../components/common/Card';
import Button from '../../components/common/Button';
import Badge from '../../components/common/Badge';
import { Sparkles, Plus, X, Briefcase, Save, ArrowLeft, AlertCircle } from 'lucide-react';

export const CreateJob: React.FC = () => {
  const navigate = useNavigate();
  const [title, setTitle] = useState('');
  const [department, setDepartment] = useState('Engineering');
  const [location, setLocation] = useState('Remote');
  const [workMode, setWorkMode] = useState<'remote' | 'hybrid' | 'onsite'>('remote');
  const [minExp, setMinExp] = useState(3);
  const [maxExp, setMaxExp] = useState(8);
  const [description, setDescription] = useState('');
  const [skills, setSkills] = useState<{ name: string; is_required: boolean }[]>([]);
  const [newSkill, setNewSkill] = useState('');
  const [isSkillRequired, setIsSkillRequired] = useState(true);

  const [parsingJD, setParsingJD] = useState(false);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // AI JD Parser
  const handleAIExtract = async () => {
    if (!description.trim()) {
      setError('Please enter a job description before running AI extraction.');
      return;
    }
    setParsingJD(true);
    setError(null);

    try {
      const res = await api.post('/jobs/extract-skills', {
        text: description,
        title: title || 'Software Engineer'
      });
      const data = res.data;
      const extracted: { name: string; is_required: boolean }[] = [];
      (data.required_skills || []).forEach((s: string) => {
        extracted.push({ name: s, is_required: true });
      });
      (data.preferred_skills || []).forEach((s: string) => {
        extracted.push({ name: s, is_required: false });
      });
      setSkills(extracted);
      if (data.minimum_experience) setMinExp(data.minimum_experience);
      if (data.maximum_experience) setMaxExp(data.maximum_experience);
    } catch (err: any) {
      setError('Failed to extract skills via AI.');
    } finally {
      setParsingJD(false);
    }
  };

  const handleAddSkill = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newSkill.trim()) return;
    const exists = skills.some((s) => s.name.toLowerCase() === newSkill.trim().toLowerCase());
    if (!exists) {
      setSkills([...skills, { name: newSkill.trim(), is_required: isSkillRequired }]);
    }
    setNewSkill('');
  };

  const handleRemoveSkill = (skillName: string) => {
    setSkills(skills.filter((s) => s.name !== skillName));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    setError(null);

    try {
      const payload = {
        title,
        department,
        location,
        work_mode: workMode,
        employment_type: 'Full-time',
        minimum_experience: minExp,
        maximum_experience: maxExp,
        education_requirement: "Bachelor's Degree in Computer Science or related field",
        target_shortlist_count: 20,
        description,
        skills
      };
      const res = await api.post('/jobs/', payload);
      navigate(`/recruiter/screening?jobId=${res.data.id}`);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to create job position.');
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      <div className="flex items-center justify-between">
        <div>
          <button
            onClick={() => navigate(-1)}
            className="inline-flex items-center text-xs text-slate-400 hover:text-white mb-2 transition"
          >
            <ArrowLeft className="w-3.5 h-3.5 mr-1" />
            Back to Dashboard
          </button>
          <h1 className="text-2xl font-bold text-white">Create New Job Position</h1>
          <p className="text-sm text-slate-400">
            Define requirements and leverage AI JD parsing to identify mandatory vs preferred skills.
          </p>
        </div>
      </div>

      {error && (
        <div className="p-4 rounded-xl bg-rose-500/10 border border-rose-500/20 text-rose-300 text-sm flex items-center gap-3">
          <AlertCircle className="w-5 h-5 flex-shrink-0" />
          <span>{error}</span>
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-6">
        <Card className="p-6 space-y-5">
          <h3 className="text-base font-semibold text-white border-b border-slate-800 pb-3">
            Position Details
          </h3>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">
                Job Title *
              </label>
              <input
                type="text"
                required
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                placeholder="e.g. Senior Machine Learning Engineer"
                className="w-full px-3.5 py-2.5 bg-slate-950 border border-slate-700 rounded-lg text-white text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">
                Department
              </label>
              <select
                value={department}
                onChange={(e) => setDepartment(e.target.value)}
                className="w-full px-3.5 py-2.5 bg-slate-950 border border-slate-700 rounded-lg text-white text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
              >
                <option value="Engineering">Engineering</option>
                <option value="AI / Research">AI / Research</option>
                <option value="Product">Product</option>
                <option value="Data & Analytics">Data & Analytics</option>
                <option value="DevOps & Infrastructure">DevOps & Infrastructure</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">
                Location
              </label>
              <input
                type="text"
                value={location}
                onChange={(e) => setLocation(e.target.value)}
                placeholder="e.g. San Francisco, CA / Bengaluru / Remote"
                className="w-full px-3.5 py-2.5 bg-slate-950 border border-slate-700 rounded-lg text-white text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">
                Work Mode
              </label>
              <select
                value={workMode}
                onChange={(e) => setWorkMode(e.target.value as any)}
                className="w-full px-3.5 py-2.5 bg-slate-950 border border-slate-700 rounded-lg text-white text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
              >
                <option value="remote">Remote</option>
                <option value="hybrid">Hybrid</option>
                <option value="onsite">Onsite</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">
                Min Experience (years)
              </label>
              <input
                type="number"
                min="0"
                max="30"
                value={minExp}
                onChange={(e) => setMinExp(parseFloat(e.target.value) || 0)}
                className="w-full px-3.5 py-2.5 bg-slate-950 border border-slate-700 rounded-lg text-white text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">
                Max Experience (years)
              </label>
              <input
                type="number"
                min="0"
                max="30"
                value={maxExp}
                onChange={(e) => setMaxExp(parseFloat(e.target.value) || 0)}
                className="w-full px-3.5 py-2.5 bg-slate-950 border border-slate-700 rounded-lg text-white text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
            </div>
          </div>
        </Card>

        {/* Job Description & AI Parser Button */}
        <Card className="p-6 space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-base font-semibold text-white">Job Description</h3>
            <Button
              type="button"
              variant="secondary"
              size="sm"
              onClick={handleAIExtract}
              loading={parsingJD}
            >
              <Sparkles className="w-3.5 h-3.5 mr-1 text-indigo-400" />
              AI Extract Requirements
            </Button>
          </div>

          <textarea
            rows={8}
            required
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="Paste complete role description, responsibilities, technical requirements, and preferred qualifications..."
            className="w-full p-3.5 bg-slate-950 border border-slate-700 rounded-xl text-white text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 font-mono"
          />
        </Card>

        {/* Skills Tagging */}
        <Card className="p-6 space-y-4">
          <h3 className="text-base font-semibold text-white border-b border-slate-800 pb-3">
            Role Skill Criteria ({skills.length})
          </h3>

          <div className="flex gap-2">
            <input
              type="text"
              value={newSkill}
              onChange={(e) => setNewSkill(e.target.value)}
              placeholder="Skill (e.g. Python, FAISS, PyTorch)..."
              className="flex-1 px-3.5 py-2 bg-slate-950 border border-slate-700 rounded-lg text-white text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
            <select
              value={isSkillRequired ? 'req' : 'pref'}
              onChange={(e) => setIsSkillRequired(e.target.value === 'req')}
              className="px-3 py-2 bg-slate-950 border border-slate-700 rounded-lg text-white text-xs"
            >
              <option value="req">Required</option>
              <option value="pref">Preferred</option>
            </select>
            <Button type="button" variant="secondary" size="md" onClick={handleAddSkill}>
              <Plus className="w-4 h-4 mr-1" />
              Add
            </Button>
          </div>

          <div className="flex flex-wrap gap-2 pt-2">
            {skills.map((s, idx) => (
              <span
                key={idx}
                className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-lg text-xs font-medium border ${
                  s.is_required
                    ? 'bg-indigo-500/10 text-indigo-300 border-indigo-500/30'
                    : 'bg-slate-800 text-slate-300 border-slate-700'
                }`}
              >
                <span>{s.name}</span>
                <span className="text-[10px] opacity-70">({s.is_required ? 'Req' : 'Pref'})</span>
                <button
                  type="button"
                  onClick={() => handleRemoveSkill(s.name)}
                  className="text-slate-400 hover:text-rose-400 transition ml-1"
                >
                  <X className="w-3.5 h-3.5" />
                </button>
              </span>
            ))}
          </div>
        </Card>

        <div className="flex justify-end gap-3">
          <Button type="button" variant="ghost" size="md" onClick={() => navigate(-1)}>
            Cancel
          </Button>
          <Button type="submit" variant="primary" size="md" loading={saving}>
            <Save className="w-4 h-4 mr-1.5" />
            Publish Role & Screen Candidates
          </Button>
        </div>
      </form>
    </div>
  );
};
