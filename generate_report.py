from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
from reportlab.lib import colors
from datetime import datetime

def create_report():
    doc = SimpleDocTemplate("Project_Development_Report.pdf", pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Title
    title_style = styles['Title']
    story.append(Paragraph("Project Development Report", title_style))
    story.append(Paragraph("Chemical Equipment Parameter Visualizer", styles['Heading2']))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}", styles['Normal']))
    story.append(Spacer(1, 24))

    # Introduction
    story.append(Paragraph("1. Project Overview", styles['Heading2']))
    intro_text = """
    The goal was to build a functional <b>Hybrid Application</b> (Web + Desktop) for visualizing chemical equipment data. 
    The system consists of a centralized Django backend that serves two different frontends: a React-based web app and a PyQt5-based desktop app.
    """
    story.append(Paragraph(intro_text, styles['Normal']))
    story.append(Spacer(1, 12))

    # Backend
    story.append(Paragraph("2. Backend Architecture (Django)", styles['Heading2']))
    backend_bullets = [
        ListItem(Paragraph("<b>REST API</b>: Built using Django REST Framework to handle CSV uploads, parsing, and data retrieval.", styles['Normal'])),
        ListItem(Paragraph("<b>Data Processing</b>: Integrated <i>Pandas</i> to read CSVs, calculate flowrate/pressure averages, and analyze equipment type distributions.", styles['Normal'])),
        ListItem(Paragraph("<b>PDF Generation</b>: Implemented an endpoint using <i>ReportLab</i> to generate dynamic PDF reports of equipment data.", styles['Normal'])),
        ListItem(Paragraph("<b>Authentication</b>: Secured endpoints using Basic Authentication and Django's User system.", styles['Normal'])),
        ListItem(Paragraph("<b>Cloud Readiness</b>: Configured <i>WhiteNoise</i> for static files and <i>Gunicorn</i> for production serving.", styles['Normal']))
    ]
    story.append(ListFlowable(backend_bullets, bulletType='bullet', start='circle'))
    story.append(Spacer(1, 12))

    # Web Frontend
    story.append(Paragraph("3. Web Frontend (React + Vite)", styles['Heading2']))
    web_bullets = [
        ListItem(Paragraph("<b>Tech Stack</b>: React.js, Chart.js, Axios, Vite.", styles['Normal'])),
        ListItem(Paragraph("<b>UI Design</b>: Implemented a 'Premium' aesthetic using CSS variables, gradients, glassmorphism effects, and the 'Inter' font.", styles['Normal'])),
        ListItem(Paragraph("<b>Features</b>: Login screen, File Upload with progress, History sidebar, and Interactive Charts.", styles['Normal'])),
        ListItem(Paragraph("<b>Deployment</b>: Configured for Vercel deployment, ensuring proper handling of environment variables like <i>VITE_API_URL</i> for connecting to the production backend.", styles['Normal']))
    ]
    story.append(ListFlowable(web_bullets, bulletType='bullet', start='circle'))
    story.append(Spacer(1, 12))

    # Desktop Frontend
    story.append(Paragraph("4. Desktop Frontend (PyQt5)", styles['Heading2']))
    desktop_bullets = [
        ListItem(Paragraph("<b>GUI Implementation</b>: Built a native Windows interface using PyQt5 widgets (<i>QTabWidget, QTableWidget</i>).", styles['Normal'])),
        ListItem(Paragraph("<b>Visualization</b>: Embedded <i>Matplotlib</i> figures directly into the PyQt interface for data plotting.", styles['Normal'])),
        ListItem(Paragraph("<b>Integration</b>: Created a custom <i>APIClient</i> with session management to handle authenticated requests to the Django backend.", styles['Normal'])),
        ListItem(Paragraph("<b>Stability</b>: Fixed crashing issues by implementing proper threading and error handling during login.", styles['Normal']))
    ]
    story.append(ListFlowable(desktop_bullets, bulletType='bullet', start='circle'))
    story.append(Spacer(1, 12))

    # Deployment
    story.append(Paragraph("5. Deployment & Challenges Solved", styles['Heading2']))
    deploy_bullets = [
        ListItem(Paragraph("<b>Cross-Platform Git Issues</b>: Solved a critical issue where Windows <i>node_modules</i> were accidentally pushed to GitHub, breaking Linux builds. Fixed by updating <i>.gitignore</i> and clearing the git cache.", styles['Normal'])),
        ListItem(Paragraph("<b>Backend Hosting</b>: Deployed Django to <b>Render</b> using a custom <i>Procfile</i> and environment variables for security.", styles['Normal'])),
        ListItem(Paragraph("<b>Frontend Hosting</b>: Deployed React to <b>Vercel</b>, configuring it to communicate with the Render backend via secure HTTPS.", styles['Normal']))
    ]
    story.append(ListFlowable(deploy_bullets, bulletType='bullet', start='circle'))
    story.append(Spacer(1, 24))

    # Conclusion
    story.append(Paragraph("Conclusion", styles['Heading2']))
    story.append(Paragraph("The project is now fully functional and deployed. Users can upload data via the Web or Desktop, and the persistent SQLite database syncs the history across both platforms.", styles['Normal']))

    doc.build(story)
    print("Report generated successfully: Project_Development_Report.pdf")

if __name__ == "__main__":
    create_report()
