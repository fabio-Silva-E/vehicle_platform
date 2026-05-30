document.addEventListener("DOMContentLoaded", function () {

    const searchForm =
        document.getElementById("searchForm");

    const filterForm =
        document.getElementById("sidebarFilterForm");

    const carsContainer =
        document.getElementById("carsContainer");

    let timeout = null;

    // 🔥 carrega anúncios AJAX
    function loadCars(customUrl = null) {

    const params = new URLSearchParams();

    if (searchForm) {

        const searchData = new FormData(searchForm);

        for (const [key, value] of searchData.entries()) {
            params.append(key, value);
        }
    }

    if (filterForm) {

        const filterData = new FormData(filterForm);

        for (const [key, value] of filterData.entries()) {
            params.append(key, value);
        }
    }

    const url = customUrl ||
        `${window.location.pathname}?${params.toString()}`;

    fetch(url, {
        headers: {
            "X-Requested-With": "XMLHttpRequest"
        }
    })
    .then(response => response.json())
    .then(data => {

        carsContainer.innerHTML = data.html;

    });

}

    // 🔥 busca digitando
    if (searchForm) {

        const searchInput =
            searchForm.querySelector('input[name="q"]');

        if (searchInput) {

            searchInput.addEventListener("keyup", function () {

                clearTimeout(timeout);

                timeout = setTimeout(function () {

                    loadCars();

                }, 400);

            });

        }

    }

    // 🔥 filtros sidebar
    if (filterForm) {

        const selects =
            filterForm.querySelectorAll("select");

        selects.forEach(select => {

            select.addEventListener("change", function () {

                loadCars();

            });

        });

    }

});