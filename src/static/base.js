import {Language} from "./language.js"

function loadLanguages(){

    let selection = document.getElementById("languages;available_languages")

    lang = []

    for(const[i, language] of lang.entries()){
        let option = document.createElement("option");
        option.className = "selection-item-language"
        option.id = "option;" + language[i];
        option.index = i;
        option.onclick = function(){
            return false;
        }
        option.appendChild(document.createTextNode[lang[0]])
        selection.appendChild(option);
    }
    

}