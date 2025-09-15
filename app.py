from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import qrcode, os, json
from blockchain import CertificateBlockchain

# Initialize app
app = FastAPI()
blockchain = CertificateBlockchain()

# Mount static files (QR codes, CSS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Home Page
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Add Certificate Page
@app.get("/add", response_class=HTMLResponse)
async def add_page(request: Request):
    return templates.TemplateResponse("add_certificate.html", {"request": request})

# Add Certificate Action
@app.post("/add", response_class=HTMLResponse)
async def add_certificate(
    request: Request,
    cert_id: str = Form(...),
    name: str = Form(...),
    course: str = Form(...),
    date: str = Form(...)
):
    certificate_data = {"id": cert_id, "name": name, "course": course, "date": date}
    cert_hash = blockchain.add_certificate(certificate_data)

    # Generate QR
    qr_data = {"id": cert_id, "hash": cert_hash}
    img = qrcode.make(json.dumps(qr_data))
    filename = f"static/{cert_id}.png"
    img.save(filename)

    return templates.TemplateResponse("add_certificate.html", {
        "request": request,
        "message": "✅ Certificate Added Successfully!",
        "qr_path": f"/{filename}"
    })

# Verify Certificate Page
@app.get("/verify", response_class=HTMLResponse)
async def verify_page(request: Request):
    return templates.TemplateResponse("verify_certificate.html", {"request": request})

# Verify Certificate Action
@app.post("/verify", response_class=HTMLResponse)
async def verify_certificate(
    request: Request,
    cert_id: str = Form(...),
    name: str = Form(...),
    course: str = Form(...),
    date: str = Form(...)
):
    certificate_data = {"id": cert_id, "name": name, "course": course, "date": date}
    valid = blockchain.verify_certificate(certificate_data)

    return templates.TemplateResponse("verify_certificate.html", {
        "request": request,
        "status": "✅ Valid Certificate" if valid else "❌ Fake / Tampered Certificate"
    })
