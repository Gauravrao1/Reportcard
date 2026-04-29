"""
Student Report Card Generator
Generates beautiful PDF report cards from CSV file input
"""

import csv
import os
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.graphics.shapes import Drawing, Rect, String
from reportlab.graphics.charts.barcharts import VerticalBarChart

def calculate_grade(percentage):
    """Calculate grade based on percentage"""
    if percentage >= 90:
        return 'A+', 'Outstanding', '#2E7D32'  # Green
    elif percentage >= 80:
        return 'A', 'Excellent', '#388E3C'
    elif percentage >= 70:
        return 'B+', 'Very Good', '#1976D2'  # Blue
    elif percentage >= 60:
        return 'B', 'Good', '#1E88E5'
    elif percentage >= 50:
        return 'C+', 'Above Average', '#F9A825'  # Yellow
    elif percentage >= 40:
        return 'C', 'Average', '#FB8C00'  # Orange
    elif percentage >= 33:
        return 'D', 'Pass', '#E65100'
    else:
        return 'F', 'Needs Improvement', '#C62828'  # Red


def get_remarks(percentage):
    """Generate personalized remarks based on performance"""
    if percentage >= 90:
        return "Exceptional performance! Keep up the outstanding work. You're a role model for others."
    elif percentage >= 80:
        return "Excellent work! You have shown great dedication and understanding of the subjects."
    elif percentage >= 70:
        return "Very good performance! Continue your hard work and aim for excellence."
    elif percentage >= 60:
        return "Good effort! With a little more practice, you can achieve even better results."
    elif percentage >= 50:
        return "Satisfactory performance. Focus on weak areas and seek help when needed."
    elif percentage >= 40:
        return "You have passed, but there is significant room for improvement. Work harder next time."
    elif percentage >= 33:
        return "You have barely passed. Serious effort is required to improve your grades."
    else:
        return "Unfortunately, you need to work much harder. Please seek additional support and guidance."


def create_header(styles):
    """Create report card header elements"""
    elements = []
    
    # School Name
    school_style = ParagraphStyle(
        'SchoolName',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=colors.HexColor('#1565C0'),
        alignment=TA_CENTER,
        spaceAfter=2
    )
    elements.append(Paragraph("🏫 SUNSHINE PUBLIC SCHOOL", school_style))
    
    # School Address
    address_style = ParagraphStyle(
        'Address',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.HexColor('#424242'),
        alignment=TA_CENTER,
        spaceAfter=1
    )
    elements.append(Paragraph("123 Education Street, Knowledge City - 110001", address_style))
    elements.append(Paragraph("Phone: +91-11-12345678 | Email: info@sunshineschool.edu", address_style))
    elements.append(Spacer(1, 5))
    
    # Report Card Title
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.white,
        alignment=TA_CENTER,
        backColor=colors.HexColor('#1976D2'),
        borderPadding=6,
        spaceAfter=8
    )
    elements.append(Paragraph("📋 STUDENT REPORT CARD", title_style))
    elements.append(Spacer(1, 5))
    
    return elements


def create_student_info_table(student_data, styles):
    """Create student information section"""
    info_data = [
        ['Student Name:', student_data.get('name', 'N/A'), 'Roll Number:', student_data.get('roll_no', 'N/A')],
        ['Class:', student_data.get('class', 'N/A'), 'Section:', student_data.get('section', 'N/A')],
        ['Academic Year:', student_data.get('academic_year', '2025-2026'), 'Date:', datetime.now().strftime('%d-%m-%Y')]
    ]
    
    table = Table(info_data, colWidths=[1.5*inch, 2.5*inch, 1.5*inch, 2*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#E3F2FD')),
        ('BACKGROUND', (2, 0), (2, -1), colors.HexColor('#E3F2FD')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1565C0')),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#90CAF9')),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
    ]))
    
    return table


def create_marks_table(subjects_data, styles):
    """Create the marks table with subjects and scores"""
    # Table Header
    header = ['Subject', 'Max Marks', 'Obtained', 'Percentage', 'Grade', 'Status']
    table_data = [header]
    
    for subject in subjects_data:
        name = subject['subject']
        max_marks = subject['max_marks']
        obtained = subject['obtained']
        percentage = (obtained / max_marks) * 100
        grade, _, color = calculate_grade(percentage)
        status = 'PASS' if percentage >= 33 else 'FAIL'
        
        table_data.append([
            name,
            str(max_marks),
            str(obtained),
            f"{percentage:.1f}%",
            grade,
            status
        ])
    
    # Calculate totals
    total_max = sum(s['max_marks'] for s in subjects_data)
    total_obtained = sum(s['obtained'] for s in subjects_data)
    overall_percentage = (total_obtained / total_max) * 100
    overall_grade, _, _ = calculate_grade(overall_percentage)
    overall_status = 'PASS' if overall_percentage >= 33 else 'FAIL'
    
    table_data.append(['TOTAL', str(total_max), str(total_obtained), 
                       f"{overall_percentage:.1f}%", overall_grade, overall_status])
    
    table = Table(table_data, colWidths=[2*inch, 1.2*inch, 1.2*inch, 1.2*inch, 1*inch, 1*inch])
    
    # Styling
    style_commands = [
        # Header
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1565C0')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        
        # Total row
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#FFF3E0')),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        
        # General
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#BBDEFB')),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
    ]
    
    # Color alternate rows
    for i in range(1, len(table_data) - 1):
        if i % 2 == 0:
            style_commands.append(('BACKGROUND', (0, i), (-1, i), colors.HexColor('#E3F2FD')))
        else:
            style_commands.append(('BACKGROUND', (0, i), (-1, i), colors.white))
        
        # Color grade and status based on performance
        percentage = float(table_data[i][3].replace('%', ''))
        _, _, grade_color = calculate_grade(percentage)
        style_commands.append(('TEXTCOLOR', (4, i), (4, i), colors.HexColor(grade_color)))
        
        if percentage >= 33:
            style_commands.append(('TEXTCOLOR', (5, i), (5, i), colors.HexColor('#2E7D32')))
        else:
            style_commands.append(('TEXTCOLOR', (5, i), (5, i), colors.HexColor('#C62828')))
    
    table.setStyle(TableStyle(style_commands))
    return table, overall_percentage


def create_summary_section(percentage, styles):
    """Create the summary section with grade and remarks"""
    elements = []
    
    grade, performance, color = calculate_grade(percentage)
    remarks = get_remarks(percentage)
    
    # Summary Title
    summary_title = ParagraphStyle(
        'SummaryTitle',
        parent=styles['Heading2'],
        fontSize=12,
        textColor=colors.HexColor('#1565C0'),
        alignment=TA_LEFT,
        spaceBefore=8,
        spaceAfter=5
    )
    elements.append(Paragraph("📊 Performance Summary", summary_title))
    
    # Grade Box
    summary_data = [
        ['Overall Percentage', f"{percentage:.2f}%"],
        ['Grade', grade],
        ['Performance', performance],
        ['Result', 'PASSED ✓' if percentage >= 33 else 'NEEDS IMPROVEMENT ✗']
    ]
    
    summary_table = Table(summary_data, colWidths=[2.5*inch, 5*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#E8F5E9') if percentage >= 33 else colors.HexColor('#FFEBEE')),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#1B5E20') if percentage >= 33 else colors.HexColor('#B71C1C')),
        ('TEXTCOLOR', (1, 0), (1, -1), colors.HexColor(color)),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('FONTSIZE', (1, 1), (1, 1), 14),  # Large grade
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#C8E6C9') if percentage >= 33 else colors.HexColor('#FFCDD2')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
    ]))
    elements.append(summary_table)
    elements.append(Spacer(1, 8))
    
    # Remarks
    remarks_title = ParagraphStyle(
        'RemarksTitle',
        parent=styles['Heading2'],
        fontSize=12,
        textColor=colors.HexColor('#1565C0'),
        alignment=TA_LEFT,
        spaceAfter=3
    )
    elements.append(Paragraph("💬 Teacher's Remarks", remarks_title))
    
    # Create remarks in a table for proper alignment
    remarks_table_data = [[remarks]]
    remarks_table = Table(remarks_table_data, colWidths=[7.5*inch])
    remarks_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F5F5F5')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#424242')),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#90CAF9')),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    elements.append(remarks_table)
    elements.append(Spacer(1, 8))
    
    return elements


def create_signature_section(styles):
    """Create signature section"""
    sig_data = [
        ['_________________', '_________________', '_________________'],
        ["Class Teacher", "Principal", "Parent's Signature"]
    ]
    
    sig_table = Table(sig_data, colWidths=[2.5*inch, 2.5*inch, 2.5*inch])
    sig_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 1), (-1, 1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#616161')),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    
    return sig_table


def create_grading_scale(styles):
    """Create grading scale reference"""
    elements = []
    
    scale_title = ParagraphStyle(
        'ScaleTitle',
        parent=styles['Heading2'],
        fontSize=10,
        textColor=colors.HexColor('#1565C0'),
        alignment=TA_LEFT,
        spaceBefore=5,
        spaceAfter=3
    )
    elements.append(Paragraph("📈 Grading Scale", scale_title))
    
    scale_data = [
        ['A+ (90-100%)', 'A (80-89%)', 'B+ (70-79%)', 'B (60-69%)', 'C+ (50-59%)', 'C (40-49%)', 'D (33-39%)', 'F (<33%)']
    ]
    
    scale_table = Table(scale_data, colWidths=[0.95*inch, 0.95*inch, 0.95*inch, 0.95*inch, 0.95*inch, 0.95*inch, 0.95*inch, 0.85*inch])
    scale_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (1, 0), colors.HexColor('#E8F5E9')),
        ('BACKGROUND', (2, 0), (3, 0), colors.HexColor('#E3F2FD')),
        ('BACKGROUND', (4, 0), (5, 0), colors.HexColor('#FFF8E1')),
        ('BACKGROUND', (6, 0), (6, 0), colors.HexColor('#FFF3E0')),
        ('BACKGROUND', (7, 0), (7, 0), colors.HexColor('#FFEBEE')),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#E0E0E0')),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    elements.append(scale_table)
    
    return elements


def generate_report_card(student_data, subjects_data, output_folder):
    """Generate a single student report card PDF"""
    
    # Create output filename
    student_name = student_data.get('name', 'Student').replace(' ', '_')
    roll_no = student_data.get('roll_no', '0')
    filename = f"ReportCard_{student_name}_{roll_no}.pdf"
    filepath = os.path.join(output_folder, filename)
    
    # Create PDF document
    doc = SimpleDocTemplate(
        filepath,
        pagesize=A4,
        rightMargin=0.5*inch,
        leftMargin=0.5*inch,
        topMargin=0.5*inch,
        bottomMargin=0.5*inch
    )
    
    styles = getSampleStyleSheet()
    elements = []
    
    # Add header
    elements.extend(create_header(styles))
    
    # Add student info
    elements.append(create_student_info_table(student_data, styles))
    elements.append(Spacer(1, 8))
    
    # Add marks table section title
    marks_title = ParagraphStyle(
        'MarksTitle',
        parent=styles['Heading2'],
        fontSize=12,
        textColor=colors.HexColor('#1565C0'),
        alignment=TA_LEFT,
        spaceAfter=5
    )
    elements.append(Paragraph("📝 Academic Performance", marks_title))
    
    # Add marks table
    marks_table, percentage = create_marks_table(subjects_data, styles)
    elements.append(marks_table)
    
    # Add summary section
    elements.extend(create_summary_section(percentage, styles))
    
    # Add grading scale
    elements.extend(create_grading_scale(styles))
    elements.append(Spacer(1, 10))
    
    # Add signature section
    elements.append(create_signature_section(styles))
    
    # Build PDF
    doc.build(elements)
    
    return filepath


def parse_csv_and_generate_reports(csv_file_path, output_folder=None):
    """
    Parse CSV file and generate report cards for all students
    
    Expected CSV format:
    name,roll_no,class,section,academic_year,subject1,subject1_max,subject2,subject2_max,...
    
    Example:
    name,roll_no,class,section,academic_year,Math,Math_Max,Science,Science_Max,English,English_Max,Hindi,Hindi_Max,Social,Social_Max
    John Doe,101,10,A,2025-2026,85,100,78,100,92,100,88,100,76,100
    """
    
    if output_folder is None:
        output_folder = os.path.join(os.path.dirname(csv_file_path), 'Report_Cards')
    
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    generated_files = []
    
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        headers = reader.fieldnames
        
        # Find subject columns (columns that have corresponding _Max columns)
        subject_columns = []
        for header in headers:
            if header.endswith('_Max'):
                subject_name = header.replace('_Max', '')
                if subject_name in headers:
                    subject_columns.append(subject_name)
        
        for row in reader:
            # Extract student data
            student_data = {
                'name': row.get('name', row.get('Name', 'Unknown')),
                'roll_no': row.get('roll_no', row.get('Roll_No', row.get('RollNo', '0'))),
                'class': row.get('class', row.get('Class', 'N/A')),
                'section': row.get('section', row.get('Section', 'N/A')),
                'academic_year': row.get('academic_year', row.get('Academic_Year', '2025-2026'))
            }
            
            # Extract subjects data
            subjects_data = []
            for subject in subject_columns:
                try:
                    obtained = float(row.get(subject, 0))
                    max_marks = float(row.get(f'{subject}_Max', 100))
                    subjects_data.append({
                        'subject': subject.replace('_', ' '),
                        'obtained': obtained,
                        'max_marks': max_marks
                    })
                except ValueError:
                    continue
            
            if subjects_data:
                filepath = generate_report_card(student_data, subjects_data, output_folder)
                generated_files.append(filepath)
                print(f"✅ Generated: {filepath}")
    
    return generated_files


def main():
    """Main function to run the report card generator"""
    print("=" * 60)
    print("🎓 STUDENT REPORT CARD GENERATOR 🎓")
    print("=" * 60)
    print()
    
    # Get CSV file path from user
    csv_path = input("📁 Enter the path to your CSV file: ").strip()
    
    # Remove quotes if present
    csv_path = csv_path.strip('"').strip("'")
    
    if not os.path.exists(csv_path):
        print(f"❌ Error: File not found - {csv_path}")
        return
    
    if not csv_path.lower().endswith('.csv'):
        print("❌ Error: Please provide a CSV file")
        return
    
    print()
    print("⏳ Generating report cards...")
    print()
    
    try:
        generated_files = parse_csv_and_generate_reports(csv_path)
        
        print()
        print("=" * 60)
        print(f"🎉 SUCCESS! Generated {len(generated_files)} report card(s)")
        print("=" * 60)
        
        if generated_files:
            output_folder = os.path.dirname(generated_files[0])
            print(f"📂 Output folder: {output_folder}")
            print()
            print("Generated files:")
            for f in generated_files:
                print(f"  📄 {os.path.basename(f)}")
                
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise


if __name__ == "__main__":
    main()
