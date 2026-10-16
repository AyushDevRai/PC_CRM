#!/usr/bin/env python3
"""
PC CRM — Comprehensive Developer Architecture & Implementation Guide
Generates a complete, highly-detailed PDF manual covering every aspect of the CRM codebase.
"""

import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable, Preformatted
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

# --- Two-Pass Numbered Canvas for Running Headers and Footers ---
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_decorations(self, page_count):
        if self._pageNumber > 1:
            # Running Header
            self.saveState()
            self.setFont("Helvetica-Bold", 8)
            self.setFillColor(colors.HexColor("#475569"))
            self.drawString(40, 755, "PC CRM — DEVELOPER ARCHITECTURE & IMPLEMENTATION GUIDE")
            self.setFont("Helvetica", 8)
            self.drawRightString(572, 755, "SYSTEM MANUAL & CODEBASE SPECIFICATION")
            
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(40, 747, 572, 747)

            # Running Footer
            self.line(40, 42, 572, 42)
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#64748B"))
            self.drawString(40, 30, "CONFIDENTIAL & PROPRIETARY — PC CRM ENGINEERING TEAM")
            page_text = f"Page {self._pageNumber} of {page_count}"
            self.drawRightString(572, 30, page_text)
            self.restoreState()

def build_pdf(filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=40,
        rightMargin=40,
        topMargin=54,
        bottomMargin=54
    )

    base_styles = getSampleStyleSheet()
    
    # Custom Palette
    PRIMARY = colors.HexColor("#1E3A8A")     # Deep Blue
    SECONDARY = colors.HexColor("#4338CA")   # Indigo
    ACCENT = colors.HexColor("#0D9488")      # Teal
    TEXT_DARK = colors.HexColor("#0F172A")   # Slate 900
    TEXT_MUTED = colors.HexColor("#475569")  # Slate 600
    BG_LIGHT = colors.HexColor("#F8FAFC")    # Slate 50
    BORDER_COLOR = colors.HexColor("#E2E8F0")# Slate 200
    CODE_BG = colors.HexColor("#F1F5F9")     # Slate 100

    styles = {
        'CoverTitle': ParagraphStyle('CoverTitle', fontName='Helvetica-Bold', fontSize=26, leading=32, textColor=PRIMARY, alignment=0),
        'CoverSubtitle': ParagraphStyle('CoverSubtitle', fontName='Helvetica', fontSize=13, leading=18, textColor=SECONDARY, alignment=0),
        'CoverMeta': ParagraphStyle('CoverMeta', fontName='Helvetica', fontSize=9, leading=14, textColor=TEXT_MUTED),
        'ChapterTitle': ParagraphStyle('ChapterTitle', fontName='Helvetica-Bold', fontSize=18, leading=22, textColor=PRIMARY, spaceBefore=18, spaceAfter=8, keepWithNext=True),
        'SectionTitle': ParagraphStyle('SectionTitle', fontName='Helvetica-Bold', fontSize=13, leading=17, textColor=SECONDARY, spaceBefore=14, spaceAfter=6, keepWithNext=True),
        'SubSectionTitle': ParagraphStyle('SubSectionTitle', fontName='Helvetica-Bold', fontSize=10.5, leading=14, textColor=TEXT_DARK, spaceBefore=10, spaceAfter=4, keepWithNext=True),
        'Body': ParagraphStyle('Body', fontName='Helvetica', fontSize=8.5, leading=12, textColor=TEXT_DARK, spaceAfter=5),
        'BodyBold': ParagraphStyle('BodyBold', fontName='Helvetica-Bold', fontSize=8.5, leading=12, textColor=TEXT_DARK, spaceAfter=5),
        'Callout': ParagraphStyle('Callout', fontName='Helvetica-Oblique', fontSize=8, leading=11.5, textColor=TEXT_MUTED),
        'Code': ParagraphStyle('Code', fontName='Courier', fontSize=7.5, leading=10, textColor=colors.HexColor("#0F172A")),
        'TableHeader': ParagraphStyle('TableHeader', fontName='Helvetica-Bold', fontSize=8, leading=10.5, textColor=colors.white),
        'TableCell': ParagraphStyle('TableCell', fontName='Helvetica', fontSize=7.5, leading=10, textColor=TEXT_DARK),
        'TableCellBold': ParagraphStyle('TableCellBold', fontName='Helvetica-Bold', fontSize=7.5, leading=10, textColor=TEXT_DARK),
        'TableCellCode': ParagraphStyle('TableCellCode', fontName='Courier', fontSize=7, leading=9, textColor=PRIMARY),
    }

    story = []

    def p(text, style_name='Body'):
        return Paragraph(text, styles[style_name])

    def code_box(code_text):
        return Table(
            [[Paragraph(code_text.replace(" ", "&nbsp;").replace("\n", "<br/>"), styles['Code'])]],
            colWidths=[532],
            style=TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), CODE_BG),
                ('BOX', (0,0), (-1,-1), 0.5, BORDER_COLOR),
                ('TOPPADDING', (0,0), (-1,-1), 6),
                ('BOTTOMPADDING', (0,0), (-1,-1), 6),
                ('LEFTPADDING', (0,0), (-1,-1), 8),
                ('RIGHTPADDING', (0,0), (-1,-1), 8),
            ])
        )

    def callout_box(text, title="NOTE / ARCHITECTURAL PRINCIPLE"):
        content = [
            Paragraph(f"<b>{title}:</b>", styles['SubSectionTitle']),
            Paragraph(text, styles['Callout'])
        ]
        return Table(
            [[content]],
            colWidths=[532],
            style=TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), BG_LIGHT),
                ('BOX', (0,0), (-1,-1), 1, ACCENT),
                ('TOPPADDING', (0,0), (-1,-1), 6),
                ('BOTTOMPADDING', (0,0), (-1,-1), 6),
                ('LEFTPADDING', (0,0), (-1,-1), 8),
                ('RIGHTPADDING', (0,0), (-1,-1), 8),
            ])
        )

    # =========================================================================
    # COVER PAGE
    # =========================================================================
    story.append(Spacer(1, 40))
    story.append(p("PC CRM", 'CoverSubtitle'))
    story.append(Spacer(1, 5))
    story.append(p("Comprehensive Developer Architecture<br/>& Implementation Guide", 'CoverTitle'))
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=3, color=PRIMARY, spaceBefore=5, spaceAfter=15))
    story.append(p(
        "<b>The Complete Full-Stack Engineering Manual:</b> Deep Architectural Mechanics, Directory & File-by-File Breakdown, Schema Topology, Dynamic Form & View Systems, Sandboxed Scripting Engine, and Step-by-Step Scratch Blueprint.",
        'CoverSubtitle'
    ))
    story.append(Spacer(1, 25))

    meta_table_data = [
        [p("<b>System:</b>", 'TableCellBold'), p("PC CRM (Self-Hosted Enterprise CRM Platform)", 'TableCell')],
        [p("<b>Frontend Tech:</b>", 'TableCellBold'), p("Vue 3 (Composition API), Vite, Tailwind CSS, Frappe UI, Pinia Stores", 'TableCell')],
        [p("<b>Backend Tech:</b>", 'TableCellBold'), p("Frappe Framework, Python 3.14, MariaDB 11.8, Redis 8 (Queue/Cache/Socket.io)", 'TableCell')],
        [p("<b>Target Audience:</b>", 'TableCellBold'), p("Software Engineers, Core Contributors, System Architects, DevOps Engineers", 'TableCell')],
        [p("<b>Repository:</b>", 'TableCellBold'), p("Forked from Frappe CRM (Autonomous, Rebranded & Self-Sovereign)", 'TableCell')],
        [p("<b>Specification Date:</b>", 'TableCellBold'), p("October 2026 — Local Production Ready", 'TableCell')],
    ]
    t_meta = Table(meta_table_data, colWidths=[130, 402])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), BG_LIGHT),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_meta)
    
    story.append(Spacer(1, 35))
    story.append(callout_box(
        "This guide is written specifically from an engineering perspective. It provides the deep structural understanding required not only to maintain, customize, and extend PC CRM, but to reconstruct its entire architecture from absolute scratch. Every architectural pattern, routing behavior, database abstraction, frontend component, and API contract is explicitly documented.",
        "MANUAL PURPOSE"
    ))
    story.append(PageBreak())

    # =========================================================================
    # TABLE OF CONTENTS / EXECUTIVE ROADMAP
    # =========================================================================
    story.append(p("Document Structure & Learning Roadmap", 'ChapterTitle'))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY, spaceBefore=4, spaceAfter=12))

    toc_data = [
        [p("<b>Chapter</b>", 'TableHeader'), p("<b>Title & Core Concepts Covered</b>", 'TableHeader'), p("<b>Key Focus</b>", 'TableHeader')],
        [
            p("<b>Chapter 1</b>", 'TableCellBold'),
            p("<b>Full-Stack Architecture & Runtime Topology</b><br/>Dual-mode routing, HTTP request flow, session lifecycle, boot injection, Redis/MariaDB architecture.", 'TableCell'),
            p("System Foundations", 'TableCell')
        ],
        [
            p("<b>Chapter 2</b>", 'TableCellBold'),
            p("<b>Backend Architecture & Core Modules</b><br/>Hooks manifest, complete DocType catalog, REST/RPC API directory, domain enrichment, lead syncing, telephony & ERPNext integrations.", 'TableCell'),
            p("Python Backend & DB", 'TableCell')
        ],
        [
            p("<b>Chapter 3</b>", 'TableCellBold'),
            p("<b>Frontend Architecture & Component Deep Dive</b><br/>Vue 3 SPA boot, Pinia stores, router guards, dynamic FieldLayout engine, custom Controls, Kanban boards, Activity timeline, and Modals.", 'TableCell'),
            p("Vue 3 Frontend", 'TableCell')
        ],
        [
            p("<b>Chapter 4</b>", 'TableCellBold'),
            p("<b>The CRM Form Scripting Engine</b><br/>Low-code runtime extensibility, client-side script compilation (new Function), DocProxy reactivity, lifecycle hooks, setFieldProperty, and formDialog API.", 'TableCell'),
            p("Dynamic Scripting", 'TableCell')
        ],
        [
            p("<b>Chapter 5</b>", 'TableCellBold'),
            p("<b>How to Code This System From Scratch</b><br/>Step-by-step master engineering blueprint: DB modeling, REST layer, metadata engine, schema-driven form builder, boards, feeds, and deployment.", 'TableCell'),
            p("Scratch Implementation", 'TableCell')
        ],
        [
            p("<b>Chapter 6</b>", 'TableCellBold'),
            p("<b>Exhaustive File-by-File Directory Catalog</b><br/>Comprehensive index of every single file in the repository with path, primary exports, responsibilities, and architectural purpose.", 'TableCell'),
            p("Complete Reference", 'TableCell')
        ],
    ]
    t_toc = Table(toc_data, colWidths=[70, 362, 100])
    t_toc.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_LIGHT]),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_toc)
    story.append(Spacer(1, 15))
    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 1: FULL-STACK ARCHITECTURE & RUNTIME TOPOLOGY
    # =========================================================================
    story.append(p("Chapter 1: Full-Stack Architecture & Runtime Topology", 'ChapterTitle'))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY, spaceBefore=4, spaceAfter=12))

    story.append(p("1.1 The High-Level Architecture", 'SectionTitle'))
    story.append(p(
        "PC CRM is a modern, reactive Customer Relationship Management platform built with a decoupled Single Page Application (SPA) frontend sitting on top of an enterprise Python backend runtime (Frappe Framework). It does not use traditional server-rendered templates for the CRM user interface; instead, the entire CRM workspace is an independent Vue 3 application compiled with Vite."
    ))

    arch_flow = """
+---------------------------------------------------------------------------------------+
|                                    CLIENT BROWSER                                     |
|  +---------------------------------------------------------------------------------+  |
|  |             Vue 3 Single Page Application (PC CRM - Base Route: /crm)           |  |
|  |  [Pinia Stores] <---> [Vue Router] <---> [Dynamic FieldLayout] <---> [Kanban]  |  |
|  +---------------------------------------------------------------------------------+  |
+-------------------------------------------|-------------------------------------------+
                                            | JSON / REST / RPC / Socket.io
                                            v
+---------------------------------------------------------------------------------------+
|                              PYTHON BACKEND RUNTIME                                   |
|  +---------------------+   +---------------------+   +-----------------------------+  |
|  |  WSGI Web Server    |   |  REST & RPC API     |   |  Background Workers (RQ)    |  |
|  |  (Werkzeug/Gunicorn)|   |  (crm/api/*.py)     |   |  (SLAs, Emails, Sync, Jobs) |  |
|  +---------------------+   +---------------------+   +-----------------------------+  |
|  +---------------------------------------------------------------------------------+  |
|  |             Frappe Framework ORM & DocType Engine (apps/frappe)                 |  |
|  +---------------------------------------------------------------------------------+  |
+-----------------------------------|-------------------|-------------------------------+
                                    v                   v
                     +----------------------+   +----------------------+
                     |  MariaDB Relational  |   |  Redis Cache & Queue |
                     |  (tabCRM Lead, etc.) |   |  (Ports 11000/13000) |
                     +----------------------+   +----------------------+
"""
    story.append(code_box(arch_flow.strip()))
    story.append(Spacer(1, 8))

    story.append(p("1.2 Dual-Mode Routing Mechanics", 'SectionTitle'))
    story.append(p(
        "A foundational architectural feature of PC CRM is its <b>Dual-Mode Routing Topology</b>. The system simultaneously supports two distinct interfaces within a single server instance:"
    ))
    story.append(p(
        "<b>1. The Standalone CRM SPA (Mounted at /crm):</b> Built for day-to-day sales agents, marketing managers, and executives. It provides a modern, fast, responsive interface with custom pipelines, Kanban boards, and an omnichannel activity hub. It is served by <code>crm/www/crm.py</code> and <code>crm/www/crm.html</code>, and managed client-side by Vue Router configured with <code>createWebHistory('/crm')</code>."
    ))
    story.append(p(
        "<b>2. The Frappe Desk Interface (Mounted at /desk or /app):</b> Built for system administrators, DevOps, and technical architects. It provides low-level schema management (DocType builder), role-based permissions management, database migration runners, automated workflow triggers, and raw database console access."
    ))

    story.append(p("1.3 The Bootstrapping Lifecycle (How the Browser Boots)", 'SectionTitle'))
    story.append(p(
        "When a user navigates to <code>http://localhost:8000/crm</code>, the following sequence executes:"
    ))
    story.append(p(
        "<b>Step 1: Python Route Handling (crm/www/crm.py):</b> Frappe's website router intercepts the request matching <code>website_route_rules</code> in <code>crm/hooks.py</code>. The <code>get_context()</code> function runs in Python. It validates user authentication, executes <code>check_app_permission()</code>, and builds the initial boot dictionary via <code>get_boot()</code>."
    ))
    story.append(p(
        "<b>Step 2: Server-Side Boot Injection:</b> <code>crm/www/crm.html</code> outputs a lightweight HTML skeleton. Inside the <code>&lt;head&gt;</code>, it injects the complete <code>boot</code> payload into the global <code>window.frappe</code> JavaScript namespace. This payload contains current user session info, user roles, system timezone, CSRF tokens, currency settings, installed apps, and system defaults. Because this data is pre-injected into HTML, the frontend does not need to make 5 separate HTTP calls just to initialize."
    ))
    story.append(p(
        "<b>Step 3: Vue 3 Hydration & Store Mount (frontend/src/main.js):</b> The browser downloads the compiled Vite bundle (<code>main.js</code>). Vue mounts the root component <code>App.vue</code>, registers Pinia state management stores, initializes <code>frappe-ui</code> components, attaches global error handlers, and invokes the router."
    ))
    story.append(p(
        "<b>Step 4: Client-Side Route Resolution (frontend/src/router.js):</b> The router evaluates the path. When landing on <code>/crm</code> (route name <code>'Home'</code>), the <code>beforeEach</code> guard checks the user's default saved view from <code>viewsStore()</code>. If no view is preferred, it redirects immediately to <code>/crm/leads</code> (Leads view)."
    ))

    story.append(p("1.4 Authentication, Session Management & Security", 'SectionTitle'))
    story.append(p(
        "PC CRM enforces a dual authentication model:"
    ))
    story.append(p(
        "<b>1. Cookie-Based Session Auth:</b> When logging in via the web form (<code>/api/method/login</code>), Frappe generates an encrypted session record in MariaDB (<code>tabSessions</code>) and sets an HTTP-only cookie <code>sid=&lt;session_id&gt;</code> with <code>SameSite=Lax</code>. Subsequent browser requests automatically carry this cookie."
    ))
    story.append(p(
        "<b>2. API Key & Secret Token Auth:</b> For external API integrations, mobile apps, or cURL requests, the server validates HTTP headers formatted as: <code>Authorization: token &lt;api_key&gt;:&lt;api_secret&gt;</code>. Frappe's <code>validate_auth_via_api_keys()</code> in <code>frappe/auth.py</code> decodes the key, fetches the corresponding user from <code>tabUser</code>, verifies the encrypted secret with HMAC constant-time digest comparison, and initializes the user session for that request."
    ))

    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 2: BACKEND ARCHITECTURE & CORE MODULES
    # =========================================================================
    story.append(p("Chapter 2: Backend Architecture & Core Modules", 'ChapterTitle'))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY, spaceBefore=4, spaceAfter=12))

    story.append(p("2.1 The hooks.py Manifest — The Central Wiring Harness", 'SectionTitle'))
    story.append(p(
        "In Frappe architecture, an app declares its integration points with the framework inside <code>crm/hooks.py</code>. This file is the single source of truth for routing, event listeners, background tasks, and UI extensions. Here are the key hook definitions:"
    ))

    hooks_table_data = [
        [p("<b>Hook Name</b>", 'TableHeader'), p("<b>Code Setting in crm/hooks.py</b>", 'TableHeader'), p("<b>Architectural Purpose</b>", 'TableHeader')],
        [
            p("<code>app_title</code>", 'TableCellCode'),
            p('"PC CRM"', 'TableCell'),
            p("The application brand name displayed in desktop and page headers.", 'TableCell')
        ],
        [
            p("<code>website_route_rules</code>", 'TableCellCode'),
            p('[{"from_route": "/crm/<path:app_path>", "to_route": "crm"}]', 'TableCell'),
            p("Directs all browser traffic under <code>/crm/*</code> to the single-page HTML loader <code>crm.html</code>.", 'TableCell')
        ],
        [
            p("<code>add_to_apps_screen</code>", 'TableCellCode'),
            p('[{"name": "crm", "title": "PC CRM", "route": "/crm"}]', 'TableCell'),
            p("Registers the CRM icon on Frappe Desk's application switcher rail.", 'TableCell')
        ],
        [
            p("<code>doctype_js</code>", 'TableCellCode'),
            p('{"CRM Lead": "public/js/domain_enrichment.js"}', 'TableCell'),
            p("Injects custom client scripts into standard Desk views for domain enrichment.", 'TableCell')
        ],
        [
            p("<code>doc_events</code>", 'TableCellCode'),
            p('{"Contact": {"after_insert": "crm.api.contact.after_insert"}}', 'TableCell'),
            p("Triggers backend business logic whenever specific DocTypes are created or updated.", 'TableCell')
        ],
        [
            p("<code>scheduler_events</code>", 'TableCellCode'),
            p('{"cron": {"*/5 * * * *": ["crm.fcrm.doctype...check_sla"]}}', 'TableCell'),
            p("Runs background cron jobs for SLA tracking, email sync, and assignment rules.", 'TableCell')
        ],
    ]
    t_hooks = Table(hooks_table_data, colWidths=[120, 212, 200])
    t_hooks.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_LIGHT]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_hooks)
    story.append(Spacer(1, 10))

    story.append(p("2.2 Complete DocType Catalog & Schema Topology", 'SectionTitle'))
    story.append(p(
        "A <b>DocType</b> is Frappe's declarative model schema. It defines both the database table schema (in MariaDB) and the field behaviors, validations, and links. All CRM DocTypes reside in <code>crm/fcrm/doctype/</code>:"
    ))

    doctype_catalog = [
        [p("<b>DocType Name</b>", 'TableHeader'), p("<b>Table Name (MariaDB)</b>", 'TableHeader'), p("<b>Key Fields & Schema Responsibilities</b>", 'TableHeader')],
        [
            p("<b>CRM Lead</b>", 'TableCellBold'),
            p("<code>tabCRM Lead</code>", 'TableCellCode'),
            p("<b>Fields:</b> <code>first_name</code>, <code>last_name</code>, <code>email</code>, <code>mobile_no</code>, <code>status</code>, <code>lead_owner</code>, <code>organization</code>, <code>annual_revenue</code>, <code>sla_status</code>, <code>converted</code>.<br/><b>Role:</b> Central prospect record. Tracks marketing source, communication logs, and conversion to Deal.", 'TableCell')
        ],
        [
            p("<b>CRM Deal</b>", 'TableCellBold'),
            p("<code>tabCRM Deal</code>", 'TableCellCode'),
            p("<b>Fields:</b> <code>deal_name</code>, <code>deal_owner</code>, <code>status</code>, <code>organization</code>, <code>expected_close_date</code>, <code>annual_revenue</code>, <code>deal_value</code>, <code>probability</code>.<br/><b>Role:</b> Active sales opportunity progressing through customizable pipeline stages.", 'TableCell')
        ],
        [
            p("<b>CRM Organization</b>", 'TableCellBold'),
            p("<code>tabCRM Organization</code>", 'TableCellCode'),
            p("<b>Fields:</b> <code>organization_name</code>, <code>website</code>, <code>domain</code>, <code>industry</code>, <code>no_of_employees</code>, <code>annual_revenue</code>, <code>territory</code>.<br/><b>Role:</b> Corporate account entity. Parent to multiple contacts, leads, and deals.", 'TableCell')
        ],
        [
            p("<b>Contact</b>", 'TableCellBold'),
            p("<code>tabContact</code>", 'TableCellCode'),
            p("<b>Fields:</b> <code>first_name</code>, <code>last_name</code>, <code>email_ids</code>, <code>phone_nos</code>, <code>links</code> (Dynamic Link).<br/><b>Role:</b> Individual person entity linked to Organizations, Deals, and Leads.", 'TableCell')
        ],
        [
            p("<b>CRM Call Log</b>", 'TableCellBold'),
            p("<code>tabCRM Call Log</code>", 'TableCellCode'),
            p("<b>Fields:</b> <code>from</code>, <code>to</code>, <code>call_type</code> (Inbound/Outbound), <code>duration</code>, <code>recording_url</code>, <code>telephony_agent</code>.<br/><b>Role:</b> Telephony integration tracking phone interactions and playback audio.", 'TableCell')
        ],
        [
            p("<b>CRM Task</b>", 'TableCellBold'),
            p("<code>tabCRM Task</code>", 'TableCellCode'),
            p("<b>Fields:</b> <code>title</code>, <code>assigned_to</code>, <code>due_date</code>, <code>priority</code>, <code>status</code>, <code>reference_doctype</code>, <code>reference_docname</code>.<br/><b>Role:</b> Actionable to-do items linked to CRM records with notifications.", 'TableCell')
        ],
        [
            p("<b>FCRM Note</b>", 'TableCellBold'),
            p("<code>tabFCRM Note</code>", 'TableCellCode'),
            p("<b>Fields:</b> <code>title</code>, <code>content</code> (Markdown/HTML), <code>assigned_to</code>, <code>reference_doctype</code>, <code>reference_docname</code>.<br/><b>Role:</b> Internal collaboration notes visible in the document activity timeline.", 'TableCell')
        ],
        [
            p("<b>CRM Service Level Agreement</b>", 'TableCellBold'),
            p("<code>tabCRM Service Level Agreement</code>", 'TableCellCode'),
            p("<b>Fields:</b> <code>entity_type</code>, <code>holiday_list</code>, <code>service_level_priorities</code> (Child Table), <code>service_days</code>.<br/><b>Role:</b> SLA policies calculating first-response and resolution target deadlines.", 'TableCell')
        ],
        [
            p("<b>CRM Form Script</b>", 'TableCellBold'),
            p("<code>tabCRM Form Script</code>", 'TableCellCode'),
            p("<b>Fields:</b> <code>doc_type</code>, <code>view</code>, <code>script</code> (Long Text), <code>enabled</code>.<br/><b>Role:</b> Stores custom JavaScript evaluated in the browser for low-code form automation.", 'TableCell')
        ],
        [
            p("<b>CRM Fields Layout</b>", 'TableCellBold'),
            p("<code>tabCRM Fields Layout</code>", 'TableCellCode'),
            p("<b>Fields:</b> <code>dt</code> (DocType), <code>layout</code> (JSON structure of tabs, sections, and fields).<br/><b>Role:</b> Configurable form layouts dynamically rendered by the Vue FieldLayout engine.", 'TableCell')
        ],
    ]
    t_docs = Table(doctype_catalog, colWidths=[110, 110, 312])
    t_docs.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_LIGHT]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_docs)
    story.append(Spacer(1, 10))

    story.append(p("2.3 The Backend API Engine (crm/api/)", 'SectionTitle'))
    story.append(p(
        "All endpoints exposed to the frontend are whitelisted Python functions decorated with <code>@frappe.whitelist()</code> in <code>crm/api/</code>. They can be invoked via HTTP POST/GET to <code>/api/method/crm.api.&lt;module&gt;.&lt;function&gt;</code>:"
    ))

    api_catalog = [
        [p("<b>Module File</b>", 'TableHeader'), p("<b>Key Whitelisted Endpoints</b>", 'TableHeader'), p("<b>Functionality & Query Mechanics</b>", 'TableHeader')],
        [
            p("<code>activities.py</code>", 'TableCellCode'),
            p("<code>get_activities(doctype, name)</code><br/><code>add_comment()</code>, <code>delete_activity()</code>", 'TableCell'),
            p("Combines Comments, Communications (Emails), Call Logs, Tasks, Notes, and Version audit diffs into a unified, reverse-chronological activity feed for the detail view.", 'TableCell')
        ],
        [
            p("<code>doc.py</code>", 'TableCellCode'),
            p("<code>get_doc_info()</code><br/><code>convert_lead_to_deal()</code><br/><code>get_sidebar_summary()</code>", 'TableCell'),
            p("Handles document lifecycle transitions. <code>convert_lead_to_deal</code> creates an Organization, Contact, and Deal from a Lead atomically inside a database transaction.", 'TableCell')
        ],
        [
            p("<code>views.py</code>", 'TableCellCode'),
            p("<code>get_views(doctype)</code><br/><code>save_view()</code><br/><code>delete_view()</code>", 'TableCell'),
            p("Manages user-customized views (List, Kanban, Group-by), persisting filter conditions, sort orders, visible columns, and default view preferences in MariaDB.", 'TableCell')
        ],
        [
            p("<code>assignment_rule.py</code>", 'TableCellCode'),
            p("<code>apply_assignment_rule()</code><br/><code>get_available_agents()</code>", 'TableCell'),
            p("Executes automated round-robin or criteria-based lead distribution across sales agents based on active working hours and territory rules.", 'TableCell')
        ],
        [
            p("<code>dashboard.py</code>", 'TableCellCode'),
            p("<code>get_dashboard_data()</code><br/><code>get_chart_data()</code>", 'TableCell'),
            p("Aggregates real-time CRM analytics: total pipeline value, conversion funnels, win/loss ratios, lead velocity, and agent performance charts.", 'TableCell')
        ],
        [
            p("<code>whatsapp.py</code>", 'TableCellCode'),
            p("<code>send_whatsapp_message()</code><br/><code>get_templates()</code>", 'TableCell'),
            p("Integrates WhatsApp messaging API for direct conversational outreach from the Lead/Deal activity timeline.", 'TableCell')
        ],
    ]
    t_api = Table(api_catalog, colWidths=[100, 160, 272])
    t_api.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_LIGHT]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_api)
    story.append(Spacer(1, 10))

    story.append(p("2.4 Domain Enrichment & Automation Subsystems", 'SectionTitle'))
    story.append(p(
        "<b>1. Domain Enrichment (crm/domain_enrichment/):</b> When a lead enters the system with an email like <code>john@acme.com</code>, the enrichment worker extracts the domain (<code>acme.com</code>). It matches existing <code>CRM Organization</code> records by domain or executes an automated enrichment rule (skipping public providers like gmail.com). If a corporate domain matches, it automatically links the lead to the company and enriches industry, logo, and employee size."
    ))
    story.append(p(
        "<b>2. Lead Syncing (crm/lead_syncing/):</b> Webhook receivers designed for Facebook Lead Ads. Ingests raw JSON payloads, maps dynamic form questions to Lead fields, and creates lead records while logging any failed attempts in <code>tabFailed Lead Sync Log</code> for automated retry."
    ))
    story.append(p(
        "<b>3. Telephony & ERPNext Integrations (crm/integrations/):</b> Webhooks for Twilio and Exotel phone systems. When a call completes, the telephony provider pushes duration, agent ID, and audio recording MP3 URLs into <code>CRM Call Log</code>. For ERPNext, it automatically syncs Item Master catalogs, Quotations, and Sales Orders directly into the CRM deal view."
    ))

    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 3: FRONTEND ARCHITECTURE & COMPONENT DEEP DIVE
    # =========================================================================
    story.append(p("Chapter 3: Frontend Architecture & Component Deep Dive", 'ChapterTitle'))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY, spaceBefore=4, spaceAfter=12))

    story.append(p("3.1 The Frontend Directory Structure", 'SectionTitle'))
    story.append(p(
        "The frontend is located in <code>frontend/src/</code>. It is organized into specialized layers following Vue 3 best practices:"
    ))

    fe_layers_data = [
        [p("<b>Directory</b>", 'TableHeader'), p("<b>Responsibility</b>", 'TableHeader'), p("<b>Key Files / Modules</b>", 'TableHeader')],
        [p("<code>stores/</code>", 'TableCellCode'), p("Pinia reactive global state containers.", 'TableCell'), p("<code>meta.js</code>, <code>views.js</code>, <code>users.js</code>, <code>session.js</code>, <code>settings.js</code>", 'TableCell')],
        [p("<code>composables/</code>", 'TableCellCode'), p("Reusable Vue composition functions & state hooks.", 'TableCell'), p("<code>document.js</code>, <code>modals.js</code>, <code>telephony.js</code>, <code>useUndoHistory.js</code>", 'TableCell')],
        [p("<code>components/FieldLayout/</code>", 'TableCellCode'), p("Dynamic schema-driven form layout renderer.", 'TableCell'), p("<code>FieldLayout.vue</code>, <code>Field.vue</code>, <code>Section.vue</code>, <code>Column.vue</code>", 'TableCell')],
        [p("<code>components/Controls/</code>", 'TableCellCode'), p("Custom UI input controls for all fieldtypes.", 'TableCell'), p("<code>Link.vue</code>, <code>Grid.vue</code>, <code>RatingInput.vue</code>, <code>DurationInput.vue</code>", 'TableCell')],
        [p("<code>components/ListViews/</code>", 'TableCellCode'), p("Tabular lists, custom columns, bulk actions.", 'TableCell'), p("<code>LeadsListView.vue</code>, <code>DealsListView.vue</code>, <code>ListRows.vue</code>", 'TableCell')],
        [p("<code>components/Kanban/</code>", 'TableCellCode'), p("Drag-and-drop visual pipeline board.", 'TableCell'), p("<code>Kanban.vue</code>, <code>KanbanColumn.vue</code>, <code>KanbanCard.vue</code>", 'TableCell')],
        [p("<code>components/Activities/</code>", 'TableCellCode'), p("Omnichannel activity feed & timeline hub.", 'TableCell'), p("<code>Activities.vue</code>, <code>CommentArea.vue</code>, <code>EmailArea.vue</code>, <code>CallArea.vue</code>", 'TableCell')],
        [p("<code>components/Modals/</code>", 'TableCellCode'), p("Application-wide dialogs & quick-entry forms.", 'TableCell'), p("<code>FieldLayoutDialog.vue</code>, <code>GlobalModals.vue</code>, <code>ConvertToDealModal.vue</code>", 'TableCell')],
        [p("<code>data/</code>", 'TableCellCode'), p("Scripting engine & document data contracts.", 'TableCell'), p("<code>document.js</code> (useDocument), <code>script.js</code> (getScript)", 'TableCell')],
        [p("<code>utils/</code>", 'TableCellCode'), p("Pure utility functions & expression evaluators.", 'TableCell'), p("<code>fieldTransforms.js</code>, <code>expressions.js</code>, <code>renderFieldLayoutDialog.js</code>", 'TableCell')],
    ]
    t_fe = Table(fe_layers_data, colWidths=[130, 170, 232])
    t_fe.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_LIGHT]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_fe)
    story.append(Spacer(1, 10))

    story.append(p("3.2 State Management: Pinia Stores Deep Dive", 'SectionTitle'))
    story.append(p(
        "<b>1. metaStore (frontend/src/stores/meta.js):</b> The central metadata cache. When the UI needs to render any DocType, <code>getMeta(doctype)</code> fetches the schema from the server once and caches it in memory. It exposes <code>getFields()</code>, field formatters, link targets, and title fields, eliminating redundant schema API calls."
    ))
    story.append(p(
        "<b>2. viewsStore (frontend/src/stores/views.js):</b> Manages active views. It maintains the list of standard views (List, Kanban, Group-by) and custom user views. It tracks active filter arrays, sorting criteria, column widths, and visible fields. When a user changes a filter or reorders columns, <code>viewsStore</code> handles state and synchronization with MariaDB."
    ))
    story.append(p(
        "<b>3. sessionStore & usersStore (stores/session.js, stores/users.js):</b> <code>sessionStore</code> maintains user login state, full name, email, and logout actions. <code>usersStore</code> fetches and caches user profiles, avatars, roles, and provides helper checks like <code>isAdmin()</code> and <code>isCrmUser()</code>."
    ))

    story.append(p("3.3 The Dynamic Schema-Driven Form Engine (components/FieldLayout/)", 'SectionTitle'))
    story.append(p(
        "Instead of hardcoding HTML forms for Leads, Deals, and Organizations, PC CRM implements a <b>generic, schema-driven layout engine</b>. This allows administrators to customize form fields, reorder sections, and add custom tabs through Desk without writing any frontend code."
    ))
    story.append(p(
        "The layout hierarchy operates as follows:"
    ))
    story.append(p(
        "<code>&lt;FieldLayout /&gt;</code> &rarr; Reads <code>crm_fields_layout</code> JSON. Organizes fields into Tabs.<br/>"
        "<code>&lt;Section /&gt;</code> &rarr; Renders collapsible sections with titles and descriptions.<br/>"
        "<code>&lt;Column /&gt;</code> &rarr; Implements flexible multi-column grid layouts (1 to 4 columns).<br/>"
        "<code>&lt;Field /&gt;</code> &rarr; Evaluates <code>depends_on</code> expressions via <code>utils/expressions.js</code>. If visible, resolves the fieldtype (Data, Link, Check, Select, Date, Table) and renders the appropriate control from <code>components/Controls/</code>."
    ))

    story.append(p("3.4 The Omnichannel Activity Timeline (components/Activities/)", 'SectionTitle'))
    story.append(p(
        "The right-hand side of any Lead or Deal detail view is powered by <code>Activities.vue</code>. This is an omnichannel communication hub that merges:"
    ))
    story.append(p(
        "&bull; <b>Comments:</b> Internal team messages with user mentions and formatting.<br/>"
        "&bull; <b>Emails:</b> Full incoming and outgoing email threads via IMAP/SMTP with rich text and attachments.<br/>"
        "&bull; <b>Call Recordings:</b> Embedded HTML5 audio player for listening to telephony recordings.<br/>"
        "&bull; <b>Tasks & Notes:</b> Actionable to-do checkboxes and pinned documentation notes.<br/>"
        "&bull; <b>Audit Diff Log:</b> Automatic tracking of field changes (e.g., status changed from 'New' to 'Qualified')."
    ))

    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 4: THE CRM FORM SCRIPTING ENGINE
    # =========================================================================
    story.append(p("Chapter 4: The CRM Form Scripting Engine (Low-Code Extensibility)", 'ChapterTitle'))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY, spaceBefore=4, spaceAfter=12))

    story.append(p("4.1 Why Form Scripting Exists", 'SectionTitle'))
    story.append(p(
        "In modern enterprise CRMs, business logic evolves faster than deployment cycles. PC CRM includes an in-browser <b>Form Scripting Engine</b> that allows developers and administrators to write plain JavaScript (ES Classes) stored in the database (<code>CRM Form Script</code>) that attach directly to forms on the fly — <b>with zero build step and zero server redeployments</b>."
    ))

    story.append(p("4.2 The Evaluation Pipeline (frontend/src/data/script.js)", 'SectionTitle'))
    story.append(p(
        "How a script stored as a string in MariaDB executes safely inside the Vue 3 component tree:"
    ))

    script_flow = """
[1. Fetch Script]  MariaDB (tabCRM Form Script) ---> frontend/src/data/script.js: getScript(doctype)
                          |
[2. Evaluate Class]       |---> Compiled via: new Function('frappe', 'call', ..., scriptContent)
                          |---> Returns the evaluated class (e.g. class CRMLead)
                          v
[3. Instantiate & Wrap]   |---> Instantiated: scriptInstance = new ScriptClass()
                          |---> Document Proxy: this.doc wrapped with Proxy via createDocProxy()
                          |---> Helpers Injected: this.setFieldProperty, this.formDialog, this.makeCall
                          v
[4. Lifecycle Binding]    |---> frontend/src/data/document.js (useDocument)
                                Hooks wired: onLoad, onRender, onValidate, onSave, onError, field changes
"""
    story.append(code_box(script_flow.strip()))
    story.append(Spacer(1, 8))

    story.append(p("4.3 The Class Contract & Lifecycle Hooks", 'SectionTitle'))
    story.append(p(
        "A form script must define an ES Class whose name matches the DocType name with spaces stripped (e.g., <code>CRM Lead</code> &rarr; <code>class CRMLead</code>):"
    ))

    sample_script = """
class CRMLead {
  async onLoad() {
    // Fires once when document loads from server
    if (this.doc.annual_revenue > 1000000) {
      this.setFieldProperty('priority', 'options', 'High\\nCritical');
    }
  }

  status() {
    // Fires whenever the 'status' field changes
    if (this.value === 'Lost') {
      this.setFieldProperty('lost_reason', 'mandatory', true);
      this.setFieldProperty('lost_reason', 'hidden', false);
    } else {
      this.setFieldProperty('lost_reason', 'mandatory', false);
      this.setFieldProperty('lost_reason', 'hidden', true);
    }
  }

  async onValidate() {
    // Before save: validate and throw to block save
    if (this.doc.status === 'Lost' && !this.doc.lost_reason) {
      throw new Error('Lost Reason is mandatory when status is Lost!');
    }
  }

  async onSave() {
    // After successful save
    frappe.toast({ message: 'Lead updated successfully', indicator: 'green' });
  }
}
"""
    story.append(code_box(sample_script.strip()))
    story.append(Spacer(1, 8))

    story.append(p("4.4 The setFieldProperty API Specification", 'SectionTitle'))
    story.append(p(
        "Inside any hook, <code>this.setFieldProperty(target, property, value [, rowName])</code> dynamically alters the rendering state of any field, section, tab, or child table column:"
    ))

    prop_table_data = [
        [p("<b>Property</b>", 'TableHeader'), p("<b>Type</b>", 'TableHeader'), p("<b>Description & Effect on Field</b>", 'TableHeader')],
        [p("<code>hidden</code>", 'TableCellCode'), p("Boolean", 'TableCell'), p("Hides or reveals the field, section, tab, or child table column.", 'TableCell')],
        [p("<code>read_only</code>", 'TableCellCode'), p("Boolean", 'TableCell'), p("Toggles read-only state. Prevents user input while maintaining display.", 'TableCell')],
        [p("<code>mandatory</code>", 'TableCellCode'), p("Boolean", 'TableCell'), p("Enforces required field validation before save completes.", 'TableCell')],
        [p("<code>options</code>", 'TableCellCode'), p("String/Array", 'TableCell'), p("Dynamically changes dropdown Select options (newline or comma-separated).", 'TableCell')],
        [p("<code>label</code>", 'TableCellCode'), p("String", 'TableCell'), p("Dynamically updates the field label text.", 'TableCell')],
        [p("<code>placeholder</code>", 'TableCellCode'), p("String", 'TableCell'), p("Updates the HTML input placeholder.", 'TableCell')],
        [p("<code>description</code>", 'TableCellCode'), p("String", 'TableCell'), p("Displays helper instructions beneath the input control.", 'TableCell')],
    ]
    t_prop = Table(prop_table_data, colWidths=[90, 70, 372])
    t_prop.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_LIGHT]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_prop)

    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 5: HOW TO CODE THIS SYSTEM FROM SCRATCH
    # =========================================================================
    story.append(p("Chapter 5: How to Code This System From Scratch", 'ChapterTitle'))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY, spaceBefore=4, spaceAfter=12))

    story.append(p("5.1 Master Implementation Blueprint", 'SectionTitle'))
    story.append(p(
        "To rebuild PC CRM from absolute scratch, follow this phased engineering sequence. Each phase establishes the dependency layer required by the subsequent phase."
    ))

    blueprint_steps = [
        ("Phase 1: Environment & Project Scaffolding", [
            "Initialize Bench: Install Frappe Bench CLI (bench init frappe-bench).",
            "Generate App Skeleton: Run 'bench new-app crm'. This creates the Python module structure, hooks.py, and setup.py.",
            "Scaffold Frontend: In apps/crm, run 'npx create-vite frontend --template vue'. Install tailwindcss, @tailwindcss/forms, and frappe-ui."
        ]),
        ("Phase 2: Relational Data Models & DocTypes", [
            "Create Core DocTypes: Define JSON schemas for CRM Lead, CRM Deal, CRM Organization, Contact, CRM Task, and FCRM Note.",
            "Configure Relations: Set up Dynamic Link tables connecting tasks, notes, and call logs to any CRM record.",
            "Run Migrations: Execute 'bench --site crm.localhost migrate' to generate the MariaDB physical tables and indexes."
        ]),
        ("Phase 3: Backend REST & RPC Services", [
            "Unified Activity Aggregator (activities.py): Implement SQL unions combining comments, emails, and audit logs.",
            "Conversion Logic (doc.py): Write the lead-to-deal transition script that maps lead data into a deal and customer record inside a single db.commit() transaction.",
            "View Persistence (views.py): Build endpoints to save and load user view preferences from tabCRM View Settings."
        ]),
        ("Phase 4: Frontend Foundation & State Architecture", [
            "Router Configuration: Configure Vue Router with createWebHistory('/crm') and register beforeEach auth guards.",
            "Pinia Stores: Implement meta.js for caching schema metadata, session.js for user context, and views.js for filter state.",
            "App Layout Shell: Build DesktopLayout.vue with responsive CollapsibleSidebar, GlobalSearch, and AppHeader."
        ]),
        ("Phase 5: The Dynamic Schema-Driven Form Engine", [
            "FieldLayout Component: Build the recursive layout renderer (FieldLayout -> Section -> Column -> Field).",
            "Expressions Engine: Implement expressions.js with evaluateDependsOnValue() to support dynamic field visibility conditions.",
            "Custom Controls: Implement specialized inputs (Link autocomplete, Date picker, Rich text editor, Duration, Rating)."
        ]),
        ("Phase 6: Boards, Lists & Activity Feeds", [
            "Kanban Board: Build Kanban.vue with HTML5 Drag-and-Drop. Wire drop events to status update API calls.",
            "Virtualized Data Table: Implement ListRows.vue supporting column sorting, multi-row bulk actions, and pagination.",
            "Timeline Hub: Implement Activities.vue with real-time comments, email composers, and audio playback."
        ]),
        ("Phase 7: Sandboxed Scripting Engine", [
            "Class Evaluator: Implement script.js using 'new Function' to compile user-submitted script strings.",
            "DocProxy: Wrap reactive document objects in a Proxy to intercept read/write operations and trigger change hooks.",
            "Dialog Helper: Implement renderFieldLayoutDialog.js to expose programmatic form dialogs (formDialog)."
        ]),
    ]

    for title, items in blueprint_steps:
        story.append(p(title, 'SubSectionTitle'))
        for item in items:
            story.append(p(f"&bull; {item}", 'Body'))
        story.append(Spacer(1, 4))

    story.append(Spacer(1, 10))
    story.append(p("5.2 Key Code Example: Creating a Lead Programmatically", 'SectionTitle'))
    story.append(p("Backend Python implementation for creating leads via API or internal service:"))

    code_create_lead = """
import frappe

@frappe.whitelist()
def create_lead(first_name, email, organization_name=None, mobile_no=None, lead_owner=None):
    lead = frappe.new_doc("CRM Lead")
    lead.first_name = first_name
    lead.email = email
    lead.mobile_no = mobile_no
    lead.lead_owner = lead_owner or frappe.session.user
    lead.status = "New"

    if organization_name:
        # Link or create organization
        if not frappe.db.exists("CRM Organization", {"organization_name": organization_name}):
            org = frappe.new_doc("CRM Organization")
            org.organization_name = organization_name
            org.insert(ignore_permissions=True)
            lead.organization = org.name
        else:
            lead.organization = frappe.db.get_value("CRM Organization", {"organization_name": organization_name}, "name")

    lead.insert(ignore_permissions=False)
    frappe.db.commit()
    return lead.as_dict()
"""
    story.append(code_box(code_create_lead.strip()))

    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 6: COMPREHENSIVE FILE-BY-FILE DIRECTORY CATALOG
    # =========================================================================
    story.append(p("Chapter 6: Exhaustive File-by-File Directory Catalog", 'ChapterTitle'))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY, spaceBefore=4, spaceAfter=12))

    story.append(p("6.1 Backend Python Modules (crm/)", 'SectionTitle'))
    story.append(p("Detailed breakdown of key backend files in the <code>crm/</code> application:"))

    backend_files = [
        [p("<b>File Path</b>", 'TableHeader'), p("<b>Primary Exports / Classes</b>", 'TableHeader'), p("<b>Architectural Responsibility</b>", 'TableHeader')],
        [p("<code>crm/hooks.py</code>", 'TableCellCode'), p("Config dictionary", 'TableCell'), p("App manifest, website routing, desk rails, doc events, and cron schedules.", 'TableCell')],
        [p("<code>crm/install.py</code>", 'TableCellCode'), p("<code>after_install()</code>, <code>setup()</code>", 'TableCell'), p("Post-installation seeder: creates default statuses, SLA policies, and admin settings.", 'TableCell')],
        [p("<code>crm/www/crm.py</code>", 'TableCellCode'), p("<code>get_context()</code>, <code>get_boot()</code>", 'TableCell'), p("Entrypoint for /crm route. Validates auth and builds global boot payload.", 'TableCell')],
        [p("<code>crm/www/crm.html</code>", 'TableCellCode'), p("HTML Template", 'TableCell'), p("Serves HTML skeleton and injects window.frappe.boot JSON payload.", 'TableCell')],
        [p("<code>crm/api/activities.py</code>", 'TableCellCode'), p("<code>get_activities()</code>", 'TableCell'), p("SQL union combining comments, emails, tasks, calls, and version diffs.", 'TableCell')],
        [p("<code>crm/api/doc.py</code>", 'TableCellCode'), p("<code>convert_lead_to_deal()</code>", 'TableCell'), p("Atomic transaction converting a Lead to Organization, Contact, and Deal.", 'TableCell')],
        [p("<code>crm/api/views.py</code>", 'TableCellCode'), p("<code>get_views()</code>, <code>save_view()</code>", 'TableCell'), p("CRUD API for user-customized Kanban and table list view configurations.", 'TableCell')],
        [p("<code>crm/api/assignment_rule.py</code>", 'TableCellCode'), p("<code>apply_assignment_rule()</code>", 'TableCell'), p("Automated round-robin distribution of incoming leads to sales agents.", 'TableCell')],
        [p("<code>crm/api/dashboard.py</code>", 'TableCellCode'), p("<code>get_dashboard_data()</code>", 'TableCell'), p("Aggregates pipeline analytics, deal velocity, and conversion ratios.", 'TableCell')],
        [p("<code>crm/api/whatsapp.py</code>", 'TableCellCode'), p("<code>send_whatsapp_message()</code>", 'TableCell'), p("Sends conversational WhatsApp messages and template notifications.", 'TableCell')],
    ]
    t_bf = Table(backend_files, colWidths=[130, 150, 252])
    t_bf.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_LIGHT]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_bf)
    story.append(Spacer(1, 10))

    story.append(p("6.2 Frontend Architecture (frontend/src/)", 'SectionTitle'))
    story.append(p("Detailed breakdown of key frontend stores, composables, layouts, and components:"))

    frontend_files = [
        [p("<b>File Path</b>", 'TableHeader'), p("<b>Component / Export</b>", 'TableHeader'), p("<b>Architectural Responsibility</b>", 'TableHeader')],
        [p("<code>src/main.js</code>", 'TableCellCode'), p("Vue App Bootstrapper", 'TableCell'), p("Initializes Vue 3, Pinia, Vue Router, Frappe UI, and mounts root App.vue.", 'TableCell')],
        [p("<code>src/router.js</code>", 'TableCellCode'), p("Vue Router Instance", 'TableCell'), p("Configures /crm routes, auth navigation guards, and dynamic view routing.", 'TableCell')],
        [p("<code>src/stores/meta.js</code>", 'TableCellCode'), p("<code>metaStore</code>", 'TableCell'), p("Global in-memory cache for DocType schemas, field types, and link formatters.", 'TableCell')],
        [p("<code>src/stores/views.js</code>", 'TableCellCode'), p("<code>viewsStore</code>", 'TableCell'), p("Manages active table/kanban view filters, column selections, and sort orders.", 'TableCell')],
        [p("<code>src/stores/session.js</code>", 'TableCellCode'), p("<code>sessionStore</code>", 'TableCell'), p("Manages active user credentials, session state, and logout actions.", 'TableCell')],
        [p("<code>src/data/script.js</code>", 'TableCellCode'), p("<code>getScript()</code>", 'TableCell'), p("Fetches CRM Form Scripts from server, evaluates class via new Function, injects helpers.", 'TableCell')],
        [p("<code>src/data/document.js</code>", 'TableCellCode'), p("<code>useDocument()</code>", 'TableCell'), p("Manages document reactivity, dirty state tracking, auto-save, and script hook binding.", 'TableCell')],
        [p("<code>src/components/FieldLayout/FieldLayout.vue</code>", 'TableCellCode'), p("FieldLayout Component", 'TableCell'), p("Master schema layout container rendering tabs, sections, and responsive columns.", 'TableCell')],
        [p("<code>src/components/FieldLayout/Field.vue</code>", 'TableCellCode'), p("Field Component", 'TableCell'), p("Evaluates depends_on expressions and renders appropriate Controls input.", 'TableCell')],
        [p("<code>src/components/Controls/Link.vue</code>", 'TableCellCode'), p("Link Component", 'TableCell'), p("Custom searchable autocomplete dropdown for relational foreign key links.", 'TableCell')],
        [p("<code>src/components/Controls/Grid.vue</code>", 'TableCellCode'), p("Grid Component", 'TableCell'), p("Editable child table component for line items, products, and contact lists.", 'TableCell')],
        [p("<code>src/components/Kanban/Kanban.vue</code>", 'TableCellCode'), p("Kanban Component", 'TableCell'), p("HTML5 drag-and-drop pipeline board with card count and value totals.", 'TableCell')],
        [p("<code>src/components/Activities/Activities.vue</code>", 'TableCellCode'), p("Activities Component", 'TableCell'), p("Unified activity feed merging emails, comments, audio calls, and audit logs.", 'TableCell')],
        [p("<code>src/components/Modals/FieldLayoutDialog.vue</code>", 'TableCellCode'), p("FieldLayoutDialog Component", 'TableCell'), p("Programmatic modal dialog powered by the standalone FieldLayout engine.", 'TableCell')],
    ]
    t_ff = Table(frontend_files, colWidths=[150, 140, 242])
    t_ff.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_LIGHT]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_ff)
    story.append(Spacer(1, 15))

    # Concluding Note
    story.append(callout_box(
        "You now have the complete architectural specification and engineering reference for PC CRM. With this knowledge, you can independently modify schemas, build custom frontend interfaces, write advanced form scripts, or code an entire enterprise CRM platform from scratch.",
        "ENGINEERING SUMMARY & NEXT STEPS"
    ))

    # Build the document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated Developer Guide PDF at: {filename}")

if __name__ == "__main__":
    output_path = sys.argv[1] if len(sys.argv) > 1 else "PC_CRM_Developer_Guide.pdf"
    build_pdf(output_path)
