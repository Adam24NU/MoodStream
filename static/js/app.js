// Save a playlist to the server
function savePlaylist(name, url, image) {
    fetch("/playlist/save_playlist", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({name, url, image})
    })
    .then(res => res.json())
    .then(data => {
        // Handle response statuses
        if (data.status === "ok") {
            console.log("Playlist saved!");
        } else if (data.status === "exists") {
            console.log("Already saved!");
        } else {
            console.log("Error:", data.message);
        }
    });
}

// Delete a saved playlist
function deletePlaylist(url) {
    fetch("/playlist/delete", {
        method: "DELETE",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url: url })
    })
    .then(res => res.json())
    .then(data => {
        // Handle delete operation result
        if (data.status === "ok") {
            console.log("Deleted");
        } else {
            console.log("Error:", data.message);
        }
    });
}

// Toggle between saving and unsaving a playlist
function toggleSave(button, name, url, image) {
    const icon = button.querySelector("i");
    const isSaved = button.dataset.saved === "true";

    if (isSaved) {
        // If currently saved, delete it
        deletePlaylist(url);
        button.dataset.saved = "false";
        icon.classList.remove("bi-suit-heart-fill");
        icon.classList.add("bi-suit-heart");
        console.log("Deleted:", name);
    } else {
        // If not saved, save it
        savePlaylist(name, url, image);
        button.dataset.saved = "true";
        icon.classList.remove("bi-suit-heart");
        icon.classList.add("bi-suit-heart-fill");
        console.log("Saved:", name);
    }
}

// Close flash alert with fade-out animation
function closeFlash(btn) {
    const box = btn.parentElement;
    box.style.opacity = "0";
    // Wait for fade-out before removing element
    setTimeout(() => box.remove(), 300);
}

// Run scripts after page load
document.addEventListener("DOMContentLoaded", () => {

    // ========== SHOW / HIDE PASSWORD ==========
    document.querySelectorAll(".toggle-password").forEach(btn => {
        btn.addEventListener("click", () => {
            // Target input field associated with this toggle button
            const targetId = btn.getAttribute("data-target");
            const input = document.getElementById(targetId);

            // Toggle password visibility
            if (input.type === "password") {
                input.type = "text";
                btn.innerHTML = "<i class=\"bi bi-eye-slash\"></i>";
            } else {
                input.type = "password";
                btn.innerHTML = "<i class=\"bi bi-eye\"></i>";
            }
        });
    });


    // ========== PASSWORD VALIDATION AND HINTS ==========
    const passwordInput = document.getElementById("password");
    if (passwordInput) {

        // Elements representing each password rule
        const len = document.getElementById("len");
        const upper = document.getElementById("upper");
        const lower = document.getElementById("lower");
        const digit = document.getElementById("digit");

        // Validation rules list
        const rules = [
            { element: len, check: v => v.length >= 8 },
            { element: upper, check: v => /[A-Z]/.test(v) },
            { element: lower, check: v => /[a-z]/.test(v) },
            { element: digit, check: v => /\d/.test(v) },
        ];

        // Update rule hints as user types
        passwordInput.addEventListener("input", () => {
            const value = passwordInput.value;

            rules.forEach(rule => {
                const ok = rule.check(value);
                // Hide rule when satisfied
                rule.element.classList.toggle("hidden", ok);
            });
        });
    }
});
