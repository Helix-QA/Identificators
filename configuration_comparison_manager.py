import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import table
import shutil
import os
from datetime import datetime
import logging

# Определение базового каталога, где находятся все файлы
base_dir = "D:\\Identificators\\log"

# Пути к файлам и папкам относительно базового каталога
file_path = os.path.join(base_dir, 'ConfigurationComparison.xlsx')
output_path = os.path.join(base_dir, 'ConfigurationComparison.png')
history_folder = os.path.join(base_dir, 'ИсторияСверок')

# Создание PNG
try:
    df = pd.read_excel(file_path)
except FileNotFoundError:
    logging.error(f"File not found: {file_path}")
    raise
except Exception as e:
    logging.error(f"Error reading Excel file: {e}")
    raise

try:
    fig, ax = plt.subplots(figsize=(20, 10))  # Размер изображения
    ax.xaxis.set_visible(False)  # Убираем ось X
    ax.yaxis.set_visible(False)  # Убираем ось Y
    ax.set_frame_on(False)  # Убираем рамку
    tabla = table(ax, df, loc='center', cellLoc='center', colWidths=[0.2]*len(df.columns))

    tabla.auto_set_font_size(False)  # Устанавливаем размер шрифта вручную
    tabla.set_fontsize(10)
    tabla.scale(1.2, 1.2)  # Масштабируем таблицу

    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.close()  # Закрываем фигуру после сохранения
    logging.info(f"Saved PNG file to: {output_path}")
except Exception as e:
    logging.error(f"Error creating PNG file: {e}")
    raise

# Перемещение и переименование оригинального файла
if not os.path.exists(history_folder):
    os.makedirs(history_folder)  # Создание папки, если она не существует

# Генерация нового имени файла с текущей датой и временем
current_date = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
history_file_name = f'ConfigurationComparison_{current_date}.xlsx'
history_file_path = os.path.join(history_folder, history_file_name)

try:
    shutil.move(file_path, history_file_path)  # Перемещение и переименование
    logging.info(f"File moved and renamed to: {history_file_path}")
except Exception as e:
    logging.error(f"Error moving and renaming file: {e}")
    raise

# Удаление оригинала после успешного перемещения
if os.path.exists(file_path):
    os.remove(file_path)
    logging.info(f"Original file {file_path} deleted.")
else:
    logging.warning(f"Original file {file_path} not found for deletion.")