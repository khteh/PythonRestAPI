from datetime import datetime, date
from typing import Dict, Any, List, Literal, Optional
from pydantic import BaseModel, Field, computed_field
"""
https://ai.google.dev/gemini-api/docs/structured-output
"""
class ReceiptItem(BaseModel):
    """Receipt item."""
    name: str = Field(
        default=None,
        description="The name of the goods or service item spent on the receipt.",
    )
    amount: float = Field(
        default=None,
        description="The amount of the item spent on the receipt.",
    )

class ReceiptModel(BaseModel):
    """Receipt bill."""
    date_str: str | None = Field(
        default=None,
        exclude=True,
        repr=False,
        description="The date of the receipt reformatted to match dd-mm-YYYY. This is usually found in the Date field in the receipt. Ignore the timestamp and timezone part of the Date",
    )
    vendor: str = Field(
        default=None,
        description="The vendor or merchant which issued the receipt",
    )
    currency: str = Field(
        default=None,
        description="3-character currency code used in the amount of items, tax_amount and total of the receipt",
    )
    items: list[ReceiptItem] = Field(
        default=None,
        description="List of items spent in the receipt. Every item should have the name and amount spent for the item."
    )
    tax: float = Field(
        default=None,
        description="The GST/Tax amount payable on the total of all the items' amount.",
    )
    total: float = Field(
        default=None,
        description="The total amount spend on the receipt which includes the total of the items' amount and the tax",
    )
    @staticmethod
    def _convert_string_to_date(date_str: str | None) -> date | None:
        """
        locale.getlocale()
        local.setlocale(local.LC_ALL, 'en_US')
        https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes
        Date: Wed, 02 Apr 2025 15:39:59 -0700
        """
        try:
            #return datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %z') if date_str else None
            return datetime.strptime(date_str, "%d-%m-%Y").date() if date_str else None
        except Exception as e:
            print(e)
            return None

    @computed_field
    @property
    def date_of_receipt(self) -> date | None:
        return self._convert_string_to_date(self.date_str) if self.date_str else None
