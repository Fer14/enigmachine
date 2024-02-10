from dataclasses import dataclass


class RotorConfig:
    wiring: str
    name: str

    def __init__(self, wiring: str, name: str):
        self.wiring = wiring
        self.name = name


ROTOR_CONFIGURATIONS = {
    "Commercial Enigma A, B": [
        RotorConfig(wiring="DMTWSILRUYQNKFEJCAZBPGXOHV", name="IC"),
        RotorConfig(wiring="HQZGPJTMOBLNCIFDYAWVEUSRKX", name="IIC"),
        RotorConfig(wiring="UQNTLSZFMREHDPXKIBVYGJCWOA", name="IIIC"),
    ],
    "German Railway (Rocket)": [
        RotorConfig(wiring="JGDQOXUSCAMIFRVTPNEWKBLZYH", name="I"),
        RotorConfig(wiring="NTZPSFBOKMWRCJDIVLAEYUXHGQ", name="II"),
        RotorConfig(wiring="JVIUBHTCDYAKEQZPOSGXNRMWFL", name="III"),
        RotorConfig(wiring="QYHOGNECVPUZTFDJAXWMKISRBL", name="UKW"),
        RotorConfig(wiring="QWERTZUIOASDFGHJKPYXCVBNML", name="ETW"),
    ],
    "Swiss K": [
        RotorConfig(wiring="PEZUOHXSCVFMTBGLRINQJWAYDK", name="I-K"),
        RotorConfig(wiring="ZOUESYDKFWPCIQXHMVBLGNJRAT", name="II-K"),
        RotorConfig(wiring="EHRVXGAOBQUSIMZFLYNWKTPDJC", name="III-K"),
        RotorConfig(wiring="IMETCGFRAYSQBZXWLHKDVUPOJN", name="UKW-K"),
        RotorConfig(wiring="QWERTZUIOASDFGHJKPYXCVBNML", name="ETW-K"),
    ],
    "Enigma I": [
        RotorConfig(wiring="EKMFLGDQVZNTOWYHXUSPAIBRCJ", name="I"),
        RotorConfig(wiring="AJDKSIRUXBLHWTMCQGZNPYFVOE", name="II"),
        RotorConfig(wiring="BDFHJLCPRTXVZNYEIWGAKMUSQO", name="III"),
    ],
    "M3 Army": [
        RotorConfig(wiring="ESOVPZJAYQUIRHXLNFTGKDCMWB", name="IV"),
        RotorConfig(wiring="VZBRGITYUPSDNHLXAWMJQOFECK", name="V"),
    ],
    "M3 & M4 Naval (FEB 1942)": [
        RotorConfig(wiring="JPGVOUMFYQBENHZRDKASXLICTW", name="VI"),
        RotorConfig(wiring="NZJHGRCXMYSWBOUFAIVLPEKQDT", name="VII"),
        RotorConfig(wiring="FKQHTLXOCBJSPDZRAMEWNIUYGV", name="VIII"),
    ],
    "M4 R2": [
        RotorConfig(wiring="LEYJVCNIXWPBQMDRTAKZGFUHOS", name="Beta"),
        RotorConfig(wiring="FSOKANUERHMBTIYCWLQPZXVGJD", name="Gamma"),
    ],
}


@dataclass
class ReflectorConfig:
    wiring: str
    name: str


REFLECTOR_CONFIGURATIONS = {
    "A": ReflectorConfig(wiring="EJMZALYXVBWFCRQUONTSPIKHGD", name="A"),
    "B": ReflectorConfig(wiring="YRUHQSLDPXNGOKMIEBFZCWVJAT", name="B"),
    "C": ReflectorConfig(wiring="FVPJIAOYEDRZXWGCTKUQSBNMHL", name="C"),
    "B Thin": ReflectorConfig(wiring="ENKQAUYWJICOPBLMDXZVFTHRGS", name="B Thin"),
    "C Thin": ReflectorConfig(wiring="RDOBJNTKVEHMLFCWZAXGYIPSUQ", name="C thin"),
}
