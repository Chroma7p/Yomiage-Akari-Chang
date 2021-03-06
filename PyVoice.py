import time
import clr
import json

clr.AddReference("AI.Talk.Editor.Api")
import AI.Talk.Editor.Api as API


class Preset:
    """
    AIVoiceのプリセット用クラス
    --------------------------
    dict:辞書化
    toJSON:JSON化
    """

    def __init__(self,PresetName="紲星 あかり",VoiceName="akari_emo_48",Volume=1,Speed=1,Pitch=1,PitchRange=1,MiddlePause=200,LongPause=200,BasePitchVoiceName="",MergedVoices=[],StyleJ=0,StyleA=0,StyleS=0,JSON=None):
        """
        
        """
        if JSON!=None:
            dic=json.loads(JSON)

        self.PresetName=PresetName
        self.VoiceName=VoiceName
        self.Volume=Volume
        self.Spped=Speed
        self.Pitch=Pitch
        self.PitchRange=PitchRange
        self.MiddlePause=MiddlePause
        self.LongPause=LongPause
        self.BasePitchVoiceName=BasePitchVoiceName
        self.MergedVoices=MergedVoices
        self.StyleJ=StyleJ
        self.StyleA=StyleA
        self.StyleS=StyleS
    
    def __dict__(self):
        return {
            "PresetName":self.PresetName,
            "VoiceName":self.VoiceName,
            "Volume":self.Volume,
            "Speed":self.Spped,
            "Pitch":self.Pitch,
            "PitchRange":self.PitchRange,
            "MiddlePause":self.MiddlePause,
            "LongPause":self.LongPause,
            "MergedVoiceContainer":{
                "BasePitchVoiceName":self.BasePitchVoiceName,
                "MergedVoices":self.MergedVoices
            },
            "Style":[
                {
                    "Name":"J",
                    "Value":self.StyleA
                },
                {
                    "Name":"A",
                    "Value":0
                },
                {
                    "Name":"S",
                    "Value":0
                }
            ]
        }
    
    def toJSON(self):
        return json.dumps(dict(self))





class PyVoice:
    """
    APIラッパーのクラス
    ---------------------------
    control:APIのインスタンス
    Version:現在のホストプログラムのバージョン
    Hosts:ホストプログラムの一覧
    Voices:保有しているボイスの一覧
    Presets:プリセット一覧
    CurrentHost:現在のホストプログラム
    CurrentText:現在保持しているテキスト
    CurrentPresetName:現在登録しているプリセット名
    """

    def __init__(self):
        """
        インスタンスの初期化
        -------------------
        APIの情報の取得
        APIの初期化
        ホストプログラムの起動
        ホストプログラムへの接続
        """
        self.control=API.TtsControl()
        self.CurrentText=-1
        try:
            self.Hosts=list(self.control.GetAvailableHostNames())
            if len(self.Hosts)>0:
                self.CurrentHost=self.Hosts[0]
            else:
                print("Can't find Host...")
                raise Exception
            self.control.Initialize(self.CurrentHost)
            print("Intialized!")
            if self.control.Status==0:
                self.control.StartHost()
            self.control.Connect()
            if self.control.Status in (0,1):
                print("Can't Connect...")
                raise Exception
            else:
                print("Connected!")
                self.Version=self.control.Version
                self.CurrentPresetName=self.control.CurrentVoicePresetName
                self.Voices=list(self.control.VoiceNames)
                self.Presets=list(self.control.VoicePresetNames)
                self.CurrentPreset=json.loads(self.control.GetVoicePreset(str(self.CurrentPresetName)))
                print("- "*20)
                print(f"A.I.Voice Version : {self.Version}")
                print(f"Voice List : {self.Voices}")  
                print(f"Voice Preset List : {self.Presets}")
                print(f"Host List : {self.Hosts}")
                print(f"Current Host : {self.CurrentHost}")   
                print(f"Current Preset Name: {self.CurrentPresetName}")
                print(f"Current Preset:")
                print(json.dumps(self.CurrentPreset,indent=4,ensure_ascii = False))
                print("- "*20)
                
        except Exception as e:
            print("error occurred during connection...")
            print(e)
            self.shutdown()
            exit()


    def shutdown(self):
        """
        切断とシャットダウン
        """
        try:
            if self.control.Status==2:
                self.control.Disconnect()
                self.control.TerminateHost()
            elif self.control.Status==1:
                self.control.TerminateHost()
            elif self.control.Status==3:
                print("host is busy now...")
                time.sleep(1)
                self.shutdown()
            else:
                print("can't shutdown...")
                raise Exception
            print("Shutdown : goodbye!")
        except:
            print("couldn't shutdown")


    def SetText(self,string):
        """
        テキストの設定
        """
        if self.control.TextEditMode!=0:
            print("SetText use in text mode")
            return
        self.control.Text=string
        self.CurrentText=string
        print(f"Text:\n{self.control.Text}")

    def PlayVoice(self):
        """
        設定中のテキストの再生
        """
        try:
            playtime=self.control.GetPlayTime()
            print(f"Play Time:{playtime}ms")
            
            self.control.Play()
            time.sleep(playtime/900)
        except:
            print("failed to play")

    def SaveVoice(self,path="path"):
        """
        設定中のテキストの音声の保存
        """
        if self.CurrentText==-1:
            print("set text for voice")
            return 
        if path=="path":
            savepath=f"{self.CurrentText[:10]}.wav"
        self.control.SaveAudioToFile(savepath)
        print(f"saving: {savepath}")

    def Talk(self,string):
        """
        指定した単語を喋る
        """
        self.SetText(string)

        self.PlayVoice()

    def GetPreset(self,preset_name):
        """
        引数nameのプリセットの詳細をJSON形式で取得
        """
        return self.control.GetVoicePreset(preset_name)

    def GetPlayTime(self):
        """
        現在登録されているテキストの再生時間を取得
        """
        return self.control.GetPlayTime()
    
    def SetPresetName(self,name):
        """
        プリセットを名前で指定
        """
        new_preset=self.GetPreset(name)
        print(new_preset)
        self.control.CurrentVoicePresetName=name

    def GetPresetList(self):
        """
        プリセットのリストを取得
        """
        return self.Presets
    
    def SetPresetJSON(self,preset):
        """
        JSON形式てプリセットを指定
        """
        self.control.SetVoicePreset(preset)

    def GetCurrentPresetName(self):
        """
        現在のプリセット名を取得
        """
        return self.control.CurrentVoicePresetName

    def SetPreset(self,preset:Preset):
        """
        Preset型をそのままプリセットとして指定
        """
        self.control.SetVoicePreset(preset.toJSON())

