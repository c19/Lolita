class App {
	constructor() {
		let self = this;
		self.logined = false;
		self.records = [];
		self.names = [];
		self.catagories = [];
		self.status = [];

		self.newRecord = {
			get price() {
				return parseInt(document.getElementById("price").value||"0");
			},
			get baseprice() {
				return parseInt(document.getElementById("baseprice").value||"0");
			},
			get name() {
				return document.getElementById("name").value||"";
			},
			get status() {
				return document.getElementById("status").value||"";	
			},
			get catagory() {
				return document.getElementById("catagory").value||"";	
			},
			get remark() {
				return document.getElementById("remark").value||"";	
			},
			get mail_fee() {
				return parseInt(document.getElementById("mail_fee").value||"0");
			},
			get paid() {
				return parseInt(document.getElementById("paid").value||"0");
			}
		};

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

		self.backEnd.on("/get/records/all", function(records, ret) {
			self.RefreshData(records);
			window.scrollTo(0,document.body.scrollHeight);
		});
	}

	setTable(items, headers, columns) {
		let table = createTable(items, headers, columns);
		let container = document.getElementById('tableContainer');
		clearChildren(container);
		container.appendChild(table);
		return table;
	}

	RefreshData(records) {
		let self = this;
		self.records = records;
		self.setTable(records, ['买卖', '名称', '价格', '付款', '状态', '备注'], 
							[['buyorsell', (item, k) => item[k] ? '买' : '卖'],
							'name',
							'price',
							'paid',
							'status',
							'remark',
							]);
		self.names = Array.from((new Set(self.records.map(a=>a.name))).keys()).sort();
		self.catagories = Array.from((new Set(self.records.map(a=>a.catagory))).keys()).sort();
		self.status = Array.from((new Set(self.records.map(a=>a.status))).keys()).sort();

		setOptions("selectNames", self.names);
		setOptions("selectCatagories", self.catagories);
		setOptions("selectStatus", self.status);
	}

	Login() {
		User.username = document.getElementById("username").value;
		User.password = document.getElementById("password").value;
		this.backEnd.sendWithSign({
			protocol: "/login"
		});
	}

	ShowAddNew() {
		showID("popups");
		showID("AddNew");
		scrollToBottom("add-content");
	}

	HideAddNew() {
		hideID("AddNew");
		hideID("popups");
	}

	AddNew() {
		let self = this;
		self.backEnd.sendWithSign({protocol: "/add/record", payload: self.newRecord});
	}
}