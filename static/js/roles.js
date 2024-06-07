var popupc = false;

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

function popupview(element){
    const rgb2hex = (rgb) => `#${rgb.match(/^rgb\((\d+),\s*(\d+),\s*(\d+)\)$/).slice(1).map(n => parseInt(n, 10).toString(16).padStart(2, '0')).join('')}`
    var popup = document.getElementById('popup');
    popup.style.display = "block";
    var roleid = element.currentTarget.getAttribute('name');
    var rolename = element.currentTarget.children[0].getAttribute('id');
    var rolecolor = element.currentTarget.children[0].children[0].children[0].style.color;
    var popup_rname = document.getElementById('popup_rname');
    popup_rname.innerHTML = rolename
    popup_rname.setAttribute("class", roleid);
    var popup_color = document.getElementById('popup_color');
    popup_color.defaultValue = rgb2hex(String(rolecolor));
    // if (String(rolecolor) == ""){
    //     popup_color.defaultValue = "#ffffff";
    // }
    // else{
    //     popup_color.defaultValue = rgb2hex(String(rolecolor));
    // }
    $("body").css("overflow", "hidden");
}


function popupviewclose(){
    if (popupc == false){
        var popup = document.getElementById('popup');
        popup.style.display = "none";
        $("body").css("overflow", "auto");
    }
    else{
        popupc = false;
    }
}

function popupcontent(){
    popupc = true;
}

function rolecolor(element){
    var databar = document.getElementById("databar");
    var roleid = element.currentTarget.parentElement.parentElement.children[1].getAttribute('class');
    var color = String(element.currentTarget.value);
    $.getJSON("/change_role_color/"+String(roleid)+"/"+String(element.currentTarget.value).replace('#', ''), function() {}).done(function(data, textStatus, jqXHR){
        var response = jqXHR.responseText;
        if (JSON.parse(response)['status'] == 403){
            databar.innerHTML = `<ion-icon name="ban"></ion-icon> Error<br>Move the bot role above role trying to be edited`
            databar.style.padding = "2vh";
            databar.style.height = "8vh";
            databar.style.color = "white";
            databar.style.backgroundColor = "#ff3126";
            setTimeout(function() {
                databar.style.color = "transparent";
                databar.style.height = "0vh";
                databar.style.padding = "0vh";
            }, 10000);
        }
        else{
            var icon = document.getElementById(String(roleid));
            icon.style.color = color;
            databar.style.padding = "2vh";
            databar.style.height = "6vh";
            databar.style.color = "white";
            databar.innerHTML = `<ion-icon name="checkmark-circle"></ion-icon> Saved`
            databar.style.backgroundColor = "#28A745";
            setTimeout(function() {
                databar.style.color = "transparent";
                databar.style.height = "0vh";
                databar.style.padding = "0vh";
            }, 2000);
        }
    });
}

function set_role_name(element) {
    var rolename = document.getElementById("rolename").value;
    var roleid = element.currentTarget.parentElement.parentElement.children[1].getAttribute('class');
    $.getJSON("/set_role_name/"+String(roleid)+"/"+String(rolename), function() {}).done(function(data, textStatus, jqXHR){
        var response = jqXHR.responseText;
        if (JSON.parse(response)['status'] == 403){
            databar.innerHTML = `<ion-icon name="ban"></ion-icon> Error<br>Move the bot role above role trying to be edited`
            databar.style.padding = "2vh";
            databar.style.height = "8vh";
            databar.style.color = "white";
            databar.style.backgroundColor = "#ff3126";
            setTimeout(function() {
                databar.style.color = "transparent";
                databar.style.height = "0vh";
                databar.style.padding = "0vh";
            }, 10000);
        }
        else{
            var icon = document.getElementById(String(roleid));
            var popup_rname = document.getElementById("popup_rname");
            var splittext = icon.parentElement.innerHTML.split('>');
            var finaltext = `${splittext[0]}>${splittext[1]}> ${rolename}`
            icon.parentElement.innerHTML = finaltext;
            popup_rname.innerHTML = rolename;
            databar.style.padding = "2vh";
            databar.style.height = "6vh";
            databar.style.color = "white";
            databar.innerHTML = `<ion-icon name="checkmark-circle"></ion-icon> Saved`
            databar.style.backgroundColor = "#28A745";
            setTimeout(function() {
                databar.style.color = "transparent";
                databar.style.height = "0vh";
                databar.style.padding = "0vh";
            }, 2000);
        }
    });
}

window.onload=function(){
    var searchInput = document.getElementById('search');
    searchInput.addEventListener('keyup', search);

    var elements = document.getElementsByClassName('role');
    for (var element of elements){
        element.addEventListener('click', popupview);
    }

    var searchInput = document.getElementById('popup');
    searchInput.addEventListener('click', popupviewclose);

    var searchInput = document.getElementById('popup-content');
    searchInput.addEventListener('click', popupcontent);

    var searchInput = document.getElementById('popup_color');
    searchInput.addEventListener('change', rolecolor);

    var setnick = document.getElementById("setrolename");
    setnick.addEventListener('click', set_role_name);
}
