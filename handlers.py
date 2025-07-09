import os
import logging
from telegram import Update
from telegram.ext import ContextTypes
from audio_utils import convert_ogg_to_wav, transcribe_with_google
from api_utils import ask_voice_api, forward_to_external_api
from config import TEMP_AUDIO_PATH

async def universal_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if update.message.voice:
            logging.info("Received voice message. Downloading...")
            file = await context.bot.get_file(update.message.voice.file_id)
            ogg_path = os.path.join(TEMP_AUDIO_PATH, f"{update.message.message_id}.ogg")
            await file.download_to_drive(ogg_path)

            wav_path = convert_ogg_to_wav(ogg_path)
            transcript = transcribe_with_google(wav_path)
            logging.info(f"Transcription: {transcript}")
            if transcript.startswith("❌"):
                await update.message.reply_text(f"Transcription failed: {transcript}")
                return

            answer = await ask_voice_api(transcript)
            await update.message.reply_text(f"🗣️ Transcription: {transcript}\n\n💬 Response:\n{answer}")

        elif update.message.text:
            logging.info("Received text message. Forwarding to webhook...")
            await forward_to_external_api(update)
        else:
            logging.warning("Unsupported message type ignored.")
    except Exception as e:
        logging.exception(f"Exception occurred during processing: {e}")
        await update.message.reply_text(f"❌ Error during processing: {str(e)}")

async def button_click_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await forward_to_external_api(update)
    await query.message.reply_text(f"❓ Button clicked: {query.data}")
    logging.info(f"Button clicked with data: {query.data}")
