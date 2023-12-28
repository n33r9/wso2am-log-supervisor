from fastapi import FastAPI, BackgroundTasks, Query, Request, Form
from fastapi.templating import Jinja2Templates
from datetime import date
import watchdog.events
import watchdog.observers

app = FastAPI()
templates = Jinja2Templates(directory="templates")
total_pages=0
file_status = 0
search_keywords = []
relevant_lines = []

class Handler(watchdog.events.PatternMatchingEventHandler):
    def __init__(self):
        watchdog.events.PatternMatchingEventHandler.__init__(self, patterns=["*"], ignore_directories=True, case_sensitive=False)

    def on_created(self, event):
        global file_status
        file_status = 1

    def on_modified(self, event):
        global file_status
        file_status = 1

def start_observer():
    path = '/home/william/Desktop/wso2am-4.0.0/repository/logs/'
    event_handler = Handler()
    observer = watchdog.observers.Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "file_status": file_status, "total_pages": 0,
        "current_page": 0, "relevant_lines": []})

@app.post("/search/")
async def search_log(request: Request, search_term: str = Form(...)):
    global search_keywords
    global relevant_lines
    search_keywords = []
    search_keywords.append(search_term)
    
    today = date.today()
    filename = '/home/william/Desktop/wso2am-4.0.0/repository/logs/http_access_.' + today.strftime('%Y-%m-%d') + '.log'

    relevant_lines = []
    try:
        with open(filename, 'r') as f:
            for line in f:
                if any(keyword in line for keyword in search_keywords):
                    relevant_lines.append(line.strip())
    except FileNotFoundError:
        return {"error": "File not found."}

    # Tính toán số lượng trang (ví dụ: mỗi trang có 10 dòng)
    items_per_page = 250
    global total_pages
    total_pages = len(relevant_lines) // items_per_page + ((len(relevant_lines) % items_per_page) > 0)
    print(total_pages)
    
    # Lấy trang hiện tại 
    current_page = int(request.query_params.get("page", 1))  # Nếu không có query parameter 'page', mặc định là trang 1
    start_index = (current_page - 1) * items_per_page
    end_index = current_page * items_per_page
    
    # Trả về dữ liệu cho trang hiện tại
    current_page_lines = relevant_lines[start_index:end_index]
    
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "file_status": file_status, 
        "relevant_lines": current_page_lines,
        "total_pages": total_pages,
        "current_page": current_page
        })

# @app.get("/search/?page=${page}")
# async def search_log(request: Request):
#     page = int(request.query_params.get("page", 1))
#     items_per_page = 10
#     start_index = (page - 1) * items_per_page
#     end_index = page * items_per_page
#     current_page_lines = relevant_lines[start_index:end_index]

#     return {
#         "file_status": file_status,
#         "relevant_lines": current_page_lines,
#         "total_pages": total_pages,
#         "current_page": page
#     }
if __name__ == "__main__":
    start_observer()
    import uvicorn
    uvicorn.run(app, host="btl86.wso2amlog.com", port=8000)
