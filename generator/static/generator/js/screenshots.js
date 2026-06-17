const input =
    document.getElementById("screenshot-input");

const preview =
    document.getElementById("screenshot-preview");

const continueButton =
    document.getElementById("screenshots-continue");

let screenshots = [];


input.addEventListener("change", function () {

    screenshots = Array.from(input.files);

    preview.innerHTML = "";

    screenshots.forEach((file, index) => {

        const reader = new FileReader();

        reader.onload = function (event) {

            const card =
                document.createElement("div");

            card.className =
                "screenshot-card";

            card.innerHTML = `
                <img src="${event.target.result}">
                <span>${file.name}</span>
            `;

            preview.appendChild(card);
        };

        reader.readAsDataURL(file);

    });

});


continueButton.addEventListener("click", function () {

    localStorage.setItem(
        "screenshotCount",
        screenshots.length
    );

    window.location.href =
        "/review/";

});