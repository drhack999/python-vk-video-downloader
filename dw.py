import os
import sys

try:
    import yt_dlp
except ImportError:
    print("Ошибка: Модуль yt-dlp не найден.")
    print("Пожалуйста, установите его, выполнив команду в вашем терминале или командной строке:")
    print("pip install yt-dlp")
    print("\nЭтот скрипт требует yt-dlp для скачивания видео с VK и других сайтов.")
    sys.exit(1)

# --- Глобальные переменные для хранения состояния ---
urls_to_download = []
current_download_folder = "C:/Users/Admin/Desktop/coding/MyDownloadedVkVideos" # Ваш путь по умолчанию
cookies_file_path = None # Путь к файлу cookies


# --- Функции для работы с yt-dlp ---

def progress_hook(d):
    filename = d.get('filename')
    base_filename = "Processing..." 

    if filename:
        base_filename = os.path.basename(filename)
    elif d.get('info_dict'):
        base_filename = d['info_dict'].get('title', 'Extracting info...')

    if d['status'] == 'downloading':
        total_bytes_str = d.get('total_bytes_estimate', d.get('total_bytes'))
        downloaded_bytes_str = d.get('downloaded_bytes')

        if total_bytes_str is None or downloaded_bytes_str is None:
            print(f"\rDownloading {base_filename}: preparing...", end="")
            return

        try:
            total_bytes = float(total_bytes_str)
            downloaded_bytes = float(downloaded_bytes_str)
        except (ValueError, TypeError):
            print(f"\rDownloading {base_filename}: invalid byte data...", end="")
            return

        if total_bytes > 0:
            percentage = downloaded_bytes / total_bytes * 100
            speed_bytes_sec = d.get('speed')
            speed_val = f"{speed_bytes_sec / 1024 / 1024:.2f} MB/s" if speed_bytes_sec else "N/A"
            eta_seconds = d.get('eta')
            eta_val = f"{int(eta_seconds // 60)}m {int(eta_seconds % 60)}s" if eta_seconds is not None else "N/A"
            
            downloaded_mb = downloaded_bytes / (1024 * 1024)
            total_mb = total_bytes / (1024 * 1024)

            max_len_filename = 35
            display_filename = (base_filename[:max_len_filename-3] + '...') if len(base_filename) > max_len_filename else base_filename
            
            print(f"\rDownloading {display_filename}: {percentage:.1f}% of {total_mb:.2f}MB at {speed_val} (ETA: {eta_val})      ", end="")
        else:
            downloaded_mb = downloaded_bytes / (1024 * 1024)
            print(f"\rDownloading {base_filename}: {downloaded_mb:.2f}MB (total size unknown)      ", end="")

    elif d['status'] == 'finished':
        final_filepath = d.get('info_dict', {}).get('_filename', base_filename if base_filename != "Processing..." else "Unknown file")
        if not final_filepath or final_filepath == "NA":
            final_filepath = base_filename if base_filename != "Processing..." else "Unknown file"
        print(f"\nFinished: {os.path.basename(final_filepath)}")

    elif d['status'] == 'error':
        print(f"\nError during processing of {base_filename}. It might require login/cookies.")


class MyLogger:
    def debug(self, msg):
        if "deprecated" in msg.lower() or msg.startswith('[debug] '):
            pass

    def warning(self, msg):
        if "video is only available for registered users" in msg.lower() or \
           "sign up to watch videos without restrictions" in msg.lower() or \
           "this video is private" in msg.lower() or \
           "login required" in msg.lower():
            print(f"YDL_WARNING: {msg}")
            print("INFO: Это видео может требовать авторизации. Укажите файл cookies (опция 6).")
        else:
            print(f"YDL_WARNING: {msg}")

    def error(self, msg):
        print(f"YDL_ERROR: {msg}")


def download_video_with_yt_dlp(video_url, download_path, cookies_path=None):
    if not os.path.exists(download_path):
        try:
            os.makedirs(download_path)
            print(f"Создана папка для загрузок: {download_path}")
        except OSError as e:
            print(f"Ошибка при создании папки {download_path}: {e}")
            return False

    output_template = os.path.join(download_path, '%(title).180B [%(id)s].%(ext)s')

    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': output_template,
        'noplaylist': True,
        'progress_hooks': [progress_hook],
        'logger': MyLogger(),
        'noprogress': True,
        'postprocessors': [{'key': 'FFmpegEmbedSubtitle','already_have_subtitle': False}],
    }

    if cookies_path:
        if os.path.exists(cookies_path):
            ydl_opts['cookiefile'] = cookies_path
            print(f"Используется файл cookies: {cookies_path}")
        else:
            print(f"ПРЕДУПРЕЖДЕНИЕ: Файл cookies не найден по пути: {cookies_path}. Загрузка без cookies.")

    print(f"\nПопытка скачивания URL через yt-dlp: {video_url}")
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        return True
    except yt_dlp.utils.DownloadError:
        pass # yt-dlp сам выведет достаточно информации через логгер
    except Exception as e:
        print(f"Неожиданная ошибка при обработке {video_url} через yt-dlp: {e}")
    return False

# --- Функции для консольного меню ---

def display_main_menu():
    print("\n+-----------------------------------------+")
    print("|      VK & Video Downloader (yt-dlp)     |")
    print("+-----------------------------------------+")
    
    folder_display_name = current_download_folder
    max_len_display = 35 
    if len(folder_display_name) > max_len_display:
        folder_display_name = "..." + folder_display_name[-(max_len_display-3):]
    print(f"|  Загрузка в: {folder_display_name:<{max_len_display}} |")

    cookies_display_name = "Не указан"
    if cookies_file_path:
        cookies_display_name = os.path.basename(cookies_file_path)
        if len(cookies_display_name) > (max_len_display - len("Cookies: ")):
             cookies_display_name = "..." + cookies_display_name[-(max_len_display - len("Cookies: ") -3):]
    print(f"|  Cookies: {cookies_display_name:<{max_len_display-9}} |")
    
    print("+-----------------------------------------+")
    print("| 1. Добавить URL видео для скачивания    |")
    print("| 2. Показать список URL-адресов          |")
    print("| 3. Начать скачивание добавленных видео  |")
    print("| 4. Изменить папку для сохранения        |")
    print("| 5. Очистить список URL-адресов          |")
    print("| 6. Указать путь к файлу cookies (VK)    |")
    print("| 0. Выход                                |")
    print("+-----------------------------------------+")
    return input("Выберите опцию (0-6): ")

def add_url_ui():
    print("\n--- Добавление URL ---")
    print("Введите URL видео (или несколько URL через пробел/запятую):")
    urls_input = input("> ")
    added_urls = [url.strip() for url_group in urls_input.split(',') for url in url_group.split() if url.strip()]
    
    if not added_urls:
        print("Не введено ни одного URL.")
        return

    for url in added_urls:
        if url not in urls_to_download:
            urls_to_download.append(url)
            print(f"Добавлен URL: {url}")
        else:
            print(f"URL уже в списке: {url}")
    print(f"Всего URL в списке: {len(urls_to_download)}")


def show_urls_ui():
    print("\n--- Список URL для скачивания ---")
    if not urls_to_download:
        print("Список пуст. Добавьте URL с помощью опции '1'.")
        return
    for i, url in enumerate(urls_to_download, 1):
        print(f"{i}. {url}")

def start_download_ui():
    global current_download_folder, cookies_file_path
    print("\n--- Начало скачивания ---")
    if not urls_to_download:
        print("Нет URL для скачивания. Добавьте их сначала.")
        return
    
    if not os.path.exists(current_download_folder):
        try:
            os.makedirs(current_download_folder)
            print(f"Папка для загрузок '{current_download_folder}' создана.")
        except OSError as e:
            print(f"Критическая ошибка: Не удалось создать папку '{current_download_folder}': {e}")
            return

    print(f"Будет скачано {len(urls_to_download)} видео в папку: '{current_download_folder}'")
    if cookies_file_path:
        print(f"С использованием cookies из: '{cookies_file_path}'")
    else:
        print("Без использования cookies (некоторые видео могут быть недоступны).")
        
    confirm = input("Начать? (y/n): ").lower()
    if confirm != 'y':
        print("Скачивание отменено.")
        return

    successful_downloads = 0
    failed_downloads = 0
    urls_to_process = list(urls_to_download) 
    
    for i, url in enumerate(urls_to_process, 1):
        print(f"\n[{i}/{len(urls_to_process)}] Скачивание видео по URL: {url}")
        if download_video_with_yt_dlp(url, current_download_folder, cookies_file_path):
            successful_downloads += 1
        else:
            failed_downloads += 1
        print("-" * 40)

    print("\n--- Статистика скачивания ---")
    print(f"Успешно скачано: {successful_downloads}")
    print(f"Не удалось скачать: {failed_downloads}")
    
    if failed_downloads == 0 and successful_downloads > 0 and successful_downloads == len(urls_to_process): 
        clear_choice = input("Все видео из списка обработаны. Очистить список URL? (y/n): ").lower()
        if clear_choice == 'y':
            urls_to_download.clear()
            print("Список URL очищен.")


def change_download_folder_ui():
    global current_download_folder
    print("\n--- Изменение папки для сохранения ---")
    print(f"Текущая папка: {current_download_folder}")
    new_folder_input = input("Введите новый путь к папке (оставьте пустым, чтобы не менять): ").strip()
    
    if new_folder_input:
        new_folder = new_folder_input.replace("\\", "/")
        invalid_chars_pattern = r'[:*?"<>|]' 
        if any(char in new_folder for char in ':*?"<>|'):
            path_parts = os.path.splitdrive(new_folder)
            if path_parts[1] and any(char in path_parts[1] for char in ':*?"<>|'):
                 print("Путь содержит недопустимые символы. Пожалуйста, используйте корректное имя папки.")
                 return

        current_download_folder = new_folder
        print(f"Папка для сохранения изменена на: {current_download_folder}")
        
        if not os.path.exists(current_download_folder):
            try:
                os.makedirs(current_download_folder)
                print(f"Папка '{current_download_folder}' успешно создана/проверена.")
            except OSError as e:
                print(f"Внимание: Не удалось создать папку '{current_download_folder}': {e}")
        else:
            print(f"Папка '{current_download_folder}' уже существует.")
    else:
        print("Папка не изменена.")


def clear_urls_ui():
    global urls_to_download
    if not urls_to_download:
        print("Список URL уже пуст.")
        return
    confirm = input(f"Вы уверены, что хотите очистить список из {len(urls_to_download)} URL? (y/n): ").lower()
    if confirm == 'y':
        urls_to_download.clear()
        print("Список URL очищен.")
    else:
        print("Очистка отменена.")

def set_cookies_file_ui():
    global cookies_file_path
    print("\n--- Указание файла Cookies ---")
    if cookies_file_path:
        print(f"Текущий файл cookies: {cookies_file_path}")
    else:
        print("Файл cookies не указан.")
    
    new_cookies_path_input = input("Введите полный путь к файлу cookies (например, vk_cookies.txt) или оставьте пустым, чтобы сбросить: ").strip()

    if not new_cookies_path_input:
        cookies_file_path = None
        print("Путь к файлу cookies сброшен.")
        return

    new_cookies_path = new_cookies_path_input.replace("\\", "/")

    if os.path.exists(new_cookies_path) and os.path.isfile(new_cookies_path):
        cookies_file_path = new_cookies_path
        print(f"Файл cookies установлен: {cookies_file_path}")
    else:
        print(f"Ошибка: Файл не найден по указанному пути '{new_cookies_path}' или это не файл.")
        print("Пожалуйста, убедитесь, что файл существует и путь указан верно.")

# --- Основной цикл программы ---
if __name__ == "__main__":
    try:
        "╔".encode(sys.stdout.encoding)
    except (UnicodeEncodeError, TypeError): 
        print("INFO: Ваша консоль может некорректно отображать некоторые символы из названий видео.")
        print("INFO: Для лучшего отображения символов в Windows попробуйте выполнить команду 'chcp 65001' в консоли перед запуском скрипта.")

    if not os.path.exists(current_download_folder):
        print(f"Папка по умолчанию '{current_download_folder}' не найдена.")
        try:
            os.makedirs(current_download_folder)
            print(f"Папка по умолчанию '{current_download_folder}' успешно создана.")
        except OSError as e:
            print(f"ОШИБКА: Не удалось создать папку по умолчанию '{current_download_folder}': {e}")

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        choice = display_main_menu()
        
        if choice == '1':
            add_url_ui()
        elif choice == '2':
            show_urls_ui()
        elif choice == '3':
            start_download_ui()
        elif choice == '4':
            change_download_folder_ui()
        elif choice == '5':
            clear_urls_ui()
        elif choice == '6':
            set_cookies_file_ui()
        elif choice == '0':
            print("Выход из программы. До свидания!")
            break
        else:
            print("Неверный выбор. Пожалуйста, введите число от 0 до 6.")
        
        if choice != '0': 
             input("\nНажмите Enter для продолжения...")