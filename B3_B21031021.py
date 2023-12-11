import sys    
import json
from datetime import date
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon,QFont
from PyQt5.QtWidgets import QWidget,QApplication,QVBoxLayout,QHBoxLayout,QPushButton,QLabel,QSizePolicy,QDesktopWidget,QLineEdit,QGridLayout,QDialog,QMessageBox,QScrollArea,QSlider

def save(货物) -> None:
    '''保存货物信息到文件中'''

    json_货物=货物.copy()
    for i,goods in enumerate(json_货物):
        json_货物[i]=货物[i].copy()
        json_货物[i]["进货时间"]=goods["进货时间"].isoformat()
        json_货物[i]["过期时间"]=goods["过期时间"].isoformat()
    with open("goods.json","w",encoding="utf-8") as f:
        json.dump(json_货物,f,ensure_ascii=False)
def load() -> list:
    '''从文件中读取货物信息'''
    with open("goods.json",'r',encoding='utf-8') as f:
        货物:list=json.load(f)
    for i,goods in enumerate(货物):
        货物[i]["进货时间"]=date.fromisoformat(goods["进货时间"])
        货物[i]["过期时间"]=date.fromisoformat(goods["过期时间"])
    return 货物


class main_UI(QWidget):

    def __init__(self) -> None:
        super().__init__()

        self.initUI()
    
    def search(self,aim_str) -> list:
        '''以列表的形式返回所有含有aim_str的货物'''
        result:list=[]
        if aim_str=="":
            return result
        for goods in self.出货排序:
            if aim_str in (str(goods["品名"])+str(goods["简介"])):
                result.append(goods)
        return result

    def 进货(self,goods) -> None:
        '''将货物加入到self.出货排序中，并根据此修改其他相关属性'''
        today: date=date.today()
        self.出货排序.append(goods)
        self.过期时间排序=sorted(self.出货排序,key=lambda x:(x["过期时间"]-today).days)
        self.出货排序=sorted(self.出货排序,key=lambda x:(-(today-x["进货时间"]).days,(x["过期时间"]-today).days))
        self.即将过期货物=list(filter(lambda x:(x["过期时间"]-today).days < 10,self.过期时间排序))
        save(self.出货排序)
    
    def switch(self) -> None:
        '''根据左侧按钮列表切换界面'''
        sender:QPushButton = self.sender()
        self.hbox.itemAt(1).widget().setParent(None)
        UI_list: dict[str, QLabel]={"进货":self.UI_1,"出货":self.UI_2,"查询":self.UI_3,"过期提示":self.UI_4,"关于":self.UI_5}
        if sender.text()=="过期提示":
            self.refresh_UI_4()
        if sender.text()=="出货":
            self.refresh_UI_2()
        self.hbox.insertWidget(1, UI_list[sender.text()],3)
        for i in range(len(UI_list)):
            self.vbox.itemAt(i).widget().setStyleSheet("background-color: rgb(255, 255, 255);border:none;font-size: 30px;font-Family:KaiTi;")
        sender.setStyleSheet("background-color: rgb(238 238 239);border:none;font-size: 30px;font-Family:KaiTi;")
         
    def center(self) -> None:
        '''使窗口居中'''
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    
    def 提交(self) -> None:
        '''根据提交的信息进行进货'''
        try:
            goods={
            '品名':self.UI_1_data_edit[0].text(),
            "进货时间":date.fromisoformat(self.UI_1_data_edit[1].text()),
            "过期时间":date.fromisoformat(self.UI_1_data_edit[2].text()),
            "简介":self.UI_1_data_edit[3].text(),
            "数量":int(self.UI_1_data_edit[4].text())
            }
        except:
            错误提示=QMessageBox()
            错误提示.setText("错误的数据格式")
            错误提示.setWindowTitle("提示")
            错误提示.exec_()
            return 
        self.进货(goods)
        成功提示=QMessageBox()
        成功提示.setText("进货成功")
        成功提示.setWindowTitle("提示")
        成功提示.exec_()
        
    def ok(self) -> None:
        '''选择确认则关闭窗口并提交信息'''
        self.dialog.close()
        self.提交()
        
    def showDialog(self) -> None:
        '''展示一个提示确认保存的信息窗口'''
        vbox = QVBoxLayout()      
        hbox=QHBoxLayout()
        panel=QLabel("确定保存信息？")
        self.dialog=QDialog()
        self.dialog.resize(250,150)
        self.okBtn=QPushButton("确定")#确认键
        self.cancelBtn=QPushButton("取消")#取消键

        self.okBtn.clicked.connect(self.ok)
        self.cancelBtn.clicked.connect(self.dialog.close)

        self.dialog.setWindowTitle("提示信息！")
        hbox.addWidget(self.okBtn)
        hbox.addWidget(self.cancelBtn)
 
        vbox.addWidget(panel)
        vbox.addLayout(hbox)
        self.dialog.setLayout(vbox)
 
        self.dialog.exec_()
        self.dialog.setWindowModality(Qt.ApplicationModal)#该模式下，只有该dialog关闭，才可以关闭父界面

    def goods_search(self) -> None:
        '''实现货物搜索功能,调用search函数的结果形成展示结果的窗口(UI)'''
        sender=self.sender()
        self.result=self.search(sender.text())
        self.search_vbox.itemAt(1).widget().setParent(None)
        self.search_vbox_vbox=QVBoxLayout()
        for i in self.result:
            temp=QLabel(f'品名：{i["品名"]}\n进货时间：{i["进货时间"]}\n过期时间：{i["过期时间"]}\n简介：{i["简介"]}\n数量：{i["数量"]}\n')
            temp.setStyleSheet("background-color: rgb(255, 255, 255);font-family:KaiTi;font-size:30px")
            temp.setAlignment(Qt.AlignCenter)
            self.search_vbox_vbox.addWidget(temp)
        self.b=QWidget()
        self.search_vbox_vbox.setContentsMargins(0, 0, 0, 0)
        self.search_vbox_vbox.setSpacing(3)
        self.b.setLayout(self.search_vbox_vbox)
        self.c.setWidget(self.b)
        self.search_vbox.insertWidget(1,self.c)
        
    def number(self) -> None:
        sender:QSlider=self.sender()
        name: str=sender.objectName()
        index=int(name.strip("sld_"))
        parent=sender.parent()
        数字:QLabel=parent.findChild(QLabel,f"数字_{index}")
        数字.setText(str(sender.value()))
   
    def refresh_UI_2(self) -> None:
        for i in range(self.出货信息窗口_vbox.count()-1,-1,-1):
            obj=self.出货信息窗口_vbox.itemAt(i).widget()
            if(obj!=None):
                obj.setParent(None)
            else:
                self.出货信息窗口_vbox.itemAt(i).layout().itemAt(2).widget().setParent(None)
                self.出货信息窗口_vbox.itemAt(i).layout().itemAt(1).widget().setParent(None)
                self.出货信息窗口_vbox.itemAt(i).layout().itemAt(0).widget().setParent(None)
                self.出货信息窗口_vbox.itemAt(i).layout().setParent(None)

        for index,i in enumerate(self.出货排序):
            temp=QLabel(f'\n品名：{i["品名"]}\n进货时间：{i["进货时间"]}\n过期时间：{i["过期时间"]}\n简介：{i["简介"]}\n数量：{i["数量"]}')
            进货数量=QLabel("出货数量：")
            数字=QLabel('0')
            sld = QSlider(Qt.Horizontal, self)
            temp.setStyleSheet("background-color: rgb(255, 255, 255);font-family:KaiTi;font-size:30px")
            进货数量.setStyleSheet("font-size: 30px;font-Family:KaiTi;background-color: rgb(255, 255, 255)")
            数字.setStyleSheet("font-size: 30px;font-Family:KaiTi;background-color: rgb(255, 255, 255)")
            数字.setObjectName(f"数字_{index}")
            sld.setObjectName(f"sld_{index}")
            sld.setStyleSheet('background-color: rgb(255, 255, 255);border:0px')
            sld.setContentsMargins(0,0,0,0)
            sld.setFocusPolicy(Qt.NoFocus)
            sld.setRange(0,i["数量"])
            sld.valueChanged.connect(self.number)
            滑条_hox=QHBoxLayout()
            滑条_hox.setSpacing(0)
            滑条_hox.setContentsMargins(0, 0, 0, 0)
            滑条_hox.addWidget(进货数量)
            滑条_hox.addWidget(数字)
            滑条_hox.addWidget(sld)
            self.出货信息窗口_vbox.addWidget(temp)
            self.出货信息窗口_vbox.addLayout(滑条_hox)
    
    def shipment(self) -> None:
        '''实现出货功能'''
        sender=self.sender()
        parent=sender.parent()
        for i,goods in enumerate(self.出货排序):
            sld:QSlider=parent.findChild(QSlider,f'sld_{i}')
            self.出货排序[i]["数量"]=goods["数量"]-sld.value()
        for i in range(len(self.出货排序)-1, -1, -1):
            if(self.出货排序[i]["数量"]==0):
                del self.出货排序[i]
        self.出货排序=sorted(self.出货排序,key=lambda x:(-(self.today-x["进货时间"]).days,(x["过期时间"]-self.today).days))
        self.过期时间排序=sorted(self.出货排序,key=lambda x:(x["过期时间"]-self.today).days)
        self.即将过期货物=list(filter(lambda x:(x["过期时间"]-self.today).days < 10,self.过期时间排序))
        save(self.出货排序)
        self.refresh_UI_2()
        
    def refresh_UI_4(self) -> None:
        '''对UI_4进行更新'''
        for i in range(self.UI_4_vbox.count()-1,-1,-1):
            self.UI_4_vbox.itemAt(i).widget().setParent(None)
        for i in self.即将过期货物:
            temp=QLabel(f'品名：{i["品名"]}\n进货时间：{i["进货时间"]}\n过期时间：{i["过期时间"]}\n简介：{i["简介"]}\n数量：{i["数量"]}')
            temp.setStyleSheet("background-color: rgb(255, 255, 255);font-family:KaiTi;font-size: 30px")
            temp.setAlignment(Qt.AlignCenter)
            self.UI_4_vbox.addWidget(temp)
    
    def initialization_UI_1(self) -> None:
        '''进货按键对应UI初始化'''
        self.UI_1=QWidget()
        name_list=['品名:','进货时间:','过期时间:',"简介:",'数量:',]
        self.UI_1_data_edit=[]
        grid = QGridLayout()
        for i,name in enumerate(name_list):
            name_label=QLabel(name)
            name_label.setFont(QFont('KaiTi', 20))
            grid.addWidget(name_label,i,0,Qt.AlignCenter)
            self.UI_1_data_edit.append(QLineEdit())
            grid.addWidget(self.UI_1_data_edit[i],i,1)      
        grid.setSpacing(0)
        确认按钮=QPushButton("提交")
        确认按钮.setStyleSheet("font-size: 30px;font-Family:KaiTi;")
        确认按钮.clicked.connect(self.showDialog)
        grid.addWidget(确认按钮,6,1)
        self.UI_1.setLayout(grid)
        
    def initialization_UI_2(self) -> None:
        '''出货按键对应UI初始化'''
        self.UI_2=QWidget()
        UI_2_vbox=QVBoxLayout()
        出货按钮=QPushButton("确认出货")
        出货按钮.clicked.connect(self.shipment)
        UI_2_vbox.addWidget(出货按钮)
        出货信息窗口=QWidget()
        self.出货信息窗口_vbox=QVBoxLayout()
        self.出货信息窗口_vbox.setContentsMargins(0, 0, 0, 0)
        self.出货信息窗口_vbox.setSpacing(0)
        出货信息窗口.setLayout(self.出货信息窗口_vbox)
        sa=QScrollArea()
        sa.setWidget(出货信息窗口)
        sa.setAlignment(Qt.AlignCenter)
        sa.setWidgetResizable(True)
        sa.setStyleSheet("border:none")
        UI_2_vbox.addWidget(sa)
        UI_2_vbox.setContentsMargins(0, 0, 0, 0)
        UI_2_vbox.setSpacing(3)
        self.UI_2.setLayout(UI_2_vbox)     

    def initialization_UI_3(self) -> None:
        '''查询按键对应UI初始化'''
        self.c=QScrollArea()
        self.UI_3=QWidget()
        self.search_vbox=QVBoxLayout()
        self.result=[]
        search_edit=QLineEdit()
        search_edit.textChanged.connect(self.goods_search)
        search_edit.setPlaceholderText("输入以开始搜索")
        self.search_vbox.addWidget(search_edit)
        self.b=QWidget()
        self.c.setMinimumSize(300,300)
        self.c.setAlignment(Qt.AlignCenter)
        self.c.setWidgetResizable(True)
        self.c.setStyleSheet("border:none")
        self.search_vbox.addWidget(self.c)
        self.search_vbox.setContentsMargins(0, 0, 0, 0)
        self.search_vbox.setSpacing(0)
        self.c.setWidget(self.b)
        self.UI_3.setLayout(self.search_vbox)

    def initialization_UI_4(self) -> None:
        '''过期提醒界面初始化'''
        self.UI_4=QScrollArea()
        self.UI_4.setStyleSheet("border:none")
        self.UI_4.setAlignment(Qt.AlignCenter)
        self.UI_4.setWidgetResizable(True)
        self.UI_4.setMinimumSize(600,400)
        a=QWidget()
        self.UI_4_vbox=QVBoxLayout()
        self.UI_4_vbox.setContentsMargins(0, 0, 0, 0)
        self.UI_4_vbox.setSpacing(3)
        a.setLayout(self.UI_4_vbox)
        self.UI_4.setWidget(a)      
    
    def initialization_UI_5(self) -> None:
        '''关于界面（UI_5)初始化'''
        self.UI_5=QLabel("小杨出品，必属寄品\nB21031021")
        self.UI_5.setStyleSheet("background-color: rgb(255, 255, 255);font-size:40px;font-family:KaiTi")
        self.UI_5.setAlignment(Qt.AlignCenter)
          
    def initUI(self) -> None:  
        '''初始化主UI'''    
        self.vbox=QVBoxLayout()
        self.hbox=QHBoxLayout()
        h: int=QDesktopWidget().availableGeometry().height()
        w: int=QDesktopWidget().availableGeometry().width()
        self.resize(int(w/2), int(h/2))
        self.center()
        self.today: date=date.today()
        self.货物=load()
        self.出货排序=sorted(self.货物,key=lambda x:(-(self.today-x["进货时间"]).days,(x["过期时间"]-self.today).days))
        self.过期时间排序=sorted(self.出货排序,key=lambda x:(x["过期时间"]-self.today).days)
        self.即将过期货物=list(filter(lambda x:(x["过期时间"]-self.today).days < 10,self.过期时间排序))
        
        
        #-----初始化UI_1到UI_5--------
        self.initialization_UI_1()   
        self.initialization_UI_2()  
        self.initialization_UI_3()
        self.initialization_UI_4()   
        self.initialization_UI_5()
        
        #----------左侧按键栏------------
        for i in ["进货","出货","查询","过期提示","关于"]:
            btn=QPushButton(i,self)
            btn.clicked.connect(self.switch)
            btn.setStyleSheet("background-color: rgb(255, 255, 255);border:none;font-size: 30px;font-Family:KaiTi;")
            if i=="进货":
                btn.setStyleSheet("background-color: rgb(238 238 239);border:none;font-size: 30px;font-Family:KaiTi;")
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.vbox.addWidget(btn)  
        self.vbox.setSpacing(0)
        self.hbox.setSpacing(3)
        self.hbox.setContentsMargins(0, 0, 0, 0)
        self.hbox.addLayout(self.vbox,1)
        self.hbox.addWidget(self.UI_1,3)

        #----------主窗口-------------
        self.setLayout(self.hbox)
        self.setWindowIcon(QIcon("head_img.jpg"))
        self.setWindowTitle('电子商务进货系统')
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = main_UI()
    sys.exit(app.exec_())