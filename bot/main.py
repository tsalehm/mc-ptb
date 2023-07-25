if "start":
   import logging
   from telegram import ForceReply, Update,Chat, KeyboardButton, InlineKeyboardButton , ReplyKeyboardMarkup, Bot,InputMediaDocument, InlineKeyboardMarkup, MessageEntity,User, CallbackQuery
   from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, ExtBot, ConversationHandler, CallbackQueryHandler,JobQueue
   from telegram import __version__ as TG_VER
   from telegram.constants import ParseMode
   from os import popen
   from re import sub,findall,match
   import mytoken


   try:
      from telegram import __version_info__
   except ImportError:
      __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

   if __version_info__ < (20, 0, 0, "alpha", 1):
      raise RuntimeError(
         f"This example is not compatible with your current PTB version {TG_VER}. To view the "
         f"{TG_VER} version of this example, "
         f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
      )

   # logging.basicConfig(
   #    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
   # )
   # logger = logging.getLogger(__name__)

#|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||

gbapp = Application.builder().token(mytoken.token).proxy_url("socks5://127.0.0.1:33256").get_updates_proxy_url("socks5://127.0.0.1:33256").build()
gp=-1001702007504

turnon=InlineKeyboardMarkup([[InlineKeyboardButton("روشن کردن سرور",callback_data=2)]])

async def start (update:Update,context:ContextTypes.DEFAULT_TYPE):
   
   global cmes
   
   if update.effective_chat.type != "supergroup":
      return
   
   with open("/root/mc/logs/latest.log","r") as f:
      logs=f.read()
      
   if len(findall("mcscr",popen("screen -ls").read())) ==0:
      cmes=await gbapp.bot.send_message(gp,"سرور در حال حاضر خاموش است\nاخرین ساعتی که سرور روشن بوده : "+findall("\[(.*?)\] \[Server thread/INFO\]",logs)[-1],reply_markup=turnon) 
   elif len(findall("\[Server thread/INFO\]: Stopping the server",logs))>0: 
      cmes=await gbapp.bot.send_message(gp,"سرور در حال خاموش شدن است")
   elif len(findall("\[Server thread/INFO\]: Done \(",logs))==0: 
      cmes=await gbapp.bot.send_message(gp,"سرور در حال روشن شدن است، صبر کن"+mytoken.ipv)
   else : 
      cmes=await gbapp.bot.send_message(gp,"سرور روشنه، بپر توش"+mytoken.ipv)
      
   await gbapp.bot.pin_chat_message(gp,cmes.id)
   
   await gbapp.bot.delete_message(gp,cmes.id+1)


async def startserver(update:Update,context:ContextTypes.DEFAULT_TYPE):
   
   global cmes
   
   await update.callback_query.answer()
   popen("screen -S mcscr -dm bash -c \"cd /root/mc; java -Xmx2G -jar /root/mc/spigot-1.20.1.jar\"")
   await gbapp.bot.delete_message(gp,cmes.id)
   
   cmes=await gbapp.bot.send_message(gp,"سرور در حال روشن شدن است، صبر کن"+mytoken.ipv)
   await gbapp.bot.pin_chat_message(gp,cmes.id)
   
   await gbapp.bot.delete_message(gp,cmes.id+1)

   
async def queue (context:ContextTypes.DEFAULT_TYPE):
   
   global cmes   
   
   with open("/root/mc/logs/latest.log","r") as f:
      logs=f.read()
            
   if len(findall("mcscr",popen("screen -ls").read())) ==0:
      await gbapp.bot.edit_message_text("سرور در حال حاضر خاموش است\nاخرین ساعتی که سرور روشن بوده : "+findall("\[(.*?)\] \[Server thread/INFO\]",logs)[-1],gp,cmes.id,reply_markup=turnon) 
   elif len(findall("\[Server thread/INFO\]: Stopping the server",logs))>0: 
      await gbapp.bot.edit_message_text("سرور در حال خاموش شدن است",gp,cmes.id)
   elif len(findall("\[Server thread/INFO\]: Done \(",logs))==0: 
      await gbapp.bot.edit_message_text("سرور در حال روشن شدن است، صبر کن"+mytoken.ipv,gp,cmes.id)
   else : 
      await gbapp.bot.edit_message_text("سرور روشنه، بپر توش\nپلیر های آنلاین :\n"+findall("There are \d of a max of \d players online:(.*)",logs)[-1]+mytoken.ipv,gp,cmes.id)


def main() -> None:
   

   gbapp.add_handlers([
   CommandHandler("mcstart", start),
   CallbackQueryHandler(callback=startserver,pattern=str(2))
   ])
   
   gbapp.job_queue.run_repeating(queue,15)

   gbapp.run_polling()


if __name__ == '__main__':
   main()
