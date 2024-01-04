
from pydantic import BaseModel
from datetime import datetime, date


class TimeStamp(BaseModel):
  dt: date = date.today()

  def __str__(self):
    return self.str
  
  @property
  def stamp(self):
    return self.str

  @property
  def str(self):
    return self.dt.strftime("%Y-%m-%d")
  
  @property
  def month(self) -> int:
    return self.dt.month

  @property
  def year(self) -> int:
    return self.dt.year
  
  @property
  def month_offset(self) -> int:
    now = TimeStamp()
    return (self.dt.year - now.year) * 12 + (self.dt.month - now.month)

  @property
  def month_str(self) -> str:
    return self.dt.strftime("%b")
  
  @property
  def month_int(self) -> int:
    return self.dt.month


