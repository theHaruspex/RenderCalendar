from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, A4

from classes.month import Month


class Calendar:
    BACKGROUND_COLOR = (0, 0, 0)
    PADDING = 30
    MONTHS = ['JANUARY', 'FEBRUARY', 'MARCH', 'APRIL', 'MAY', 'JUNE', 'JULY', 'AUGUST', 'SEPTEMBER', 'OCTOBER',
              'NOVEMBER', 'DECEMBER']

    def __init__(self, filename='calendar.pdf'):
        self.filename = filename
        self._create_canvas()
        self._check_padding()

    def _create_canvas(self):
        self.page_width, self.page_height = landscape(A4)
        self.pdf_canvas = canvas.Canvas(self.filename, pagesize=(self.page_width, self.page_height))
        self._draw_background()

    def _check_padding(self):
        if self.PADDING >= min(self.page_width, self.page_height) / 2:
            raise ValueError('Padding value is too large')


    def generate(self):
        for month in self.MONTHS:
            self.add_month(month)

            if month != self.MONTHS[-1]:
                self.add_new_page()

        self.save()

    def add_month(self, month_name):
        """Add a month to the calendar with the specified name."""
        month = Month(self, month_name)
        month.draw()

    def add_new_page(self):
        """Add a new page to the calendar."""
        self.pdf_canvas.showPage()
        self._draw_background()

    def save(self):
        """Save the calendar to a PDF file."""
        self.pdf_canvas.save()

    def _draw_background(self):
        """Draw the background of the calendar."""
        self.pdf_canvas.rect(0, 0, self.page_width, self.page_height, fill=1)
        self.pdf_canvas.setFillColorRGB(*self.BACKGROUND_COLOR)