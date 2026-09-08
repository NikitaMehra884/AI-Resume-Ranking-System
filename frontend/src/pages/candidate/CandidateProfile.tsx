import React, { useState, useEffect } from 'react';
import api from '../../services/api';
import { CandidateProfile as ProfileType } from '../../types';
import Card from '../../components/common/Card';
import Button from '../../components/common/Button';
import Badge from '../../components/common/Badge';
import { User, Briefcase, MapPin, Plus, X, Save, AlertCircle, CheckCircle2 } from 'lucide-react';

export const CandidateProfile: React.FC = () => {
  const [profile, setProfile] = useState<ProfileType | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);
  const [newSkill, setNewSkill] = useState('');

  useEffect(() => {
    fetchProfile();
  }, []);

  const fetchProfile = async () => {
    try {
      const res = await api.get('/candidates/me');
      setProfile(res.data);
    } catch (err: any) {
      setError('Failed to load profile.');
    } finally {
      setLoading(false);
    }
  };

  const handleAddSkill = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newSkill.trim() || !profile) return;
    const exists = profile.skills.some(
      (s) => s.name.toLowerCase() === newSkill.trim().toLowerCase()
    );
    if (!exists) {
      setProfile({
        ...profile,
        skills: [...profile.skills, { name: newSkill.trim() }]
      });
    }
    setNewSkill('');
  };

  const handleRemoveSkill = (skillName: string) => {
    if (!profile) return;
    setProfile({
      ...profile,
      skills: profile.skills.filter((s) => s.name !== skillName)
    });
  };

  const handleSave = async () => {
    if (!profile) return;
    setSaving(true);
    setError(null);
    setSuccess(false);

    try {
      await api.put('/candidates/me', {
        full_name: profile.full_name,
        headline: profile.headline,
        summary: profile.summary,
        years_of_experience: profile.years_of_experience,
        current_title: profile.current_title,
        current_company: profile.current_company,
        location: profile.location,
        skills: profile.skills
      });
      setSuccess(true);
      setTimeout(() => setSuccess(false), 3000);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to update profile.');
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[50vh]">
        <div className="animate-spin w-8 h-8 border-4 border-indigo-500 border-t-transparent rounded-full" />
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-white mb-1">My Professional Profile</h1>
          <p className="text-sm text-slate-400">
            Keep your technical credentials, experience, and skills up to date for ranking algorithms.
          </p>
        </div>
        <Button variant="primary" size="md" onClick={handleSave} loading={saving}>
          <Save className="w-4 h-4 mr-1.5" />
          Save Changes
        </Button>
      </div>

      {error && (
        <div className="p-4 rounded-xl bg-rose-500/10 border border-rose-500/20 text-rose-300 text-sm flex items-center gap-3">
          <AlertCircle className="w-5 h-5 flex-shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {success && (
        <div className="p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/20 text-emerald-300 text-sm flex items-center gap-3">
          <CheckCircle2 className="w-5 h-5 flex-shrink-0" />
          <span>Profile saved successfully!</span>
        </div>
      )}

      {profile && (
        <div className="space-y-6">
          {/* Basic Info */}
          <Card className="p-6 space-y-5">
            <h3 className="text-base font-semibold text-white border-b border-slate-800 pb-3">
              General Information
            </h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">
                  Full Name
                </label>
                <input
                  type="text"
                  value={profile.full_name || ''}
                  onChange={(e) => setProfile({ ...profile, full_name: e.target.value })}
                  className="w-full px-3.5 py-2.5 bg-slate-950 border border-slate-700 rounded-lg text-white text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">
                  Years of Experience
                </label>
                <input
                  type="number"
                  step="0.5"
                  value={profile.years_of_experience || 0}
                  onChange={(e) =>
                    setProfile({ ...profile, years_of_experience: parseFloat(e.target.value) || 0 })
                  }
                  className="w-full px-3.5 py-2.5 bg-slate-950 border border-slate-700 rounded-lg text-white text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">
                  Current Title / Designation
                </label>
                <input
                  type="text"
                  value={profile.current_title || ''}
                  onChange={(e) => setProfile({ ...profile, current_title: e.target.value })}
                  className="w-full px-3.5 py-2.5 bg-slate-950 border border-slate-700 rounded-lg text-white text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">
                  Current Company
                </label>
                <input
                  type="text"
                  value={profile.current_company || ''}
                  onChange={(e) => setProfile({ ...profile, current_company: e.target.value })}
                  className="w-full px-3.5 py-2.5 bg-slate-950 border border-slate-700 rounded-lg text-white text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>

              <div className="sm:col-span-2">
                <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">
                  Headline / One-Liner
                </label>
                <input
                  type="text"
                  value={profile.headline || ''}
                  onChange={(e) => setProfile({ ...profile, headline: e.target.value })}
                  placeholder="e.g. Senior Machine Learning Engineer specializing in NLP & Distributed Training"
                  className="w-full px-3.5 py-2.5 bg-slate-950 border border-slate-700 rounded-lg text-white text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>

              <div className="sm:col-span-2">
                <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">
                  Location
                </label>
                <input
                  type="text"
                  value={profile.location || ''}
                  onChange={(e) => setProfile({ ...profile, location: e.target.value })}
                  placeholder="e.g. San Francisco, CA / Bengaluru, India"
                  className="w-full px-3.5 py-2.5 bg-slate-950 border border-slate-700 rounded-lg text-white text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>
            </div>
          </Card>

          {/* Skills Management */}
          <Card className="p-6 space-y-4">
            <h3 className="text-base font-semibold text-white border-b border-slate-800 pb-3">
              Skills & Proficiencies ({profile.skills.length})
            </h3>
            
            <form onSubmit={handleAddSkill} className="flex gap-3">
              <input
                type="text"
                value={newSkill}
                onChange={(e) => setNewSkill(e.target.value)}
                placeholder="Add a new skill (e.g. PyTorch, Kubernetes, TypeScript)..."
                className="flex-1 px-3.5 py-2.5 bg-slate-950 border border-slate-700 rounded-lg text-white text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
              <Button type="submit" variant="secondary" size="md">
                <Plus className="w-4 h-4 mr-1" />
                Add Skill
              </Button>
            </form>

            <div className="flex flex-wrap gap-2 pt-2">
              {profile.skills.map((skill, idx) => (
                <span
                  key={idx}
                  className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium bg-slate-800 text-slate-200 border border-slate-700 hover:border-slate-600 transition"
                >
                  {skill.name}
                  <button
                    type="button"
                    onClick={() => handleRemoveSkill(skill.name)}
                    className="text-slate-400 hover:text-rose-400 transition"
                  >
                    <X className="w-3.5 h-3.5" />
                  </button>
                </span>
              ))}
            </div>
          </Card>
        </div>
      )}
    </div>
  );
};
