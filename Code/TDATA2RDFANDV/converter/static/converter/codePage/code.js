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
            console.log("Here making spinner hidden")
            // rdf = data['RDF']
            // epw = data['EPW']
            // document.getElementById('rdf').href = rdf
            // document.getElementById('epw').href = epw
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
    

// function progressBar(){
//     $('.progress-bar').animate(
//         {width:'100%'}, 
//         {
//             duration:4000      
//         }        
//     );
//   }



$(document).ready(function(){

    // Convert all the links with the progress-button class to
    // actual buttons with progress meters.
    // You need to call this function once the page is loaded.
    // If you add buttons later, you will need to call the function only for them.

    $('.progress-button').progressInitialize();

    // Listen for clicks on the first three buttons, and start 
    // the progress animations

    $('#submitButton').click(function(e){
        e.preventDefault();

        // This function will show a progress meter for
        // the specified amount of time

        $(this).progressTimed(2);
    });

    $('#actionButton').click(function(e){
        e.preventDefault();
        $(this).progressTimed(2);
    });

    $('#generateButton').one('click', function(e){
        e.preventDefault();

        // It can take a callback

        var button = $(this);
        button.progressTimed(3, function(){

            // In this callback, you can set the href attribute of the button
            // to the URL of the generated file. For the demo, we will only 
            // set up a new event listener that alerts a message.

            button.click(function(){
                alert('Showing how a callback works!');
            });
        });
    });

    // Custom progress handling

    var controlButton = $('#controlButton');

    controlButton.click(function(e){
        e.preventDefault();

        // You can optionally call the progressStart function.
        // It will simulate activity every 2 seconds if the
        // progress meter has not been incremented.

        controlButton.progressStart();
    });

    $('.command.increment').click(function(){

        // Increment the progress bar with 10%. Pass a number
        // as an argument to increment with a different amount.

        controlButton.progressIncrement();
    });

    $('.command.set-to-1').click(function(){

        // Set the progress meter to the specified percentage

        controlButton.progressSet(1);
    });

    $('.command.set-to-50').click(function(){
        controlButton.progressSet(50);
    });

    $('.command.finish').click(function(){

        // Set the progress meter to 100% and show the done text.
        controlButton.progressFinish();
    });

});

// The progress meter functionality is available as a series of plugins.
// You can put this code in a separate file if you wish to keep things tidy.

(function($){

    // Creating a number of jQuery plugins that you can use to
    // initialize and control the progress meters.

    $.fn.progressInitialize = function(){

        // This function creates the necessary markup for the progress meter
        // and sets up a few event listeners.

        // Loop through all the buttons:

        return this.each(function(){

            var button = $(this),
                progress = 0;

            // Extract the data attributes into the options object.
            // If they are missing, they will receive default values.

            var options = $.extend({
                type:'background-horizontal',
                loading: 'Loading...',
                finished: 'Submit'
            }, button.data());

            // Add the data attributes if they are missing from the element.
            // They are used by our CSS code to show the messages
            button.attr({'data-loading': options.loading, 'data-finished': options.finished});

            // Add the needed markup for the progress bar to the button
            var bar = $('<span class="tz-bar ' + options.type + '">').appendTo(button);

            // The progress event tells the button to update the progress bar
            button.on('progress', function(e, val, absolute, finish){

                if(!button.hasClass('in-progress')){

                    // This is the first progress event for the button (or the
                    // first after it has finished in a previous run). Re-initialize
                    // the progress and remove some classes that may be left.

                    bar.show();
                    progress = 0;
                    button.removeClass('finished').addClass('in-progress')
                }

                // val, absolute and finish are event data passed by the progressIncrement
                // and progressSet methods that you can see near the end of this file.

                if(absolute){
                    progress = val;
                }
                else{
                    progress += val;
                }

                if(progress >= 100){
                    progress = 100;
                }

                if(finish){

                    button.removeClass('in-progress').addClass('finished');

                    bar.delay(500).fadeOut(function(){

                        // Trigger the custom progress-finish event
                        button.trigger('progress-finish');
                        setProgress(0);
                    });

                }

                setProgress(progress);
            });

            function setProgress(percentage){
                bar.filter('.background-horizontal,.background-bar').width(percentage+'%');
                bar.filter('.background-vertical').height(percentage+'%');
            }

        });

    };

    // progressStart simulates activity on the progress meter. Call it first,
    // if the progress is going to take a long time to finish.

    $.fn.progressStart = function(){

        var button = this.first(),
            last_progress = new Date().getTime();

        if(button.hasClass('in-progress')){
            // Don't start it a second time!
            return this;
        }

        button.on('progress', function(){
            last_progress = new Date().getTime();
        });

        // Every half a second check whether the progress 
        // has been incremented in the last two seconds

        var interval = window.setInterval(function(){

            if( new Date().getTime() > 2000+last_progress){

                // There has been no activity for two seconds. Increment the progress
                // bar a little bit to show that something is happening

                button.progressIncrement(5);
            }

        }, 500);

        button.on('progress-finish',function(){
            window.clearInterval(interval);
        });

        return button.progressIncrement(10);
    };

    $.fn.progressFinish = function(){
        return this.first().progressSet(100);
    };

    $.fn.progressIncrement = function(val){

        val = val || 10;

        var button = this.first();

        button.trigger('progress',[val])

        return this;
    };

    $.fn.progressSet = function(val){
        val = val || 10;

        var finish = false;
        if(val >= 100){
            finish = true;
        }

        return this.first().trigger('progress',[val, true, finish]);
    };

    // This function creates a progress meter that 
    // finishes in a specified amount of time.

    $.fn.progressTimed = function(seconds, cb){

        seconds = seconds+10

        var button = this.first(),
            bar = button.find('.tz-bar');

        if(button.is('.in-progress')){
            return this;
        }

        // Set a transition declaration for the duration of the meter.
        // CSS will do the job of animating the progress bar for us.

        bar.css('transition', seconds+'s linear');
        button.progressSet(99);

        window.setTimeout(function(){
            bar.css('transition','');
            button.progressFinish();

            if($.isFunction(cb)){
                cb();
            }

        }, seconds*1000);
    };

})(jQuery);