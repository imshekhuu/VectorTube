function toggleSidebar() {
  const sb = document.getElementById("sidebar");
  if (sb) sb.classList.toggle("collapsed");
}

const input = document.getElementById("messageInput");
const sendButton = document.querySelector(".input button");

if (input) {
  input.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  });

  input.addEventListener("input", () => {
    input.style.height = "auto";
    input.style.height = input.scrollHeight + "px";
  });
}

async function sendMessage() {
  if (!input) return;

  const question = input.value.trim();
  if (!question) return;

  const videoUrl = window.vectorTubeVideoUrl || "";
  if (!videoUrl) {
    addMessage("Missing video URL. Reload and start chat again.", "bot");
    return;
  }

  addMessage(question, "user");
  input.value = "";
  input.style.height = "auto";

  if (sendButton) sendButton.disabled = true;

  const typing = addMessage("", "bot typing");
  typing.innerHTML = "<span></span><span></span><span></span>";

  try {
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        video_url: videoUrl,
        question: question,
      }),
    });

    const data = await response.json();
    typing.classList.remove("typing");

    if (!response.ok) {
      typing.innerText = data.error || "Request failed.";
      return;
    }

    typing.innerText = data.answer || "No answer returned.";
  } catch (err) {
    typing.classList.remove("typing");
    typing.innerText = "Server error. Make sure Flask is running.";
  } finally {
    if (sendButton) sendButton.disabled = false;
  }
}

function addMessage(text, role) {
  const wrapper = document.createElement("div");
  wrapper.className = `msg ${role}`;

  const avatar = document.createElement("div");
  avatar.className = "avatar";
  avatar.innerText = role === "user" ? "U" : "AI";

  const content = document.createElement("div");
  content.className = "msg-content";
  content.innerText = text;

  const time = document.createElement("div");
  time.className = "copy";
  time.innerText = new Date().toLocaleTimeString();
  time.onclick = () => navigator.clipboard.writeText(text);

  content.appendChild(time);

  wrapper.appendChild(avatar);
  wrapper.appendChild(content);

  const box = document.getElementById("chatBox");
  if (box) {
    box.appendChild(wrapper);
    box.scrollTop = box.scrollHeight;
  }

  return content;
}
