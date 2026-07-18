"""
html_preview.py

Displays generated HTML inside Streamlit.
"""

from pathlib import Path
import streamlit.components.v1 as components


class HTMLPreview:

    @staticmethod
    def preview_html(html_code, height=700):

        components.html(
            html_code,
            height=height,
            scrolling=True
        )

    @staticmethod
    def preview_file(file_path, height=700):

        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"{file_path} not found.")

        html = file_path.read_text(
            encoding="utf-8"
        )

        components.html(
            html,
            height=height,
            scrolling=True
        )

    @staticmethod
    def save_html(html_code, output_path):

        output_path = Path(output_path)

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        output_path.write_text(
            html_code,
            encoding="utf-8"
        )

        return str(output_path)

    @staticmethod
    def save_and_preview(
        html_code,
        output_path="generated/index.html",
        height=700
    ):

        HTMLPreview.save_html(
            html_code,
            output_path
        )

        HTMLPreview.preview_html(
            html_code,
            height
        )

        return output_path