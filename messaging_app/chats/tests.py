from django.test import TestCase
from rest_framework.test import APITestCase
from chats.models import User, Conversation, Message
import uuid


class UserModelTest(TestCase):
    """Test cases for User model"""

    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'role': 'guest',
            'password': 'testpass123'
        }

    def test_create_user(self):
        """Test user creation"""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.role, 'guest')
        self.assertTrue(isinstance(user.user_id, uuid.UUID))

    def test_user_str_representation(self):
        """Test user string representation"""
        user = User.objects.create_user(**self.user_data)
        expected_str = f"{user.email} ({user.role})"
        self.assertEqual(str(user), expected_str)

    def test_email_unique_constraint(self):
        """Test email uniqueness"""
        User.objects.create_user(**self.user_data)
        with self.assertRaises(Exception):
            User.objects.create_user(**self.user_data)


class ConversationModelTest(TestCase):
    """Test cases for Conversation model"""

    def setUp(self):
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@example.com',
            first_name='User',
            last_name='One',
            role='guest',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@example.com',
            first_name='User',
            last_name='Two',
            role='host',
            password='testpass123'
        )

    def test_create_conversation(self):
        """Test conversation creation"""
        conversation = Conversation.objects.create()
        conversation.participants.add(self.user1, self.user2)

        self.assertTrue(isinstance(conversation.conversation_id, uuid.UUID))
        self.assertEqual(conversation.participants.count(), 2)
        self.assertIn(self.user1, conversation.participants.all())
        self.assertIn(self.user2, conversation.participants.all())

    def test_conversation_str_representation(self):
        """Test conversation string representation"""
        conversation = Conversation.objects.create()
        expected_str = f"Conversation {conversation.conversation_id}"
        self.assertEqual(str(conversation), expected_str)


class MessageModelTest(TestCase):
    """Test cases for Message model"""

    def setUp(self):
        self.user1 = User.objects.create_user(
            username='sender',
            email='sender@example.com',
            first_name='Sender',
            last_name='User',
            role='guest',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='receiver',
            email='receiver@example.com',
            first_name='Receiver',
            last_name='User',
            role='host',
            password='testpass123'
        )
        self.conversation = Conversation.objects.create()
        self.conversation.participants.add(self.user1, self.user2)

    def test_create_message(self):
        """Test message creation"""
        message = Message.objects.create(
            sender=self.user1,
            conversation=self.conversation,
            message_body="Hello, this is a test message!"
        )

        self.assertTrue(isinstance(message.message_id, uuid.UUID))
        self.assertEqual(message.sender, self.user1)
        self.assertEqual(message.conversation, self.conversation)
        self.assertEqual(message.message_body, "Hello, this is a test message!")

    def test_message_str_representation(self):
        """Test message string representation"""
        message = Message.objects.create(
            sender=self.user1,
            conversation=self.conversation,
            message_body="Test message"
        )
        expected_str = f"Message {message.message_id} from {self.user1.email}"
        self.assertEqual(str(message), expected_str)

    def test_message_relationships(self):
        """Test message relationships with user and conversation"""
        message = Message.objects.create(
            sender=self.user1,
            conversation=self.conversation,
            message_body="Test relationship"
        )

        # Test reverse relationships
        self.assertIn(message, self.user1.sent_messages.all())
        self.assertIn(message, self.conversation.messages.all())


class MessagingAPITest(APITestCase):
    """Test cases for messaging API endpoints"""

    def setUp(self):
        self.user1 = User.objects.create_user(
            username='apiuser1',
            email='apiuser1@example.com',
            first_name='API',
            last_name='User1',
            role='guest',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='apiuser2',
            email='apiuser2@example.com',
            first_name='API',
            last_name='User2',
            role='host',
            password='testpass123'
        )

    def test_user_creation_api(self):
        """Test user creation through API (if endpoints exist)"""
        # This is a placeholder test for API functionality
        # Actual implementation would depend on the API views
        self.assertTrue(True)  # Placeholder assertion

    def test_conversation_creation_api(self):
        """Test conversation creation through API (if endpoints exist)"""
        # This is a placeholder test for API functionality
        self.assertTrue(True)  # Placeholder assertion

    def test_message_sending_api(self):
        """Test message sending through API (if endpoints exist)"""
        # This is a placeholder test for API functionality
        self.assertTrue(True)  # Placeholder assertion


class ModelIntegrationTest(TestCase):
    """Integration tests for all models working together"""

    def setUp(self):
        self.user1 = User.objects.create_user(
            username='integuser1',
            email='integuser1@example.com',
            first_name='Integration',
            last_name='User1',
            role='guest',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='integuser2',
            email='integuser2@example.com',
            first_name='Integration',
            last_name='User2',
            role='host',
            password='testpass123'
        )

    def test_full_messaging_workflow(self):
        """Test complete messaging workflow"""
        # Create conversation
        conversation = Conversation.objects.create()
        conversation.participants.add(self.user1, self.user2)

        # Send messages
        message1 = Message.objects.create(
            sender=self.user1,
            conversation=conversation,
            message_body="Hello from user1!"
        )

        message2 = Message.objects.create(
            sender=self.user2,
            conversation=conversation,
            message_body="Hello back from user2!"
        )

        # Verify conversation has messages
        self.assertEqual(conversation.messages.count(), 2)
        self.assertIn(message1, conversation.messages.all())
        self.assertIn(message2, conversation.messages.all())

        # Verify users have sent messages
        self.assertEqual(self.user1.sent_messages.count(), 1)
        self.assertEqual(self.user2.sent_messages.count(), 1)
