# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division

import random

import otree.models
from otree.db import models
from otree import widgets
from otree.common import Currency as c, currency_range, safe_json
from otree.constants import BaseConstants
from otree.models import BaseSubsession, BaseGroup, BasePlayer
# </standard imports>

author = 'Cesar Mantilla'

doc = """
Questionnaire to apply after the experiment. In Chinese
"""


class Constants(BaseConstants):
    name_in_url = 'questionnaire_ch'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):

    # Demographic items

    year_birth = models.PositiveIntegerField(initial=None,
                            choices=range(1950, 2000),
                            verbose_name=u'年',
                            #widget=widgets.RadioSelectHorizontal()
                                             )

    month_birth = models.CharField(initial=None,
                            choices=[('Jan', u'一月'),
                                     ('Feb', u'二月'),
                                     ('Mar', u'三月'),
                                     ('Apr', u'四月'),
                                     ('May', u'五月'),
                                     ('Jun', u'六月'),
                                     ('Jul', u'七月'),
                                     ('Aug', u'八月'),
                                     ('Sep', u'九月'),
                                     ('Oct', u'十月'),
                                     ('Nov', u'十一月'),
                                     ('Dec', u'十二月'),],
                            verbose_name=u'月',
                                            )

    living_Xsh = models.CharField(initial=None,
                            choices=[('Birth', u'自出生起'),
                                     ('Other', u'后来移居到西双版纳（请注明具体的年份）'),],
                            verbose_name=u'',
                                            )

    year_Xsh = models.PositiveIntegerField(initial=None,
                                           blank=True,
                                           choices=range(1950, 2016),
                                           verbose_name=u'年',
                                             )

    gender = models.CharField(initial=None,
                              choices=[('Male', u'男'),
                                       ('Female', u'女')],
                              verbose_name=u'性别',
                              widget=widgets.RadioSelectHorizontal())

    ethnic_self = models.CharField(initial=None,
                              choices=[('Dai', u'傣'),
                                       ('Han', u'汉'),
                                       ],
                              verbose_name=u'您的民族是什么？（请选择您最有认同感的民族）',
                                    )

    relig_self = models.CharField(initial=None,
                              choices=[('Buddhist', u'佛教'),
                                       # ('Taoist', 'Taoist'),
                                       ('Christian', u'基督教（新教）'),
                                       # ('Catholic', 'Catholic'),
                                       # ('Muslim', 'Muslim'),
                                       # ('Other', 'Other (please specify)'),
                                       ('Atheist', u'无宗教信仰'),
                                       ],
                              verbose_name=u'您的宗教信仰是什么？（请选择您最有认同感的宗教信仰）',
                                    )

    urban_15 = models.CharField(initial=None,
                              choices=[('Urban', u'城市地区'),
                                       ('Rural', u'农村地区'),
                                       ('Both', u'城市、农村都生活过'),],
                              verbose_name=u'在15岁以前，您生活在城市地区还是农村地区？',
                              widget=widgets.RadioSelectHorizontal())

    marital_status = models.CharField(initial=None,
                              choices=[('Never', u'从未结过婚'),
                                       ('Married', u'已婚，第一段婚姻'),
                                       ('Married+', u'已婚，但不是第一段婚姻'),
                                       ('Cohabiting', u'未婚同居'),
                                       ('Widowed', u'丧偶'),
                                       ('Separated', u'分居（不再以配偶关系共同生活）/离异'),
                                       ('Other', u'其他'),],
                              verbose_name=u'您现在的婚姻状况是？',
                              #widget=widgets.RadioSelectHorizontal()
                                      )

    education = models.CharField(initial=None,
                              choices=[('None', u'未受正规教育'),
                                       ('Primary', u'小学'),
                                       ('Secondary', u'初中'),
                                       ('HighSchool', u'高中/中专/职高'),
                                       ('University', u'本科/大专'),
                                       ('Graduate', u'硕士/博士'),
                                       ('Professional', u'技校'),
                                       ('Other', u'其他'),
                                       ],
                              verbose_name=u'您的最高学历是？',
                              #widget=widgets.RadioSelectHorizontal()
                                 )

    hh_register = models.CharField(initial=None,
                              choices=[('Urban', u'城市户口'),
                                       ('Rural', u'农村户口'),
                                       ],
                              verbose_name=u'您现在的户籍情况是？',
                              widget=widgets.RadioSelectHorizontal())

    current_register = models.CharField(initial=None,
                              choices=[('Villager group', u'本村民小组'),
                                       ('Other Villager group', u'本村委会其他村民小组'),
                                       ('Other Committee', u'本乡（镇）其他村委会'),
                                       ('Other Village', u'本县（市）其他乡镇'),
                                       ('Other County', u'本州其他县（市）'),
                                       ('Other Prefecture', u'本省其他州（市）'),
                                       ('Other Province', u'其他省：'),
                                       ],
                              verbose_name=u'',
                              #widget=widgets.RadioSelectHorizontal()
                                        )

    other_register = models.CharField(initial=None,blank=True,
                                          verbose_name=u'如果不在“本村民小组”，请注明:',
                                          )

    health = models.CharField(initial=None,
                              choices=[('Bad', u'很差'),
                                       ('Poor', u'比较差'),
                                       ('Fair', u'一般'),
                                       ('Good', u'好'),
                                       ('Excellent', u'非常好'),
                                       ],
                              verbose_name=u'您如何评价您的身体健康状况？',
                              widget=widgets.RadioSelectHorizontal())

    satisfaction = models.PositiveIntegerField(initial=None,
                            choices=range(1, 11),
                            verbose_name=u'',
                            widget=widgets.RadioSelectHorizontal())

    employment = models.CharField(initial=None,
                              choices=[('Farmer', u'务农'),
                                       ('Employed', u'打工'),
                                       ('Self-employed', u'个体经营/企业老板'),
                                       ('Teacher', u'教师'),
                                       ('Civil_servant', u'公务员'),
                                       ('Doctor', u'医生'),
                                       ('Retired', u'退休'),
                                       ('Student', u'学生'),
                                       ('Inactive', u'待业'),
                                       ('Other', u'其他：'),
                                       ],
                              verbose_name=u'您的工作情况是？',
                              #widget=widgets.RadioSelectHorizontal()
                                  )
    #company = models.CharField(initial=None,
    #                         choices=[('Government', u'政府机关'),
    #                                   ('Gov_affiliated', u'政府下属机构'),
    #                                   ('State', u'国有企业/国有控股企业/军工企业'),
    #                                   ('Private', u'私营企业'),
    #                                   ('Collective', u'集体企业'),
    #                                   ('Foreign', u'外资企业/中外合资企业'),
    #                                   ('Individual', u'个体工商户'),
    #                                   ('Other', u'其他'),
    #                                   ],
    #                         verbose_name=u'您单位是什么性质的？',
    #                          #widget=widgets.RadioSelectHorizontal()
    #                           )

    # Items from the HTML Questions 1
    # Includes: Identification questions and reciprocity questions

    identification1 = models.PositiveIntegerField(initial=None,
                            choices=range(1, 8),
                            verbose_name=u'住在西双版纳并与您属于同一个民族的人',
                            widget=widgets.RadioSelectHorizontal())

    identification2 = models.PositiveIntegerField(initial=None,
                            choices=range(1, 8),
                            verbose_name=u'不住在西双版纳但与您是同一个民族的人',
                            widget=widgets.RadioSelectHorizontal())

    identification3 = models.PositiveIntegerField(initial=None,
                            choices=range(1, 8),
                            verbose_name=u'住在西双版纳并与您有同一种宗教信仰的人',
                            widget=widgets.RadioSelectHorizontal())

    identification4 = models.PositiveIntegerField(initial=None,
                            choices=range(1, 8),
                            verbose_name=u'不住在西双版纳但与您有同一种宗教信仰的人',
                            widget=widgets.RadioSelectHorizontal())

    belief_recipr1 = models.PositiveIntegerField(initial=None,
                            choices=range(1, 8),
                            verbose_name=u'我避免对别人不礼貌，因为我不想别人对我不礼貌。',
                            widget=widgets.RadioSelectHorizontal())

    belief_recipr2 = models.PositiveIntegerField(initial=None,
                            choices=range(1, 8),
                            verbose_name=u'我不对他人言行恶劣，因此来避免其他人对我的恶劣言行。',
                            widget=widgets.RadioSelectHorizontal())

    positive_recipr1 = models.PositiveIntegerField(initial=None,
                            choices=range(1, 8),
                            verbose_name=u'我会竭尽全力帮助那些以前对我好的人',
                            widget=widgets.RadioSelectHorizontal())

    positive_recipr2 = models.PositiveIntegerField(initial=None,
                            choices=range(1, 8),
                            verbose_name=u'我已经准备好要付出代价来帮助那些曾经帮助我的人',
                            widget=widgets.RadioSelectHorizontal())

    positive_recipr3 = models.PositiveIntegerField(initial=None,
                            choices=range(1, 8),
                            verbose_name=u'如果别人给我恩惠，我已经准备好要回报',
                            widget=widgets.RadioSelectHorizontal())

    negative_recipr1 = models.PositiveIntegerField(initial=None,
                            choices=range(1, 8),
                            verbose_name=u'如果有人让我陷入困境，我会以牙还牙',
                            widget=widgets.RadioSelectHorizontal())

    negative_recipr2 = models.PositiveIntegerField(initial=None,
                            choices=range(1, 8),
                            verbose_name=u'如果有人让我身陷险境，我会尽快报复'
                                         u'不计代价',
                            widget=widgets.RadioSelectHorizontal())

    negative_recipr3 = models.PositiveIntegerField(initial=None,
                            choices=range(1, 8),
                            verbose_name=u'如果有人冒犯了我，我也会冒犯他/她',
                            widget=widgets.RadioSelectHorizontal())

    # Items from the HTML Questions 2
    # Includes: Trust questions and questions about religious behavior

    trust1 = models.CharField(initial=None,
                              choices=[('Trusted', u'大多数人值得信任'),
                                       ('Careful', u'在与其他人打交道时必须特别小心'),
                                       ],
                              verbose_name=u'在与他人打交道时，您更同意大多数人值得信任'
                                           u'还是更同意需要特别小心？',
                              widget=widgets.RadioSelectHorizontal())

    trust2 = models.CharField(initial=None,
                              choices=[('Disagree+', u'完全不同意'),
                                       ('Disagree', u'不太同意'),
                                       ('Inbetween', u'介于两者之间'),
                                       ('Agree', u'比较同意'),
                                       ('Agree+', u'完全同意'),
                                       ],
                              verbose_name=u'请问您对“如果有机会，大多数人会想趁机占你便宜”看法 ',
                              widget=widgets.RadioSelectHorizontal())

    trust3 = models.CharField(initial=None,
                              choices=[('Disagree+', u'完全不同意'),
                                       ('Disagree', u'不太同意'),
                                       ('Inbetween', u'介于两者之间'),
                                       ('Agree', u'比较同意'),
                                       ('Agree+', u'完全同意'),
                                       ],
                              verbose_name=u'请问您对“大多数人乐于帮助他人”的看法',
                              widget=widgets.RadioSelectHorizontal())

    trust4 = models.CharField(initial=None,
                              choices=[('Never', u'从不'),
                                       ('Sometimes', u'有时'),
                                       ('Often', u'经常'),
                                       ('Always', u'总是'),
                                       ],
                              verbose_name=u'您借钱给朋友的频率是？',
                              widget=widgets.RadioSelectHorizontal())

    trust5 = models.CharField(initial=None,
                              choices=[('Disagree+', u'完全不同意'),
                                       ('Disagree', u'不太同意'),
                                       ('Inbetween', u'介于两者之间'),
                                       ('Agree', u'比较同意'),
                                       ('Agree+', u'完全同意'),
                                       ],
                              verbose_name=u'我是个可信的人',
                              widget=widgets.RadioSelectHorizontal())

    pray = models.CharField(initial=None,
                              choices=[('Yearly', u'极少/仅在特殊情况下（一年一次或几次）'),
                                       ('Monthly', u'每月一两次'),
                                       ('Weekly', u'大约一个星期一次'),
                                       ('Weekly+', u'一个星期几次'),
                                       ('Daily', u'每天'),
                                       ],
                              verbose_name=u'祷告/祈福的频率如何？',
                            )

    relig_activ = models.CharField(initial=None,
                              choices=[('Yearly', u'极少/仅在特殊情况下（一年一次或几次）'),
                                       ('Monthly', u'每月一两次'),
                                       ('Weekly', u'大约一个星期一次'),
                                       ('Weekly+', u'一个星期几次'),
                                       ('Daily', u'每天'),
                                       ],
                              verbose_name=u'您参加宗教组织/场所活动的频率如何？',
                            )

    temple = models.CharField(initial=None,
                              choices=[('Yearly', u'极少/仅在特殊情况下（一年一次或几次）'),
                                       ('Monthly', u'每月一两次'),
                                       ('Weekly', u'大约一个星期一次'),
                                       ('Weekly+', u'一个星期几次'),
                                       ('Daily', u'每天'),
                                       ],
                              verbose_name=u'您出于宗教信仰的原因去寺庙/教堂/清真寺的频率如何？',
                            )

    donation = models.CharField(initial=None,
                              choices=[('No', u'没有'),
                                       ('Yes', u'有，请注明金额（如果有物品，请折合为钱数，然后计算总数）'),
                                       ],
                              verbose_name=u'',
                            )

    donated_amount = models.PositiveIntegerField(initial=None,
                              blank=True,
                              verbose_name=u'过去十二个月内捐钱的数量（以元为单位）',
                            )

    importance_relig = models.CharField(initial=None,
                            choices=[('Important+', u'非常重要'),
                                     ('Important', u'重要'),
                                     ('Important-', u'有点重要'),
                                     ('Not important', u'不重要'),
                                     ('Not important+', u'完全不重要'),
                                    ],
                            verbose_name=u'不管您是否参加宗教活动/事宜, '
                                         u'宗教对您自己来说重要吗 ',
                            widget=widgets.RadioSelectHorizontal())

    relig_father = models.CharField(initial=None,
                              choices=[('Buddhist', u'佛教'),
                                       ('Original', u'原始宗教'),
                                       ('Taoist', u'道教'),
                                       ('Muslim', u'回教/伊斯兰教'),
                                       ('Christian', u'基督教（新教）'),
                                       ('Catholic', u'天主教'),
                                       ('Atheist', u'无宗教信仰'),
                                       ('Other', u'其他（请注明）'),
                                       ],
                              verbose_name=u'',
                                    )

    relig_father_other = models.CharField(initial=None,blank=True,
                                          verbose_name=u'其他宗教：',
                                          )

    relig_mother = models.CharField(initial=None,
                              choices=[('Buddhist', u'佛教'),
                                       ('Original', u'原始宗教'),
                                       ('Taoist', u'道教'),
                                       ('Muslim', u'回教/伊斯兰教'),
                                       ('Christian', u'基督教（新教）'),
                                       ('Catholic', u'天主教'),
                                       ('Atheist', u'无宗教信仰'),
                                       ('Other', u'其他（请注明）'),
                                       ],
                              verbose_name=u'',
                                    )

    relig_mother_other = models.CharField(initial=None,blank=True,
                                          verbose_name=u'其他宗教：',
                                          )

    marriage_religion = models.CharField(initial=None,
                              choices=[('Important+', u'非常重要'),
                                       ('Important', u'重要'),
                                       ('Important-', u'有点重要'),
                                       ('Not important', u'不重要'),
                                       ('Not important+', u'完全不重要'),
                                       ],
                              verbose_name=u'在一段婚姻中和相同宗教信仰的人结婚对您来说重要？',
                              widget=widgets.RadioSelectHorizontal())

    # Items from the HTML Family
    # Includes: Questions regarding family background

    hh_income = models.CharField(initial=None,
                              choices=[('Below1000', u'在一千元以下'),
                                       ('Below4000', u'在一千到四千元之间'),
                                       ('Below10000', u'在四千到一万元之间'),
                                       ('Below20000', u'在一万到两万元之间'),
                                       ('Below50000', u'在两万到五万元之间'),
                                       ('Above50000', u'在五万元以上'),
                                       ],
                              verbose_name=u'您家2015年平均每个月的家庭收入大概是多少？',
                                 )

    income_contribute = models.PositiveSmallIntegerField(initial=None,
                              verbose_name=u'除了您以外，有多少家庭成员的收入被算在了上述的家庭收入中？',
                                 )

    self_contribute = models.CharField(initial=None,
                              choices=[('No', u'没有'),
                                       ('Yes', u'有，请注明您贡献了多少。'),
                                       ],
                              verbose_name=u'',
                            )

    self_contrib_amount = models.PositiveIntegerField(initial=None,
                              blank=True,
                              verbose_name=u'对家庭收入的贡献',
                            )

    income_dependence = models.PositiveSmallIntegerField(initial=None,
                              verbose_name=u'除了您以外，您家有多少家庭成员依靠上述家庭收入生活？',
                                 )

    relative_wealth = models.PositiveIntegerField(initial=None,
                            choices=range(1, 11),
                            verbose_name=u'下面从1到10总共有10个数字。如果1代表您家是本村/镇最富裕的家庭，'
                                         u'10代表您家是本村/镇最贫穷的家庭，'
                                         u'客观来说，您觉得您家的经济水平在村/镇里所有家庭中位于哪个位置？',
                            widget=widgets.RadioSelectHorizontal())

    ethnic_father = models.CharField(initial=None,
                              choices=[('Dai', u'傣'),
                                       ('Han', u'汉'),
                                       ('Hani',u'哈尼族'),
                                       ('Yi',u'彝族'),
                                       ('Lahu',u'拉祜族'),
                                       ('Bulang',u'布朗族'),
                                       ('Jinuo',u'基诺族'),
                                       ('Yao',u'瑶族'),
                                       ('Miao',u'苗族'),
                                       ('Bai',u'白族'),
                                       ('Hui',u'回族'),
                                       ('Zhuang',u'壮族'),
                                       ('Wa',u'佤族'),
                                       ('Other', u'其他（请注明）'),
                                       ],
                              verbose_name=u'',
                                    )

    ethnic_father_other = models.CharField(initial=None,blank=True,
                                          verbose_name=u'其他民族：',
                                          )

    ethnic_mother = models.CharField(initial=None,
                              choices=[('Dai', u'傣'),
                                       ('Han', u'汉'),
                                       ('Hani',u'哈尼族'),
                                       ('Yi',u'彝族'),
                                       ('Lahu',u'拉祜族'),
                                       ('Bulang',u'布朗族'),
                                       ('Jinuo',u'基诺族'),
                                       ('Yao',u'瑶族'),
                                       ('Miao',u'苗族'),
                                       ('Bai',u'白族'),
                                       ('Hui',u'回族'),
                                       ('Zhuang',u'壮族'),
                                       ('Wa',u'佤族'),
                                       ('Other', u'其他（请注明）'),
                                       ],
                              verbose_name=u'',
                                    )

    ethnic_mother_other = models.CharField(initial=None,blank=True,
                                          verbose_name=u'其他民族：',
                                          )

    marriage_ethnicity = models.CharField(initial=None,
                              choices=[('Acceptable+', u'完全可以接受'),
                                       ('Acceptable-', u'比较能接受'),
                                       ('Unacceptable-', u'不太能接受'),
                                       ('Unacceptable+', u'完全不能接受'),
                                       ],
                              verbose_name=u'如果您的儿子/女儿和其他民族的人结婚，您会怎么想？',
                              widget=widgets.RadioSelectHorizontal())

    ethnic_spouse = models.CharField(initial=None,blank=True,
                              choices=[('Dai', u'傣'),
                                       ('Han', u'汉'),
                                       ('Hani',u'哈尼族'),
                                       ('Yi',u'彝族'),
                                       ('Lahu',u'拉祜族'),
                                       ('Bulang',u'布朗族'),
                                       ('Jinuo',u'基诺族'),
                                       ('Yao',u'瑶族'),
                                       ('Miao',u'苗族'),
                                       ('Bai',u'白族'),
                                       ('Hui',u'回族'),
                                       ('Zhuang',u'壮族'),
                                       ('Wa',u'佤族'),
                                       ('Other', u'其他（请注明）'),
                                       ],
                              verbose_name=u'',
                                    )

    ethnic_spouse_other = models.CharField(initial=None,blank=True,
                                          verbose_name=u'其他民族：',
                                          )

    relig_spouse = models.CharField(initial=None,blank=True,
                              choices=[('Buddhist', u'佛教'),
                                       ('Original', u'原始宗教'),
                                       ('Taoist', u'道教'),
                                       ('Muslim', u'回教/伊斯兰教'),
                                       ('Christian', u'基督教（新教）'),
                                       ('Catholic', u'天主教'),
                                       ('Atheist', u'无宗教信仰'),
                                       ('Other', u'其他（请注明）'),
                                       ],
                              verbose_name=u'',
                                    )

    relig_spouse_other = models.CharField(initial=None,blank=True,
                                          verbose_name=u'其他宗教：',
                                          )
