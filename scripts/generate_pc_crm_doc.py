import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_margins(cell, top=140, bottom=140, left=180, right=180):
    """Set cell padding in dxa (1 pt = 20 dxa)."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_background(cell, hex_color):
    """Set cell background shading."""
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_border(cell, **kwargs):
    """Set specific borders for a cell (e.g. left='4B6B94')."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = OxmlElement('w:tcBorders')
    for edge in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        edge_data = kwargs.get(edge)
        if edge_data:
            tag = f'w:{edge}'
            element = OxmlElement(tag)
            element.set(qn('w:val'), edge_data.get('val', 'single'))
            element.set(qn('w:sz'), str(edge_data.get('sz', 4)))
            element.set(qn('w:space'), '0')
            element.set(qn('w:color'), edge_data.get('color', 'auto'))
            tcBorders.append(element)
    tcPr.append(tcBorders)

def add_callout(doc, text, title=None, bg_color="F0F4F8", border_color="1B365D"):
    """Adds a stylish callout box."""
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    cell = table.cell(0, 0)
    cell.width = Inches(6.5)
    set_cell_background(cell, bg_color)
    set_cell_margins(cell, top=160, bottom=160, left=220, right=200)
    set_cell_border(cell, left={'val': 'single', 'sz': 24, 'color': border_color},
                          top={'val': 'none'}, right={'val': 'none'}, bottom={'val': 'none'})
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.15
    
    if title:
        run_title = p.add_run(f"📌 {title}\n")
        run_title.bold = True
        run_title.font.name = 'Calibri'
        run_title.font.size = Pt(11)
        run_title.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
    
    run_text = p.add_run(text)
    run_text.font.name = 'Calibri'
    run_text.font.size = Pt(10.5)
    run_text.font.italic = True
    run_text.font.color.rgb = RGBColor(0x2D, 0x37, 0x48)
    
    doc.add_paragraph().paragraph_format.space_after = Pt(6)

def build_document(file_path):
    doc = docx.Document()
    
    # Page setup - 1 inch margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)
        
    # Color Palette Definitions
    COLOR_NAVY = RGBColor(0x1B, 0x36, 0x5D)      # Primary Headers
    COLOR_TEAL = RGBColor(0x02, 0x84, 0xC7)      # Subheaders / Accents
    COLOR_DARK = RGBColor(0x2D, 0x37, 0x48)      # Body Text
    COLOR_MUTED = RGBColor(0x71, 0x80, 0x96)     # Meta / Footnotes
    
    # Base Normal Style
    style_normal = doc.styles['Normal']
    style_normal.font.name = 'Calibri'
    style_normal.font.size = Pt(11)
    style_normal.font.color.rgb = COLOR_DARK
    
    # ==================== DOCUMENT HEADER / TITLE ====================
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(0)
    title_p.paragraph_format.space_after = Pt(4)
    run_title = title_p.add_run("PC CRM & LEAD CLASSIFICATION SYSTEM (LCS)")
    run_title.font.name = 'Calibri'
    run_title.font.size = Pt(22)
    run_title.font.bold = True
    run_title.font.color.rgb = COLOR_NAVY
    
    subtitle_p = doc.add_paragraph()
    subtitle_p.paragraph_format.space_before = Pt(0)
    subtitle_p.paragraph_format.space_after = Pt(14)
    run_subtitle = subtitle_p.add_run("Executive Architecture Overview: In-House Sales Platform, Middleware Intelligence & Enterprise Analytics")
    run_subtitle.font.name = 'Calibri'
    run_subtitle.font.size = Pt(12)
    run_subtitle.font.color.rgb = COLOR_TEAL
    
    # Meta Info Table
    meta_table = doc.add_table(rows=1, cols=3)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_table.autofit = False
    
    col_widths = [Inches(2.5), Inches(2.0), Inches(2.0)]
    meta_data = [
        ("Platform", "PC CRM (Proprietary In-House)"),
        ("Architecture", "LCS Middleware & SLA Engine"),
        ("Target Integration", "Organizational BI Dashboard")
    ]
    for i, (label, val) in enumerate(meta_data):
        cell = meta_table.cell(0, i)
        cell.width = col_widths[i]
        set_cell_background(cell, "F7FAFC")
        set_cell_margins(cell, top=80, bottom=80, left=120, right=120)
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        r_lbl = p.add_run(f"{label}: ")
        r_lbl.font.size = Pt(9.5)
        r_lbl.font.bold = True
        r_lbl.font.color.rgb = COLOR_NAVY
        r_val = p.add_run(val)
        r_val.font.size = Pt(9.5)
        r_val.font.color.rgb = COLOR_MUTED

    p_div = doc.add_paragraph()
    p_div.paragraph_format.space_before = Pt(10)
    p_div.paragraph_format.space_after = Pt(14)
    r_div = p_div.add_run("―" * 58)
    r_div.font.color.rgb = RGBColor(0xCB, 0xD5, 0xE1)

    # Helper function for adding headings
    def add_sec_heading(title, number=None):
        h = doc.add_paragraph()
        h.paragraph_format.space_before = Pt(18)
        h.paragraph_format.space_after = Pt(6)
        h.paragraph_format.keep_with_next = True
        if number:
            r_num = h.add_run(f"{number}. ")
            r_num.font.bold = True
            r_num.font.size = Pt(15)
            r_num.font.color.rgb = COLOR_TEAL
        r = h.add_run(title)
        r.font.bold = True
        r.font.size = Pt(15)
        r.font.color.rgb = COLOR_NAVY
        return h

    def add_sub_heading(title):
        h = doc.add_paragraph()
        h.paragraph_format.space_before = Pt(12)
        h.paragraph_format.space_after = Pt(4)
        h.paragraph_format.keep_with_next = True
        r = h.add_run(title)
        r.font.bold = True
        r.font.size = Pt(12.5)
        r.font.color.rgb = COLOR_TEAL
        return h

    # ==================== SECTION 1: WHAT IS PC CRM? ====================
    add_sec_heading("Executive Summary: What is PC CRM?", 1)
    
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(8)
    p.paragraph_format.line_spacing = 1.15
    p.add_run(
        "PC CRM is PACE's own proprietary, custom-built Customer Relationship Management platform. "
        "Unlike generic commercial CRM products (such as standard Salesforce, HubSpot, or off-the-shelf Frappe CRM), "
        "PC CRM has been engineered entirely around PACE Court's specialized sales lifecycle, client qualification workflows, "
        "and multi-tier sports infrastructure sales cycles."
    )

    add_callout(
        doc,
        "Key Strategic Principle: PC CRM is an independent in-house software asset. "
        "We have eliminated all third-party branding, external promotional links, and generic onboarding tutorials. "
        "Every data model, pipeline stage, automation hook, and user interface element belongs 100% to PACE.",
        title="In-House Intellectual Property"
    )

    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(8)
    p.paragraph_format.line_spacing = 1.15
    p.add_run(
        "Modern sports court construction, turnkey infrastructure, and premium sports surfacing projects require high-touch, "
        "fast-response consultative sales. Traditional sales pipelines fail when high-value enterprise leads are treated the same "
        "as casual retail queries. PC CRM solves this through unified lead intelligence, automated task routing, and strict response enforcement."
    )

    # Bullet points on core capabilities
    core_features = [
        ("Proprietary System Ownership: ", "Full control over backend logic, security, access roles, and zero per-user licensing fees."),
        ("Tailored Pipeline Stages: ", "Custom workflows built specifically for inquiries, site evaluations, estimates, quotes, and handoffs."),
        ("Integrated Communication Hub: ", "Unified records for telephone call logs, email threads, notes, reminders, and activity timelines."),
        ("Elimination of Third-Party Dependencies: ", "Completely de-branded and optimized for private enterprise deployment on our dedicated Azure cloud infrastructure.")
    ]
    for bold_txt, norm_txt in core_features:
        bp = doc.add_paragraph(style='List Bullet')
        bp.paragraph_format.space_after = Pt(4)
        bp.paragraph_format.line_spacing = 1.15
        r_b = bp.add_run(bold_txt)
        r_b.bold = True
        r_b.font.color.rgb = COLOR_NAVY
        bp.add_run(norm_txt)

    # ==================== SECTION 2: LCS AS A MIDDLEWARE ====================
    add_sec_heading("The Lead Classification System (LCS) as Middleware", 2)
    
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(8)
    p.paragraph_format.line_spacing = 1.15
    p.add_run(
        "At the heart of PC CRM lies the Lead Classification System (LCS). Rather than acting simply as a static database column, "
        "LCS functions as an intelligent middleware layer that sits squarely between incoming raw prospect inquiries and our frontline sales team."
    )

    add_callout(
        doc,
        "What is a Middleware in this context? Think of LCS as an automated 'Digital Sorting Concierge'. "
        "Before any salesperson touches a lead, LCS intercepts the inquiry, evaluates who the buyer is (Fit) and how urgent "
        "their project is (Intent), assigns them an objective tier, and programs their exact response deadline.",
        title="Understanding LCS as Middleware"
    )

    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 1.15
    p.add_run("LCS evaluates two distinct objective dimensions:")

    dim_points = [
        ("Dimension 1: Fit Score (0–50 Points): ", "Measures organizational compatibility. Evaluates project scope, budget scale, commercial vs. residential nature, institution type (school, sports club, real estate developer, private estate), and court specifications."),
        ("Dimension 2: Intent Score (0–50 Points): ", "Measures buying urgency and readiness. Evaluates project start date, readiness for civil work, decision-maker authority, responsiveness, and buying timeline.")
    ]
    for bold_txt, norm_txt in dim_points:
        bp = doc.add_paragraph(style='List Bullet')
        bp.paragraph_format.space_after = Pt(4)
        bp.paragraph_format.line_spacing = 1.15
        r_b = bp.add_run(bold_txt)
        r_b.bold = True
        r_b.font.color.rgb = COLOR_NAVY
        bp.add_run(norm_txt)

    # Table of Tiers
    p_tbl = doc.add_paragraph()
    p_tbl.paragraph_format.space_before = Pt(10)
    p_tbl.paragraph_format.space_after = Pt(4)
    r_tbl_t = p_tbl.add_run("Table 1: LCS Classification Matrix & Automatic Service Level Agreements (SLAs)")
    r_tbl_t.bold = True
    r_tbl_t.font.size = Pt(10)
    r_tbl_t.font.color.rgb = COLOR_NAVY

    tier_table = doc.add_table(rows=6, cols=5)
    tier_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    tier_table.autofit = False

    t_widths = [Inches(1.0), Inches(1.1), Inches(1.1), Inches(1.1), Inches(2.2)]
    headers = ["Tier", "Fit Rating", "Intent Rating", "SLA Target", "Strategic Action & Business Priority"]
    
    # Format Header Row
    hdr_cells = tier_table.rows[0].cells
    for i, title in enumerate(headers):
        hdr_cells[i].width = t_widths[i]
        set_cell_background(hdr_cells[i], "1B365D")
        set_cell_margins(hdr_cells[i], top=120, bottom=120, left=140, right=140)
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if i in (0, 3) else WD_ALIGN_PARAGRAPH.LEFT
        r = p.add_run(title)
        r.bold = True
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    # Data Rows
    tier_data = [
        ("A1", "High (≥35)", "High (≥35)", "4 Hours", "Crown Jewel Enterprise. Immediate direct call by Senior Specialist; bespoke pitch."),
        ("A2", "High (≥35)", "Medium (20-34)", "24 Hours", "High-value long-cycle project. Requires consultative education and technical specs."),
        ("B1", "Medium (25-34)", "High (≥35)", "24 Hours", "Immediate buyer needing standard fast turnaround court installation."),
        ("B2", "Medium (25-34)", "Medium (20-34)", "48 Hours", "Standard lead. Nurture with case studies, standard pricing catalogs."),
        ("C1", "Entry (<25)", "High (≥35)", "24 Hours", "Small scope inquiry but high readiness to purchase immediately.")
    ]

    for row_idx, row in enumerate(tier_data):
        row_cells = tier_table.rows[row_idx + 1].cells
        bg = "F7FAFC" if row_idx % 2 == 0 else "FFFFFF"
        for col_idx, text in enumerate(row):
            row_cells[col_idx].width = t_widths[col_idx]
            set_cell_background(row_cells[col_idx], bg)
            set_cell_margins(row_cells[col_idx], top=100, bottom=100, left=140, right=140)
            p = row_cells[col_idx].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if col_idx in (0, 3) else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(text)
            r.font.size = Pt(9)
            if col_idx == 0:
                r.bold = True
                r.font.color.rgb = COLOR_NAVY
            elif col_idx == 3 and "4" in text:
                r.bold = True
                r.font.color.rgb = RGBColor(0xC5, 0x30, 0x30) # High-priority red accent

    # ==================== SECTION 3: THE END-TO-END FLOW ====================
    add_sec_heading("The Operational Lifecycle: Step-by-Step Lead Journey", 3)
    
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(8)
    p.paragraph_format.line_spacing = 1.15
    p.add_run(
        "The power of PC CRM is how seamlessly each stage connects into the next without human friction or manual data entry. "
        "The following sequential flow illustrates how a prospect moves through the system:"
    )

    flow_steps = [
        ("Step 1: Ingress & Normalization",
         "The lead enters PC CRM through an automated inbound channel (Website Form, Direct Phone Call, WhatsApp Inquiry, or Campaign Landing Page). "
         "The system instantly cleans the phone number, checks for duplicates, and assigns basic metadata."),
         
        ("Step 2: LCS Middleware Processing & Matrix Tiering",
         "LCS processes the lead data. Based on project requirements, budget, and readiness, the middleware automatically calculates the "
         "Fit Score and Intent Score. The lead is stamped with its Matrix Tier (e.g., A1, A2, B1) and marked as a Marketing Qualified Lead (MQL) where applicable."),
         
        ("Step 3: Intelligent Salesperson Assignment",
         "The lead is automatically assigned to a designated salesperson based on territory, expertise (e.g., turnkey tennis vs. pickleball vs. multi-sport), "
         "and current workload. The salesperson is recorded as the official 'Lead Owner'."),
         
        ("Step 4: Dynamic SLA Timer Activation & Task Creation",
         "The moment the lead is assigned, the SLA clock begins ticking. For an A1 lead, exactly 4 hours are allocated. "
         "Simultaneously, PC CRM automatically generates a dedicated 'CRM Task' on the salesperson's workbench titled:\n"
         "• 'Call Lead: [Client Name] (A1 · 4h SLA)'\n"
         "This task contains the exact deadline timestamp, the customer's background, and the pre-selected sales playbook."),
         
        ("Step 5: Real-Time Notifications & 1-Hour Warning Countdown",
         "PC CRM communicates proactively with the sales representative:\n"
         "• Instant Alert: Real-time browser WebSocket push and notification banner when the lead is assigned.\n"
         "• 1-Hour Proactive Warning: Exactly 60 minutes before the SLA deadline, the automated background engine detects that the lead has not yet been contacted. "
         "It triggers an urgent reminder banner directly to the salesperson indicating the exact minutes remaining."),
         
        ("Step 6: SLA Breach Escalation (Failure Safeguard)",
         "If the deadline passes and the salesperson has still not contacted the client, the SLA status is marked as 'Failed'. "
         "PC CRM automatically escalates an urgent breach notification to Sales Managers and System Administrators, ensuring zero lead neglect."),
         
        ("Step 7: Automated SLA Completion & Verification",
         "The salesperson does not need to manually check off checkboxes. As soon as the representative logs a Call Log in PC CRM "
         "or updates the lead to 'Contacted' / 'Qualified', the system automatically marks the SLA as 'Fulfilled', records the exact first-response time, "
         "and marks the task 'Done'.")
    ]

    for title, desc in flow_steps:
        add_sub_heading(title)
        p_step = doc.add_paragraph()
        p_step.paragraph_format.space_before = Pt(2)
        p_step.paragraph_format.space_after = Pt(6)
        p_step.paragraph_format.line_spacing = 1.15
        p_step.add_run(desc)

    # ==================== SECTION 4: STRATEGIC BUSINESS ADVANTAGES ====================
    add_sec_heading("Strategic Business Impact", 4)
    
    advantages = [
        ("Elimination of 'Speed-to-Lead' Decay: ", "Industry benchmarks demonstrate that reaching out to an enterprise prospect within 1 hour increases conversion likelihood by over 700%. PC CRM ensures our highest-tier leads are contacted in hours, not days."),
        ("Removal of Sales Cherry-Picking: ", "Without LCS, salespeople naturally gravitate toward easy, informal leads while letting complex, high-value inquiries linger. LCS enforces fair, high-priority routing."),
        ("Operational Transparency: ", "Every single call attempt, timestamp, and response duration is logged immutably in the CRM database, establishing complete sales accountability."),
        ("Tailored Client Experience: ", "High-value clients receive rapid executive attention and tailored playbooks, elevating PACE Court's brand reputation in the market.")
    ]
    for bold_txt, norm_txt in advantages:
        bp = doc.add_paragraph(style='List Bullet')
        bp.paragraph_format.space_after = Pt(4)
        bp.paragraph_format.line_spacing = 1.15
        r_b = bp.add_run(bold_txt)
        r_b.bold = True
        r_b.font.color.rgb = COLOR_NAVY
        bp.add_run(norm_txt)

    # ==================== SECTION 5: FUTURE DASHBOARD INTEGRATION ====================
    add_sec_heading("Future Roadmap: The Executive Organizational Dashboard", 5)
    
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(8)
    p.paragraph_format.line_spacing = 1.15
    p.add_run(
        "PC CRM is not an isolated silo. It is designed to act as the primary commercial engine feeding real-time operational data "
        "into our forthcoming Executive Organizational Dashboard (Central Business Intelligence Hub)."
    )

    add_callout(
        doc,
        "Vision for Organizational BI: Company leadership will have a live, bird's-eye view of PACE's operational health. "
        "The executive dashboard will pull continuous data streams directly from PC CRM, presenting high-level summaries without "
        "requiring executives to log into the daily CRM task board.",
        title="Executive Visibility & Data Integration"
    )

    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 1.15
    p.add_run("Key performance indicators (KPIs) that the Organizational Dashboard will pull from PC CRM include:")

    bi_metrics = [
        ("Lead Velocity & Matrix Distribution: ", "Live breakdown of total inbound leads sorted by LCS Tiers (A1 vs A2 vs B1). Visualizes whether marketing campaigns are generating high-fit buyers or low-intent inquiries."),
        ("Speed-to-Lead & SLA Compliance Index: ", "Percentage of leads contacted within the target SLA window across regional teams. Instantly highlights operational bottlenecks or rep capacity limits."),
        ("LCS Conversion Economics: ", "Win-rate and revenue generated per matrix tier. Enables leadership to calculate the exact ROI per lead tier and optimize marketing spend accordingly."),
        ("Sales Pipeline Momentum: ", "Total open contract value, average deal cycle length, and pipeline movement from Initial Contact → Site Inspection → Quotation → Won."),
        ("Rep Efficiency & Accountability Scorecards: ", "Objective metrics comparing call volume, average response speed, lead completion rate, and overdue task ratios per team member.")
    ]
    for bold_txt, norm_txt in bi_metrics:
        bp = doc.add_paragraph(style='List Bullet')
        bp.paragraph_format.space_after = Pt(4)
        bp.paragraph_format.line_spacing = 1.15
        r_b = bp.add_run(bold_txt)
        r_b.bold = True
        r_b.font.color.rgb = COLOR_NAVY
        bp.add_run(norm_txt)

    # Data Architecture Table
    p_arch = doc.add_paragraph()
    p_arch.paragraph_format.space_before = Pt(10)
    p_arch.paragraph_format.space_after = Pt(4)
    r_arch_t = p_arch.add_run("Table 2: Data Pipeline from PC CRM to Organizational Dashboard")
    r_arch_t.bold = True
    r_arch_t.font.size = Pt(10)
    r_arch_t.font.color.rgb = COLOR_NAVY

    pipe_table = doc.add_table(rows=5, cols=4)
    pipe_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    pipe_table.autofit = False

    p_widths = [Inches(1.5), Inches(1.8), Inches(1.6), Inches(1.6)]
    p_headers = ["CRM Source Data", "Processing Method", "Sync Frequency", "Dashboard Metric / Visualization"]
    
    hdr_cells = pipe_table.rows[0].cells
    for i, title in enumerate(p_headers):
        hdr_cells[i].width = p_widths[i]
        set_cell_background(hdr_cells[i], "1B365D")
        set_cell_margins(hdr_cells[i], top=120, bottom=120, left=140, right=140)
        p = hdr_cells[i].paragraphs[0]
        r = p.add_run(title)
        r.bold = True
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    pipe_rows = [
        ("CRM Lead Records", "LCS Tier & Score aggregation", "Real-Time / 5 mins", "Tier Distribution & Quality Heatmap"),
        ("CRM Task & SLA Timers", "Time-to-response & Breach calculation", "Hourly Aggregation", "SLA Compliance % & Rep Response Times"),
        ("CRM Call Logs", "Activity volume & duration tracking", "Daily Sync", "Rep Activity & Customer Touchpoints"),
        ("CRM Deals & Value", "Pipeline stage progression & close ratios", "Real-Time", "Revenue Forecast & Conversion Funnel")
    ]

    for row_idx, row in enumerate(pipe_rows):
        row_cells = pipe_table.rows[row_idx + 1].cells
        bg = "F7FAFC" if row_idx % 2 == 0 else "FFFFFF"
        for col_idx, text in enumerate(row):
            row_cells[col_idx].width = p_widths[col_idx]
            set_cell_background(row_cells[col_idx], bg)
            set_cell_margins(row_cells[col_idx], top=100, bottom=100, left=140, right=140)
            p = row_cells[col_idx].paragraphs[0]
            r = p.add_run(text)
            r.font.size = Pt(9)
            if col_idx == 0:
                r.bold = True
                r.font.color.rgb = COLOR_NAVY

    # ==================== SECTION 6: CONCLUSION & ROADMAP ====================
    add_sec_heading("Summary & Next Steps", 6)
    
    p_conc = doc.add_paragraph()
    p_conc.paragraph_format.space_after = Pt(8)
    p_conc.paragraph_format.line_spacing = 1.15
    p_conc.add_run(
        "By building PC CRM in-house and empowering it with the Lead Classification System (LCS) as an intelligent middleware, "
        "PACE has transitioned from manual, reactive sales management into a high-performance, automated sales machine. "
        "Every lead is scored, tiered, assigned, and tracked against uncompromising response standards."
    )

    p_road = doc.add_paragraph()
    p_road.paragraph_format.space_after = Pt(8)
    p_road.paragraph_format.line_spacing = 1.15
    p_road.add_run(
        "Immediate roadmap priorities currently in planning:\n"
        "1. WhatsApp SLA Direct Alerts: Integrating automated WhatsApp reminder messages sent directly to salespeople's mobile phones 1 hour prior to deadline.\n"
        "2. Organizational Dashboard API Connector: Finalizing the automated data warehouse feed to mirror CRM data to the leadership dashboard.\n"
        "3. Predictive Conversion Modeling: Training LCS on historical conversion records to dynamically refine score weights over time."
    )

    doc.save(file_path)
    print(f"Document successfully created at {file_path}")

if __name__ == "__main__":
    output_path = r"c:\PACE\PC_CRM\PC_CRM\PC_CRM_and_LCS_Overview.docx"
    build_document(output_path)
