import streamlit as st
from docx import Document
from docx.shared import Inches, Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_SECTION
import io

# ── PAGE CONFIG ────────────────────────────────────────────────────
st.set_page_config(
    page_title="ગુજરાત હાઇકોર્ટ નિયમ મુજબ - લીગલ ડ્રાફ્ટિંગ ટૂલ",
    page_icon="⚖️",
    layout="wide"
)

# ── HEADER ─────────────────────────────────────────────────────────
st.title("⚖️ લીગલ દસ્તાવેજ ડ્રાફ્ટિંગ સોફ્ટવેર")
st.subtitle = st.markdown("**ગુજરાત હાઇકોર્ટના નવા A4 સાઇઝ અને ફોર્મેટિંગ નિયમો અનુસાર**")
st.divider()

col_input, col_preview = st.columns([1, 1])

with col_input:
    st.header("📝 વિગતો ભરો")
    
    # કેસ/દસ્તાવેજની માહિતી
    doc_type = st.selectbox("દસ્તાવેજનો પ્રકાર પસંદ કરો:", [
        "બાંહેધરી પત્ર (Affidavit)",
        "મકાન ભાડા કરાર (Rent Agreement)",
        "સામાન્ય અરજી (General Application)"
    ])
    
    court_name = st.text_input("કોર્ટ / ઓથોરિટીનું નામ:", "ગુજરાત હાઇકોર્ટ, અમદાવાદ")
    applicant_name = st.text_input("અરજદારનું નામ (Applicant Name):", "રમેશભાઈ પટેલ")
    opposite_party = st.text_input("સામાવાળાનું નામ (Opposite Party):", "ગુજરાત રાજ્ય")
    case_number = st.text_input("કેસ / પિટિશન નંબર:", "C.A. No. 1024 of 2026")
    
    st.subheader("📄 દસ્તાવેજનું લખાણ (Content)")
    doc_body = st.text_area("મુખ્ય વિગત / સોગંદનામાનું લખાણ:", 
                            value="આથી હું નીચે સહી કરનાર સોગંદ ઉપર જણાવું છું કે ઉપર દર્શાવેલ વિગતો મારી જાણ અને વિશ્વાસ મુજબ સત્ય અને સાચી છે...", 
                            height=200)

    st.subheader("⚙️ હાઇકોર્ટ નિયમ મુજબ પેજ સેટિંગ્સ")
    st.info("📌 A4 Size | Left/Right Margin: 4 cm | Top/Bottom Margin: 2 cm")

# ── WORD DOCUMENT GENERATOR FUNCTION ───────────────────────────────
def generate_docx():
    doc = Document()
    
    # 1. પેજ સાઇઝ A4 સેટ કરવી (29.7 cm x 21 cm)
    section = doc.sections[0]
    section.page_height = Cm(29.7)
    section.page_width = Cm(21.0)
    
    # 2. હાઇકોર્ટ પરિપત્ર મુજબ માર્જિન સેટ કરવું
    section.top_margin = Cm(2.0)
    section.bottom_margin = Cm(2.0)
    section.left_margin = Cm(4.0)
    section.right_margin = Cm(4.0)
    
    # 3. હેડર / કોર્ટનું નામ
    p_head = doc.add_paragraph()
    p_head.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_head = p_head.add_run(f"મેહરબાન {court_name} માં\n")
    run_head.bold = True
    run_head.font.name = 'Gujarati Font'
    run_head.font.size = Pt(14)
    
    # કેસ નંબર
    p_case = doc.add_paragraph()
    p_case.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_case = p_case.add_run(f"{case_number}\n")
    run_case.font.size = Pt(12)
    
    # પાર્ટીના નામ
    p_party = doc.add_paragraph()
    p_party.paragraph_format.line_spacing = 1.5  # 1.5 લાઇન સ્પેસિંગ
    run_party = p_party.add_run(f"અરજદાર: {applicant_name}\nઅન્યે/વિરુદ્ધ\nસામાવાળા: {opposite_party}\n")
    run_party.font.size = Pt(13)
    
    # ટાઇટલ
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_title = p_title.add_run(f"\n:: {doc_type} ::\n")
    run_title.bold = True
    run_title.font.size = Pt(14)
    
    # મુખ્ય લખાણ
    p_body = doc.add_paragraph()
    p_body.paragraph_format.line_spacing = 1.5
    run_body = p_body.add_run(doc_body)
    run_body.font.size = Pt(13)
    
    # સહીની જગ્યા
    p_sign = doc.add_paragraph()
    p_sign.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_sign.paragraph_format.space_before = Pt(30)
    run_sign = p_sign.add_run(f"\n\n_____________________\n({applicant_name})\nઅરજદારની સહી")
    run_sign.font.size = Pt(13)
    
    # મેમરીમાં બાઈટ્સ તરીકે સેવ કરવું
    target_stream = io.BytesIO()
    doc.save(target_stream)
    return target_stream.getvalue()

with col_preview:
    st.header("👁️ પ્રિવ્યૂ અને ડાઉનલોડ")
    st.success("તમારો દસ્તાવેજ ગુજરાત હાઇકોર્ટના માપદંડો મુજબ તૈયાર થશે.")
    
    docx_data = generate_docx()
    
    # ડાઉનલોડ બટન
    st.download_button(
        label="📥 દસ્તાવેજ (Word File) ડાઉનલોડ કરો",
        data=docx_data,
        file_name=f"{doc_type}_Gujarat_Highcourt_Format.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        use_container_width=True
    )
    
    st.markdown("""
    ---
    ### 📋 એપ્લિકેશનની વિશેષતાઓ:
    * ✅ **A4 Size પેપર ફોર્મેટ** ઓટોમેટિક સેટ થશે.
    * ✅ **Left/Right 4cm અને Top/Bottom 2cm** માર્જિન સેટ રહેશે.
    * ✅ **1.5 Line Spacing** નિયમ મુજબ ઓટો-એપ્લાય થઈ જશે.
    * ✅ સીધી **Word (.docx)** ફાઈલ ડાઉનલોડ થશે જેને તમે પ્રિન્ટ પણ કરી શકશો.
    """)
