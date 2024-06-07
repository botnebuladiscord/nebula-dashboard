var clicked = false;

function search(){
    var input, text, subtitle, searchlist;
    input = document.getElementById('search');
    text = input.value.toUpperCase();
    subtitle = document.getElementById('commands');
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

function clickHandler(element){
    if (clicked == true){
        clicked = false;
    }
    else{
        var elements = document.getElementsByClassName(element.currentTarget.id);
        for (var element of elements){
            if (element.style.display == "block"){
                element.style.display = "none";
                element.parentElement;
                element.parentElement.children[0].children[0].children[0].children[1].children[1].style.display = "inline-block";
                element.parentElement.children[0].children[0].children[0].children[1].children[2].style.display = "none";
            }
            else{
                element.style.display = "block";
                element.parentElement.children[0].children[0].children[0].children[1].children[2].style.display = "inline-block";
                element.parentElement.children[0].children[0].children[0].children[1].children[1].style.display = "none";
            }
        }
    }
}

function cmdbtn(element){
    clicked = true;
    if (element.currentTarget.style.backgroundColor == "red"){
        element.currentTarget.style.backgroundColor = "#28A745";
        var databar = document.getElementById("databar");
        databar.style.padding = "2vh";
        databar.style.height = "6vh";
        databar.style.color = "white";
        var cmdname = element.currentTarget.parentElement.parentElement.children[0].innerHTML
        $.getJSON("/change_command_status_e"+String(cmdname), function() {});
        setTimeout(function() {
            databar.style.color = "transparent";
            databar.style.height = "0vh";
            databar.style.padding = "0vh";
        }, 2000);
    }
    else{
        element.currentTarget.style.backgroundColor = "red";
        var databar = document.getElementById("databar");
        databar.style.padding = "2vh";
        databar.style.height = "6vh";
        databar.style.color = "white";
        var cmdname = element.currentTarget.parentElement.parentElement.children[0].innerHTML
        $.getJSON("/change_command_status_d"+String(cmdname), function() {});
        setTimeout(function() {
            databar.style.color = "transparent";
            databar.style.height = "0vh";
            databar.style.padding = "0vh";
        }, 2000);
    }
}

window.onload=function(){
    var elements = document.getElementsByClassName('command-content');
    for (var element of elements){
        element.addEventListener('click', clickHandler);
    }

    var elements = document.getElementsByClassName('cmdbtn');
    for (var element of elements){
        element.addEventListener('click', cmdbtn);
    }

    var searchInput = document.getElementById('search');
    searchInput.addEventListener('keyup', search);
}
