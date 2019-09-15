config = {
    'group1': {
        'number_of_parallel_threads': 2,
        'tasks': {
            'task1': {
                'cmd': 'sleep 5'
            },
            'task2': {
                'cmd': 'sleep 4'
            },
            'task3': {
                'cmd': 'sleep 3'
            },
            'task4': {
                'cmd': 'sleep 2'
            },
            'task5': {
                'cmd': 'sleep 1'
            },
            'performance_end': {
                'cmd': 'sleep 0',
                'dependencies': {
                    'group1': {'task1', 'task2'}
                }
            },
            'end': {
                'cmd': 'sleep 0',
                'dependencies': {
                    'group1': None
                }
            }
        }
    },
    'group2': {
        'number_of_parallel_threads': 3,
        'tasks': {
            'start': {
                'cmd': 'sleep 0',
                'dependencies': {
                    'group1': {'performance_end'}
                }
            },
            'task1': {
                'cmd': 'sleep 5'
            },
            'task2': {
                'cmd': 'sleep 4'
            },
            'task3': {
                'cmd': 'sleep 3'
            },
            'task4': {
                'cmd': 'sleep 2'
            },
            'task5': {
                'cmd': 'sleep 1'
            },
            'performance_end': {
                'cmd': 'sleep 0',
                'dependencies': {
                    'group2': {'task1', 'task2'}
                }
            },
            'end': {
                'cmd': 'sleep 0',
                'dependencies': {
                    'group2': None
                }
            }
        }
    },
    'group3': {
        'number_of_parallel_threads': 3,
        'tasks': {
            'start': {
                'cmd': 'sleep 0',
                'dependencies': {
                    'group1': {'end'},
                    'group2': {'performance_end'}
                }
            },
            'task1': {
                'cmd': 'sleep 5'
            },
            'task2': {
                'cmd': 'sleep 4'
            },
            'task3': {
                'cmd': 'sleep 3'
            },
            'task4': {
                'cmd': 'sleep 2'
            },
            'task5': {
                'cmd': 'sleep 1'
            },
            'end': {
                'cmd': 'sleep 0',
                'dependencies': {
                    'group3': None
                }
            }
        }
    },
    'end_group': {
        'number_of_parallel_threads': -1,
        'tasks': {
            'start': {
                'cmd': 'sleep 0',
                'dependencies': {
                    'group1': {'end'},
                    'group2': {'end'},
                    'group3': {'end'},
                }
            }
        }
    }
}