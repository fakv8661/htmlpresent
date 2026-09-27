// Скрипт страницы `admin_presentations.html`
const MODAL = document.getElementById("adding-modal");

let modal_lock = false;

function showModal() {
  MODAL.showModal();
  forceUpdateFileInputs();
}

function closeModal() {
  if (!modal_lock) {
    document.getElementById("adding-form").reset();
    MODAL.close();
  }
}

// Обновляет текст в .filename рядом с input-ом
function updateFileName(input, labelSpan) {
  const MAX_LENGTH = 24;

  const files = Array.from(input.files);
  if (files.length === 0) {
    labelSpan.textContent = "Прикрепить файл"; // текст по умолчанию
    return;
  }

  if (input.multiple && files.length > 1) {
    // несколько файлов — показываем количество и короткие имена
    const names = files.map((f) => f.name).join(", ");
    labelSpan.textContent = `${files.length} файлов`;
  } else {
    // один файл — просто имя
    labelSpan.textContent = files[0].name;
  }
  if (labelSpan.textContent.length > MAX_LENGTH) {
    labelSpan.textContent =
      labelSpan.textContent.slice(0, MAX_LENGTH - 1) + "…";
  }
}

// Привязываем обработчики к каждому input
function wireFileInputs() {
  const fileInput = document.getElementById("pres-file-input");
  const previewInput = document.getElementById("preview-file-input");
  const assetsInput = document.getElementById("assets-file-input");

  for (const input of [fileInput, previewInput, assetsInput]) {
    if (!input) continue;

    // label стоит перед input в разметке → ищем ближайший .filename
    const span =
      input.previousElementSibling?.querySelector(".filename") ??
      input.parentElement.querySelector(".filename");

    input.addEventListener("change", () => updateFileName(input, span));
  }
}

// Принудительно обновляет отображаемые имена для всех input-ов с файлами
function forceUpdateFileInputs() {
  const inputs = [
    document.getElementById("pres-file-input"),
    document.getElementById("preview-file-input"),
    document.getElementById("assets-file-input"),
  ];

  for (const input of inputs) {
    if (!input) continue;

    // label стоит перед input в разметке → ищем ближайший .filename
    const span =
      input.previousElementSibling?.querySelector(".filename") ??
      input.parentElement.querySelector(".filename");

    if (span) updateFileName(input, span);
  }
}

wireFileInputs();
