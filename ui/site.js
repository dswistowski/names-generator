const button = document.getElementById("button");
const namePlaceholder = document.getElementById("namePlaceholder");

let isUpdating = false;
const updateName = () => {
    if (isUpdating) return;
    isUpdating = true;
    fetch("/api/name").then(function (response) {
        return response.json();
    }).then(function (data) {
        namePlaceholder.innerHTML = data.name;
    }).finally(() => isUpdating = false);
}

button.addEventListener("click", updateName);
updateName();