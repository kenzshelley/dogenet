var ip = "8675.309.0";

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
				if (ip === leaders[i].get("ip")) {
					console.log(leaders[i].get("ip"));
					for (var j = 0; j < leaders[i].get("credentials").length; j++) {
						var table = document.getElementById("history-table");
						var row = table.insertRow(-1);
						var cell1 = row.insertCell(0);
						var cell2 = row.insertCell(1);
						var cell3 = row.insertCell(2);
						cell1.innerHTML = leaders[i].get("credentials")[j][0];
						cell2.innerHTML = leaders[i].get("credentials")[j][1];
						cell3.innerHTML = leaders[i].get("credentials")[j][2];
					}
					break;
				}
			}	
		}
	});
});