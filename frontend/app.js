document.getElementById("dreamForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const dream = document.getElementById("dream").value;
  const constraints = document.getElementById("constraints").value;

  try {
    const response = await fetch("http://127.0.0.1:8000/generate", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ dream, constraints }),
    });

    if (!response.ok) {
      throw new Error("Failed to fetch response from backend");
    }

    const data = await response.json();
    document.getElementById("output").textContent = data.result;
  } catch (error) {
    document.getElementById("output").textContent = "❌ Error: " + error.message;
  }
});
