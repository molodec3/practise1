from collections import deque, namedtuple

OPERATIONS = {'+', '*', '.'}

SubstrState = namedtuple('SubstrState', 'letter_count if_last_is_letter')


def process_star(given_states):
    current_state = dict()
    if given_states.get('without_last'):
        current_state['without_last'] = given_states['without_last']

    if given_states.get('with_last') is not None:
        if given_states['with_last'] != 0:
            current_state['with_last'] = SubstrState(float('inf'), True)
        else:
            current_state['with_last'] = SubstrState(0, True)
    else:
        current_state['with_last'] = SubstrState(0, True)
    return current_state


def process_plus(first_states, second_states):
    current_states = dict()
    if first_states.get('with_last') is not None and second_states.get('with_last') is not None:
        if first_states['with_last'].letter_count > second_states['with_last'].letter_count:
            current_states['with_last'] = first_states['with_last']
        else:
            current_states['with_last'] = second_states['with_last']
    elif first_states.get('with_last') is not None:
        current_states['with_last'] = first_states['with_last']
    elif second_states.get('with_last') is not None:
        current_states['with_last'] = second_states['with_last']
        
    if first_states.get('without_last') is not None and second_states.get('without_last') is not None:
        if first_states['without_last'].letter_count > second_states['without_last'].letter_count:
            current_states['without_last'] = first_states['without_last']
        else:
            current_states['without_last'] = second_states['without_last']
    elif first_states.get('without_last') is not None:
        current_states['without_last'] = first_states['without_last']
    elif second_states.get('without_last') is not None:
        current_states['without_last'] = second_states['without_last']
        
    return current_states


def process_concat(first_state_set, second_state_set):
    current_states = dict()
    if first_state_set.get('with_last') is not None:
        if second_state_set.get('with_last') is not None:
            current_states['with_last'] = SubstrState(
                first_state_set['with_last'].letter_count + second_state_set['with_last'].letter_count, True
            )

        if first_state_set.get('without_last') is not None and second_state_set.get('without_last') is not None:
            if first_state_set['with_last'].letter_count + second_state_set['without_last'].letter_count > \
                    first_state_set['without_last'].letter_count:
                current_states['without_last'] = SubstrState(
                    first_state_set['with_last'].letter_count + second_state_set['without_last'].letter_count, False
                )
            else:
                current_states['without_last'] = SubstrState(
                    first_state_set['without_last'].letter_count, False
                )
        elif first_state_set.get('without_last') is not None:
            current_states['without_last'] = first_state_set['without_last']
        elif second_state_set.get('without_last') is not None:
            current_states['without_last'] = SubstrState(
                    first_state_set['with_last'].letter_count + second_state_set['without_last'].letter_count, False
            )
    else:
        current_states = first_state_set

    return current_states


def add_letter(state_deque, element, letter):
    if element == letter:
        state_deque.append({'with_last': SubstrState(1, True)})
    elif element == '1':
        state_deque.append({'with_last': SubstrState(0, True)})
    else:
        state_deque.append({'without_last': SubstrState(0, False)})


def process_reg_exp(reg_exp, letter):
    letters_state = deque()

    for element in reg_exp:
        if element in OPERATIONS:
            if element == '*':
                if len(letters_state) < 1:
                    return 'ERROR'
                result = process_star(letters_state.pop())
                letters_state.append(result)

            else:
                if len(letters_state) < 2:
                    return 'ERROR'
                current_state = None
                second_states = letters_state.pop()
                first_states = letters_state.pop()
                if element == '+':
                    current_state = process_plus(first_states, second_states)
                elif element == '.':
                    current_state = process_concat(first_states, second_states)
                letters_state.append(current_state)
        else:
            add_letter(letters_state, element, letter)

    final_max = 0
    if len(letters_state) != 1:
        return 'ERROR'
    else:
        state = letters_state.pop()
        for element in state.values():
            if element.letter_count > final_max:
                final_max = element.letter_count

    return final_max


if __name__ == '__main__':
    reg_exp, letter = input().split()
    result = process_reg_exp(reg_exp, letter)
    if result == float('inf'):
        print('INF')
    else:
        print(result)
