const recognitionForm = document.getElementById("recognition-form");
const synthesisForm = document.getElementById("synthesis-form");
const recognitionOutput = document.getElementById("recognition-output");
const synthesisOutput = document.getElementById("synthesis-output");

recognitionForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const formData = new FormData(recognitionForm);
    const response = await fetch("/predict", {
        method: "POST",
        body: formData,
    });
    recognitionOutput.textContent = await response.text();
});

synthesisForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const text = synthesisForm.elements.text.value;
    const response = await fetch("/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text }),
    });
    synthesisOutput.textContent = await response.text();
});
