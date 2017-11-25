class BackEnd {
	constructor(uri){
		self = this;
		self.uri = uri;
		self.ws = new WebSocket(uri)
		self.protocol_callbacks = {};
		self.onError = function(j){
			console.error(j);
		}
		self.ws.onmessage = function(event){
			let j = JSON.parse(event.data);
			let callback = self.protocol_callbacks[j.protocol];
			if (j.status == 'error'){
				self.onError(j.msg);
			}else{
				if (callback==undefined){
					console.warn('unkown protocol: '+j.protocol);
				}else{
					callback(j.result, j.ret);
				}
			}
		}
	}
	sendWithSign(json){
		json['timestamp'] = Date.now();
		var content = JSON.stringify(json);
		json['user'] = User.username;
		json['sign'] = User.sign(content);
		this.ws.send(JSON.stringify(json));
	}
	on(protocol, callback){
		this.protocol_callbacks[protocol] = callback;
	}

}