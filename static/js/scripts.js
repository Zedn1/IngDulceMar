document.addEventListener("DOMContentLoaded", function () {
    const detailsSection = document.getElementById("details-section");
    const viewDetailsButton = document.querySelector(".btn-view");

    viewDetailsButton.addEventListener("click", function () {
        detailsSection.style.display =
            detailsSection.style.display === "none" || detailsSection.style.display === ""
                ? "block"
                : "none";
    });
});
