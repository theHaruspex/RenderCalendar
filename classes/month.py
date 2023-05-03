from classes.box import Box, Header
import calendar

from classes.day import Day


class Month:
    FOREGROUND_COLOR = 255, 255, 255
    HEADER_FONT = "Helvetica-Bold"
    WEEKDAY_CELL_HEIGHT = 30
    HEADER_BOX_HEIGHT = 75

    def __init__(self, _calendar, month_name):
        self.month_name = month_name
        self.month_number = _calendar.MONTHS.index(month_name) + 1

        self.year = _calendar.YEAR

        self.width = _calendar.page_width - (2 * _calendar.PADDING)
        self.height = _calendar.page_height - (2 * _calendar.PADDING)

        self.x = _calendar.PADDING
        self.y = _calendar.PADDING

        self.canvas = _calendar.pdf_canvas

        self.header_box_y = self.y + self.height - self.HEADER_BOX_HEIGHT

    def draw(self):
        self._draw_main_box()
        self._draw_header()
        self._draw_weekday_cells()
        self._draw_days()

    def _draw_main_box(self):
        main_box = Box(
            canvas=self.canvas,
            x=self.x,
            y=self.y,
            width=self.width,
            height=self.height,
            font=self.HEADER_FONT,
            fg_color=self.FOREGROUND_COLOR
        )
        main_box.draw()

    def _draw_header(self):
        header = Header(
            canvas=self.canvas,
            x=self.x,
            y=self.header_box_y,
            width=self.width,
            height=self.HEADER_BOX_HEIGHT,
            font=self.HEADER_FONT,
            fg_color=self.FOREGROUND_COLOR
        )
        header.draw(text=self.month_name, font_size=55)

    def _draw_weekday_cells(self):
        cell_width = self.width / 7
        weekdays = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']

        for i in range(7):
            cell_x = self.x + i * cell_width
            self.weekday_cell_y = self.header_box_y - self.WEEKDAY_CELL_HEIGHT
            cell = Box(
                canvas=self.canvas,
                x=cell_x,
                y=self.weekday_cell_y,
                width=cell_width,
                height=self.WEEKDAY_CELL_HEIGHT,
                font=self.HEADER_FONT,
                fg_color=self.FOREGROUND_COLOR
            )
            cell.draw(text=weekdays[i], font_size=12)

    def _draw_days(self):
        [day.draw() for day in self.get_days()]

    def get_days(self):
        weeks_in_month = calendar.monthcalendar(self.year, self.month_number)

        for week_num, week in enumerate(weeks_in_month):
            for weekday, day_number in enumerate(week):
                if day_number == 0:
                    continue  # day is not part of this month
                yield Day(self, day_number, weekday, week_num)
