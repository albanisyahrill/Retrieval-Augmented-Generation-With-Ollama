from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class UserInput(BaseModel):
    """
    Model for validating user input
    """
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "input_prompt": "undang undang mana yang mengatur mengenai kenegaraan"
            }
        }
    )
    
    input_prompt: str = Field(
        ..., 
        description="Teks pertanyaan dari pengguna",
        json_schema_extra={"example": "undang undang mana yang mengatur mengenai kenegaraan"}
    )
    

class AnswerResponse(BaseModel):
    """
    Model for validating the answer response
    """
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success": True,
                "input_prompt": "undang undang mana yang mengatur mengenai kenegaraan",
                "answer": "Undang-Undangnya diatur pada Undang-Undang Nomor 24 Tahun 2009 tentang Bendera, Bahasa, dan Lambang Negara, serta Lagu Kebangsaan. Terima kasih sudah bertanya!",
                "docs_and_scores": {"Undang-Undang Mengenai kenegaraan diatur pada...": 0.9876,
                                    "Undang-Undang Mengenai kenegaraan diatur pada bla": 0.9543,
                                    "Undang-Undang Mengenai kenegaraan diatur pada blabla": 0.9126
                                    },
                "input_tokens": 103,
                "output_tokens": 234,
                "total_tokens": 337
            }
        }
    )
    
    success: bool = Field(..., description="Status prediksi")
    input_prompt: str = Field(..., description="Teks pertanyaan dari pengguna")
    answer: str = Field(..., description="Jawaban dari LLM")
    docs_and_scores: dict = Field(..., description="Dokumen pendukung beserta skor kemiripannya")
    input_tokens: Optional[int] = Field(None, description="Jumlah token input yang digunakan")
    output_tokens: Optional[int] = Field(None, description="Jumlah token output yang dihasilkan")
    total_tokens: Optional[int] = Field(None, description="Total token yang digunakan")