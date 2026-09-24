// Скрипт страницы `main_page.html`

async function updatePresentions(search = "") {
  const response = await fetch("/presentations");
  if (response.ok) {
    const TABLE = document.getElementById("presentations-table");
    const STATS = document.getElementById("found-result");
    const json = await response.json();
    STATS.innerText = json.length;
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

      TABLE.innerHTML += row;
    });
  }
}

updatePresentions();

// $("#achievements-btn").click(function (e) {
//   e.preventDefault();

//   window.location.href = "/achievements";
// });
