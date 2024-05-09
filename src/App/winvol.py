from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume, IAudioEndpointVolume

# Windows volume control
class CVolume():
    # initializer for volume control - master volume and common application lists
    def __init__(self):
        self.m_master_device = AudioUtilities.GetSpeakers()
        self.m_master_interface = self.m_master_device.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.m_master_volume = self.m_master_interface.QueryInterface(IAudioEndpointVolume)
        self.m_voip_enum = ['Discord.exe', 'slack.exe', 'ms-teams.exe']
        self.m_music_apps_enum = ['Spotify.exe', 'iTunes.exe']
        self.m_browsers_enum = ['msedge.exe', 'firefox.exe', 'chrome.exe', 'opera.exe']