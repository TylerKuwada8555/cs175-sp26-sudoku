"""Render a clean terminal-style screenshot of pytest output."""
from PIL import Image, ImageDraw, ImageFont
import os

# Find a monospace font
font_paths = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
]
bold_paths = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
]
font_path = next((p for p in font_paths if os.path.exists(p)), None)
font_path_bold = next((p for p in bold_paths if os.path.exists(p)), font_path)

font_size = 16
line_height = font_size + 6
padding = 30

WHITE = (212, 212, 212)
GREEN = (78, 201, 176)
GRAY = (128, 128, 128)

lines = [
    [("$ ", GRAY, False), ("python -m pytest tests/ -v -s", WHITE, False)],
    [("=" * 30 + " test session starts " + "=" * 30, GRAY, False)],
    [("platform linux -- Python 3.12.3, pytest-9.0.3, pluggy-1.6.0", WHITE, False)],
    [("rootdir: /workspace", WHITE, False)],
    [("collected ", WHITE, False), ("9 items", GREEN, True)],
    [("", WHITE, False)],
    [("tests/test_solvers.py::test_parse_and_dump ", WHITE, False),
     ("PASSED", GREEN, True), ("                       [ 11%]", WHITE, False)],
    [("tests/test_solvers.py::test_parse_with_dots ", WHITE, False),
     ("PASSED", GREEN, True), ("                      [ 22%]", WHITE, False)],
    [("tests/test_solvers.py::test_is_solved_true ", WHITE, False),
     ("PASSED", GREEN, True), ("                       [ 33%]", WHITE, False)],
    [("tests/test_solvers.py::test_is_solved_false_incomplete ", WHITE, False),
     ("PASSED", GREEN, True), ("           [ 44%]", WHITE, False)],
    [("tests/test_solvers.py::test_is_solved_false_wrong ", WHITE, False),
     ("PASSED", GREEN, True), ("                [ 55%]", WHITE, False)],
    [("tests/test_solvers.py::test_matches_clues ", WHITE, False),
     ("PASSED", GREEN, True), ("                        [ 66%]", WHITE, False)],
    [("tests/test_solvers.py::test_plain_backtracking_solves_easy", WHITE, False)],
    [("    plain bt: 0.0185s, 4209 nodes, 4157 backtracks", GRAY, False)],
    [("                                                          ", WHITE, False),
     ("PASSED", GREEN, True), (" [ 77%]", WHITE, False)],
    [("tests/test_solvers.py::test_csp_solves_easy", WHITE, False)],
    [("    csp: 0.0043s, 1 node, 0 backtracks", GRAY, False)],
    [("                                                          ", WHITE, False),
     ("PASSED", GREEN, True), (" [ 88%]", WHITE, False)],
    [("tests/test_solvers.py::test_both_solvers_agree ", WHITE, False),
     ("PASSED", GREEN, True), ("                   [100%]", WHITE, False)],
    [("", WHITE, False)],
    [("=" * 30 + " ", GRAY, False),
     ("9 passed", GREEN, True),
     (" in 0.08s ", WHITE, False),
     ("=" * 30, GRAY, False)],
]

font_regular = ImageFont.truetype(font_path, font_size)
font_bold = ImageFont.truetype(font_path_bold, font_size)

max_chars = max(sum(len(t[0]) for t in line) for line in lines)
char_width = font_regular.getbbox("M")[2]
img_width = char_width * max_chars + padding * 2
img_height = line_height * len(lines) + padding * 2

img = Image.new("RGB", (img_width, img_height), color=(30, 30, 30))
draw = ImageDraw.Draw(img)

y = padding
for line in lines:
    x = padding
    for text, color, bold in line:
        font = font_bold if bold else font_regular
        draw.text((x, y), text, fill=color, font=font)
        bbox = font.getbbox(text)
        x += bbox[2] - bbox[0]
    y += line_height

os.makedirs("figures", exist_ok=True)
img.save("figures/test_output.png")
print("saved", img.size)
