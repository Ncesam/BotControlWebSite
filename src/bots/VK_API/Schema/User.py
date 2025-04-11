from pydantic import BaseModel, computed_field


class User(BaseModel):
    firstName: str
    lastName: str
    userId: int

    @computed_field
    def full_name(self) -> str:
        return f"{self.firstName} {self.lastName}"
