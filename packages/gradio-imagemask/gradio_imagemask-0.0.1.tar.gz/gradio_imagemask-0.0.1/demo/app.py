
import gradio as gr
from gradio_imagemask import ImageMask


example = ImageMask().example_value()

demo = gr.Interface(
    lambda x:x,
    ImageMask(),  # interactive version of your component
    ImageMask(),  # static version of your component
    # examples=[[example]],  # uncomment this line to view the "example version" of your component
)


if __name__ == "__main__":
    demo.launch()
