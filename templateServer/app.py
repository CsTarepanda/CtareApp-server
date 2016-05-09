import ws
from ws import router

class Root(ws.WebSocket, ws.Root):
    BASE_URL = ws.Root.plus("sample")

@router("samplews")
class Sample(Root):
    pass
