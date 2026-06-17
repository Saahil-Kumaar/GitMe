const sectionCards =
    document.querySelectorAll(".section-card");

const continueButton =
    document.getElementById("sections-continue");


/* Restore saved sections */

const savedSections =
    JSON.parse(
        localStorage.getItem("sections") || "[]"
    );


if (savedSections.length > 0) {

    sectionCards.forEach(card => {

        const checkbox =
            card.querySelector("input");

        checkbox.checked =
            savedSections.includes(
                checkbox.value
            );

        card.classList.toggle(
            "selected",
            checkbox.checked
        );

    });

}


/* Select / deselect */

sectionCards.forEach(card => {

    const checkbox =
        card.querySelector("input");


    card.addEventListener("click", function () {

        checkbox.checked =
            !checkbox.checked;

        card.classList.toggle(
            "selected",
            checkbox.checked
        );

    });

});


/* Continue */

continueButton.addEventListener(
    "click",
    function () {

        const selectedSections =
            Array.from(
                document.querySelectorAll(
                    ".section-card input:checked"
                )
            ).map(
                checkbox => checkbox.value
            );


        if (selectedSections.length === 0) {

            alert(
                "Please select at least one section."
            );

            return;
        }


        localStorage.setItem(
            "sections",
            JSON.stringify(selectedSections)
        );


        window.location.href =
            "/screenshots/";

    }
);