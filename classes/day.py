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

        self.weeks_in_month = calendar.monthcalendar(
            month.year,
            month.month_number
        )

        width, height = self._cell_dimensions
        x, y = self._cell_position

        super().__init__(
            canvas=month.canvas,
            x=x,
            y=y,
            width=width,
            height=height,
            font=month.HEADER_FONT,
            fg_color=month.FOREGROUND_COLOR
        )

    @property
    def _cell_dimensions(self):
        width = self.month.width / 7
        remaining_space = self.month.height - self.month.HEADER_BOX_HEIGHT - self.month.WEEKDAY_CELL_HEIGHT

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
        font_size = 12
        is_straggler = self._check_straggler()
        if is_straggler:
            self.y += self.height
            self.height /= 2

        # Use the Box draw method to draw the rectangle
        super().draw()

        # Use the Box draw_text method to draw the text inside the cell
        self.draw_text(str(self.day_number), font_size)

    def _check_straggler(self):
        if self.week_number == 5 and self.weeks_in_month[self.week_number][self.weekday] != 0:
            print(self.month.month_name)
            return True

        return False
