document.getElementById('profileIcon').addEventListener('click', function () {
    document.getElementById('profileDropdown').classList.toggle('active');
});

// Close the dropdown if the user clicks outside of it
window.addEventListener('click', function (event) {
    if (!event.target.matches('#profileIcon') && !event.target.closest('#profileIcon')) {
        var dropdowns = document.getElementsByClassName("dropdown-menu");
        for (var i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('active')) {
                openDropdown.classList.remove('active');
            }
        }
    }
});

const image = document.getElementById('id_cert_image')
const preview = document.getElementById('preview')
image.addEventListener('change', () => {
    const [file] = image.files
    if (file) {
        preview.src = URL.createObjectURL(file)
        preview.classList.remove('hidden')
    }
})
if (preview.getAttribute('src')) {
        preview.classList.remove('hidden');
    }