const initPage = () => {
    const btn_send = document.getElementById("btn-send");
    if (btn_send) {
        btn_send.addEventListener("click", () => {
            const infos = document.querySelector(".all-inputs");
            const mots_inputs = infos.querySelectorAll(".inner-inputs");
            const data = {"mots": [], "defs": []};
            for (let i = 0; i< mots_inputs.length; i++) {
                data["mots"].push(mots_inputs[i].children[0].value);
                data["defs"].push(mots_inputs[i].children[1].value);
            }
            const headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            };
            fetch("http://localhost:5000/generate", {
                method: "POST",
                headers: headers,
                body: JSON.stringify(data)
            })
        })
    }
}

initPage();