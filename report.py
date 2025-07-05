# report.py
from fpdf import FPDF
import os
import arabic_reshaper
from bidi.algorithm import get_display

class ReportBuilder:
    def __init__(self, output_path="report.pdf"):
        self.pdf = FPDF()
        self.pdf.set_auto_page_break(auto=True, margin=15)
        self.output_path = output_path
        self._add_unicode_support()

    def _add_unicode_support(self):
        font_path = "DejaVuSans.ttf"
        if not os.path.exists(font_path):
            raise FileNotFoundError("DejaVuSans.ttf is required for Arabic and Unicode support.")
        self.pdf.add_font("DejaVu", "", font_path, uni=True)
        self.pdf.set_font("DejaVu", size=12)

    def _process_arabic(self, text):
        try:
            reshaped = arabic_reshaper.reshape(text)
            return get_display(reshaped)
        except:
            return text  # fallback

    def add_title(self, title):
        self.pdf.add_page()
        self.pdf.set_font("DejaVu", "", 16)
        title = self._process_arabic(title)
        self.pdf.cell(0, 10, title, ln=True, align="C")
        self.pdf.ln(10)

    def add_section(self, title, body):
        self.pdf.set_font("DejaVu", "", 14)
        title = self._process_arabic(title)
        self.pdf.cell(0, 10, title, ln=True)
        self.pdf.set_font("DejaVu", "", 12)
        body = self._process_arabic(body)
        self.pdf.multi_cell(0, 10, body)
        self.pdf.ln(5)

    def add_plot(self, image_path, caption):
        if os.path.exists(image_path):
            self.pdf.image(image_path, w=160)
            self.pdf.set_font("DejaVu", "", 11)
            caption = self._process_arabic(caption)
            self.pdf.multi_cell(0, 8, caption)
            self.pdf.ln(5)

    def save(self):
        self.pdf.output(self.output_path)
