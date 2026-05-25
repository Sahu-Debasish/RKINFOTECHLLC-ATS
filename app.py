from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import os, re, json, math
from collections import Counter

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
UPLOAD_FOLDER = '/tmp/ats_uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ─── ATS KEYWORD DATABASE ──────────────────────────────────────────────────────
JOB_KEYWORDS = {
    "Software Engineer": {
        "technical": ["python","java","javascript","typescript","c++","c#","golang","rust","sql","nosql","postgresql","mysql","mongodb","redis","elasticsearch","docker","kubernetes","aws","azure","gcp","git","ci/cd","rest","api","microservices","agile","scrum","algorithms","data structures","system design","oop","tdd","unit testing","react","node.js","html","css","linux","bash"],
        "soft": ["problem solving","team collaboration","communication","leadership","mentoring","code review","documentation"],
        "action_verbs": ["developed","built","designed","implemented","optimized","architected","deployed","maintained","led","collaborated"]
    },
    "Data Scientist": {
        "technical": ["python","r","machine learning","deep learning","tensorflow","pytorch","scikit-learn","pandas","numpy","sql","spark","hadoop","tableau","power bi","statistics","nlp","computer vision","a/b testing","data wrangling","feature engineering","neural networks","xgboost","regression","classification","clustering","time series","jupyter","git","aws","databricks","airflow"],
        "soft": ["analytical thinking","storytelling","communication","research","problem solving","attention to detail"],
        "action_verbs": ["analyzed","predicted","modeled","visualized","trained","evaluated","deployed","researched","discovered","automated"]
    },
    "Product Manager": {
        "technical": ["roadmap","agile","scrum","jira","confluence","user stories","kpi","metrics","a/b testing","sql","google analytics","mixpanel","figma","wireframing","product strategy","go-to-market","ux","market research","competitive analysis","okrs","sprint","backlog","mvp","stakeholder management","data analysis"],
        "soft": ["leadership","communication","strategic thinking","empathy","decision making","prioritization","negotiation","cross-functional"],
        "action_verbs": ["launched","defined","prioritized","collaborated","drove","delivered","managed","led","analyzed","improved"]
    },
    "Marketing Manager": {
        "technical": ["seo","sem","google ads","facebook ads","email marketing","hubspot","salesforce","crm","content marketing","social media","analytics","google analytics","marketing automation","lead generation","campaign management","branding","copywriting","pr","market research","roi","cac","ltv","a/b testing","mailchimp"],
        "soft": ["creativity","communication","leadership","analytical","strategic","collaboration","storytelling"],
        "action_verbs": ["launched","managed","grew","increased","created","developed","drove","executed","optimized","analyzed"]
    },
    "UI/UX Designer": {
        "technical": ["figma","sketch","adobe xd","invision","prototyping","wireframing","user research","usability testing","information architecture","design systems","typography","color theory","responsive design","html","css","after effects","illustrator","photoshop","zeplin","user journey","accessibility","wcag","interaction design","motion design"],
        "soft": ["empathy","creativity","communication","collaboration","attention to detail","problem solving"],
        "action_verbs": ["designed","created","prototyped","researched","tested","improved","collaborated","delivered","redesigned","conducted"]
    },
    "DevOps Engineer": {
        "technical": ["docker","kubernetes","terraform","ansible","jenkins","github actions","aws","azure","gcp","linux","bash","python","ci/cd","infrastructure as code","monitoring","prometheus","grafana","elk stack","nginx","apache","networking","security","ssl","load balancing","scalability","microservices","helm","vagrant","packer","argocd"],
        "soft": ["problem solving","collaboration","communication","reliability engineering","documentation"],
        "action_verbs": ["automated","deployed","built","maintained","optimized","monitored","implemented","designed","migrated","reduced"]
    },
    "Data Analyst": {
        "technical": ["sql","python","r","excel","tableau","power bi","google analytics","statistics","data visualization","etl","data modeling","looker","pandas","numpy","reporting","dashboard","a/b testing","pivot tables","vlookup","regression","hypothesis testing","mysql","postgresql","aws","bigquery","snowflake"],
        "soft": ["analytical thinking","attention to detail","communication","storytelling","problem solving"],
        "action_verbs": ["analyzed","reported","visualized","identified","tracked","monitored","created","developed","automated","presented"]
    },
    "Sales Executive": {
        "technical": ["salesforce","crm","hubspot","lead generation","pipeline management","b2b","saas","cold calling","negotiation","closing","account management","territory management","quota","revenue","prospecting","linkedin sales navigator","forecasting","objection handling"],
        "soft": ["communication","persuasion","resilience","relationship building","goal oriented","self motivated","teamwork"],
        "action_verbs": ["achieved","exceeded","closed","built","managed","grew","developed","negotiated","generated","led"]
    },
    "Human Resources": {
        "technical": ["recruiting","talent acquisition","hris","workday","adp","onboarding","performance management","compensation","benefits","labor law","compliance","learning development","succession planning","employee relations","ats","linkedin recruiter","job descriptions","diversity inclusion","workforce planning"],
        "soft": ["empathy","communication","confidentiality","conflict resolution","leadership","organizational","multitasking"],
        "action_verbs": ["recruited","hired","managed","developed","implemented","facilitated","trained","partnered","improved","supported"]
    },
    "Finance Analyst": {
        "technical": ["financial modeling","excel","bloomberg","tableau","sql","python","accounting","gaap","ifrs","budgeting","forecasting","valuation","dcf","lbo","variance analysis","pivot tables","vba","powerpoint","erp","sap","oracle","quickbooks","financial reporting","audit","risk management"],
        "soft": ["analytical thinking","attention to detail","communication","problem solving","integrity"],
        "action_verbs": ["analyzed","forecasted","modeled","reported","managed","developed","improved","reduced","identified","presented"]
    },
    "Project Manager": {
        "technical": ["pmp","agile","scrum","waterfall","jira","ms project","risk management","budget management","stakeholder management","gantt chart","confluence","resource planning","kpi","milestones","scope management","change management","earned value","prince2","six sigma","lean"],
        "soft": ["leadership","communication","organization","problem solving","negotiation","multitasking","decision making"],
        "action_verbs": ["managed","led","delivered","coordinated","planned","executed","monitored","facilitated","improved","reduced"]
    },
    "Cybersecurity Analyst": {
        "technical": ["penetration testing","siem","splunk","network security","firewall","ids/ips","vulnerability assessment","incident response","malware analysis","owasp","iso 27001","nist","soc","threat intelligence","encryption","pki","oauth","zero trust","cloud security","aws security","ethical hacking","ceh","cissp","comptia security+"],
        "soft": ["analytical thinking","attention to detail","communication","problem solving","continuous learning"],
        "action_verbs": ["secured","monitored","detected","responded","analyzed","implemented","hardened","tested","investigated","remediated"]
    },
    "Machine Learning Engineer": {
        "technical": ["python","tensorflow","pytorch","keras","scikit-learn","mlops","kubeflow","mlflow","feature store","model serving","docker","kubernetes","aws sagemaker","vertex ai","databricks","spark","sql","deep learning","transformers","llm","fine-tuning","rag","vector database","a/b testing","git","ci/cd","rest api"],
        "soft": ["research mindset","problem solving","collaboration","communication","continuous learning"],
        "action_verbs": ["trained","deployed","optimized","built","researched","implemented","reduced","improved","scaled","automated"]
    },
    "Business Analyst": {
        "technical": ["requirements gathering","process mapping","uml","bpmn","sql","excel","tableau","power bi","jira","visio","wireframing","user stories","gap analysis","stakeholder analysis","agile","scrum","data analysis","erp","sap","crm"],
        "soft": ["analytical thinking","communication","facilitation","problem solving","attention to detail","stakeholder management"],
        "action_verbs": ["analyzed","documented","facilitated","identified","improved","managed","collaborated","presented","developed","supported"]
    },
    "Full Stack Developer": {
        "technical": ["javascript","typescript","react","angular","vue","node.js","express","django","flask","spring boot","sql","postgresql","mongodb","redis","docker","kubernetes","aws","git","rest api","graphql","html","css","tailwind","webpack","jest","ci/cd","microservices","linux"],
        "soft": ["problem solving","collaboration","communication","adaptability","attention to detail"],
        "action_verbs": ["built","developed","designed","implemented","deployed","optimized","maintained","collaborated","led","refactored"]
    }
}

# ─── TEXT EXTRACTION ───────────────────────────────────────────────────────────
def extract_text_from_pdf(filepath):
    try:
        import PyPDF2
        text = ""
        with open(filepath, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() or ""
        return text
    except Exception as e:
        return f"PDF extraction error: {e}"

def extract_text_from_docx(filepath):
    try:
        from docx import Document
        doc = Document(filepath)
        return "\n".join([para.text for para in doc.paragraphs])
    except Exception as e:
        return f"DOCX extraction error: {e}"

def extract_text(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    if ext == '.pdf':
        return extract_text_from_pdf(filepath)
    elif ext in ['.docx', '.doc']:
        return extract_text_from_docx(filepath)
    elif ext == '.txt':
        with open(filepath, 'r', errors='ignore') as f:
            return f.read()
    return ""

# ─── ATS ANALYSIS ENGINE ───────────────────────────────────────────────────────
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s\+\#\.]', ' ', text)
    return text

def analyze_resume(resume_text, job_title=None, job_description=None):
    clean = clean_text(resume_text)
    words = clean.split()
    
    results = {}
    
    # 1. Basic Metrics
    results['word_count'] = len(words)
    results['char_count'] = len(resume_text)
    results['page_estimate'] = max(1, round(len(words) / 400))
    
    # 2. Contact Info Check
    email_found = bool(re.search(r'[\w\.-]+@[\w\.-]+\.\w+', resume_text))
    phone_found = bool(re.search(r'[\+\(]?[\d\s\-\(\)]{10,15}', resume_text))
    linkedin_found = bool(re.search(r'linkedin\.com|linkedin', resume_text.lower()))
    github_found = bool(re.search(r'github\.com|github', resume_text.lower()))
    results['contact'] = {
        'email': email_found,
        'phone': phone_found,
        'linkedin': linkedin_found,
        'github': github_found,
        'score': sum([email_found, phone_found, linkedin_found, github_found]) * 25
    }
    
    # 3. Section Detection
    sections = {
        'experience': bool(re.search(r'experience|work history|employment|professional background', clean)),
        'education': bool(re.search(r'education|degree|university|college|bachelor|master|phd', clean)),
        'skills': bool(re.search(r'skills|technologies|tools|competencies|expertise', clean)),
        'summary': bool(re.search(r'summary|objective|profile|about|overview', clean)),
        'projects': bool(re.search(r'projects|portfolio|works', clean)),
        'certifications': bool(re.search(r'certif|certification|license|credential', clean)),
        'achievements': bool(re.search(r'achievement|award|honor|recognition|publication', clean))
    }
    results['sections'] = sections
    results['section_score'] = round((sum(sections.values()) / len(sections)) * 100)
    
    # 4. Action Verbs
    all_action_verbs = set()
    for jd in JOB_KEYWORDS.values():
        all_action_verbs.update(jd['action_verbs'])
    found_verbs = [v for v in all_action_verbs if v in clean]
    results['action_verbs'] = found_verbs[:10]
    results['action_verb_score'] = min(100, len(found_verbs) * 10)
    
    # 5. Quantification Check
    numbers_with_context = re.findall(r'\d+[\%\+]?\s*(?:percent|%|\+|x|times|million|billion|thousand|k\b)', resume_text.lower())
    plain_numbers = re.findall(r'\b\d{2,}\b', resume_text)
    results['quantification_count'] = len(numbers_with_context) + min(5, len(plain_numbers))
    results['quantification_score'] = min(100, results['quantification_count'] * 12)
    
    # 6. ATS Formatting Checks
    formatting_issues = []
    formatting_good = []
    
    if len(words) < 200:
        formatting_issues.append("Resume too short (less than 200 words)")
    else:
        formatting_good.append("Good resume length")
    
    if len(words) > 900:
        formatting_issues.append("Resume may be too long for ATS (>900 words)")
    
    if re.search(r'table|header|footer|text box', clean):
        formatting_issues.append("Complex formatting detected (tables/text boxes may not parse)")
    
    if not email_found:
        formatting_issues.append("No email address detected")
    else:
        formatting_good.append("Email address present")
    
    if not phone_found:
        formatting_issues.append("No phone number detected")
    else:
        formatting_good.append("Phone number present")
    
    special_chars = len(re.findall(r'[★●◆▪→►]', resume_text))
    if special_chars > 10:
        formatting_issues.append(f"Too many special characters ({special_chars}) - may confuse ATS")
    else:
        formatting_good.append("Clean character usage")
    
    results['formatting_issues'] = formatting_issues
    results['formatting_good'] = formatting_good
    results['formatting_score'] = max(0, 100 - len(formatting_issues) * 15)
    
    # 7. Job-Specific Keyword Analysis
    job_score = 0
    job_keywords_found = []
    job_keywords_missing = []
    
    if job_title and job_title in JOB_KEYWORDS:
        kw_data = JOB_KEYWORDS[job_title]
        all_kws = kw_data['technical'] + kw_data['soft']
        for kw in all_kws:
            if kw.lower() in clean:
                job_keywords_found.append(kw)
            else:
                job_keywords_missing.append(kw)
        
        if all_kws:
            job_score = round((len(job_keywords_found) / len(all_kws)) * 100)
    
    results['job_title'] = job_title
    results['job_keywords_found'] = job_keywords_found[:20]
    results['job_keywords_missing'] = job_keywords_missing[:15]
    results['job_match_score'] = job_score
    
    # 8. JD-Based Analysis
    jd_score = 0
    jd_keywords_found = []
    jd_keywords_missing = []
    
    if job_description and len(job_description.strip()) > 20:
        clean_jd = clean_text(job_description)
        # Extract meaningful words from JD (filter stopwords)
        stopwords = set(['the','a','an','and','or','but','in','on','at','to','for','of','with','is','are','was','were','be','been','being','have','has','had','do','does','did','will','would','could','should','may','might','shall','can','need','must','by','from','up','about','into','through','during','before','after','above','below','to','from','up','down','in','out','off','over','under','then','once','as','if','while','because','until','both','each','few','more','most','other','some','such','no','nor','not','only','own','same','so','than','too','very','just','also','it','its','this','that','these','those','we','you','he','she','they'])
        jd_words = [w for w in clean_jd.split() if len(w) > 3 and w not in stopwords]
        # Get most frequent meaningful JD words
        jd_freq = Counter(jd_words)
        top_jd_kws = [w for w, _ in jd_freq.most_common(40) if len(w) > 3]
        
        for kw in top_jd_kws:
            if kw in clean:
                jd_keywords_found.append(kw)
            else:
                jd_keywords_missing.append(kw)
        
        if top_jd_kws:
            jd_score = round((len(jd_keywords_found) / len(top_jd_kws)) * 100)
    
    results['jd_keywords_found'] = jd_keywords_found[:20]
    results['jd_keywords_missing'] = jd_keywords_missing[:15]
    results['jd_match_score'] = jd_score
    
    # 9. Overall ATS Score Calculation
    weights = {
        'contact': 0.10,
        'sections': 0.15,
        'action_verbs': 0.10,
        'quantification': 0.10,
        'formatting': 0.15,
        'job_match': 0.20,
        'jd_match': 0.20
    }
    
    base_score = (
        results['contact']['score'] * weights['contact'] +
        results['section_score'] * weights['sections'] +
        results['action_verb_score'] * weights['action_verbs'] +
        results['quantification_score'] * weights['quantification'] +
        results['formatting_score'] * weights['formatting']
    )
    
    if job_title and job_score > 0:
        base_score += job_score * weights['job_match']
    else:
        base_score = base_score / (1 - weights['job_match'])
    
    if job_description and jd_score > 0:
        base_score += jd_score * weights['jd_match']
    else:
        base_score = base_score / (1 - weights['jd_match']) if (not job_title or not job_score) else base_score + 50 * weights['jd_match']
    
    results['overall_score'] = min(98, max(10, round(base_score)))
    
    # 10. Grade & Recommendation
    score = results['overall_score']
    if score >= 85:
        results['grade'] = 'Excellent'
        results['grade_color'] = '#00ff88'
        results['recommendation'] = "Outstanding resume! Highly ATS-optimized with strong keyword density and formatting."
    elif score >= 70:
        results['grade'] = 'Good'
        results['grade_color'] = '#ffd700'
        results['recommendation'] = "Good ATS score. Minor improvements can push you to top shortlisting."
    elif score >= 55:
        results['grade'] = 'Average'
        results['grade_color'] = '#ff9500'
        results['recommendation'] = "Your resume needs optimization. Add more keywords and improve structure."
    elif score >= 40:
        results['grade'] = 'Poor'
        results['grade_color'] = '#ff4444'
        results['recommendation'] = "Significant ATS issues detected. Major revision recommended before applying."
    else:
        results['grade'] = 'Critical'
        results['grade_color'] = '#ff0000'
        results['recommendation'] = "Resume will likely be rejected by ATS. Complete rewrite strongly advised."
    
    # 11. Top Suggestions
    suggestions = []
    if not email_found: suggestions.append("Add your email address")
    if not phone_found: suggestions.append("Add your phone number")
    if not linkedin_found: suggestions.append("Add LinkedIn profile URL")
    if not sections['summary']: suggestions.append("Add a professional summary/objective section")
    if not sections['skills']: suggestions.append("Add a dedicated Skills section")
    if results['quantification_count'] < 3: suggestions.append("Add more quantified achievements (e.g., 'increased sales by 30%')")
    if len(found_verbs) < 5: suggestions.append("Use more strong action verbs (led, built, achieved, optimized)")
    if job_keywords_missing: suggestions.append(f"Add missing keywords: {', '.join(job_keywords_missing[:5])}")
    if jd_keywords_missing: suggestions.append(f"Include JD keywords: {', '.join(jd_keywords_missing[:5])}")
    if not sections['certifications']: suggestions.append("Add certifications/courses if applicable")
    
    results['suggestions'] = suggestions[:8]
    
    return results

# ─── ROUTES ───────────────────────────────────────────────────────────────────
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/job-titles', methods=['GET'])
def get_job_titles():
    return jsonify({'titles': list(JOB_KEYWORDS.keys())})

@app.route('/api/analyze', methods=['POST'])
def analyze():
    try:
        if 'resume' not in request.files:
            return jsonify({'error': 'No resume file uploaded'}), 400
        
        file = request.files['resume']
        job_title = request.form.get('job_title', '')
        job_description = request.form.get('job_description', '')
        
        if not file.filename:
            return jsonify({'error': 'No file selected'}), 400
        
        allowed = {'.pdf', '.docx', '.doc', '.txt'}
        ext = os.path.splitext(file.filename)[1].lower()
        if ext not in allowed:
            return jsonify({'error': f'Unsupported format. Use: {", ".join(allowed)}'}), 400
        
        filepath = os.path.join(UPLOAD_FOLDER, 'resume' + ext)
        file.save(filepath)
        
        resume_text = extract_text(filepath)
        
        if len(resume_text.strip()) < 50:
            return jsonify({'error': 'Could not extract text from resume. Try a different format.'}), 400
        
        results = analyze_resume(
            resume_text,
            job_title=job_title if job_title else None,
            job_description=job_description if job_description else None
        )
        
        os.remove(filepath)
        return jsonify({'success': True, 'results': results})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
