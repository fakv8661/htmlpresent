// Скрипт страницы `admin_login.html`

function togglePasswordVisibility() {
  const input = document.getElementById("password-input");
  const button = document.getElementById("password-toggle");

  button.classList.toggle("concealed");
  const isConcealed = button.classList.contains("concealed");
  if (isConcealed) {
    input.setAttribute("type", "password");
  } else {
    input.setAttribute("type", "text");
  }
}
