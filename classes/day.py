import calendar

from classes.box import Box

calendar.setfirstweekday(calendar.SUNDAY)


class Day(Box):  # Inherit from the Box class
    FG_COLOR = (255, 255, 255)

    def __init__(self, month, day_number, weekday, week_number):
        self.month = month
        self.day_number = day_number
        self.weekday = weekday
        self.week_number = week_number

        width, height = self._cell_dimensions
        x, y = self._cell_position

        # Call the superclass constructor
        super().__init__(month.canvas, x, y, width, height, month.HEADER_FONT, month.FOREGROUND_COLOR)

    @property
    def _cell_dimensions(self):
        width = self.month.width / 7
        remaining_space = self.month.height - self.month.HEADER_BOX_HEIGHT - self.month.WEEKDAY_CELL_HEIGHT

        # Default to 5 rows for displaying the days
        required_rows = 5

        height = remaining_space / required_rows
        return width, height

    @property
    def _cell_position(self):
        width, height = self._cell_dimensions
        x = self.month.x + self.weekday * width
        y = self.month.weekday_cell_y - (self.week_number + 1) * height
        return x, y

    def draw(self, **kwargs):

        # Use the Box draw_text method to draw the text inside the cell
        font_size = 12
        is_straggler = self._check_straggler()
        if is_straggler:
            # Adjust the text_y position to draw the straggler day below the main day
            self.y -= self.height / 2

        # Use the Box draw method to draw the rectangle
        super().draw()

        self.draw_text(str(self.day_number), font_size)

    def _required_rows(self):
        year = 2012  # Change this to the desired year
        weeks_in_month = calendar.monthcalendar(year, self.month.month_number)
        # Check if the last week contains days from the next month and adjust the number of rows accordingly
        extra_row = 1 if weeks_in_month[-1][0] != 0 else 0
        return len(weeks_in_month) + extra_row

    def _check_straggler(self):
        year = 2023  # Change this to the desired year
        weeks_in_month = calendar.monthcalendar(year, self.month.month_number)

        if self.week_number == 4 and weeks_in_month[-1][self.weekday] == 0:
            print(self.month.month_name)
            return True
        return False
