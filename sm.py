from transitions import Machine


class SmBot(object):
    states = ['begin', 'order_made', 'pmt_chosen', 'end']

    def __init__(self):
        self.product = None
        self.pmt = None
        self.data = None
        self.machine = Machine(model=self, states=SmBot.states, initial='end')

        self.dialogs = {
            'Пиццy':
                [{'message': 'Какую вы хотите пиццу?  Большую или маленькую?', 'buttons': ['Большую', 'Маленькую']},
                 {'message': 'Как вы будете платить?', 'buttons': ['Картой', 'Наличными', 'Переводом']},
                 {'message': 'Вы хотите PRODUCT пиццу, оплата - PMT??', 'buttons': ['Да', 'Изменить']},
                 {'message': 'Спасибо за заказ', 'buttons': ['Сделать еще один заказ', 'До свидания!']}],
            'Кофе':
                [{'message': 'Какой вы хотите кофе?  Каппучино, Латте или Американо?',
                  'buttons': ['Каппучино', 'Латте', 'Американо']},
                 {'message': 'Как вы будете платить?', 'buttons': ['Картой', 'Наличными', 'Переводом']},
                 {'message': 'Вы хотите кофе PRODUCT, оплата - PMT?', 'buttons': ['Да', 'Изменить']},
                 {'message': 'Спасибо за заказ', 'buttons': ['Сделать еще один заказ', 'До свидания!']}]
        }

        self.machine.add_transition(trigger='next', source='begin', dest='order_made', after='choose_pmt')
        self.machine.add_transition(trigger='next', source='order_made', dest='pmt_chosen', after='confirm_order')
        self.machine.add_transition(trigger='next', source='pmt_chosen', dest='end', after='thanks',
                                    conditions=['is_yes'])
        self.machine.add_transition(trigger='next', source='pmt_chosen', dest='begin', after='choose_product',
                                    conditions=['is_no'])
        self.machine.add_transition(trigger='next', source='end', dest='begin', after='choose_product')

    def get_dialogs(self):
        return list(self.dialogs.keys())

    def set_dialog(self, dialog):
        self.dialog = self.dialogs[dialog]

    def choose_product(self, param=None):
        self.data = self.dialog[0]

    def choose_pmt(self, param=None):
        self.product = param.lower()
        self.data = self.dialog[1]

    def confirm_order(self, param=None):
        self.pmt = param.lower()
        self.data = {'message': self.dialog[2]['message'].replace('PRODUCT', self.product).replace('PMT', self.pmt),
                     'buttons': ['Да', 'Изменить']}

    def is_yes(self, param: str = None):
        return param.lower() == 'да'

    def is_no(self, param: str = None):
        return param.lower() == 'изменить'

    def thanks(self, param=None):
        self.data = self.dialog[3]
