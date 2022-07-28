from genericpath import isdir, isfile
import os

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

root = "."
current = "."
PWD = os.path.abspath(root)
IFFILE = False
FILEPATH = "none"

def fixpath(path):
    global PWD
    return os.path.abspath(path).replace(PWD, "ROOT")

def listfiles(folder):
    global PWD
    folder = folder.replace("ROOT", ".")
    l = [folder +"/"+ i for i in os.listdir(folder)]
    l = [i for i in l if "/." not in i]
    l = [i for i in l if ((".tex" in i) or os.path.isdir(i))]
    l_dir = [i for i in l if os.path.isdir(i)]
    l_dir.sort()
    l_fil = [i for i in l if not(os.path.isdir(i))]
    l_fil.sort()
    l = l_dir+l_fil
    l = [fixpath(i) for i in l]
    if os.path.abspath(folder)==PWD:
        l = [fixpath(folder+"/.")] + l
    else:
        l = list(set([fixpath(i) for i in [folder+"/.", ".", folder+"/.."]])) + l
    return l


files = listfiles(current)

controls = [
    dcc.Dropdown(
        id="dropdown",
        options=[{"label": x, "value": x} for x in files],
        value=files[0],
    )
]

app.layout = html.Div( html.Div(
    [html.H1("File Browser"),
    html.Div(controls),
    html.Div(id='status2',
             children=''),
    dcc.Textarea(
        id='textarea',
        value='Empty',
        style={'width': '100%', 'height': 300},
    ),
    html.Button('Save', id='submit', n_clicks=0),
    html.Div(id='status',
             children=''),
    ],
    style={"max-width": "900px", "margin":"auto"}
))


@app.callback(Output("dropdown", "options"), Input("dropdown", "value"))
def list_all_files(folder_name):
    folder_name = folder_name.replace("ROOT", ".")
    if os.path.isfile(folder_name):
        folder_name = os.path.dirname(folder_name)
    files = listfiles(folder_name)
    return [{"label": x, "value": x} for x in files]

@app.callback(Output("textarea", "value"), Input("dropdown", "value"))
def list_all_files(file_name):
    global IFFILE, FILEPATH
    file_name = file_name.replace("ROOT", ".")
    if os.path.isfile(file_name):
        text = "".join(open(file_name, 'r').readlines())
        IFFILE = True
        FILEPATH = file_name
    else:
        text = "Empty"
        IFFILE = False
        FILEPATH = "none"
    return text

@app.callback(Output("status2", "children"), Input("dropdown", "value"))
def list_all_files(file_name):
    global IFFILE, FILEPATH
    file_name = file_name.replace("ROOT", ".")
    if os.path.isfile(file_name):
        IFFILE = True
        FILEPATH = file_name
    else:
        IFFILE = False
        FILEPATH = "none"
    return "FILEPATH: "+FILEPATH

@app.callback(Output("status", "children"), [Input("submit", "n_clicks")], [State('textarea', 'value')])
def save(nclick, text):
    global IFFILE, FILEPATH
    if IFFILE and text!="Empty":
        with open(FILEPATH, "w") as f:
            for line in text.split("\n"):
                f.write(line+"\n")
    return "SAVED FILEPATH: "+FILEPATH

def run():
    app.run_server(debug=True)

if __name__ == "__main__":
    app.run_server(debug=True)
