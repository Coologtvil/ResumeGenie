from typing import Dict, List
from agents.granite_client import safe_generate
import subprocess
import os


def _format_local_resume(master_profile: Dict, job: Dict, projects: List[Dict]) -> str:
    lines: List[str] = []
    lines.append(f"# Resume Target: {job.get('title')}")
    lines.append(f"Company: {job.get('company')}")
    lines.append(f"Name: {master_profile.get('name','')}")
    lines.append(f"Email: {master_profile.get('email','')}")
    lines.append(f"LinkedIn: {master_profile.get('linkedin','')}")
    lines.append(f"GitHub: https://github.com/{master_profile.get('github_username','')}")
    # Add bigger summary section (include bio if present)
    summary = master_profile.get('summary', '')
    bio = master_profile.get('bio', '')
    if summary or bio:
        lines.append(f"\n## Summary\n{summary}\n{bio}")
    lines.append("\n## Key Skills\n" + ", ".join(sorted(set(master_profile.get("skills", [])))))
    if projects:
        lines.append("\n## Relevant Projects")
        for p in projects:
            desc = (p.get("description") or "")[:80]
            lines.append(f"- {p.get('name',p.get('title',''))}: {desc}")
    lines.append("\n## Education")
    for edu in master_profile.get("education", []):
        lines.append(f"- {edu.get('degree','')} in {edu.get('field','')} at {edu.get('institution','')} ({edu.get('startDate','')}–{edu.get('endDate','')}) | {edu.get('location','')}")
        if edu.get('gpa'): lines.append(f"  GPA: {edu['gpa']}")
        if edu.get('achievements'): lines.append(f"  Achievements: {', '.join(edu['achievements'])}")
    # Certifications section (LaTeX format)
    lines.append("\n## Certifications (LaTeX format)")
    certs = master_profile.get("certifications", [])
    if certs:
        for cert in certs:
            lines.append(f"\\textbf{{{cert.get('name','')}}} -- {cert.get('issuer','')} \\hfill {cert.get('date','')} \\")
            lines.append(f"\\href{{{cert.get('link','')}}}{{Certificate Link}} \\")
    else:
        lines.append("- None")
    # Experience section
    lines.append("\n## Experience (Action → Context → Result)")
    for exp in master_profile.get("experience", []):
        lines.append(f"- Action: {exp['action']}\n  Context: {exp['context']}\n  Result: {exp['result']}")
    return "\n".join(lines)

def build_granite_resume(master_profile: Dict, job: Dict, projects: List[Dict]) -> str:
    sr = open("samp_res.tex", "r", encoding="utf-8").read()
    # Compose education and certifications for prompt
    edu_lines = []
    for edu in master_profile.get("education", []):
        line = f"{edu.get('degree','')} in {edu.get('field','')} at {edu.get('institution','')} ({edu.get('startDate','')}–{edu.get('endDate','')})"
        if edu.get('gpa'): line += f", GPA: {edu['gpa']}"
        edu_lines.append(line)
    cert_lines = []
    for cert in master_profile.get("certifications", []):
        cert_lines.append(f"{cert.get('name','')} ({cert.get('issuer','')}, {cert.get('date','')}) [{cert.get('link','')}]")
    # Experience lines
    exp_lines = []
    for exp in master_profile.get("experience", []):
        exp_lines.append(f"Action: {exp['action']}, Context: {exp['context']}, Result: {exp['result']}")
    # Bigger summary (include bio if present)
    summary = master_profile.get('summary', '')
    bio = master_profile.get('bio', '')
    full_summary = summary + (' ' + bio if bio else '')
    prompt = f"""
You are an ATS optimization assistant and a skilled LaTeX resume writer. Generate a tailored resume using the sample_resume.tex template.
OUTPUT A COMPLETE LaTeX document with this EXACT structure present in the sample below: {', '.join(sr.splitlines())}
Change the content to reflect the JOB DESCRIPTION and the CANDIDATE SKILLS and PROJECTS provided.
JOB TITLE: {job.get('title')}
COMPANY: {job.get('company')}
NAME: {master_profile.get('name','')}
EMAIL: {master_profile.get('email','')}
LINKEDIN: {master_profile.get('linkedin','')}
GITHUB: https://github.com/{master_profile.get('github_username','')}
SUMMARY: {full_summary}
JOB DESCRIPTION:
{job.get('description','')[:1500]}
EXPERIENCE: {'; '.join(exp_lines)}
CANDIDATE SKILLS: {', '.join(master_profile.get('skills', []))}
EDUCATION: {'; '.join(edu_lines)}
CERTIFICATIONS: {'; '.join(cert_lines)}
PROJECTS:
{'; '.join([p.get('name',p.get('title','')) + ': ' + (p.get('description','')[:120]) for p in projects])}

CERTIFICATIONS: List all certifications with name, issuer, date, and link. This section MUST appear in the output, formatted as in the sample template.

Output COMPLETE LaTeX Code with sections:
1. Summary (2+ sentences)
2. Core Skills (comma separated)
3. Education (chronological, include university name, all entries)
4. Certifications (chronological, all entries)
5. Achievements (Action → Context → Result bullets) (3-5 items)
6. Contact Info (name, email, linkedin, github)
Use only real candidate skills.

Ensure the LaTeX compiles without errors and conflicts.
"""
    generated = safe_generate(prompt)
    # Post-process: ensure certifications section is present and document ends properly
    certs = master_profile.get("certifications", [])
    cert_block = ""
    if certs:
        cert_lines_latex = []
        for cert in certs:
            cert_lines_latex.append(f"\\textbf{{{cert.get('name','')}}} -- {cert.get('issuer','')} \\hfill {cert.get('date','')} \\")
            cert_lines_latex.append(f"\\href{{{cert.get('link','')}}}{{Certificate Link}} \\")
        cert_block = "\\section*{Certifications}\n" + "\n".join(cert_lines_latex) + "\n"
    # If certifications section is present but truncated, replace it
    if '\\section*{Certifications}' in generated:
        cert_start = generated.find('\\section*{Certifications}')
        doc_end = generated.find('\\end{document}', cert_start)
        if doc_end != -1:
            generated = generated[:cert_start] + cert_block + generated[doc_end:]
        else:
            generated = generated[:cert_start] + cert_block + '\n\\end{document}\n'
    elif cert_block:
        # If missing, append before \end{document}
        if '\\end{document}' in generated:
            generated = generated.replace('\\end{document}', cert_block + '\\end{document}')
        else:
            generated += cert_block + '\n\\end{document}\n'
    # Ensure document ends properly
    if '\\end{document}' not in generated:
        generated += '\n\\end{document}\n'
    if not generated:
        return _format_local_resume(master_profile, job, projects)
    if '\\documentclass' in generated:
        generated = '\\documentclass' + generated.split('\\documentclass', 1)[1]
    generated = generated.replace('\\usepackage{XCharter}', '% XCharter removed for compatibility')
    generated = generated.replace('\\usepackage[T1]{fontenc}', '')
    if '\\begin{itemize}' in generated and generated.count('\\begin{itemize}') > generated.count('\\end{itemize}'):
        if '\\end{document}' in generated:
            generated = generated.replace('\\end{document}', '\\end{itemize}\n\n\\end{document}')
        else:
            generated += '\n\\end{itemize}\n'
    if '\\end{document}' not in generated:
        generated += '\n\n\\end{document}\n'
    generated = generated.replace('[Contact Info]', '')
    generated = generated.replace('[Candidate Name]', master_profile.get('name','Professional'))
    job_id = job.get('id', 'temp').replace('/', '_')
    tex_file = f'resume_{job_id}.tex'
    pdf_file = f'resume_{job_id}.pdf'
    try:
        with open(tex_file, 'w', encoding='utf-8') as f:
            f.write(generated)
        print(f"[INFO] LaTeX saved to {tex_file}")
        try:
            result = subprocess.run(
                ['pdflatex', '-interaction=nonstopmode', tex_file],
                capture_output=True,
                timeout=30,
                cwd='.',
                text=True
            )
            if result.returncode == 0 and os.path.exists(pdf_file):
                print(f"[SUCCESS] PDF generated: {pdf_file}")
            else:
                print(f"[WARN] PDFLaTeX failed: {result.stderr[:200]}")
        except FileNotFoundError:
            print(f"[WARN] pdflatex not found in PATH")
        except Exception as pdf_err:
            print(f"[WARN] PDF generation failed: {pdf_err}")
    except Exception as e:
        print(f"[ERROR] Could not save resume: {e}")
    return generated


def build_cheat_sheet(master_profile: Dict, job: Dict) -> Dict:
    return {
        "job_id": job.get("id"),
        "years_experience": master_profile.get("years_experience"),
        "primary_stack": ", ".join(master_profile.get("skills", [])[:5]),
        "work_auth": master_profile.get("work_auth"),
        "salary_expectation": master_profile.get("salary_expectation", "Negotiable"),
    }
