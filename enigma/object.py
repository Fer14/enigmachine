from abc import ABC, abstractmethod

LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


class MachineObject(ABC):
    @abstractmethod
    def forward(self, letter: str) -> str:
        pass


class Rotor(MachineObject):
    """Class representing a rotor in an Enigma machine.
    A rotor is characterized by its position
    """

    def __init__(self, offset: int, wiring: str, name: str = None):
        """_summary_

        Parameters
        ----------
        offset : int
            The initial offset of the rotor. Must be between 0 and 25
        wiring : str
            The ordering of the letters in the rotor
        name: str, optional
            The name of the rotor, by default None

        Raises
        ------
        AssertionError
            If the position is not within the valid range.
        """
        self.name = name
        assert 0 <= offset <= 25, "Rotor position must be between 0 and 25"
        self.offset = offset
        assert all(
            [len(wiring) == 26, set(wiring) == set(LETTERS)]
        ), "Letter ordering must contain exactly 26 letters in wiring"
        self.wiring = wiring

    def __str__(self):
        return f"Rotor instance {self.name if self.name is not None else ''} with offset: {self.offset} and wiring: {self.wiring}"

    def change_position(self, offset: int):
        """Change the position of the rotor.

        Parameters
        ----------
        offset : int
            The new offset of the rotor.

        Raises
        ------
        AssertionError
            If the offset is not within the valid range.
        """
        assert 1 <= offset <= 26, "Rotor offset must be between 1 and 26"
        self.offset = offset

    def click_rotor(self):
        """Rotate the rotor by one position."""
        self.offset = (self.offset + 1) % 26

    def forward(self, letter: str, verbose: bool = False) -> str:
        """Encrypt a letter using the current rotor position.

        Parameters
        ----------
        letter : str
            The letter to encrypt.
        verbose : bool, optional
            If True, prints the encryption process.

        Returns
        -------
        str
            The encrypted letter.

        Raises
        ------
        AssertionError
            If the letter is not a capital English letter.
        """
        assert letter in self.wiring, "Letter must be a capital english letter"
        letter_index = LETTERS.index(letter)
        encrypted_letter_index = (letter_index + self.offset) % 26
        if verbose:
            print(
                f"Encrypting {letter} to {self.wiring[encrypted_letter_index]} with rotor {self.name if self.name is not None else ''} at offset {self.offset}"
            )
        return self.wiring[encrypted_letter_index]

    def inverse(self, letter: str, verbose: bool = False) -> str:
        """Encrypt a letter using the current rotor position.

        Parameters
        ----------
        letter : str
            The letter to encrypt.
        verbose : bool, optional
            If True, prints the encryption process.

        Returns
        -------
        str
            The encrypted letter.

        Raises
        ------
        AssertionError
            If the letter is not a capital English letter.
        """
        assert letter in self.wiring, "Letter must be a capital english letter"
        letter_index = self.wiring.index(letter)
        encrypted_letter_index = (letter_index - self.offset) % 26
        if verbose:
            print(
                f"Encrypting {letter} to {LETTERS[encrypted_letter_index]} with rotor {self.name} at offset {self.offset}"
            )
        return LETTERS[encrypted_letter_index]


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

    def forward(self, letter: str, verbose: bool = False) -> str:
        """Encrypt a letter using the Enigma machine.

        Parameters
        ----------
        letter : str
            The letter to encrypt.
        verbose : bool, optional
            If True, prints the encryption process.

        Returns
        -------
        str
            The encrypted letter.
        """
        if self.inverse:
            return self._inverse(letter, verbose)
        else:
            return self._forward(letter, verbose)

    def _forward(self, letter: str, verbose: bool = False) -> str:
        """Encrypt a letter in the forward direction using the Enigma machine.

        Parameters
        ----------
        letter : str
            The letter to encrypt.
        verbose : bool, optional
            If True, prints the encryption process.

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
        for rotor in self.rotors:
            letter = rotor.forward(letter, verbose)
        return letter

    def _inverse(self, letter: str, verbose: bool = False) -> str:
        """Encrypt a letter in the inverse direction using the Enigma machine.

        Parameters
        ----------
        letter : str
            The letter to encrypt.
        verbose : bool, optional
            If True, prints the encryption process.

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
        for rotor in reversed(self.rotors):
            letter = rotor.inverse(letter, verbose)
        self.click()
        return letter


class PlugBoard(MachineObject):
    """Class representing a plugboard in an Enigma machine."""

    def __init__(self, wiring: dict = None):
        """Initialize the plugboard with given wiring.

        Parameters
        ----------
        wiring : dict, optional
            A string representing wiring in the plugboard, by default None

        Raises
        ------
        AssertionError
            If wiring is not a dictionary or if it doesn't meet
            the requirements for a valid wiring dictionary.
        """
        if wiring is not None:
            assert isinstance(wiring, dict), "Wiring must be a dictionary"
            assert all(
                [key in LETTERS for key in wiring.keys()]
            ), "Wiring must be a dictionary containing english letters"
            self.wiring = wiring
        else:
            self.wiring = {}

    def __str__(self):
        return f"PlugBoard instance with wiring: {self.wiring}"

    def forward(self, letter: str, verbose: bool = False) -> str:
        """Encrypt a letter using the plugboard.

        Parameters
        ----------
        letter : str
            The letter to encrypt.
        verbose : bool, optional
            If True, prints the encryption process.

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
        if verbose:
            print(
                f"Encrypting {letter} to {self.wiring.get(letter, letter)} with plugboard"
            )
        return self.wiring.get(letter, letter)


class Reflector(MachineObject):
    """Class representing a reflector in an Enigma machine."""

    def __init__(self, wiring: str, name: str = None):
        """Initialize the reflector.

        Parameters
        ----------
        wiring : dict
            A dictionary representing wiring in the reflector, by default None

        Raises
        ------
        AssertionError
            If wiring is not a dictionary or if it doesn't meet
            the requirements for a valid wiring dictionary.
        """
        assert all(
            [len(wiring) == 26, set(wiring) == set(LETTERS)]
        ), "Letter ordering must contain exactly 26 letters"
        self.wiring = wiring
        self.name = name

    def __str__(self):
        return f"Reflector instance {self.name if self.name is not None else ''} with wiring: {self.wiring}"

    def forward(self, letter: str, verbose: bool = False) -> str:
        """Encrypt a letter using the reflector.

        Parameters
        ----------
        letter : str
            The letter to encrypt.
        verbose : bool, optional
            If True, prints the encryption process.

        Returns
        -------
        str
            The encrypted letter.

        Raises
        ------
        AssertionError
            If the letter is not a capital English letter.
        """
        assert letter in self.wiring, "Letter must be a capital english letter"
        letter_index = LETTERS.index(letter)
        if verbose:
            print(f"Encrypting {letter} to {self.wiring[letter_index]} with reflector")
        return self.wiring[letter_index]
