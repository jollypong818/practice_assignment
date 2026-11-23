"""비즈니스 오류는 키·SQL·원문을 메시지에 포함하지 않습니다."""
class DomainError(Exception):
    def __init__(self,status:int,code:str,message:str):
        self.status,self.code,self.message=status,code,message
        super().__init__(message)
