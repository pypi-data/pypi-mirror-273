import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageFilter
import os
import random
import time
from get_data.get_data import get_ranking, ok_user_id, register_user, get_random_jpg
import pygame
import io
import sys



#打包指令:
#pyinstaller --icon=icon.ico --add-data="C:\Users\eric2\Desktop\git_repos\PLAY\get_data.py:." --add-data="start.png:." --add-data="sign_up.jpg:." --add-data="topic_menu.jpg:." --add-data="anime_menu.jpg:." --add-data="kpop_menu.jpg:." --add-data="anime_bg.jpg:." --add-data="anime_bg2.jpg:." --add-data="anime_bg3.jpg:." --add-data="anime_result.jpg:." --add-data="anime_result2.jpg:." --add-data="anime_result3.jpg:." --add-data="anime_result4.jpg:." --add-data="anime_result5.jpg:." --add-data="kpop_bg.jpg:." --add-data="kpop_result.jpg:." --add-data="kpop_result2.jpg:." --add-data="database.yml:." --add-data="Better Day.mp3:." --add-data="Ethereal Vistas.mp3:." --add-data="Host.mp3:." --add-data="Mellow Future Bass.mp3:." --add-data="Midnight Forest.mp3:." --add-data="Movement.mp3:." --add-data="Sad Soul.mp3:." --add-data="Separation.mp3:." C:\Users\eric2\Desktop\git_repos\PLAY\main.py -F -w


names = []
backgrounds = []
result_bgs = []

animes = ['蠟筆小新', '鏈鋸人', '藍色監獄', '獵人', '實力至上', '間諜家家酒', '棍勇',
          '鬼滅之刃', '海賊王', '果青', '咒術迴戰', '我英', '死神', '死亡筆記本',
          '火影', '刀劍神域']
kpops = ['TWICE', 'TRI.BE', 'STAYC', 'solo', 'Red Velvet', 'NMIXX', 'NewJeans',
         'MAMAMOO', 'LE SSERAFIM', 'KISS OF LIFE', 'IVE ITZY', 'fromis_9',
         'BLACKPINK', 'Billlie', 'aespa', '(G)I-DLE']
checkbox_vars = []
musics = []
# 建立等級串列
levelList = ['Very easy', 'Easy','Normal','Hard']
# 建立題數串列
totalList = ['5', '10', '20', '30', '40', '50', '100']
bg_width = 1550
bg_height = 870
img_width = 450
img_height = 450
correct_count = 0
style_fg = '#4D0000'
style_bg = '#9D9D9D'
root = None
entry = None
ok_correct = None
img = None
tk_img = None
bg_tk_img = None
canvas = None
incorrect_label = None
anime = None
answer = None
bg = None
title = None
title_text = None
confirm_btn = None
leave_btn = None
next_btn = None
question_num_text = None
answer_text = None
user_entry = None
now_time = None
sign_up_title = None
sign_up_rec = None
sign_up_id = None
sign_up_pw = None
sign_up_pw2 = None
after_id = None
selected_topic = None
anime_word = None
kpop_word = None
counter = 0
turn = 0
back_count = 0
music_index = 0
user_id = ""
now_music = ""
paused = False
text_color = 'white'
topic_color = 'white'

# 初始化pygame
pygame.init()
pygame.mixer.init()

"""打包相關"""
# 將所需檔案新增至此Python檔案
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

"""圖片處理"""
# 模糊化處理
def blurry(img, mosaic_level):
    img = img.filter(ImageFilter.BoxBlur(mosaic_level))  # 套用基本模糊化 建議:36
    return img

# 馬賽克處理
def mosaic(img, level):
    w,h = img.size                                      # 讀取圖片長寬
    img2 = img.resize((int(w/level),int(h/level)))      # 縮小圖片
    img2 = img2.resize((w,h), resample = Image.NEAREST) # 放大圖片為原始大小
    return img2

# 抓取圖片名稱
def get_jpg_names() -> None:
    global backgrounds, result_bgs
    try:
        # 當前資料夾
        current_dir = os.getcwd()

        backgrounds = []
        result_bgs = []
        # 根據選擇的主題更換背景
        if selected_topic == 'anime':
            backgrounds = [resource_path('anime_bg.jpg'), resource_path('anime_bg2.jpg'), resource_path('anime_bg3.jpg')]
            result_bgs = [resource_path('anime_result.jpg'), resource_path('anime_result2.jpg'), resource_path('anime_result3.jpg'),
                           resource_path('anime_result4.jpg'), resource_path('anime_result5.jpg')]
        elif selected_topic == 'kpop':
            backgrounds = [resource_path('kpop_bg.jpg')]
            result_bgs = [resource_path('kpop_result.jpg'), resource_path('kpop_result2.jpg')]
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        # 強制離開遊戲
        leave()


"""音樂相關設定"""
# 音樂設定
def music_setting() -> None:
    global musics
    musics = [resource_path('Better Day.mp3'), resource_path('Ethereal Vistas.mp3'), resource_path('Host.mp3'), 
              resource_path('Mellow Future Bass.mp3'), resource_path('Midnight Forest.mp3'), resource_path('Movement.mp3'), 
              resource_path('Sad Soul.mp3'), resource_path('Separation.mp3')]
    # 隨機音樂順序
    random.shuffle(musics)

# 播放音樂
def play_music() -> None:
    global paused, music_index, now_music
    paused = False
    
    if music_index == len(musics):
        music_index = 0
    # 選取當前歌曲、下一首歌曲
    music = musics[music_index]
    now_music = os.path.basename(music[:-4])
    canvas.itemconfig(music_text, text=f"Now Playing: {now_music}")
    pygame.mixer.music.load(music)
    pygame.mixer.music.play(fade_ms=2000)
    music_index += 1

# 播放完畢後播放下一首
def next_song() -> None:
    if (not pygame.mixer.music.get_busy()) and (not paused):
        play_music()
    root.after(100, next_song)

# 放music物件
def canvas_music() -> None:
    global music_text
    # 放入音樂名稱text

    music_text  = canvas.create_text(bg_width-250, 
                                    bg_height-90,
                                    text = f"Now Playing: {now_music}",
                                    font=('Jokerman', 18, 'bold'),
                                    fill='#00FFFF')
    play_pause_btn = tk.Button(root, 
                               text='PLAY/STOP', 
                               font=('Jokerman', 12, 'bold'), 
                               relief='solid', 
                               bd=2, 
                               fg=style_fg,
                               bg=style_bg, 
                               command=play_pause)
    next_song_btn = tk.Button(root, 
                               text='NEXT SONG', 
                               font=('Jokerman', 12, 'bold'), 
                               relief='solid', 
                               bd=2, 
                               fg=style_fg,
                               bg=style_bg, 
                               command=play_music)

    canvas.create_window(bg_width-320, bg_height-30, window=play_pause_btn)
    canvas.create_window(bg_width-170, bg_height-30, window=next_song_btn)

# 暫停、播放
def play_pause() -> None:
    global paused

    paused = not paused

    if paused:
        pygame.mixer.music.pause()
    else:
        pygame.mixer.music.unpause()


"""在主選單內執行"""
# 設定顏色
anime_title_colors = ['#FF44AA', '#FF3333', '#FF7744', '#FFAA33', '#FFCC22', '#FFFF33', 
                    '#CCFF33', '#99FF33', '#33FF33', '#33FFAA', '#33FFDD', '#33FFFF',
                    '#33CCFF', '#5599FF', '#5555FF', '#7744FF', '#9955FF', '#B94FFF',
                    '#E93EFF', '#FF3EFF']
kpop_title_colors = ['#A20055', '#AA0000', '#C63300', '#CC6600', '#AA7700', '#BBBB00',
                    '#88AA00', '#55AA00', '#00AA00', '#00AA55', '#00AA88', '#00AAAA',
                    '#0088A8', '#003C9D', '#0000AA', '#2200AA', '#4400B3', '#66009D', 
                    '#7A0099', '#990099']
color = 0
anime_word = 0
kpop_word = 0
# 顏色循環
def run_color() -> None:
    global color, anime_word, kpop_word, after_id
    if selected_topic == 'anime':
        title_colors = anime_title_colors
        if color  == len(title_colors):
            color = 0
        if anime_word == len(title_text):
            anime_word = 0
        # 更改標題顏色
        canvas.itemconfig(title_text[anime_word], fill=title_colors[color]) if title_text else None
        color += 1
        anime_word += 1
        after_id = root.after(150, run_color)
    elif selected_topic == 'kpop':
        title_colors = kpop_title_colors
        if color  == len(title_colors):
            color = 0
        if kpop_word == len(title_text):
            kpop_word = 0
        # 更改標題顏色
        canvas.itemconfig(title_text[kpop_word], fill=title_colors[color]) if title_text else None
        color += 1
        kpop_word += 1
        after_id = root.after(150, run_color)


    

# 執行全部checkbox取消
def cancel_all() -> None:
    # 全部取消
    for checkbox_var in checkbox_vars:
        checkbox_var.set(False)

# 執行全部checkbox選取
def select_all() -> None:
    # 全部選取
    for checkbox_var in checkbox_vars:
        checkbox_var.set(True)

# 切換使用者
def switch_user() -> None:
    set_user_name.set('')
    user_entry.config(state=tk.NORMAL)
    set_password.set('')
    password_entry.config(state=tk.NORMAL)

"""結束遊戲"""
# 關閉視窗
def leave() -> None:
    pygame.mixer.music.stop()
    root.destroy()

"""一直在背景執行""" 
# 印出時間
def print_time() -> None:
    t = time.time()
    #print(time.ctime(t))
    
    canvas.itemconfig(now_time, text=f"NOW:{time.ctime(t)}")
    root.after(1000, print_time)

"""程式主體"""
# 開啟tkinter介面
def tkinter() -> None:
    global root
    
    # 建立tkinter介面
    root = tk.Tk()
    root.title('Anime_Guess')
    root.iconbitmap('icon.ico')
    root.geometry(f'{bg_width}x{bg_height}+100+0')
    # 禁用視窗縮放功能
    root.resizable(False, False)
    try:
        # 建立主題選擇
        topic_menu()
        # 建立主選單背景
        #main_menu()
        # 播放音樂
        music_setting()
        play_music()
        # 播放完後接下一首
        next_song()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

    root.mainloop()

# 主題選擇
def topic_menu() -> None:
    global canvas, topic_menu_tk_img, now_time, text_color
    canvas.delete('all') if canvas else None
    # 假設after_id還在進行，取消它
    if after_id:
        root.after_cancel(after_id)

    # 放入主選單背景圖片
    topic_menu_img = Image.open(resource_path('topic_menu.jpg'))
    topic_menu_img = topic_menu_img.resize((bg_width, bg_height))
    topic_menu_tk_img = ImageTk.PhotoImage(topic_menu_img)
    canvas = tk.Canvas(root, width=bg_width, height=bg_height)
    canvas.create_image(0, 0, anchor='nw', image=topic_menu_tk_img)   # 在 Canvas 中放入圖片
    canvas.place(x=0, y=0)
    # 建立標題
    canvas.create_text(bg_width/2,120,font=('Jokerman', 45, 'bold'), text="Choose a topic", fill="black")
    # 建立Anime按鈕
    topic_btn1 = tk.Button(root, 
                                text='Anime', 
                                font=('Jokerman', 30, 'bold'), 
                                relief='solid', 
                                bd=2, 
                                fg=style_fg,
                                bg=style_bg,
                                command=topic_anime_to_main)
    canvas.create_window(bg_width/2-100, bg_height/2-200, window=topic_btn1)

    # 建立K-pop按鈕
    topic_btn2 = tk.Button(root, 
                                text='K-pop', 
                                font=('Jokerman', 30, 'bold'), 
                                relief='solid', 
                                bd=2, 
                                fg=style_fg,
                                bg=style_bg,
                                command=topic_kpop_to_main)
    
    canvas.create_window(bg_width/2+100, bg_height/2-200, window=topic_btn2)

    # 放入現在時間
    now_time = canvas.create_text(250, bg_height-50, 
                               text='', 
                               font=('Jokerman', 20, 'bold'), 
                               fill=topic_color)
    print_time()
    text_color = 'white'
    # 音樂物件
    canvas_music()

# 依據主題到主選單
def topic_anime_to_main() -> None:
    global selected_topic
    selected_topic = 'anime'
    # 刪除canvas所有物件
    canvas.delete('all') if canvas else None
    main_menu()
def topic_kpop_to_main() -> None:
    global selected_topic
    selected_topic = 'kpop'
    # 刪除canvas所有物件
    canvas.delete('all') if canvas else None
    main_menu()

# 主選單
def main_menu() -> None:
    global canvas, menu_tk_img, menu, title_text, level_value, total_value, start_tk_img, check_btn, checkbox_vars, user_entry, password_entry
    global now_time, set_user_name, set_password
    global text_color

    # 取得所有jpg的名稱

    get_jpg_names()
    
    if selected_topic == 'anime':
        # 放入主選單背景圖片
        menu_img = Image.open(resource_path('anime_menu.jpg'))
        title = 'Anime Challenge'
        title_text_left = 400
        text_color = 'white'
        name_text = 'Animes'
        checkbox = animes
        checkbox_left = 200
    elif selected_topic == 'kpop':
        # 放入主選單背景圖片
        menu_img = Image.open(resource_path('kpop_menu.jpg'))
        title = 'K-pop(Girls) Challenge'
        title_text_left = 270
        text_color = 'black'
        name_text = 'Groups'
        checkbox = kpops
        checkbox_left = 120
    

    
    
    menu_img = menu_img.resize((bg_width, bg_height))
    menu_tk_img = ImageTk.PhotoImage(menu_img)
    canvas = tk.Canvas(root, width=bg_width, height=bg_height)
    menu = canvas.create_image(0, 0, anchor='nw', image=menu_tk_img)   # 在 Canvas 中放入圖片
    canvas.place(x=0, y=0)
    # 放入標題text
    title_text = []
    
    for index, j in enumerate(title):
        word = canvas.create_text(title_text_left+50*index,70,font=('Jokerman', 45, 'bold'), text=j,anchor='nw')
        title_text.append(word)
    # 顏色循環
    run_color()

    # 已登入過後
    if back_count != 0:
        # 放入切換使用者鍵
        switch_user_btn = tk.Button(root, 
                            text='Switch User', 
                            font=('Jokerman', 12, 'bold'), 
                            relief='solid', 
                            bd=2, 
                            fg=style_fg,
                            bg=style_bg,
                            command=switch_user)
        switch_user_window = canvas.create_window(bg_width/2, 750, window=switch_user_btn)

    # 放入start鍵
    start_img = Image.open(resource_path('start.png'))
    start_img = start_img.resize((200, 200))
    start_tk_img = ImageTk.PhotoImage(start_img)
    start_btn = canvas.create_image(bg_width/2, 810, image=start_tk_img)
    canvas.tag_bind(start_btn, "<Button-1>", play) # -1:左鍵,-2:中鍵,-3:右鍵
    # 放入"User Name"text
    canvas.create_text(bg_width/2-110, 650, 
                               text='User Name:', 
                               font=('Jokerman', 30, 'bold'), 
                               fill=text_color)
    # 放入單行名字輸入框
    set_user_name = tk.StringVar()
    user_entry = tk.Entry(root, font=('Arial', 18), width=12,justify='center', textvariable=set_user_name)
    user_window = canvas.create_window(bg_width/2+100, 650,window=user_entry)

    # 放入"Password:"text
    canvas.create_text(bg_width/2-100, 700, 
                               text='Password:', 
                               font=('Jokerman', 30, 'bold'), 
                               fill=text_color)
    # 放入單行密碼輸入框
    set_password = tk.StringVar()
    password_entry = tk.Entry(root, font=('Arial', 18), width=12,justify='center', textvariable=set_password, show='*')
    password_window = canvas.create_window(bg_width/2+100, 700,window=password_entry)
    
    # 有返回Menu過
    if back_count != 0:
        set_user_name.set(user_id)
        user_entry.config(state=tk.DISABLED)
        set_password.set(user_pw)
        password_entry.config(state=tk.DISABLED)

    # 放入exit鍵
    exit_btn = tk.Button(root, 
                         text='Exit', 
                         font=('Jokerman', 14, 'bold'), 
                         fg='green',
                         bg=style_bg,
                         command=leave)
    exit_window = canvas.create_window(60, 50, window=exit_btn)

    # 放入switch topic鍵
    switch_topic_btn = tk.Button(root, 
                         text='Switch topic', 
                         font=('Jokerman', 14, 'bold'),  
                         fg=style_fg,
                         bg=style_bg,
                         command=topic_menu)
    exit_window = canvas.create_window(20, 100, window=switch_topic_btn, anchor='nw')

    # 放入sign up鍵
    sign_up_btn = tk.Button(root, 
                   text='Sign Up', 
                   font=('Jokerman', 14, 'bold'), 
                   fg=style_fg,
                   bg=style_bg,
                   command=sign_up)
    sign_up_window = canvas.create_window(bg_width-100, 50, window=sign_up_btn)
    # 放入選擇難易度text
    canvas.create_text(bg_width/2, 190, 
                               text='Challenge Level', 
                               font=('Jokerman', 20, 'bold'), 
                               fill='black')
    # 放入難易度選單
    level_value = tk.StringVar()
    level_value.set(levelList[1])
    level_menu = tk.OptionMenu(root, level_value, *levelList)  
    # 設定樣式
    level_menu.config(width=8, 
                      font=('Jokerman',15,'bold'),
                      fg=style_fg, 
                      bg=style_bg)
    
    # 放入選擇總題數text
    canvas.create_text(bg_width/2, 280, 
                               text='Total Rounds', 
                               font=('Jokerman', 20, 'bold'), 
                               fill='black')
    # 放入題數選單
    total_value = tk.StringVar()
    total_value.set(totalList[0])
    total_menu = tk.OptionMenu(root, total_value, *totalList)    
    # 設定樣式
    total_menu.config(width=2,
                      font=('Jokerman',15,'bold'),
                      fg=style_fg, 
                      bg=style_bg,)
    
    # 放入選擇text
    canvas.create_text(bg_width/2, 370, 
                               text=f'{name_text}(At least select five)', 
                               font=('Jokerman', 20, 'bold'), 
                               fill='black')
    # 放入多選按鈕
    checkbox_vars = []
    if selected_topic == 'anime':
        width = 105
    elif selected_topic == 'kpop':
        width = 130

    # 定義每行的按鈕數量和按鈕之間的間距
    buttons_per_row = 8
    button_spacing_x = 30
    button_spacing_y = 40
    for i, name in enumerate(checkbox):
        # 控制每行的高度
        row = i // buttons_per_row
        col = i % buttons_per_row

        x = checkbox_left + width * (col + 1) + button_spacing_x * col
        y = 470 + button_spacing_y * row

        var = tk.BooleanVar(value=True) 
        checkbox_vars.append(var)
        check_btn = tk.Checkbutton(root, 
                                   text=name, 
                                   font=('Jokerman', 12, 'bold'), 
                                   relief='solid', 
                                   bd=2, 
                                   fg=style_fg,
                                   bg=style_bg,
                                   variable=var)

        #check_btn_window = canvas.create_window(280+width*(i%8+1), 470+h, window=check_btn)
        check_btn_window = canvas.create_window(x, y, window=check_btn)
    # 放入全部取消按鈕
    select_all_btn = tk.Button(root, 
                               text='全部選擇', 
                               font=('Jokerman', 12, 'bold'), 
                               relief='solid', 
                               bd=2, 
                               fg=style_fg,
                               bg=style_bg,
                               command=select_all)
    select_all_window = canvas.create_window(bg_width/2-50, 420, window=select_all_btn)

    # 放入全部取消按鈕
    cancel_all_btn = tk.Button(root, 
                               text='全部取消', 
                               font=('Jokerman', 12, 'bold'), 
                               relief='solid', 
                               bd=2, 
                               fg=style_fg,
                               bg=style_bg,
                               command=cancel_all)
    cancel_all_window = canvas.create_window(bg_width/2+50, 420, window=cancel_all_btn)

    # 放入現在時間
    now_time = canvas.create_text(250, bg_height-50, 
                               text='', 
                               font=('Jokerman', 20, 'bold'), 
                               fill=text_color)
    print_time()
    # 音樂物件
    canvas_music()
    
    canvas.create_window(bg_width/2, 235, window=level_menu)
    canvas.create_window(bg_width/2, 320, window=total_menu)

# 註冊畫面
def sign_up() -> None:
    global sign_up_tk_img, now_time, sign_up_id,sign_up_id_entry, sign_up_pw, sign_up_pw_entry, sign_up_pw2, sign_up_pw2_entry
    global sign_up_title
    # 刪除canvas所有物件
    canvas.delete('all')
    
    # 假設after_id還在進行，取消它
    if after_id:
        root.after_cancel(after_id)
        
    # 放入註冊背景圖片
    sign_up_img = Image.open(resource_path('sign_up.jpg'))
    sign_up_img = sign_up_img.resize((bg_width, bg_height))
    sign_up_tk_img = ImageTk.PhotoImage(sign_up_img)
    canvas.create_image(0, 0, anchor='nw', image=sign_up_tk_img)   # 在 Canvas 中放入圖片

    # 音樂物件
    canvas_music()

    # 加入返回主選單按鈕
    back_menu_btn = tk.Button(root, 
                                text='Menu', 
                                font=('Jokerman', 14, 'bold'), 
                                fg=style_fg, 
                                bg=style_bg,
                                command=sign_up_back_main_menu)
    
    # 放入註冊標題
    sign_up_title = canvas.create_text(bg_width/2, 120, 
                    text='Sign Up', 
                    font=('Jokerman', 45, 'bold'), 
                    fill='black')
    
    # 放入"User Name:"text
    id = canvas.create_text(bg_width/2, 
                       320, 
                       text='User Name:',
                       font=('Jokerman', 20, 'bold'),
                       fill='#80FFFF')
    # 放入名字輸入框
    sign_up_id = tk.StringVar()
    sign_up_id_entry = tk.Entry(root, font=('Arial', 18), width=12,justify='center', textvariable=sign_up_id)
    

    #放入"Password:"text
    pw = canvas.create_text(bg_width/2,  
                       410, 
                       text='Password:',
                       font=('Jokerman', 20, 'bold'),
                       fill='#80FFFF')
    # 放入密碼輸入框
    sign_up_pw = tk.StringVar()
    sign_up_pw_entry = tk.Entry(root, font=('Arial', 18), width=12,justify='center', textvariable=sign_up_pw, show="*")
    

    #放入"Reapeat Password:"text
    pw2 = canvas.create_text(bg_width/2, 
                       530, 
                       text='Reapeat Password:',
                       font=('Jokerman', 20, 'bold'),
                       fill='#80FFFF')
    # 放入重複密碼輸入框
    sign_up_pw2 = tk.StringVar()
    sign_up_pw2_entry = tk.Entry(root, font=('Arial', 18), width=12,justify='center', textvariable=sign_up_pw2, show="*")
    

    # 放入送出按鈕
    sign_up_btn = tk.Button(root, 
                               text='Sign Up', 
                               font=('Jokerman', 12, 'bold'), 
                               relief='solid', 
                               bd=2, 
                               fg=style_fg,
                               bg=style_bg,
                               command=confirm_sign_up)
    
    # 繪製圖片周圍的邊框
    border_width = 8
    sign_up_rec = canvas.create_rectangle(
        bg_width/2-200,
        260,
        bg_width/2+200,
        260 + 450,
        outline="black", width=border_width
    )

    # 放入現在時間
    text_color = 'white'
    now_time = canvas.create_text(250, bg_height-50, 
                               text='', 
                               font=('Jokerman', 20, 'bold'), 
                               fill=text_color)
    print_time()

    canvas.create_window(60, 35, window=back_menu_btn)
    canvas.create_window(bg_width/2, 360, window=sign_up_id_entry)
    canvas.create_window(bg_width/2, 460, window=sign_up_pw_entry)
    canvas.create_window(bg_width/2, 580, window=sign_up_pw2_entry)
    canvas.create_window(bg_width/2, 630, window=sign_up_btn)

# 註冊確認
def confirm_sign_up() -> None:
    id = sign_up_id.get()
    pw = sign_up_pw.get()
    pw2 = sign_up_pw2.get()
    
    # 確認是否重複註冊
    password = ok_user_id(id)
    if password != "":
        messagebox.showwarning("Warning", "此帳號名稱已存在!")
        return
    # 任一欄位未輸入時
    if id == '' or pw == '' or pw2 == '':
        messagebox.showwarning("Warning", "任一欄位不可為空!")
        return
    
    # 名字長度過長時
    if len(id) >= 10:
        messagebox.showwarning('Warning', '名字長度過長! (>=10)')
        return
    # 密碼不一致時
    if pw != pw2:
        messagebox.showwarning('Warning', "密碼不一致!")
        sign_up_pw2_entry.delete(0, 'end')
        return
    # 任一欄位包含空白時
    if " " in id or " " in pw or " " in pw2:
        messagebox.showwarning("Warning", "名字或密碼不可包含空白!")
        sign_up_pw_entry.delete(0, 'end')
        sign_up_pw2_entry.delete(0, 'end')
        return
    # 密碼只能包含英文字母及數字
    for i in pw:
        if not(i >= 'A' and i <= 'Z' or i >= 'a' and i <= 'z' or i >= '0' and i <='9'):
            messagebox.showwarning("Warning", "密碼只能包含英文字母及數字")
            sign_up_pw_entry.delete(0, 'end')
            sign_up_pw2_entry.delete(0, 'end')
            return
    # 密碼長度必須四個字或以上
    if len(pw) < 4:
        messagebox.showwarning("Warning", "密碼長度必須四個字或以上")
        sign_up_pw_entry.delete(0, 'end')
        sign_up_pw2_entry.delete(0, 'end')
        return
    
    # 註冊成功
    register_user(id, pw)
    messagebox.showinfo("", "註冊成功!")
    # 刪除canvas所有物件
    canvas.delete('all')
    # 回登入畫面
    main_menu()

# 清除註冊畫面，並回到主選單
def sign_up_back_main_menu() -> None:
    try:
        canvas.destroy() if canvas else None
        main_menu()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        leave()

# 遊玩介面
def play(event) -> None:
    global hint_label, entry, answer, ok_correct, img, canvas, incorrect_label
    global question_img, confirm_btn, bg_tk_img, bg, tk_img, mosaic_level, blur_level, question_num, question_num_text
    global score, correct_count, total, level, turn, answers, pictures, groups, user_id, user_pw, now_time, group
    try:
        # 取得選取難易度
        level = level_value.get()
        # 取得選取總題數
        total = total_value.get()
        # 取得user name
        user_id = user_entry.get()
        # 取得user password
        user_pw = password_entry.get()

        # 名字未輸入時
        if user_id == "":
            # 跳出警告訊息 
            messagebox.showwarning('Warning', 'Please enter your name!')
            return
        # 密碼未輸入時
        if user_pw == "":
            # 跳出警告訊息 
            messagebox.showwarning('Warning', 'Please enter your password!')
            return
        # 包含空白時
        if " " in user_id or " " in user_pw:
            # 跳出警告訊息 
            messagebox.showwarning('Warning', '名字或密碼包含空白，請重新輸入!')
            return
        # 判斷是否註冊過
        password = ok_user_id(user_id)
        if password == '':
            messagebox.showwarning('Warning', '尚未註冊帳號\n前往註冊畫面')
            sign_up()
            return
        elif user_pw != password:
            messagebox.showwarning('Warning', '帳號或密碼錯誤!')
            return

        selected_num = 0
        if selected_topic == 'anime':
            # 取得選取動漫
            selected_animes = []
            for i, checkbox_var in enumerate(checkbox_vars):
                if checkbox_var.get():
                    selected_num += 1
                    # 把選取的動漫加到同一個串列
                    selected_animes.append(animes[i])
            print(selected_animes)
            answers, pictures, groups= get_random_jpg(selected_topic, selected_animes)

        elif selected_topic == 'kpop':
            # 取得選取kpop團體
            selected_kpops = []
            for i, checkbox_var in enumerate(checkbox_vars):
                if checkbox_var.get():
                    selected_num += 1
                    # 把選取的kpop團體加到同一個串列
                    selected_kpops.append(kpops[i])
            print(selected_kpops)
            answers, pictures, groups = get_random_jpg(selected_topic, selected_kpops)
        
        # 選擇數量未達5個時
        if selected_num < 5:
            # 跳出警告訊息 
            messagebox.showwarning('Warning', 'Please select five or more!')
            return
        
        # 假設after_id還在進行，取消它
        if after_id:
            root.after_cancel(after_id)
        # 根據難易度調整馬賽克、模糊程度
        if level == 'Very easy':
            mosaic_level = 1    # 由於分母不可為0，改1
            blur_level = 0
        elif level == 'Easy':
            mosaic_level = 10
            blur_level = 10
        elif level == 'Normal':
            mosaic_level = 30
            blur_level = 30
        elif level == 'Hard':
            mosaic_level = 50
            blur_level = 50

        # 刪除canvas所有物件
        canvas.delete('all')
        # 隨機選一張背景
        selected_bg = random.choice(backgrounds)
        # 選取題目
        turn = 0
        selected_jpg = pictures[turn]        
        # 答案(人物名稱==檔名)
        answer = answers[turn]
        # 團名、動漫名
        group = groups[turn]
        # 開啟圖片
        bg_img = Image.open(selected_bg)
        bg_img = bg_img.resize((bg_width, bg_height))
        # 將二進制轉回圖片
        img = Image.open(io.BytesIO(selected_jpg))
        img = img.resize((img_width, img_height))
        if selected_topic == 'anime':
            # 馬賽克處理
            mosaicked_img = mosaic(img, mosaic_level)
            # 轉換為 tk 圖片物件
            tk_img = ImageTk.PhotoImage(mosaicked_img)
        elif selected_topic == 'kpop':
            # 模糊化處理
            blurred_img = blurry(img, blur_level)
            # 轉換為 tk 圖片物件    
            tk_img = ImageTk.PhotoImage(blurred_img)

        # 轉換為 tk 圖片物件 
        bg_tk_img = ImageTk.PhotoImage(bg_img)
        # 放入canvas並放入背景圖片
        canvas = tk.Canvas(root, width=bg_width, height=bg_height)
        bg = canvas.create_image(0, 0, anchor='nw', image=bg_tk_img)   # 在 Canvas 中放入圖片
        canvas.place(x=0, y=0)

        # 音樂物件
        canvas_music()

        # 放入第幾題顯示
        question_num = 1
        question_num_text = canvas.create_text(bg_width/2, 35, text=f'第{question_num}題', font=('Jokerman', 25, 'bold'), fill='white')
        # 顯示分數
        score = 0
        #score_text = canvas.create_text(bg_width-110, 35, text=f"SCORE:{score}", font=('Jokerman', 25, 'bold'))
        # 顯示"請輸入人物名稱"
        hint_label = canvas.create_text(bg_width/2, 570, text='請輸入角色名稱', font=('Jokerman', 18, 'bold'), fill='white')
        # 放入判別對錯 text
        ok_correct = canvas.create_text(bg_width/2, 700, text='', font=('Jokerman', 21, 'bold'), fill='red')
        # 放入答對題數計算器
        correct_count = 0
        incorrect_label = canvas.create_text(bg_width-110, 35, text=f'Corrects:{correct_count}', font=('Jokerman', 20, 'bold'), fill='white')

        # 在 canvas 中放入圖片
        question_img = canvas.create_image(bg_width/2-img.width/2, 90, anchor='nw', image=tk_img)   # 在 Canvas 中放入圖片
        # 繪製圖片周圍的邊框
        border_width = 8
        canvas.create_rectangle(
            bg_width/2-img.width/2,
            90,
            bg_width/2-img.width/2 + img.width,
            90 + img.height,
            outline="black", width=border_width
        )
        # 放入單行輸入框
        entry = tk.Entry(root, font=('Arial', 18), width=25,justify='center')
        # 放入Submit按鈕
        confirm_btn = tk.Button(root, 
                                text='Submit', 
                                font=('Algerian', 14,'bold'), 
                                fg=style_fg, 
                                bg=style_bg,
                                command=confirm)   # 放入顯示按鈕，點擊後執行 confirm 函式
        # 加入返回主選單按鈕
        back_menu_btn = tk.Button(root, 
                                  text='Menu', 
                                  font=('Jokerman', 14, 'bold'), 
                                  fg=style_fg, 
                                  bg=style_bg,
                                command=back_main_menu)
        # 放入現在時間
        now_time = canvas.create_text(250, 
                                      bg_height-50, 
                                      text='', 
                                      font=('Jokerman', 20, 'bold'), 
                                      fill=text_color)
        print_time()
        entry_window = canvas.create_window(bg_width/2, 610, window=entry)
        confirm_window = canvas.create_window(bg_width/2, 658, window=confirm_btn)
        back_menu_window = canvas.create_window(60, 35, window=back_menu_btn)
    except Exception as e:
        # 跳錯誤訊息
        messagebox.showerror("Error", f"An error occurred: {e}")
        # 強制離開遊戲
        leave()

# 判斷正確與否
def confirm() -> None:
    global answer_tk_img, correct_count, next_btn, answer_text, group_text, score
    try:
        entered_name = entry.get()
        print(entered_name)
        
        # 輸入不為空且在檔名裡
        if (entered_name.lower() in answer.lower()) and (len(entry.get()) != 0) and ('、' not in entered_name):
            text = 'Correct'
            canvas.itemconfig(ok_correct,text=text, fill='green')
            # 答對題數加1
            correct_count += 1
            # 分數加10
            score += 10
            #canvas.itemconfig(score_text, text=f"SCORE:{score}")
        else:
            text = 'Wrong'
            canvas.itemconfig(ok_correct,text=text, fill='red')
        # 顯示答案
        answer_text = canvas.create_text(bg_width/2, 800, text="", font=('Jokerman', 25, 'bold'), fill=text_color)
        canvas.itemconfig(answer_text, text=f"Answer:{answer}")
        group_text = canvas.create_text(bg_width/2, 845, text="", font=('Jokerman', 25, 'bold'), fill=text_color)
        canvas.itemconfig(group_text, text=f"{group}")
        # 禁止輸入
        entry.config(state=tk.DISABLED)
        # 禁用按鈕
        confirm_btn.config(state=tk.DISABLED)

        # 顯示原始圖片
        answer_tk_img = ImageTk.PhotoImage(img)
        canvas.itemconfig(question_img, image=answer_tk_img)
        # 更新答對題數
        canvas.itemconfig(incorrect_label, text=f'Corrects:{correct_count}')

        # 超過選擇的總題數結束遊戲
        if question_num == int(total):
            # 放入"Show Result"按鈕
            result_btn = tk.Button(root,
                                text="Show Result",
                                font=('Jokerman', 14, 'bold'),
                                fg=style_fg,
                                bg=style_bg,
                                command=gameover)
            canvas.create_window(bg_width/2, 750, window=result_btn)
            # 延遲3秒顯示答案
            #root.after(3000, gameover)  
        else:
            # 放入"Next"按鈕
            next_btn = tk.Button(root,
                                text='Next',
                                font=('Algerian', 14, 'bold'),
                                command=go_next)
            next_window = canvas.create_window(bg_width/2, 750, window=next_btn)

            # 清空輸入框
            entry.delete(0, tk.END)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        leave()
    
# 前往下一題
def go_next() -> None:
    global answer, group, tk_img, img, question_num, turn
    try:
        # 清空答案
        canvas.itemconfig(answer_text, text=" ")
        canvas.itemconfig(group_text, text="")
        # 題號加1
        question_num += 1
        canvas.itemconfig(question_num_text, text=f"第{question_num}題")
        
        # 清空"答對"
        canvas.itemconfig(ok_correct, text="")
        # 隨機選一張jpg檔
        turn += 1
        selected_jpg = pictures[turn]
        # 答案(人物名稱==檔名)
        answer = answers[turn]
        # 團名、動漫名
        group = groups[turn]
        # 將二進制轉回圖片
        img = Image.open(io.BytesIO(selected_jpg))       
        img = img.resize((img_width, img_height))
        if selected_topic == 'anime':
            # 馬賽克處理
            mosaicked_img = mosaic(img, mosaic_level)
            tk_img = ImageTk.PhotoImage(mosaicked_img)
            canvas.itemconfig(question_img, image=tk_img)
        elif selected_topic == 'kpop':
            #模糊處理
            blurred_img = blurry(img, blur_level)
            tk_img = ImageTk.PhotoImage(blurred_img)
            canvas.itemconfig(question_img, image=tk_img)
        # 開放輸入
        entry.config(state=tk.NORMAL)
        # 清空輸入框
        entry.delete(0, tk.END)  
        # 開放按鈕
        confirm_btn.config(state=tk.NORMAL)
        # 刪除下一題按鈕
        next_btn.destroy()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        leave()

# 遊戲結束時觸發
def gameover() -> None:
    global gameover2_tk_img, leave_btn, result, counter, now_time
    try:
        # 刪除canvas所有物件
        canvas.delete('all')
        # 更換背景為隨機背景
        selected_result_bg = random.choice(result_bgs)
        gameover2_img = Image.open(selected_result_bg)
        gameover2_img = gameover2_img.resize((bg_width, bg_height))
        gameover2_tk_img = ImageTk.PhotoImage(gameover2_img)
        canvas.create_image(0, 0,anchor='nw', image=gameover2_tk_img)

        # 音樂物件
        canvas_music()
        # 放入現在時間
        now_time = canvas.create_text(250, 
                                      bg_height-50, 
                                      text='', 
                                      font=('Jokerman', 20, 'bold'), 
                                      fill=text_color)
        print_time()

        # 加入分數結果text
        result = canvas.create_text(bg_width/2, 180, text='Your Score:\n0', font=('Jokerman', 50, 'bold'), fill='white', justify='center')
        # 加入返回主選單按鈕
        back_menu_btn = tk.Button(root, 
                                text='Menu', 
                                font=('Algerian', 18, 'bold'), 
                                fg='green', 
                                command=back_main_menu)
        # 加入離開遊戲按鈕
        leave_btn = tk.Button(root, 
                            text='Exit', 
                            font=('Algerian', 18, 'bold'), 
                            fg='green',
                            command=leave)
        
        back_main_window = canvas.create_window(bg_width/2-200, bg_height/2, window=back_menu_btn)
        leave_window = canvas.create_window(bg_width/2+200, bg_height/2, window=leave_btn)

        counter = 0
        update_score()

        ranking()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        leave()
    
# 排行榜
def ranking() -> None:
    # 取得現在時間
    now = time.ctime(time.time())
    # 加入資料庫，且取得前10名串列
    top_10 = get_ranking(now, user_id, score, total, level, selected_topic)
    #計數器
    c = 0
    # 抓取db資料
    for data in top_10:
        data_name = data[0]
        data_score = data[1]
        data_time = data[2]
        text = f"#{c+1:<3}Name:{data_name:<10}Score:{data_score:<4}\n\tTime:{data_time[-20:]}\n"
        # 上榜的話標註
        if data_time == now:
            canvas.create_text(250, 180+c*65, text=text, font=('Arial', 18, 'bold'), fill='#FFFF37', justify='left')
        else:
            canvas.create_text(250, 180+c*65, text=text, font=('Arial', 18, 'bold'), fill='white', justify='left')
        c += 1

    # 放入"Ranking:"text
    canvas.create_text(20, 
                       20, 
                       text=f"Ranking({total}, {level}, {selected_topic}):\n", 
                       font=('Jokerman', 25, 'bold'), 
                       fill='white', 
                       justify='center',
                       anchor='nw')

# 更新分數
def update_score() -> None:
    global counter
    try:
        if counter == score:
            canvas.itemconfig(result, text=f"Your Score:\n", fill='white')
            canvas.create_text(bg_width/2, 210, text=f'{counter}', font=('Jokerman', 50, 'bold'), fill='yellow', justify='center')
        if counter < score:
            canvas.itemconfig(result, text=f"Your Score:\n{counter}")
            counter += 1
            canvas.after(20, update_score)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        leave()

# 清除遊玩畫面，並回到主選單
def back_main_menu() -> None:
    global back_count
    try:
        back_count += 1
        canvas.destroy() if canvas else None
        main_menu()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        leave()


def main() ->None:
    global  user_id

    tkinter()
    # 取得現在時間
    end_time = time.ctime(time.time())
    if user_id != "":
        print(f"{user_id}:{counter}, End Time:{end_time}, 題數:{total}")
    
if __name__ == '__main__':
    main()
