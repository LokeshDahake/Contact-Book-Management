function deleteContact(contactId) {
    if (confirm("Are you sure you want to delete this contact?")) {
        fetch(`/delete/${contactId}`, { method: 'DELETE' })
            .then(response => {
                if (response.ok) {
                    location.reload();
                } else {
                    alert('Failed to delete contact.');
                }
            });
    }
}