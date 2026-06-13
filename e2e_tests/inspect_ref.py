import openpyxl, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
wb = openpyxl.load_workbook(r'c:\Users\thiru\StudioProjects\crowdsense\E2E_Test_Report_PancreaScan_2026-06-09T16-22-48.xlsx')

ws = wb['Summary']
print("=== Summary header styles ===")
for cell in ws[1]:
    fill = cell.fill
    font = cell.font
    fg = fill.fgColor.rgb if fill.fill_type == "solid" else None
    fc = font.color.rgb if font.color and font.color.type == "rgb" else None
    print(f"  {cell.coordinate}: value={cell.value!r}, fill_fg={fg}, font_color={fc}, bold={font.bold}, size={font.size}")

ws2 = wb['Passed Tests']
print("\n=== Passed Tests header styles ===")
for cell in ws2[1]:
    fill = cell.fill
    font = cell.font
    fg = fill.fgColor.rgb if fill.fill_type == "solid" else None
    fc = font.color.rgb if font.color and font.color.type == "rgb" else None
    print(f"  {cell.coordinate}: value={cell.value!r}, fill_fg={fg}, font_color={fc}, bold={font.bold}, size={font.size}")

ws3 = wb['Failed Tests']
print("\n=== Failed Tests header styles ===")
for cell in ws3[1]:
    fill = cell.fill
    font = cell.font
    fg = fill.fgColor.rgb if fill.fill_type == "solid" else None
    fc = font.color.rgb if font.color and font.color.type == "rgb" else None
    print(f"  {cell.coordinate}: value={cell.value!r}, fill_fg={fg}, font_color={fc}, bold={font.bold}, size={font.size}")

# Also check a passed row and failed row colour
print("\n=== Passed row 2 styles ===")
for cell in ws2[2]:
    fill = cell.fill
    fg = fill.fgColor.rgb if fill.fill_type == "solid" else None
    print(f"  {cell.coordinate}: value={cell.value!r}, fill_fg={fg}")

print("\n=== Failed row 2 styles ===")
for cell in ws3[2]:
    fill = cell.fill
    fg = fill.fgColor.rgb if fill.fill_type == "solid" else None
    print(f"  {cell.coordinate}: value={cell.value!r}, fill_fg={fg}")
