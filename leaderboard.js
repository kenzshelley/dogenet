
$(document).ready(function(){

	Parse.initialize("KNf3x2GGrkFOoRapY8D9y6PkrHKRPlk6FgeWblEF", "hfutDYnw41mayLiVZdcNBL3e3d1fB9DAfoAw5XtO");

	console.log("this is working");
	var leader = Parse.Object.extend("Client");
	var query = new Parse.Query(leader);
	query.descending("score")
	console.log("here");
	query.find({
		success:function(leaders){
			//DISPLAY LEADERS]
			console.log(leaders.length);
			for(var i = 0; i < leaders.length; i++){
				console.log(leaders[i].get("ip"));
				console.log(leaders[i].get("score"));
			}
		}
	});
});