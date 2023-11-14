from layout import layout
from app import app

app.layout = layout

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=3040)