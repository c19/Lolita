function clearChildren(node){
	while (node.firstChild) {
		node.removeChild(node.firstChild);
	}
	return node;
}

function setOptions(name, values){
	let frag = createOptions(values);
	Array.from(document.getElementsByName(name)).map(clearChildren).map(select=>{
		select.appendChild(frag);
	});
}

function createOptions(values){
	let frag = document.createDocumentFragment();
	values.map(v=>{
		let option = document.createElement('option');
		option.value = v;
		option.innerText = v;
		return option;
	}).map(op=>frag.appendChild(op));
	return frag;
}

function createTR(item, keys){
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

function createTable(items, headers, columns) {
	let table = document.createElement('table');
	let tableBody = document.createElement('tbody');
	
	// body
	items.map(a => createTR(a, columns))
		 .map(tr => tableBody.appendChild(tr));
	table.appendChild(tableBody);

	// header
	let tr = document.createElement('tr');
	tr.id = 'table-header'
	headers.map(n=>{
		let td = document.createElement('td');
		td.innerText = n;
		return td;
	}).map(td=>tr.appendChild(td));
	tableBody.appendChild(tr);
	return table;
}

function scrollToBottom(id){
	let s = document.getElementById(id);
	s.scrollTop = s.scrollHeight;
}

function RunHtmlSnippet(attr){
	document.querySelectorAll(`[${attr}]`).forEach(elm=>{
		Function("elm", elm.getAttribute(attr))(elm);
	});
}

function SetHtmlDefault(){
	document.querySelectorAll("[default]").forEach(elm=>{
		elm.value = elm.getAttribute("default");
	});
}

function setWriteToListener(){
	document.querySelectorAll("[writeTo]").forEach(elm=>{
		let target = document.getElementById(elm.getAttribute("writeTo"));
		elm.addEventListener("change", function(event){
			target.value = event.target.value;
		});
	});
}

function setOnChildListChange(){
	document.querySelectorAll("[onChildListChange]").forEach(elm=>{
		// create an observer instance
		var observer = new MutationObserver(function(mutations) {
			console.log(mutations);   
		});

		// configuration of the observer:
		var config = { attributes: false, childList: true, characterData: false };

		// pass in the target node, as well as the observer options
		observer.observe(target, config);
	});
}