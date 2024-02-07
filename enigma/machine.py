import random
from .object import MachineObject,LETTERS,Rotor,RotorMechanism,PlugBoard,Reflector

class Machine:
    """Class representing an Enigma machine."""

    def __init__(self, config: list):
        """Initialize the Enigma machine with the given components.

        Parameters
        ----------
        config : list, optional
            List of components, by default []
        """
        assert all(
            [isinstance(component, MachineObject) for component in config]
        ), "Config must be a list of RotorMechanism, Reflector or PlugBoard instances"
        self.config = config

    def __str__(self):
        return f"Machine instance with rotor: {self.rotor}, reflector: {self.reflector} and plugboard: {self.plugboard}"

    def encrypt(self, letters: str) -> str:
        """Encrypt a letter using the configured Enigma machine.

        Parameters
        ----------
        letter : str
            The letter to encrypt.

        Returns
        -------
        str
            The encrypted letter.

        Raises
        ------
        AssertionError
            If the letter is not a capital English letter.
        """
        assert all(
            [l in LETTERS for l in letters]
        ), "Letter must be a capital english letter"
        encrypted_letters = ""
        for letter_ in letters:
            for component in self.config:
                letter_ = component.encrypt(letter_)
            encrypted_letters += letter_

        return encrypted_letters


class EnigmaMachine(Machine):
    """Class representing an Enigma machine, inheriting from Machine class."""

    def __init__(
        self,
        rotor_positions: list[int] = None,
        plugboard_connections: dict = None,
        reflector_connections: dict = None,
    ):
        """
        Initialize an Enigma machine.

        Parameters
        ----------
        rotor_positions : list[int], optional
            The initial positions of the rotors.
            Defaults to None.
        plugboard_connections : dict, optional
            The connections for the plugboard.
            Defaults to None.
        reflector_connections : dict, optional
            The connections for the reflector.
            Defaults to None.

        Raises
        ------
        AssertionError
            If rotor_positions list is provided and doesn't have 3 elements,
            or if any rotor position is not between 1 and 26.
        """
        if rotor_positions is not None:
            assert len(rotor_positions) == 3, "Enigma machine must have 3 rotors"
            assert all(
                [1 <= position <= 26 for position in rotor_positions]
            ), "Rotor position must be between 1 and 26"
        else:
            rotor_positions = [random.randint(1, 26) for _ in range(3)]
        # Create rotor mechanism with forward and inverse configurations
        rotors = [Rotor(position=position) for position in rotor_positions]

        rotor_mechanism = RotorMechanism(rotors=rotors)
        rotor_mechanism_inverted = RotorMechanism(
            rotors=rotors,
            inversed=True,
        )
        # Initialize Enigma machine using Machine superclass
        super().__init__(
            [
                PlugBoard(connections=plugboard_connections),
                rotor_mechanism,
                Reflector(connections=reflector_connections),
                rotor_mechanism_inverted,
                PlugBoard(connections=reflector_connections),
            ]
        )
