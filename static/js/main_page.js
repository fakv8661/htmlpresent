// Скрипт страницы `main_page.html`

async function updatePresentions(search = "") {
  const response = await fetch("/presentations");
  if (response.ok) {
    const TABLE = document.getElementById("presentations-table");
    const STATS = document.getElementById("found-result");
    const json = await response.json();

    STATS.innerText = json.length;
    TABLE.innerHTML = "";
    json.forEach((value, index) => {
      const row = `
      <tr>
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
        TABLE.innerHTML += row;
      }
    });
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
