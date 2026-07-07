# Software Requirements Specification (SRS)
# SI-NUTRI BALITA - Sistem Pakar Kalkulator Stunting

---

| **Document Information** | |
|-------------------------|--------------------------------------------------------------|
| **Project Name** | SI-NUTRI BALITA (Sistem Pakar Prediksi Gizi Balita) |
| **Version** | 1.0.0 |
| **Date** | 7 Juli 2026 |
| **Author** | [Nama Mahasiswa] - [NIM] |
| **Course** | Pemrograman Berorientasi Objek - Semester 4 |
| **Institution** | [Nama Universitas] |
| **Document Status** | Final |

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Overall Description](#2-overall-description)
3. [System Requirements](#3-system-requirements)
4. [Functional Requirements](#4-functional-requirements)
5. [Non-Functional Requirements](#5-non-functional-requirements)
6. [System Architecture](#6-system-architecture)
7. [Data Model](#7-data-model)
8. [API Specification](#8-api-specification)
9. [User Interface Design](#9-user-interface-design)
10. [Testing Requirements](#10-testing-requirements)
11. [References](#11-references)

---

## 1. Introduction

### 1.1 Purpose

Software Requirements Specification (SRS) ini mendefinisikan persyaratan fungsional dan non-fungsional untuk sistem **SI-NUTRI BALITA**, sebuah sistem pakar berbasis web untuk deteksi dini status gizi balita menggunakan standar antropometri dari Permenkes No. 2 Tahun 2020 dan WHO.

### 1.2 Document Scope

Dokumen ini mencakup seluruh persyaratan teknis untuk pengembangan sistem yang terdiri dari:
- Backend API menggunakan FastAPI (Python)
- Frontend Single-Page Application (HTML/CSS/JavaScript)
- Database standar gizi WHO dalam format JSON
- Sistem penyimpanan riwayat lokal (LocalStorage)

### 1.3 Intended Audience

- Developer dan Programmer
- Dosen Pembimbing Mata Kuliah PBO
- User Akhir (Orang Tua, Kader Posyandu, Tenaga Kesehatan)
- Stakeholder Kesehatan Anak

### 1.4 Product Overview

**SI-NUTRI BALITA** adalah sistem pakar yang menghitung status gizi balita berdasarkan parameter antropometri (berat badan, tinggi badan, umur, jenis kelamin) dan memberikan rekomendasi medis sesuai standar Permenkes 2020.

#### Key Features:
1. ✅ Kalkulasi Z-Score BB/U (Berat Badan menurut Umur)
2. ✅ Kalkulasi Z-Score TB/U (Tinggi Badan menurut Umur)
3. ✅ Klasifikasi Status Gizi (Normal, Stunted, Severely Stunted, dll)
4. ✅ Analisis Tren Pertumbuhan Bulanan
5. ✅ Rekomendasi Tindakan Gizi Berbasis Evidence
6. ✅ Riwayat Pengukuran Lokal
7. ✅ Share Laporan ke WhatsApp

---

## 2. Overall Description

### 2.1 System Philosophy

Sistem ini dirancang dengan filosofi **"Deteksi Dini, Tindakan Tepat"** - memberikan kemampuan skrining awal gizi balita secara instan dengan presisi tinggi berbasis standar medis resmi.

### 2.2 System Goals

| Goal | Description |
|------|-------------|
| **G1** | Menyediakan kalkulator status gizi balita yang akurat sesuai standar WHO |
| **G2** | Mendeteksi dini kasus stunting pada balita 0-60 bulan |
| **G3** | Memberikan rekomendasi tindakan gizi yang sesuai Permenkes 2020 |
| **G4** | Memfasilitasi tracking riwayat tumbuh kembang balita |
| **G5** | Mendukung pelaporan otomatis ke WhatsApp untuk konsultasi medis |

### 2.3 System Context

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER ACTORS                                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ Orang Tua    │  │ Kader         │  │ Tenaga Medis  │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     SI-NUTRI BALITA SYSTEM                       │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │              FRONTEND (Single-Page Application)              │ │
│  │  • Input Form (Nama, JK, Umur, BB, TB)                      │ │
│  │  • Result Dashboard (Status Gizi, Z-Score, Saran)           │ │
│  │  • History Management (LocalStorage)                        │ │
│  │  • WhatsApp Integration                                      │ │
│  └────────────────────────────────────────────────────────────┘ │
│                              │ REST API                           │
│                              ▼                                    │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │              BACKEND (FastAPI Server)                        │ │
│  │  • POST /api/evaluasi (Calculate Z-Score)                  │ │
│  │  • Z-Score Calculation Engine                               │ │
│  │  • Growth Trend Analysis                                    │ │
│  └────────────────────────────────────────────────────────────┘ │
│                              │                                    │
│                              ▼                                    │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │         DATA LAYER (Standar Permenkes JSON)                │ │
│  │  • WHO Growth Standards (BB/U, TB/U)                        │ │
│  │  • Reference Median & SD Values                             │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

### 2.4 User Characteristics

| Actor | Description | Technical Proficiency |
|-------|-------------|----------------------|
| **Orang Tua** | Pengguna utama yang ingin memantau gizi balita | Low-Medium |
| **Kader Posyandu** | Petugas kesehatan desa/urban | Medium |
| **Tenaga Medis** | Dokter/Bidan/Perawat | Medium-High |

### 2.5 Constraints

| Constraint | Description |
|-----------|-------------|
| **C1** | Sistem harus mengikuti standar Permenkes No. 2 Tahun 2020 |
| **C2** | Rentang umur balita: 0-60 bulan (5 tahun) |
| **C3** | Backend harus menggunakan FastAPI dengan Python |
| **C4** | Frontend harus berupa Single-Page Application tanpa framework |
| **C5** | Data riwayat disimpan di LocalStorage (max 20 record) |
| **C6** | Sistem harus dapat berjalan offline (kecuali API call) |

### 2.6 Assumptions and Dependencies

| Assumption | Description |
|------------|-------------|
| **A1** | Pengguna memiliki browser modern dengan JavaScript enabled |
| **A2** | Backend FastAPI berjalan di `http://127.0.0.1:8000` |
| **A3** | Standar WHO Growth Standards yang digunakan valid dan terkini |
| **A4** | Pengguna menginputkan data antropometri dengan benar |

---

## 3. System Requirements

### 3.1 Hardware Requirements

#### Minimum Requirements:
- **Processor**: Intel Core i3 / AMD equivalent atau lebih tinggi
- **RAM**: 4 GB
- **Storage**: 100 MB available space
- **Network**: Koneksi internet untuk share WhatsApp

#### Recommended:
- **Processor**: Intel Core i5 / AMD equivalent
- **RAM**: 8 GB
- **Storage**: 500 MB SSD

### 3.2 Software Requirements

#### Backend:
- **OS**: Windows 10/11, Linux (Ubuntu 20.04+), macOS 10.15+
- **Python Version**: Python 3.8 atau lebih tinggi
- **Dependencies**:
  - FastAPI >= 0.68.0
  - Pydantic >= 1.8.0
  - uvicorn >= 0.15.0
  - CORS Middleware

#### Frontend:
- **Browser**: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+
- **JavaScript**: ES6+ support required
- **CSS**: Tailwind CSS via CDN
- **Libraries**: Font Awesome 6.4.0 (via CDN)

---

## 4. Functional Requirements

### 4.1 Input Data Module (FR-01)

| ID | Requirement | Priority |
|----|-------------|----------|
| **FR-01.1** | Sistem harus menyediakan form input untuk data balita: Nama, Jenis Kelamin (L/P), Umur (0-60 bulan), Berat Badan (kg), Tinggi Badan (cm) | **Mandatory** |
| **FR-01.2** | Sistem harus menyediakan input opsional untuk data bulan lalu: Berat Badan Lalu, Tinggi Badan Lalu | **Optional** |
| **FR-01.3** | Sistem harus melakukan validasi input: Umur 0-60, Berat > 0, Tinggi > 0, JK harus dipilih | **Mandatory** |
| **FR-01.4** | Sistem harus memberikan error message jika input tidak valid | **Mandatory** |

### 4.2 Z-Score Calculation Module (FR-02)

| ID | Requirement | Priority |
|----|-------------|----------|
| **FR-02.1** | Sistem harus menghitung Z-Score BB/U menggunakan rumus: (Nilai Aktual - Median) / Simpang Baku | **Mandatory** |
| **FR-02.2** | Sistem harus menghitung Z-Score TB/U menggunakan rumus yang sama | **Mandatory** |
| **FR-02.3** | Sistem harus mengambil nilai Median dan SD dari database standar Permenkes berdasarkan umur dan jenis kelamin | **Mandatory** |
| **FR-02.4** | Sistem harus menangani kasus pembagian dengan nol (jika SD = 0) | **Mandatory** |

### 4.3 Status Classification Module (FR-03)

| ID | Requirement | Priority |
|----|-------------|----------|
| **FR-03.1** | Sistem harus mengklasifikasikan status BB/U berdasarkan Z-Score: | **Mandatory** |
| | • Z < -3.0: "Berat Badan Sangat Kurang" | |
| | • -3.0 ≤ Z < -2.0: "Berat Badan Kurang" | |
| | • -2.0 ≤ Z ≤ 1.0: "Berat Badan Normal" | |
| | • Z > 1.0: "Risiko Berat Badan Lebih" | |
| **FR-03.2** | Sistem harus mengklasifikasikan status TB/U berdasarkan Z-Score: | **Mandatory** |
| | • Z < -3.0: "Sangat Pendek (Severely Stunted)" | |
| | • -3.0 ≤ Z < -2.0: "Pendek (Stunted)" | |
| | • -2.0 ≤ Z ≤ 3.0: "Normal" | |
| | • Z > 3.0: "Tinggi" | |

### 4.4 Recommendation Module (FR-04)

| ID | Requirement | Priority |
|----|-------------|----------|
| **FR-04.1** | Sistem harus memberikan saran medis sesuai status BB/U | **Mandatory** |
| **FR-04.2** | Sistem harus memberikan saran medis sesuai status TB/U | **Mandatory** |
| **FR-04.3** | Sistem harus memberikan saran umum tentang ASI Eksklusif dan MPASI | **Mandatory** |

### 4.5 Growth Trend Analysis Module (FR-05)

| ID | Requirement | Priority |
|----|-------------|----------|
| **FR-05.1** | Jika data bulan lalu tersedia, sistem harus menghitung kenaikan BB dan TB | **Mandatory** |
| **FR-05.2** | Sistem harus membandingkan kenaikan aktual dengan target minimal Permenkes | **Mandatory** |
| **FR-05.3** | Sistem harus memberikan status tren: "Naik Cukup" atau "Kenaikan Kurang" | **Mandatory** |
| **FR-05.4** | Jika data bulan lalu tidak ada, sistem harus menampilkan pesan "Data Bulan Lalu Belum Ada" | **Mandatory** |

### 4.6 History Management Module (FR-06)

| ID | Requirement | Priority |
|----|-------------|----------|
| **FR-06.1** | Sistem harus menyimpan hasil analisis ke LocalStorage browser | **Mandatory** |
| **FR-06.2** | Sistem harus menyimpan maksimal 20 record riwayat (FIFO) | **Mandatory** |
| **FR-06.3** | Sistem harus menyediakan fitur view riwayat dalam drawer/sidebar | **Mandatory** |
| **FR-06.4** | Sistem harus menyediakan fitur delete single history | **Mandatory** |
| **FR-06.5** | Sistem harus menyediakan fitur clear all history | **Mandatory** |
| **FR-06.6** | Sistem harus dapat reload riwayat untuk ditampilkan kembali | **Mandatory** |

### 4.7 WhatsApp Sharing Module (FR-07)

| ID | Requirement | Priority |
|----|-------------|----------|
| **FR-07.1** | Sistem harus menyediakan tombol share ke WhatsApp | **Mandatory** |
| **FR-07.2** | Sistem harus generate text laporan dalam format WhatsApp | **Mandatory** |
| **FR-07.3** | Text laporan harus mencakup: Biodata, Status Gizi, Z-Score, Rekomendasi | **Mandatory** |
| **FR-07.4** | Sistem harus membuka WhatsApp API dengan formatted text | **Mandatory** |

---

## 5. Non-Functional Requirements

### 5.1 Performance Requirements

| ID | Requirement | Metric |
|----|-------------|--------|
| **NFR-01** | Response time untuk API /api/evaluasi | ≤ 500 ms |
| **NFR-02** | Page load time untuk frontend | ≤ 2 seconds |
| **NFR-03** | Render time untuk result screen | ≤ 300 ms |
| **NFR-04** | LocalStorage read/write operation | ≤ 100 ms |

### 5.2 Usability Requirements

| ID | Requirement | Description |
|----|-------------|-------------|
| **NFR-05** | UI harus responsif | Mobile-friendly, tablet-friendly, desktop-friendly |
| **NFR-06** | Navigasi harus intuitif | Maximum 2 clicks untuk sampai ke fitur utama |
| **NFR-07** | Feedback visual harus jelas | Loading state, success/error message |
| **NFR-08** | Form harus user-friendly | Clear label, placeholder, validation message |

### 5.3 Reliability Requirements

| ID | Requirement | Metric |
|----|-------------|--------|
| **NFR-09** | System uptime | Target 99% saat development |
| **NFR-10** | Data integrity | Z-Score calculation harus 100% akurat sesuai standar WHO |
| **NFR-11** | Error handling | Graceful failure jika backend tidak accessible |

### 5.4 Security Requirements

| ID | Requirement | Description |
|----|-------------|-------------|
| **NFR-12** | Data privacy | Tidak ada data personal yang dikirim ke external server selain localhost |
| **NFR-13** | Input sanitization | Backend harus memvalidasi semua input menggunakan Pydantic |
| **NFR-14** | CORS policy | Backend harus mengizinkan origin tertentu saja |

### 5.5 Maintainability Requirements

| ID | Requirement | Description |
|----|-------------|-------------|
| **NFR-15** | Code documentation | Setiap function/class harus memiliki docstring |
| **NFR-16** | Code structure | Menggunakan OOP principles: Class, Object, Inheritance, Polymorphism |
| **NFR-17** | Naming convention | Mengikuti PEP 8 untuk Python |

### 5.6 Compatibility Requirements

| ID | Requirement | Description |
|----|-------------|-------------|
| **NFR-17** | Browser compatibility | Chrome, Firefox, Safari, Edge (versi 2 tahun terakhir) |
| **NFR-18** | OS compatibility | Windows 10+, macOS 10.15+, Linux (Ubuntu 20.04+) |
| **NFR-19** | Screen resolution | Minimum 320px width (mobile) hingga 1920px (desktop) |

---

## 6. System Architecture

### 6.1 Architecture Overview

Sistem menggunakan arsitektur **Client-Server** dengan pendekatan **REST API**:

```
┌────────────────────────────────────────────────────────────────┐
│                     CLIENT SIDE (Frontend)                      │
│                  Single-Page Application                        │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  • HTML5 Structure                                       │  │
│  │  • Tailwind CSS (Styling)                                │  │
│  │  • Vanilla JavaScript (Logic)                            │  │
│  │  • Font Awesome (Icons)                                 │  │
│  │  • LocalStorage (Persistence)                           │  │
│  └────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────┘
                              │
                    HTTP/HTTPS (REST)
                              │
                              ▼
┌────────────────────────────────────────────────────────────────┐
│                    SERVER SIDE (Backend)                        │
│                     FastAPI Application                         │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  • Pydantic Models (Validation)                         │  │
│  │  • CORS Middleware (Cross-Origin)                        │  │
│  │  • Z-Score Calculator (Business Logic)                   │  │
│  │  • Standar Permenkes Loader (Data Access)               │  │
│  └────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌────────────────────────────────────────────────────────────────┐
│                      DATA LAYER                                  │
│              Standar Permenkes JSON File                         │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  • WHO Growth Standards Data                            │  │
│  │  • L (Laki-laki) & P (Perempuan)                         │  │
│  │  • BBU (Berat Badan menurut Umur)                        │  │
│  │  • TBU (Tinggi Badan menurut Umur)                       │  │
│  │  • SD Values (-3SD, -2SD, -1SD, Median, +1SD, +2SD)    │  │
│  └────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────┘
```

### 6.2 Technology Stack

#### Frontend Stack:
```
HTML5          ← Structure
Tailwind CSS   ← Styling (via CDN)
JavaScript ES6 ← Logic
Font Awesome   ← Icons (via CDN)
LocalStorage   ← Client-side Persistence
```

#### Backend Stack:
```
Python 3.8+    ← Core Language
FastAPI        ← Web Framework
Pydantic       ← Data Validation
Uvicorn        ← ASGI Server
JSON           ← Data Storage
```

### 6.3 Design Patterns

| Pattern | Implementation | Location |
|---------|----------------|----------|
| **Model-View-Controller (MVC)** | Frontend JavaScript = Controller, HTML = View, Backend = Model | Entire System |
| **Singleton** | Standar Permenkes data loaded once | `storage.py` |
| **Factory Pattern** | Z-Score calculation based on indicator type | `kalkulator.py` |
| **Strategy Pattern** | Different recommendation strategies per status | `kalkulator.py` |

---

## 7. Data Model

### 7.1 Input Data Model (Pydantic)

```python
class BalitaInput(BaseModel):
    umur_bulan: int           # 0-60 bulan
    jenis_kelamin: str        # "L" atau "P"
    berat_badan: float        # dalam kg
    tinggi_badan: float       # dalam cm
    berat_badan_lalu: Optional[float]  # opsional, kg
    tinggi_badan_lalu: Optional[float] # opsional, cm
```

### 7.2 Output Data Model

```python
class ApiResponse(BaseModel):
    status: str                    # "success" atau "error"
    biodata: Dict                  # {umur, jk}
    gizi: NutritionResult          # Z-Score & Status
    tren: TrendResult              # Kenaikan bulanan
```

### 7.3 Database Schema (Standar Permenkes JSON)

```json
{
  "L": {
    "BBU": {
      "0": {"-3SD": 2.1, "-2SD": 2.5, "-1SD": 2.9, "median": 3.3, "1SD": 3.9, "2SD": 4.4, "3SD": 5.0},
      "1": {...},
      ...
      "60": {...}
    },
    "TBU": {
      "0": {"-3SD": 44.2, "-2SD": 46.1, "-1SD": 48.0, "median": 49.9, "1SD": 51.8, "2SD": 53.7, "3SD": 55.6},
      ...
    }
  },
  "P": {
    "BBU": {...},
    "TBU": {...}
  }
}
```

### 7.4 LocalStorage Schema

```json
{
  "si_nutri_history": [
    {
      "nama": "string",
      "umur": 0,
      "jk": "string",
      "berat": 0.0,
      "tinggi": 0.0,
      "imt": 0.0,
      "gizi": {
        "indikator": {
          "BB_U": {"z_score": 0.0, "status": "string", "saran": "string"},
          "TB_U": {"z_score": 0.0, "status": "string", "saran": "string"}
        },
        "saran_umum": "string"
      },
      "tren": {...},
      "timestamp": "string"
    }
  ]
}
```

---

## 8. API Specification

### 8.1 Endpoint: Evaluate Nutrition

**Request:**
```
POST /api/evaluasi
Content-Type: application/json

{
  "umur_bulan": 12,
  "jenis_kelamin": "L",
  "berat_badan": 9.5,
  "tinggi_badan": 75.0,
  "berat_badan_lalu": 9.0,
  "tinggi_badan_lalu": 74.0
}
```

**Response (Success):**
```json
{
  "status": "success",
  "biodata": {
    "umur": 12,
    "jk": "L"
  },
  "gizi": {
    "indikator": {
      "BB_U": {
        "z_score": -1.2,
        "status": "Berat Badan Normal",
        "saran": "Pertahankan pola makan seimbang sesuai panduan Isi Piringku."
      },
      "TB_U": {
        "z_score": -1.5,
        "status": "Normal",
        "saran": "Lanjutkan pemberian gizi seimbang dan pantau tinggi setiap bulan."
      }
    },
    "saran_umum": "Pastikan balita mendapat ASI Eksklusif (jika < 6 bulan) dan MPASI adekuat (> 6 bulan). Patuhi jadwal imunisasi."
  },
  "tren": {
    "tren_berat_badan": {
      "kenaikan_aktual": "500 gram",
      "target_minimal": "200 gram",
      "status": "Naik Cukup (N)"
    },
    "tren_tinggi_badan": {
      "kenaikan_aktual": "1.0 cm",
      "target_minimal": "1.0 cm",
      "status": "Tumbuh Cukup"
    },
    "kesimpulan_tren": "Pertumbuhan Bagus!"
  }
}
```

**Response (Error):**
```json
{
  "error": "Data standar untuk umur tersebut belum tersedia di database."
}
```

---

## 9. User Interface Design

### 9.1 Screen Navigation

```
┌─────────────────────────────────────────────────────────────┐
│                    NAVIGATION FLOW                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐             │
│  │ Welcome  │───▶│  Input   │───▶│  Result  │             │
│  │  Screen  │    │  Screen  │    │  Screen  │             │
│  └──────────┘    └──────────┘    └──────────┘             │
│                                     │                        │
│                                     ▼                        │
│                              ┌──────────┐                   │
│                              │ History  │                   │
│                              │  Drawer  │                   │
│                              └──────────┘                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 9.2 Screen Descriptions

#### 9.2.1 Welcome Screen
- Hero section dengan CTA button
- 3 Feature highlights (API Perhitungan, Standar Permenkes, Log Riwayat)
- Clean, modern design dengan gradient emerald/teal

#### 9.2.2 Input Screen
- Form input dengan 2 column layout
- Gender selection dengan radio button custom style
- Umur/Berat/Tinggi input dengan center-aligned number
- Optional section untuk data bulan lalu
- Panduan akurat sidebar

#### 9.2.3 Result Screen
- Biodata card (Nama, JK, Umur, Berat, Tinggi, IMT)
- Gauge bar untuk visualisasi Z-Score BB/U
- Status card dengan color coding:
  - Red: Sangat Kurang / Severely Stunted
  - Amber: Kurang / Stunted  
  - Emerald: Normal
  - Purple: Risiko Lebih
- Trend analysis card (jika ada data bulan lalu)
- Rekomendasi tindakan gizi
- Action buttons: Share WhatsApp, Save to History

#### 9.2.4 History Drawer
- Slide-in drawer dari kanan
- List riwayat dengan status bullet color coding
- Delete single item button
- Clear all history button

### 9.3 Color Palette

| Color | Usage | Hex Code |
|-------|-------|----------|
| **Emerald 500** | Primary CTA, Success | `#10b981` |
| **Teal 600** | Secondary, Gradient | `#0d9488` |
| **Amber 500** | Warning | `#f59e0b` |
| **Red 500** | Error, Danger | `#ef4444` |
| **Slate 800** | Text Primary | `#1e293b` |
| **Slate 400** | Text Secondary | `#94a3b8` |

---

## 10. Testing Requirements

### 10.1 Unit Testing

| Component | Test Cases |
|-----------|------------|
| **Z-Score Calculator** | • Test Z-Score calculation with known values<br>• Test edge cases (SD = 0)<br>• Test negative Z-Score values |
| **Status Classification** | • Test all BB/U status categories<br>• Test all TB/U status categories<br>• Test boundary values |
| **Trend Analysis** | • Test with data bulan lalu<br>• Test without data bulan lalu<br>• Test target comparison |

### 10.2 Integration Testing

| Scenario | Test Cases |
|----------|------------|
| **API Integration** | • Test POST /api/evaluasi with valid payload<br>• Test with invalid payload<br>• Test backend unavailability |
| **LocalStorage** | • Test save to history<br>• Test load from history<br>• Test delete single item<br>• Test clear all history |

### 10.3 End-to-End Testing

| User Flow | Test Cases |
|-----------|------------|
| **Complete Analysis** | 1. Open app → 2. Fill form → 3. Submit → 4. View result → 5. Save to history → 6. Share WhatsApp |
| **History Reload** | 1. Open app → 2. View history → 3. Click item → 4. View result again |
| **Error Handling** | 1. Open app → 2. Submit without gender → 3. Verify error message |

### 10.4 Acceptance Testing

| Criteria | Acceptance Condition |
|----------|---------------------|
| **Accuracy** | Z-Score calculation must match WHO standards |
| **Usability** | User must be able to complete analysis in < 2 minutes |
| **Responsiveness** | UI must work on mobile (320px width) |
| **Performance** | API response time must be < 500ms |

---

## 11. References

### 11.1 Standards and Regulations

1. **Permenkes No. 2 Tahun 2020** - Standar Antropometri Penilaian Status Gizi Anak
2. **WHO Child Growth Standards** - Length/height-for-age, Weight-for-age
3. **PEP 8** - Style Guide for Python Code
4. **PEP 257** - Docstring Conventions

### 11.2 Technical Documentation

1. **FastAPI Documentation** - https://fastapi.tiangolo.com/
2. **Pydantic Documentation** - https://pydantic-docs.helpmanual.io/
3. **Tailwind CSS Documentation** - https://tailwindcss.com/docs
4. **Font Awesome** - https://fontawesome.com/docs

### 11.3 Academic Resources

1. **Matkul Pemrograman Berorientasi Objek** - Semester 4, [Nama Universitas]
2. **CLAUDE.md Project Guidelines** - Repository Documentation

---

## Appendix A: Glossary

| Term | Definition |
|------|------------|
| **Z-Score** | Standard deviation score; measure of how far a value is from the median |
| **BB/U** | Berat Badan menurut Umur (Weight-for-Age) |
| **TB/U** | Tinggi Badan menurut Umur (Height-for-Age) |
| **Stunted** | Pendek (tinggi badan < -2 SD) |
| **Severely Stunted** | Sangat Pendek (tinggi badan < -3 SD) |
| **Antropometri** | Pengukuran dimensi tubuh manusia |
| **Posyandu** | Pos Pelayanan Terpadu (Integrated Health Service Post) |
| **MPASI** | Makanan Pendamping ASI (Complementary Feeding) |

---

## Appendix B: Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 7 Juli 2026 | [Nama] | Initial SRS Release |

---

**END OF DOCUMENT**

---

> This SRS document is part of the Final Project for Object-Oriented Programming Course (Pemrograman Berorientasi Objek), Semester 4, 2026.
> 
> **Project Repository**: `H:\KULIAH\SEM4\Praktikum Pemrograman Berorientasi Objek\UAS\`
> 
> **Developer**: [Nama Mahasiswa] - [NIM]
