// Скрипт страницы `admin_users.html`
const MODAL = document.getElementById("adding-modal");

let modal_lock = false;

function showModal() {
  MODAL.showModal();
}

function closeModal() {
  if (!modal_lock) {
    MODAL.close();
    document.getElementById("adding-form").reset();
    document.getElementById("adding-response").classList.add("hidden");
    document.getElementById("submit-btn").classList.remove("hidden");
    document.getElementById("username-input").value = "";
    document.getElementById("username-input").readonly = false;
    document.getElementById("back-btn").classList.add("secondary");
    document.getElementById("back-btn").disabled = false;
  }
}

function addUser() {
  modal_lock = true;
  MODAL.setAttribute("closedby", "none");
  document.getElementById("adding-response").classList.remove("hidden");
  document.getElementById("submit-btn").classList.add("hidden");
  document.getElementById("username-input").readonly = true;
  document.getElementById("back-btn").classList.remove("secondary");
  document.getElementById("back-btn").disabled = true;
  setTimeout(() => {
    document.getElementById("back-btn").disabled = false;
    modal_lock = false;
  }, 3000);
}
