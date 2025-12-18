import pytest

from day_19 import process


def test_program():
    program = """\
#ip 0
seti 5 0 1
seti 6 0 2
addi 0 1 0
addr 1 2 3
setr 1 0 0
seti 8 0 4
seti 9 0 5"""
    dvm = process.DeviceVM.read_input(program, debug=True)
    dvm_gen = dvm.run_program()

    op_0 = next(dvm_gen)
    assert op_0 == process.ProgramBreakpoint(
        ip=0,
        before_registers=[0, 0, 0, 0, 0, 0],
        instr=process.Instructions('seti', 5, 0, 1),
        after_registers=[0, 5, 0, 0, 0, 0]
    )

    op_1 = next(dvm_gen)
    assert op_1 == process.ProgramBreakpoint(
        ip=1,
        before_registers=[1, 5, 0, 0, 0, 0],
        instr=process.Instructions('seti', 6, 0, 2),
        after_registers=[1, 5, 6, 0, 0, 0]
    )

    op_2 = next(dvm_gen)
    assert op_2 == process.ProgramBreakpoint(
        ip=2,
        before_registers=[2, 5, 6, 0, 0, 0],
        instr=process.Instructions('addi', 0, 1, 0),
        after_registers=[3, 5, 6, 0, 0, 0]
    )

    op_3 = next(dvm_gen)
    assert op_3 == process.ProgramBreakpoint(
        ip=4,
        before_registers=[4, 5, 6, 0, 0, 0],
        instr=process.Instructions('setr', 1, 0, 0),
        after_registers=[5, 5, 6, 0, 0, 0]
    )

    op_4 = next(dvm_gen)
    assert op_4 == process.ProgramBreakpoint(
        ip=6,
        before_registers=[6, 5, 6, 0, 0, 0],
        instr=process.Instructions('seti', 9, 0, 5),
        after_registers=[6, 5, 6, 0, 0, 9]
    )

    with pytest.raises(StopIteration) as excinfo:
        next(dvm_gen)

    assert excinfo.value.value == [6, 5, 6, 0, 0, 9]
