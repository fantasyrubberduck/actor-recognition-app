// Elements del DOM
const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const captureBtn = document.getElementById('capture');
const messageBox = document.getElementById('message');
const spinner = document.getElementById('spinner');

// Funció per mostrar missatges
function showMessage(text, type = "info") {
  messageBox.textContent = text;
  messageBox.className = `message ${type}`; // CSS: .message.info, .message.error, .message.success
  messageBox.style.display = "block";
}

// Activar la càmera
navigator.mediaDevices.getUserMedia({ video: true })
  .then(stream => {
    video.srcObject = stream;
  })
  .catch(err => {
    showMessage("Error accedint a la càmera: " + err.message, "error");
  });

// Funció per enviar la imatge al backend
async function postIdentify(formData, timeoutMs = 15000) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);

  try {
    const response = await fetch("http://localhost:8000/identify", {
      method: "POST",
      body: formData,
      signal: controller.signal
    });
    clearTimeout(timer);

    let payload = null;
    try {
      payload = await response.json();
    } catch {
      payload = null;
    }

    if (!response.ok) {
      switch (response.status) {
        case 400:
          showMessage(payload?.detail || "Sol·licitud invàlida (400).", "error");
          break;
        case 404:
          showMessage(payload?.detail || "No s’ha trobat cap cara o actor (404).", "error");
          break;
        case 422:
          showMessage("La petició no compleix el format esperat (422).", "error");
          break;
        case 500:
          showMessage(payload?.detail || "Error intern del servidor (500).", "error");
          break;
        default:
          showMessage(`Error del servidor: ${response.status}`, "error");
      }
      return null;
    }

    return payload;
  } catch (err) {
    clearTimeout(timer);
    if (err.name === "AbortError") {
      showMessage("La petició ha excedit el temps límit.", "error");
    } else {
      showMessage("No s’ha pogut connectar amb el servidor.", "error");
      console.error("Error en la petició:", err);
    }
    return null;
  }
}

// Captura i enviament
captureBtn.addEventListener('click', async () => {
  captureBtn.disabled = true;
  spinner.style.display = "inline-block"; // mostra spinner

  try {
    canvas.width = video.videoWidth || 640;
    canvas.height = video.videoHeight || 480;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    canvas.toBlob(async (blob) => {
      if (!blob) {
        showMessage("Error capturant la imatge.", "error");
        captureBtn.disabled = false;
        spinner.style.display = "none";
        return;
      }

      const formData = new FormData();
      formData.append("file", blob, "capture.jpg");

      const result = await postIdentify(formData);

      if (result) {
        if (result.actor && result.actor.name) {
          const conf = typeof result.confidence === "number"
            ? (result.confidence * 100).toFixed(0) + "%"
            : "—";
          showMessage(`Actor identificat: ${result.actor.name} (confiança: ${conf})`, "success");
        } else {
          showMessage("No s’ha pogut identificar cap actor.", "error");
        }
      }

      captureBtn.disabled = false;
      spinner.style.display = "none";
    }, "image/jpeg");
  } catch (err) {
    captureBtn.disabled = false;
    spinner.style.display = "none";
    showMessage("Error inesperat capturant o enviant la imatge.", "error");
    console.error(err);
  }
});
