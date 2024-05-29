var clicked = false;

function search(){
    var input, text, subtitle, searchlist;
    input = document.getElementById('search');
    text = input.value.toUpperCase();
    subtitle = document.getElementById('roles');
    searchlist = Array.prototype.slice.call(subtitle.children);
    searchlist.shift()
    for (var element of searchlist){
        try{
            if (element.children[0].id.toUpperCase().indexOf(text) > -1) {
                element.style.display = "block";
            }
            else{
                element.style.display = "none";
            }
        }
        catch{
            //pass
        }
    }
}
window.onload=function(){
    var searchInput = document.getElementById('search');
    searchInput.addEventListener('keyup', search);
}