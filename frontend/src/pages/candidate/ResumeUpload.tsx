import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../../services/api';
import Card from '../../components/common/Card';
import Button from '../../components/common/Button';
import Badge from '../../components/common/Badge';
import { 
  Upload, 
  FileText, 
  CheckCircle2, 
  AlertCircle, 
  Sparkles, 
  Save, 
  ArrowRight,
  Briefcase
} from 'lucide-react';

export const ResumeUpload: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [pastedText, setPastedText] = useState('');
  const [loading, setLoading] = useState(false);
  const [parsedData, setParsedData] = useState<any | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [saveSuccess, setSaveSuccess] = useState(false);
  const navigate = useNavigate();

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setError(null);
    }
  };

  const handleParse = async () => {
    if (!file && !pastedText.trim()) {
      setError('Please select a resume file (PDF/DOCX) or paste resume text.');
      return;
    }

    setLoading(true);
    setError(null);
    setSaveSuccess(false);

    try {
      let res;
      if (file) {
        const formData = new FormData();
        formData.append('file', file);
        res = await api.post('/candidates/parse-resume', formData);
      } else {
        res = await api.post('/candidates/parse-resume-text', {
          text: pastedText
        });
      }
      setParsedData(res.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to parse resume. Please ensure the file is valid.');
    } finally {
      setLoading(false);
    }
  };

  const handleSaveToProfile = async () => {
    if (!parsedData) return;
    setLoading(true);
    setError(null);

    try {
      await api.put('/candidates/me', {
        full_name: parsedData.contact_info?.name || 'Candidate',
        current_title: parsedData.current_title || '',
        current_company: parsedData.current_company || '',
        skills: (parsedData.skills || []).map((s: any) => ({ name: typeof s === 'string' ? s : s.name })),
        career_history: parsedData.experience || [],
        education: parsedData.education || []
      });
      setSaveSuccess(true);
      setTimeout(() => {
        navigate('/candidate/profile');
      }, 1500);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to update profile.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      <div>
        <h1 className="text-2xl font-bold text-white mb-1">Resume Parser & Skill Extractor</h1>
        <p className="text-sm text-slate-400">
          Upload your resume in PDF or DOCX format, or paste your raw text. Our AI will automatically extract normalized skills, experience, and contact details.
        </p>
      </div>

      {error && (
        <div className="p-4 rounded-xl bg-rose-500/10 border border-rose-500/20 text-rose-300 text-sm flex items-center gap-3">
          <AlertCircle className="w-5 h-5 flex-shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {saveSuccess && (
        <div className="p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/20 text-emerald-300 text-sm flex items-center gap-3">
          <CheckCircle2 className="w-5 h-5 flex-shrink-0" />
          <span>Profile updated successfully! Redirecting to your profile...</span>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Upload File Box */}
        <Card className="p-6 flex flex-col justify-between">
          <div>
            <h3 className="text-base font-semibold text-white mb-2 flex items-center gap-2">
              <Upload className="w-4 h-4 text-indigo-400" />
              Upload Document
            </h3>
            <p className="text-xs text-slate-400 mb-4">
              Supported formats: PDF, DOCX, TXT (Max 10MB)
            </p>

            <label className="border-2 border-dashed border-slate-700 hover:border-indigo-500 rounded-xl p-8 flex flex-col items-center justify-center cursor-pointer transition bg-slate-950/40">
              <FileText className="w-10 h-10 text-indigo-400 mb-3" />
              <span className="text-sm font-medium text-slate-200 text-center">
                {file ? file.name : 'Click or drag file here'}
              </span>
              <span className="text-xs text-slate-500 mt-1">
                {file ? `${(file.size / 1024).toFixed(1)} KB` : 'PDF or DOCX files'}
              </span>
              <input
                type="file"
                accept=".pdf,.docx,.txt"
                onChange={handleFileChange}
                className="hidden"
              />
            </label>
          </div>

          <Button
            variant="primary"
            size="md"
            className="w-full mt-6"
            onClick={handleParse}
            loading={loading}
            disabled={!file && !pastedText.trim()}
          >
            <Sparkles className="w-4 h-4 mr-2" />
            Extract Profile Signals
          </Button>
        </Card>

        {/* Paste Raw Text Box */}
        <Card className="p-6 flex flex-col justify-between">
          <div>
            <h3 className="text-base font-semibold text-white mb-2 flex items-center gap-2">
              <FileText className="w-4 h-4 text-violet-400" />
              Or Paste Resume Text
            </h3>
            <p className="text-xs text-slate-400 mb-4">
              Directly paste raw text from your CV or LinkedIn export.
            </p>
            <textarea
              rows={8}
              value={pastedText}
              onChange={(e) => {
                setPastedText(e.target.value);
                if (file) setFile(null);
              }}
              placeholder="Paste summary, experience, education, and technical skills..."
              className="w-full p-3 bg-slate-950 border border-slate-700 rounded-xl text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition resize-none font-mono"
            />
          </div>

          <Button
            variant="secondary"
            size="md"
            className="w-full mt-6"
            onClick={handleParse}
            loading={loading}
            disabled={!file && !pastedText.trim()}
          >
            <Sparkles className="w-4 h-4 mr-2" />
            Extract from Text
          </Button>
        </Card>
      </div>

      {/* Parsed Extraction Result Display */}
      {parsedData && (
        <Card className="p-6 border-indigo-500/40 shadow-2xl space-y-6">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800 pb-4">
            <div>
              <Badge variant="primary" className="mb-2">AI Extraction Result</Badge>
              <h2 className="text-xl font-bold text-white">
                {parsedData.contact_info?.name || 'Parsed Candidate Profile'}
              </h2>
              <p className="text-xs text-slate-400 mt-0.5">
                {parsedData.contact_info?.email} • {parsedData.contact_info?.phone || 'No phone'}
              </p>
            </div>
            <Button
              variant="primary"
              size="md"
              onClick={handleSaveToProfile}
              loading={loading}
            >
              <Save className="w-4 h-4 mr-1.5" />
              Save to My Profile
            </Button>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800">
              <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Years Experience</span>
              <p className="text-2xl font-bold text-white mt-1">{parsedData.years_of_experience || 0} yrs</p>
            </div>
            <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800">
              <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Current Role</span>
              <p className="text-base font-semibold text-white mt-1 truncate">{parsedData.current_title || 'Not specified'}</p>
              <p className="text-xs text-slate-400 truncate">{parsedData.current_company}</p>
            </div>
            <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800">
              <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Normalized Skills</span>
              <p className="text-2xl font-bold text-indigo-400 mt-1">{parsedData.skills?.length || 0}</p>
            </div>
          </div>

          {/* Skills Badges */}
          <div>
            <h4 className="text-xs font-semibold text-slate-300 uppercase tracking-wider mb-3">Extracted Skills Taxonomy</h4>
            <div className="flex flex-wrap gap-2">
              {parsedData.skills && parsedData.skills.length > 0 ? (
                parsedData.skills.map((skill: any, idx: number) => {
                  const sName = typeof skill === 'string' ? skill : (skill.name || JSON.stringify(skill));
                  return (
                    <span
                      key={idx}
                      className="px-3 py-1 rounded-lg text-xs font-medium bg-indigo-500/10 border border-indigo-500/20 text-indigo-300"
                    >
                      {sName}
                    </span>
                  );
                })
              ) : (
                <p className="text-xs text-slate-500">No skills recognized.</p>
              )}
            </div>
          </div>
        </Card>
      )}
    </div>
  );
};
