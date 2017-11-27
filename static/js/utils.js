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