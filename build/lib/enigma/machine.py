from .object import MachineObject, LETTERS, Rotor, RotorMechanism, PlugBoard, Reflector
from .configurations import ReflectorConfig, RotorConfig
from tabulate import tabulate


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
        return f"Machine instance with components: {self.config}"

    def encrypt(self, letters: str, verbose: bool = False) -> str:
        """Encrypt a letter using the configured Enigma machine.

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
        assert all(
            [l in LETTERS for l in letters]
        ), "Letter must be a capital english letter"
        encrypted_letters = ""
        for letter_ in letters:
            for component in self.config:
                letter_ = component.forward(letter_, verbose)
            encrypted_letters += letter_

        return encrypted_letters

    def get_config(self):
        table = []
        for component in self.config:
            if isinstance(component, PlugBoard):
                table.append(["PlugBoard", f"Wiring: {component.wiring}"])
            elif isinstance(component, RotorMechanism) and not component.inverse:
                table.append(["RotorMechanism", ""])
                for rotor in component.rotors:
                    table.append(
                        [
                            f"Rotor {rotor.name}",
                            f"Offset: {rotor.offset}, Wiring: {rotor.wiring}",
                        ]
                    )
            elif isinstance(component, Reflector):
                table.append(["Reflector", f"Wiring: {component.wiring}"])

        print(tabulate(table, headers=["Component", "Details"], tablefmt="grid"))


class EnigmaMachine(Machine):
    """Class representing an Enigma machine, inheriting from Machine class."""

    def __init__(
        self,
        rotor_wirings: list[str],
        rotor_offsets: list[int],
        reflector_wirings: str,
        plugboard_wirings: dict = None,
        rotor_names: list[str] = ["R", "M", "L"],
        reflector_name: str = None,
    ):
        """
        Initialize an Enigma machine.

        Parameters
        ----------
        rotor_wirings : list[str]
            List of rotor wirings.
        rotor_offsets : list[int]
            List of rotor offsets.
        reflector_wirings : str
            Reflector wiring.
        plugboard_wirings : dict, optional
            Plugboard wiring, by default None.
        rotor_names : list[str], optional
            List of rotor names, by default ["R", "M", "L"].
        reflector_name : str, optional
            Reflector name, by default None.


        Raises
        ------
        AssertionError
            If rotor_positions list is provided and doesn't have 3 elements,
            or if any rotor position is not between 1 and 26.
        """
        assert len(rotor_wirings) == len(
            rotor_offsets
        ), "Rotor wirings and offsets must have the same length"

        assert all(
            [wiring.isalpha() for wiring in rotor_wirings]
        ), "Rotor wirings must be strings"

        rotors = [
            Rotor(offset=offset, wiring=wiring, name=name)
            for offset, wiring, name in zip(rotor_offsets, rotor_wirings, rotor_names)
        ]

        rotor_mechanism = RotorMechanism(rotors=rotors)
        rotor_mechanism_inverted = RotorMechanism(
            rotors=rotors,
            inversed=True,
        )
        # Initialize Enigma machine using Machine superclass
        super().__init__(
            [
                PlugBoard(wiring=plugboard_wirings),
                rotor_mechanism,
                Reflector(wiring=reflector_wirings, name=reflector_name),
                rotor_mechanism_inverted,
                PlugBoard(wiring=plugboard_wirings),
            ]
        )

    @classmethod
    def from_configuration(
        cls,
        rotor_config: list[RotorConfig],
        rotor_offsets: list[int],
        reflector_config: ReflectorConfig,
        plugboard_wirings: dict = None,
    ):
        """
        Create a new EnigmaMachine instance from configuration settings.

        Parameters
        ----------
        rotor_config : list[RotorConfig]
            List of RotorConfig objects representing the rotor configurations.
        rotor_offsets : list[int]
            List of rotor offsets.
        reflector_config : ReflectorConfig
            ReflectorConfig object representing the reflector configuration.
        plugboard_wirings : dict, optional
            Dictionary representing the plugboard wirings,
            where keys and values correspond to connected letters,
            by default None

        Returns
        -------
        EnigmaMachine
            An instance of EnigmaMachine initialized with the provided configurations.
        """
        if not isinstance(rotor_config, list) or any(
            not isinstance(r_c, RotorConfig) for r_c in rotor_config
        ):
            raise AssertionError(
                "Rotor configurations must be a list of RotorConfig objects"
            )

        if not isinstance(reflector_config, ReflectorConfig):
            raise AssertionError(
                "Reflector configuration must be a ReflectorConfig object"
            )

        return cls(
            rotor_wirings=[r_c.wiring for r_c in rotor_config],
            rotor_offsets=rotor_offsets,
            reflector_wirings=reflector_config.wiring,
            plugboard_wirings=plugboard_wirings,
            rotor_names=[r_c.name for r_c in rotor_config],
            reflector_name=reflector_config.name,
        )
