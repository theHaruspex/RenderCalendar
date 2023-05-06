import calendar
import datetime
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.utils import simpleSplit


from calendar_components.box import Box
from calendar_components.constants import DATE_FONT_SIZE, DAYS_IN_WEEK
from calendar_components.constants import HEADER_BOX_HEIGHT, WEEKDAY_CELL_HEIGHT, FOREGROUND_COLOR
from calendar_components.constants import HEADER_FONT, ROWS_IN_MONTH

from calendar_components.resources.black_history_dates import black_history_moments_dict


calendar.setfirstweekday(calendar.SUNDAY)


class Day(Box):  # Inherit from the Box class

    def __init__(self, month, date, weekday, week_number):
        self._initialize_properties(month, date, weekday, week_number)
        super().__init__(canvas=month.canvas, x=self._cell_x, y=self._cell_y, width=self._cell_width,
                         height=self._cell_height, font=HEADER_FONT)

    def draw(self, **kwargs):
        if self._is_straggler:
            self.y += self.height
            self.height /= 2
        super().draw()
        self.draw_date()
        self.draw_history_event()

    def draw_history_event(self):
        if self.history_event is not None:
            event_text_x, event_text_y = self._event_text_position
            event_font_size = DATE_FONT_SIZE - 2  # Use a smaller font size for the event text
            self.canvas.setFont(self.font, event_font_size)
            self.canvas.setFillColorRGB(*FOREGROUND_COLOR)

            # Calculate the available width for the text
            padding = 5
            text_width = self._cell_width - 2 * padding

            # Split the text to fit within the available width
            wrapped_text = simpleSplit(self.history_event, self.font, event_font_size, text_width)

            # Draw each line of the wrapped text
            for i, line in enumerate(wrapped_text):
                self.canvas.drawString(event_text_x, event_text_y - i * (event_font_size * 1.2), line)

    def draw_date(self):
        text_x, text_y = self._text_position
        self.canvas.setFont(self.font, DATE_FONT_SIZE)
        self.canvas.setFillColorRGB(*FOREGROUND_COLOR)
        self.canvas.drawString(text_x, text_y, str(self.date))

    def _initialize_properties(self, month, date, weekday, week_number):
        self.month = month
        self.date = date
        self.weekday = weekday
        self.week_number = week_number
        self.weeks_in_month = calendar.monthcalendar(month.year, month.month_number)

        try:
            event_date = datetime.date(2023, month.month_number, date)
            self.history_event = black_history_moments_dict.get(event_date)
        except ValueError:
            self.history_event = None

    @property
    def _event_text_position(self):
        font = pdfmetrics.getFont(self.font)
        face = font.face
        string_height = DATE_FONT_SIZE * (face.ascent - face.descent) / 1000
        event_string_height = (DATE_FONT_SIZE - 2) * (face.ascent - face.descent) / 1000
        padding = 5
        event_text_y = self.y + self.height - string_height - event_string_height - 2 * padding
        event_text_x = self.x + padding

        return event_text_x, event_text_y

    @property
    def _cell_x(self):
        return self.month.x + self.weekday * self._cell_width

    @property
    def _cell_y(self):
        return self.month.weekday_cell_y - (self.week_number + 1) * self._cell_height

    @property
    def _cell_width(self):
        return self.month.width / DAYS_IN_WEEK

    @property
    def _cell_height(self):
        remaining_space = self.month.height - HEADER_BOX_HEIGHT - WEEKDAY_CELL_HEIGHT
        return remaining_space / ROWS_IN_MONTH

    @property
    def _text_position(self):
        font = pdfmetrics.getFont(self.font)
        face = font.face
        string_height = DATE_FONT_SIZE * (face.ascent - face.descent) / 1000
        padding = 5
        text_y = self.y + self.height - string_height - padding
        text_x = self.x + padding

        return text_x, text_y

    @property
    def _is_straggler(self):
        if self.week_number == ROWS_IN_MONTH and self.weeks_in_month[self.week_number][self.weekday] != 0:
            return True
        return False
