import edge_tts
import asyncio
import logging

VOICE_OPTIONS = {
    "ru": {
        "male": "Microsoft Server Speech Text to Speech Voice (ru-RU, DmitryNeural)",
        "female": "Microsoft Server Speech Text to Speech Voice (ru-RU, SvetlanaNeural)"
    },
    "en": {
        "male": "Microsoft Server Speech Text to Speech Voice (en-US, GuyNeural)",
        "female": "Microsoft Server Speech Text to Speech Voice (en-US, JennyNeural)"
    }
}

OUTPUT_FORMATS = {
    "1": "audio-16khz-32kbitrate-mono-mp3",
    "2": "audio-24khz-48kbitrate-mono-mp3",
    "3": "riff-16khz-16bit-mono-pcm",
    "4": "riff-24khz-16bit-mono-pcm"
}

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

async def synthesize_speech(text, voice, rate, output_file):
    kwargs = {"voice": voice, "rate": rate}

    logger.info(f"Синтез речи: voice={voice}, rate={rate}, output_file={output_file}")

    communicate = edge_tts.Communicate(text=text, **kwargs)

    try:
        await communicate.save(output_file)
        logger.info(f"Речь успешно сохранена в файл {output_file}")
    except Exception as e:
        logger.error(f"Ошибка синтеза речи: {e}")

def get_number_input(prompt, default, min_value, max_value, suffix=""):
    user_input = input(prompt).strip()
    if not user_input:
        return f"{default:+d}{suffix}" if suffix else f"{default:+d}"
    try:
        value = int(user_input)
        if min_value <= value <= max_value:
            return f"{value:+d}{suffix}" if suffix else f"{value:+d}"
        else:
            raise ValueError
    except ValueError:
        print(f"Некорректное значение. Установлено значение по умолчанию ({default}).")
        return f"{default:+d}{suffix}" if suffix else f"{default:+d}"

def get_user_input():
    print("Добро пожаловать в синтезатор речи Edge-TTS!")

    language = input("Введите код языка для голоса (например, ru, en): ").strip().lower()
    if language not in VOICE_OPTIONS:
        print(f"Извините, для языка '{language}' голоса недоступны.")
        return None, None, None, None, None

    print("Выберите тип голоса:")
    print("[1] Мужской")
    print("[2] Женский")
    voice_type = input("Введите ваш выбор (1 или 2): ").strip()
    voice = VOICE_OPTIONS[language].get("male" if voice_type == "1" else "female")

    text = input("Введите текст для синтеза: ").strip()
    rate = get_number_input("Введите скорость речи (-100 до 100): ", 0, -100, 100, "%")

    print("Выберите формат вывода:")
    print("\n".join([f"[{key}] {value}" for key, value in OUTPUT_FORMATS.items()]))
    format_choice = input("Введите ваш выбор (1-4): ").strip()
    output_format = OUTPUT_FORMATS.get(format_choice, "audio-16khz-32kbitrate-mono-mp3")

    output_file = input("Введите имя выходного файла (по умолчанию output.mp3): ").strip() or "output.mp3"
    if not output_file.endswith(".mp3"):
        output_file += ".mp3"

    return text, voice, rate, output_file

async def main():
    user_input = get_user_input()
    if not user_input:
        return

    text, voice, rate, output_file = user_input
    await synthesize_speech(text, voice, rate, output_file)

if __name__ == "__main__":
    asyncio.run(main())
