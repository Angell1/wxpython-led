import wx
import socket
import wx.gizmos as gizmos
import re

class Example(wx.Frame):
    def __init__(self, parent, title):
        super(Example, self).__init__(parent, title=title,size=(800,800))
        self.Init_Panel()
        self.Init_Box()
        self.Init_Left()
        self.Init_Right()
        # 将三个垂直盒子添加到垂直盒子
        self.Boxh1.Add(self.LeftPanel,proportion = 1, border = 2,flag = wx.ALL | wx.EXPAND)
        self.Boxh1.Add(self.RightPanel, proportion=4, border=2, flag=wx.ALL | wx.EXPAND)

        #将垂直盒子和主框架关联
        self.SetSizer(self.Boxh1)
        #显示主框架
        self.Show()
        self.s = None
    #创建两个面板
    def Init_Panel(self):
        self.LeftPanel = wx.Panel(self)
        self.RightPanel = wx.Panel(self)

    #创建三个盒子
    #一个垂直盒子、两个水平盒子
    def Init_Box(self):
        #两个垂直盒子
        self.Boxv1 = wx.BoxSizer(wx.VERTICAL)
        self.Boxv2 = wx.BoxSizer(wx.VERTICAL)
        #一个水平盒子
        self.Boxh1 = wx.BoxSizer(wx.HORIZONTAL)
        self.Boxh2 = wx.BoxSizer(wx.HORIZONTAL)
    def Init_Left(self):
        self.Label3 = wx.StaticText(self.LeftPanel, -1, "设置客户端链接")
        self.Label3.SetForegroundColour('white')
        self.Label3.SetBackgroundColour('black')
        self.Boxv1.Add(self.Label3, 0, wx.ALIGN_CENTRE, 10)
        self.Label1 = wx.StaticText(self.LeftPanel, -1, "服务器：")
        # 服务器ip输入文本框
        self.inputText = wx.TextCtrl(self.LeftPanel, -1, "", pos=(80, 10), size=(150, -1))
        self.inputText.SetInsertionPoint(0)  # 设置焦点位置
        self.Boxv1.Add(self.Label1, 0, wx.EXPAND | wx.ALL, 0)
        self.Boxv1.Add(self.inputText, 0, wx.EXPAND | wx.ALL, 0)

        self.Label2 = wx.StaticText(self.LeftPanel, -1, "端口：")
        # 服务器端口输入框
        self.pwdText = wx.TextCtrl(self.LeftPanel, -1, "", pos=(80, 50), size=(150, -1))
        self.Boxv1.Add(self.Label2, 0, wx.EXPAND | wx.ALL,0)
        self.Boxv1.Add(self.pwdText, 0, wx.EXPAND | wx.ALL,2)

        self.ButtonC = wx.Button(self.LeftPanel, -1, "确认连接")
        self.Bind(wx.EVT_BUTTON, self.ButtonConclick, self.ButtonC)
        self.Boxv1.Add(self.ButtonC, 0, wx.EXPAND | wx.ALL, 5)


        self.Labellamp = wx.StaticText(self.LeftPanel, -1, "灯管理")
        self.Labellamp.SetForegroundColour('white')
        self.Labellamp.SetBackgroundColour('black')
        self.Boxv1.Add(self.Labellamp, 0, wx.ALIGN_CENTRE, 5)
        #创建树表控件
        self.tree = gizmos.TreeListCtrl(self.LeftPanel,-1)
        #添加树表的列
        self.tree.AddColumn("灯名")
        self.tree.AddColumn("灯状态")
        # self.tree.SetColumnWidth(0,186)
        self.root = self.tree.AddRoot("灯")
        self.tree.Expand(self.root)
        self.Boxv1.Add(self.tree, 0, wx.EXPAND | wx.ALL, 5)
        self.lamp = []

        child1 = self.tree.AppendItem(self.root, "led1")  # 添加一行
        self.tree.SetItemText(child1, "led1", 0)  # 按照索引设置每一列的数据
        self.tree.SetItemText(child1, "关闭", 1)  # 按照索引设置每一列的数据
        self.tree.Expand(self.root)
        self.lamp.append(child1)
        child2 = self.tree.AppendItem(self.root, "led2")  # 添加一行
        self.tree.SetItemText(child2, "led2", 0)  # 按照索引设置每一列的数据
        self.tree.SetItemText(child2, "关闭", 1)  # 按照索引设置每一列的数据
        self.tree.Expand(self.root)
        self.lamp.append(child2)

        #添加灯管理
        self.Label3 = wx.StaticText(self.LeftPanel, -1, "添加灯：")
        self.lampText1 = wx.TextCtrl(self.LeftPanel, -1, "", pos=(80, 10), size=(150, -1))
        self.lampText1.SetInsertionPoint(0)  # 设置焦点位置
        self.Boxv1.Add(self.Label3, 0, wx.EXPAND | wx.ALL, 0)
        self.Boxv1.Add(self.lampText1, 0, wx.EXPAND | wx.ALL, 0)
        self.ButtonD = wx.Button(self.LeftPanel, -1, "确认")
        self.Bind(wx.EVT_BUTTON, self.ButtonDonclick, self.ButtonD)
        self.Boxv1.Add(self.ButtonD, 0, wx.EXPAND | wx.ALL, 5)

        # 添加灯管理
        self.Label4 = wx.StaticText(self.LeftPanel, -1, "删除灯：")
        self.lampText2 = wx.TextCtrl(self.LeftPanel, -1, "", pos=(80, 10), size=(150, -1))
        self.lampText2.SetInsertionPoint(0)  # 设置焦点位置
        self.Boxv1.Add(self.Label4, 0, wx.EXPAND | wx.ALL, 0)
        self.Boxv1.Add(self.lampText2, 0, wx.EXPAND | wx.ALL, 0)
        self.ButtonF = wx.Button(self.LeftPanel, -1, "确认")
        self.Bind(wx.EVT_BUTTON, self.ButtonFonclick, self.ButtonF)
        self.Boxv1.Add(self.ButtonF, 0, wx.EXPAND | wx.ALL, 5)

        self.logLabel = wx.StaticText(self.LeftPanel, -1, "日志")
        self.logLabel.SetForegroundColour('white')
        self.logLabel.SetBackgroundColour('black')
        self.Boxv1.Add(self.logLabel,0, wx.ALIGN_CENTRE, 10)
        # 创建文本域
        self.logmultiText = wx.TextCtrl(self.LeftPanel, -1, style=wx.TE_MULTILINE)  # 创建一个文本控件
        self.logmultiText.SetInsertionPoint(0)  # 设置插入点
        #  在垂直盒子里添加StaticBoxSizer盒子
        self.Boxv1.Add(self.logmultiText,5, wx.EXPAND | wx.ALL, 10)

        #把垂直盒子与LeftPanel关联起来
        self.LeftPanel.SetSizer(self.Boxv1)

    def ButtonDonclick(self,event):
        lampname = self.lampText1.GetValue()
        zhmodel = re.compile(u'[\u4e00-\u9fa5]')  # 检查中文
        if(lampname):
            match = zhmodel.search(lampname)
            if match:
                self.logmultiText.write('添加：' +  '名字含有中文字符' + "\n")
                return
            for i in self.lamp:
                if (self.tree.GetItemText(i, 0) == lampname):
                    self.logmultiText.write('添加：' + lampname + '重复' + "\n")
                    return
            child = self.tree.AppendItem(self.root,lampname)  # 添加一行
            self.tree.SetItemText(child,lampname, 0)  # 按照索引设置每一列的数据
            self.tree.SetItemText(child, "关闭", 1)  # 按照索引设置每一列的数据
            self.tree.Expand(self.root)
            self.lamp.append(child)
            self.logmultiText.write('添加：' + lampname + '成功'+"\n")
            return
        self.logmultiText.write('添加：内容为空' + "\n")
    def ButtonFonclick(self, event):
        lampname = self.lampText2.GetValue()
        if (lampname):
            for i in self.lamp:
                if (self.tree.GetItemText(i,0)==lampname):
                    self.tree.Delete(i)
                    self.logmultiText.write('删除: '+ lampname +  '成功' + "\n")
                    self.lamp.remove(i)
                    return
            self.logmultiText.write('删除：'+lampname+"不存在"+"\n")
            return
        self.logmultiText.write('删除：内容为空' + "\n")
    def ButtonConclick(self,event):
        ip = self.inputText.GetValue()
        if(ip == ''):
            self.logmultiText.write('连接：ip内容为空' + "\n")
            return
        #验证服务器ip
        if re.match(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$", ip):
            self.logmultiText.write('连接：ip有效' + "\n")
        else:
            self.logmultiText.write('连接：ip无效' + "\n")
            return
        port = self.pwdText.GetValue()

        # 验证端口
        if (port== ''):
            self.logmultiText.write('连接：port内容为空' + "\n")
            return
        if re.match(r"^[1-9]$|(^[1-9][0-9]$)|(^[1-9][0-9][0-9]$)|(^[1-9][0-9][0-9][0-9]$)|(^[1-6][0-5][0-5][0-3][0-5]$)", port):
            port = int(port)
            self.logmultiText.write('连接：port有效' + "\n")
        else:
            self.logmultiText.write('连接：port无效' + "\n")
            return
        self.password = (ip,port)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.s.connect(self.password)
            self.logmultiText.write('连接：' +  str(self.password) + "成功"+ "\n")
        except ConnectionRefusedError as e:
            self.logmultiText.write('连接：' +str(e) + "\n")
            self.s = None
    def Init_Right(self):
        # 创建一个wx.StaticBox对象
        # 声明一个wx.StaticBoxSizer与创建的wx.StaticBox对象作为其参数
        nm1 = wx.StaticBox(self.RightPanel, -1)
        nmSizer1 = wx.StaticBoxSizer(nm1, wx.VERTICAL)
        # 创建文本域
        self.multiText3 = wx.TextCtrl(self.RightPanel, -1, style=wx.TE_MULTILINE)  # 创建一个文本控件
        self.multiText3.SetInsertionPoint(0)  # 设置插入点
        nmSizer1.Add(self.multiText3, 1, wx.EXPAND | wx.ALL, 10)
        #  在垂直盒子里添加StaticBoxSizer盒子
        self.Boxv2.Add(nmSizer1, 10, wx.EXPAND | wx.ALL, 10)

        self.text1 = wx.StaticText(self.RightPanel, label="消息内容：", style=wx.ALIGN_CENTER)
        self.Boxh2.Add(self.text1, 1, wx.ALIGN_LEFT, 10)


        self.input = wx.TextCtrl(self.RightPanel, -1)
        self.Boxh2.Add(self.input,5, wx.ALIGN_LEFT, 10)

        self.Button2 = wx.Button(self.RightPanel, -1, "发送信息")
        self.Boxh2.Add(self.Button2, 1, wx.ALIGN_LEFT, 10)
        self.Bind(wx.EVT_BUTTON, self.Button2onclick,self.Button2)

        self.Boxv2.Add(self.Boxh2,1, wx.ALL | wx.EXPAND)

        self.text1 = wx.StaticText(self.RightPanel, label="消息格式：灯名:控制命令;例如：led1:1、lamp1:0", style=wx.ALIGN_CENTER)
        self.Boxv2.Add(self.text1, 1, wx.ALL | wx.EXPAND)
        # 把垂直盒子与RightPanel关联起来
        self.RightPanel.SetSizer(self.Boxv2)

    def Button2onclick(self,event):
        if(self.s):
            content = self.input.GetValue()
            if(self.s and content):
                ledinfo = content.split(":")
                if(len(ledinfo)<2):
                    self.logmultiText.write("发送：" + "数据无效" + "\n")
                    return
                if(ledinfo[1] == "1" or ledinfo[1] == "0" ):
                    # self.input.Clear()
                    for i in self.lamp:
                        print(self.tree.GetItemText(i,0))
                        if (self.tree.GetItemText(i,0)==ledinfo[0]):
                            content1 = str("客户端") + "：" + content + "\n"
                            self.multiText3.write(content1)
                            try:
                                self.s.send(content.encode('utf-8'))
                                self.logmultiText.write("发送：" + content + "\n")
                                reponse = self.s.recv(1024).decode('utf-8')
                                self.multiText3.write("服务端："+reponse + "\n")
                                self.logmultiText.write("接收：" + reponse + "\n")
                                # print(reponse)
                                result = re.match('^(\S+)\s+(\S+)$', reponse)
                                print(result.group(1))
                                print(result.group(2))
                                if(result.group(1).lower() == ledinfo[0]):
                                    if(result.group(2)=="on"):
                                        self.tree.SetItemText(i, "开启", 1)
                                    elif(result.group(2)=="off"):
                                        self.tree.SetItemText(i, "关闭", 1)
                            except ConnectionResetError as e:
                                self.logmultiText.write('连接：' + str(e) + "\n")
                            return
                    self.logmultiText.write("警告：" + ledinfo[0] + "不存在" + "\n")
                    return
                else:
                    self.logmultiText.write("发送：" + "数据无效" + "\n")
        else:
            self.logmultiText.write("连接：" + "还未连接服务器，不能发送信息" + "\n")

app = wx.App()
Example(None, title='LED控制客户端')
app.MainLoop()

