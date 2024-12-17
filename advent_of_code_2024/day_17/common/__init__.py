"""Common methods for the Day 17"""

import os
import typing as t
from enum import Enum


class OperandEnum(Enum):
    """Operand enum."""

    LITERAL = 1
    COMBO = 2


class Computer:
    """Computer class."""

    register_a: int
    register_b: int
    register_c: int
    instructions: t.List[int]
    output: t.List[int]
    instructions_functions: t.Dict[int, t.Callable[[int], int]]

    def __init__(
        self,
        register_a: int,
        register_b: int,
        register_c: int,
        instructions: t.List[int],
    ) -> None:
        self.register_a = register_a
        self.register_b = register_b
        self.register_c = register_c
        self.instructions = instructions
        self.output = []
        self.instructions_functions = {
            0: self.__adv,
            1: self.__bxl,
            2: self.__bst,
            3: self.__jnz,
            4: self.__bxc,
            5: self.__out,
            6: self.__bdv,
            7: self.__cdv,
        }

    def __str__(self) -> str:
        return (
            f"Computer(\n"
            f"    Register A: {self.register_a}\n"
            f"    Register B: {self.register_b}\n"
            f"    Register C: {self.register_c}\n"
            f"    Instructions: {self.instructions}\n"
            ")"
        )

    def __compute_combo_operand(self, next_instruction: int) -> int:
        """Compute combo operand from next instruction.

        Args:
            next_instruction (int): Next instruction.

        Returns:
            int: The computed operand.
        """
        match next_instruction:
            case 4:
                return self.register_a
            case 5:
                return self.register_b
            case 6:
                return self.register_c
            case 7:
                raise ValueError("Invalid operand")
            case _:  # 0, 1, 2, 3
                return next_instruction

    def __compute_operand(
        self,
        next_instruction: int,
        operand_type: OperandEnum,
    ) -> int:
        """Compute operand from next instruction.

        Args:
            next_instruction (int): Next instruction.
            operand_type (OperandEnum): Operand type.

        Returns:
            int: The computed operand.
        """
        match operand_type:
            case OperandEnum.LITERAL:
                return next_instruction
            case OperandEnum.COMBO:
                return self.__compute_combo_operand(next_instruction)
            case _:
                raise ValueError("Invalid operand type")

    def __adv(self, instruction_id: int) -> int:
        """Divide A by 2^COMBO and store the result in A.

        Args:
            instruction_id (int): Current instruction ID.

        Returns:
            int: Next instruction ID.
        """
        operand: int = self.__compute_operand(
            next_instruction=self.instructions[instruction_id + 1],
            operand_type=OperandEnum.COMBO,
        )
        self.register_a = int(self.register_a / pow(2, operand))
        return instruction_id + 2

    def __bxl(self, instruction_id: int) -> int:
        """Compute XOR of B and LITERAL and store the result in B.

        Args:
            instruction_id (int): Current instruction ID.

        Returns:
            int: Next instruction ID.
        """
        operand: int = self.__compute_operand(
            next_instruction=self.instructions[instruction_id + 1],
            operand_type=OperandEnum.LITERAL,
        )
        self.register_b = int(self.register_b ^ operand)
        return instruction_id + 2

    def __bst(self, instruction_id: int) -> int:
        """Compute the modulo 8 of the COMBO and store the result in B.

        Args:
            instruction_id (int): Current instruction ID.

        Returns:
            int: Next instruction ID.
        """
        operand: int = self.__compute_operand(
            next_instruction=self.instructions[instruction_id + 1],
            operand_type=OperandEnum.COMBO,
        )
        self.register_b = int(operand % 8)
        return instruction_id + 2

    def __jnz(self, instruction_id: int) -> int:
        """Jump to another instruction if A is not zero.

        Args:
            instruction_id (int): Current instruction ID.

        Returns:
            int: Next instruction ID.
        """
        operand: int = self.__compute_operand(
            next_instruction=self.instructions[instruction_id + 1],
            operand_type=OperandEnum.LITERAL,
        )
        if self.register_a == 0:
            return instruction_id + 2
        if operand != instruction_id:
            return operand
        return instruction_id + 2

    def __bxc(self, instruction_id: int) -> int:
        """Compute B^C and store the result in B.

        Args:
            instruction_id (int): Current instruction ID.

        Returns:
            int: Next instruction ID.
        """
        self.register_b = int(self.register_b ^ self.register_c)
        return instruction_id + 2

    def __out(self, instruction_id: int) -> int:
        """Compute COMBO % 8 and store the result in the output.

        Args:
            instruction_id (int): Current instruction ID.

        Returns:
            int: Next instruction ID.
        """
        operand: int = self.__compute_operand(
            next_instruction=self.instructions[instruction_id + 1],
            operand_type=OperandEnum.COMBO,
        )
        self.output.append(operand % 8)
        return instruction_id + 2

    def __bdv(self, instruction_id: int) -> int:
        """Divide A by 2^COMBO and store the result in B.

        Args:
            instruction_id (int): Current instruction ID.

        Returns:
            int: Next instruction ID.
        """
        operand: int = self.__compute_operand(
            next_instruction=self.instructions[instruction_id + 1],
            operand_type=OperandEnum.COMBO,
        )
        self.register_b = int(self.register_a / pow(2, operand))
        return instruction_id + 2

    def __cdv(self, instruction_id: int) -> int:
        """Divide A by 2^COMBO and store the result in C.

        Args:
            instruction_id (int): Current instruction ID.

        Returns:
            int: Next instruction ID.
        """
        operand: int = self.__compute_operand(
            next_instruction=self.instructions[instruction_id + 1],
            operand_type=OperandEnum.COMBO,
        )
        self.register_c = int(self.register_a / pow(2, operand))
        return instruction_id + 2

    def run(self) -> str:
        """Run program.

        Returns:
            str: Program output.
        """
        instruction_id: int = 0
        while instruction_id < len(self.instructions) - 1:
            instruction: int = self.instructions[instruction_id]
            instructions_function = self.instructions_functions.get(instruction)
            if instructions_function is None:
                raise ValueError("Invalid instruction")
            instruction_id = instructions_function(instruction_id)
        return ",".join([str(output) for output in self.output])

    def fix_register_a(self) -> int:
        """Fix register A value so that the output
            is the same as the instructions.

        Returns:
            int: Fixed register A value.
        """
        register_a: int = pow(8, len(self.instructions) - 1)
        register_b = int(self.register_b)
        register_c = int(self.register_c)
        self.output: t.List[int] = [-1 for _ in range(len(self.instructions))]
        i: int = len(self.instructions) - 1
        changed: bool

        while i >= 0:
            changed = False

            while self.instructions[i] != self.output[i]:
                changed = True
                register_a += pow(8, i)
                self.register_a = int(register_a)
                self.register_b = int(register_b)
                self.register_c = int(register_c)
                self.output = []
                self.run()

            if changed:
                i = len(self.instructions) - 1
            else:
                i -= 1

        return register_a


def initialize_computer(
    file_name: str,
    from_file: str,
) -> Computer:
    """Initialize computer using configuration from a txt file.

    Args:
        file_name (str): Input file name.
        from_file (str): File from where the method is called.

    Returns:
        Computer: The instantiated computer.
    """
    absolute_path_to_file: str = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(from_file), file_name)
    )

    register_a: int = 0
    register_b: int = 0
    register_c: int = 0
    instructions: t.List[int] = []
    with open(absolute_path_to_file, "r", encoding="utf-8") as file_descriptor:
        for line in file_descriptor.readlines():
            if line.startswith("Register A:"):
                register_a = int(line.split(":")[1].strip())
            elif line.startswith("Register B:"):
                register_b = int(line.split(":")[1].strip())
            elif line.startswith("Register C:"):
                register_c = int(line.split(":")[1].strip())
            elif line.startswith("Program:"):
                instructions = [
                    int(x) for x in line.split(":")[1].strip().split(",")
                ]

    return Computer(
        register_a=register_a,
        register_b=register_b,
        register_c=register_c,
        instructions=instructions,
    )
