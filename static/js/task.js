// SELECTORS
const buttons = document.querySelectorAll(".card-footer");

// EVENT LISTENERS
for (const button of buttons) {
  button.addEventListener("click", deleteCheck);
}

// FUNCTIONS
function deleteCheck(event) {
  const item = event.target;
  const todo = item.closest(".card");
  // Delete the todo
  if (item.classList[0] === "trash-btn") {
    // Animation
    todo.classList.add("fall");
    todo.addEventListener("transitionend", function () {
      todo.remove();
    });
  }

  // Mark as done
  if (item.classList[0] === "complete-btn") {
    todo.classList.toggle("completed");
  }
}
