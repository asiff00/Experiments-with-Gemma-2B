import os
import gradio as gr
from src.brain import generate_answers
from huggingface_hub import login
from dotenv import load_dotenv

load_dotenv()
token = os.environ.get("TOKEN")
login(token=token)

processing = False


def response(query, history):
    global processing
    processing = True
    output = generate_answers(query)
    history.append((query, output))
    processing = False
    return "", history


with open("src/style.css", "r") as file:
    css = file.read()

with open("src/content.html", "r") as file:
    html_content = file.read()
    parts = html_content.split("<!-- split here -->")
    title_html = parts[0]
    bts_html = parts[1] if len(parts) > 1 else ""


def loading():
    return "Loading ..."


with gr.Blocks(css=css) as app:
    with gr.Column(elem_id="column_container"):
        gr.HTML(title_html)
        chatbot = gr.Chatbot([], elem_id="chatbot")
        with gr.Column():
            send = gr.Label(value="Write your QUESTION bellow and hit ENTER")
        query = gr.Textbox(
            label="Type your questions here:",
            placeholder="What do you want to know?",
        )
        clear = gr.ClearButton([query, chatbot])
        gr.HTML(bts_html)
    query.submit(response, [query, chatbot], [query, chatbot], queue=True)

app.launch()
