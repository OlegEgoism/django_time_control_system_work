// user_info.html -- Биография
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


// user_info.html -- Участие в проектах
function toggleDescriptionProject(counter) {
    const shortDescPro = document.getElementById(`description-short-${counter}`);
    const fullDescPro = document.getElementById(`description-full-${counter}`);
    const toggleLink = document.getElementById(`toggle-description-${counter}`);

    if (fullDescPro.style.display === "none") {
        fullDescPro.style.display = "inline";
        shortDescPro.style.display = "none";
        toggleLink.innerText = "Свернуть";
    } else {
        fullDescPro.style.display = "none";
        shortDescPro.style.display = "inline";
        toggleLink.innerText = "Развернуть";
    }
}


// subdivision_list.html -- Подразделения
function toggleDescriptionSub(counter) {
    const shortSub = document.getElementById(`sub-short-${counter}`);
    const fullSub = document.getElementById(`sub-full-${counter}`);
    const toggleSub = document.getElementById(`sub-toggle-${counter}`);

    if (fullSub.style.display === "none") {
        fullSub.style.display = "inline";
        shortSub.style.display = "none";
        toggleSub.innerText = "Свернуть";
    } else {
        fullSub.style.display = "none";
        shortSub.style.display = "inline";
        toggleSub.innerText = "Развернуть";
    }
}


// project_info.html
function toggleDescription() {
    const shortDesc = document.getElementById('short-description');
    const fullDesc = document.getElementById('full-description');
    const toggleLink = document.getElementById('toggle-description');

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

// project_list.html
function toggleDescriptionProd(counter) {
    const shortDescProd = document.getElementById(`short-desc-${counter}`);
    const fullDescProd = document.getElementById(`full-desc-${counter}`);
    const toggleLinkProd = document.getElementById(`toggle-desc-${counter}`);

    if (fullDescProd.style.display === "none") {
        fullDescProd.style.display = "inline";
        shortDescProd.style.display = "none";
        toggleLinkProd.innerText = "Свернуть";
    } else {
        fullDescProd.style.display = "none";
        shortDescProd.style.display = "inline";
        toggleLinkProd.innerText = "Развернуть";
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