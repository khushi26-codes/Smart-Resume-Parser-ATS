import streamlit as st
import fitz, docx, re, json, pandas as pd
from PIL import Image
import io
import numpy as np

st.set_page_config(page_title="Smart Resume Parser", layout="wide", page_icon="📄")
st.markdown("<style>.card{background:#f8f9fa;padding:15px;border-radius:12px;border:1px solid #e9ecef;}</style>", unsafe_allow_html=True)

@st.cache_resource
def load_ocr():
    import easyocr
    return easyocr.Reader(['en'], gpu=False)
reader = load_ocr()

st.title("📄 Smart Resume Parser - AI Based ATS System")
st.caption("Final Year Project | Python • PyMuPDF • python-docx • spaCy • EasyOCR • Streamlit")
st.markdown("---")

def extract_any(file):
    file.seek(0)
    data=file.read()
    text=""
    try:
        doc=fitz.open(stream=data, filetype="pdf")
        for p in doc: text+=p.get_text()+"\n"
    except: pass
    if len(text.split())<30:
        try:
            doc=fitz.open(stream=data, filetype="pdf")
            full=""
            for page in doc:
                pix=page.get_pixmap(matrix=fitz.Matrix(2.5,2.5))
                img=Image.open(io.BytesIO(pix.tobytes("png")))
                res=reader.readtext(np.array(img), detail=0, paragraph=True)
                full+=" ".join(res)+"\n"
            if len(full.split())>20: text=full
        except: pass
    if len(text.split())<20 and file.name.lower().endswith(".docx"):
        file.seek(0)
        d=docx.Document(file)
        text="\n".join([p.text for p in d.paragraphs])
    return text

def parse(text):
    lower=text.lower()
    email=re.search(r"[\w\.-]+@[\w\.-]+\.\w+", text)
    phone=re.search(r"\+?91[\s-]*\d{10}|\b[6-9]\d{9}\b", text)
    linkedin=re.search(r"linkedin\.com\S+", lower)
    skills_db=["python","java","sql","html","css","javascript","react","excel","power bi","machine learning","ai","dbms","oops","communication","teamwork","ms office","c","c++"]
    edu_db=["10th","12th","diploma","b.tech","btech","m.tech","bca","mca","b.sc","m.sc","graduation"]
    found_skills=[s.upper() for s in skills_db if re.search(r'\b'+re.escape(s)+r'\b', lower)]
    found_edu=[e.upper() for e in edu_db if e in lower]
    name="Not Found"
    lines=[l.strip() for l in text.split("\n") if len(l.strip())>3 and len(l.strip())<50]
    for l in lines[:5]:
        if "resume" not in l.lower() and "curriculum" not in l.lower() and "@" not in l and not any(c.isdigit() for c in l):
            if len(l.split())<=4:
                name=l
                break
    if name=="Not Found" and lines: name=lines[0]
    exp_text="Not Found"
    if "fresher" in lower: exp_text="Fresher"
    elif "intern" in lower: exp_text="Internship Mentioned"
    elif "experience" in lower: exp_text="Experience Mentioned"
    score=20
    if email: score+=20
    if phone: score+=15
    if found_skills: score+=25
    if found_edu: score+=10
    if name!="Not Found": score+=10
    score=min(score, 95)
    return {"Name":name.title(),"Email":email.group(0) if email else "Not Found","Phone":phone.group(0) if phone else "Not Found","LinkedIn":linkedin.group(0) if linkedin else "Not Found","Skills":", ".join(found_skills) if found_skills else "Not Found","Education":", ".join(found_edu) if found_edu else "Not Found","Experience":exp_text,"ATS Score":score,"Words":len(text.split()),"Raw":text}

with st.sidebar:
    st.header("⚙️ Guide Steps")
    st.markdown("1. PyMuPDF / docx\n2. Cleaning\n3. spaCy + Regex\n4. JSON/Table\n5. Streamlit UI\n6. Export")
    st.success("OCR Enabled")

upload=st.file_uploader("Drag & Drop Resumes (Any Candidate)", type=["pdf","docx"], accept_multiple_files=True)

if upload:
    all_data=[]
    for f in upload:
        txt=extract_any(f)
        parsed=parse(txt)
        parsed["File"]=f.name
        all_data.append(parsed)
        st.markdown("---")
        c1,c2,c3,c4 = st.columns(4)
        c1.metric("Name", parsed["Name"])
        c2.metric("ATS Score", f"{parsed['ATS Score']}%")
        c3.metric("Skills", len(parsed["Skills"].split(",")) if parsed["Skills"]!="Not Found" else 0)
        c4.metric("Words", parsed["Words"])
        col1,col2 = st.columns([2,1])
        with col1:
            st.subheader("📋 Extracted Information")
            st.markdown(f"""<div class="card"><b>📧 Email:</b> {parsed['Email']}<br><b>📞 Phone:</b> {parsed['Phone']}<br><b>🔗 LinkedIn:</b> {parsed['LinkedIn']}<br><b>🎓 Education:</b> {parsed['Education']}<br><b>💼 Experience:</b> {parsed['Experience']}<br><b>🛠️ Skills:</b> {parsed['Skills']}</div>""", unsafe_allow_html=True)
            st.progress(parsed["ATS Score"])
        with col2:
            st.subheader("📊 Analysis")
            if parsed["Skills"]!="Not Found":
                # FIXED: Simple display, no error
                st.write("Skills List:")
                st.write(parsed["Skills"])
            st.text_area("Raw Text Preview", parsed["Raw"][:600], height=180)
    st.markdown("---")
    st.subheader("📑 Final Report")
    df_final=pd.DataFrame(all_data)[["File","Name","Email","Phone","Education","Experience","Skills","ATS Score"]]
    st.dataframe(df_final, use_container_width=True)
    c1,c2=st.columns(2)
    c1.download_button("⬇️ Download CSV", df_final.to_csv(index=False).encode(), "ATS_Report.csv", "text/csv", use_container_width=True)
    c2.download_button("⬇️ Download JSON", json.dumps(all_data, indent=2), "ATS_Report.json", "application/json", use_container_width=True)