function toggleBio() {
    const shortBio = document.getElementById("bio-short");
    const fullBio = document.getElementById("bio-full");
    const toggleLink = document.getElementById("toggle-bio");

    if (fullBio.style.display === "none") {
        fullBio.style.display = "inline";
        shortBio.style.display = "none";
        toggleLink.innerText = "Свернуть";
    } else {
        fullBio.style.display = "none";
        shortBio.style.display = "inline";
        toggleLink.innerText = "Развернуть";
    }
}
