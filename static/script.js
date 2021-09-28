let dropdown = $('#select-disease');

dropdown.empty();

dropdown.append('<option disabled>Choose your Symptoms</option>');
//dropdown.prop('selectedIndex',0);

const url = 'sym.json';


$.getJSON(url, function (data){
    $.each(data, function(key, entry){
        dropdown.append($('<option></option>').attr('data-tokens', entry.name).text(entry.name));
    })
});

// //'https://api.myjson.com/bins/fnf2y'


