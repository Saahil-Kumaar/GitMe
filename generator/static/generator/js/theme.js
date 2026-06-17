const themeCards =
    document.querySelectorAll(".theme-card-new");

const continueButton =
    document.getElementById("theme-continue");


let selectedTheme =
    localStorage.getItem("selectedTheme") || "warm";


/* Restore selected theme */

themeCards.forEach(card => {

    if (card.dataset.theme === selectedTheme) {
        card.classList.add("selected");
    } else {
        card.classList.remove("selected");
    }

});


/* Select theme */

themeCards.forEach(card => {

    card.addEventListener("click", function () {

        themeCards.forEach(item => {
            item.classList.remove("selected");
        });

        card.classList.add("selected");

        selectedTheme =
            card.dataset.theme;

        localStorage.setItem(
            "selectedTheme",
            selectedTheme
        );

    });

});


/* Continue */

continueButton.addEventListener("click", function () {

    localStorage.setItem(
        "selectedTheme",
        selectedTheme
    );

    window.location.href =
        "/technologies/";

});