// Скрипт страницы `main_page.html`

//#region !!! DANGER: ВАЙБКОД !!!
function downloadFile(filename, content, mimeType = "text/plain") {
  // Создаём Blob с содержимым
  const blob = new Blob([content], { type: mimeType });

  // Создаём временную ссылку
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = filename; // например: 'report.txt'

  // Добавляем в DOM, кликаем и удаляем
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);

  // Освобождаем память
  URL.revokeObjectURL(url);
}

/**
 * Преобразует произвольный текст в корректное имя файла,
 * безопасное для Windows, macOS и Linux.
 *
 * @param {string} text - Исходный текст
 * @param {object} [options] - Опции
 * @param {string} [options.replacement='_'] - Чем заменять недопустимые символы
 * @param {number} [options.maxLength=255] - Максимальная длина имени (без расширения)
 * @param {string} [options.fallback='file'] - Имя, если после очистки ничего не осталось
 * @param {boolean} [options.preserveExtension=true] - Сохранять ли расширение файла
 * @returns {string} Корректное имя файла
 */
function toSafeFileName(text, options = {}) {
  const {
    replacement = "_",
    maxLength = 255,
    fallback = "file",
    preserveExtension = true,
  } = options;

  if (text == null) return fallback;

  let name = String(text).normalize("NFC");

  // Запрещённые символы в Windows: < > : " / \ | ? * и управляющие (0x00–0x1F)
  // Плюс запрещаем точку и пробел в начале/конце (проблемы в Windows).
  const invalidChars = /[<>:"/\\|?*\u0000-\u001F]/g;
  name = name.replace(invalidChars, replacement);

  // Заменяем пробелы идущие подряд и другие "белые" символы
  name = name.replace(/\s+/g, " ").trim();

  // Убираем точки и пробелы в начале и конце
  name = name.replace(/^[.\s]+|[.\s]+$/g, "");

  // Схлопываем повторяющиеся замены
  if (replacement) {
    const re = new RegExp(
      replacement.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + "+",
      "g",
    );
    name = name.replace(re, replacement);
  }

  if (!name) name = fallback;

  // Зарезервированные имена в Windows (CON, PRN, AUX, NUL, COM1-9, LPT1-9)
  const reserved = /^(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])$/i;

  let baseName = name;
  let ext = "";

  if (preserveExtension) {
    const dotIndex = name.lastIndexOf(".");
    if (dotIndex > 0 && dotIndex < name.length - 1) {
      baseName = name.slice(0, dotIndex);
      ext = name.slice(dotIndex); // включает точку
    }
  }

  if (reserved.test(baseName)) {
    baseName = replacement ? baseName + replacement : baseName + "_";
  }

  // Ограничение длины
  const maxBase = Math.max(1, maxLength - ext.length);
  if (baseName.length > maxBase) {
    baseName = baseName.slice(0, maxBase).replace(/[.\s]+$/g, "");
  }

  // Дополнительная защита: имя не должно заканчиваться точкой (Windows)
  baseName = baseName.replace(/[.\s]+$/g, "") || fallback;

  return baseName + ext;
}
//#endregion

// Элементы
let presentationModal = document.getElementById("presentation-modal");
let table = document.getElementById("presentations-table");
let search_stats = document.getElementById("found-result");

// Переменные
let presentations = [];

window.onload = onLoad;
table.innerHTML = "";

// Запрос на сервер
async function onLoad() {
  const response = await fetch("/pres");
  if (response.ok) {
    const json = await response.json();
    presentations = json;
  } else {
    console.error("Server request failed.");
  }
  updatePresentions();
}

// Обработка ввода в поле поиска
document.getElementById("searchbar").oninput = (e) => {
  const SEARCH = document.getElementById("searchbar").value;
  updatePresentions(SEARCH);
};

// Закрытие модального окна по клику за его пределами
presentationModal.addEventListener("click", (e) => {
  if (presentationModal.open) {
    const rect = presentationModal.getBoundingClientRect();
    const outside =
      e.clientX < rect.left ||
      e.clientX > rect.right ||
      e.clientY < rect.top ||
      e.clientY > rect.bottom;

    if (outside) {
      presentationModal.close();
    }
  }
});

// Функция для отображения модального окна
async function showModal(id) {
  const current = presentations.find((value) => value.id == id);

  const ENDPOINT = `/pres/${current.id}`;

  document.getElementById("presentation-download").onclick = async (e) => {
    const FILE = await fetch(ENDPOINT);
    const TEXT = await FILE.text();
    downloadFile(toSafeFileName(current.title) + ".html", TEXT, "text/html");
  };

  const previewWrapper = document.getElementById("modal-preview-wrapper");
  if (current.cover !== null) {
    if (previewWrapper.classList.contains("hidden")) {
      previewWrapper.classList.remove("hidden");
    }
    document.getElementById("modal-preview").src = current.cover;
  } else {
    if (!previewWrapper.classList.contains("hidden")) {
      previewWrapper.classList.add("hidden");
    }
  }
  document.getElementById("presentation-view").href = ENDPOINT;
  document.getElementById("modal-title").innerText = current.title;
  document.getElementById("modal-authors").innerText = current.authors;
  document.getElementById("modal-description").innerText = current.description;
  presentationModal.showModal();
}

// Функция для обновления списка презентаций
async function updatePresentions(search = "") {
  let resultCount = 0;

  let resultHTML = "";
  presentations.forEach((value) => {
    const type = value.file_type.trim();
    const row = `
      <tr class="clickable-row" onclick="showModal(${value.id})">
      <th scope="row" class="th-title">
      <span class="format-icon ${type.toLowerCase()}">
      ${type.toUpperCase()}
      </span>
      ${value.title}
      </th>
      <td>${value.authors}</td>
      <!-- <td>-</td> -->
      <!-- <td>-</td> -->
      </tr>
      `;

    if (
      search === "" ||
      value.title.toLowerCase().includes(search.toLowerCase()) ||
      value.authors.toLowerCase().includes(search.toLowerCase()) ||
      value.description.toLowerCase().includes(search.toLowerCase())
    ) {
      resultHTML += row;
      resultCount += 1;
    }
  });

  if (resultCount === 0) {
    document.getElementById("table-wrapper").hidden = true;
    search_stats.innerText = "Ничего не найдено";
  } else if (resultCount === presentations.length) {
    document.getElementById("table-wrapper").hidden = false;
    search_stats.innerText = `Всего ${resultCount} презентаций`;
  } else {
    document.getElementById("table-wrapper").hidden = false;
    search_stats.innerText = `Найдено ${resultCount} презентаций`;
  }

  table.innerHTML = resultHTML;
}

// $("#achievements-btn").click(function (e) {
//   e.preventDefault();

//   window.location.href = "/achievements";
// });
