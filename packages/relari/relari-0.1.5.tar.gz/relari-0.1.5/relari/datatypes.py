from dataclasses import dataclass

@dataclass(frozen=True, eq=True)
class LabeledDatum:
    label: str
    data: dict

    def asdict(self):
        return {
            "label": self.label,
            "data": self.data,
        }


