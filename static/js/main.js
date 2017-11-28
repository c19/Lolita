let app = undefined;

function load() {
	app = new App();
	RunHtmlSnippet("init");
	SetHtmlDefault();
	setWriteToListener();
	setOnChildListChange();
}

window.onload = load;