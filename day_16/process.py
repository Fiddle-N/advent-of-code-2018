import ast
import collections
import dataclasses
import functools
import operator
import timeit


@dataclasses.dataclass(frozen=True)
class Instructions:
    opcode: int
    a: int
    b: int
    c: int


@dataclasses.dataclass(frozen=True)
class Sample:
    before: list
    instructions: Instructions
    after: list



class DeviceVM:

    def __init__(self, samples, test_program=None):
        self.samples = samples
        self.test_program = test_program
        self.opcodes = None

    @classmethod
    def read_file(cls):
        with open('input.txt') as f:
            input_ = f.read().strip()
        raw_samples, raw_test_program = input_.split('\n\n\n\n')

        raw_samples = raw_samples.split('\n\n')
        samples = []
        for raw_sample in raw_samples:
            raw_before, raw_instrs, raw_after = raw_sample.split('\n')

            _, before_data = raw_before.split(': ')
            before = ast.literal_eval(before_data)

            instrs_data = [int(num) for num in raw_instrs.split()]
            instrs = Instructions(*instrs_data)

            _, after_data = raw_after.split(':  ')
            after = ast.literal_eval(after_data)

            samples.append(Sample(before, instrs, after))

        raw_test_program = raw_test_program.split('\n')
        test_program = []
        for raw_instrs in raw_test_program:
            instrs_data = [int(num) for num in raw_instrs.split()]
            instrs = Instructions(*instrs_data)
            test_program.append(instrs)

        return cls(samples, test_program)

    def calculate_opcodes(self, skip_opcode_resolution=False):
        total = 0
        unresolved_opcodes = collections.defaultdict(set)
        for sample in self.samples:
            possible_opcodes = set()
            for opcode, opcode_fn in self.OPCODE_FNS.items():
                exp = opcode_fn(sample.before, sample.instructions.a, sample.instructions.b, sample.instructions.c)
                if sample.after == exp:
                    possible_opcodes.add(opcode)
            if len(possible_opcodes) >= 3:
                total += 1
            unresolved_opcodes[sample.instructions.opcode] |= possible_opcodes
        if not skip_opcode_resolution:
            self.opcodes = self._resolve_opcode_results(unresolved_opcodes)
        return total

    @staticmethod
    def _resolve_opcode_results(unresolved_opcodes):
        while not all((len(name) == 1) for name in unresolved_opcodes.values()):
            initial_unresolved_opcodes = unresolved_opcodes
            resolved_names = set.union(*[names for names in unresolved_opcodes.values() if len(names) == 1])
            unresolved_opcodes = {}
            for number, names in initial_unresolved_opcodes.items():
                if len(names) == 1:
                    unresolved_opcodes[number] = names
                else:
                    unresolved_opcodes[number] = (names - resolved_names)

        resolved_opcodes = [None] * len(unresolved_opcodes)
        for number, names in unresolved_opcodes.items():
            name, = names
            resolved_opcodes[number] = name
        return resolved_opcodes

    def run_program(self):
        registers = [0, 0, 0, 0]
        for instrs in self.test_program:
            fn = getattr(self, self.opcodes[instrs.opcode])
            registers = fn(registers, instrs.a, instrs.b, instrs.c)
        return registers

    @staticmethod
    def _r(fn, input_, a, b, c):
        output = input_.copy()
        output[c] = fn(output[a], output[b])
        return output

    @staticmethod
    def _i(fn, input_, a, b, c):
        output = input_.copy()
        output[c] = fn(output[a], b)
        return output

    _addr = functools.partialmethod(_r, operator.add)
    _addi = functools.partialmethod(_i, operator.add)
    _mulr = functools.partialmethod(_r, operator.mul)
    _muli = functools.partialmethod(_i, operator.mul)
    _banr = functools.partialmethod(_r, operator.and_)
    _bani = functools.partialmethod(_i, operator.and_)
    _borr = functools.partialmethod(_r, operator.or_)
    _bori = functools.partialmethod(_i, operator.or_)

    @staticmethod
    def _setr(input_, a, b, c):
        output = input_.copy()
        output[c] = output[a]
        return output

    @staticmethod
    def _seti(input_, a, b, c):
        output = input_.copy()
        output[c] = a
        return output

    @staticmethod
    def _ir(fn, input_, a, b, c):
        output = input_.copy()
        output[c] = int(fn(a, output[b]))
        return output

    @staticmethod
    def _ri(fn, input_, a, b, c):
        output = input_.copy()
        output[c] = int(fn(output[a], b))
        return output

    @staticmethod
    def _rr(fn, input_, a, b, c):
        output = input_.copy()
        output[c] = int(fn(output[a], output[b]))
        return output

    _gtir = functools.partialmethod(_ir, operator.gt)
    _gtri = functools.partialmethod(_ri, operator.gt)
    _gtrr = functools.partialmethod(_rr, operator.gt)
    _eqir = functools.partialmethod(_ir, operator.eq)
    _eqri = functools.partialmethod(_ri, operator.eq)

    _eqrr = functools.partialmethod(_rr, operator.eq)

    @property
    def OPCODE_FNS(self):
        opcodes = [
            '_addr',
            '_addi',
            '_mulr',
            '_muli',
            '_banr',
            '_bani',
            '_borr',
            '_bori',
            '_setr',
            '_seti',
            '_gtir',
            '_gtri',
            '_gtrr',
            '_eqir',
            '_eqri',
            '_eqrr',
        ]
        return {opcode: getattr(self, opcode) for opcode in opcodes}


def main():
    dvm = DeviceVM.read_file()
    print(f'Number of samples that behave like 3 or more opcodes: {dvm.calculate_opcodes()}')
    print(f'Register 0 value after executing test program: {dvm.run_program()[0]}')


if __name__ == '__main__':
    print(f"Completed in {timeit.timeit(main, number=1)} seconds")
