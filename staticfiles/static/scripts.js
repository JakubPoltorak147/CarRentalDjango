document.addEventListener("DOMContentLoaded", () => {
  console.log("Car Rental System is up and running!");

  // Animacje dla przyciskĂłw
  document.querySelectorAll(".btn-custom").forEach(button => {
    button.addEventListener("mouseenter", () => {
      button.style.transform = "scale(1.05)";
    });

    button.addEventListener("mouseleave", () => {
      button.style.transform = "scale(1)";
    });
  });
const form = document.getElementById("registration-form");

  form.addEventListener("submit", (event) => {
    let isValid = true;

    // Czyszczenie wcześniejszych komunikatów błędów
    const errorMessages = form.querySelectorAll(".error-message");
    errorMessages.forEach((error) => error.remove());

    const inputs = form.querySelectorAll(".form-control");
    inputs.forEach((input) => input.classList.remove("error"));

    const showError = (input, message) => {
      isValid = false;
      input.classList.add("error");
      const errorElement = document.createElement("div");
      errorElement.className = "error-message";
      errorElement.textContent = message;
      input.insertAdjacentElement("afterend", errorElement);
    };

    const nameRegex = /^[A-Za-z]+$/;
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    const phoneRegex = /^(\d{10}|\d{3}-\d{3}-\d{4})$/;
    const licenseRegex = /^[A-Za-z0-9]+$/;

    const firstname = document.getElementById("firstname");
    const lastname = document.getElementById("lastname");
    const username = document.getElementById("username");
    const password = document.getElementById("password");
    const email = document.getElementById("email");
    const mobile = document.getElementById("mobile");
    const license = document.getElementById("license");

    if (!firstname.value.trim() || !nameRegex.test(firstname.value.trim())) {
      showError(firstname, "First name can only contain letters and cannot be empty.");
    }

    if (!lastname.value.trim() || !nameRegex.test(lastname.value.trim())) {
      showError(lastname, "Last name can only contain letters and cannot be empty.");
    }

    if (username.value.trim().length < 5) {
      showError(username, "Username must be at least 5 characters long.");
    }

    if (password.value.trim().length < 8) {
      showError(password, "Password must be at least 8 characters long.");
    }

    if (!emailRegex.test(email.value.trim())) {
      showError(email, "Please enter a valid email address.");
    }

    if (!phoneRegex.test(mobile.value.trim())) {
      showError(mobile, "Contact number must be a valid 10-digit number or in the format 123-456-7890.");
    }

    if (!license.value.trim() || !licenseRegex.test(license.value.trim())) {
      showError(license, "Driver's License Number must be alphanumeric and cannot be empty.");
    }

    if (!isValid) {
      event.preventDefault();
    }
  });
});

document.addEventListener("DOMContentLoaded", () => {
  // ...

  // Prosty sort: załóżmy każda <th> ma data-sort="string" lub "int"
  document.querySelectorAll(".table-custom th").forEach(th => {
    th.addEventListener("click", () => {
      const table = th.closest("table");
      const body = table.querySelector("tbody");
      const rows = Array.from(body.querySelectorAll("tr"));
      const index = Array.from(th.parentNode.children).indexOf(th);
      const sortType = th.getAttribute("data-sort") || "string";

      // Wyróżnienie kolumny
      table.querySelectorAll("th").forEach(h => h.classList.remove("sorted-asc", "sorted-desc"));

      let ascending = !th.classList.contains("sorted-asc");
      th.classList.toggle("sorted-asc", ascending);
      th.classList.toggle("sorted-desc", !ascending);

      rows.sort((a, b) => {
        let A = a.children[index].innerText.trim();
        let B = b.children[index].innerText.trim();

        if (sortType === "int") {
          A = parseInt(A.replace(/\D/g, ""), 10) || 0;
          B = parseInt(B.replace(/\D/g, ""), 10) || 0;
        }

        if (A < B) return ascending ? -1 : 1;
        if (A > B) return ascending ? 1 : -1;
        return 0;
      });

      rows.forEach(r => body.appendChild(r));
    });
  });
});
