import re

from flask import Flask, jsonify, render_template, request
from huggingface_hub.errors import HfHubHTTPError
import os
from rag.chain import VectorTubeChain
from src.logger import logger

app = Flask(__name__)
rag_chain = None


def get_hf_status_code(exc: HfHubHTTPError) -> int:
    if exc.response is not None and exc.response.status_code:
        return exc.response.status_code

    match = re.search(r"\b([45]\d{2})\s+Client Error\b", str(exc))
    if match:
        return int(match.group(1))

    return 502


def extract_hf_error_message(exc: HfHubHTTPError) -> str:
    if exc.response is not None:
        try:
            payload = exc.response.json()
            error = payload.get("error")
            if isinstance(error, dict) and error.get("message"):
                return error["message"]
        except Exception:
            pass

    return str(exc)


def get_rag_chain():
    global rag_chain
    if rag_chain is None:
        rag_chain = VectorTubeChain()
    return rag_chain

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    link = request.form.get("video_link", "").strip()
    if not link:
        return render_template("index.html", error="Please enter a valid YouTube link.")

    return render_template("chat.html", video_url=link)


@app.route("/api/chat", methods=["POST"])
def api_chat():
    payload = request.get_json(silent=True) or {}
    video_url = (payload.get("video_url") or "").strip()
    question = (payload.get("question") or "").strip()

    if not video_url:
        return jsonify({"error": "Missing video_url."}), 400
    if not question:
        return jsonify({"error": "Missing question."}), 400

    try:
        chain = get_rag_chain()
        response = chain.ask(video_url=video_url, question=question)
        return jsonify(response)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    except RuntimeError as exc:
        return jsonify({"error": str(exc)}), 500
    except HfHubHTTPError as exc:
        logger.exception("Hugging Face API error while handling /api/chat")
        status_code = get_hf_status_code(exc)
        error_message = extract_hf_error_message(exc)

        if status_code == 401:
            return (
                jsonify(
                    {
                        "error": (
                            "Hugging Face auth failed (token missing/expired). "
                            "Set HUGGINGFACEHUB_API_TOKEN with a valid token and restart Flask. "
                            f"Details: {error_message}"
                        )
                    }
                ),
                401,
            )

        if status_code and 400 <= status_code < 600:
            return jsonify({"error": f"Hugging Face: {error_message}"}), status_code

        return jsonify({"error": f"Hugging Face API request failed: {error_message}"}), 502
    except Exception:
        logger.exception("Unexpected error while handling /api/chat")
        return jsonify({"error": "Could not generate response. Try again."}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
