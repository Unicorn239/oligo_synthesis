import os
import dash
from dash.dependencies import Input, Output 
import dash_core_components as dcc
import dash_html_components as html
import jupyter_plotly_dash as JupyterDash
import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
import plotly.graph_objs as go

df = pd.read_csv('gene_clone.csv')
lst_variable = df.columns.tolist()
lst_variable.remove('correct_num')
str_formula = 'correct_num ~ ' + ' + '.join(lst_variable)
    
model = smf.poisson(data = df, formula = str_formula)
results = model.fit()
    
    
# dash app
app = dash.Dash(__name__)
server = app.server
port = int(os.environ.get("PORT", 5000))

app.layout = html.Div(
                  children = [    # This container is to host control components
                               html.H2('Poisson regression analysis'),
                               html.H3(''),
                               html.H3('Select length of oligos in base pairs'),
                               dcc.Slider(
                                           id = 'len_gene',
                                           min = 325,
                                           max = 2250,
                                           value = 500,
                                           tooltip = {'always_visible' : True}
                                              ),
                               html.H3('Select clones being made'),
                               dcc.Dropdown(
                                            id = 'syn_clone',
                                            options = [
                                                       {'label' : '%s clones' %i, 'value' : i} for i in 
                                                         range(2, 8)
                                                          ],
                                            value = 3,
                                            style = { 
                                                      'width' : '40%',
                                                      'height' : 25
                                                        }
                                                ),                                           
                                html.Div(
                                     children = [    # This container is to host the graph
                                                  html.H3('Prediction of number of correct clones'),
                                                  html.Button(
                                                               'Predict', 
                                                               id = 'calc',
                                                               style = {
                                                                         'width' : '10%',
                                                                         'height' : 25
                                                                           }
                                                                  ),
                                                  dcc.Graph( 
                                                             id = 'graph',
                                                             style = {
                                                                       'width' : '75%', 
                                                                       'height' : 500
                                                                         }
                                                             ) 
                                                       ]
                                            )
                                       ]
                           )


# update graph
@app.callback(
               Output('graph', 'figure'),
               Input('len_gene', 'value'),
               Input('syn_clone', 'value'),
               Input('calc', 'n_clicks')
                 )
def update_graph(length_value, clone_value, n_clicks):
    interval = np.linspace(df.error_rate.min(), df.error_rate.max())
    log_count = results.params.values[0] + results.params.values[1] * length_value + results.params.values[2] \
            * clone_value + results.params.values[3] * interval
    success_clones = np.exp(log_count)
    if n_clicks > 0:
        trace = go.Scatter(
                            x = interval,
                            y = success_clones, 
                            mode = 'lines', 
                            line = {'width' : 1}
                              )
        fig = go.Figure(trace)
        return fig
   

    
if __name__ == '__main__':
    oligo.run_server(debug = False, 
                   host="0.0.0.0",
                   port=port)



