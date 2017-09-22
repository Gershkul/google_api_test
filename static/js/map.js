/**
 * Created by developer on 19.09.17.
 */
var map;
var markers;
var fusionTablesLayer;
var options;

function render_table(data) {
    if (!data.length) {
        $('#list').html('');
        $('#reset-button').hide();
        return;
    }
    $('#reset-button').show();
    var content = '<table class="table table-striped">';
    content += '<tr><th>Address</th><th>lat</th><th>lng</th></tr><tbody>';
    for (var row in data) {
        content += '<tr><td>' + data[row].address + '</td><td>' + data[row].lat + '</td><td>' + data[row].lng + '</td></tr>'
    }
    content += '</tbody></table>';
    $('#list').html(content)
}

function delete_markers() {

    for (var i in markers) {
        markers[i].setMap(null)
    }
    markers = []
}

function render_markers(data) {

    delete_markers();
    for (var i in data) {
        var marker = new google.maps.Marker({
            position: {
                lat: parseFloat(data[i].lat),
                lng: parseFloat(data[i].lng)
            },
            map: map
        });
        markers.push(marker)
    }
}

function update_fusionTablesLayer(){

    fusionTablesLayer.setOptions({
        query: {
            select: 'Location',
            from: options.table_id
        }
    });

}

/**
 * Important: this function callbacks parameters on Google Maps API calling (file: /maptapp/templates/home.html)
 */
function initMap() {

    options = JSON.parse(map_options);

    map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: options.latLng.lat, lng: options.latLng.lng},
        zoom: options.zoom
    });

    fusionTablesLayer = new google.maps.FusionTablesLayer({
          query: {
            select: 'Location',
            from: options.table_id
          }
    });
    fusionTablesLayer.setMap(map);

    markers = [];
    map.addListener('click', function (a) {

        $.post('api/', {'lat': a.latLng.lat(), 'lng': a.latLng.lng()}, function (data) {
            render_table(data.data);
            render_markers(data.data);
            update_fusionTablesLayer();
            
        }).fail(function (data, a, b) {
            if(data.status == 404){
                alert( JSON.parse(data.responseText).message)
            }
        })
    });

    $('#reset-button').on('click', function (e) {

        $.ajax({
            url: 'api/',
            type: 'DELETE',
            success: function (data) {
                render_table([])
                delete_markers();
                update_fusionTablesLayer();
            }

        });


    });
    $.get('api/', function (data) {
        render_table(data.results);
        render_markers(data.results);
    })
}

