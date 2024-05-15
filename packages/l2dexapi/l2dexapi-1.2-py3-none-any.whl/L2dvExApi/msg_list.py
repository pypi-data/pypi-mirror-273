Msg_list = [
    {
        "name": "RegisterModelEventListener",
        "code": 10000
    },
    {
        "name": "UnregisterModelEventListener",
        "code": 10001
    },
    {
        "name": "OnModelEvent",
        "code": 10002
    },
    {
        "name": "ShowTextBubble",
        "code": 11000
    },
    {
        "name": "SetBackground",
        "code": 12000
    },
    {
        "name": "SetBackgroundV2",
        "code": 12010
    },
    {
        "name": "Set360Background",
        "code": 12100
    },
    {
        "name": "Set360BackgroundV2",
        "code": 12110
    },
    {
        "name": "SetModel",
        "code": 13000
    },
    {
        "name": "RemoveModel",
        "code": 13100
    },
    {
        "name": "StartMotion",
        "code": 13200
    },
    {
        "name": "SetExpression",
        "code": 13300
    },
    {
        "name": "NextExpression",
        "code": 13301
    },
    {
        "name": "ClearExpression",
        "code": 13302
    },
    {
        "name": "SetPosition",
        "code": 13400
    },
    {
        "name": "SetEffect",
        "code": 14000
    },
    {
        "name": "AddEffect",
        "code": 14100
    },
    {
        "name": "RemoveEffect",
        "code": 14200
    },
    {
        "name": "SyncResourceMonitor",
        "code": 20000
    }
]

Msg_name_to_code = {msg["name"]:msg["code"] for msg in Msg_list}
Msg_code_to_name = {msg["code"]:msg["name"] for msg in Msg_list}