
document.addEventListener("DOMContentLoaded", () => {
    // Elementos de los filtros del catálogo.
    const searchInput = document.getElementById("search");
    const categoryFilter = document.getElementById("category-filter");
    const priceFilter = document.getElementById("price-filter");
    const clearFiltersButton = document.getElementById("clear-filters");
    const restaurantGrid = document.getElementById("restaurant-grid");
    const restaurantCount = document.getElementById("restaurant-count");
    const noResults = document.getElementById("no-results");

    // Filtrar las tarjetas sin recargar toda la página.
    function filterRestaurants() {
        if (!restaurantGrid) return;

        const search = (searchInput?.value || "").trim().toLowerCase();
        const category = (categoryFilter?.value || "").toLowerCase();
        const price = priceFilter?.value || "";

        const cards = restaurantGrid.querySelectorAll(".restaurant-card");
        let visibleCount = 0;

        cards.forEach((card) => {
            const name = card.dataset.name || "";
            const city = card.dataset.city || "";
            const cardCategory = card.dataset.category || "";
            const cardPrice = card.dataset.price || "";

            const matchesSearch = name.includes(search) || city.includes(search);
            const matchesCategory = !category || cardCategory === category;
            const matchesPrice = !price || cardPrice === price;

            const visible =
                matchesSearch && matchesCategory && matchesPrice;

            card.hidden = !visible;

            if (visible) visibleCount++;
        });

        if (restaurantCount) {
            restaurantCount.textContent = visibleCount;
        }

        if (noResults) {
            noResults.hidden = visibleCount !== 0;
        }
    }

    searchInput?.addEventListener("input", filterRestaurants);
    categoryFilter?.addEventListener("change", filterRestaurants);
    priceFilter?.addEventListener("change", filterRestaurants);

    clearFiltersButton?.addEventListener("click", () => {
        if (searchInput) searchInput.value = "";
        if (categoryFilter) categoryFilter.value = "";
        if (priceFilter) priceFilter.value = "";
        filterRestaurants();
    });

    // Mostrar mensajes en el formulario.
    function showFormMessage(message, isError = false) {
        const messageElement = document.getElementById("form-message");

        if (!messageElement) return;

        messageElement.textContent = message;
        messageElement.hidden = false;
        messageElement.classList.toggle("error", isError);
    }

    // Crear o editar un restaurante utilizando la API.
    const restaurantForm = document.getElementById("restaurant-form");

    restaurantForm?.addEventListener("submit", async (event) => {
        event.preventDefault();

        const restaurantId = restaurantForm.dataset.restaurantId;
        const isEditing = Boolean(restaurantId);
        const submitButton = restaurantForm.querySelector(
            'button[type="submit"]'
        );

        const photoUrl = document.getElementById("photoUrl").value.trim();

        const data = {
            name: document.getElementById("name").value.trim(),
            category: document.getElementById("category").value.trim(),
            city: document.getElementById("city").value.trim(),
            price: Number(document.getElementById("price").value),
            photoUrl: photoUrl || null
        };

        if (submitButton) {
            submitButton.disabled = true;
            submitButton.textContent = "Guardando...";
        }

        try {
            const url = isEditing
                ? `/api/v1/restaurants/${encodeURIComponent(restaurantId)}`
                : "/api/v1/restaurants";

            const response = await fetch(url, {
                method: isEditing ? "PATCH" : "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(data)
            });

            const result = response.status === 204
                ? null
                : await response.json();

            if (!response.ok) {
                const detail = result?.detail;
                const message = Array.isArray(detail)
                    ? detail.map((item) => item.msg).join(", ")
                    : detail || "No se pudo guardar el restaurante.";

                throw new Error(message);
            }

            window.location.href = `/restaurants/${encodeURIComponent(result.id)}`;
        } catch (error) {
            showFormMessage(
                error.message || "Ocurrió un error al guardar.",
                true
            );
        } finally {
            if (submitButton) {
                submitButton.disabled = false;
                submitButton.textContent = isEditing
                    ? "Guardar cambios"
                    : "Crear restaurante";
            }
        }
    });

    // Eliminar desde la página de detalle.
    document.addEventListener("click", async (event) => {
        const deleteButton = event.target.closest("[data-delete-id]");

        if (!deleteButton) return;

        const restaurantId = deleteButton.dataset.deleteId;
        const restaurantName = deleteButton.dataset.deleteName || "este restaurante";

        const confirmed = window.confirm(
            `¿Seguro que deseas eliminar "${restaurantName}"? Esta acción no se puede deshacer.`
        );

        if (!confirmed) return;

        deleteButton.disabled = true;
        deleteButton.textContent = "Eliminando...";

        try {
            const response = await fetch(
                `/api/v1/restaurants/${encodeURIComponent(restaurantId)}`,
                { method: "DELETE" }
            );

            if (!response.ok) {
                let message = "No se pudo eliminar el restaurante.";

                try {
                    const result = await response.json();
                    message = result.detail || message;
                } catch {
                    // La respuesta podría no contener JSON.
                }

                throw new Error(message);
            }

            window.location.href = "/";
        } catch (error) {
            window.alert(error.message || "Ocurrió un error al eliminar.");

            deleteButton.disabled = false;
            deleteButton.textContent = "Eliminar";
        }
    });
});
