import os
import shutil
import gradio as gr
import os
from modules import script_callbacks, paths
import gradio as gr
import requests
import subprocess
import os
import re
import tqdm
from PIL import Image

def format_file_size(size):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.2f}{unit}"
        size /= 1024
    return f"{size:.2f}TB"

def get_file_details(path):
    try:
        stat = os.stat(path)
        return {
            "Boyut": format_file_size(stat.st_size),
            "Son Değiştirilme": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(stat.st_mtime))
        }
    except Exception as e:
        return {"Hata": str(e)}

# Dosya işlemleri
def list_files(directory):
    try:
        files = os.listdir(directory)
        return "\n".join(files)
    except Exception as e:
        return str(e)

def copy_file(source, destination):
    try:
        shutil.copy(source, destination)
        return f"Kopyalandı: {source} -> {destination}"
    except Exception as e:
        return str(e)

def delete_file(file_path):
    try:
        os.remove(file_path)
        return f"Silindi: {file_path}"
    except Exception as e:
        return str(e)

def move_file(source, destination):
    try:
        shutil.move(source, destination)
        return f"Taşındı: {source} -> {destination}"
    except Exception as e:
        return str(e)

def on_ui_tabs():
    with gr.Blocks(analytics_enabled=False) as downloader:
        create_parent_dirs = gr.Checkbox(True, label="Create parent model directories if they do not exist (this may result in unintended consequences if you mistype something!)", interactive=True)
        with gr.Tab("File Manager"):
            with gr.Column():
		with gr.Row():
			list_button = gr.Button("List Files")
			directory_input = gr.Textbox(label="Directory", value=".")
			list_output = gr.Textbox(label="Files", multiline=True, interactive=False)
			list_button.click(list_files, inputs=[directory_input], outputs=[list_output])
		
		# Dosya Kopyalama
		with gr.Row():
			copy_source = gr.Textbox(label="Copy - Source File")
			copy_destination = gr.Textbox(label="Copy - Destination File")
			copy_button = gr.Button("Copy")
			copy_output = gr.Textbox(label="Result", interactive=False)
			copy_button.click(copy_file, inputs=[copy_source, copy_destination], outputs=[copy_output])
		
		# Dosya Silme
		with gr.Row():
			delete_file_input = gr.Textbox(label="Delete - File Path")
			delete_button = gr.Button("Delete")
			delete_output = gr.Textbox(label="Result", interactive=False)
			delete_button.click(delete_file, inputs=[delete_file_input], outputs=[delete_output])
		
		# Dosya Taşıma
		with gr.Row():
			move_source = gr.Textbox(label="Move - Source File")
			move_destination = gr.Textbox(label="Move - Destination File")
			move_button = gr.Button("Move")
			move_output = gr.Textbox(label="Result", interactive=False)
			move_button.click(move_file, inputs=[move_source, move_destination], outputs=[move_output])
		
		# Dosya Detayları
		with gr.Row():
			file_path_input = gr.Textbox(label="Dosya/Klasör Yolu")
			file_details_button = gr.Button("Dosya Detayları")
			file_details_output = gr.Textbox(label="Detaylar", multiline=True, interactive=False)
			file_details_button.click(lambda path: "\n".join([f"{k}: {v}" for k, v in get_file_details(path).items()]), inputs=[file_path_input], outputs=[file_details_output])
	
	
    return (downloader, "Filemanager", "downloader"),


script_callbacks.on_ui_tabs(on_ui_tabs)
