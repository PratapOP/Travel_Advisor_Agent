"""
Service layer for the chat agent — bridges Django models and the AI engine.
"""
import logging

from ai_engine.agent import TravelAdvisorAgent

from .models import Conversation, Message

logger = logging.getLogger('ai_engine')


class ChatService:
    """Orchestrates chat interactions between the user and the AI agent."""

    @staticmethod
    def get_or_create_conversation(user, conversation_id=None):
        """Get an existing conversation or create a new one."""
        if conversation_id:
            try:
                return Conversation.objects.get(id=conversation_id, user=user, is_active=True)
            except Conversation.DoesNotExist:
                pass

        return Conversation.objects.create(user=user)

    @staticmethod
    def get_user_preferences(user) -> dict:
        """Extract user preferences for AI context."""
        try:
            prefs = user.travel_preferences
            return {
                'budget_tier': prefs.preferred_budget_tier,
                'interests': ', '.join(prefs.interests) if prefs.interests else '',
                'dietary_restrictions': ', '.join(prefs.dietary_restrictions) if prefs.dietary_restrictions else '',
                'mobility_needs': prefs.mobility_needs,
                'accommodation': prefs.preferred_accommodation,
                'travel_style': prefs.travel_style,
                'climate': prefs.preferred_climate,
                'languages': ', '.join(prefs.languages_spoken) if prefs.languages_spoken else '',
            }
        except Exception:
            return {}

    @staticmethod
    def process_message(user, message_text: str, conversation_id=None) -> dict:
        """
        Process a user message and return the AI response.

        Returns:
            dict with conversation_id, user_message, assistant_message
        """
        # Get or create conversation
        conversation = ChatService.get_or_create_conversation(user, conversation_id)

        # Save user message
        user_msg = Message.objects.create(
            conversation=conversation,
            role='user',
            content=message_text,
        )

        # Auto-generate title from first message
        if conversation.messages.count() == 1:
            title = message_text[:80]
            if len(message_text) > 80:
                title += '...'
            conversation.title = title
            conversation.save(update_fields=['title'])

        # Get conversation history (exclude the message we just added)
        history = conversation.get_message_history(limit=20)
        # Remove the last entry since it's the current message
        if history and history[-1]['content'] == message_text:
            history = history[:-1]

        # Get user preferences for AI context
        preferences = ChatService.get_user_preferences(user)

        # Invoke the AI agent
        logger.info(f"Processing message for conversation {conversation.id}")
        agent = TravelAdvisorAgent(user_preferences=preferences)
        response_text = agent.chat(
            user_message=message_text,
            conversation_history=history,
        )

        # Save assistant response
        assistant_msg = Message.objects.create(
            conversation=conversation,
            role='assistant',
            content=response_text,
        )

        # Update conversation timestamp
        conversation.save(update_fields=['updated_at'])

        return {
            'conversation_id': conversation.id,
            'conversation_title': conversation.title,
            'user_message': {
                'id': user_msg.id,
                'content': user_msg.content,
                'created_at': user_msg.created_at,
            },
            'assistant_message': {
                'id': assistant_msg.id,
                'content': assistant_msg.content,
                'created_at': assistant_msg.created_at,
            },
        }
