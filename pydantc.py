from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator, model_validator , computed_field
from typing import Dict, Annotated

class Patient(BaseModel):
    name: Annotated[str, Field(max_length=50)]
    email: EmailStr
    linkedin_url: AnyUrl
    age: int = Field(gt=0, lt=120)
    weight: Annotated[float, Field(gt=0, strict=True)]
    height : float
    married: Annotated[bool, Field(default=None)]
    contact_details: Dict[str, str]

    #field_validator

    @field_validator("email")
    @classmethod
    def email_validator(cls, value):
        valid_domains = ['edu.np', 'bank.np']
        if value.split("@")[-1] not in valid_domains:
            raise ValueError("Not in domain.")
        return value
    
    #model validator

    @model_validator(mode='after')
    def validate_emergency_contact(self):
        if self.age > 60 and 'emergency' not in self.contact_details:
            raise ValueError('Patients older than 60 must have an emergency contact')
        return self
    
    # computed field
    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight/(self.height**2),2)
        return bmi


def update_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.email)
    print(patient.married)
    print(patient.weight)
    print(patient.bmi)
    print('updated')


patient_info = {
    'name': 'amir',
    'email': 'abc@edu.np',
    'linkedin_url': 'http://linkedin.com/1322',
    'age': 22,
    'weight': 75.2,
    'height' : 1.7,
    'contact_details': {'phone': '9818585524'}
}

patient1 = Patient(**patient_info)
update_patient_data(patient1)