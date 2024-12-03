import gradio as gr

# Define the function that takes a name and returns a greeting.
def greet(name):
    return "Hello " + name + "!"

# Create a Gradio interface with a title and an image.
# demo = gr.Interface(
#     fn=greet, 
#     inputs="textbox", 
#     outputs="textbox",
#     title="Welcome to My Gradio App",  # Add a title to the app
#     description="Enter your name to receive a personalized greeting.",  # Add a description
#     theme=gr.themes.Default(),  # Use the default theme
#     allow_flagging="never",  # Disable flagging
#     css="""
#     .gradio-container {
#         display: flex;
#         align-items: center;
#         justify-content: center;
#         flex-direction: column;
#     }
#     .gradio-app-header {
#         display: flex;
#         align-items: center;
#         justify-content: center;
#     }
#     .gradio-app-header img {
#         margin-left: 20px;  /* Add some space between the title and the image */
#     }
#     """
# )

demo = gr.Blocks(    css="""
    .gradio-container {
        display: flex;
        align-items: center;
        justify-content: center;
        flex-direction: column;
    }
    .gradio-app-header {
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .gradio-app-header img {
        margin-left: 20px;  /* Add some space between the title and the image */
    }
    """)

# # Add an image next to the title
with demo:
    gr.Markdown("<div class='gradio-app-header'><h1>Welcome to My Gradio App</h1><img src='https://static.wixstatic.com/media/57e244_1d2901d649c34d6f9ce37a75285a42f1~mv2.png' alt='App Logo' style='width: 100px; height: auto;'></div>")

# Launch the interface.
if __name__ == "__main__":

    demo.launch(show_error=True)