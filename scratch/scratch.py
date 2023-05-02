from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table, TableStyle, CellStyle
from datetime import date, timedelta

# Create a stylesheet with default styles
styles = getSampleStyleSheet()

# Create a document with letter page size
doc = SimpleDocTemplate("calendar.pdf", pagesize=letter)

# Get weekdays as a list, starting from Sunday
weekdays = [Paragraph(day, styles['Normal']) for day in ['Su', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa']]

# Create a list of cells with dates for each day of the month
cells = []
today = date.today()
month_start_date = date(today.year, today.month, 1)
month_end_date = date(today.year, today.month+1, 1) if today.month < 12 else date(today.year+1, 1, 1)
delta = month_end_date - month_start_date
for i in range(delta.days):
    day = month_start_date + timedelta(days=i)
    cells.append(Paragraph(str(day.day), styles['Normal']))

# Add empty cells at the beginning of the first row to account for the days of the week
empty_cells = [Paragraph('', styles['Normal']) for i in range(month_start_date.weekday())]
cells = empty_cells + cells

# Add empty cells at the end of the last row to complete the grid
empty_cells = [Paragraph('', styles['Normal']) for i in range(42 - len(cells))]
cells = cells + empty_cells

# Create a table with 6 rows and 7 columns
table_data = [weekdays] + [cells[i:i+7] for i in range(0, 42, 7)]
table = Table(table_data)

# Apply a style to the table
table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.grey),
    ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
    ('BACKGROUND', (0,1), (-1,-1), colors.white),
    ('TEXTCOLOR', (0,1), (-1,-1), colors.black),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTSIZE', (0,0), (-1,0), 14),
    ('BOTTOMPADDING', (0,0), (-1,0), 12),
    ('GRID', (0,0), (-1,-1), 1, colors.black),
]))

# Add the table to the document and save it
doc.build([table])