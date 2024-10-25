const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
        console.log(entry);
        if (entry.intersectionRatio > 0) {
            entry.target.classList.add('show');
        } else {
            entry.target.classList.remove('show');
        }
    });
});

const hiddenElements = document.querySelectorAll('.hidden');
hiddenElements.forEach((el) => observer.observe(el));

function sendMail(){
    var name = document.getElementById("name").value;
    var email = document.getElementById("email").value;
    var message = document.getElementById("message").value;

    if (email.trim() === "" || message.trim() === "" || name.trim() === "") {
        alert("Please fill in all fields");
        return;
    }

    var params = {
        name: name,
        email: email,
        message: message,
    };

    const serviceID = "service_d65zr5v";
    const templateID = "template_e0qy7ej";

    emailjs.send(serviceID, templateID, params)
        .then(res => {
            document.getElementById("name").value = "";
            document.getElementById("email").value = "";
            document.getElementById("message").value = "";
            console.log(res);
            alert("Your message has been sent successfully");
        })
        .catch((err) => console.log(err));
}

