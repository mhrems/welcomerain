function app() {
	console.log(this); //window
}

var app = new app();