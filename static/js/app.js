class App {
	constructor() {
		let self = this;
		self.logined = false;
		self.records = [];

		if (window.location.hash !== "") {
			window.location.hash = "";
		}

		self.router = new Router({
			"": "login",
			"home": "home"
		});

		self.backEnd = new BackEnd("ws://" + location.host + "/ws");
		self.backEnd.on("/login", function(result, ret) {
			if (result.status == "ok") {
				self.logined = true;
				window.location.hash = "#home";
				self.backEnd.sendWithSign({"protocol": "/get/records/all"});
			}
		});

		self.backEnd.on("/get/records/all", function(result, ret) {
			self.records = result;
			self.createTable(result, ['买卖', '名称', '价格', '付款', '状态', '备注'], 
								[['buyorsell', (item, k) => item[k] ? '买' : '卖'],
								'name',
								'price',
								'paid',
								'status',
								'remark',
								]);
		});
	}

	Login() {
		User.username = document.getElementById("username").value;
		User.password = document.getElementById("password").value;
		this.backEnd.sendWithSign({
			protocol: "/login"
		});
	}

	AddNew() {
		showID("popups")
		showID("AddNew");
	}

	createTR(item, keys){
		let tr = document.createElement('tr');
		keys.map(k=>{
			let td = document.createElement('td');
			if (typeof k == 'string'){
				td.innerText = item[k];
			}else{
				td.innerText = k[1](item, k[0]);
			}
			return td;
		}).map(td=>tr.appendChild(td));
		return tr;
	}

	createTable(items, headers, columns) {
		let self = this;
		let table = document.createElement('table');
		let tableBody = document.createElement('tbody');
		
		// body
		items.map(a => self.createTR(a, columns))
			 .map(tr => tableBody.appendChild(tr));
		table.appendChild(tableBody);
		let container = document.getElementById('tableContainer');

		// header
		let tr = document.createElement('tr');
		tr.id = 'table-header'
		headers.map(n=>{
			let td = document.createElement('td');
			td.innerText = n;
			return td;
		}).map(td=>tr.appendChild(td));
		tableBody.appendChild(tr);

		container.appendChild(table);
		return table;
	}
}