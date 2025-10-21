document.addEventListener('DOMContentLoaded', function() {
    const sortElement = document.getElementById('sort');
    if (sortElement) {
        sortElement.addEventListener('change', function() {
            const sortCriteria = this.value;

            fetch(`${pinsUrl}?sort=${sortCriteria}`, {
                method: 'GET',
                headers: { 'X-Requested-With': 'XMLHttpRequest' }
            })
            .then(response => response.text())
            .then(html => {
                document.getElementById('pins-container').innerHTML = html;
            })
            .catch(error => console.error(error));
        });
    }
});
