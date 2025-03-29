#!/usr/bin/python3

import operator
import pprint
import time
from collections import defaultdict

OPERATORS = {
    "AND" : operator.and_,
    "OR"  : operator.or_,
    "XOR" : operator.xor
}
class Gate:
    def __init__(self, signal1:str, signal2:str, out_signal:str, operation:str):
        self.signal1 = signal1
        self.signal2 = signal2
        self.out_signal = out_signal
        self.opstring = operation
        self.operator = OPERATORS[operation]

    def get_signals(self):
        return (self.signal1, self.signal2)

    def get_out_signal(self):
        return self.out_signal

    def output(self, signal1:int, signal2:int):
        return self.operator(signal1, signal2)

    def __repr__(self):
        return f"{self.signal1} {self.opstring} {self.signal2} -> {self.out_signal}"

class Circuit:
    def __init__(self, gates:list[Gate], initial_values):
        self.gates = gates
        self.signals:dict[str, int] = initial_values.copy()
        self.relation:dict[str, list[Gate]] = self._get_relations()

    # def _initialize_signal_list(self, initial_values:dict):
    #     signal_list = initial_values.copy()
    #     signal_list.update({signal:None for gate in self.gates for signal in gate.get_signals() if signal not in signal_list})
    #     return signal_list

    def _get_relations(self):
        relations = defaultdict(lambda:list())
        for gate in self.gates:
            for signal in gate.get_signals():
                relations[signal].append(gate)
        # pprint.pprint(relations)
        return relations

    def solve(self):
        signals = self.signals.copy()
        gate_list = self.gates.copy()

        while gate_list:
            check_gates = gate_list.copy()

            for gate in gate_list:
                signal1, signal2 = gate.get_signals()

                if signal1 in signals and signal2 in signals:
                    signals[gate.get_out_signal()] = gate.output(signals[signal1], signals[signal2])
                    check_gates.remove(gate)
                    continue

            gate_list = check_gates

        z_values = {x:signals[x] for x in signals if x.startswith("z")}
        # print(z_values)
        number = sum([z_values[x] * 2**(int(x.removeprefix("z"))) for x in z_values])
        print(f"Part1: {number}")

    def create_graph(self):
        with open("mermaid.md", "w") as file:
            file.writelines(["```mermaid\n","---\n", "title: Circuit printout\n", "---\n"])
            file.write("flowchart TD\n")

            for gate in self.gates:
                sig1, sig2 = gate.get_signals()
                file.write(f"{sig1} --> {gate.get_out_signal()}\n")
                file.write(f"{sig2} --> {gate.get_out_signal()}\n")

            file.write("```\n")

def main():
    with open("day24.input", "r") as file:
        raw_signals, raw_gates = file.read().split("\n\n")

    initial_values = dict()
    for signal in raw_signals.split("\n"):
        name, value = signal.split(": ")
        initial_values[name] = int(value)

    gates = []
    for gate in raw_gates.split("\n"):
        signal1, op, signal2, output = gate.replace("->", "").split()
        gates.append(Gate(signal1, signal2, output, op))

    # pprint.pprint(gates)

    circuit = Circuit(gates, initial_values)
    circuit.solve()

    circuit.create_graph()

if __name__ == "__main__":
    main()