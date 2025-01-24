import os
from typing import Optional
from contextlib import asynccontextmanager
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import PyPDF2
from docx import Document
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification, AutoConfig

tokenizer: Optional[AutoTokenizer] = None
model: Optional[AutoModelForSequenceClassification] = None

SCORE_MAPPING = {
    0: {
        "score": 1,
        "description": "Esai menunjukkan kemampuan pengembangan sudut pandang yang sangat lemah, tidak memiliki bukti pendukung, struktur tidak koheren, dan kesalahan tata bahasa yang signifikan merusak makna."
    },
    1: {
        "score": 2,
        "description": "Esai menunjukkan penguasaan rendah dengan sudut pandang yang kurang, bukti pendukung tidak memadai, dan tata bahasa yang sangat terbatas."
    },
    2: {
        "score": 3,
        "description": "Esai menunjukkan penguasaan yang masih berkembang dengan sudut pandang yang belum baik, bukti pendukung tidak konsisten, dan beragam kesalahan tata bahasa."
    },
    3: {
        "score": 4,
        "description": "Esai menunjukkan penguasaan memadai dengan sudut pandang yang dikembangkan baik, bukti pendukung cukup kuat, struktur koheren, dan tata bahasa yang konsisten meski ada beberapa kesalahan."
    },
    4: {
        "score": 5,
        "description": "Esai menunjukkan penguasaan baik dengan sudut pandang efektif, bukti pendukung yang tepat, struktur koheren, dan tata bahasa terampil dengan kesalahan yang minim."
    },
    5: {
        "score": 6,
        "description": "Esai menunjukkan penguasaan sangat baik dengan sudut pandang mendalam, bukti sangat tepat dan relevan, struktur sangat koheren, dan penggunaan tata bahasa yang sangat baik."
    }
}

def load_model():
    global tokenizer, model
    model_directory = "./final-model"
    # model_directory = "./bert-sbert"


    if not os.path.isdir(model_directory):
        raise RuntimeError(f"Direktori model tidak ditemukan: {model_directory}")

    config_path = os.path.join(model_directory, "config.json")
    if not os.path.isfile(config_path):
        raise RuntimeError(f"File config.json tidak ditemukan di {model_directory}")

    try:
        config = AutoConfig.from_pretrained(model_directory)
        tokenizer = AutoTokenizer.from_pretrained(model_directory)
        model = AutoModelForSequenceClassification.from_pretrained(
            model_directory,
            config=config,
            use_safetensors=True,
            torch_dtype=torch.float32,
            low_cpu_mem_usage=True
        )
        model.eval()
    except Exception as e:
        raise RuntimeError(f"Gagal memuat model atau tokenizer: {e}")

def predict_score(text: str) -> dict:
    global tokenizer, model
    
    if not tokenizer or not model:
        raise RuntimeError("Model atau tokenizer belum dimuat.")

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=512
    )

    with torch.no_grad():
        outputs = model(**inputs)

    logits = outputs.logits
    predicted_class = torch.argmax(logits, dim=1).item()

    return SCORE_MAPPING.get(predicted_class, {
        "score": -1,
        "description": "Deskripsi tidak tersedia."
    })

def extract_text(file: UploadFile) -> str:
    try:
        if file.content_type == "application/pdf":
            pdf_reader = PyPDF2.PdfReader(file.file)
            extracted_text = []
            for page in pdf_reader.pages:
                page_text = page.extract_text().strip()
                if page_text:
                    page_text = ' '.join(page_text.split())
                    extracted_text.append(page_text)
            return "\n\n".join(extracted_text)
        
        elif file.content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            doc = Document(file.file)
            return "\n".join(para.text for para in doc.paragraphs)
        
        elif file.content_type == "text/plain":
            return file.file.read().decode("utf-8")
        
        else:
            raise HTTPException(
                status_code=400,
                detail="Format file tidak didukung. Silakan unggah .pdf, .docx, atau .txt."
            )
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Terjadi kesalahan saat membaca file: {str(e)}"
        )

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        load_model()
        yield
    finally:
        global model, tokenizer
        model = None
        tokenizer = None

app = FastAPI(
    title="Automated Essay Scoring API",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/predict")
async def process_essay(file: UploadFile = File(...)):
    """Endpoint untuk ekstraksi teks dan prediksi skor dalam satu request."""
    essay_text = extract_text(file)  # Mengekstrak teks dari file
    score_data = predict_score(essay_text)  # Menilai teks untuk mendapatkan skor
    
    return {
        "essay_text": essay_text,  # Mengembalikan teks esai
        "score": score_data["score"],  # Skor prediksi
        "description": score_data["description"]  # Deskripsi skor
    }
