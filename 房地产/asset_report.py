# encoding=utf-8


class Buyer:
    index = 0
    """
    收入：
    fund: 公积金：1200
    salary: 每月工资（打到卡里的钱）：17000
    出租房收入：3000
    总收入：22000
    
    支出：
    房租：2650+265=2915
    生活费：60*30=1800
    其他：200+，500
    总支出：5215
    
    负债：
    消费贷：5940，消费贷总数：30w，利率：7%，还款方式：等额本息，贷款年限：5年
    房贷：7430，房贷总数：140w，利率：4.9%，还款方式：等额本息，贷款年限：30年
    总负债：13370
    
    结余：
    总收入-总支出-总负债=3415
    
    风险：
    失业
    房租下降
    生病
    生孩子
    
    
    收入：
    fund: 公积金：1200
    salary: 每月工资（打到卡里的钱）：17000
    出租房收入：3000
    总收入：22000
    
    支出：
    房租：2650+265=2915
    生活费：60*30=1800
    其他：200+，500
    总支出：5215
    
    负债：
    消费贷：5572，消费贷总数：15w，利率：7%，还款方式：等额本息，贷款年限：5年
    房贷：2970，房贷总数：105w，利率：4.9%，还款方式：等额本息，贷款年限：30年
    总负债：8542
    
    结余：
    总收入-总支出-总负债=8243
    
    
    收入：
    fund: 公积金：3500
    salary: 每月工资（打到卡里的钱）：20000
    出租房收入：6000
    总收入：3500 + 20000 + 6000 =29500
    
    支出：
    房租：3200+320=3520
    生活费：80*30=2400
    其他：2000
    总支出：3520 + 2400 + 2000 = 7920
    
    负债：
    消费贷：RepayUtils.average_capital_method_year(60, 0.07, 5)，消费贷总数：60w，利率：7%，还款方式：等额本息，贷款年限：5年
    房贷：RepayUtils.average_capital_method_year(260, 0.049, 30)，房贷总数：260w，利率：4.9%，还款方式：等额本息，贷款年限：30年
    总负债：RepayUtils.average_capital_method_year(60, 0.07, 5) + RepayUtils.average_capital_method_year(260, 0.049, 30)=25679
    
    结余：
    总收入-总支出-总负债=29500-8243-25679=-4422
    
    """

    def __init__(self, fund, offer_price):
        self.name = "买家" + str(Buyer.index)
        self.fund = fund
        self.offer_price = offer_price


class RepayUtils:
    @classmethod
    def average_capital_method(cls, a, b, m):
        """
        等额本息还款法
        贷款总额为A，银行月利率为β，总期数为m（个月），月还款额设为X
        """
        x = (a * b * ((1 + b) ** m)) / ((1 + b) ** m - 1)
        return x

    @classmethod
    def average_capital_method_year(cls, a, b, m):
        """
        等额本息还款法
        贷款总额为A，银行年利率为β，总期数为m（年），月还款额设为X
        """
        b = b / 12.0
        m = m * 12
        return cls.average_capital_method(a, b, m)


class CreditMoney:
    def __init__(self,
                 money,  # 总数额
                 interest,  # 年利率
                 year  # 年限
                 ):
        self.money = money
        self.interest = interest
        self.year = year

    def repay_money_per_month(self):
        return RepayUtils.average_capital_method_year(self.money, self.interest, self.year)

    def __str__(self):
        return "消费贷：{repay_money}，消费贷总数：{money}w，利率：{interest}%，还款方式：等额本息，贷款年限：{year}年".format(
            repay_money=int(self.repay_money_per_month()),
            money=self.money/10000,
            interest="%.2f" % float(self.interest*100),
            year=self.year
        )


class MyBill:
    @classmethod
    def output(cls,
               fund,  # 公积金
               salary,  # 每月工资
               rent_price,  # 出租房收入
               my_rent_price,  # 房租
               alimoney,  # 生活费
               other_money,  # 其他
               credit_consume,
               credit_house,
               ):
        in_total = fund + salary + rent_price
        out_total = my_rent_price + alimoney + other_money
        total_credit = credit_consume.repay_money_per_month() + credit_house.repay_money_per_month()
        total = in_total - out_total - total_credit
        out_str = """
        收入：
        公积金：{fund}
        每月工资（打到卡里的钱）：{salary}
        出租房收入：{rent_price}
        总收入：{in_total}

        支出：
        房租：{my_rent_price}
        生活费：{alimoney}
        其他：{other_money}
        总支出：{out_total}

        负债：
        消费贷：{credit_consume}
        房贷：{credit_house}
        总负债：{total_credit}

        结余：
        总收入-总支出-总负债：{total}
        """.format(
            fund=fund,
            salary=salary,
            rent_price=rent_price,
            in_total=in_total,
            my_rent_price=my_rent_price,
            alimoney=alimoney,
            other_money=other_money,
            out_total=out_total,
            credit_consume=credit_consume,
            credit_house=credit_house,
            total_credit=int(total_credit),
            total=int(total)
        )
        print(out_str)


if __name__ == '__main__':
    """
    收入：
    fund: 公积金：3500
    salary: 每月工资（打到卡里的钱）：20000
    出租房收入：6000
    总收入：3500 + 20000 + 6000 =29500
    
    支出：
    房租：3200+320=3520
    生活费：80*30=2400
    其他：2000
    总支出：3520 + 2400 + 2000 = 7920
    
    负债：
    消费贷：RepayUtils.average_capital_method_year(60, 0.07, 5)，消费贷总数：60w，利率：7%，还款方式：等额本息，贷款年限：5年
    房贷：RepayUtils.average_capital_method_year(260, 0.049, 30)，房贷总数：260w，利率：4.9%，还款方式：等额本息，贷款年限：30年
    总负债：RepayUtils.average_capital_method_year(60, 0.07, 5) + RepayUtils.average_capital_method_year(260, 0.049, 30)=25679
    
    结余：
    总收入-总支出-总负债=29500-8243-25679=-4422
    """
    MyBill.output(fund=3500,  # 公积金
               salary=20000,  # 每月工资
               rent_price=6000,  # 出租房收入
               my_rent_price=3520,  # 房租
               alimoney=2400,  # 生活费
               other_money=2000,  # 其他
               credit_consume=CreditMoney(
                   money=600000,
                   interest=0.07,
                   year=5
               ),
               credit_house=CreditMoney(
                   money=2600000,
                   interest=0.049,
                   year=30
               ))
