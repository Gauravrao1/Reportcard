=============================================
🎓 STUDENT REPORT CARD GENERATOR (CLI TOOL)
=============================================

📌 DESCRIPTION
Generate beautiful PDF report cards from CSV file input using Python.

---------------------------------------------
🚀 FEATURES
---------------------------------------------
✔ Automatic PDF generation
✔ Calculates percentage, grade & result
✔ Adds smart teacher remarks
✔ Clean & professional design
✔ Supports multiple students
✔ Fully terminal-based

---------------------------------------------
📁 PROJECT STRUCTURE
---------------------------------------------
.
├── report_generator.py
├── input.csv
├── Report_Cards/
└── README.md

---------------------------------------------
🧾 CSV FORMAT
---------------------------------------------
name,roll_no,class,section,academic_year,Math,Math_Max,Science,Science_Max

Example:
John Doe,101,10,A,2025-2026,85,100,78,100

Rules:
- Each subject must have Subject + Subject_Max
- Column names must match exactly

---------------------------------------------
⚙️ INSTALLATION
---------------------------------------------
git clone https://github.com/your-username/report-card-generator.git
cd report-card-generator
pip install reportlab

---------------------------------------------
▶️ USAGE
---------------------------------------------
python report_generator.py

Then enter:
📁 Enter the path to your CSV file: input.csv

---------------------------------------------
📤 OUTPUT
---------------------------------------------
Report_Cards/
├── ReportCard_John_Doe_101.pdf
├── ReportCard_Jane_Smith_102.pdf

---------------------------------------------
📊 GRADING SYSTEM
---------------------------------------------
A+ : 90 - 100  → Outstanding
A  : 80 - 89   → Excellent
B+ : 70 - 79   → Very Good
B  : 60 - 69   → Good
C+ : 50 - 59   → Above Average
C  : 40 - 49   → Average
D  : 33 - 39   → Pass
F  : <33       → Fail

---------------------------------------------
💬 REMARKS SYSTEM
---------------------------------------------
✔ Auto-generated based on performance
✔ Personalized feedback
✔ Helps improvement tracking

---------------------------------------------
🛠️ TECH STACK
---------------------------------------------
Python 🐍
ReportLab 📄
CSV Module 📊

---------------------------------------------
🧠 WORKFLOW
---------------------------------------------
1. Read CSV file
2. Extract student data
3. Calculate percentage & grade
4. Generate PDF report
5. Save in output folder

---------------------------------------------
❌ ERROR HANDLING
---------------------------------------------
❗ Invalid file path → Error shown
❗ Non-CSV file → Rejected
❗ Missing data → Skipped

---------------------------------------------
📌 SAMPLE RUN
---------------------------------------------
=============================================
🎓 STUDENT REPORT CARD GENERATOR 🎓
=============================================

📁 Enter the path to your CSV file: data.csv

⏳ Generating report cards...

✅ Generated: ReportCard_John_Doe_101.pdf

🎉 SUCCESS! Generated 1 report card(s)

---------------------------------------------
👨‍💻 AUTHOR
---------------------------------------------
Gaurav Rao

---------------------------------------------
⭐ SUPPORT
---------------------------------------------
Star ⭐ | Fork 🍴 | Share 📢

=============================================
