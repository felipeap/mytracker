var map;
var idInfoBoxAberto;
var infoBox = [];
var markers = [];

function initialize() {	
	var latlng = new google.maps.LatLng(-18.8800397, -47.05878999999999);
	
    var options = {
        zoom: 5,
		center: latlng,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };

    map = new google.maps.Map(document.getElementById("mapa"), options);
}

initialize();

function abrirInfoBox(id, marker) {
	if (typeof(idInfoBoxAberto) == 'number' && typeof(infoBox[idInfoBoxAberto]) == 'object') {
		infoBox[idInfoBoxAberto].close();
	}

	infoBox[id].open(map, marker);
	idInfoBoxAberto = id;
}

function carregaImg(c){
	var icon  = 'img/marcador2.png'
	if (c.search("Hard")>0){
		icon= 'img/marcador.png';
	}
	if (c.search("Calibration")>0){
		icon= 'img/marcador.png';
	}
	if (c.search("Impact")>0){
		icon= 'img/marcador.png';
	}
	return icon
}

function carregarPontos() {
	
	$.getJSON('js/pontos.json', function(pontos) {
		
		var latlngbounds = new google.maps.LatLngBounds();
		
		/*var enderDe = '-19.957200,-44.198914';
		var enderAte = '-19.958610,-44.198700';
		var local1 = {location:'-19.957210,-44.198914'};
		var local2 = {location:'-19.957400,-44.198914'};
		
		var request = {
			origin:endDe, 
			destination:endPara,
			travelMode: google.maps.DirectionsTravelMode.DRIVING,
			waypoints: new Array (local1, local2)
		};*/
		
		$.each(pontos, function(index, ponto) {
			var marker = new google.maps.Marker({
				position: new google.maps.LatLng(ponto.Latitude, ponto.Longitude),
				title: "Equipamento: 7001035",
				icon: carregaImg(ponto.Descricao)
			});
			
			var myOptions = {
				content: "<p>" + ponto.Descricao + "</p>",
				pixelOffset: new google.maps.Size(-150, 0)
        	};
			infoBox[ponto.Id] = new InfoBox(myOptions);
			infoBox[ponto.Id].marker = marker;
			infoBox[ponto.Id].listener = google.maps.event.addListener(marker, 'click', function (e) {
				abrirInfoBox(ponto.Id, marker);
			});
		
			//request.waypoints.push ({location: ponto.Latitude+','+ponto.Longitude});		
			
			markers.push(marker);
			latlngbounds.extend(marker.position);		
		});
		
		var markerCluster = new MarkerClusterer(map, markers);
		
		map.fitBounds(latlngbounds);
		
	});
	
}

carregarPontos();