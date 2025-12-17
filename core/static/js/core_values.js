document.addEventListener("DOMContentLoaded", function () {
    const hiddenInput = document.getElementById("id_core_values_json");
    if (!hiddenInput) return;

    const listContainer = document.getElementById("core-values-list");
    const addBtn = document.getElementById("add-core-value-btn");

    // Load initial data
    let currentData = JSON.parse(hiddenInput.value || "[]");

    function render() {
        listContainer.innerHTML = "";
        currentData.forEach((item, index) => {
            const row = document.createElement("div");
            row.className = "flex gap-4 items-start bg-gray-50 p-4 rounded-lg border border-gray-200 moving-border-animation";
            row.innerHTML = `
                <div class="flex-1 space-y-2">
                    <input type="text" placeholder="Title (e.g. Co-operation)" 
                           class="w-full p-2 border rounded focus:ring-2 focus:ring-green-500 font-bold text-gray-800"
                           value="${item.title || ''}" data-index="${index}" data-field="title">
                    <textarea placeholder="Description" rows="2"
                              class="w-full p-2 border rounded focus:ring-2 focus:ring-green-500 text-sm text-gray-600"
                              data-index="${index}" data-field="description">${item.description || ''}</textarea>
                </div>
                <button type="button" class="text-red-500 hover:text-red-700 p-2" onclick="removeCoreValue(${index})">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
                    </svg>
                </button>
            `;
            listContainer.appendChild(row);
        });
        updateHiddenInput();
    }

    // Expose remove function globally
    window.removeCoreValue = function (index) {
        currentData.splice(index, 1);
        render();
    };

    addBtn.addEventListener("click", function () {
        currentData.push({ title: "", description: "" });
        render();
    });

    // Update data when inputs change
    listContainer.addEventListener("input", function (e) {
        if (e.target.dataset.index) {
            const index = e.target.dataset.index;
            const field = e.target.dataset.field;
            currentData[index][field] = e.target.value;
            updateHiddenInput();
        }
    });

    function updateHiddenInput() {
        hiddenInput.value = JSON.stringify(currentData);
    }

    render();
});
