import uiautomation as uia

class Window:
    @staticmethod
    def close(target: str | uia.Control) -> None:
        """
        关闭窗口

        window.close(target)

        :param target: [必选参数]拾取器获取的目标元素特征字符串或目标元素对象(指定被获取子元素的根节点元素)
        :return: None
        """
    @staticmethod
    def getActive() -> uia.Control:
        """
        获取活动窗口

        window.getActive()

        :return:control
        """
    @staticmethod
    def setActive(target: str | uia.Control) -> bool:
        """
        设置活动窗口

        window.setActive(target)

        :param target: [必选参数]拾取器获取的目标元素特征字符串或目标元素对象
        :return: bool。激活成功返回True，否则返回False
        """
    @staticmethod
    def show(target: str | uia.Control, showStatus: str) -> bool:
        '''
        更改窗口显示状态

        window.show(target, "show")

        :param target: [必选参数]拾取器获取的目标元素特征字符串或目标元素对象
        :param showStatus: [必选参数] 显示：\'show\' 隐藏：\'hide\' 最大化：\'max\' 最小化：\'min\' 还原：\'restore\'
        :return: bool。执行成功返回True，否则返回False
        '''
    @staticmethod
    def exists(target: str | uia.Control) -> bool:
        """
        判断窗口是否存在

        window.exists(target)

        :param target: [必选参数]拾取器获取的目标元素特征字符串或目标元素对象
        :return: bool。窗口存在返回True,否则返回False
        """
    @staticmethod
    def getSize(target: str | uia.Control) -> dict:
        '''
        获取窗口大小

        window.getSize(target)

        :param target: [必选参数]拾取器获取的目标元素特征字符串或目标元素对象
        :return: {"height":int, "width":int, "x":int, "y":int}
        '''
    @staticmethod
    def setSize(target: str | uia.Control, width: int, height: int) -> None:
        """
        改变窗口大小

        window.setSize(target, 800, 600)

        :param target: [必选参数]拾取器获取的目标元素特征字符串或目标元素对象
        :param width: [必选参数]窗口宽度
        :param height: [必选参数]窗口高度
        :return: None
        """
    @staticmethod
    def move(target: str | uia.Control, x: int, y: int) -> None:
        """
        移动窗口位置

        window.move(target, 0, 0)

        :param target: [必选参数]拾取器获取的目标元素特征字符串或目标元素对象
        :param x: [必选参数]移动到新位置的横坐标
        :param y: [必选参数]移动到新位置的纵坐标
        :return: None
        """
    @staticmethod
    def topMost(target: str | uia.Control, isTopMost: bool = True) -> None:
        """
        窗口置顶

        window.topMost(target, isTopMost=True)

        :param target: [必选参数]拾取器获取的目标元素特征字符串或目标元素对象
        :param isTopMost: [可选参数]是否使窗口置顶，窗口置顶:true 窗口取消置顶:false。默认True
        :return: None
        """
    @staticmethod
    def getClass(target: str | uia.Control) -> str:
        """
        获取窗口类名

        window.getClass(target)

        :param target: [必选参数]拾取器获取的目标元素特征字符串或目标元素对象
        :return: 窗口的类名称
        """
    @staticmethod
    def getPath(target: str | uia.Control) -> str:
        """
        获取窗口程序的文件路径

        window.getPath(target)

        :param target: [必选参数]拾取器获取的目标元素特征字符串或目标元素对象
        :return: 文件绝对路径
        """
    @staticmethod
    def getPID(target: str | uia.Control) -> int:
        """
        获取进程PID

        window.getPID(target)

        :param target: [必选参数]拾取器获取的目标元素特征字符串或目标元素对象
        :return: PID
        """
