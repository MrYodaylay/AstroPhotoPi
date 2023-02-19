
function onLoad() {

    fetch("/api/cameras")
        .then((response) => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            return response.text();
        }).then((text) => {
                selecter = document.getElementById("config_camera_select");
                selecter.appendChild(new Option(text));
        })


}

window.addEventListener("DOMContentLoaded", onLoad);
