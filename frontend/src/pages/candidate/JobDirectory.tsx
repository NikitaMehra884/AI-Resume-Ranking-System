import React, { useState, useEffect } from 'react';
import api from '../../services/api';
import { Job } from '../../types';
import Card from '../../components/common/Card';
import Button from '../../components/common/Button';
import Badge from '../../components/common/Badge';
import Modal from '../../components/common/Modal';
import { 
  Search, 
  MapPin, 
  Briefcase, 
  Clock, 
  CheckCircle2, 
  Send,
  AlertCircle,
  Upload,
  User,
  Phone,
  Mail,
  GraduationCap
} from 'lucide-react';

export const JobDirectory: React.FC = () => {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedDept, setSelectedDept] = useState('ALL');
  const [appliedJobIds, setAppliedJobIds] = useState<Set<number>>(new Set());
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);

  // Application Modal state
  const [activeApplyJob, setActiveApplyJob] = useState<Job | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const [parsingResume, setParsingResume] = useState(false);
  const [parseStatus, setParseStatus] = useState<string | null>(null);
  const [resumeText, setResumeText] = useState('');

  // Application Form fields
  const [fullName, setFullName] = useState('');
  const [email, setEmail] = useState('');
  const [phone, setPhone] = useState('');
  const [currentTitle, setCurrentTitle] = useState('');
  const [yearsExperience, setYearsExperience] = useState('2.0');
  const [skills, setSkills] = useState('');
  const [education, setEducation] = useState('');
  const [coverNote, setCoverNote] = useState('');

  useEffect(() => {
    fetchJobs();
    loadCandidateProfile();
  }, []);

  const fetchJobs = async () => {
    try {
      const res = await api.get('/jobs/');
      setJobs(res.data);
      const appRes = await api.get('/candidates/my-applications');
      const applied = new Set<number>(appRes.data.map((a: any) => a.job_id));
      setAppliedJobIds(applied);
    } catch (err: any) {
      // ignore
    } finally {
      setLoading(false);
    }
  };

  const loadCandidateProfile = async () => {
    try {
      const res = await api.get('/candidates/me');
      if (res.data) {
        setFullName(res.data.full_name || '');
        setCurrentTitle(res.data.current_title || '');
        setYearsExperience(String(res.data.years_of_experience || 2.0));
        if (res.data.skills) {
          const sList = res.data.skills.map((s: any) => s.name || s).join(', ');
          setSkills(sList);
        }
      }
      const userStr = localStorage.getItem('user');
      if (userStr) {
        const u = JSON.parse(userStr);
        setEmail(u.email || '');
      }
    } catch {
      // ignore if profile not created yet
    }
  };

  const handleOpenApplyModal = (job: Job) => {
    setActiveApplyJob(job);
    setParseStatus(null);
  };

  const handleResumeFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files || !e.target.files[0]) return;
    const file = e.target.files[0];
    setParsingResume(true);
    setParseStatus('Analyzing resume and extracting skills...');

    try {
      const formData = new FormData();
      formData.append('file', file);
      const res = await api.post('/candidates/parse-resume', formData);
      const data = res.data;
      if (data.full_name && !fullName) setFullName(data.full_name);
      if (data.email && !email) setEmail(data.email);
      if (data.phone) setPhone(data.phone);
      if (data.current_title) setCurrentTitle(data.current_title);
      if (data.years_of_experience) setYearsExperience(String(data.years_of_experience));
      if (data.skills && data.skills.length > 0) {
        const extracted = data.skills.map((s: any) => typeof s === 'string' ? s : s.name).join(', ');
        setSkills(extracted);
      }
      if (data.raw_text) setResumeText(data.raw_text);
      setParseStatus(`Extracted ${data.skills?.length || 0} skills & ${data.years_of_experience || 0} yrs experience.`);
    } catch (err: any) {
      setParseStatus('Could not auto-parse file. You can enter details manually.');
    } finally {
      setParsingResume(false);
    }
  };

  const handleSubmitApplication = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!activeApplyJob) return;

    if (!fullName.trim() || !skills.trim()) {
      alert('Please provide your Full Name and at least one Skill.');
      return;
    }

    setSubmitting(true);
    try {
      const payload = {
        full_name: fullName,
        email: email,
        phone: phone,
        current_title: currentTitle,
        years_of_experience: parseFloat(yearsExperience) || 0.0,
        skills: skills,
        education: education,
        cover_note: coverNote,
        resume_text: resumeText || `${fullName} - ${currentTitle}. Skills: ${skills}. Experience: ${yearsExperience} years.`
      };

      const res = await api.post(`/jobs/${activeApplyJob.id}/apply`, payload);
      setAppliedJobIds((prev) => new Set(prev).add(activeApplyJob.id));
      const score = res.data.match_score || 85;
      setMessage({
        type: 'success',
        text: `Application submitted for "${activeApplyJob.title}"! AI evaluated your match score at ${score}%. You can track your shortlisting status in My Applications.`
      });
      setActiveApplyJob(null);
      setTimeout(() => setMessage(null), 6000);
    } catch (err: any) {
      alert(err.response?.data?.detail || 'Failed to submit application.');
    } finally {
      setSubmitting(false);
    }
  };

  const departments = ['ALL', ...Array.from(new Set(jobs.map((j) => j.department).filter(Boolean)))];

  const filteredJobs = jobs.filter((job) => {
    const matchesSearch =
      job.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      job.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
      job.location.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesDept = selectedDept === 'ALL' || job.department === selectedDept;
    return matchesSearch && matchesDept;
  });

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-white mb-1">Open Positions Directory</h1>
          <p className="text-sm text-slate-400">
            Explore active openings and apply directly with your verified AI candidate profile.
          </p>
        </div>
      </div>

      {message && (
        <div
          className={`p-4 rounded-xl text-sm flex items-center gap-3 ${
            message.type === 'success'
              ? 'bg-emerald-500/10 border border-emerald-500/20 text-emerald-300'
              : 'bg-rose-500/10 border border-rose-500/20 text-rose-300'
          }`}
        >
          {message.type === 'success' ? (
            <CheckCircle2 className="w-5 h-5 flex-shrink-0" />
          ) : (
            <AlertCircle className="w-5 h-5 flex-shrink-0" />
          )}
          <span>{message.text}</span>
        </div>
      )}

      {/* Search & Filter bar */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="sm:col-span-2 relative">
          <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-3.5" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search by job title, skill keywords, or location..."
            className="w-full pl-10 pr-4 py-2.5 bg-slate-900 border border-slate-700 rounded-xl text-white placeholder-slate-500 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
        </div>

        <div>
          <select
            value={selectedDept}
            onChange={(e) => setSelectedDept(e.target.value)}
            className="w-full px-3.5 py-2.5 bg-slate-900 border border-slate-700 rounded-xl text-white text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
          >
            {departments.map((dept) => (
              <option key={dept} value={dept}>
                {dept === 'ALL' ? 'All Departments' : dept}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Jobs Grid */}
      {loading ? (
        <div className="flex items-center justify-center min-h-[40vh]">
          <div className="animate-spin w-8 h-8 border-4 border-indigo-500 border-t-transparent rounded-full" />
        </div>
      ) : filteredJobs.length === 0 ? (
        <div className="text-center py-16 border border-dashed border-slate-800 rounded-2xl">
          <Briefcase className="w-12 h-12 mx-auto text-slate-600 mb-3" />
          <p className="text-base font-semibold text-slate-300">No matching jobs found</p>
          <p className="text-xs text-slate-500 mt-1">Try adjusting your keyword search or department filter.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {filteredJobs.map((job) => {
            const isApplied = appliedJobIds.has(job.id);
            return (
              <Card key={job.id} className="p-6 flex flex-col justify-between hover:border-indigo-500/50 transition">
                <div>
                  <div className="flex items-start justify-between gap-3 mb-3">
                    <div>
                      <h3 className="text-lg font-bold text-white">{job.title}</h3>
                      <p className="text-xs text-indigo-400 font-medium mt-0.5">
                        {job.company_name || 'Redrob AI'} • {job.department}
                      </p>
                    </div>
                    <Badge variant="primary">{job.work_mode}</Badge>
                  </div>

                  <div className="flex flex-wrap items-center gap-x-4 gap-y-2 text-xs text-slate-400 mb-4">
                    <span className="flex items-center gap-1">
                      <MapPin className="w-3.5 h-3.5" />
                      {job.location}
                    </span>
                    <span className="flex items-center gap-1">
                      <Briefcase className="w-3.5 h-3.5" />
                      {job.minimum_experience} - {job.maximum_experience} yrs
                    </span>
                    <span className="flex items-center gap-1">
                      <Clock className="w-3.5 h-3.5" />
                      {job.employment_type || 'Full-time'}
                    </span>
                  </div>

                  <p className="text-xs text-slate-300 line-clamp-3 mb-4 leading-relaxed">
                    {job.description}
                  </p>

                  {/* Skills badges */}
                  <div className="space-y-2 mb-4">
                    <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block">
                      Required Skills:
                    </span>
                    <div className="flex flex-wrap gap-1.5">
                      {job.skills && job.skills.length > 0 ? (
                        job.skills.slice(0, 6).map((skill, sIdx) => (
                          <span
                            key={sIdx}
                            className={`px-2 py-0.5 rounded text-[11px] font-medium ${
                              skill.is_required
                                ? 'bg-indigo-500/10 text-indigo-300 border border-indigo-500/20'
                                : 'bg-slate-800 text-slate-400 border border-slate-700'
                            }`}
                          >
                            {skill.name}
                          </span>
                        ))
                      ) : (
                        <span className="text-xs text-slate-500">General software engineering</span>
                      )}
                    </div>
                  </div>
                </div>

                <div className="pt-4 border-t border-slate-800 flex items-center justify-between">
                  <span className="text-xs text-slate-500">
                    Posted {new Date(job.created_at).toLocaleDateString()}
                  </span>
                  <Button
                    variant={isApplied ? 'ghost' : 'primary'}
                    size="sm"
                    disabled={isApplied}
                    onClick={() => handleOpenApplyModal(job)}
                  >
                    {isApplied ? (
                      <>
                        <CheckCircle2 className="w-3.5 h-3.5 mr-1 text-emerald-400" />
                        Applied
                      </>
                    ) : (
                      <>
                        <Send className="w-3.5 h-3.5 mr-1" />
                        Apply Now
                      </>
                    )}
                  </Button>
                </div>
              </Card>
            );
          })}
        </div>
      )}

      {/* Interactive Application Modal */}
      {activeApplyJob && (
        <Modal
          isOpen={true}
          onClose={() => setActiveApplyJob(null)}
          title={`Apply for ${activeApplyJob.title}`}
          maxWidth="max-w-2xl"
        >
          <form onSubmit={handleSubmitApplication} className="space-y-4">
            <div className="p-3.5 rounded-xl bg-indigo-950/40 border border-indigo-800/40 text-xs text-indigo-300">
              <span className="font-semibold text-white">{activeApplyJob.title}</span> ({activeApplyJob.department}) • Requires {activeApplyJob.minimum_experience}+ yrs experience
            </div>

            {/* Resume Upload Box */}
            <div className="p-4 rounded-xl bg-slate-900 border border-slate-800 space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-xs font-semibold text-slate-300 uppercase tracking-wider flex items-center gap-1.5">
                  <Upload className="w-3.5 h-3.5 text-indigo-400" />
                  Attach Resume (PDF / DOCX / TXT)
                </span>
                {parsingResume && (
                  <span className="text-xs text-indigo-400 animate-pulse">Analyzing resume...</span>
                )}
              </div>

              <input
                type="file"
                accept=".pdf,.docx,.txt"
                onChange={handleResumeFileUpload}
                className="w-full text-xs text-slate-400 file:mr-3 file:py-1.5 file:px-3 file:rounded-lg file:border-0 file:text-xs file:font-medium file:bg-indigo-600 file:text-white hover:file:bg-indigo-500 cursor-pointer"
              />

              {parseStatus && (
                <div className="text-xs text-emerald-400 flex items-center gap-1.5">
                  <CheckCircle2 className="w-3.5 h-3.5" />
                  <span>{parseStatus}</span>
                </div>
              )}
            </div>

            {/* Form Fields */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1">
                  Full Name *
                </label>
                <div className="relative">
                  <User className="w-4 h-4 text-slate-500 absolute left-3 top-2.5" />
                  <input
                    type="text"
                    required
                    value={fullName}
                    onChange={(e) => setFullName(e.target.value)}
                    placeholder="Candidate Name"
                    className="w-full pl-9 pr-3 py-2 bg-slate-950 border border-slate-700 rounded-lg text-white text-xs focus:ring-2 focus:ring-indigo-500"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1">
                  Email Address *
                </label>
                <div className="relative">
                  <Mail className="w-4 h-4 text-slate-500 absolute left-3 top-2.5" />
                  <input
                    type="email"
                    required
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="email@example.com"
                    className="w-full pl-9 pr-3 py-2 bg-slate-950 border border-slate-700 rounded-lg text-white text-xs focus:ring-2 focus:ring-indigo-500"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1">
                  Phone Number
                </label>
                <div className="relative">
                  <Phone className="w-4 h-4 text-slate-500 absolute left-3 top-2.5" />
                  <input
                    type="text"
                    value={phone}
                    onChange={(e) => setPhone(e.target.value)}
                    placeholder="+91 98765 43210"
                    className="w-full pl-9 pr-3 py-2 bg-slate-950 border border-slate-700 rounded-lg text-white text-xs focus:ring-2 focus:ring-indigo-500"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1">
                  Current Title / Role
                </label>
                <input
                  type="text"
                  value={currentTitle}
                  onChange={(e) => setCurrentTitle(e.target.value)}
                  placeholder="e.g. Software Engineer / Student"
                  className="w-full px-3 py-2 bg-slate-950 border border-slate-700 rounded-lg text-white text-xs focus:ring-2 focus:ring-indigo-500"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1">
                  Years of Experience
                </label>
                <input
                  type="number"
                  step="0.5"
                  value={yearsExperience}
                  onChange={(e) => setYearsExperience(e.target.value)}
                  placeholder="3.0"
                  className="w-full px-3 py-2 bg-slate-950 border border-slate-700 rounded-lg text-white text-xs focus:ring-2 focus:ring-indigo-500"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1">
                  Education / College
                </label>
                <div className="relative">
                  <GraduationCap className="w-4 h-4 text-slate-500 absolute left-3 top-2.5" />
                  <input
                    type="text"
                    value={education}
                    onChange={(e) => setEducation(e.target.value)}
                    placeholder="B.Tech Computer Science"
                    className="w-full pl-9 pr-3 py-2 bg-slate-950 border border-slate-700 rounded-lg text-white text-xs focus:ring-2 focus:ring-indigo-500"
                  />
                </div>
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">
                Your Skills (comma-separated) *
              </label>
              <input
                type="text"
                required
                value={skills}
                onChange={(e) => setSkills(e.target.value)}
                placeholder="Python, React, FastAPI, Machine Learning, Docker, SQL"
                className="w-full px-3 py-2 bg-slate-950 border border-slate-700 rounded-lg text-white text-xs focus:ring-2 focus:ring-indigo-500"
              />
              <span className="text-[11px] text-slate-500 mt-1 block">
                These skills will be matched by AI against the job requirements.
              </span>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">
                Cover Note / Pitch (optional)
              </label>
              <textarea
                rows={2}
                value={coverNote}
                onChange={(e) => setCoverNote(e.target.value)}
                placeholder="Briefly mention why you are interested in this position..."
                className="w-full px-3 py-2 bg-slate-950 border border-slate-700 rounded-lg text-white text-xs focus:ring-2 focus:ring-indigo-500 resize-none"
              />
            </div>

            <div className="flex items-center justify-end gap-3 pt-3 border-t border-slate-800">
              <Button
                type="button"
                variant="ghost"
                size="sm"
                onClick={() => setActiveApplyJob(null)}
              >
                Cancel
              </Button>
              <Button
                type="submit"
                variant="primary"
                size="sm"
                loading={submitting}
              >
                <Send className="w-3.5 h-3.5 mr-1.5" />
                Submit Application with AI Match
              </Button>
            </div>
          </form>
        </Modal>
      )}
    </div>
  );
};
