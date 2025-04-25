import json

webServerDAT = op('webserver1')
clientsTable = op('clientList')

def send_command_to_clients(command, target_id="all"):
    rout_dic = {
        '0': 'http://192.168.0.12/inotex/1.mp4',
        '1': 'http://192.168.0.12/inotex/2.mp4',
        '2': 'http://192.168.0.12/inotex/3.mp4',
        '3': 'http://192.168.0.12/inotex/4.mp4',
        '19': 'http://192.168.0.12/inotex/5.mp4',
        '17': 'http://192.168.0.12/inotex/6.mp4',
        '88': 'http://192.168.0.12/inotex/7.mp4',
        '9': 'http://192.168.0.12/inotex/8.mp4',
        '999': 'http://localhost/inotex/8.mp4',
    }
    if clientsTable is None:
        debug('clients_table DAT not found.')
        return

    for i in range(1, clientsTable.numRows):  # skip header
        client_id = clientsTable[i, 0].val
        if target_id == "all" :
            message = json.dumps({"type": "command", "id": "all", "action": command})
            webServerDAT.webSocketSendText(client_id, message)
        else:
            message = json.dumps({"type": "command", "id": target_id, "action": command})
            webServerDAT.webSocketSendText(client_id, message)

def send_url_command_to_clients(url, target_id="all"):
    if clientsTable is None:
        debug('clients_table DAT not found.')
        return

    for i in range(1, clientsTable.numRows):  # skip header
        client_id = clientsTable[i, 0].val
        if target_id == "all" :
            message = json.dumps({"action": "url", "url": url, "id": "all"})
            webServerDAT.webSocketSendText(client_id, message)
        else:
            message = json.dumps({"action": "url", "url": url, "id": target_id})
            webServerDAT.webSocketSendText(client_id, message)

def onCreate():
    send_command_to_clients("play")  # Example: Send 'play' command to all clients


def onStart():
    # Send to the first client (optional)
    if callbacks.clients:
        webServerDAT.webSocketSendText(callbacks.clients[0], 'Hello, first client!')
    return

def onExit():
    send_command_to_clients("pause")  # Example: Send 'play' command to all clients
    return

def onFrameStart(frame):
    send_command_to_clients("play")  # Example: Send 'play' command to all clients
    return

def onFrameEnd(frame):
    send_command_to_clients("restart")  # Example: Send 'play' command to all clients
    return

def onPlayStateChange(state):
    send_url_command_to_clients(url="http://192.168.0.12/inotex/1.mp4", target_id="all")
    return

def onDeviceChange():
    send_url_command_to_clients(url="http://192.168.0.12/inotex/2.mp4", target_id="all")
    return

def onProjectPreSave():
    return

def onProjectPostSave():
    return

    