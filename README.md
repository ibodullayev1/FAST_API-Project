# FastAPI Kitoblar Boshqaruv Dasturi

Bu FastAPI yordamida yaratilgan Kitoblar Boshqaruv Dasturidir. Bu API foydalanuvchilarga kitoblarni qo‘shish, o‘zgartirish, o‘chirish va ko‘rish imkoniyatini beradi. Foydalanuvchilar JWT orqali autentifikatsiya qilishadi va faqat o‘z kitoblarini boshqarish imkoniyatiga ega bo‘lishadi.

## Talablar

- Python 3.7 yoki undan yuqori versiya
- Virtual environment
- FastAPI
- SQLAlchemy
- Alembic
- SQLite (yoki boshqa ma'lumotlar bazasi)

## O‘rnatish

1. **Virtual Muhitni Yaratish**:
 
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Linux/MacOS
   .venv\Scripts\activate      # Windows

2. **Kerakli Kutubxonalarni urnating**:
 
   ```bash
   pip install -r requirements.txt


3. **Ma'lumotlar Bazasi**:
 
   ```bash
    alembic upgrade head


4. **Serverni Ishga Tushirish:**:
 
   ```bash
    uvicorn app.main:app --reload



