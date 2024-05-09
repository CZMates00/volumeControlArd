from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume, IAudioEndpointVolume
from math import log, pow

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

    # master volume getter in % format in range <0, 100>
    # inverse to logarithmic function used for volume setting
    def getMasterVolumeNative(self):
        self.cur = self.getMasterVolume()
        if self.cur == -65.25: return 0
        elif self.cur >= -65 and self.cur < -55 : return round(pow(10, 2+(self.cur/29)))
        elif self.cur >= -55 and self.cur < -46 : return round(pow(10, 2+(self.cur/31.2)))
        elif self.cur >= -46 and self.cur < -41 : return round(pow(10, 2+(self.cur/32.5)))
        elif self.cur >= -41 and self.cur < -34 : return round(pow(10, 2+(self.cur/33)))
        elif self.cur >= -34 and self.cur < -28 : return round(pow(10, 2+(self.cur/33.5)))
        elif self.cur >= -28 and self.cur < 0 : return round(pow(10, 2+(self.cur/34)))
        elif self.cur == 0.0: return 100
        else: raise Exception("Invalid volume level returned!")

    # set master volume using % format as specified above
    # approximation of a logarithmic function for platforms with native format range <-65.25, 0>
    def setMasterVolumeNative(self, volume):   
        self.min_db = -65.25
        self.max_db = 0
        if (type(volume) is not int): raise TypeError("Volume must be int type!")
        if volume <= 0: new_volume_to_set = self.min_db
        elif volume < 2 and volume > 0: new_volume_to_set = 29*log(volume/100, 10)
        elif volume < 4 and volume >= 2: new_volume_to_set = 31.2*log(volume/100, 10)
        elif volume < 6 and volume >= 4: new_volume_to_set = 32.5*log(volume/100, 10)
        elif volume < 10 and volume >= 6: new_volume_to_set = 33*log(volume/100, 10)
        elif volume < 15 and volume >= 10: new_volume_to_set = 33.5*log(volume/100, 10)
        elif volume < 100 and volume >= 15: new_volume_to_set = 34*log(volume/100, 10)
        elif volume >= 100: new_volume_to_set = self.max_db
        else: raise Exception("Invalid volume value!"); return

        self.setMasterVolume(new_volume_to_set)
        return new_volume_to_set

    # increment master volume by number in native format
    def setMasterVolumeIncNative(self, volInc):
        cur = self.getMasterVolumeNative()
        self.setMasterVolumeNative(cur+volInc)

    # decrement master volume by number in native format
    def setMasterVolumeDecNative(self, volDec):
        cur = self.getMasterVolumeNative()
        self.setMasterVolumeNative(cur-volDec)

    # get all sessions for further volume modification
    def getSessions(self):
        self.m_sessions = AudioUtilities.GetAllSessions()
        return self.m_sessions
    
    # find all running applications names and return them as a list
    def getSessionsNames(self):
        self.m_sessions = AudioUtilities.GetAllSessions()
        self.m_s_array = []
        for s in self.m_sessions:
            if s.Process:
                self.m_s_array.append(s.Process.name())
        return self.m_s_array
    
    # find all running applications names and return them to the user specified list
    def getSessionNamesOut(self, array):
        self.m_sessions = AudioUtilities.GetAllSessions()
        for s in self.m_sessions:
            if s.Process:
                array.append(str(s.Process.name()))
    
    # set the specified sessions' volume to vol percent of the default audio output device
    # when vol > 100, volume is set to 100
    # when vol < 0, volume is set to 0
    def setSessionVolume(self, sessionName, vol):
        if vol > 100: v = 100
        if vol < 0: v = 0
        else: v = vol
        for s in self.getSessions():
            volume = s._ctl.QueryInterface(ISimpleAudioVolume)
            if s.Process and s.Process.name().lower() == sessionName.lower():
                volume.SetMasterVolume(v/100, None)
    
    # get session volume; value returned is in % of master output level
    def getSessionVolume(self, sessionName):
        for s in self.getSessions():
            volume = s._ctl.QueryInterface(ISimpleAudioVolume)
            if s.Process and s.Process.name().lower() == sessionName.lower():
                return round(volume.GetMasterVolume()*100)
            
    # increment session volume
    def setSessionVolumeInc(self, sessionName, volInc):
        cur = self.getSessionVolume(sessionName)
        self.setSessionVolume(sessionName, cur+volInc)

    # decrement session volume
    def setSessionVolumeDec(self, sessionName, volDec):
        cur = self.getSessionVolume(sessionName)
        self.setSessionVolume(sessionName, cur-volDec)

    # returns 0 if the session is not muted
    # returns 1 if the session is muted
    def getSessionState(self, sessionName):
        pass

    # set the sessions mute state 0 or 1
    def setSessionState(self, sessionName):
        pass

    # toggle between muted and unmuted state
    def toggleSessionState(self, sessionName):
        pass