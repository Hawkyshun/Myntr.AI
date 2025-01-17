from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import yfinance as yf
import pandas as pd
import numpy as np
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from datasets import load_dataset
import re

app = FastAPI(title="Myntr.AI v0.1 - Finansal Danışmanlık API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Model ve tokenizer yükleme
MODEL_NAME = "yusufbaykaloglu/turkish-finance-chat"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)

# Dünya Bankası finansal verilerini yükleme
def load_worldbank_data():
    try:
        df = pd.read_csv("datasets/worldbank-global-financial-development.csv")
        return df
    except Exception as e:
        print(f"Dünya Bankası verileri yüklenirken hata: {str(e)}")
        return None

# Türkçe finans datasetini yükleme
def load_turkish_finance_data():
    try:
        dataset = load_dataset("yusufbaykaloglu/turkish-finance-dataset")
        return dataset
    except Exception as e:
        print(f"Türkçe finans verileri yüklenirken hata: {str(e)}")
        return None

# Veri setlerini yükleme
worldbank_data = load_worldbank_data()
turkish_finance_data = load_turkish_finance_data()

class FinancialQuery(BaseModel):
    question: str
    risk_tolerance: str = "medium"

class FinancialAdvice(BaseModel):
    answer: str
    recommendations: List[str]
    additional_info: Optional[dict] = None

def generate_ai_response(question: str, context: str = "") -> str:
    try:
        # Prompt hazırlama
        prompt = f"Soru: {question}\nBağlam: {context}\nCevap:"
        
        # Model girdisi hazırlama
        inputs = tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True)
        
        # Yanıt oluşturma
        outputs = model.generate(
            inputs["input_ids"],
            max_length=1024,
            num_return_sequences=1,
            temperature=0.7,
            top_p=0.9,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id
        )
        
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response.split("Cevap:")[-1].strip()
    except Exception as e:
        print(f"AI yanıtı oluşturulurken hata: {str(e)}")
        return None

def get_market_context(risk_tolerance: str) -> str:
    if worldbank_data is not None:
        try:
            # Türkiye'ye ait güncel finansal göstergeleri filtreleme
            turkey_data = worldbank_data[worldbank_data['country_name'] == 'Turkey'].tail(1)
            
            context = f"""
            Risk toleransı: {risk_tolerance}
            Piyasa göstergeleri:
            - Borsa değeri/GSYİH: {turkey_data['stock_market_capitalization_to_gdp'].values[0]:.2f}%
            - Banka kredileri/GSYİH: {turkey_data['bank_credit_to_bank_deposits'].values[0]:.2f}%
            - Finansal sistem mevduatları/GSYİH: {turkey_data['financial_system_deposits_to_gdp'].values[0]:.2f}%
            """
            return context
        except Exception as e:
            print(f"Piyasa bağlamı oluşturulurken hata: {str(e)}")
    return ""

def analyze_question(question: str, risk_tolerance: str) -> FinancialAdvice:
    try:
        # Piyasa bağlamını al
        market_context = get_market_context(risk_tolerance)
        
        # AI yanıtı oluştur
        ai_response = generate_ai_response(question, market_context)
        
        if ai_response:
            # Yanıtı işle ve yapılandır
            recommendations = []
            allocation = {}
            
            # Yanıttan önerileri çıkar
            response_parts = ai_response.split("\n")
            main_answer = response_parts[0]
            
            for part in response_parts[1:]:
                if part.strip().startswith("-"):
                    recommendations.append(part.strip()[2:])
                elif ":" in part:
                    key, value = part.split(":")
                    if "%" in value:
                        allocation[key.strip()] = value.strip()
            
            return FinancialAdvice(
                answer=main_answer,
                recommendations=recommendations if recommendations else ["Öneriler oluşturulamadı."],
                additional_info={"suggested_allocation": allocation} if allocation else None
            )
    except Exception as e:
        print(f"Soru analizi sırasında hata: {str(e)}")
    
    # Hata durumunda varsayılan yanıt
    return FinancialAdvice(
        answer="Üzgünüm, şu anda yanıt oluşturulamıyor. Lütfen daha sonra tekrar deneyin.",
        recommendations=["Sistem şu anda bakımda."],
        additional_info=None
    )

@app.post("/analyze", response_model=FinancialAdvice)
async def analyze_query(query: FinancialQuery):
    try:
        return analyze_question(query.question, query.risk_tolerance)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/market-data/{symbol}")
async def get_market_data(symbol: str):
    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        return {
            "symbol": symbol,
            "current_price": info.get("currentPrice"),
            "company_name": info.get("longName"),
            "market_cap": info.get("marketCap"),
            "pe_ratio": info.get("trailingPE")
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Symbol {symbol} not found or error occurred") 