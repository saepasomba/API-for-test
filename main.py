from typing import Optional

import shutil
from fastapi import Body, FastAPI, UploadFile
from pydantic import BaseModel

app = FastAPI()

class Mahasiswa(BaseModel):
    nama: str
    npm: str
    alamat: str

db = {
}

@app.get("/mahasiswa/{npm}")
def get_mahasiswa(npm: str):
    return db[npm]

# This function is made inefficient on purpose
@app.get("/mahasiswa/2/{npm}")
def get_mahasiswa(npm: str):
    for npmDB in db:
        if npm == npmDB:
            mahasiswa = db[npm]
    return mahasiswa

@app.post("/mahasiswa")
def post_mahasiswa(mahasiswa: Mahasiswa):
    npm = mahasiswa.npm
    db[npm] = mahasiswa
    return mahasiswa

@app.put("/mahasiswa/{npm}")
def edit_mahasiswa(npm: str, nama: str = Body(...), alamat: str = Body(...)):
    db[npm].nama = nama
    db[npm].alamat = alamat
    return db[npm]

@app.delete("/mahasiswa/{npm}")
def delete_mahasiswa(npm: str):
    db.pop(npm)
    return {
        "npm" : npm,
        "status" : "Deleted"
    }

@app.post("/upload")
def upload_file(file: UploadFile):
    file_location = f"files/{file.filename}"
    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)
    return {
        "filename" : file.filename,
        "status" : "Success"
        }

