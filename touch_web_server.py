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

# return the response dictionary
def onHTTPRequest(webServerDAT, request, response):
    # Set 'n' to '0' if not provided
    n = request['pars'].get('n', '0')
    print(f"Parameter n: {n}")

    rout_dic = {
        '0': 'http://192.168.0.12/inotex/1.mp4',
        '1': 'http://192.168.0.12/inotex/2.mp4',
        '2': 'http://192.168.0.12/inotex/3.mp4',
        '3': 'http://192.168.0.12/inotex/4.mp4',
        '19': 'http://192.168.0.12/inotex/5.mp4',
        '17': 'http://192.168.0.12/inotex/6.mp4',
        '88': 'http://192.168.0.12/inotex/7.mp4',
        '9': 'http://192.168.0.12/inotex/8.mp4',
    }

    selected_url = rout_dic.get(str(n), 'http://192.168.0.12/inotex/1.mp4')
    print(f"Selected video URL: {selected_url}")

    response['statusCode'] = 200
    response['statusReason'] = 'OK'
    response['data'] = op('webPage').text.replace('specialchar', selected_url)

    return response

def onWebSocketOpen(webServerDAT, client, uri):
	return

def onWebSocketClose(webServerDAT, client):
	return

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
	