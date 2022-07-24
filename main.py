BALANCE_LS = ['(((([{}]))))', '[([])((([[[]]])))]{()}', '{{[()]}}']
UNBALANCE_LS = ['}{}', '{{[(])]}}', '[[{())}]]']


class Stack:

    def __init__(self):
        self.stack = []

    def isEmpty(self):
        return len(self.stack) == 0

    def push(self, item):
        self.stack.append(item)

    def pop(self):
        if self.isEmpty():
            return None
        return self.stack.pop()

    def peek(self):
        if not self.isEmpty():
            return self.stack[-1]

    def size(self):
        return len(self.stack)

    def chek_string(self, string):
        br_pairs = {')': '(', ']': '[', '}': '{'}
        stack = Stack()

        for item in string:
            if item in br_pairs.keys() and stack.peek() == br_pairs[item]:
                stack.pop()
            else:
                stack.push(item)
        if stack.isEmpty():
            return 'Сбалансированно'
        else:
            return 'Несбалансированно'


if __name__ == '__main__':
    res = Stack()
    for i in BALANCE_LS + UNBALANCE_LS:
        print(res.chek_string(i))