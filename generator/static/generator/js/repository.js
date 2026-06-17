async function analyzeRepository(repositoryUrl) {

    try {

        const response =
            await fetch(
                "/api/github/analyze/?url=" +
                encodeURIComponent(repositoryUrl)
            );

        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.error ||
                "Failed to analyze repository."
            );

        }


        console.log(
            "Repository data:",
            data
        );


        localStorage.setItem(
            "repositoryData",
            JSON.stringify(data)
        );


        return data;

    } catch (error) {

        console.error(
            "GitHub analysis failed:",
            error
        );

        alert(
            error.message
        );

        return null;
    }
}
document.addEventListener("DOMContentLoaded", () => {
    const params = new URLSearchParams(window.location.search);
    const repositoryUrl = params.get("url");

    if (repositoryUrl) {
        analyzeRepository(repositoryUrl);
    }
});