const uploadForm = document.getElementById("uploadForm");

uploadForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  console.log("submit fired");

  const input = document.getElementById("fileInput");
  const file = input.files[0];

  const token = localStorage.getItem("accessToken");

  if (!token) {
    alert("Unathenticated!");
    return;
  }

  if (!file) {
    alert("Будь ласка, виберіть файл!");
    return;
  }

  const formData = new FormData();

  formData.append("image", file);

  try {
    const response = await fetch("http://127.0.0.1:8000/images/remove", {
      method: "POST",
      body: formData,
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      throw new Error(`Помилка сервера: ${response.status}`);
    }

    const data = await response.json();

    const baseUrl = "http://127.0.0.1:8000/";

    document.getElementById("originalImg").src = baseUrl + data.original_url;
    document.getElementById("resultImg").src = baseUrl + data.processed_url;

    document.getElementById("originalBlock").classList.remove("hidden");
    document.getElementById("resultBlock").classList.remove("hidden");
  } catch (error) {
    console.error(error);
  }
});

const uploadSection = document.getElementById("uploadSection");
const gallerySection = document.getElementById("gallerySection");
const btnNew = document.getElementById("btnNew");
const btnHistory = document.getElementById("btnHistory");
const galleryGrid = document.getElementById("galleryGrid");

btnNew.addEventListener("click", () => {
  uploadSection.classList.remove("hidden");
  gallerySection.classList.add("hidden");

  btnNew.classList.add("active");
  btnHistory.classList.remove("active");
});

btnHistory.addEventListener("click", async () => {
  uploadSection.classList.add("hidden");
  gallerySection.classList.remove("hidden");

  btnNew.classList.remove("active");
  btnHistory.classList.add("active");

  await loadHistoryImages();
});

async function loadHistoryImages() {
  const token = localStorage.getItem("accessToken");
  if (!token) return alert("Спочатку увійдіть!");

  galleryGrid.innerHTML = "";

  try {
    const response = await fetch("http://127.0.0.1:8000/images/get_all", {
      headers: { Authorization: `Bearer ${token}` },
    });

    if (!response.ok) throw new Error("Не вдалося завантажити історію");

    const images = await response.json();

    images.forEach((image) => {
      createGalleryCard(image);
    });
  } catch (error) {
    console.error(error);
    galleryGrid.innerHTML = "<p>Помилка завантаження історії</p>";
  }
}

function createGalleryCard(imageData) {
  const baseUrl = "http://127.0.0.1:8000/";

  const card = document.createElement("div");
  card.className = "history-card";

  card.innerHTML = `
        <div style="font-size: 12px; color: #888; align-self: flex-start;">
            ${new Date(imageData.created_at).toLocaleDateString()}
        </div>
        <img src="${baseUrl + imageData.processed_url}" alt="Processed">
        <a href="${baseUrl + imageData.processed_url}" 
           download="removed_bg_${imageData.id}.png" 
           target="_blank"
           class="download-link">
           Скачати PNG
        </a>
    `;

  galleryGrid.appendChild(card);
}
