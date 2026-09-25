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

const MODAL = document.getElementById("presentation-modal");
MODAL.addEventListener("click", (e) => {
  if (MODAL.open) {
    const rect = MODAL.getBoundingClientRect();
    const outside =
      e.clientX < rect.left ||
      e.clientX > rect.right ||
      e.clientY < rect.top ||
      e.clientY > rect.bottom;

    if (outside) {
      MODAL.close();
    }
  }
});

async function showModal(id) {
  const response = await fetch("/presentations");

  if (response.ok) {
    MODAL.showModal();
    const json = await response.json();
    let current = null;
    json.forEach((value) => {
      if (value.id == id) {
        current = value;
      }
    });

    const ENDPOINT = `/presentation/${current.id}`;
    const FILE = await fetch(ENDPOINT);
    const TEXT = await FILE.text();

    document.getElementById("presentation-download").onclick = (e) => {
      downloadFile(toSafeFileName(current.title) + ".html", TEXT, "text/html");
    };
    document.getElementById("presentation-view").href = ENDPOINT;
    document.getElementById("modal-preview").src = current.cover;
    document.getElementById("modal-title").innerText = current.title;
    document.getElementById("modal-authors").innerText = current.authors;
    document.getElementById("modal-description").innerText =
      current.description;
  }
}

async function updatePresentions(search = "") {
  const response = await fetch("/presentations");
  if (response.ok) {
    const TABLE = document.getElementById("presentations-table");
    const STATS = document.getElementById("found-result");
    const json = await response.json();
    let resultCount = 0;

    let resultHTML = "";
    json.forEach((value) => {
      const row = `
      <tr class="presentation-row" onclick="showModal(${value.id})">
      <th scope="row">
      <span class="format-icon">
      HTML
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
      STATS.innerText = "Ничего не найдено";
    } else if (resultCount === json.length) {
      document.getElementById("table-wrapper").hidden = false;
      STATS.innerText = `Всего ${resultCount} презентаций`;
    } else {
      document.getElementById("table-wrapper").hidden = false;
      STATS.innerText = `Найдено ${resultCount} презентаций`;
    }

    TABLE.innerHTML = resultHTML;
  }
}

updatePresentions();

document.getElementById("searchbar").oninput = (e) => {
  console.log("s");
  const SEARCH = document.getElementById("searchbar").value;
  updatePresentions(SEARCH);
};

// $("#achievements-btn").click(function (e) {
//   e.preventDefault();

//   window.location.href = "/achievements";
// });
