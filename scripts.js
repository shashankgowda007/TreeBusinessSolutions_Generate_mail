// JavaScript to update progress bar on scroll
window.onscroll = function () {
    const winScroll = document.documentElement.scrollTop || document.body.scrollTop;
    const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    const scrolled = (winScroll / height) * 100;
    document.getElementById("myProgressBar").style.width = scrolled + "%";
};

const express = require('express');
const bodyParser = require('body-parser');

const app = express();
const port = 3000;

// Middleware to parse incoming form data
app.use(bodyParser.urlencoded({ extended: false }));

// Serve static files (index.html, styles.css, scripts.js)
app.use(express.static('public'));

// Route to handle form submission
app.post('/send_message', (req, res) => {
    const name = req.body.name;
    const email = req.body.email;
    const message = req.body.message;

    // Code to send the message (You can use email libraries or integrate with a messaging service)
    // For this example, we'll simply log the received message
    console.log('Received message:');
    console.log('Name:', name);
    console.log('Email:', email);
    console.log('Message:', message);

    // Return a success response to the frontend
    res.send('Message sent successfully!');
});

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});
document.addEventListener("DOMContentLoaded", function () {
    // Get the form element
    const contactForm = document.querySelector("form");

    // Add event listener for form submission
    contactForm.addEventListener("submit", function (event) {
        event.preventDefault(); // Prevent default form submission

        // Get form data
        const name = document.querySelector("input[name='name']").value;
        const email = document.querySelector("input[name='email']").value;
        const subject = document.querySelector("input[name='subject']").value;
        const message = document.querySelector("textarea[name='message']").value;

        // Compose the email body
        const body = `Name: ${name}\nEmail: ${email}\nSubject: ${subject}\nMessage: ${message}`;

        // Send the email using a simple mail-to link
        const mailtoLink = `mailto:myselfshashankgowda@gmail.com?subject=${encodeURIComponent(
            subject
        )}&body=${encodeURIComponent(body)}`;

        // Open the mail client with the email data
        window.open(mailtoLink);

        // Clear the form fields after submission
        contactForm.reset();
    });

    // Link icons to their respective URLs
    const facebookIcon = document.querySelector(".bx-bxl-facebook-circle");
    facebookIcon.parentElement.href = "https://www.facebook.com/profile.php?id=100049342447666";

    const instagramIcon = document.querySelector(".bx-bxl-instagram");
    instagramIcon.parentElement.href = "https://www.instagram.com/shashank_gowda._._/";

    const twitterIcon = document.querySelector(".bx-bxl-twitter");
    twitterIcon.parentElement.href = "https://twitter.com/cse000111";

    const linkedinIcon = document.querySelector(".bx-bxl-linkedin");
    linkedinIcon.parentElement.href = "https://www.linkedin.com/in/shashank-83623220b/";
});


