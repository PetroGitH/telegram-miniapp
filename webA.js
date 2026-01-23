Telegram.WebApp.MainButton
    .setText("Valider")
    .show()
    .onClick(() => {
        Telegram.WebApp.sendData("ok");
    });