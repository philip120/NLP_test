import gradio as gr
from theme_classifier import ThemeClassifier
from character_network import CharacterNetworkGenerator,NamedEntityRecognizer
from utils import load_subtitles_dataset

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

def get_character_network(subtitles_path,ner_path):
    ner = NamedEntityRecognizer()
    ner_df = ner.get_ners(subtitles_path,ner_path)
    
    character_network_generator = CharacterNetworkGenerator()
    relationship_df = character_network_generator.generate_character_network(ner_df)
    html = character_network_generator.draw_network_graph(relationship_df)
    
    return html
    
    

def main():
    with gr.Blocks() as iface:
        # First section for theme classification
        with gr.Row():
            with gr.Column():
                gr.HTML("<h1>Theme Classification (Zero-Shot Classifiers)</h1>")
                with gr.Row():
                    with gr.Column():
                        plot = gr.BarPlot()
                    with gr.Column():
                        theme_list = gr.Textbox(label="Themes")
                        subtitles_path = gr.Textbox(label="Subtitles or Script Path")
                        save_path = gr.Textbox(label="Save Path")
                        get_themes_button = gr.Button("Get Themes")
                        get_themes_button.click(
                            get_themes, 
                            inputs=[theme_list, subtitles_path, save_path], 
                            outputs=plot
                        )

        # Second section for character network
        with gr.Row():
            with gr.Column():
                gr.HTML("<h1>Character Network (Networks and Graphs)</h1>")
                with gr.Row():
                    with gr.Column():
                        network_html = gr.HTML()
                    with gr.Column():
                        subtitles_path_network = gr.Textbox(label="Subtitles or Script Path")
                        ner_path = gr.Textbox(label="NERs Save Path")
                        get_network_graph_button = gr.Button("Get Character Network")  
                        get_network_graph_button.click(get_character_network, inputs=[subtitles_path_network, ner_path], outputs=[network_html])

    iface.launch(share=True)
                    
if __name__ == '__main__':
    main()