# me - this DAT.
# webServerDAT - the connected Web Server DAT
# request - A dictionary of the request fields. The dictionary will always contain the below entries, plus any additional entries dependent on the contents of the request
# 		'method' - The HTTP method of the request (ie. 'GET', 'PUT').
# 		'uri' - The client's requested URI path. If there are parameters in the URI then they will be located under the 'pars' key in the request dictionary.
#		'pars' - The query parameters.
# 		'clientAddress' - The client's address.
# 		'serverAddress' - The server's address.
# 		'data' - The data of the HTTP request.
# response - A dictionary defining the response, to be filled in during the request method. Additional fields not specified below can be added (eg. response['content-type'] = 'application/json').
# 		'statusCode' - A valid HTTP status code integer (ie. 200, 401, 404). Default is 404.
# 		'statusReason' - The reason for the above status code being returned (ie. 'Not Found.').
# 		'data' - The data to send back to the client. If displaying a web-page, any HTML would be put here.
import json

# return the response dictionary
def onHTTPRequest(webServerDAT, request, response):
    # Set 'n' to '0' if not provided
    n = request['pars'].get('n', '0')
    print(f"Parameter n: {n}")

    rout_dic = {
        '0': 'http://192.168.0.12/inotex/1.mp4',
        '1': 'http://192.168.0.12/inotex/2.mp4',
        '2': 'http://192.168.0.12/inotex/n2.mp4',
        '5': 'http://192.168.0.12/inotex/n5.mp4',
        '6': 'http://192.168.0.12/inotex/n6.mp4',
        '9': 'http://192.168.0.12/inotex/n9.mp4',
        '19': 'http://192.168.0.12/inotex/n19.mp4',
        '17': 'http://192.168.0.12/inotex/n17.mp4',
        '3': 'http://192.168.0.12/inotex/n23.mp4',
        '88': 'http://192.168.0.12/inotex/n88.mp4',
        '999': 'http://localhost/inotex/8.mp4',
    }

    selected_url = rout_dic.get(str(n), 'http://192.168.0.12/inotex/1.mp4')
    print(f"Selected video URL: {selected_url}")

    response['statusCode'] = 200
    response['statusReason'] = 'OK'
    response['data'] = op('webPage').text.replace('specialchar', selected_url)

    return response

clients = []

def updateClientTable():
    table = op('clientList')
    table.clear()
    table.appendRow(['id', 'client'])
    for i, c in enumerate(clients):
        table.appendRow([str(i), str(c)])

# def onWebSocketOpen(webServerDAT, client):
#     clients.append(client)
#     updateClientTable()
#     return

# def onWebSocketClose(webServerDAT, client):
#     if client in clients:
#         clients.remove(client)
#     updateClientTable()
#     return


def onWebSocketOpen(webServerDAT, client):
	clients_table = op('clientList')
	if clients_table is not None:
		clients_table.appendRow([client])
	return

def onWebSocketClose(webServerDAT, client):
	clients_table = op('clientList')
	if clients_table is not None:
		for i in range(1, clients_table.numRows):  # skip header
			if clients_table[i, 0].val == str(client):
				clients_table.deleteRow(i)
				break
	return
# def onWebSocketOpen(webServerDAT, client):
#     # webServerDAT.webSocketSendText(client, "Welcome to the server!")
# 	return


# def onWebSocketClose(webServerDAT, client):
# 	return

def onWebSocketReceiveText(webServerDAT, client, data):
	webServerDAT.webSocketSendText(client, data)
	return

def onWebSocketReceiveBinary(webServerDAT, client, data):
	webServerDAT.webSocketSendBinary(client, data)
	return

def onWebSocketReceivePing(webServerDAT, client, data):
	webServerDAT.webSocketSendPong(client, data=data);
	return

def onWebSocketReceivePong(webServerDAT, client, data):
	return


def onServerStart(webServerDAT):
	return

def onServerStop(webServerDAT):
	return
	