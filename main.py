from controller.ChatController import app

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app=app,
                host="0.0.0.0",
                port=8081,
                workers=1)