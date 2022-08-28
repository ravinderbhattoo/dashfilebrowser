import os

import dash
from dash import ctx, dcc, html
from dash.dependencies import Input, Output, State
from genericpath import isdir, isfile

external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    # f'https://fonts.googleapis.com/css2?family={font}:wght@400;500&display=swap',
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

root = "."
current = "."
PWD = os.path.abspath(root)
IFFILE = False
FILEPATH = "none"
FILEEXT = [".tex", ".txt", ".py", ".jl", ".md"]
CURRENTDIR = PWD


def iffileis(name): return any(
    map(lambda x: name[-len(x):] == x if (x in name) else False, FILEEXT))


def fixpath(path):
    global PWD
    return os.path.abspath(path).replace(PWD, "ROOT")


def listfiles(folder):
    global PWD, CURRENTDIR
    folder = folder.replace("ROOT", ".")
    CURRENTDIR = folder
    l = [folder + "/" + i for i in os.listdir(folder)]
    l = [i for i in l if "/." not in i]
    l = [i for i in l if (iffileis(i) or os.path.isdir(i))]
    l_dir = [i for i in l if os.path.isdir(i)]
    l_dir.sort()
    l_fil = [i for i in l if not(os.path.isdir(i))]
    l_fil.sort()
    l = l_dir+l_fil
    l = [fixpath(i) for i in l]
    if os.path.abspath(folder) == PWD:
        l = [fixpath(folder+"/.")] + l
    else:
        l1 = list(set([fixpath(i)
                       for i in [".", folder+"/.."]]))
        l1.remove('ROOT')
        l = ['ROOT'] + l1 + l
    return l


files = listfiles(current)

controls = [
    dcc.Dropdown(
        id="dropdown",
        options=[{"label": x, "value": x} for x in files],
        value='ROOT',
    )
]

app.layout = html.Div(html.Div(
    [html.Div([
        html.H1("File Browser", style={"width": "300px"}),
        html.Div([
            html.Button('Reload', id='loadfile', n_clicks=0),
            html.Button(
                html.Div('Save', style={"color": "red"}), id='submit', n_clicks=0),
            html.Div(id='status', children=''),
        ], style={"flex-grow": "1", "text-align": "right"}),
    ], style={"display": "flex", }),
        html.Div(id='status2', children=''),
        html.Div([
            html.Div(controls, style={
                "background-color": "#EEEEEE", "width": "300px"}),
            html.Div(dcc.Textarea(
                id='textarea',
                value='Empty',
                style={'width': '100%', 'height': 700,
                       'font-family': "roboto condensed", "font-size": "18px"},
            ), style={"flex-grow": "1"}),
        ],
        style={"background-color": "#EEEEEE", "display": "flex"}),
    ],

), style={"max-width": "100%", "margin": "auto"})


def get_parent(x):
    return os.path.basename(os.path.dirname(x))


def labelfile(x):
    global CURRENTDIR
    if os.path.isdir(x.replace("ROOT", ".")):
        x = os.path.basename(x)
        if x == get_parent(CURRENTDIR):
            return html.Div("..", style={"color": "red"})
        elif x == "ROOT":
            return html.Div(x, style={"color": "red"})
        return html.Div(x, style={"color": "green"})
    else:
        x = os.path.basename(x)
        return x


@ app.callback(Output("dropdown", "options"), Input("dropdown", "value"))
def list_all_files(folder_name):
    folder_name = folder_name.replace("ROOT", ".")
    if os.path.isfile(folder_name):
        folder_name = os.path.dirname(folder_name)
    files = listfiles(folder_name)
    return [{"label": labelfile(x), "value": x} for x in files]


@ app.callback(Output("textarea", "value"), [Input("dropdown", "value"), Input("loadfile", "n_clicks")])
def list_all_files(file_name, nclicks):
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
    print(nclicks)
    return text


@ app.callback(Output("status2", "children"), Input("dropdown", "value"))
def list_all_files2(file_name):
    global IFFILE, FILEPATH
    file_name = file_name.replace("ROOT", ".")
    file_name = fixpath(file_name)
    if os.path.isfile(file_name):
        IFFILE = True
        FILEPATH = file_name
    else:
        IFFILE = False
        FILEPATH = file_name
    return html.Div("Location: "+FILEPATH, style={"color": "black", "font-weight": "700"})


@ app.callback(Output("status", "children"), [Input("submit", "n_clicks"), Input("loadfile", "n_clicks")], [State('textarea', 'value')])
def save(nclick, nclick2, text):
    button_id = ctx.triggered_id if not None else 'No clicks yet'
    global IFFILE, FILEPATH
    if IFFILE and text != "Empty":
        with open(FILEPATH, "w") as f:
            for line in text.split("\n"):
                f.write(line+"\n")
    if button_id == "submit":
        return html.Div("SAVED FILEPATH: "+FILEPATH, style={"color": "red"})
    else:
        return html.Div("RELOAD FILEPATH: "+FILEPATH, style={"color": "green"})


def run():
    app.run_server(debug=True)


if __name__ == "__main__":
    app.run_server(debug=True)
