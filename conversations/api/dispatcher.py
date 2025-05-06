from .handlers import new_conversation, new_message, close_conversation

EVENT_HANDLERS = {
  "NEW_CONVERSATION":   new_conversation.handle,
  "NEW_MESSAGE":        new_message.handle,
  "CLOSE_CONVERSATION": close_conversation.handle,
}

def dispatch_event(event_type, data):
  handler = EVENT_HANDLERS.get(event_type)

  if not handler:
    raise ValueError(f"Unhandled event_type: {event_type}")

  return handler(data)