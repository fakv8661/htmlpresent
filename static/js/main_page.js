// Скрипт страницы `main_page.html`

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
      ХЗ
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
