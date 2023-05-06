from calendar_components.box import Box, Header
import calendar

from calendar_components.day import Day
from calendar_components.constants import HEADER_BOX_HEIGHT, HEADER_FONT, WEEKDAY_CELL_HEIGHT
from calendar_components.constants import MONTHS, YEAR, DOCUMENT_PADDING


class Month:

    def __init__(self, my_calendar, month_name):
        self.month_name = month_name
        self.month_number = MONTHS.index(month_name) + 1

        self.year = YEAR

        self.width = my_calendar.page_width - (2 * DOCUMENT_PADDING)
        self.height = my_calendar.page_height - (2 * DOCUMENT_PADDING)

        self.x = DOCUMENT_PADDING
        self.y = DOCUMENT_PADDING

        self.canvas = my_calendar.pdf_canvas

        self.header_box_y = self.y + self.height - HEADER_BOX_HEIGHT

    def draw(self):
        self._draw_main_box()
        self._draw_header()
        self._draw_weekday_cells()
        self._draw_days()

    def _draw_main_box(self):
        main_box = Box(canvas=self.canvas, x=self.x, y=self.y, width=self.width, height=self.height,
                       font=HEADER_FONT)
        main_box.draw()

    def _draw_header(self):
        header = Header(
            canvas=self.canvas,
            x=self.x,
            y=self.header_box_y,
            width=self.width,
            height=HEADER_BOX_HEIGHT,
            font=HEADER_FONT,
        )
        header.draw(text=self.month_name, font_size=55)

    def _draw_weekday_cells(self):
        cell_width = self.width / 7
        weekdays = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']

        for i in range(7):
            cell_x = self.x + i * cell_width
            self.weekday_cell_y = self.header_box_y - WEEKDAY_CELL_HEIGHT
            cell = Box(canvas=self.canvas, x=cell_x, y=self.weekday_cell_y, width=cell_width,
                       height=WEEKDAY_CELL_HEIGHT, font=HEADER_FONT)
            cell.draw(text=weekdays[i], font_size=12)

    def _draw_days(self):
        [day.draw() for day in self.get_days()]

    def get_days(self):
        weeks_in_month = calendar.monthcalendar(self.year, self.month_number)

        for week_num, week in enumerate(weeks_in_month):
            for weekday, date in enumerate(week):
                if date == 0:
                    continue  # day is not part of this month
                yield Day(self, date, weekday, week_num)
