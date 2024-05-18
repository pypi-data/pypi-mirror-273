import os 
import random
import pygame
import threading
# 初始化pygame
pygame.init()
pygame.mixer.init()
musics = []
i = 0
def setting():
    # 當前資料夾
    current_dir = os.getcwd()
    # 設定音樂資料夾
    music_dir = os.path.join(current_dir, 'music')
    for file_name in os.listdir(music_dir):
        if file_name.endswith('.mp3'):
            full_path = os.path.join(music_dir, file_name)
            musics.append(full_path)
    # 隨機音樂順序
    random.shuffle(musics)


def play_music():
    global paused, i
    paused = False
    
    if i == len(musics):
        i = 0
    # 選取當前歌曲、下一首歌曲
    music = musics[i]
    music2 = musics[(i + 1) % len(musics)]
    print(music)
    pygame.mixer.music.load(music)
    pygame.mixer.music.play(fade_ms=2000)
    i += 1

# 暫停、播放
def play_pause() -> None:
    global paused

    paused = not paused

    if paused:
        pygame.mixer.music.pause()

    else:
        pygame.mixer.music.unpause()
 
setting()
play_music()
def next_song():
    while True:
        if (not pygame.mixer.music.get_busy()) and (not paused):
            play_music()

threading.Thread(target=next_song).start()
for k in range(3):
    c = input(';::')
    if c== 'c':
        play_pause()