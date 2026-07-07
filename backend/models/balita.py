from pydantic import BaseModel, Field
from typing import Optional

class BalitaInput(BaseModel):
    umur_bulan: int = Field(..., ge=0, le=60, description="Umur anak dalam bulan (0-60)")
    jenis_kelamin: str = Field(..., pattern="^(L|P)$", description="L atau P")
    berat_badan: float = Field(..., gt=0, description="Berat badan sekarang (KG)")
    tinggi_badan: float = Field(..., gt=0, description="Tinggi badan sekarang (CM)")
    
    # Input opsional untuk menghitung tren increment
    berat_badan_lalu: Optional[float] = Field(None, description="Berat badan bulan lalu (KG)")
    tinggi_badan_lalu: Optional[float] = Field(None, description="Tinggi badan bulan lalu (CM)")