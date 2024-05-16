from .ApiList import Msg_name_to_code
import websocket, json

class WebSocket:

    def __init__(self,url:str=None,**options) -> None:
        self.ws = websocket.WebSocket()
        self.url = url
        self.connect_options = options
        self.msgid = 1
    
    def __enter__(self):
        self.connect()
        return self
    
    def __exit__(self,exc_type,exc_val,exc_tb):
        self.close()
        
    def connect(self,url:str=None,**options) -> None:
        if url:
            self.url = url
        if options:
            self.connect_options = options
        return self.ws.connect(self.url,**self.connect_options)
    
    def send(self,data:str) -> None:
        return self.ws.send(data)
    
    def recv(self) -> str:
        return self.ws.recv()
    
    def close(self) -> None:
        return self.ws.close()
    
    def _command(self,msg:int,in_data=None) -> int:
        msgid = self.msgid
        self.msgid += 1
        data = {
            "msg": msg,
            "msgId": msgid,
        }
        if in_data:
            data["data"] = in_data
        self.send(json.dumps(data,ensure_ascii=False))
        return msgid
    
    def get(self) -> dict:
        if self.ws.connected:
            return json.loads(self.recv())
        
    def RegisterModelEventListener(self) -> int:
        """注册模型事件监听

        Returns:
            int: msgid
        """
        return self._command(Msg_name_to_code["RegisterModelEventListener"])
    
    def UnregisterModelEventListener(self) -> int:
        """取消注册模型事件监听

        Returns:
            int: msgid
        """
        return self._command(Msg_name_to_code["UnregisterModelEventListener"])
    
    def ShowTextBubble(
        self,
        modelID:int,
        text:str,
        choices:list[str]=[],
        textFrameColor:int = 0x000000,
        textColor:int = 0xFFFFFF,
        duration:int = 3000,
        ) -> int:
        """显示气泡文本

        Args:
            modelID (int): 模型序号，从0开始，即模型#1的序号是0
            text (str): 要显示的文本[支持的标签: Rich Text]
            choices (list[str], optional): 按钮选项
            textFrameColor (int, optional): 文本框颜色，RGB整形值（如0xFFFFFF）。Defaults to 0x000000.
            textColor (int, optional): 文本颜色，RGB整形值（如0xFFFFFF）。Defaults to 0xFFFFFF.
            duration (int, optional): 显示时长，单位为毫秒,若为-1，气泡将不会自动消失。Defaults to 3000.

        Returns:
            int: msgid
        """
        return self._command(
            Msg_name_to_code["ShowTextBubble"],
            {
                "id": modelID,
                "text": text,
                "choices": choices,
                "textFrameColor": textFrameColor,
                "textColor": textColor,
                "duration": duration
            } 
        )
        
    def SetBackgroundV2(self,displayID:int,image:str) -> int:
        """
        设置普通背景

        Args:
            displayID (int): 显示器序号，从0开始，即显示器#1的序号是0
            image (str): 背景文件路径

        Returns:
            int: msgid
        """
        return self._command(
            Msg_name_to_code["SetBackgroundV2"],
            {
                "id": displayID,
                "file": image
            }
        )
    
    def Set360BackgroundV2(self,displayID:int,image:str) -> int:
        """
        设置360全景背景

        Args:
            displayID (int): 显示器序号，从0开始，即显示器#1的序号是0
            image (str): 背景文件路径

        Returns:
            int: msgid
        """
        return self._command(
            Msg_name_to_code["Set360BackgroundV2"],
            {
                "id": displayID,
                "file": image
            }
        )
    
    def SetModel(self,modelID:int,file_path:str) -> int:
        """
        设置模型，目前仅支持json模型

        Args:
            displayID (int): 模型序号，从0开始，即模型#1的序号是0
            image (str): *.model.json文件路径

        Returns:
            int: msgid
        """
        return self._command(
            Msg_name_to_code["SetModel"],
            {
                "id": modelID,
                "file": file_path
            }
        )
    
    def RemoveModel(self,modelID:int) -> int:
        """
        移除模型

        Args:
            displayID (int): 模型序号，从0开始，即模型#1的序号是0
            image (str): *.model.json文件路径

        Returns:
            int: msgid
        """
        return self._command(
            Msg_name_to_code["RemoveModel"],
            modelID
        )
    
    def StartMotion(self,modelID:int,mtnType:int,mtn:str) -> int:
        """触发动作

        Args:
            modelID (int): 模型序号，从0开始，即模型#1的序号是0
            mtnType (int): 类型
            mtn (str): type值为0时，填写格式为 “group:motion”，例如 "tap:mtn1"※ 不指定motion时请直接写group名即可，例如 "tap"type值为1时，此处填写动作文件相对路径，例如“motion1.mtn”
        
        Returns:
            int: msgid
        """
        return self._command(
            Msg_name_to_code["StartMotion"],
            {
                "id": modelID,
                "type": mtnType,
                "mtn": mtn
            }
        )
    
    def SetExpression(self,modelID:int,expID:int) -> int:
        """
        触发表情

        Args:
            modelID (int): 模型序号，从0开始，即模型#1的序号是0
            expID (int): 表情ID
        
        Returns:
            int: msgid
        """
        return self._command(
            Msg_name_to_code["SetExpression"],
            {
                "id": modelID,
                "expId": expID
            }
        )
    
    def NextExpression(self,modelID:int) -> int:
        """下一个表情

        Args:
            modelID (int): 模型序号，从0开始，即模型#1的序号是0

        Returns:
            int: msgid
        """
        return self._command(
            Msg_name_to_code["NextExpression"],
            modelID
        )
    
    def ClearExpression(self,modelID:int) -> int:
        """
        清除表情

        Args:
            modelID (int): 模型序号，从0开始，即模型#1的序号是0

        Returns:
            int: msgid
        """
        return self._command(
            Msg_name_to_code["ClearExpression"],
            modelID
        )
    
    def SetPosition(self,modelID:int,x:int,y:int) -> int:
        """设置位置

        Args:
            modelID (int): 模型序号，从0开始，即模型#1的序号是0
            x (int): 屏幕像素点横坐标（屏幕左下角为原点）
            y (int): 屏幕像素点纵坐标（屏幕左下角为原点）

        Returns:
            int: msgid
        """
        return self._command(
            Msg_name_to_code["SetPosition"],
            modelID
        )
    
    def SetEffect(self,effectID:int) -> int:
        """设置特效

        Args:
            effectID (int): 特效ID， 详见ID列表
                100100	雨
                100110	雪

        Returns:
            int: msgid
        """
        return self._command(
            Msg_name_to_code["SetEffect"],
            effectID
        )
    
    def AddEffect(self,effectID:int) -> int:
        """添加特效

        Args:
            effectID (int): 特效ID， 详见ID列表
                100100	雨
                100110	雪

        Returns:
            int: msgid
        """
        return self._command(
            Msg_name_to_code["AddEffect"],
            effectID
        )
        
    def RemoveEffect(self,effectID:int) -> int:
        """移除指定ID的模型，设置为-1来移除所有特效

        Args:
            effectID (int): 特效ID， 详见ID列表
                100100	雨
                100110	雪

        Returns:
            int: msgid
        """
        return self._command(
            Msg_name_to_code["RemoveEffect"],
            effectID
        )