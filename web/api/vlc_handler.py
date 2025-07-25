import subprocess
import webbrowser
import os
import sys

class VLCHandler:
    """Handler for video player integration"""
    
    def __init__(self):
        pass
    
    def play_video(self, video_url, player='vlc', title=''):
        """Play video with the specified player"""
        try:
            if player == 'vlc':
                return self._play_with_vlc(video_url, title)
            elif player == 'mpv':
                return self._play_with_mpv(video_url, title)
            elif player == 'default':
                return self._play_with_default(video_url)
            else:
                print(f"Unknown player: {player}")
                return False
                
        except Exception as e:
            print(f"Error playing video: {e}")
            return False
    
    def _play_with_vlc(self, video_url, title=''):
        """Play video with VLC player"""
        try:
            # Try different methods to open VLC
            vlc_commands = [
                ['vlc', video_url],
                ['/usr/bin/vlc', video_url],
                ['/Applications/VLC.app/Contents/MacOS/VLC', video_url],
                ['C:\\Program Files\\VideoLAN\\VLC\\vlc.exe', video_url],
                ['C:\\Program Files (x86)\\VideoLAN\\VLC\\vlc.exe', video_url]
            ]
            
            if title:
                # Add title option for VLC
                for cmd in vlc_commands:
                    cmd.extend(['--meta-title', title])
            
            for cmd in vlc_commands:
                try:
                    subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    return True
                except FileNotFoundError:
                    continue
            
            # If VLC not found, try opening with system default
            print("VLC not found, trying system default...")
            return self._play_with_default(video_url)
            
        except Exception as e:
            print(f"Error with VLC: {e}")
            return False
    
    def _play_with_mpv(self, video_url, title=''):
        """Play video with MPV player"""
        try:
            cmd = ['mpv', video_url]
            
            if title:
                cmd.extend(['--force-media-title', title])
            
            subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
            
        except FileNotFoundError:
            print("MPV not found, trying system default...")
            return self._play_with_default(video_url)
        except Exception as e:
            print(f"Error with MPV: {e}")
            return False
    
    def _play_with_default(self, video_url):
        """Play video with system default player"""
        try:
            # Try to open with system default application
            if sys.platform.startswith('linux'):
                subprocess.Popen(['xdg-open', video_url])
            elif sys.platform == 'darwin':  # macOS
                subprocess.Popen(['open', video_url])
            elif sys.platform == 'win32':  # Windows
                os.startfile(video_url)
            else:
                # Fallback to webbrowser
                webbrowser.open(video_url)
            
            return True
            
        except Exception as e:
            print(f"Error with default player: {e}")
            # Last resort: open in web browser
            try:
                webbrowser.open(video_url)
                return True
            except Exception as e2:
                print(f"Error opening in browser: {e2}")
                return False
    
    def is_player_available(self, player):
        """Check if a specific player is available on the system"""
        if player == 'vlc':
            return self._check_vlc_available()
        elif player == 'mpv':
            return self._check_mpv_available()
        else:
            return True  # Default player should always be available
    
    def _check_vlc_available(self):
        """Check if VLC is available"""
        try:
            subprocess.run(['vlc', '--version'], 
                         stdout=subprocess.DEVNULL, 
                         stderr=subprocess.DEVNULL, 
                         check=True)
            return True
        except (FileNotFoundError, subprocess.CalledProcessError):
            return False
    
    def _check_mpv_available(self):
        """Check if MPV is available"""
        try:
            subprocess.run(['mpv', '--version'], 
                         stdout=subprocess.DEVNULL, 
                         stderr=subprocess.DEVNULL, 
                         check=True)
            return True
        except (FileNotFoundError, subprocess.CalledProcessError):
            return False