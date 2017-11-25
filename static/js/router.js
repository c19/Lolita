function showId(id) {
	let elm = document.getElementById(id);
	if (elm) {
		elm.style.display = "block";
	} else {
		console.error("can't getElementById: " + id);
	}
}

function hideId(id) {
	let elm = document.getElementById(id);
	if (elm) {
		elm.style.display = "none";
	} else {
		console.error("can't getElementById: " + id);
	}
}

class Router {
	constructor(routes) {
		this.routes = routes;
		this.onerror = console.log;
		this.init();
	}
	handle(hash, oldHash) {
		let self = this;
		let route = self.routes[hash];
		let oldRoute = self.routes[oldHash];
		if (route && typeof route == 'string') {
			hideId(oldRoute);
			showId(route);
		} else {
			self.onerror("invalid route for: " + hash);
		}
	}
	init() {
		var self = this;
		window.addEventListener('hashchange',
			function(event) {
				let prev = event.oldURL.split("#")[1] || "";
				self.handle.call(self, window.location.hash, prev);
			}, false);
		window.addEventListener('beforeunload',
			function(event) {
				return "Please do not refresh the page";
			}, false);
		window.addEventListener('load',
			function(event) {
				self.handle.call(self, window.location.hash, "");
			}, false);
		if(document.readyState === "complete") {
			self.handle.call(self, window.location.hash, "");
		}
	}
}