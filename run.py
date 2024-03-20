from fastapi import FastAPI
import gradio as gr

from app import demo

fast_app = FastAPI()

@fast_app.get('/')
async def root():
    return 'Gradio app is running at /gradio', 200

app = gr.mount_gradio_app(fast_app, demo, path='/gradio')
