import ws
from ws import router

class Root(ws.WebSocket, ws.Router):
    BASE_URL = ws.Router.plus("sample")

@router("samplews")
class Sample(Root):
    pass
