# Weather Dashboard

## 1. Опис проєкту

**Weather Dashboard** — це веб-застосунок для відстеження та візуалізації погодних даних у реальному часі. Він отримує інформацію з **WeatherAPI** та відображає її у зручному форматі. 

<img width="1352" alt="Screenshot 2025-03-11 at 17 21 39" src="https://github.com/user-attachments/assets/cf632018-0be7-4ddc-a982-dd14253831d6" />

<img width="1352" alt="Screenshot 2025-03-11 at 17 21 52" src="https://github.com/user-attachments/assets/9c6b3d48-ffcd-4dd5-bb75-1b290d75947a" />

<img width="1352" alt="Screenshot 2025-03-11 at 17 22 01" src="https://github.com/user-attachments/assets/a7ee8524-2065-4145-825e-b07d9bc521fd" />


<img width="1352" alt="Screenshot 2025-03-11 at 17 22 14" src="https://github.com/user-attachments/assets/23761647-14e2-4271-8f29-f184ecbfa9f2" />

<img width="1352" alt="Screenshot 2025-03-11 at 17 22 24" src="https://github.com/user-attachments/assets/0102ae76-d997-4dc4-91e9-f81e4bd32bb8" />


<img width="1352" alt="Screenshot 2025-03-11 at 17 22 50" src="https://github.com/user-attachments/assets/2b0792e6-ce20-4d50-a8f4-2b5f80e6e6d1" />

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
