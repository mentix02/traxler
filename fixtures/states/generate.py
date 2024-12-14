#!/usr/bin/env python
from __future__ import annotations

import json
import random
from dataclasses import dataclass


@dataclass
class State:

    pk: int
    tax: int
    name: str
    code: str
    is_ut: bool = False

    def to_json(self):
        return {
            'pk': self.pk,
            'model': 'tax.State',
            'fields': {
                'tax': self.tax,
                'name': self.name,
                'code': self.code,
                'is_ut': self.is_ut,
            },
        }


STATE_CODES: list[tuple[str, str]] = [
    ('37', 'Andhra Pradesh'),
    ('12', 'Arunachal Pradesh'),
    ('18', 'Assam'),
    ('10', 'Bihar'),
    ('22', 'Chhattisgarh'),
    ('30', 'Goa'),
    ('24', 'Gujarat'),
    ('06', 'Haryana'),
    ('02', 'Himachal Pradesh'),
    ('20', 'Jharkhand'),
    ('29', 'Karnataka'),
    ('32', 'Kerala'),
    ('23', 'Madhya Pradesh'),
    ('27', 'Maharashtra'),
    ('14', 'Manipur'),
    ('17', 'Meghalaya'),
    ('15', 'Mizoram'),
    ('13', 'Nagaland'),
    ('21', 'Orissa'),
    ('03', 'Punjab'),
    ('08', 'Rajasthan'),
    ('11', 'Sikkim'),
    ('33', 'Tamil Nadu'),
    ('36', 'Telengana'),
    ('16', 'Tripura'),
    ('09', 'Uttar Pradesh'),
    ('05', 'Uttarakhand'),
    ('19', 'West Bengal'),
]

UNION_TERRITORY_CODES: list[tuple[str, str]] = [
    ('35', 'Andaman & Nicobar Islands'),
    ('04', 'Chandigarh'),
    ('26', 'Dadra & Nagar Haveli'),
    ('25', 'Daman & Diu'),
    ('07', 'Delhi'),
    ('31', 'Lakshadweep'),
    ('34', 'Puducherry'),
    ('01', 'Jammu & Kashmir'),
]


def main():
    states: list[dict] = []
    num_states = len(STATE_CODES)

    for i, (code, name) in enumerate(STATE_CODES, start=1):
        states.append(State(i, random.randint(0, 40), name, code).to_json())

    for i, (code, name) in enumerate(UNION_TERRITORY_CODES, start=1):
        states.append(State(i + num_states, 0, name, code, is_ut=True).to_json())

    json.dump(states, open('data.json', 'w+'), indent=2)


if __name__ == '__main__':
    main()
