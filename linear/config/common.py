
spinboxes_to_create = [
    {
        'name': 'amplitude',
        'label': 'Амплитуда',
        'type': float,
        'max_value': 4.5,
        'min_value': 1e-7,
        'step': 0.1,
        'default_value': 3,
    },
    {
        'name': 'number_of_pendulums',
        'label': 'Количество',
        'type': int,
        'max_value': 128,
        'min_value': 1,
        'step': 1,
        'default_value': 10
    },
    {
        'name': 'size',
        'label': 'Размер',
        'type': int,
        'max_value': 16,
        'min_value': 1,
        'step': 1,
        'default_value': 10
    },
    {
        'name': 'length',
        'label': 'Изначальная\nдлина подвеса',
        'type': int,
        'max_value': 5,
        'min_value': 0.001,
        'step': 1,
        'default_value': 4
    },
    {
        'name': 'delta_nu',
        'label': 'Разность частот',
        'type': float,
        'max_value': 250,
        'min_value': 0,
        'step': 0.05,
        'default_value': 0.1
    },
    {
        'name': 'time',
        'label': 'Стартовое время',
        'type': float,
        'max_value': 100000,
        'min_value': 0,
        'step': 0.01,
        'default_value': 0
    },
]

pendulums_default_params = {
    'time': 0,
    'length': 4,
    'amplitude': 100,
    'number_of_pendulums': 10,
    'size': 10,
    'delta_nu': 0.1,
    'delta_type_nu': 1
}
