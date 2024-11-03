// user_info.html
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


// user_info.html
function toggleDescriptionProject(counter) {
    const shortDesc = document.getElementById(`description-short-${counter}`);
    const fullDesc = document.getElementById(`description-full-${counter}`);
    const toggleLink = document.getElementById(`toggle-description-${counter}`);

    if (fullDesc.style.display === "none") {
        fullDesc.style.display = "inline";
        shortDesc.style.display = "none";
        toggleLink.innerText = "Свернуть";
    } else {
        fullDesc.style.display = "none";
        shortDesc.style.display = "inline";
        toggleLink.innerText = "Развернуть";
    }
}


// project_info.html
function toggleDescription(counter) {
    const shortDesc = document.getElementById(`sub-desc-short-${counter}`);
    const fullDesc = document.getElementById(`sub-desc-full-${counter}`);
    const toggleLink = document.getElementById(`toggle-desc-${counter}`);

    if (fullDesc.style.display === "none") {
        fullDesc.style.display = "inline";
        shortDesc.style.display = "none";
        toggleLink.innerText = "Свернуть";
    } else {
        fullDesc.style.display = "none";
        shortDesc.style.display = "inline";
        toggleLink.innerText = "Развернуть";
    }
}


function toggleInfo() {
    const short = document.getElementById("short");
    const full = document.getElementById("full");
    const toggle = document.getElementById("toggle");

    if (full.style.display === "none") {
        full.style.display = "inline";
        short.style.display = "none";
        toggle.innerText = "Свернуть";
    } else {
        full.style.display = "none";
        short.style.display = "inline";
        toggle.innerText = "Развернуть";
    }
}