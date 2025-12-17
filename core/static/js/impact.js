const input = document.getElementById("impact-input");
const addBtn = document.getElementById("add-impact-btn");
const container = document.getElementById("impact-container");
const hidden = document.getElementById("id_impact_json");

let impactItems = [];

// If editing, load existing Items
if (hidden.value) {
    try {
        impactItems = JSON.parse(hidden.value);
    } catch { }
}

function renderImpactItems() {
    container.innerHTML = "";
    impactItems.forEach((item, index) => {
        const tag = document.createElement("div");
        tag.className = "bg-blue-100 text-blue-800 px-3 py-1 rounded-full flex items-center gap-2";

        tag.innerHTML = `
                <span>${item}</span>
                <button type="button" class="text-red-500 font-bold">×</button>
            `;

        tag.querySelector("button").onclick = () => {
            impactItems.splice(index, 1);
            updateField();
            renderImpactItems();
        };

        container.appendChild(tag);
    });
}

function updateField() {
    hidden.value = JSON.stringify(impactItems);
}

if (addBtn) {
    addBtn.addEventListener("click", () => {
        if (!input.value.trim()) return;
        impactItems.push(input.value.trim());
        input.value = "";
        updateField();
        renderImpactItems();
    });
}

if (input) {
    input.addEventListener("keypress", (e) => {
        if (e.key === "Enter") {
            e.preventDefault();
            addBtn.click();
        }
    });
}

// Render initial (for edit)
if (container) {
    renderImpactItems();
}
