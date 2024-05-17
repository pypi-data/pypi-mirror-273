import uiautomation as uia

class WinElement:
    @staticmethod
    def findElementByTd(tdTargetStr: str = None, anchorsElement: uia.Control = None, searchDelay: int = 10000, continueOnError: bool = False):
        """
        依据tdrpa拾取器获取的元素特征码查找元素

        WinElement.findElementByTd('', anchorsElement=None, searchDelay=10000, continueOnError=False)

        :param tdTargetStr: 目标元素特征码(tdrpa拾取器获取)
        :param anchorsElement: 从哪个元素开始找，不传则从桌面顶级元素开始找（有值可提高查找速度）
        :param searchDelay: 查找延时（豪秒）。默认10000
        :param continueOnError: 错误继续执行。默认False
        :return: 目标元素 or None
        """
    @staticmethod
    def getChildren(target: str | uia.Control, searchType: str = 'all', searchDelay: int = 10000, anchorsElement: uia.Control = None, continueOnError: bool = False, delayAfter: int = 100, delayBefore: int = 100) -> list | uia.Control:
        '''
        获取子元素

        WinElement.getChildren(target, searchType=\'all\', searchDelay=10000, anchorsElement=None, continueOnError=False, delayAfter=100, delayBefore=100)

        :param target: [必选参数]拾取器获取的目标元素特征字符串或目标元素对象(指定被获取子元素的根节点元素)
        :param searchType: [可选参数]搜索方式。全部子元素:"all" 首个子元素:"first" 最后一个子元素:"last"。默认"all"
        :param searchDelay: [可选参数]超时时间(毫秒)。默认10000
        :param anchorsElement: [可选参数]锚点元素，从它开始找，不传则从桌面顶级元素开始找（有值可提高查找速度）。默认None
        :param continueOnError: [可选参数]错误继续执行。默认False
        :param delayAfter: [可选参数]执行后延时(毫秒)。默认100
        :param delayBefore: [可选参数]执行前延时(毫秒)。默认100
        :return: 目标元素对象的子元素列表 或 首个子元素 或 最后一个子元素
        '''
    @staticmethod
    def getParent(target: str | uia.Control, searchDelay: int = 10000, anchorsElement: uia.Control = None, searchTop: bool = False, continueOnError: bool = False, delayAfter: int = 100, delayBefore: int = 100) -> uia.Control:
        """
        获取父元素

        WinElement.getParent(target, searchDelay=10000, anchorsElement=None, searchTop=False, continueOnError=False, delayAfter=100, delayBefore=100)

        :param target: [必选参数]拾取器获取的目标元素特征字符串或目标元素对象
        :param searchDelay: [可选参数]超时时间(毫秒)。默认10000
        :param anchorsElement: [可选参数]锚点元素，从它开始找，不传则从桌面顶级元素开始找（有值可提高查找速度）。默认None
        :param searchTop: [可选参数]是否搜索顶级父元素。搜索临近一层的父元素:False 搜索顶级的父元素:True。默认False
        :param continueOnError: [可选参数]错误继续执行。默认False
        :param delayAfter: [可选参数]执行后延时(毫秒)。默认100
        :param delayBefore: [可选参数]执行前延时(毫秒)。默认100
        :return: 目标元素对象的上一层父级元素 或 顶层父级元素
        """
    @staticmethod
    def getSibling(target: str | uia.Control, position: str = 'next', searchDelay: int = 10000, anchorsElement: uia.Control = None, continueOnError: bool = False, delayAfter: int = 100, delayBefore: int = 100) -> uia.Control | None:
        '''
        获取相邻元素

        WinElement.getSibling(target, position="next", searchDelay=10000, anchorsElement=None, continueOnError=False, delayAfter=100, delayBefore=100)

        :param target: [必选参数]拾取器获取的目标元素特征字符串或目标元素对象
        :param position: [可选参数]相邻位置。下一个："next"  上一个："previous"。默认"next"
        :param searchDelay: [可选参数]超时时间(毫秒)。默认10000
        :param anchorsElement: [可选参数]锚点元素，从它开始找，不传则从桌面顶级元素开始找（有值可提高查找速度）。默认None
        :param continueOnError: [可选参数]错误继续执行。默认False
        :param delayAfter: [可选参数]执行后延时(毫秒)。默认100
        :param delayBefore: [可选参数]执行前延时(毫秒)。默认100
        :return: 目标元素对象的下一个相邻元素对象 或 上一个相邻元素对象，没有返回None
        '''
    @staticmethod
    def exists(target: str | uia.Control, anchorsElement: uia.Control = None, continueOnError: bool = False, delayAfter: int = 100, delayBefore: int = 100) -> bool:
        """
        判断元素是否存在

        WinElement.exists(target, anchorsElement=None, continueOnError=False, delayAfter=100, delayBefore=100)

        :param target: [必选参数]拾取器获取的目标元素特征字符串或目标元素对象
        :param anchorsElement: [可选参数]锚点元素，从它开始找，不传则从桌面顶级元素开始找（有值可提高查找速度）。默认None
        :param continueOnError: [可选参数]错误继续执行。默认False
        :param delayAfter: [可选参数]执行后延时(毫秒)。默认100
        :param delayBefore: [可选参数]执行前延时(毫秒)。默认100
        :return: bool
        """
    @staticmethod
    def getCheck(target: str | uia.Control, searchDelay: int = 10000, anchorsElement: uia.Control = None, continueOnError: bool = False, delayAfter: int = 100, delayBefore: int = 100) -> bool:
        """
        获取元素勾选

        WinElement.getCheck(target, searchDelay=10000, anchorsElement=None, continueOnError=False, delayAfter=100, delayBefore=100)

        :param target: [必选参数]拾取器获取的目标元素特征字符串或目标元素对象
        :param searchDelay: [可选参数]超时时间(毫秒)。默认10000
        :param anchorsElement: [可选参数]锚点元素，从它开始找，不传则从桌面顶级元素开始找（有值可提高查找速度）。默认None
        :param continueOnError: [可选参数]错误继续执行。默认False
        :param delayAfter: [可选参数]执行后延时(毫秒)。默认100
        :param delayBefore: [可选参数]执行前延时(毫秒)。默认100
        :return: bool
        """
    @staticmethod
    def setCheck(target: str | uia.Control, searchDelay: int = 10000, isCheck: bool = True, anchorsElement: uia.Control = None, continueOnError: bool = False, delayAfter: int = 100, delayBefore: int = 100) -> None:
        """
        设置元素勾选

        WinElement.setCheck(target, searchDelay=10000, isCheck=True, anchorsElement=None, continueOnError=False, delayAfter=100, delayBefore=100)

        :param target: [必选参数]拾取器获取的目标元素特征字符串或目标元素对象
        :param searchDelay: [可选参数]超时时间(毫秒)。默认10000
        :param isCheck: [可选参数]设置勾选:True 设置取消勾选:False。默认True
        :param anchorsElement: [可选参数]锚点元素，从它开始找，不传则从桌面顶级元素开始找（有值可提高查找速度）。默认None
        :param continueOnError: [可选参数]错误继续执行。默认False
        :param delayAfter: [可选参数]执行后延时(毫秒)。默认100
        :param delayBefore: [可选参数]执行前延时(毫秒)。默认100
        :return: None
        """
    @staticmethod
    def getSelect(target: str | uia.Control, searchDelay: int = 10000, mode: str = 'text', anchorsElement: uia.Control = None, continueOnError: bool = False, delayAfter: int = 100, delayBefore: int = 100) -> str | int:
        '''
        获取元素选择

        WinElement.getSelect(target, searchDelay=10000, mode=\'text\', anchorsElement=None, continueOnError=False, delayAfter=100, delayBefore=100)

        :param target: [必选参数]拾取器获取的目标元素特征字符串或目标元素对象
        :param searchDelay: [可选参数]超时时间(毫秒)。默认10000
        :param mode: [可选参数]获取文本："text" 获取序号：“index” 获取值：“value”。默认"text"
        :param anchorsElement: [可选参数]锚点元素，从它开始找，不传则从桌面顶级元素开始找（有值可提高查找速度）。默认None
        :param continueOnError: [可选参数]错误继续执行。默认False
        :param delayAfter: [可选参数]执行后延时(毫秒)。默认100
        :param delayBefore: [可选参数]执行前延时(毫秒)。默认100
        :return: 已选项的文本 或 序号 或 值，没有则返回None
        '''
    @staticmethod
    def setSelect(target: str | uia.Control, option: str | int, searchDelay: int = 10000, mode: str = 'text', anchorsElement: uia.Control = None, continueOnError: bool = False, delayAfter: int = 100, delayBefore: int = 100, setForeground: bool = True, cursorPosition: str = 'center', cursorOffsetX: int = 0, cursorOffsetY: int = 0, simulateType: str = 'simulate') -> None:
        '''
        设置元素选择

        WinElement.setSelect(target, \'\', searchDelay=10000, mode="text", anchorsElement=None, continueOnError=False, delayAfter=100, delayBefore=100, setForeground=True, cursorPosition=\'center\', cursorOffsetX=0, cursorOffsetY=0, simulateType=\'simulate\')

        :param target: [必选参数]拾取器获取的目标元素特征字符串或目标元素对象
        :param option: [必选参数]选择选项
        :param searchDelay: [可选参数]超时时间(毫秒)。默认10000
        :param mode: [可选参数]选择文本："text" 选择序号：“index” 选择值：“value”。默认"text"
        :param anchorsElement: [可选参数]锚点元素，从它开始找，不传则从桌面顶级元素开始找（有值可提高查找速度）。默认None
        :param continueOnError: [可选参数]错误继续执行。默认False
        :param delayAfter: [可选参数]执行后延时(毫秒)。默认100
        :param delayBefore: [可选参数]执行前延时(毫秒)。默认100
        :param setForeground: [可选参数]激活窗口。默认True
        :param cursorPosition: [可选参数]光标位置。中心:"center" 左上角:"topLeft" 右上角:"topRight" 左下角:"bottomLeft" 右下角:"bottomRight"。默认"center"
        :param cursorOffsetX: [可选参数]横坐标偏移。默认0
        :param cursorOffsetY: [可选参数]纵坐标偏移。默认0
        :param simulateType: [可选参数]鼠标点击选中项时的模式。模拟操作:"simulate" 消息操作:"message"。默认"simulate"
        :return: None
        '''
    @staticmethod
    def getValue(target: str | uia.Control, getMethod: str = 'auto', searchDelay: int = 10000, anchorsElement: uia.Control = None, continueOnError: bool = False, delayAfter: int = 100, delayBefore: int = 100) -> str:
        '''
        获取元素文本

        WinElement.getValue(target, getMethod="auto", searchDelay=10000, anchorsElement=None, continueOnError=False, delayAfter=100, delayBefore=100)

        :param target: [必选参数]拾取器获取的目标元素特征字符串或目标元素对象
        :param getMethod: [可选参数]获取方式。自动方式："auto" 搜元素Name方式："name" 搜元素Value方式："value"。默认"auto"
        :param searchDelay: [可选参数]超时时间(毫秒)。默认10000
        :param anchorsElement: [可选参数]锚点元素，从它开始找，不传则从桌面顶级元素开始找（有值可提高查找速度）。默认None
        :param continueOnError: [可选参数]错误继续执行。默认False
        :param delayAfter: [可选参数]执行后延时(毫秒)。默认100
        :param delayBefore: [可选参数]执行前延时(毫秒)。默认100
        :return: 元素文本
        '''
    @staticmethod
    def setValue(target: str | uia.Control, value: str, searchDelay: int = 10000, anchorsElement: uia.Control = None, continueOnError: bool = False, delayAfter: int = 100, delayBefore: int = 100) -> None:
        '''
        设置元素文本

        WinElement.setValue(target, "", searchDelay=10000, anchorsElement=None, continueOnError=False, delayAfter=100, delayBefore=100)

        :param target: [必选参数]拾取器获取的目标元素特征字符串或目标元素对象
        :param value: [必选参数]待写入UI界面元素的文本内容
        :param searchDelay: [可选参数]超时时间(毫秒)。默认10000
        :param anchorsElement: [可选参数]锚点元素，从它开始找，不传则从桌面顶级元素开始找（有值可提高查找速度）。默认None
        :param continueOnError: [可选参数]错误继续执行。默认False
        :param delayAfter: [可选参数]执行后延时(毫秒)。默认100
        :param delayBefore: [可选参数]执行前延时(毫秒)。默认100
        :return: None
        '''
    @staticmethod
    def getRect(target: str | uia.Control, relativeType: str = 'parent', searchDelay: int = 10000, anchorsElement: uia.Control = None, continueOnError: bool = False, delayAfter: int = 100, delayBefore: int = 100) -> dict:
        '''
        获取元素区域

        WinElement.getRect(target, relativeType="parent", searchDelay=10000, anchorsElement=None, continueOnError=False, delayAfter=100, delayBefore=100)

        :param target: [必选参数]拾取器获取的目标元素特征字符串或目标元素对象
        :param relativeType: [可选参数]返回元素位置是相对于哪一个坐标而言的。 相对父元素:"parent" 相对窗口客户区:"root" 相对屏幕坐标:"screen"。默认"parent"
        :param searchDelay: [可选参数]超时时间(毫秒)。默认10000
        :param anchorsElement: [可选参数]锚点元素，从它开始找，不传则从桌面顶级元素开始找（有值可提高查找速度）。默认None
        :param continueOnError: [可选参数]错误继续执行。默认False
        :param delayAfter: [可选参数]执行后延时(毫秒)。默认100
        :param delayBefore: [可选参数]执行前延时(毫秒)。默认100
        :return: {"height" : int, "width" : int, "x" : int, "y" : int}
        '''
    @staticmethod
    def screenCapture(target: str | uia.Control, filePath: str, rect: dict = None, searchDelay: int = 10000, anchorsElement: uia.Control = None, continueOnError: bool = False, delayAfter: int = 100, delayBefore: int = 100) -> bool:
        '''
        元素截图

        WinElement.screenCapture(target, \'D:/1.png\', rect=None, searchDelay=10000, anchorsElement=None, continueOnError=False, delayAfter=100, delayBefore=100)

        :param target: [必选参数]拾取器获取的目标元素特征字符串或目标元素对象
        :param filePath: [必选参数]图片存储的绝对路径。如 \'D:/1.png\'(支持图片保存格式：bmp、jpg、jpeg、png、gif、tif、tiff)
        :param rect: [可选参数]对指定界面元素截图的范围，若传None，则截取该元素的全区域。若传{"x":int,"y":int,"width":int,"height":int}，则以该元素左上角位置偏移x,y的坐标为原点，根据高宽进行截图。默认None
        :param searchDelay: [可选参数]超时时间(毫秒)。默认10000
        :param anchorsElement: [可选参数]锚点元素，从它开始找，不传则从桌面顶级元素开始找（有值可提高查找速度）。默认None
        :param continueOnError: [可选参数]错误继续执行。默认False
        :param delayAfter: [可选参数]执行后延时(毫秒)。默认100
        :param delayBefore: [可选参数]执行前延时(毫秒)。默认100
        :return: bool(截图成功返回True，否则返回假)
        '''
    @staticmethod
    def wait(target: str | uia.Control, waitType: str = 'show', searchDelay: int = 10000, anchorsElement: uia.Control = None, continueOnError: bool = False, delayAfter: int = 100, delayBefore: int = 100) -> None:
        '''
        等待元素（等待元素显示或消失）

        WinElement.wait(target, waitType=\'show\', searchDelay=10000, anchorsElement=None, continueOnError=False, delayAfter=100, delayBefore=100)

        :param target: [必选参数]拾取器获取的目标元素特征字符串或目标元素对象
        :param waitType: [可选参数]等待方式。 等待显示："show" 等待消失:"hide"。默认"show"
        :param searchDelay: [可选参数]超时时间(毫秒)。默认10000
        :param anchorsElement: [可选参数]锚点元素，从它开始找，不传则从桌面顶级元素开始找（有值可提高查找速度）。默认None
        :param continueOnError: [可选参数]错误继续执行。默认False
        :param delayAfter: [可选参数]执行后延时(毫秒)。默认100
        :param delayBefore: [可选参数]执行前延时(毫秒)。默认100
        :return: None
        '''
