const repositoryElement =
    document.getElementById("review-repository");

const themeElement =
    document.getElementById("review-theme");

const technologiesElement =
    document.getElementById("review-technologies");

const sectionsElement =
    document.getElementById("review-sections");

const screenshotsElement =
    document.getElementById("review-screenshots");


// Repository

const repository =
    localStorage.getItem("repositoryUrl");

repositoryElement.textContent =
    repository || "Not provided";


// Theme

const theme =
    localStorage.getItem("selectedTheme") || "warm";

themeElement.textContent =
    theme.charAt(0).toUpperCase() +
    theme.slice(1);


// Technologies

const technologies =
    JSON.parse(
        localStorage.getItem("technologies") || "[]"
    );

technologiesElement.innerHTML = "";

technologies.forEach(technology => {

    const tag =
        document.createElement("span");

    tag.className = "review-tag";

    tag.textContent = technology;

    technologiesElement.appendChild(tag);

});


// Sections

const sections =
    JSON.parse(
        localStorage.getItem("sections") || "[]"
    );

sectionsElement.innerHTML = "";

sections.forEach(section => {

    const tag =
        document.createElement("span");

    tag.className = "review-tag";

    tag.textContent = section;

    sectionsElement.appendChild(tag);

});


// Screenshots

const screenshotCount =
    localStorage.getItem("screenshotCount") || 0;

screenshotsElement.textContent =
    `${screenshotCount} screenshot${
        screenshotCount == 1 ? "" : "s"
    }`;


// Generate

document
    .getElementById("generate-button")
    .addEventListener("click", function () {

        window.location.href =
            "/result/";

    });