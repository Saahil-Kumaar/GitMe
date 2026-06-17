const technologyCards =
    document.querySelectorAll(".tech-card");

const continueButton =
    document.getElementById("technology-continue");


/* Restore previously selected technologies */

const savedTechnologies =
    JSON.parse(
        localStorage.getItem("technologies") || "[]"
    );


technologyCards.forEach(card => {

    const checkbox =
        card.querySelector("input");

    if (
        savedTechnologies.includes(
            checkbox.value
        )
    ) {
        checkbox.checked = true;
    }


    card.addEventListener("click", function () {

        checkbox.checked =
            !checkbox.checked;

    });

});


/* Continue */

continueButton.addEventListener("click", function () {

    const selected =
        Array.from(
            document.querySelectorAll(
                ".tech-card input:checked"
            )
        ).map(
            checkbox => checkbox.value
        );


    localStorage.setItem(
        "technologies",
        JSON.stringify(selected)
    );


    window.location.href =
        "/sections/";

});