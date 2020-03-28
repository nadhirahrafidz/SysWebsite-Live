$('document').ready(function(){
    $('#div_id_locationParent_country').attr('hidden', true);
    $('#div_id_locationParent_region').attr('hidden', true);
});

$('#id_locationType').change(function() {
    observe();
});

function observe() 
{
    var chosenQuestion = $('#id_locationType').val();
    console.log(chosenQuestion)
    if(chosenQuestion == 2)
    {
        $('#div_id_locationParent_country').attr('hidden', false);
        $('#div_id_locationParent_region').attr('hidden', true);
    }
    else if(chosenQuestion == 3)
    {
        $('#div_id_locationParent_region').attr('hidden', false);
        $('#div_id_locationParent_country').attr('hidden', true);
    }
    else
    {
        $('#div_id_locationParent_country').attr('hidden', true);
        $('#div_id_locationParent_region').attr('hidden', true);
    }
}