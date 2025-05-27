# 🐍 Python VK & Video Downloader

📅 Последнее обновление: 2025-05-27

Простой скрипт на Python для скачивания видео с ВКонтакте и других сайтов, поддерживаемых [`yt-dlp`](https://github.com/yt-dlp/yt-dlp). Поддерживает загрузку приватных видео через cookies, консольное меню и настройку папки для сохранения файлов.

---

## 📚 Оглавление

- [Возможности](#возможности)
- [Требования](#требования)
- [Установка](#установка)
- [Настройка cookies для VK](#настройка-cookies-для-vk)
- [Запуск скрипта](#запуск-скрипта)
- [Частые проблемы](#частые-проблемы)
- [Лицензия](#лицензия)
- [Благодарности](#благодарности)

---

## ✅ Возможности

- Скачивание видео с **VK** и других платформ (`YouTube`, `Rutube`, `TikTok`, и т.д.)
- Поддержка **приватных** видео через cookies
- Консольное меню для управления загрузками
- Возможность выбрать папку сохранения
- Отображение прогресса загрузки

---

## ⚙️ Требования

- **Python** 3.7 или новее
- **yt-dlp** (`pip install yt-dlp`)
- **FFmpeg** (рекомендуется для объединения аудио/видео)

---

## 💾 Установка

### 1. Установка Python

1. Перейдите на сайт: [python.org/downloads](https://www.python.org/downloads/)
2. Скачайте и установите Python.
3. Во время установки **поставьте галочку "Add Python to PATH"**.

Проверьте установку:

```bash
python --version
pip --version
```

### 2. Скачивание скрипта

- Скачайте ZIP с GitHub или клонируйте репозиторий:

```bash
git clone https://github.com/your_username/vk-video-downloader.git
```

- Распакуйте в удобную папку:

```plaintext
C:\Users\Вы\Documents\VK_Downloader\
```

### 3. Установка yt-dlp

```bash
pip install yt-dlp
```

### 4. Установка FFmpeg

**Windows:**

1. Скачайте FFmpeg: [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)
2. Рекомендуем сборки от [gyan.dev](https://www.gyan.dev/ffmpeg/builds/)
3. Распакуйте и добавьте `bin/` в переменную среды `PATH`
4. Проверьте установку:

```bash
ffmpeg -version
```

**macOS:**

```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**

```bash
sudo apt update && sudo apt install ffmpeg
```

---

## 🍪 Настройка Cookies для VK

### Зачем нужны cookies?

Приватные видео доступны только авторизованным пользователям. Скрипт использует cookies, чтобы представиться как вы.

### Получение cookies:

1. Используйте Firefox и расширение [`cookies.txt`](https://addons.mozilla.org/en-US/firefox/addon/cookies-txt/)
2. Авторизуйтесь на [vk.com](https://vk.com)
3. Кликните по иконке расширения
4. Нажмите “Download cookies.txt”
5. Переименуйте в `vk_cookies.txt` и положите рядом со скриптом

Пример строки в файле:

```txt
.vk.com	TRUE	/	TRUE	1700000000	remixsid	abc123456...
```

---

## 🚀 Запуск скрипта

1. Откройте терминал или командную строку
2. Перейдите в папку:

```bash
cd путь_к_папке_со_скриптом
```

3. Запустите:

```bash
python dw.py
```

4. Следуйте меню:
   - Введите URL
   - Укажите путь к cookies (например, `vk_cookies.txt`)
   - Выберите папку для скачивания
   - Запустите загрузку

---

## 🛠 Частые проблемы

| Ошибка                                              | Решение                                                     |
| --------------------------------------------------- | ----------------------------------------------------------- |
| `'python' is not recognized`                        | Python не в PATH. Переустановите с галочкой `Add to PATH`   |
| `No module named 'yt_dlp'`                          | Установите: `pip install yt-dlp`                            |
| `does not look like a Netscape format cookies file` | Используйте расширение `cookies.txt` для Firefox            |
| Видео без звука или не открывается                  | Установите FFmpeg                                           |
| `This video is only available for registered users` | Проверьте cookies: залогиньтесь и экспортируйте файл заново |

---

## 📄 Лицензия

Проект распространяется "как есть", без гарантий. Используйте на свой страх и риск. Соблюдайте законы и авторские права.

---

## 🙏 Благодарности

- Разработчикам [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- Сообществу Python
- Firefox и расширению `cookies.txt`

---

*Хочешь добавить GUI, .bat-файл или drag-and-drop? Напиши — помогу!*
