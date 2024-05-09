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

    # get all master info (volume state, volume level, volume range)
    def getMasterInfo(self):
        return self.m_master_volume.GetVolumeRange()

    # get master mute state
    # 0 represents unmuted
    # 1 represents muted
    def getMasterState(self):
        self.m_master_mute = self.m_master_volume.GetMute()
        return self.m_master_mute
    
    # master toggle between mute and unmute based on current state
    def toggleMasterState(self):
        if (self.getMasterState()): self.m_master_volume.SetMute(0, None)
        else: self.m_master_volume.SetMute(1, None)

    # set master mute
    # 0 for unmute
    # 1 for mute
    def setMasterState(self, mute):
        if (type(mute) is not int): raise TypeError("Mute must be int type!")
        if int(mute) > 1 or int(mute) < 0: raise Exception("Invalid mute value!"); return
        self.m_master_volume.SetMute(int(mute), None)
    
    # master volume getter in native format (-65.25 to 0, where 0 is max) ! not linear scaling
    def getMasterVolume(self):
        self.m_master_volume_level = self.m_master_volume.GetMasterVolumeLevel()
        return self.m_master_volume_level

    # set master volume using native format as specified above
    def setMasterVolume(self, volume):
        self.m_master_volume.SetMasterVolumeLevel(volume, None)