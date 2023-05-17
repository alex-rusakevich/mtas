from mtas.bot import bot

def get_reg_event_code(message):
    event_id = message.text

    bot.send_message(
            message.chat.id, f"Starting registration for {event_id}")
    bot.register_next_step_handler(message, begin_reg, event_id=event_id)

def begin_reg(message, event_id):
    bot.send_message(
            message.chat.id, f"Registration for {event_id}")