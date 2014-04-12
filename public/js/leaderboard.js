$(document).ready(function(){

	Parse.initialize("KNf3x2GGrkFOoRapY8D9y6PkrHKRPlk6FgeWblEF", "hfutDYnw41mayLiVZdcNBL3e3d1fB9DAfoAw5XtO");

	console.log("leader is working");
	var leader = Parse.Object.extend("Client");
	var query = new Parse.Query(leader);
	query.descending("score")
	query.find({
		success:function(leaders){
			console.log(leaders.length);

			var xmlHttp = null;

			xmlHttp = new XMLHttpRequest();
			xmlHttp.open( "GET", "http://192.168.1.137:3000/clients", false);
			xmlHttp.send( null );
			console.log("AHHHH");
			console.log(xmlHttp.responseText);

			var json = JSON.parse(xmlHttp.responseText);

			var ips = new Object();
			for(var i = 0; i < json.length; i++){
				ips[json[i].ip] = json[i].hostname;
			}

			for(var i = 0; i < leaders.length; i++){
				var table = document.getElementById("leaderboard-table")
				var row = table.insertRow(-1);
				var cell1 = row.insertCell(0);
				var cell2 = row.insertCell(1);
				var name;
				if(ips[leaders[i].get("ip")] == undefined){
					name = leaders[i].get("ip");
				}
				else
					name = ips[leaders[i].get("ip")];
				cell1.innerHTML = name;
				cell2.innerHTML = leaders[i].get("score");
			}

			// drop the panel down
			window.setTimeout(function() {
				document.querySelector('#leaderboard').classList.remove('unloaded');
			}, 1000);
			
		}
	});

	// click listener for the handle
	console.log("mega wat");
	$('#leaderboard-handle').on('click', function() {
		console.log("wat")
		document.querySelector('#leaderboard').classList.toggle('unopened');
	});
});