from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
import os

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# Color scheme
DARK_BLUE = RGBColor(0x2C, 0x3E, 0x50)
BLUE = RGBColor(0x34, 0x98, 0xDB)
LIGHT_BLUE = RGBColor(0x5D, 0xAE, 0xE0)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT_GRAY = RGBColor(0xEC, 0xF0, 0xF1)
GOLD = RGBColor(0xD4, 0xA8, 0x43)
DARK_GRAY = RGBColor(0x33, 0x33, 0x33)

def add_background(slide, color):
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color

def add_shape(slide, left, top, width, height, color, alpha=None):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    if alpha is not None:
        from lxml import etree
        solidFill = shape.fill._fill
        srgbClr = solidFill.find('.//{http://schemas.openxmlformats.org/drawingml/2006/main}srgbClr')
        if srgbClr is not None:
            alpha_elem = etree.SubElement(srgbClr, '{http://schemas.openxmlformats.org/drawingml/2006/main}alpha')
            alpha_elem.set('val', str(int(alpha * 1000)))
    return shape

def add_text_box(slide, left, top, width, height, text, font_size=18, color=DARK_GRAY, bold=False, alignment=PP_ALIGN.LEFT, font_name='Calibri'):
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(font_size)
    p.font.color.rgb = color
    p.font.bold = bold
    p.font.name = font_name
    p.alignment = alignment
    return txBox

def add_bullet_list(slide, left, top, width, height, items, font_size=16, color=DARK_GRAY, spacing=Pt(8)):
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    for i, item in enumerate(items):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.text = item
        p.font.size = Pt(font_size)
        p.font.color.rgb = color
        p.font.name = 'Calibri'
        p.space_after = spacing
        p.level = 0
    return txBox

# SLIDE 1: Title Slide
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_background(slide, DARK_BLUE)
add_shape(slide, Inches(0), Inches(3.2), Inches(13.333), Inches(0.06), GOLD)
add_text_box(slide, Inches(1), Inches(1.5), Inches(11.333), Inches(1.5),
             "Church Registration System", 44, WHITE, True, PP_ALIGN.CENTER)
add_text_box(slide, Inches(1), Inches(3.5), Inches(11.333), Inches(1),
             "Grace of Jesus Christ Ministries – Kitintale, Kampala", 28, LIGHT_BLUE, False, PP_ALIGN.CENTER)
add_text_box(slide, Inches(1), Inches(5), Inches(11.333), Inches(0.8),
             "A Modern Digital Solution for Church Member Management", 20, GOLD, False, PP_ALIGN.CENTER)

# SLIDE 2: About
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_background(slide, WHITE)
add_shape(slide, Inches(0), Inches(0), Inches(13.333), Inches(1.2), DARK_BLUE)
add_text_box(slide, Inches(0.8), Inches(0.25), Inches(11), Inches(0.8),
             "About", 36, WHITE, True)
add_shape(slide, Inches(0.8), Inches(1.6), Inches(0.08), Inches(0.6), GOLD)
add_text_box(slide, Inches(1.2), Inches(1.6), Inches(11), Inches(0.6),
             "Project Overview", 24, DARK_BLUE, True)
items = [
    "• Grace of Jesus Christ Ministries is a prophetic church located in Kitintale, Kampala, Uganda",
    "• The church slogan: \"An encounter with the Holy Spirit\"",
    "• Holds Sunday services, prayer meetings, counseling sessions, and special events",
    "• Experienced rapid growth, making manual registration processes inefficient",
    "• This project digitizes the entire registration and member management workflow",
    "• Built with modern web technologies: HTML5, CSS3, JavaScript, Firebase, and Google Sheets"
]
add_bullet_list(slide, Inches(1.2), Inches(2.4), Inches(10.5), Inches(4.5), items, 18, DARK_GRAY, Pt(12))

# SLIDE 3: Abstract
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_background(slide, WHITE)
add_shape(slide, Inches(0), Inches(0), Inches(13.333), Inches(1.2), DARK_BLUE)
add_text_box(slide, Inches(0.8), Inches(0.25), Inches(11), Inches(0.8),
             "Abstract", 36, WHITE, True)
add_shape(slide, Inches(0.8), Inches(1.6), Inches(0.08), Inches(0.6), GOLD)
add_text_box(slide, Inches(1.2), Inches(1.6), Inches(11), Inches(0.6),
             "Summary", 24, DARK_BLUE, True)
abstract_text = (
    "This project presents a comprehensive Church Registration System designed to replace the "
    "manual, paper-based registration process at Grace of Jesus Christ Ministries. The system "
    "provides a multi-step online registration portal for church visitors and members, coupled "
    "with an administrative dashboard for church leadership to manage member data, track church "
    "growth, and organize events.\n\n"
    "The system leverages Firebase Firestore for real-time data storage, Google Sheets as a "
    "backup database, and includes offline support through localStorage and Service Workers. "
    "Additional features include WhatsApp integration for automated confirmations, media library "
    "management, and church program scheduling."
)
add_text_box(slide, Inches(1.2), Inches(2.5), Inches(10.5), Inches(4),
             abstract_text, 18, DARK_GRAY, False, PP_ALIGN.LEFT)

# SLIDE 4: Existing System
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_background(slide, WHITE)
add_shape(slide, Inches(0), Inches(0), Inches(13.333), Inches(1.2), DARK_BLUE)
add_text_box(slide, Inches(0.8), Inches(0.25), Inches(11), Inches(0.8),
             "Existing System", 36, WHITE, True)
add_shape(slide, Inches(0.8), Inches(1.6), Inches(0.08), Inches(0.6), GOLD)
add_text_box(slide, Inches(1.2), Inches(1.6), Inches(11), Inches(0.6),
             "Current Manual Process", 24, DARK_BLUE, True)
items = [
    "• Paper-based registration books at the church entrance",
    "• Manual data entry into spreadsheets by church administrators",
    "• No centralized database for member information",
    "• Difficult to track attendance, growth trends, or member engagement",
    "• High risk of data loss, duplication, or errors",
    "• No automated communication with registered members",
    "• Time-consuming reporting and data retrieval processes",
    "• Limited accessibility – only available physically at the church"
]
add_bullet_list(slide, Inches(1.2), Inches(2.4), Inches(10.5), Inches(4.5), items, 18, DARK_GRAY, Pt(12))

# SLIDE 5: Proposed System
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_background(slide, WHITE)
add_shape(slide, Inches(0), Inches(0), Inches(13.333), Inches(1.2), DARK_BLUE)
add_text_box(slide, Inches(0.8), Inches(0.25), Inches(11), Inches(0.8),
             "Proposed System", 36, WHITE, True)
add_shape(slide, Inches(0.8), Inches(1.6), Inches(0.08), Inches(0.6), GOLD)
add_text_box(slide, Inches(1.2), Inches(1.6), Inches(11), Inches(0.6),
             "Digital Solution", 24, DARK_BLUE, True)
items = [
    "• Multi-step online registration form accessible via web browsers",
    "• Real-time data storage using Firebase Firestore",
    "• Google Sheets integration as backup database",
    "• Admin dashboard for member management, analytics, and reporting",
    "• Automated WhatsApp confirmation messages after registration",
    "• Offline support with localStorage and Service Worker caching",
    "• Media library for sermons, events, and church photos",
    "• Church program scheduling and event management",
    "• Responsive design for mobile, tablet, and desktop access"
]
add_bullet_list(slide, Inches(1.2), Inches(2.4), Inches(10.5), Inches(4.5), items, 18, DARK_GRAY, Pt(12))

# SLIDE 6: Advantages
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_background(slide, WHITE)
add_shape(slide, Inches(0), Inches(0), Inches(13.333), Inches(1.2), BLUE)
add_text_box(slide, Inches(0.8), Inches(0.25), Inches(11), Inches(0.8),
             "Advantages", 36, WHITE, True)
add_shape(slide, Inches(0.8), Inches(1.6), Inches(0.08), Inches(0.6), GOLD)
items = [
    "• Efficient Data Management – Instant storage, retrieval, and updating of member records",
    "• Accessibility – Register from anywhere with internet access",
    "• Data Security – Encrypted storage with Firebase security rules",
    "• Automated Communication – WhatsApp integration for instant confirmations",
    "• Analytics & Reporting – Real-time statistics on church growth and attendance",
    "• Offline Support – Registrations saved locally and synced when online",
    "• Scalability – System grows with the church without performance issues",
    "• Cost-Effective – Free tier Firebase and Google Sheets reduce hosting costs",
    "• User-Friendly – Intuitive interface requiring minimal training"
]
add_bullet_list(slide, Inches(1.2), Inches(2.4), Inches(10.5), Inches(4.5), items, 18, DARK_GRAY, Pt(12))

# SLIDE 7: Disadvantages
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_background(slide, WHITE)
add_shape(slide, Inches(0), Inches(0), Inches(13.333), Inches(1.2), RGBColor(0xE7, 0x4C, 0x3C))
add_text_box(slide, Inches(0.8), Inches(0.25), Inches(11), Inches(0.8),
             "Disadvantages", 36, WHITE, True)
add_shape(slide, Inches(0.8), Inches(1.6), Inches(0.08), Inches(0.6), GOLD)
items = [
    "• Internet Dependency – Requires internet connection for real-time features",
    "• Learning Curve – Church staff need training to use the admin dashboard",
    "• Third-Party Reliance – Depends on Firebase and Google services availability",
    "• Initial Setup Cost – Requires configuration of Firebase project and Google Sheets API",
    "• Data Migration – Existing paper records need to be digitized manually",
    "• Limited Offline Features – Some features unavailable without internet",
    "• Maintenance – Regular updates and monitoring required for optimal performance"
]
add_bullet_list(slide, Inches(1.2), Inches(2.4), Inches(10.5), Inches(4.5), items, 18, DARK_GRAY, Pt(12))

# SLIDE 8: Software Requirements
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_background(slide, WHITE)
add_shape(slide, Inches(0), Inches(0), Inches(13.333), Inches(1.2), DARK_BLUE)
add_text_box(slide, Inches(0.8), Inches(0.25), Inches(11), Inches(0.8),
             "Software Requirements", 36, WHITE, True)
add_shape(slide, Inches(0.8), Inches(1.6), Inches(0.08), Inches(0.6), GOLD)

# Frontend
add_text_box(slide, Inches(1.2), Inches(2.4), Inches(4.5), Inches(0.5),
             "Frontend", 22, BLUE, True)
frontend_items = [
    "• HTML5, CSS3, JavaScript (ES6+)",
    "• Responsive design with CSS Grid/Flexbox",
    "• FontAwesome icons",
    "• Google Fonts (Montserrat)",
    "• Service Workers for offline support"
]
add_bullet_list(slide, Inches(1.2), Inches(3), Inches(4.5), Inches(3), frontend_items, 16, DARK_GRAY, Pt(8))

# Backend & Database
add_text_box(slide, Inches(7), Inches(2.4), Inches(5), Inches(0.5),
             "Backend & Database", 22, BLUE, True)
backend_items = [
    "• Firebase Firestore (NoSQL database)",
    "• Firebase Authentication (Admin login)",
    "• Firebase Storage (Media files)",
    "• Google Sheets API (Backup storage)",
    "• Google Apps Script (Sheet integration)",
    "• WhatsApp Business API (Messaging)"
]
add_bullet_list(slide, Inches(7), Inches(3), Inches(5), Inches(3), backend_items, 16, DARK_GRAY, Pt(8))

# Development Tools
add_text_box(slide, Inches(1.2), Inches(5.2), Inches(4.5), Inches(0.5),
             "Development Tools", 22, BLUE, True)
tools_items = [
    "• XAMPP (Local server)",
    "• Git & GitHub (Version control)",
    "• VS Code (Code editor)",
    "• Chrome DevTools (Debugging)"
]
add_bullet_list(slide, Inches(1.2), Inches(5.8), Inches(4.5), Inches(2), tools_items, 16, DARK_GRAY, Pt(8))

# SLIDE 9: About Project
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_background(slide, WHITE)
add_shape(slide, Inches(0), Inches(0), Inches(13.333), Inches(1.2), DARK_BLUE)
add_text_box(slide, Inches(0.8), Inches(0.25), Inches(11), Inches(0.8),
             "About Project", 36, WHITE, True)
add_shape(slide, Inches(0.8), Inches(1.6), Inches(0.08), Inches(0.6), GOLD)
items = [
    "• Project Name: Church Registration System",
    "• Organization: Grace of Jesus Christ Ministries",
    "• Location: Kitintale, Kampala, Uganda",
    "• Technology Stack: Firebase, Google Sheets, Vanilla JavaScript",
    "• Development Environment: XAMPP (Local), Firebase Hosting (Production)",
    "• Repository: github.com/jessethegreat6190/Church-Registration",
    "• Key Features: Multi-step registration, admin dashboard, WhatsApp integration, offline sync",
    "• Target Users: Church visitors, members, and administrators",
    "• Status: Fully functional and deployed"
]
add_bullet_list(slide, Inches(1.2), Inches(2.4), Inches(10.5), Inches(4.5), items, 18, DARK_GRAY, Pt(12))

# SLIDE 10: System Architecture
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_background(slide, WHITE)
add_shape(slide, Inches(0), Inches(0), Inches(13.333), Inches(1.2), DARK_BLUE)
add_text_box(slide, Inches(0.8), Inches(0.25), Inches(11), Inches(0.8),
             "System Architecture", 36, WHITE, True)
add_shape(slide, Inches(0.8), Inches(1.6), Inches(0.08), Inches(0.6), GOLD)

# Architecture diagram boxes
boxes = [
    (Inches(0.8), Inches(2.2), Inches(3), Inches(1.2), "User Interface\n(HTML/CSS/JS)", BLUE),
    (Inches(5.2), Inches(2.2), Inches(3), Inches(1.2), "Firebase Services\n(Auth, Firestore, Storage)", RGBColor(0xFF, 0xA7, 0x26)),
    (Inches(9.5), Inches(2.2), Inches(3), Inches(1.2), "Google Sheets\n(Backup Database)", RGBColor(0x0F, 0x9D, 0x58)),
    (Inches(0.8), Inches(4.2), Inches(3), Inches(1.2), "Admin Dashboard\n(Gold Theme)", GOLD),
    (Inches(5.2), Inches(4.2), Inches(3), Inches(1.2), "WhatsApp API\n(Automated Messages)", RGBColor(0x25, 0xD3, 0x66)),
    (Inches(9.5), Inches(4.2), Inches(3), Inches(1.2), "Service Worker\n(Offline Support)", RGBColor(0x9B, 0x59, 0xB6)),
]

for left, top, width, height, text, color in boxes:
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    tf = shape.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(16)
    p.font.color.rgb = WHITE
    p.font.bold = True
    p.alignment = PP_ALIGN.CENTER
    tf.paragraphs[0].space_before = Pt(10)

# Arrows (simplified as lines)
add_text_box(slide, Inches(3.9), Inches(2.6), Inches(1.2), Inches(0.5), "→", 24, DARK_GRAY, True, PP_ALIGN.CENTER)
add_text_box(slide, Inches(8.3), Inches(2.6), Inches(1.2), Inches(0.5), "→", 24, DARK_GRAY, True, PP_ALIGN.CENTER)
add_text_box(slide, Inches(3.9), Inches(4.6), Inches(1.2), Inches(0.5), "→", 24, DARK_GRAY, True, PP_ALIGN.CENTER)
add_text_box(slide, Inches(8.3), Inches(4.6), Inches(1.2), Inches(0.5), "→", 24, DARK_GRAY, True, PP_ALIGN.CENTER)

# SLIDE 11: Conclusion
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_background(slide, WHITE)
add_shape(slide, Inches(0), Inches(0), Inches(13.333), Inches(1.2), DARK_BLUE)
add_text_box(slide, Inches(0.8), Inches(0.25), Inches(11), Inches(0.8),
             "Conclusion", 36, WHITE, True)
add_shape(slide, Inches(0.8), Inches(1.6), Inches(0.08), Inches(0.6), GOLD)
conclusion_text = (
    "The Church Registration System successfully addresses the challenges faced by Grace of Jesus "
    "Christ Ministries in managing member data and church operations. By transitioning from a "
    "manual, paper-based system to a modern digital solution, the church now benefits from:\n\n"
    "• Streamlined registration process accessible online\n"
    "• Centralized, secure database with real-time access\n"
    "• Automated communication through WhatsApp integration\n"
    "• Comprehensive admin dashboard for data management and analytics\n"
    "• Offline support ensuring no data is lost during connectivity issues\n\n"
    "This system positions the church for sustainable growth and improved member engagement while "
    "reducing administrative overhead and minimizing data loss risks."
)
add_text_box(slide, Inches(1.2), Inches(2.4), Inches(10.5), Inches(4.5),
             conclusion_text, 18, DARK_GRAY, False, PP_ALIGN.LEFT)

# SLIDE 12: Future Work
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_background(slide, WHITE)
add_shape(slide, Inches(0), Inches(0), Inches(13.333), Inches(1.2), DARK_BLUE)
add_text_box(slide, Inches(0.8), Inches(0.25), Inches(11), Inches(0.8),
             "Future Work", 36, WHITE, True)
add_shape(slide, Inches(0.8), Inches(1.6), Inches(0.08), Inches(0.6), GOLD)
items = [
    "• Mobile App Development – Native Android/iOS applications for easier access",
    "• SMS Integration – Alternative messaging for users without WhatsApp",
    "• Advanced Analytics – Predictive insights on church growth and attendance patterns",
    "• Online Giving Module – Secure payment gateway for tithes and offerings",
    "• Live Streaming Integration – Embedded YouTube/Facebook live services",
    "• Multi-Language Support – English, Luganda, and other local languages",
    "• Event Ticketing – QR code-based check-in for special church events",
    "• Volunteer Management – Module for tracking and scheduling church volunteers",
    "• AI Chatbot – Automated responses to common visitor inquiries"
]
add_bullet_list(slide, Inches(1.2), Inches(2.4), Inches(10.5), Inches(4.5), items, 18, DARK_GRAY, Pt(12))

# Save
output_path = os.path.join(os.path.dirname(__file__), "Church_Registration_Presentation.pptx")
prs.save(output_path)
print(f"Presentation saved to: {output_path}")
