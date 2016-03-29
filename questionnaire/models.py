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
Questionnaire to apply after the experiment
"""


class Constants(BaseConstants):
    name_in_url = 'questionnaire'
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
                            verbose_name='Year',
                            #widget=widgets.RadioSelectHorizontal()
                                             )

    month_birth = models.CharField(initial=None,
                            choices=[('Jan', 'January'),
                                     ('Feb', 'February'),
                                     ('Mar', 'March'),
                                     ('Apr', 'April'),
                                     ('May', 'May'),
                                     ('Jun', 'June'),
                                     ('Jul', 'July'),
                                     ('Aug', 'August'),
                                     ('Sep', 'September'),
                                     ('Oct', 'October'),
                                     ('Nov', 'November'),
                                     ('Dec', 'December'),],
                            verbose_name='Month',
                                            )

    living_Xsh = models.CharField(initial=None,
                            choices=[('Birth', 'Since birth'),
                                     ('Other', 'Later (please specify year)'),],
                            verbose_name='',
                                            )

    year_Xsh = models.PositiveIntegerField(initial=None,
                                           blank=True,
                                           choices=range(1950, 2016),
                                           verbose_name='Year',
                                             )

    gender = models.CharField(initial=None,
                              choices=[('Male', 'Male'),
                                       ('Female', 'Female')],
                              verbose_name='Gender',
                              widget=widgets.RadioSelectHorizontal())

    ethnic_self = models.CharField(initial=None,
                              choices=[('Dai', 'Dai'),
                                       ('Han', 'Han'),
                                       ],
                              verbose_name='Please select the ethnicity with which you identify the most',
                                    )

    relig_self = models.CharField(initial=None,
                              choices=[('Buddhist', 'Buddhist'),
                                       # ('Taoist', 'Taoist'),
                                       ('Christian', 'Christian (Protestant)'),
                                       # ('Catholic', 'Catholic'),
                                       # ('Muslim', 'Muslim'),
                                       ('Atheist','Atheist'),
                                       # ('Other', 'Other (please specify)'),
                                       ],
                              verbose_name='Please select the confession with which you identify the most',
                                    )

    urban_15 = models.CharField(initial=None,
                              choices=[('Urban', 'Urban'),
                                       ('Rural', 'Rural'),
                                       ('Both', 'Both'),],
                              verbose_name='Before you were 15 years old, did you live in an urban area or a rural area?',
                              widget=widgets.RadioSelectHorizontal())

    marital_status = models.CharField(initial=None,
                              choices=[('Never', 'Never married'),
                                       ('Married', 'First marriage'),
                                       ('Married+', 'Married but not first marriage'),
                                       ('Cohabiting', 'Cohabiting but unmarried'),
                                       ('Widowed', 'Widowed'),
                                       ('Separated', 'Separated/Divorce'),
                                       ('Other', 'Other'),],
                              verbose_name='What is your marital status?',
                              #widget=widgets.RadioSelectHorizontal()
                                      )

    education = models.CharField(initial=None,
                              choices=[('None', 'None'),
                                       ('Primary', 'Primary school'),
                                       ('Secondary', 'Secondary school'),
                                       ('HighSchool', 'High school'),
                                       ('University', 'University degree'),
                                       ('Graduate', 'Graduate degree'),
                                       ('Professional', 'Professional degree'),
                                       ('Other', 'Other'),
                                       ],
                              verbose_name='What is the highest level of education you have completed?',
                              #widget=widgets.RadioSelectHorizontal()
                                 )

    hh_register = models.CharField(initial=None,
                              choices=[('Urban', 'Urban'),
                                       ('Rural', 'Rural'),
                                       ],
                              verbose_name='What is your current administrative status of household registration?',
                              widget=widgets.RadioSelectHorizontal())

    current_register = models.CharField(initial=None,
                              choices=[('Village', 'This village'),
                                       ('Village_Committee', 'Other village of this Village Committee'),
                                       ('Town', 'Other Village Committee of this town'),
                                       ('Autonomous_Prefecture', 'Other town of this Autonomous Prefecture'),
                                       ('Other Prefecture', 'Other Prefecture of this Province'),
                                       ],
                              verbose_name='',
                              #widget=widgets.RadioSelectHorizontal()
                                        )

    other_register = models.CharField(initial=None,blank=True,
                                          verbose_name='If it is not "this village" please specify:',
                                          )

    health = models.CharField(initial=None,
                              choices=[('Bad', 'Bad'),
                                       ('Poor', 'Poor'),
                                       ('Fair', 'Fair'),
                                       ('Good', 'Good'),
                                       ('Excellent', 'Excellent'),
                                       ],
                              verbose_name='How would you rate your health status?',
                              widget=widgets.RadioSelectHorizontal())

    satisfaction = models.PositiveIntegerField(initial=None,
                            choices=range(1, 11),
                            verbose_name='',
                            widget=widgets.RadioSelectHorizontal())

    employment = models.CharField(initial=None,
                              choices=[('Farmer', 'Farmer'),
                                       ('Worker', 'Worker'),
                                       ('Autoentrepreneur', 'Autoentrepreneur'),
                                       ('Teacher', 'Teacher'),
                                       ('Civil_servant', 'Civil servant'),
                                       ('Doctor', 'Doctor'),
                                       ('Retired', 'Retired'),
                                       ('Inactive', 'Inactive'),
                                       ('Student', 'Student'),
                                       ('Other', 'Other'),
                                       ],
                              verbose_name='What is your professional situation?',
                              #widget=widgets.RadioSelectHorizontal()
                                  )

    # company = models.CharField(initial=None,
    #                           choices=[('Government', 'Government office'),
    #                                    ('Gov_affiliated', 'Government-affiliated institution'),
    #                                    ('State', 'State owned company/Military enterprise'),
    #                                    ('Private', 'Private company'),
    #                                    ('Collective', 'Collective enterprises'),
    #                                    ('Foreign', 'Foreign company'),
    #                                    ('Individual', 'Individual business'),
    #                                    ('Other', 'Other'),
    #                                    ],
    #                           verbose_name='What is/was the administrative status of your company?',
    #                           #widget=widgets.RadioSelectHorizontal()
    #                            )

    # Items from the HTML Questions 1
    # Includes: Identification questions and reciprocity questions

    identification1 = models.PositiveIntegerField(initial=None,
                            choices=range(1, 8),
                            verbose_name='Persons of your same ethnicity living in Xishuangbanna',
                            widget=widgets.RadioSelectHorizontal())

    identification2 = models.PositiveIntegerField(initial=None,
                            choices=range(1, 8),
                            verbose_name='Persons of your same ethnicity living outside Xishuangbanna',
                            widget=widgets.RadioSelectHorizontal())

    identification3 = models.PositiveIntegerField(initial=None,
                            choices=range(1, 8),
                            verbose_name='Persons with your same confession living in Xishuangbanna',
                            widget=widgets.RadioSelectHorizontal())

    identification4 = models.PositiveIntegerField(initial=None,
                            choices=range(1, 8),
                            verbose_name='Persons with your same confession living outside Xishuangbanna',
                            widget=widgets.RadioSelectHorizontal())

    belief_recipr1 = models.PositiveIntegerField(initial=None,
                            choices=range(1, 8),
                            verbose_name='I avoid being impolite because I do not want others being impolite with me',
                            widget=widgets.RadioSelectHorizontal())

    belief_recipr2 = models.PositiveIntegerField(initial=None,
                            choices=range(1, 8),
                            verbose_name='I do not behave badly with others so as to avoid them behaving badly with me',
                            widget=widgets.RadioSelectHorizontal())

    positive_recipr1 = models.PositiveIntegerField(initial=None,
                            choices=range(1, 8),
                            verbose_name='I go out of my way to help somebody who has been kind to me before',
                            widget=widgets.RadioSelectHorizontal())

    positive_recipr2 = models.PositiveIntegerField(initial=None,
                            choices=range(1, 8),
                            verbose_name='I am ready to undergo personal costs to help somebody who helped me before',
                            widget=widgets.RadioSelectHorizontal())

    positive_recipr3 = models.PositiveIntegerField(initial=None,
                            choices=range(1, 8),
                            verbose_name='If someone does a favour for me, I am ready to return it',
                            widget=widgets.RadioSelectHorizontal())

    negative_recipr1 = models.PositiveIntegerField(initial=None,
                            choices=range(1, 8),
                            verbose_name='If somebody puts me in a difficult position, I will do the same to him/her',
                            widget=widgets.RadioSelectHorizontal())

    negative_recipr2 = models.PositiveIntegerField(initial=None,
                            choices=range(1, 8),
                            verbose_name='If I suffer a serious wrong, I will take my revenge as soon as possible, '
                                         'no matter what the costs',
                            widget=widgets.RadioSelectHorizontal())

    negative_recipr3 = models.PositiveIntegerField(initial=None,
                            choices=range(1, 8),
                            verbose_name='If somebody offends me, I will offend him/her back',
                            widget=widgets.RadioSelectHorizontal())

    # Items from the HTML Questions 2
    # Includes: Trust questions and questions about religious behavior

    trust1 = models.CharField(initial=None,
                              choices=[('Trusted', 'Most people can be trusted'),
                                       ('Careful', 'Need to be very careful'),
                                       ],
                              verbose_name='Generally speaking, would you say that most people can be trusted'
                                           ' or that you need to be very careful in dealing with people?',
                              widget=widgets.RadioSelectHorizontal())

    trust2 = models.CharField(initial=None,
                              choices=[('Disagree+', 'Totally disagree'),
                                       ('Disagree', 'Kind of disagree'),
                                       ('Inbetween', 'Inbetween'),
                                       ('Agree', 'Kind of agree'),
                                       ('Agree+', 'Totally agree'),
                                       ],
                              verbose_name='To what degree you agree that most people would try to take advantage '
                                           'of you if they got a chance?',
                              widget=widgets.RadioSelectHorizontal())

    trust3 = models.CharField(initial=None,
                              choices=[('Disagree+', 'Totally disagree'),
                                       ('Disagree', 'Kind of disagree'),
                                       ('Inbetween', 'Inbetween'),
                                       ('Agree', 'Kind of agree'),
                                       ('Agree+', 'Totally agree'),
                                       ],
                              verbose_name='To what degree you agree that most of the time people try to be helpful?',
                              widget=widgets.RadioSelectHorizontal())

    trust4 = models.CharField(initial=None,
                              choices=[('Never', 'Never'),
                                       ('Sometimes', 'Sometimes'),
                                       ('Often', 'Often'),
                                       ('Always', 'Always'),
                                       ],
                              verbose_name='How often do you lend money to friends?',
                              widget=widgets.RadioSelectHorizontal())

    trust5 = models.CharField(initial=None,
                              choices=[('Disagree+', 'Totally disagree'),
                                       ('Disagree', 'Kind of disagree'),
                                       ('Inbetween', 'Inbetween'),
                                       ('Agree', 'Kind of agree'),
                                       ('Agree+', 'Totally agree'),
                                       ],
                              verbose_name='I am trustworthy',
                              widget=widgets.RadioSelectHorizontal())

    pray = models.CharField(initial=None,
                              choices=[('Yearly', 'A couple of times per year'),
                                       ('Monthly', 'Once or twice per month'),
                                       ('Weekly', 'Around once per week'),
                                       ('Weekly+', 'Several times a week'),
                                       ('Daily', 'On a daily basis'),
                                       ],
                              verbose_name='How often do you pray?',
                            )

    relig_activ = models.CharField(initial=None,
                              choices=[('Yearly', 'A couple of times per year'),
                                       ('Monthly', 'Once or twice per month'),
                                       ('Weekly', 'Around once per week'),
                                       ('Weekly+', 'Several times a week'),
                                       ('Daily', 'On a daily basis'),
                                       ],
                              verbose_name='How often do you participate in religious activities?',
                            )

    temple = models.CharField(initial=None,
                              choices=[('Yearly', 'A couple of times per year'),
                                       ('Monthly', 'Once or twice per month'),
                                       ('Weekly', 'Around once per week'),
                                       ('Weekly+', 'Several times a week'),
                                       ('Daily', 'On a daily basis'),
                                       ],
                              verbose_name='How often do you go to temple/church/mosque because of religious belief?',
                            )

    donation = models.CharField(initial=None,
                              choices=[('No', 'No'),
                                       ('Yes', 'Yes. Please specify how much.'),
                                       ],
                              verbose_name='',
                            )

    donated_amount = models.PositiveIntegerField(initial=None,
                              blank=True,
                              verbose_name='Donation in the past 12 months (in Yuan)',
                            )

    importance_relig = models.PositiveIntegerField(initial=None,
                            choices=range(1, 6),
                            verbose_name='Regardless of whether you participate in religious activities or not, '
                                         'how would you rate religion’s importance for you from 1 being '
                                         '“very important” to 5 being “not important at all”?',
                            widget=widgets.RadioSelectHorizontal())

    relig_father = models.CharField(initial=None,
                              choices=[('Buddhist', 'Buddhist'),
                                       ('Original', 'Original religions'),
                                       ('Taoist', 'Taoist'),
                                       ('Muslim', 'Muslim'),
                                       ('Christian', 'Christian (Protestant)'),
                                       ('Catholic', 'Catholic'),
                                       ('Atheist','Atheist'),
                                       ('Other', 'Other (please specify)'),
                                       ],
                              verbose_name='',
                                    )

    relig_father_other = models.CharField(initial=None,blank=True,
                                          verbose_name='Other religion:',
                                          )

    relig_mother = models.CharField(initial=None,
                              choices=[('Buddhist', 'Buddhist'),
                                       ('Original', 'Original religions'),
                                       ('Taoist', 'Taoist'),
                                       ('Muslim', 'Muslim'),
                                       ('Christian', 'Christian (Protestant)'),
                                       ('Catholic', 'Catholic'),
                                       ('Atheist','Atheist'),
                                       ('Other', 'Other (please specify)'),
                                       ],
                              verbose_name='',
                                    )

    relig_mother_other = models.CharField(initial=None,blank=True,
                                          verbose_name='Other religion:',
                                          )

    marriage_religion = models.CharField(initial=None,
                              choices=[('Important+', 'Very important'),
                                       ('Important', 'Important'),
                                       ('Important-', 'Slightly important'),
                                       ('Not important', 'Not very important'),
                                       ('Not important+', 'Not important at all'),
                                       ],
                              verbose_name='How important is that in a marriage both spouses are from the same religion?',
                              widget=widgets.RadioSelectHorizontal())

    # Items from the HTML Family
    # Includes: Questions regarding family background

    hh_income = models.CharField(initial=None,
                              choices=[('Below1000', 'Below 1000 CNY'),
                                       ('Below4000', 'Between 1000 CNY and 4000 CNY'),
                                       ('Below10000', 'Between 4000 CNY and 10000 CNY'),
                                       ('Below20000', 'Between 10000 CNY and 20000 CNY'),
                                       ('Below50000', 'Between 20000 CNY and 50000 CNY'),
                                       ('Above50000', 'Above 50000 CNY'),
                                       ],
                              verbose_name='What is your approximate average household monthly income in 2015?',
                                 )

    income_contribute = models.PositiveSmallIntegerField(initial=None,
                              verbose_name='Excluding yourself, how many people contributed to the household income you declared above?',
                                 )

    self_contribute = models.CharField(initial=None,
                              choices=[('No', 'No'),
                                       ('Yes', 'Yes. Please specify how much.'),
                                       ],
                              verbose_name='',
                            )

    self_contrib_amount = models.PositiveIntegerField(initial=None,
                              blank=True,
                              verbose_name='Contribution to household income',
                            )

    income_dependence = models.PositiveSmallIntegerField(initial=None,
                              verbose_name='Excluding yourself, how many people live from the household income declared above?',
                                 )

    relative_wealth = models.PositiveIntegerField(initial=None,
                            choices=range(1, 11),
                            verbose_name='Below there is a scale from 1 to 10. The 1 represents the richest household '
                                         'in your town/village, and the 10 represents the poorest household in your '
                                         'town/village. On which number do you think your household is located?',
                            widget=widgets.RadioSelectHorizontal())

    ethnic_father = models.CharField(initial=None,
                              choices=[('Dai', 'Dai'),
                                       ('Han', 'Han'),
                                       ('Hani', 'Hani'),
                                       ('Yi', 'Yi'),
                                       ('Lahu', 'Lahu'),
                                       ('Bulang', 'Bulang'),
                                       ('Jinuo', 'Jinuo'),
                                       ('Miao', 'Miao'),
                                       ('Bai', 'Bai'),
                                       ('Hui', 'Hui'),
                                       ('Wa', 'Wa'),
                                       ('Zhuang', 'Zhuang'),
                                       ('Other', 'Other (please specify)'),
                                       ],
                              verbose_name='',
                                    )

    ethnic_father_other = models.CharField(initial=None,blank=True,
                                          verbose_name='Other ethnicity:',
                                          )

    ethnic_mother = models.CharField(initial=None,
                              choices=[('Dai', 'Dai'),
                                       ('Han', 'Han'),
                                       ('Hani', 'Hani'),
                                       ('Yi', 'Yi'),
                                       ('Lahu', 'Lahu'),
                                       ('Bulang', 'Bulang'),
                                       ('Jinuo', 'Jinuo'),
                                       ('Miao', 'Miao'),
                                       ('Bai', 'Bai'),
                                       ('Hui', 'Hui'),
                                       ('Wa', 'Wa'),
                                       ('Zhuang', 'Zhuang'),
                                       ('Other', 'Other (please specify)'),
                                       ],
                              verbose_name='',
                                    )

    ethnic_mother_other = models.CharField(initial=None,blank=True,
                                          verbose_name='Other ethnicity:',
                                          )

    marriage_ethnicity = models.CharField(initial=None,
                              choices=[('Acceptable+', 'Totally acceptable'),
                                       ('Acceptable-', 'Kind of acceptable'),
                                       ('Unacceptable-', 'Kind of unacceptable'),
                                       ('Unacceptable+', 'Totally unacceptable'),
                                       ],
                              verbose_name='What would you feel if your son/daughter marries a person of a different ethnic group?',
                              widget=widgets.RadioSelectHorizontal())

    ethnic_spouse = models.CharField(initial=None, blank=True,
                              choices=[('Dai', 'Dai'),
                                       ('Han', 'Han'),
                                       ('Hani', 'Hani'),
                                       ('Yi', 'Yi'),
                                       ('Lahu', 'Lahu'),
                                       ('Bulang', 'Bulang'),
                                       ('Jinuo', 'Jinuo'),
                                       ('Miao', 'Miao'),
                                       ('Bai', 'Bai'),
                                       ('Hui', 'Hui'),
                                       ('Wa', 'Wa'),
                                       ('Zhuang', 'Zhuang'),
                                       ('Other', 'Other (please specify)'),
                                       ],
                              verbose_name='',
                                    )

    ethnic_spouse_other = models.CharField(initial=None, blank=True,
                                          verbose_name='Other ethnicity:',
                                          )

    relig_spouse = models.CharField(initial=None, blank=True,
                              choices=[('Buddhist', 'Buddhist'),
                                       ('Original', 'Original religions'),
                                       ('Taoist', 'Taoist'),
                                       ('Muslim', 'Muslim'),
                                       ('Christian', 'Christian (Protestant)'),
                                       ('Catholic', 'Catholic'),
                                       ('Atheist','Atheist'),
                                       ('Other', 'Other (please specify)'),
                                       ],
                              verbose_name='',
                                    )

    relig_spouse_other = models.CharField(initial=None,blank=True,
                                          verbose_name='Other religion:',
                                          )
