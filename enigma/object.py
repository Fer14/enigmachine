from abc import ABC, abstractmethod
import random

LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

class MachineObject(ABC):
    @abstractmethod
    def encrypt(self, letter: str) -> str:
        pass


class Rotor(MachineObject):
    """Class representing a rotor in an Enigma machine.
    A rotor is characterized by its position
    """

    def __init__(self, position: int, letter_ordering: list = None):
        """_summary_

        Parameters
        ----------
        position : int
            The initial position of the rotor. Must be between 1 and 26
        letter_ordering : list, optional
            The ordering of the letters in the rotor, by default None

        Raises
        ------
        AssertionError
            If the position is not within the valid range.
        """
        assert 1 <= position <= 26, "Rotor position must be between 1 and 26"
        self.rotor_position = position
        if letter_ordering is not None:
            assert all(
                [len(letter_ordering) == 26, set(letter_ordering) == set(LETTERS)]
            ), "Letter ordering must contain exactly 26 letters"
        else:
            shuffled_letters = list(LETTERS)
            random.shuffle(shuffled_letters)
            self.letters = shuffled_letters

    def __str__(self):
        return f"Rotor instance with position: {self.rotor_position}"

    def change_position(self, position: int):
        """Change the position of the rotor.

        Parameters
        ----------
        position : int
            The new position of the rotor.

        Raises
        ------
        AssertionError
            If the position is not within the valid range.
        """
        assert 1 <= position <= 26, "Rotor position must be between 1 and 26"
        self.rotor_position = position

    def click_rotor(self):
        """Rotate the rotor by one position."""
        self.rotor_position = (self.rotor_position + 1) % 26

    def encrypt(self, letter: str) -> str:
        """Encrypt a letter using the current rotor position.

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
        assert letter in self.letters, "Letter must be a capital english letter"
        letter_index = self.letters.index(letter)
        encrypted_letter_index = (letter_index + self.rotor_position) % 26
        return self.letters[encrypted_letter_index]
    



class RotorMechanism(MachineObject):
    """
    Class representing a rotor mechanism in an Enigma machine.
    """

    def __init__(self, rotors: list, inversed: bool = False) -> None:
        """
        Initialize an Enigma machine.

        Parameters
        ----------
        rotors : list
            A list containing instances of the Rotor class.
        inversed : bool, optional
            Indicates whether the machine is operating in inverse mode.
            Defaults to False.

        Raises
        ------
        AssertionError
            If any element in rotors is not an instance of the Rotor class.
        """

        assert all(isinstance(rotor, Rotor) for rotor in rotors)
        self.rotors = rotors
        self.clicks = 0
        self.inverse = inversed

    def click(self):
        """Advance the rotors of the Enigma machine by one position."""
        self.clicks += 1
        for i in range(len(self.rotors)):
            if self.clicks % (26**i) == 0:
                self.rotors[i].click_rotor()

    def __str__(self):
        s = "RotorMechanism instance with rotors:"
        for rotor in self.rotors:
            s += f"\n{rotor}"
        return s
    
    def encrypt(self, letter: str) -> str:
        """Encrypt a letter using the Enigma machine.

        Parameters
        ----------
        letter : str
            The letter to encrypt.

        Returns
        -------
        str
            The encrypted letter.
        """
        if self.inverse:
            return self.encrypt_inverse(letter)
        else:
            return self.encrypt_forward(letter)

    def encrypt_forward(self, letter: str) -> str:
        """Encrypt a letter in the forward direction using the Enigma machine.

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
            If any element in rotors is not an instance of the Rotor class.
        """
        assert letter in LETTERS, "Letter must be a capital english letter"
        for rotor in self.rotors:
            letter = rotor.encrypt(letter)
        return letter

    def encrypt_inverse(self, letter: str) -> str:
        """Encrypt a letter in the inverse direction using the Enigma machine.

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
            If any element in rotors is not an instance of the Rotor class.
        """
        assert letter in LETTERS, "Letter must be a capital english letter"
        for rotor in reversed(self.rotors):
            letter = rotor.encrypt(letter)
        self.click()
        return letter


class PlugBoard(MachineObject):
    """Class representing a plugboard in an Enigma machine."""

    def __init__(self, connections: dict = None):
        """Initialize the plugboard with given connections.

        Parameters
        ----------
        connections : dict, optional
            A dictionary representing connections in the plugboard., by default None

        Raises
        ------
        AssertionError
            If connections is not a dictionary or if it doesn't meet
            the requirements for a valid connections dictionary.
        """
        if connections is not None:
            assert isinstance(connections, dict), "Connections must be a dictionary"
            assert all(
                [key in LETTERS for key in connections.keys()]
            ), "Connections must be a dictionary containing english letters"
            self.connections = connections
        else:
            self.connections = {}

    def __str__(self):
        return f"PlugBoard instance with connections: {self.connections}"

    def encrypt(self, letter: str) -> str:
        """Encrypt a letter using the plugboard.

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
        assert letter in LETTERS, "Letter must be a capital english letter"
        return self.connections.get(letter, letter)


class Reflector(MachineObject):
    """Class representing a reflector in an Enigma machine."""

    def __init__(self, connections: dict = None):
        """Initialize the reflector.

        Parameters
        ----------
        connections : dict, optional
            A dictionary representing connections in the reflector, by default None

        Raises
        ------
        AssertionError
            If connections is not a dictionary or if it doesn't meet
            the requirements for a valid connections dictionary.
        """
        if connections is not None:
            assert isinstance(connections, dict), "Connections must be a dictionary"
            assert all(
                [
                    len(connections) == 26,
                    set(connections.keys()) == set(LETTERS),
                    set(connections.values()) == set(LETTERS),
                ]
            ), "Connections must be a dictionary with 26 keys and values"
            self.connections = connections
        else:
            shuffled_letters = list(LETTERS)
            random.shuffle(shuffled_letters)
            self.connections = {i: o for i, o in zip(LETTERS, shuffled_letters)}

    def __str__(self):
        return f"Reflector instance with connections: {self.connections}"

    def encrypt(self, letter: str) -> str:
        """Encrypt a letter using the reflector.

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
        assert letter in LETTERS, "Letter must be a capital english letter"
        return self.connections[letter]
