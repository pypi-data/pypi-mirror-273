import tkinter as tk
import tkinter.font as tkFont

root = tk.Tk()

# 获取系统中所有的字体
all_fonts = tkFont.families()

for font in all_fonts:
    print(font)

root.mainloop()
