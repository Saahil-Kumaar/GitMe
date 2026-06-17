document.addEventListener("DOMContentLoaded", () => {
    const loadingSpinner = document.getElementById("loading-spinner");
    const previewContainer = document.getElementById("view-preview");
    const rawContainer = document.getElementById("view-raw");

    const btnTabPreview = document.getElementById("btn-tab-preview");
    const btnTabRaw = document.getElementById("btn-tab-raw");
    const btnCopy = document.getElementById("btn-copy");
    const btnDownload = document.getElementById("btn-download");

    let generatedMarkdown = "";

    // 1. Gather all wizard state from localStorage
    const repoDataString = localStorage.getItem("repositoryData");
    const theme = localStorage.getItem("selectedTheme") || "Modern";
    const technologies = JSON.parse(localStorage.getItem("selectedTechnologies") || "[]");
    const sections = JSON.parse(localStorage.getItem("selectedSections") || "[]");
    const screenshots = JSON.parse(localStorage.getItem("screenshots") || "[]");
    const customNotes = localStorage.getItem("customNotes") || "";

    if (!repoDataString) {
        loadingSpinner.innerHTML = `
            <h3 style="color: #e63946;">No repository found in memory.</h3>
            <p>You must start from the Home page so the app can fetch the repository data.</p>
            <a href="/" class="btn btn-primary" style="margin-top:1rem;">Go to Home</a>
        `;
        return;
    }

    const repoData = JSON.parse(repoDataString);

    // 2. Tab switching logic (toggling btn-primary / btn-secondary classes)
    btnTabPreview.addEventListener("click", () => {
        btnTabPreview.className = "btn-tab active";
        btnTabRaw.className = "btn-tab";
        previewContainer.style.display = "block";
        rawContainer.style.display = "none";
    });

    btnTabRaw.addEventListener("click", () => {
        btnTabRaw.className = "btn-tab active";
        btnTabPreview.className = "btn-tab";
        previewContainer.style.display = "none";
        rawContainer.style.display = "block";
    });

    // 3. Copy to Clipboard
    btnCopy.addEventListener("click", async () => {
        if (!generatedMarkdown) return;
        try {
            await navigator.clipboard.writeText(generatedMarkdown);
            const originalText = btnCopy.innerText;
            btnCopy.innerText = "Copied!";
            setTimeout(() => btnCopy.innerText = originalText, 2000);
        } catch (err) {
            alert("Failed to copy text: " + err);
        }
    });

    // 4. Download README.md File
    btnDownload.addEventListener("click", () => {
        if (!generatedMarkdown) return;
        const blob = new Blob([generatedMarkdown], { type: "text/markdown;charset=utf-8;" });
        const url = URL.createObjectURL(blob);
        const link = document.createElement("a");
        link.href = url;
        link.download = "README.md";
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
    });

    // 5. Trigger Generation API
    async function executeGeneration() {
        try {
            const response = await fetch("/api/generate/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    url: repoData.html_url,
                    theme: theme,
                    technologies: technologies,
                    sections: sections,
                    screenshots: screenshots,
                    custom_notes: customNotes
                })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || "Failed to generate README.");
            }

            generatedMarkdown = data.readme;

            // Render Markdown using marked.js
            if (typeof marked !== 'undefined') {
                previewContainer.innerHTML = marked.parse(generatedMarkdown);
            } else {
                previewContainer.innerHTML = `<pre>${generatedMarkdown}</pre>`;
            }
            rawContainer.value = generatedMarkdown;

            // Reveal results
            loadingSpinner.style.display = "none";
            previewContainer.style.display = "block";

        } catch (error) {
            console.error("README Generation failed:", error);
            loadingSpinner.innerHTML = "";

            const errorMessage = document.createElement("p");
            errorMessage.style.color = "#e63946";
            errorMessage.style.fontWeight = "bold";
            errorMessage.textContent = `Error: ${error.message}`;

            const retryButton = document.createElement("button");
            retryButton.className = "secondary-button";
            retryButton.textContent = "Retry";
            retryButton.addEventListener("click", () => location.reload());

            loadingSpinner.append(errorMessage, retryButton);
        }
    }

    executeGeneration();
});