import random

class Plane:
    
    def __init__(self, role):
        self.life = 100
        self.role = role
        
    def avoiding_action(self):
        return random.random() < 0.5
    
    def on_destroyed(self, attacker_role):
        print(f"{self.role} has been destroyed by {attacker_role}.")
    
    def take_damage(self, amount, attacker_role):
        if self.avoiding_action():
            print(f"{self.role} dodged the attack from {attacker_role}.")
        else:
            self.life -= amount
            if self.life <= 0:
                self.on_destroyed(attacker_role)
            else:
                print(f"{self.role} took {amount} damage from {attacker_role} and now has {self.life} life.")

class Jet(Plane):
    
    def __init__(self, role, min_damage=5, max_damage=30):
        super().__init__(role)
        self.infl_damage = random.randint(min_damage, max_damage)
        self.ammo = 15

    def attack(self, target):
        if self.ammo > 0:
            self.ammo -= 1
            print(f"{self.role} is attacking {target.role}.")
            target.take_damage(self.infl_damage, self.role)
            if target.life <= 0:
                return True
            print(f"Remaining ammo for {self.role}: {self.ammo}")
        else:
            print(f"{self.role} is out of ammo.")
        return False

class Airbus(Plane):
    
    def __init__(self, role, passenger_count=150):
        super().__init__(role)
        self.passenger_count = passenger_count
        self.passengers_killed = 0
        self.has_dodged = False

    def avoiding_action(self):
        if self.life < 31 and not self.has_dodged:
            self.has_dodged = True
            return super().avoiding_action()
        return False

    def on_destroyed(self, attacker_role):
        super().on_destroyed(attacker_role)
        self.passengers_killed = random.randint(2, self.passenger_count)     
        print(f"{self.passengers_killed} passengers died out of {self.passenger_count}.")

attacker = Jet("Attacker Jet", min_damage=5, max_damage=20)
defender = Jet("Defender Jet", min_damage=5, max_damage=30)
airbus = Airbus("Airbus")

while airbus.life > 0 and attacker.life > 0:
    if attacker.ammo > 0:
        if attacker.attack(airbus):
            break
        print("====================================")
    else:
        print(f"{attacker.role} is out of ammo.")
        break
    if defender.ammo > 0:
        defender.attack(attacker)
        print("====================================")
    else:
        print(f"{defender.role} is out of ammo.")
        if attacker.ammo <= 0:
            print("Both jets are out of ammo, nobody won.")
            break
    if attacker.life <= 0:
        print("Attacker Jet has died. The Defender Jet has protected the Airbus successfully.")
        break
    if defender.ammo <= 0 and attacker.ammo <= 0:
        print("Both jets are out of ammo, nobody won.")
        break