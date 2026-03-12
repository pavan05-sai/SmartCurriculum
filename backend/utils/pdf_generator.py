# SmartCurriculum - PDF Generator
# Generate curriculum roadmaps as PDF documents

from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image, HRFlowable
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime


def generate_curriculum_pdf(curriculum, user):
    """
    Generate a PDF document for a curriculum roadmap.
    
    Args:
        curriculum: Curriculum model instance
        user: User model instance
        
    Returns:
        BytesIO buffer containing the PDF
    """
    # Create buffer for PDF
    buffer = BytesIO()
    
    # Create document
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )
    
    # Container for elements
    elements = []
    
    # Get styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1a1a2e'),
        spaceAfter=20,
        alignment=TA_CENTER
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Normal'],
        fontSize=12,
        textColor=colors.HexColor('#666666'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#4a4e69'),
        spaceBefore=20,
        spaceAfter=10
    )
    
    subheading_style = ParagraphStyle(
        'CustomSubheading',
        parent=styles['Heading3'],
        fontSize=12,
        textColor=colors.HexColor('#22223b'),
        spaceBefore=15,
        spaceAfter=5
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#333333'),
        spaceAfter=8,
        alignment=TA_JUSTIFY
    )
    
    # Title
    elements.append(Paragraph("SmartCurriculum", title_style))
    elements.append(Paragraph("Personalized Learning Roadmap", subtitle_style))
    
    # Horizontal line
    elements.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#4a4e69')))
    elements.append(Spacer(1, 20))
    
    # User Information Section
    elements.append(Paragraph("Student Profile", heading_style))
    
    user_info = [
        ['Name:', user.name if user else 'Student'],
        ['Career Goal:', (user.career_goal or 'Placement').replace('_', ' ').title() if user else 'Placement'],
        ['Skill Level:', (user.skill_level or 'Beginner').title() if user else 'Beginner'],
        ['Branch:', user.branch if user else 'Computer Science'],
    ]
    
    user_table = Table(user_info, colWidths=[2*inch, 4*inch])
    user_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#333333')),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
    ]))
    elements.append(user_table)
    elements.append(Spacer(1, 20))
    
    # Curriculum Overview Section
    elements.append(Paragraph("Curriculum Overview", heading_style))
    
    overview_info = [
        ['Title:', curriculum.title],
        ['Duration:', f'{curriculum.duration_weeks} weeks'],
        ['Total Hours:', f'{curriculum.total_hours} hours'],
        ['Difficulty:', curriculum.difficulty.title()],
        ['Progress:', f'{curriculum.calculate_progress():.1f}%'],
    ]
    
    overview_table = Table(overview_info, colWidths=[2*inch, 4*inch])
    overview_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#333333')),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
    ]))
    elements.append(overview_table)
    elements.append(Spacer(1, 10))
    
    if curriculum.description:
        elements.append(Paragraph(curriculum.description, body_style))
    
    elements.append(Spacer(1, 20))
    elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#cccccc')))
    
    # Phase-based Roadmap Section
    elements.append(Paragraph("Learning Phases", heading_style))
    elements.append(Spacer(1, 10))
    
    # Organize topics by phase
    topics_by_phase = {}
    phase_order = []
    
    for topic in curriculum.topics:
        phase_name = topic.phase or f"Week {topic.week}"
        if phase_name not in topics_by_phase:
            topics_by_phase[phase_name] = []
            phase_order.append(phase_name)
        topics_by_phase[phase_name].append(topic)
    
    # Render each phase
    for phase_name in phase_order:
        topics = topics_by_phase[phase_name]
        
        # Phase header
        elements.append(Paragraph(phase_name, subheading_style))
        
        # Topics table
        topic_data = [['Topic', 'Hours', 'Status']]
        
        for topic in topics:
            status_symbol = '✓' if topic.status == 'completed' else '○'
            topic_data.append([
                topic.title[:50] + ('...' if len(topic.title) > 50 else ''),
                f"{int(topic.estimated_hours)}h",
                status_symbol
            ])
        
        topic_table = Table(topic_data, colWidths=[4*inch, 0.8*inch, 0.8*inch])
        topic_table.setStyle(TableStyle([
            # Header style
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4a4e69')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            
            # Body style
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#333333')),
            ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
            ('ALIGN', (0, 1), (0, -1), 'LEFT'),
            
            # Grid
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cccccc')),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            
            # Alternating row colors
            *[('BACKGROUND', (0, i), (-1, i), colors.HexColor('#f8f8f8')) 
              for i in range(2, len(topic_data), 2)]
        ]))
        elements.append(topic_table)
        elements.append(Spacer(1, 15))
    
    # Skills Section
    elements.append(PageBreak())
    elements.append(Paragraph("Skills You Will Gain", heading_style))
    elements.append(Spacer(1, 10))
    
    # Collect all skills from topics
    all_skills = set()
    for topic in curriculum.topics:
        all_skills.update(topic.get_skills_gained())
    
    if all_skills:
        skills_text = ', '.join(sorted(all_skills))
        elements.append(Paragraph(skills_text, body_style))
    else:
        elements.append(Paragraph("Skills will be updated as you progress through the curriculum.", body_style))
    
    elements.append(Spacer(1, 30))
    
    # Footer with tips
    elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#cccccc')))
    elements.append(Spacer(1, 20))
    elements.append(Paragraph("Tips for Success", heading_style))
    
    tips = [
        "• Set aside dedicated time each day for learning",
        "• Complete topics in order - they build upon each other",
        "• Practice with hands-on projects after each topic",
        "• Take notes and create summaries",
        "• Review completed topics periodically",
        "• Track your progress regularly"
    ]
    
    for tip in tips:
        elements.append(Paragraph(tip, body_style))
    
    elements.append(Spacer(1, 30))
    
    # Generation date
    date_style = ParagraphStyle(
        'DateStyle',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.HexColor('#999999'),
        alignment=TA_CENTER
    )
    elements.append(Paragraph(
        f"Generated on {datetime.now().strftime('%B %d, %Y')} by SmartCurriculum",
        date_style
    ))
    
    # Build PDF
    doc.build(elements)
    
    # Move to beginning of buffer
    buffer.seek(0)
    
    return buffer


def generate_progress_report_pdf(user, progress_data, analytics_data):
    """
    Generate a progress report PDF for a user.
    
    Args:
        user: User model instance
        progress_data: Dictionary of progress information
        analytics_data: Dictionary of analytics
        
    Returns:
        BytesIO buffer containing the PDF
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()
    
    # Title
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        fontSize=20,
        alignment=TA_CENTER
    )
    elements.append(Paragraph("Learning Progress Report", title_style))
    elements.append(Spacer(1, 20))
    
    # User info
    elements.append(Paragraph(f"Student: {user.name}", styles['Heading2']))
    elements.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d')}", styles['Normal']))
    elements.append(Spacer(1, 20))
    
    # Overview stats
    overview_data = [
        ['Metric', 'Value'],
        ['Topics Completed', str(analytics_data.get('completed_topics', 0))],
        ['Average Score', f"{analytics_data.get('average_score', 0):.1f}%"],
        ['Total Study Time', f"{analytics_data.get('total_time', 0)} hours"],
        ['Skills Acquired', str(analytics_data.get('skills_count', 0))],
    ]
    
    overview_table = Table(overview_data)
    overview_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4a4e69')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('PADDING', (0, 0), (-1, -1), 8),
    ]))
    elements.append(overview_table)
    
    # Build and return
    doc.build(elements)
    buffer.seek(0)
    return buffer
