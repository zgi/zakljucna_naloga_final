
function izbrisi(sporocilo_id)
{
    var potrdi = confirm('Ali  resnično želiš !IZBRISATI! sporočilo?')
    if (potrdi == true)
    {
        var xhr = new XMLHttpRequest();
        xhr.open("POST", '/izbrisi/' + sporocilo_id, true);
        xhr.send();
    }
    else
    {
        alert('Izbris sporočila preklican');
    }
}

function trajno_izbrisi(sporocilo_id)
{
    var potrdi = confirm('Ali  resnično želiš !IZBRISATI! sporočilo? Trajno izbrisana sporočila se ne da obnoviti!')
    if (potrdi == true)
    {
        var xhr = new XMLHttpRequest();
        xhr.open("POST", '/delete4evvah/' + sporocilo_id, true);
        xhr.send();
    }
    else
    {
        alert('Izbris sporočila preklican');
    }
}
