const initPage = () => {
    const btn_send = document.getElementById("btn-send");
    if (btn_send) {
        btn_send.addEventListener("click", (e) => {
            const infos = document.querySelector(".all-inputs");
            const mots_inputs = infos.querySelectorAll(".inner-inputs");
            const data = {"mots": [], "defs": []};
            for (let i = 0; i< mots_inputs.length; i++) {
                data["mots"].push(mots_inputs[i].children[0].value);
                data["defs"].push(mots_inputs[i].children[1].value);
            }
            console.log(data);
            const hid_btn = document.getElementById("hidden-input");
            hid_btn.value = JSON.stringify(data);
        })
    }
}

const add_inp = () => {
    const btn_add = document.getElementById("btn-add-def");
    if (btn_add) {
        btn_add.addEventListener("click", () => {
            const div_inputs = document.querySelector(".all-inputs");
            div_inputs.insertAdjacentHTML("beforeend", `
            <div class="inner-inputs">
            <input type="text" id="mots_added" class="form-control mt-2 mx-3">
            <textarea type="text" id="def_added" class="form-control mt-2 input-lg"></textarea>
            </div>`);
        })
    }
}

add_inp();
initPage();




// const headers = {
//     'Content-Type': 'application/json',
//     'Accept': 'application/json'
// };
// fetch("http://localhost:5000/generate", {
//     method: "POST",
//     headers: headers,
//     body: JSON.stringify(data)
// })
// .then(response => response.json())
// .then(data => console.log(data))
// .catch(err => console.log(err));