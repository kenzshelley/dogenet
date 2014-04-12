$(document).ready(function(){

	Parse.initialize("KNf3x2GGrkFOoRapY8D9y6PkrHKRPlk6FgeWblEF", "hfutDYnw41mayLiVZdcNBL3e3d1fB9DAfoAw5XtO");

	console.log("leader is working");
	var leader = Parse.Object.extend("Client");
	var query = new Parse.Query(leader);
	query.descending("score")
	// console.log("here");
	query.find({
		success:function(leaders){
			//DISPLAY LEADERS]
			console.log(leaders.length);

			var xmlHttp = null;

			xmlHttp = new XMLHttpRequest();
			xmlHttp.open( "GET", "http://127.0.0.1:3000/clients", false);
			xmlHttp.send( null );
			console.log("AHHHH");
			console.log(xmlHttp.responseText);

			var json = JSON.parse(xmlHttp.responseText);

/*			console.log(json.dhcp_leases);
			console.log("shit before this matters");*/
			//TEMPORARY -- will change later when on server
			txt = {"dhcp_leases": ['MackenziesMBP3','192.168.1.120','70:56:81:9E:C0:3F','1 day 00:00:00','120','Alpha-1404','192.168.1.137','B8:F6:B1:19:50:93','1 day 00:00:00','137','Matthews-MBP-5','192.168.1.117','B8:E8:56:2D:90:40','1 day 00:00:00','117','oswald-macbookpro','192.168.1.114','14:10:9F:DF:DE:05','1 day 00:00:00','114','aidan-HP-Pavilion-dv4-Notebook-PC','192.168.1.135','C4:17:FE:9C:FB:41','1 day 00:00:00','135','android-e5c4fcb41e71d444','192.168.1.123','E8:99:C4:7E:3D:5D','1 day 00:00:00','123','*','192.168.1.111','28:CF:DA:D3:69:60','1 day 00:00:00','111','android-6d2c4a72decd06a0','192.168.1.149','40:F3:08:7D:2A:FE','1 day 00:00:00','149','Lolita','192.168.1.112','00:26:C7:66:E8:06','1 day 00:00:00','112','android-ba92ac33c931f3c7','192.168.1.127','5C:0A:5B:1A:BB:53','1 day 00:00:00','127','Sachins-iPhone','192.168.1.138','AC:FD:EC:72:EA:5D','1 day 00:00:00','138','PaulineLow-PC','192.168.1.132','08:3E:8E:32:E1:ED','1 day 00:00:00','132']};
			console.log(txt.dhcp_leases);
			var ips = new Object();
			for(var i = 0; i < txt.dhcp_leases.length; i++){
				ips[txt.dhcp_leases[i+1]] = txt.dhcp_leases[i];
				i = i + 5;
			}
			console.log(ips["192.168.1.120"]);
			parser=new DOMParser();
			xmlDoc=parser.parseFromString(txt,"text/xml");

			for(var i = 0; i < leaders.length; i++){
				// console.log(leaders[i].get("ip"));
				// console.log(leaders[i].get("score"));
				//$('#leaderboard').append('<tr><td>leaders[i].get("ip")</td><td>leaders[i].get("score")</td></tr>')
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
		}
	});
});