Telegram.WebApp.MainButton
    .setText("Valider")
    .show()
    .onClick(() => {
        Telegram.WebApp.sendData("ok");
    });

Telegram.WebApp.sendData(JSON.stringify({
    action: "COMMANDE",
    panier: panier
}))

document.getElementById("addressForm").addEventListener("submit", function(e) {
    e.preventDeflault();

    const clientData ={
        name: document.getElementById("name".value),
        street: document.getElementById("street").value,
        city: document.getElementById("city").value,
        phone: document.getElementById("phone").value
    };

    // on save temporairement les données
    localStorage.setItem("clientData", JSON.stringify(clientData));

    window.location.href ="menu.html";
});