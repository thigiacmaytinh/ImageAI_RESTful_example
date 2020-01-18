from rest_framework.response import Response

ERROR_CODE = 399
SUCCESS_CODE = 200

def IsValidParameter(param):
    return (param != None and param != "")

def IsInvalidParameter(param):
    result = True if not IsValidParameter() else False
    return result

def StringEmpty(mystring):
    return IsInvalidParameter(mystring)

def CreateRespond(msg, success):
    resCode = SUCCESS_CODE if success else ERROR_CODE
    resStt = 'Success' if success else 'Error'
    return Response(
            {resStt : msg},
            status=resCode,
            content_type="application/json"
            )
            
def Error(msg):
    CreateRespond(msg,True)

def Success(msg):
    CreateRespond(msg,False)

def StrToInt(_str):
    if(_str == None or _str == ""):
        return 0
    return int(_str)