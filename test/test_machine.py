import pytest
from ..enigma_machine import EnigmaMachine


@pytest.fixture
def enigma_sender():
    return EnigmaMachine(
        rotor_wirings=[
            "BDFHJLCPRTXVZNYEIWGAKMUSQO",
            "AJDKSIRUXBLHWTMCQGZNPYFVOE",
            "EKMFLGDQVZNTOWYHXUSPAIBRCJ",
        ],
        rotor_offsets=[0, 0, 0],
        reflector_wirings="YRUHQSLDPXNGOKMIEBFZCWVJAT",
    )


@pytest.fixture
def enigma_receiver():
    return EnigmaMachine(
        rotor_wirings=[
            "BDFHJLCPRTXVZNYEIWGAKMUSQO",
            "AJDKSIRUXBLHWTMCQGZNPYFVOE",
            "EKMFLGDQVZNTOWYHXUSPAIBRCJ",
        ],
        rotor_offsets=[0, 0, 0],
        reflector_wirings="YRUHQSLDPXNGOKMIEBFZCWVJAT",
    )


def test_enigma_encryption_decryption(enigma_sender, enigma_receiver):
    original_message = "HELLO"
    encrypted_msg = enigma_sender.encrypt(original_message)
    decrypted_msg = enigma_receiver.encrypt(encrypted_msg)

    assert decrypted_msg == original_message
