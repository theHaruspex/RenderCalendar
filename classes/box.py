from reportlab.pdfbase import pdfmetrics


class Box:
    def __init__(self, canvas, x, y, width, height, font=None, fg_color=None):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font = font
        self.fg_color = fg_color

    def draw(self, text=None, font_size=None):
        self.canvas.setStrokeColorRGB(*self.fg_color)
        self.canvas.rect(self.x, self.y, self.width, self.height)

        if text and font_size:
            self.draw_text(text, font_size)

    def draw_text(self, text, font_size):
        text_x = self.x + self.width / 2
        text_y = self.y + self.height / 2

        self.canvas.setFont(self.font, font_size)
        self.canvas.setFillColorRGB(*self.fg_color)
        self.canvas.drawCentredString(text_x, text_y, text)


class Header(Box):
    def draw_text(self, text, font_size):
        # Get font face and calculate string height
        font = pdfmetrics.getFont(self.font)
        face = font.face
        string_height = font_size * (face.ascent - face.descent) / 1000

        # Calculate center position of header box
        header_center_y = self.y + self.height / 2
        header_center_x = self.x + self.width / 2

        # Calculate position of text
        text_y = header_center_y - string_height / 2
        text_x = header_center_x

        # Draw text with centered alignment
        self.canvas.setFont(self.font, font_size)
        self.canvas.setFillColorRGB(*self.fg_color)
        self.canvas.drawCentredString(text_x, text_y, text)