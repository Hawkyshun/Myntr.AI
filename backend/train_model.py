import pandas as pd
import numpy as np
from datasets import load_dataset
from transformers import (
    AutoTokenizer, 
    AutoModelForCausalLM,
    TrainingArguments, 
    Trainer,
    DataCollatorForLanguageModeling
)
import torch
from sklearn.model_selection import train_test_split
import logging
import os

# Logging ayarları
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FinanceModelTrainer:
    def __init__(self, base_model="dbmdz/bert-base-turkish-cased"):
        self.base_model = base_model
        self.tokenizer = AutoTokenizer.from_pretrained(base_model)
        self.model = AutoModelForCausalLM.from_pretrained(base_model)
        
        # Özel tokenler ekleme
        special_tokens = {
            'additional_special_tokens': [
                '[SORU]', '[CEVAP]', '[ÖNERİ]', '[BAĞLAM]',
                '[RİSK_DÜŞÜK]', '[RİSK_ORTA]', '[RİSK_YÜKSEK]'
            ]
        }
        self.tokenizer.add_special_tokens(special_tokens)
        self.model.resize_token_embeddings(len(self.tokenizer))

    def prepare_worldbank_data(self):
        """Dünya Bankası verilerini hazırla"""
        try:
            df = pd.read_csv("datasets/worldbank-global-financial-development.csv")
            turkey_data = df[df['country_name'] == 'Turkey']
            
            # Veri formatını eğitim için hazırla
            contexts = []
            for _, row in turkey_data.iterrows():
                context = f"""[BAĞLAM]
                Borsa değeri/GSYİH: {row['stock_market_capitalization_to_gdp']}%
                Banka kredileri/GSYİH: {row['bank_credit_to_bank_deposits']}%
                Finansal sistem mevduatları/GSYİH: {row['financial_system_deposits_to_gdp']}%
                [BAĞLAM]"""
                contexts.append(context)
            
            return contexts
        except Exception as e:
            logger.error(f"Dünya Bankası verileri hazırlanırken hata: {str(e)}")
            return []

    def prepare_turkish_finance_data(self):
        """Türkçe finans datasetini hazırla"""
        try:
            dataset = load_dataset("yusufbaykaloglu/turkish-finance-dataset")
            finance_data = []
            
            for item in dataset['train']:
                # Soru-cevap formatını düzenle
                qa_pair = f"""[SORU]{item['question']}[SORU]
                [CEVAP]{item['answer']}[CEVAP]"""
                finance_data.append(qa_pair)
            
            return finance_data
        except Exception as e:
            logger.error(f"Türkçe finans verileri hazırlanırken hata: {str(e)}")
            return []

    def combine_datasets(self):
        """Tüm veri setlerini birleştir"""
        worldbank_contexts = self.prepare_worldbank_data()
        finance_qa = self.prepare_turkish_finance_data()
        
        # Veri setlerini birleştir ve karıştır
        combined_data = []
        for qa in finance_qa:
            if worldbank_contexts:
                context = np.random.choice(worldbank_contexts)
                combined_data.append(f"{context}\n{qa}")
            else:
                combined_data.append(qa)
        
        return combined_data

    def prepare_training_data(self):
        """Eğitim verilerini hazırla"""
        combined_data = self.combine_datasets()
        
        # Train-validation split
        train_texts, val_texts = train_test_split(
            combined_data, 
            test_size=0.1, 
            random_state=42
        )
        
        # Tokenize
        train_encodings = self.tokenizer(
            train_texts,
            truncation=True,
            padding=True,
            max_length=512,
            return_tensors="pt"
        )
        
        val_encodings = self.tokenizer(
            val_texts,
            truncation=True,
            padding=True,
            max_length=512,
            return_tensors="pt"
        )
        
        # Dataset oluştur
        train_dataset = FinanceDataset(train_encodings)
        val_dataset = FinanceDataset(val_encodings)
        
        return train_dataset, val_dataset

    def train(self, output_dir="models/myntr-ai-v0.1"):
        """Modeli eğit"""
        try:
            train_dataset, val_dataset = self.prepare_training_data()
            
            training_args = TrainingArguments(
                output_dir=output_dir,
                num_train_epochs=3,
                per_device_train_batch_size=8,
                per_device_eval_batch_size=8,
                warmup_steps=500,
                weight_decay=0.01,
                logging_dir='./logs',
                logging_steps=100,
                evaluation_strategy="steps",
                eval_steps=500,
                save_steps=1000,
                save_total_limit=2,
            )
            
            data_collator = DataCollatorForLanguageModeling(
                tokenizer=self.tokenizer,
                mlm=False
            )
            
            trainer = Trainer(
                model=self.model,
                args=training_args,
                train_dataset=train_dataset,
                eval_dataset=val_dataset,
                data_collator=data_collator,
            )
            
            logger.info("Model eğitimi başlıyor...")
            trainer.train()
            
            # Modeli kaydet
            self.model.save_pretrained(output_dir)
            self.tokenizer.save_pretrained(output_dir)
            logger.info(f"Model başarıyla kaydedildi: {output_dir}")
            
        except Exception as e:
            logger.error(f"Model eğitimi sırasında hata: {str(e)}")

class FinanceDataset(torch.utils.data.Dataset):
    def __init__(self, encodings):
        self.encodings = encodings

    def __getitem__(self, idx):
        return {key: val[idx] for key, val in self.encodings.items()}

    def __len__(self):
        return len(self.encodings.input_ids)

if __name__ == "__main__":
    # Model eğitimini başlat
    trainer = FinanceModelTrainer()
    trainer.train() 