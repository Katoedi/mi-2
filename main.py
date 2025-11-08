from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def love_page():
    return """
    <html>
        <head>
            <title>Te iubesc ❤️</title>
            <style>
                body {
                    margin: 0;
                    height: 100vh;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    background: linear-gradient(270deg, #ff99cc, #ff6699, #ff3366, #ff99cc);
                    background-size: 800% 800%;
                    animation: gradient 10s ease infinite;
                    font-family: 'Comic Sans MS', cursive, sans-serif;
                }

                h1 {
                    font-size: 4rem;
                    color: white;
                    text-shadow: 0 0 20px #ff0066;
                    animation: heartbeat 1.5s infinite;
                }

                @keyframes heartbeat {
                    0% { transform: scale(1); }
                    25% { transform: scale(1.2); }
                    50% { transform: scale(1); }
                    75% { transform: scale(1.2); }
                    100% { transform: scale(1); }
                }

                @keyframes gradient {
                    0% { background-position: 0% 50%; }
                    50% { background-position: 100% 50%; }
                    100% { background-position: 0% 50%; }
                }
            </style>
        </head>
        <body>
            <h1>te iubesc, Cari ❤️❤️❤️</h1>
        </body>
    </html>
    """
