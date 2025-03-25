# app/models/user.py
from sqlalchemy import Column, Integer, String, Date
from app.core.database import Base
import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    api_key = Column(String, unique=True, index=True)
    monthly_limit = Column(Integer, default=50)
    monthly_usage = Column(Integer, default=0)  # usage for the current month
    usage_reset_date = Column(Date, default=None)  # when usage was last reset

    def reset_monthly_usage_if_needed(self):
        """Resets usage if we're in a new month."""
        today = datetime.date.today()
        # if usage_reset_date is None or if usage_reset_date.month != today.month
        if not self.usage_reset_date or (self.usage_reset_date.year != today.year or self.usage_reset_date.month != today.month):
            self.monthly_usage = 0
            self.usage_reset_date = today
