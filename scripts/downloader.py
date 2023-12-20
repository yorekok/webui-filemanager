import os
from modules import script_callbacks, paths
import gradio as gr
import requests
import subprocess
import os
import re
import tqdm
from PIL import Image


def list_files(directory):
    try:
        files = os.listdir(directory)
        return "\n".join(files)
    except Exception as e:
        return str(e)

# Dosya kopyalama
def copy_file(source, destination):
    try:
        shutil.copy(source, destination)
        return f"Kopyalandı: {source} -> {destination}"
    except Exception as e:
        return str(e)

# Dosya silme
def delete_file(file_path):
    try:
        os.remove(file_path)
        return f"Silindi: {file_path}"
    except Exception as e:
        return str(e)

# Dosya taşıma
def move_file(source, destination):
    try:
        shutil.move(source, destination)
        return f"Taşındı: {source} -> {destination}"
    except Exception as e:
        return str(e)

# Gradio arayüzü
def create_interface():
    with gr.Blocks() as app:
        with gr.Tabs():
            with gr.Tab("File Manager"):
                with gr.Column():
                    with gr.Row():
                        list_button = gr.Button("List Files")
                        directory_input = gr.Textbox(label="Directory", value=".")
                        list_output = gr.Textbox(label="Files", multiline=True, interactive=False)
                        list_button.click(list_files, inputs=[directory_input], outputs=[list_output])

                    with gr.Row():
                        copy_source = gr.Textbox(label="Copy - Source File")
                        copy_destination = gr.Textbox(label="Copy - Destination File")
                        copy_button = gr.Button("Copy")
                        copy_output = gr.Textbox(label="Result", interactive=False)
                        copy_button.click(copy_file, inputs=[copy_source, copy_destination], outputs=[copy_output])

                    with gr.Row():
                        delete_file_input = gr.Textbox(label="Delete - File Path")
                        delete_button = gr.Button("Delete")
                        delete_output = gr.Textbox(label="Result", interactive=False)
                        delete_button.click(delete_file, inputs=[delete_file_input], outputs=[delete_output])

                    with gr.Row():
                        move_source = gr.Textbox(label="Move - Source File")
                        move_destination = gr.Textbox(label="Move - Destination File")
                        move_button = gr.Button("Move")
                        move_output = gr.Textbox(label="Result", interactive=False)
                        move_button.click(move_file, inputs=[move_source, move_destination], outputs=[move_output])
            # Burada başka sekmeler eklenebilir
    return app

app = create_interface()

script_callbacks.launch(app)
