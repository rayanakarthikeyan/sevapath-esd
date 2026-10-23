"""Rebuild the judge-facing PDF from project facts and actual evidence."""
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor, white
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import json

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'submission'/'SevaPath-Submission-Brief.pdf'
OUT.parent.mkdir(exist_ok=True)
font_dir=Path('C:/Windows/Fonts')
for name,file in [('Body','segoeui.ttf'),('Bold','segoeuib.ttf')]:
    pdfmetrics.registerFont(TTFont(name,str(font_dir/file)))
pdfmetrics.registerFontFamily('Body',normal='Body',bold='Bold',italic='Body',boldItalic='Bold')
GREEN=HexColor('#17594c'); INK=HexColor('#243e34'); MUTED=HexColor('#5e7165'); SAGE=HexColor('#edf3e7'); GOLD=HexColor('#b68b36')
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='TitleSP',fontName='Bold',fontSize=40,leading=46,textColor=GREEN,spaceAfter=12))
styles.add(ParagraphStyle(name='LeadSP',fontName='Body',fontSize=18,leading=25,textColor=INK,spaceAfter=20))
styles.add(ParagraphStyle(name='H1SP',fontName='Bold',fontSize=25,leading=32,textColor=GREEN,spaceAfter=17))
styles.add(ParagraphStyle(name='H2SP',fontName='Bold',fontSize=13,leading=19,textColor=INK,spaceBefore=12,spaceAfter=7))
styles.add(ParagraphStyle(name='BodySP',fontName='Body',fontSize=10.5,leading=16.5,textColor=INK,spaceAfter=10))
styles.add(ParagraphStyle(name='SmallSP',fontName='Body',fontSize=8.5,leading=13,textColor=MUTED,spaceAfter=9))
styles.add(ParagraphStyle(name='EyebrowSP',fontName='Bold',fontSize=8.5,leading=14,textColor=GOLD,spaceAfter=15))
styles.add(ParagraphStyle(name='CellSP',fontName='Body',fontSize=9,leading=13,textColor=INK))
story=[]
def p(text,style='BodySP'):return Paragraph(text,styles[style])
def add(text,style='BodySP'):story.append(p(text,style))
def title(n,text):add(f'SEVAPATH / BUILD STAGE / {n:02}','EyebrowSP');add(text,'H1SP')
def table(headers,rows,widths):
    data=[[p(x,'CellSP') for x in headers]]+[[p(str(x),'CellSP') for x in row] for row in rows]
    t=Table(data,colWidths=widths,hAlign='LEFT',repeatRows=1)
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),SAGE),('FONTNAME',(0,0),(-1,0),'Bold'),('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),10),('BOTTOMPADDING',(0,0),(-1,-1),10),('LEFTPADDING',(0,0),(-1,-1),10),('RIGHTPADDING',(0,0),(-1,-1),10),('LINEBELOW',(0,0),(-1,-1),.4,HexColor('#dce5d7'))]))
    story.append(t);story.append(Spacer(1,12))
def screenshot(name,maxw=491,maxh=335):
    path=ROOT/'docs'/'evidence'/name
    if path.exists():
        w,h=ImageReader(str(path)).getSize();scale=min(maxw/w,maxh/h)
        story.append(Image(str(path),w*scale,h*scale,hAlign='LEFT'));story.append(Spacer(1,9))
def page():story.append(PageBreak())
def footer(c,doc):
    w,h=doc.pagesize;c.setStrokeColor(HexColor('#dce5d7'));c.line(52,42,w-52,42)
    c.setFont('Body',8);c.setFillColor(MUTED);c.drawString(52,28,'Independent prototype | ESD Innovation Challenge 2026 | 23 October 2026')
    c.drawRightString(w-52,28,str(doc.page))

add('TELANGANA / ELECTRONIC SERVICE DELIVERY / 2026','EyebrowSP')
story.append(Spacer(1,16))
add('SevaPath','TitleSP')
add('A clearer path to<br/>public services.','LeadSP')
add('Source-linked, bilingual preparation for an income-certificate application. A focused improvement to the citizen journey before official submission.')
story.append(Spacer(1,6));screenshot('home-desktop.png',maxh=312)
table(['COMPLETE WORKFLOW','REAL IMPLEMENTATION','INCLUSIVE BY DESIGN'],[['Income-certificate preparation, route-specific checklist and official handoff','PostgreSQL + protected CRUD API + local intent matching','English/Telugu, larger text, optional read aloud and printable plan']],[164,164,163])
add('<b>Single submission link</b><br/><link href="https://github.com/rayanakarthikeyan/sevapath-esd" color="#17594c">github.com/rayanakarthikeyan/sevapath-esd</link>','SmallSP')
add('Public demo: <link href="https://rayanakarthikeyan.github.io/sevapath-esd/" color="#17594c">rayanakarthikeyan.github.io/sevapath-esd/</link><br/>Author/committer: rayanakarthikeyan@gmail.com','SmallSP')
page()

title(2,'The gap is in preparation.')
add('A citizen may know their need without knowing the service vocabulary, acceptable evidence alternatives or what to bring to a centre.','LeadSP')
table(['PUBLISHED EVIDENCE','DESIGN RESPONSE'],[
 ['MeeSeva mobile-governance FAQ describes one-sitting completion and asks citizens to organize documents in advance. [1]','A resumable preparation stage before entering the official transaction.'],
 ['The income form lists alternative identity and income evidence. [2]','Show alternatives in plain language, including the no-payslip scenario.'],
 ['The published form exempts citizen login from the paper application requirement. [2]','Change checklist items by citizen-login versus centre route.']
],[245,246])
add('An illustrative citizen scenario','H2SP')
add('A Telugu-first student needs income-related evidence for an institution. Their household has irregular earnings and no payslip. SevaPath explains the published options, flags the need to confirm the exact service, and helps them prepare for the route they choose.')
add('Why this is feasible','H2SP')
add('The initial intervention is read-only guidance plus preparation. It does not require modification of a government transaction system or a government API. Starting with one service makes the rules inspectable and the outcome testable.')
add('Evidence boundary','H2SP')
add('The sources were reviewed as published on 23 October 2026. The FAQ may describe an older interface. No current live-portal audit, citizen interviews, abandonment rate or measured repeat-visit baseline is claimed. This is a problem hypothesis grounded in primary published material, ready for department validation.','SmallSP')
page()

title(3,'From intent to a useful next step.')
table(['STEP','WORKING BEHAVIOR'],[
 ['1 / Describe','English, Telugu-script or selected Romanized Telugu descriptions are matched locally. Unclear and mixed requests ask for clarification.'],
 ['2 / Understand','The income flow explains evidence alternatives with links to official sources. Scholarship requests prompt exact-service confirmation.'],
 ['3 / Prepare','Choose citizen login or centre. Mark readiness, check file metadata locally, and save or restore a non-identifying preparation draft.'],
 ['4 / Continue','Print or download the plan and continue with the official service or a MeeSeva centre. No government application is submitted here.']
],[95,396])
screenshot('plan-cloud-restored.png',maxh=310)
add('Actual working prototype: all four centre-route items marked, cloud copy restored. This is self-declared preparation, not certificate approval.','SmallSP')
add('Intent matching uses a small TF-IDF/cosine-similarity classifier. It is not a large language model or a verified eligibility engine. Other service categories are directory links only.','SmallSP')
page()

title(4,'Small architecture. Clear trust boundary.')
add('Browser-first assistance, database-backed preparation.','LeadSP')
table(['LAYER','IMPLEMENTATION'],[
 ['Interface','Vanilla JavaScript and Vite. English/Telugu core workflow; source links, responsive UI, keyboard focus, text enlargement, optional browser synthesis.'],
 ['Local intelligence','Unicode tokenization, curated multilingual category corpus, TF-IDF vectors, cosine similarity and ambiguity threshold. No remote inference or query storage.'],
 ['API','InsForge SDK + PostgREST RPC: save, load, delete and feedback. Source catalogue is public read-only.'],
 ['Database','PostgreSQL source records, preparation drafts and feedback. Primary/foreign keys, unique capability hash, constraints, RLS and revoked direct private-table access.'],
 ['Deployment','Public GitHub Pages demo, source-controlled build/test workflows, reproducible schema and installation instructions.']
],[105,386])
add('Minimize data instead of asking for an identity','H2SP')
add('The cloud stores only choices, checklist flags, timestamps and a hash of a random 256-bit device capability. No citizen name, phone, ID number, income amount or document is required. File checks use metadata on the device; they do not verify contents or authenticity.')
add('Explicit limitations','H2SP')
add('A bearer capability can be used by anyone who obtains it. Clearing storage loses access; shared browser profiles share the device key. Wider rollout needs quotas, throttling, retention/expiry automation, source-owner review and independent security/accessibility assessment. Hosting providers handle ordinary request metadata.','SmallSP')
page()

title(5,'Working behavior, backed by evidence.')
cloud=json.loads((ROOT/'docs/evidence/cloud-results.json').read_text(encoding='utf8'))
table(['CHECK','ACTUAL RESULT','EVIDENCE'],[
 ['Local regression suite','26 passed, 0 failed','docs/evidence/local-tests.txt'],
 ['Live PostgreSQL/API suite',f"{cloud['passed']} passed, {cloud['failed']} failed",'docs/evidence/cloud-results.json'],
 ['Production bundle','Built successfully','docs/evidence/build.txt'],
 ['Public CI and demo','GitHub build and Pages deployment succeeded','Repository Actions tab'],
 ['Browser workflow','Source-linked result, route switch, cloud save/restore and Telugu mobile checked','docs/evidence/ screenshots; docs/TESTING.md']
],[141,131,219])
add('The live tests exercise more than a happy path','H2SP')
add('The anonymous SDK client creates, reads, updates and deletes synthetic preparations. Tests also cover alternate-capability isolation, denied direct private-table reads/inserts, invalid capabilities, unexpected personal fields, invalid enums, oversized payloads and feedback ownership. Test records are removed.')
add('Bugs found and fixed','H2SP')
add('A Windows test-runner glob failed and was replaced with an explicit test path. A Romanized Telugu phrase was under-matched; normalization was corrected and the local suite rerun. Keyboard focus is preserved after key control rerenders, and local changes reset the saved-copy indicator.')
add('No invented impact figures','H2SP')
add('The tests validate defined behavior and live database connectivity. They are not a representative language benchmark, a load test, a security certification or a citizen usability study. Native Telugu review and assistive-technology testing remain necessary.','SmallSP')
page()

title(6,'Prove the citizen benefit next.')
add('A measurable pilot with ESD and service owners.','LeadSP')
table(['PILOT MEASURE','PROPOSED CRITERION'],[
 ['Correct document selection','At least 85% correct synthetic task completion; compare against published-form baseline.'],
 ['Preparation time','Target median time at least 30% lower than baseline.'],
 ['Missing items and help requests','Compare task-level errors and moderator interventions; report actual counts.'],
 ['Calibrated confidence','At least 90% can explain that checklist readiness is not approval.'],
 ['Accessibility and language','No blocker in core keyboard/assistive workflow; native Telugu comprehension review.']
],[160,331])
add('Study design','H2SP')
add('Proposed 24-person pilot across Telugu-first, first-time digital users and seniors, including participants using assistive technology. Counterbalance baseline and SevaPath task order, use synthetic situations, and report medians, ranges and uncertainty. These targets have not been measured or achieved.')
add('Practical scale-up','H2SP')
add('Validate each service with its department owner, then add approved source snapshots and service-specific rules. Static hosting and local classification avoid a per-query model bill. Bound database reads and explicit saves keep the implementation small. Add operational controls and load testing before rollout.')
add('Why this entry','H2SP')
add('A narrow, complete, testable workflow combines local language discovery, source provenance, adaptive requirements, resumable preparation and a clear handoff. It improves an existing public-service journey without pretending to replace its authority.')
page()

title(7,'A reviewable, single-link build pack.')
table(['BUILD REQUIREMENT','WHERE TO REVIEW'],[
 ['Source and working application','README.md, src/, public demo'],
 ['Database and connectivity','migrations/, docs/DATABASE.md, live cloud test results'],
 ['API and authorization','src/api.js, protected RPC migration, docs/API.md'],
 ['Dependencies and installation','package.json, package-lock.json, .env.example, README'],
 ['Testing cases and outcomes','tests/, scripts/test-cloud.mjs, docs/TESTING.md and evidence'],
 ['Demo and feasibility','docs/DEMO.md, docs/PILOT.md, this brief'],
 ['Design and source rationale','docs/PROBLEM-EVIDENCE.md, docs/PRIVACY.md']
],[164,327])
add('Stage-specific scope','H2SP')
add('This pack maps to the supplied Build-stage guidelines. The author reported Build submission complete on 23 October 2026; no portal receipt or judging decision was independently verified. No prior approved Design artifact or Final Demo guidelines PDF was supplied, so those requirements remain unverified. The screenshot separately lists Demo submission on 25 October 2026.','SmallSP')
add('Primary references','H2SP')
add('[1] Government of Telangana, mobile-governance FAQ: <link href="https://mgov.telangana.gov.in/faqnew.html" color="#17594c">mgov.telangana.gov.in/faqnew.html</link><br/>[2] Government of Telangana, income application form: <link href="https://www.telangana.gov.in/wp-content/uploads/2023/03/IncomeGeneralApplicationForm.pdf" color="#17594c">IncomeGeneralApplicationForm.pdf</link><br/>[3] Telangana State Portal: <link href="https://www.telangana.gov.in/services/public-utility-forms/" color="#17594c">Public utility forms</link>','SmallSP')
add('Submitted repository link (author-reported)','H2SP')
add('<link href="https://github.com/rayanakarthikeyan/sevapath-esd" color="#17594c">https://github.com/rayanakarthikeyan/sevapath-esd</link>')

doc=SimpleDocTemplate(str(OUT),pagesize=(595.28,841.89),rightMargin=52,leftMargin=52,topMargin=47,bottomMargin=60,title='SevaPath - ESD Build Submission Brief',author='rayanakarthikeyan@gmail.com',subject='Telangana income-certificate preparation prototype')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
print(OUT)
