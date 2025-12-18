import ast
import collections
import dataclasses
import functools
import operator
import timeit


@dataclasses.dataclass(frozen=True)
class Instructions:
    opcode: str
    a: int
    b: int
    c: int


@dataclasses.dataclass(frozen=True)
class ProgramBreakpoint:
    ip: int
    before_registers: list
    instr: Instructions
    after_registers: list


class DeviceVM:

    def __init__(self, ip_register, instrs, reg_0=0, debug=False):
        self.ip_register = ip_register
        self.instrs = instrs
        self.reg_0 = reg_0
        self.debug = debug

    @classmethod
    def read_file(cls, reg_0=0):
        with open('input.txt') as f:
            return cls.read_input(f.read().strip(), reg_0)

    @classmethod
    def read_input(cls, program, reg_0=0, debug=False):
        ip_register = None
        instrs = []
        for instr_no, raw_instr in enumerate(program.splitlines()):
            if instr_no == 0:
                assert raw_instr.startswith('#ip')
                ip_register = int(raw_instr.split(' ')[1])
            else:
                opcode, *raw_io = raw_instr.split()
                io = [int(num) for num in raw_io]
                instr = Instructions(opcode, *io)
                instrs.append(instr)
        return cls(ip_register, instrs, reg_0, debug)

    def run_program(self):
        ip = 0
        registers = [self.reg_0, 0, 0, 0, 0, 0]
        iter_ = 0
        while True:
            iter_ += 1
            registers[self.ip_register] = ip
            instr = self.instrs[ip]
            fn = self.OPCODE_FNS[instr.opcode]
            next_registers = fn(registers, instr.a, instr.b, instr.c)
            if self.debug:
                yield ProgramBreakpoint(ip, registers, instr, next_registers)
            else:
                yield
            registers = next_registers
            ip = registers[self.ip_register]
            ip += 1
            if ip >= len(self.instrs):
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

    addr = functools.partialmethod(_r, operator.add)
    addi = functools.partialmethod(_i, operator.add)
    mulr = functools.partialmethod(_r, operator.mul)
    muli = functools.partialmethod(_i, operator.mul)
    banr = functools.partialmethod(_r, operator.and_)
    bani = functools.partialmethod(_i, operator.and_)
    borr = functools.partialmethod(_r, operator.or_)
    bori = functools.partialmethod(_i, operator.or_)

    @staticmethod
    def setr(input_, a, b, c):
        output = input_.copy()
        output[c] = output[a]
        return output

    @staticmethod
    def seti(input_, a, b, c):
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

    gtir = functools.partialmethod(_ir, operator.gt)
    gtri = functools.partialmethod(_ri, operator.gt)
    gtrr = functools.partialmethod(_rr, operator.gt)
    eqir = functools.partialmethod(_ir, operator.eq)
    eqri = functools.partialmethod(_ri, operator.eq)
    eqrr = functools.partialmethod(_rr, operator.eq)

    @property
    def OPCODE_FNS(self):
        opcodes = [
            'addr',
            'addi',
            'mulr',
            'muli',
            'banr',
            'bani',
            'borr',
            'bori',
            'setr',
            'seti',
            'gtir',
            'gtri',
            'gtrr',
            'eqir',
            'eqri',
            'eqrr',
        ]
        return {opcode: getattr(self, opcode) for opcode in opcodes}


def main(reg_0):
    dvm = DeviceVM.read_file(reg_0)
    dvm_gen = dvm.run_program()

    while True:
        try:
            next(dvm_gen)
        except StopIteration as e:
            results = e.value
            break

    print(f'Register 0 value after executing test program: {results[0]}')


if __name__ == '__main__':
    print(f"Completed in {timeit.timeit('main(0)', setup='from __main__ import main', number=1)} seconds")
    # print(f"Completed in {timeit.timeit('main(1)', setup='from __main__ import main', number=1)} seconds")
