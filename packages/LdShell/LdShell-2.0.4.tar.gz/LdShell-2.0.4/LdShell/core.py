import requests
import json
import os
import sys
from configobj import ConfigObj
import time
import codecs
class LdType() :
        none=0
        Click=1;     #点击
        Swipe=2      #滑动
        Long=3       #长按
        Exists=4     #是否存在
        Start=5      #启动包名
        Kill=6       #关闭包名
        Input=7      #输入文字
        Pull=8       #文件到电脑
        Push=9       #文件到手机
        Keyevent=10  #按键
        adb=11       #ADB命令
        shell=12     #Shell命令
        text=13
        content=14
        child=15
        Tap=16
        Checked=17
        LongCLick=18
        ListText=19
        ListLocal=20
        ALL=21
        Code=22
        Count=23
class InitLdPlayer :
     index=0
     _debug=False
     def __init__(self, index=None,debug=False):
          InitLdPlayer.index=index
          InitLdPlayer._debug=debug
    
      
class d() :

    # 下面定义了一个类变量
    lds=None
    resourceid =None
    text=None
    _class=None
    package=None
    contentdesc=None
    index=None
    input_text=None
     
    def __init__(self, resourceid=None,text=None,cls=None,package=None,contentdesc=None,index=None):
        # 下面为Person对象增加2个实例变量
        self.resourceid = resourceid;
        self.text = text;
        self._class = cls;
        self.package = package;
        self.contentdesc = contentdesc;
        self.index = index;
    
    def initJson(self,type):
          self.lds = {
                "index":InitLdPlayer.index,
                "type":type,
                "txt":self.input_text,
                "cmd":{
                    "resourceid":self.resourceid,
                    "text":self.text,
                    "_class":self._class,
                    "package":self.package,
                    "contentdesc":self.contentdesc,
                    "index":self.index,
                }

            }
    def IniPost(self,ldtype):
        for a in range(3):
            try:
                self.initJson(ldtype);
                url = 'http://127.0.0.1:33221/ldshell/'
                if(InitLdPlayer._debug):
                    print(url)
                    print(json.dumps(self.lds))

                res = requests.post( url=url,data=json.dumps(self.lds),timeout=30)
                if(InitLdPlayer._debug):
                    print(res.text)
                _state=eval(res.text)
                return _state
            except Exception as e:
                if(InitLdPlayer._debug):
                    print(e)
                time.sleep(1)
                pass
        return False;

    def InistrPost(self,ldtype):
        for a in range(3):
            try:
                self.initJson(ldtype);
                url = 'http://127.0.0.1:33221/ldshell/'

                if(InitLdPlayer._debug):
                    print(url)
                    print(json.dumps(self.lds))
                res = requests.post(url=url,data=json.dumps(self.lds),timeout=30)

                if(InitLdPlayer._debug):
                    print(res.text)
                    
                return res.text
            except Exception as e:
                if(InitLdPlayer._debug):
                    print(e)
                time.sleep(1)
                pass
        return "";

    # 下面定义了一个CLick方法
    def Click(self):
        return self.IniPost(LdType.Click)

    # 下面定义了一个LongCLick方法
    def LongCLick(self):
        return self.IniPost(LdType.LongCLick)
    
    # 下面定义了一个Input方法
    def Input(self,txt):
        self.input_text=txt
        return self.IniPost(LdType.Input)

    # 下面定义了一个Exists方法
    def Exists(self):
        return self.IniPost(LdType.Exists)
    
    # 下面定义了一个Wait方法
    def Wait(self,timeout=30):
        for a in range(timeout):
            if self.IniPost(LdType.Exists):
                return True
            time.sleep(3)
        return False

    # 下面定义了一个Checked方法
    def Checked(self):
        return self.IniPost(LdType.Checked)

    # 下面定义了一个 Swipe 方法
    def Swipe(self,xy):
        self.input_text=xy
        return self.IniPost(LdType.Swipe)

    # 下面定义了一个 Keyevent 方法
    def Keyevent(self,key):
        self.input_text=key
        return self.IniPost(LdType.Keyevent)
    

    # 下面定义了一个 Start 方法
    def StartApp(self,pke):
        self.input_text=pke
        return self.IniPost(LdType.Start)
    
    # 下面定义了一个 Start 方法
    def StopApp(self,pke):
        self.input_text=pke
        return self.IniPost(LdType.Kill)

    # 下面定义了一个 ClearApp 方法
    def ClearApp(self,pke):
        self.input_text="pm clear "+pke
        return self.IniPost(LdType.shell)
    
    # 下面定义了一个 UpFile 方法
    def UpFile(self,source,mubiao):
        self.input_text=source+" "+mubiao
        return self.IniPost(LdType.Push)
    
    # 下面定义了一个 Adb 方法
    def Adb(self,adb):
        self.input_text=adb
        return self.IniPost(LdType.adb)
    
    # 下面定义了一个 Shell 方法
    def Shell(self,shell):
        self.input_text=shell
        return self.IniPost(LdType.shell)
    
    # 下面定义了一个 Text 方法
    def Text(self):
        return self.InistrPost(LdType.text)

    # 下面定义了一个 ALL 方法
    def ALL(self):
        return self.InistrPost(LdType.ALL)
    
    # 下面定义了一个 Code 方法
    def Code(self):
        return self.InistrPost(LdType.Code)
    
    # 下面定义了一个 Code 方法
    def Count(self):
        return self.InistrPost(LdType.Count)
    

    # 下面定义了一个 ListText 方法
    def ListText(self):
        return self.InistrPost(LdType.ListText)
    
    # 下面定义了一个 ListLocal 方法
    def ListLocal(self):
        return self.InistrPost(LdType.ListLocal)
    
    # 下面定义了一个 Content 方法
    def Content(self):
        return self.InistrPost(LdType.content)

    # 下面定义了一个 Child 方法
    def Child(self):
        return self.InistrPost(LdType.child)
    
    # 下面定义了一个 Tap 方法
    def Tap(self,xy):
        self.input_text=xy
        return self.IniPost(LdType.Tap)


    # 下面定义了一个 Back 方法
    def Back(self):
        self.input_text="input keyevent 4"
        return self.IniPost(LdType.shell)


    # 下面定义了一个 Home 方法
    def Home(self):
        self.input_text="input keyevent 3"
        return self.IniPost(LdType.shell)

    # 下面定义了一个 Tab 方法
    def Tab(self):
        self.input_text="input keyevent 61"
        return self.IniPost(LdType.shell)
        
    # 下面定义了一个 Enter 方法
    def Enter(self):
        self.input_text="input keyevent 66"
        return self.IniPost(LdType.shell)
    
    # 下面定义了一个 BackSpage 方法
    def BackSpage(self):
        self.input_text="input keyevent 67"
        return self.IniPost(LdType.shell)
        
    # 读取INI文件
    def ReadINI(self,node='Main',key='about',enc='gbk'):
        try:
            IniPath = os.path.dirname(os.path.abspath(sys.argv[0]))+"\\system.ini"
            config = ConfigObj(IniPath,encoding=enc)
            _value=config[node][key]
            return _value
        except Exception as e:
             print(e)
        return ""

    # 读取INI文件
    def SaveINI(self,node='Main',key='about',value='value',enc='gbk'):
        try:
            IniPath = os.path.dirname(os.path.abspath(sys.argv[0]))+"\\system.ini"
            config = ConfigObj(IniPath,encoding=enc)
            config[node][key] =value
            config.write()
            return True

        except Exception as e:
             print(e)
        return False

        

    # 保存日志
    def SaveLog(self,Info='Null',FileName='Success',logPath='',Enc='utf-8'):
        try:
            time1 = time.strftime('%Y-%m-%d %H:%M:%S')+"  "

            path = logPath
            if len(path) == 0:
                path = os.path.dirname(os.path.abspath(sys.argv[0]))+"\\"+FileName+".log"

            
            print(path)
            File = open(path,'a+',encoding=Enc)
            File.write(time1+Info+'\r\n')
            File.flush()
        except Exception as e:
             print(e)
        return ""
        

    # 读取日志
    def ReadLog(self,logPath='',FileName='Success',Enc='utf-8'):
        try:
            path = logPath
            if len(path) == 0:
                path = os.path.dirname(os.path.abspath(sys.argv[0]))+"\\"+FileName+".log"

            if os.path.exists(path):
                f = codecs.open(path,'r',encoding=Enc)#必须事先知道文件的编码格式，这里文件编码是使用的utf-8
                content = f.read()#如果open时使用的encoding和文件本身的encoding不一致的话，那么这里将将会产生错误
                return content
        except Exception as e:
            print(e)
        return ""

       
