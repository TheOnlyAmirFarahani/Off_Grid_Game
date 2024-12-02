import sys
import os
import subprocess
import time
import vlc

if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS  
else:
    base_path = os.path.dirname(os.path.abspath(__file__))  

def play_video_in_fullscreen(video_path):
    try:
        vlc_instance = vlc.Instance('--no-xlib')
        player = vlc_instance.media_player_new()
        media = vlc_instance.media_new(video_path)
        player.set_media(media)
        player.set_fullscreen(True)
        player.play()
        while player.get_state() != vlc.State.Ended:
            time.sleep(1)
        player.release()
    except Exception as e:
        print(f"Error playing video: {e}")

def launch_desktop_application():
    try:
        desktop_script = os.path.join(base_path, "desktop.py")  
        subprocess.Popen(["python", desktop_script])
    except Exception as e:
        print(f"Error launching desktop.py: {e}")

if __name__ == "__main__":
    video_path = os.path.join(base_path, "media/starts.mp4")
    play_video_in_fullscreen(video_path)
    launch_desktop_application()
