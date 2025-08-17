function confirmDelete(id) {
    if (confirm("Are you sure you want to delete this device?")) {
        window.location.href = "/delete/" + id;
    }
}