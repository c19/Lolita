let User = (function () {
	var name="";
	var secret="";
	return {get username(){
				return name;
			},
			set username(val){
				name = val;
			},
			set password(val){
				secret = CryptoJS.HmacSHA256(name+"#"+val, "b3ed5c95-b544-46d9-ac18-ddde6290b3cf").toString();
			},
			sign: function(content){
				return CryptoJS.HmacSHA256(content, secret).toString();
			}};
})();