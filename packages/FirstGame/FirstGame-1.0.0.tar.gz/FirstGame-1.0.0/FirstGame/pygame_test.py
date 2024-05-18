import pygame
import tkinter as tk

pygame.init()
pygame.mixer.init()

paused = False
# 播放
def music_play():
    if pygame.mixer.music.get_busy():
        return 1
    var1.set("Now Playing: Color Out - Host")
    pygame.mixer.music.load("music\\Color_Out_-_Host.mp3")
    pygame.mixer.music.play(fade_ms=3000)

# 暫停、播放
def play_pause() -> None:
    global paused

    paused = not paused

    if paused:
        pygame.mixer.music.pause()
        play_pause_btn.config(text='繼續')
    else:
        pygame.mixer.music.unpause()
        play_pause_btn.config(text='暫停')

    
    
    

root = tk.Tk()
root.geometry('500x500+100+0')



var1 = tk.StringVar()
label = tk.Label(root, textvariable=var1, font=('Arial', 18, 'bold'), fg='red')
music_play()

play_pause_btn = tk.Button(root,text='暫停',font=('Arial', 18, 'bold'),command=play_pause)

label.pack()
play_pause_btn.pack()

root.mainloop()
