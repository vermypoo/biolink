document.addEventListener("DOMContentLoaded", function() {
    const overlay = document.getElementById("overlay")
    const enterButton = document.getElementById("enterButton")
    const backgroundVideo = document.getElementById("backgroundVideo")
    const theme = "chill"

    backgroundVideo.controls = false

    if (theme == "chill") {
        backgroundVideo.src = "https://ibb.co/7QHFj3v"
    } 

    if (theme == "central") {
        backgroundVideo.src = "https://ibb.co/7QHFj3v"
    } 

    if (theme == "drill") {
        backgroundVideo.src = "https://ibb.co/7QHFj3v"
    }

    if (theme == "rap") {
        backgroundVideo.src = "https://ibb.co/7QHFj3v"
    }

    enterButton.addEventListener("click", function() {
        backgroundVideo.play()
        overlay.style.visibility = "hidden"
        overlay.style.opacity = 0
    })
})

function Scroll(text) {
    document.title = text;
    
    setTimeout(function() {
        Scroll(text.substr(1) + text.substr(0, 1));
    }, 300);
}

Scroll(" catboys4.life <3")