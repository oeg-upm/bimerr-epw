let jsonDataMap;


function openTab(evt, tabName) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";
}


$(".custom-file-input").on("change", function () {
    var fileName = $(this).val().split("\\").pop();
    $(this).siblings(".custom-file-label").addClass("selected").html(fileName);
});


// CÓDIGO PARA IMPRIMIR DATOS EN TABLA DE LOS DOCUMENTOS

function numberProducts(data) {
    productos = data["cities"];
    var items = [];
    var contador = 0;
    $.each(productos, function (key, val) {
        items.push("<tr>");
        items.push("<td id=''" + key + "''>" + val.adm0_a3 + "</td>");
        items.push("<td id='" + val.link + "'>" + val.link + "</td>");
        items.push("<td onclick='redirectTo(\"" + val.link + "\"," + "\"" + contador + "\")' id='Download' class='p-2'><button type='button'>Generate Files</button><div class='container' id='Loading" + contador + "' style='visibility: hidden;' align='center'><div class='spinner-border spinner-border-sm' role='status'><span class='sr-only'>Loading...</span></div></div></td>");
        items.push("</tr>");
        contador += 1;
    })
    $('<tbody/>', { html: items.join("") }).appendTo("table");
}

function redirectTo(link, contador) {
    var urlData;
    if(link.endsWith(".epw")){
        urlData = '/makeECEnergyPlus'
    }
    else if(link.endsWith(".zip")){
        urlData = '/makeExtractAndConversion'
    }
    $("#Loading" + contador).css('visibility', 'visible');
    $.ajax({
        type: 'POST',
        url: urlData,
        data: JSON.stringify({
            code: link
        }),
        success: (data, textStatus, jqXHR) => {
            console.log(data, textStatus, jqXHR)
            rdf = data['RDF']
            epw = data['EPW']
            document.getElementById('rdf').href = rdf
            document.getElementById('epw').href = epw
            $("#Loading" + contador).css('visibility', 'hidden');
        },
        contentType: 'application/json',
        dataType: 'json'
    });
}
// AQUÍ ESTÁ LA PARTE DEL MAPA

function Map2(data) {

    function refreshMap() {
        document.getElementById('mapWrapper').innerHTML='<div id="map"></div>';
    }

    refreshMap();

    var map = L.map('map', {
        minZoom: 2
    });

    map.createPane('labels');

    // This pane is above markers but below popups
    map.getPane('labels').style.zIndex = 650;

    // Layers in this pane are non-interactive and do not obscure mouse/touch events
    map.getPane('labels').style.pointerEvents = 'none';

    var cartodbAttribution = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, &copy; <a href="https://carto.com/attribution">CARTO</a>';

    var positron = L.tileLayer('https://{s}.basemaps.cartocdn.com/light_nolabels/{z}/{x}/{y}.png', {
        attribution: cartodbAttribution
    }).addTo(map);

    var positronLabels = L.tileLayer('http://{s}.basemaps.cartocdn.com/light_only_labels/{z}/{x}/{y}.png', {
        attribution: cartodbAttribution,
        pane: 'labels'
    }).addTo(map);



    function getColor(d) {
        return d == 1 ? '#800026' :
            d == 2 ? '#1570BF' :
                d == 3 ? '#38A673' :
                    d == 4 ? '#F2D129' :
                        d == 5 ? '#F26430' :
                            d == 6 ? '#F22F1D' :
                                d == 7 ? '#F22E62' :
                                    '#092601';
    }

    function style(feature) {
        return {
            fillColor: getColor(
                feature.properties.mapcolor7),
            weight: 1,
            opacity: 1,
            color: 'white',
            dashArray: '',
            fillOpacity: 0.3
        };
    }


    L.geoJson(data, { style: style }).addTo(map);



    geojson = L.geoJson(data).addTo(map);
    geojson = L.geoJson(geoOceans).addTo(map)



    map.setView({ lat: 47.040182144806664, lng: 9.667968750000002 }, 2);


    function highlightFeature(e) {
        var layer = e.target;

        layer.setStyle({
            weight: 1,
            color: '#FFFF',
            dashArray: '',
            opacity: 1,
            fillOpacity: 1
        });



        if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
            layer.bringToFront();
        }
    }



    function resetHighlight(e) {
        geojson.resetStyle(e.target);
    }




    var geojson;
    // ... our listeners
    geojson = L.geoJson(data);

    function zoomToFeature(e) {
        map.fitBounds(e.target.getBounds());
    }




    function onEachFeature(feature, layer) {
        layer.on({
            mouseover: highlightFeature,
            mouseout: resetHighlight,
            click: zoomToFeature
        });
        layer.bindPopup(function (layer) {
            if (buttonClicked == 'Climate1') {
                $.ajax({
                    type: 'POST',
                    url: '/getInfoMap/',
                    data: JSON.stringify({
                        code: layer.feature.properties.adm0_a3
                    }),
                    success: (data, textStatus, jqXHR) => {
                        console.log(data, textStatus, jqXHR)
                        jsonDataMap = data
                        $('table > tbody > tr > td').parent().remove();
                        numberProducts(data)
                    },
                    contentType: 'application/json',
                    dataType: 'json'
                });
            }
            else if (buttonClicked == 'Energy') {
                $.ajax({
                    type: 'POST',
                    url: '/getInfoMapEP/',
                    data: JSON.stringify({
                        code: layer.feature.properties.adm0_a3
                    }),
                    success: (data, textStatus, jqXHR) => {
                        console.log(data, textStatus, jqXHR)
                        jsonDataMap = data
                        $('table > tbody > tr > td').parent().remove();
                        numberProducts(data)
                    },
                    contentType: 'application/json',
                    dataType: 'json'
                });
            }


            return layer.feature.properties.name;
        });

    }

    geojson = L.geoJson(data, {
        style: style,
        onEachFeature: onEachFeature
    }).addTo(map);


    //  AQUÍ TERMINA LA PARTE DEL MAPA
}

function myFunction() {
    var input, filter, table, tr, td, i, txtValue;
    input = document.getElementById("myInput");
    filter = input.value.toUpperCase();
    table = document.getElementById("myTable");
    tr = table.getElementsByTagName("tr");
    for (i = 0; i < tr.length; i++) {
        td = tr[i].getElementsByTagName("td")[1];
        if (td) {
            txtValue = td.textContent || td.innerText;
            if (txtValue.toUpperCase().indexOf(filter) > -1) {
                tr[i].style.display = "";
            } else {
                tr[i].style.display = "none";
            }
        }
    }
}

function initMap() {

    function refreshMap() {
        document.getElementById('mapWrapper').innerHTML='<div id="map"></div>';
    }

    refreshMap();

    var map = L.map('map', {
        minZoom: 2
    }).setView([0, 0],2);

    map.createPane('labels');

    // This pane is above markers but below popups
    map.getPane('labels').style.zIndex = 650;

    // Layers in this pane are non-interactive and do not obscure mouse/touch events
    map.getPane('labels').style.pointerEvents = 'none';


    var positron = L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);


    var popup = L.popup();

    var marker = {};
    
    map.on('click', function(e){
        var coord = e.latlng;
        var lat = coord.lat;
        var lng = coord.lng;
        var c = [lat,lng];
        if (marker != undefined) {
            map.removeLayer(marker);
        };

        //Add a marker to show where you clicked.
        marker = L.marker([lat,lng]).addTo(map);

        popup
        .setLatLng(e.latlng)
        .setContent("Latitude: "+lat+ "<br>Longitude: "+lng)
        .openOn(map);

        document.getElementById("latitude").value = lat.toString();
        document.getElementById("longitude").value = lng.toString();
    });

    var searchControl = new L.esri.Controls.Geosearch().addTo(map);

    var results = new L.LayerGroup().addTo(map);

    searchControl.on('results', function(data){
    results.clearLayers();
    for (var i = data.results.length - 1; i >= 0; i--) {
        results.addLayer(L.marker(data.results[i].latlng));
        popup
        .setLatLng(data.results[i].latlng)
        .setContent("Latitude: "+data.results[i].latlng.lat.toString()+ "<br>Longitude: "+data.results[i].latlng.lng.toString())
        .openOn(map);
        document.getElementById("latitude").value = data.results[i].latlng.lat.toString();
        document.getElementById("longitude").value = data.results[i].latlng.lng.toString();
    }
    }); 
}

let buttonClicked = ''
function clickButton(id) {
    document.getElementById('mapWrapper').style.visibility="visible"
    buttonClicked = id;
    if (id == 'Climate1') {
        Map2(geoLocations);
    }
    else if (id == 'Energy') {
        Map2(geoLocations1);
    }
    else if (id == 'DarkSkyAPI') {
        initMap();
    }
}

function getDarkSkyAPIData(){
    var latitudes = document.getElementById("latitude").value
    var longitudes = document.getElementById("longitude").value
    $.ajax({
        type: 'POST',
        url: '/makeECDarkSkyAPI',
        data: JSON.stringify({
            latitude: latitudes,
            longitude: longitudes
        }),
        success: (data, textStatus, jqXHR) => {
            console.log(data, textStatus, jqXHR)
        },
        contentType: 'application/json',
        dataType: 'json'
    });
}
        