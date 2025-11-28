// Activar la càmera
navigator.mediaDevices.getUserMedia({ video: true })
  .then(stream => {
    document.getElementById('video').srcObject = stream;
  })
  .catch(err => {
    alert("Error accedint a la càmera: " + err.message);
  });

document.getElementById('capture').addEventListener('click', async () => {
  const video = document.getElementById('video');
  const canvas = document.getElementById('canvas');
  const ctx = canvas.getContext('2d');

  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  ctx.drawImage(video, 0, 0);

  const imageData = canvas.toDataURL('image/jpeg');

  try {
    const response = await fetch('http://localhost:8000/identify', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ image: imageData })
    });

    if (!response.ok) {
      throw new Error(`Error del servidor: ${response.status}`);
    }

    const result = await response.json();

    if (result.actor_name === "Desconegut") {
      alert("No s'ha pogut identificar cap actor.");
    } else {
      alert(`Actor identificat: ${result.actor_name}`);
    }
  } catch (error) {
    console.error("Error en la petició:", error);
    alert("No s'ha pogut connectar amb el servidor. Revisa que el backend estigui en marxa.");
  }
});
