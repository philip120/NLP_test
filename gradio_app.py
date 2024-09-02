import gradio as gr
from theme_classifier import ThemeClassifier

def get_themes(theme_list,subtitles_path,save_path):
    theme_list = theme_list.split(',')
    theme_classifier = ThemeClassifier(theme_list)
    output_themes = theme_classifier.get_themes(subtitles_path,save_path)
    
    #remove the dialogue from theme list
    theme_list = [theme for theme in theme_list if theme != 'dialogue']
    output_df = output_themes[theme_list]
    
    output_df = output_df[theme_list].sum().reset_index()
    output_df.columns = ['theme','score']
    
    output_chart = gr.BarPlot(
        output_df,
        x='theme',
        y='score',
        title='Series Themes',
        tooltip = ["theme","score"],
        vertical = False,
        width = 500,
        height = 250
    )
    
    return output_chart
    
    

def main():
    with gr.Blocks() as iface:
        with gr.Row():
            with gr.Column():
                gr.HTML("<h1>Theme classification (zero shot classifiers)</h1>")
                with gr.Row():
                    with gr.Column():
                        plot = gr.BarPlot()
                    with gr.Column():
                        theme_list = gr.Textbox(label="Themes")
                        subtitles_path = gr.Textbox(label="Subtititles or script path")
                        save_path=gr.Textbox(label="save path")
                        get_themes_button = gr.Button("get themes")
                        get_themes_button.click(get_themes,inputs=[theme_list,subtitles_path,save_path], outputs=[plot])
                    
    iface.launch(share=True) 
                    
if __name__ == '__main__':
    main()