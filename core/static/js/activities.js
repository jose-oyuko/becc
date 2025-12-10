const input = document.getElementById("activity-input");
const addBtn = document.getElementById("add-activity-btn");
const container = document.getElementById("activities-container");
const hidden = document.getElementById("id_activities_json");

let activities = [];

// If editing, load existing activities
if (hidden.value) {
    try {
        activities = JSON.parse(hidden.value);
    } catch { }
}

function renderActivities() {
    container.innerHTML = "";
    activities.forEach((item, index) => {
        const tag = document.createElement("div");
        tag.className = "bg-green-100 text-green-800 px-3 py-1 rounded-full flex items-center gap-2";

        tag.innerHTML = `
                <span>${item}</span>
                <button type="button" class="text-red-500 font-bold">×</button>
            `;

        tag.querySelector("button").onclick = () => {
            activities.splice(index, 1);
            updateField();
            renderActivities();
        };

        container.appendChild(tag);
    });
}

function updateField() {
    hidden.value = JSON.stringify(activities);
}

addBtn.addEventListener("click", () => {
    console.log("btn clicked");
    if (!input.value.trim()) return;
    activities.push(input.value.trim());
    input.value = "";
    updateField();
    renderActivities();
});

input.addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
        e.preventDefault();
        addBtn.click();
    }
});

// Render initial (for edit)
renderActivities();