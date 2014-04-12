$(document).ready(function(){

	Parse.initialize("KNf3x2GGrkFOoRapY8D9y6PkrHKRPlk6FgeWblEF", "hfutDYnw41mayLiVZdcNBL3e3d1fB9DAfoAw5XtO");

	console.log("history is working");
	var leader = Parse.Object.extend("Client");
	var query = new Parse.Query(leader);
	query.find({
		success:function(leaders){
			//DISPLAY HISTORY
			console.log(leaders.length);
			for(var i = 0; i < leaders.length; i++){
				console.log(leaders[i].get("ip"));
				console.log(leaders[i].get("score"));
				//$('#leaderboard').append('<tr><td>leaders[i].get("ip")</td><td>leaders[i].get("score")</td></tr>')
				var table = document.getElementById("leaderboard-table")
				var row = table.insertRow(-1);
				var cell1 = row.insertCell(0);
				var cell2 = row.insertCell(1);
				cell1.innerHTML = leaders[i].get("ip");
				cell2.innerHTML = leaders[i].get("score");
			}
		}
	});
});