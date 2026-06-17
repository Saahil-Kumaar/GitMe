const analyzeButton =
    document.getElementById("analyze-btn");

const repoInput =
    document.getElementById("repo-url");


analyzeButton.addEventListener(
    "click",
    function () {

        const repoUrl =
            repoInput.value.trim();


        if (!repoUrl) {

            alert(
                "Please enter a GitHub repository URL."
            );

            return;
        }


        if (!repoUrl.includes("github.com")) {

            alert(
                "Please enter a valid GitHub repository URL."
            );

            return;
        }


        localStorage.setItem(
            "repositoryUrl",
            repoUrl
        );


        window.location.href =
            "/repository/?url=" +
            encodeURIComponent(repoUrl);

    }
);