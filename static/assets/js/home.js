const prefix = "static/images/sponsors/";

const imageSources = [
    prefix + "99_3_Radio_layered.jpeg",
    prefix + "All_Saints_Episcopal_Church_Logo.png",
    prefix + "Bethel_AME_logo.png",
    prefix + "Logo - HDFC.jpeg",
    prefix + "New_Progressive_Church_Logo.jpeg",
    prefix + "CGLaw-Logo.png",
    prefix + "faith_mission_logo.jpeg",
    prefix + "grace_life_logo.jpeg",
    prefix + "new_directions_logo.jpeg",
    prefix + "oxnard_family_circle_logo.jpeg",
    prefix + "zion_logo.jpeg",
    prefix + "miracle_center_logo.jpeg",
];

function cycleSponsorLogos() {
    const randomLogo = imageSources[Math.floor(Math.random() * imageSources.length)];
    const sponsorImage = document.getElementById("sponsor");
    sponsorImage.setAttribute("src", randomLogo);
    setTimeout(cycleSponsorLogos, 5000);
};

window.onload = cycleSponsorLogos;