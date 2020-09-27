from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type

class OrderTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, order, timestamp):
        user_id = text_type(order.id)
        ts = text_type(timestamp)
        is_active = order.complete
        return f"{user_id}{ts}{is_active}"

order_tokenizer = OrderTokenGenerator()