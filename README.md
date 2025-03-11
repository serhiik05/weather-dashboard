# Weather Dashboard

## 1. Опис проєкту

**Weather Dashboard** — це веб-застосунок для відстеження та візуалізації погодних даних у реальному часі. Він отримує інформацію з **WeatherAPI** та відображає її у зручному форматі. 

(https://prnt.sc/aY6WA4bX_Ned)

(https://prnt.sc/gXai114XV-dJ)

(https://prnt.sc/8dEZgxfkRhiS)

(https://prnt.sc/EnZGtYZXc4t-)

(https://prnt.sc/p2ZRTdoCFeWo)

(https://prnt.sc/5TRpvMGbSzdL)

- **Backend**: Django + Django REST Framework (DRF)  
- **Frontend**: HTML / CSS / JavaScript  
- **Сховище даних**: PostgreSQL  
- **Фонові завдання**: Celery + Redis  

### Основні можливості

- **Актуальні погодні дані** — отримання з **WeatherAPI**  
- **Збереження історичних даних** — запис до **PostgreSQL**  
- **Плановий збір даних** — через **Celery** (з Redis як broker/beat)  
- **REST API** — для взаємодії з клієнтськими застосунками  

---

## 2. Інструкція з встановлення (Setup instructions)

### 2.1 Клонування репозиторію

```bash
git clone https://github.com/serhiik05/weather-dashboard.git
cd weather-dashboard
