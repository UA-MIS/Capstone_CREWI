import React, { useEffect } from 'react'

// this will load the widget in using the static files; this is not the actual widget
function WidgetEmbedded(props) {
    // runs whenever username is changed
    useEffect(() => {
        // 
        if (document.querySelector(".crewi_widget")) {
            const parent = document.querySelector(".crewi-embed");
            // apparently this doesn't remove event handlers or something? whatever lol
            parent.innerHTML = "";
        }

        const div = document.createElement("div");
        div.setAttribute("class", "crewi_widget");
        div.setAttribute("username", props.username);
        div.setAttribute("orderLink", props.orderLink);
        document.getElementsByClassName("crewi-embed")[0].appendChild(div);

        const jsScript = document.createElement("script");
        jsScript.setAttribute("class", "crewi_jsScript");
        jsScript.setAttribute("src", "https://cdn.jsdelivr.net/gh/stward1/crewiStaticFiles/static/js/main.a9ffa889.js");
        document.getElementsByClassName("crewi-embed")[0].appendChild(jsScript);

        const link = document.createElement("link");
        link.setAttribute("class", "crewi_css");
        link.setAttribute("href", "https://cdn.jsdelivr.net/gh/stward1/crewiStaticFiles/static/css/main.49542669.css");
        link.setAttribute("rel", "stylesheet");
        document.getElementsByClassName("crewi-embed")[0].appendChild(link);

        const script = document.createElement("script");
        script.setAttribute("class", "crewi_script");
        script.setAttribute("src", "https://cdn.jsdelivr.net/gh/stward1/crewiStaticFiles/static/js/787.d1453236.chunk.js");
        document.getElementsByClassName("crewi-embed")[0].appendChild(script);
        }, [props.username]);

        return (
        <section className="crewiWidget">
            <div className="crewi-embed"></div>
        </section>
        );
}

export default WidgetEmbedded;
