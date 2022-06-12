import time
import clr

clr.AddReference("AI.Talk.Editor.Api")
import AI.Talk.Editor.Api as API



class PyVoice:

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
        self.isEmpty=True
        try:
            self.Hosts=self.control.GetAvailableHostNames()
            print(self.Hosts)
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
                print("Ready!")
                print("- "*20)
                print(f"A.I.Voice Version : {self.Version}")
                print(f"Current Host : {self.CurrentHost}")     
        except:
            print("error occurred during connection...")
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
        self.isEmpty=False
        self.CurrentText=string
        print(f"Text:{self.control.Text}")

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
        if self.isEmpty:
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

