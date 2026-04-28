

class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    @classmethod
    def from_dict(cls, data):
        if "name" not in data:
            raise ValueError("name is required")  
          
        return cls(
        name=data["name"],
        age=data.get("age", 0)
        )
       
data = {"name": "Tom", "age": 20}

user = User.from_dict(data)

print(user.name)
print(user.age)
    
    