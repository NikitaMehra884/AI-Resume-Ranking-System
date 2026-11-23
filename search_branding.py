import os, re, sys
root = r"C:/Projects/AI Resume Ranking System"
patterns = [r"TalentIntelligence", r"AI Resume Ranking System", r"logo"]
matches = []
for dirpath, _, filenames in os.walk(root):
    for f in filenames:
        if f.lower().endswith(('.ts', '.tsx', '.js', '.jsx', '.py', '.md')):
            path = os.path.join(dirpath, f)
            try:
                with open(path, 'r', encoding='utf-8') as fh:
                    for i, line in enumerate(fh, 1):
                        for pat in patterns:
                            if pat in line:
                                matches.append(f"{path}:{i}: {line.strip()}")
            except Exception as e:
                pass
for m in matches:
    print(m)
